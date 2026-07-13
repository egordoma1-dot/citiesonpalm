# Architecture

## 1. Overview

The system is split into three planes with strictly asymmetric trust:

```
  ┌───────────────────────────────────────────────────────────┐
  │  INGESTION PLANE (semi-trusted, automated)                │
  │  Adapters → Normaliser → Validator → Staging              │
  └────────────────────────┬──────────────────────────────────┘
                           │  write (batch, signed)
                           ▼
  ┌───────────────────────────────────────────────────────────┐
  │  CANONICAL STORE (trusted, append-only)                   │
  │  Revision log · Object graph · Spatial index              │
  └───────┬─────────────────────────────────▲─────────────────┘
          │  one-way replication            │  write (physical only)
          ▼                                 │
  ┌───────────────────────┐        ┌────────┴──────────────────┐
  │  SERVING PLANE        │        │  CIVIC WRITE PATH         │
  │  (untrusted, public)  │        │  (air-gapped terminals)   │
  │  READ ONLY            │        │  Complaints · Ratings     │
  │  API · Tiles · 3D     │        │  Contests                 │
  └───────────────────────┘        └───────────────────────────┘
```

The single most important property: **the serving plane has no write path to the canonical store.** Not a restricted one — none. There is no code in the serving plane that constructs a write. Full compromise of every public-facing host yields a read-only replica and nothing else.

Replication is one-way and physically enforced (data diode or equivalent unidirectional gateway) at the canonical→serving boundary.

---

## 2. Ingestion plane

The primary source of data is **institutional systems**, not volunteers. Volunteer contribution matters but does not scale to the built environment of a continent; automated ingestion does.

**Adapters** are per-source, open-source, independently runnable connectors. One adapter per (jurisdiction, system) pair: a cadastral registry, a procurement portal, a utility asset database, a planning-permission feed, an OpenStreetMap extract.

Each adapter emits a stream of **source records** with mandatory provenance: source ID, retrieval timestamp, source document URI, source-native identifier, adapter version, and a content hash of the raw payload. The raw payload is retained verbatim and immutably; the normalised record must always be re-derivable from it. If our normaliser has a bug, we fix the normaliser and reprocess — we never lose the original.

**Normaliser** maps source-native shapes into the passport schema ([DATA_MODEL.md](DATA_MODEL.md)). This is where the hard, unglamorous work lives: reconciling address formats, resolving that "Dept. of Public Works" and "Public Works Department" are one entity, matching a procurement contract to the physical object it built.

**Validator** enforces schema, referential integrity, geometry validity, and plausibility rules (a bridge built in 1300 with a cost in euros is flagged). Failures do not silently drop; they enter a public rejection queue with a machine-readable reason.

**Entity resolution** is explicit and reviewable. Automatic merges above a confidence threshold; below it, a human review queue. Every merge is itself a revision, and every merge is reversible by a subsequent revision.

---

## 3. Canonical store

**Revision log.** An append-only, content-addressed log. Each revision is:

```
revision {
  id           : hash(canonical_serialisation)
  object_id    : stable identifier of the subject
  parent       : id of the revision this supersedes (null for genesis)
  payload      : the passport state after this change
  provenance   : source, adapter, verification tier, ingested_at
  valid_from   : when the fact became true in the world
  recorded_at  : when we learned it
  author       : ingestion run, or terminal-issued write receipt
}
```

**Bitemporality is mandatory.** `valid_from` (world time) and `recorded_at` (system time) are separate and both indexed. This is not a nicety. Without it you cannot answer "what did the city *believe* the budget was in March, before the revision landed in June?" — which is precisely the question that matters when investigating a discrepancy.

**Object graph.** A materialised current-state view over the log, plus edges: `contains`, `adjacent_to`, `responsible_for`, `funded_by`, `supersedes`, `located_on`. The hierarchy (Object → Street → District → City → Region → Country → World) is a set of `contains` edges, not a rigid tree — because the world is not a tree. A bridge spans two districts. A river is a border. Objects may have multiple parents at the same level; queries specify which containment relation they traverse.

**Storage.** PostgreSQL + PostGIS as the reference implementation for the graph and spatial index. The revision log is an append-only table plus an object-store archive of payloads and raw source documents. This choice is boring on purpose; boring survives.

**Scale.** Assume 10^10 objects globally, 10^11 revisions over decades. Sharding is geographic — by jurisdiction, then by a spatial cell (S2/H3) within it. Geographic sharding is chosen because it matches both the query pattern (viewport-bounded) and the political reality (a national steward operates its own shard). Cross-shard queries go through a federation layer and are explicitly slower; we accept that.

---

## 4. The write path

Civic writes — complaints, ratings, contests of a record — do not traverse the internet.

**Terminal.** A fixed workstation inside a public civic office. No wireless hardware: no Wi-Fi radio, no Bluetooth, no cellular modem — physically absent, not disabled in software. Its only interface is a wired link to a local switch on an isolated network segment. The segment carries port-based authentication (802.1X + MACsec, or equivalent) so that an unenrolled physical device gains nothing by plugging into a socket.

**Key.** A hardware security token. Issued in person by a civic clerk. The clerk verifies a government identity document, confirms it belongs to the presenting person, and enrols one key. **The clerk does not record the document's contents into the platform.** No name, no number, no address, no phone, no email enters the system. What the platform stores is a one-way commitment — a salted hash of the identity-document identifier under a jurisdiction-held key — sufficient to answer exactly one question: *does this person already have a key?* It cannot be reversed to a person by the platform, and the platform never sees the input.

One person, one key, at a time. Losing a key costs a fee and a reissue delay measured in weeks; the delay is a feature, because instant reissue is a Sybil factory.

**Split trust at issuance.** The clerk verifies the person against the document — a human judgement, and it stays human. A tamper-evident reader, not the clerk, derives the commitment from the document's issuer-attested value. The clerk cannot hand-key the input, which means a clerk cannot invent a citizen without forging a passport. Reissues, and any issuance in an office already flagged for anomalous rates, require two clerks on different shifts.

**Issuance is public.** Every key minted is a public ledger record — serial (monotonic per office, never reused), office, clerk pseudonym, timestamp, event type. Nothing about the citizen. Schema in [DATA_MODEL.md § 8](DATA_MODEL.md#8-the-issuance-ledger); threat treatment in [SECURITY.md § The corrupt clerk](SECURITY.md#the-corrupt-clerk).

**Session.** Insert key → terminal boots into the civic application only → user performs their action → key removed → session destroyed. The user may attach any handle to their key: real name, nickname, acronym, nothing. The system does not care and cannot verify it. The handle is a label, not an identity.

**Receipt.** A write produces a signed receipt. It carries: the terminal ID, the jurisdiction, a timestamp, the write's content hash, and a signature from the key. It does **not** carry the key's identity commitment, and receipts are not linkable to each other across time by anyone but the key holder — a rotating pseudonym derived from the key and the jurisdiction epoch is used, so that Sybil detection is possible within an epoch without building a permanent per-person history.

**Transfer.** Batches of receipts move from the isolated segment to the canonical store by controlled physical transfer or unidirectional gateway, signed by the terminal's hardware key. The write network has no route to the internet in either direction.

**Why.** An attacker who owns the entire internet-facing estate cannot forge one complaint. To forge one, they must physically enter an office and present a genuine identity document. Forging one is expensive; forging ten thousand is an operation that cannot be run quietly. Rationale in [VISION.md § Why the write path is physical](VISION.md#why-the-write-path-is-physical); costs in [FAQ.md](FAQ.md).

---

## 5. Serving plane

Read-only. Stateless. Fully cacheable. Assume it is hostile territory and design so that its compromise is boring.

- **API.** Read-only REST + a constrained GraphQL surface. No auth, no keys, no rate-limit-by-identity (rate limiting is by IP and is coarse; we would rather serve an abusive scraper than fingerprint a reader). Bulk dumps published on a fixed schedule so that scraping is unnecessary.
- **Tiles.** Vector tiles (MVT) for 2D. Passport data is *not* baked into tiles; tiles carry geometry and object IDs, and the client fetches passports separately. This keeps tiles cacheable forever and passports fresh.
- **3D.** 3D Tiles (OGC) with hierarchical LOD. The globe is a client of the same data, not a special case. Level-of-detail is semantic as well as geometric: at country zoom the client is fetching institution passports, not building meshes. The 3D client is one renderer; the 2D map, the HTML tables, and the JSON API are peers, not fallbacks ([PRINCIPLES.md § Accessibility](PRINCIPLES.md#6-accessibility)).
- **No telemetry.** No analytics scripts, no third-party fonts or CDNs, no request logs retained beyond ephemeral operational counters. There is nothing to leak because there is nothing collected.

---

## 6. Future AI integration

Constrained, and constrained in a specific direction: **AI may propose; it may not assert.**

Permitted, in the ingestion plane only:
- Entity resolution candidate generation (proposals into a human review queue).
- Anomaly detection — flagging a revision whose cost is three standard deviations from comparable objects, for human attention.
- Extraction from unstructured sources (scanned planning documents, PDF minutes) into candidate records, tagged with a low verification tier and always linked to the source page.
- Natural-language query translation into the existing query API, executed transparently, with the generated query shown to the user.

Forbidden:
- Writing a revision at any tier above `machine_extracted` without human confirmation.
- Any inference presented as record. A model's guess at a construction cost is not a cost; it is a guess, and it does not enter the passport.
- Any ranking, scoring, or summarisation of institutions or officials. This is [PRINCIPLES.md § Neutrality](PRINCIPLES.md#4-neutrality), and it is not negotiable.
- Any model in the serving path that could personalise output. Two readers requesting the same object receive byte-identical responses.

---

## 7. Scalability strategy

| Dimension | Approach |
|---|---|
| Read volume | Static-cacheable everything; CDN; bulk dumps to remove scraping pressure. |
| Data volume | Geographic sharding; cold revisions to object storage; hot current-state in Postgres. |
| Write volume | Structurally bounded by physical terminals. This is the one axis we are not worried about. |
| Jurisdictions | Federation: each national steward runs its own canonical store, conforming to the shared schema. There is no central store; there is a shared schema and a discovery layer. |
| Schema evolution | Versioned schemas, additive-by-default, migrations published as code, old revisions never rewritten — they are read through a compatibility layer. |

Federation is the scalability answer *and* the governance answer: a system with no central store cannot be captured by seizing the centre. See [GOVERNANCE.md](GOVERNANCE.md).
