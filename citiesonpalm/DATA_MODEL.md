# Data Model

## 1. Identifiers

Every entity carries a **COP ID**: `cop:<type>:<jurisdiction>:<ulid>`.

```
cop:obj:no-0301:01J8XQ2M7F9K3B5N6R8T2V4W6Y
cop:inst:no-0301:01J8XQ4P2C1D8E3F7G9H0J2K4L
```

Stable forever. Never reused. Never reassigned. If an object is demolished, its ID persists with a terminal revision; the ID is a handle on a *history*, not on a physical thing.

Source-native identifiers (cadastral number, OSM ID, procurement reference) are retained as `external_ids` — a set, not a field, because one object routinely has many.

---

## 2. Object passport

The core record. Every physical object of public consequence.

```yaml
id: cop:obj:no-0301:01J8XQ2M7F9K3B5N6R8T2V4W6Y
type: bridge                    # controlled vocabulary
schema_version: 1.0

names:
  - { value: "Ankerbrua", lang: no, role: official }
  - { value: "Anchor Bridge", lang: en, role: exonym }

geometry:
  crs: EPSG:4326
  shape: { type: LineString, coordinates: [...] }
  elevation_m: 12.4
  footprint_m2: 1840
  confidence: surveyed          # surveyed | derived | approximate

containment:                    # NOT a single parent — see §4
  - { relation: located_on, target: cop:str:no-0301:... }
  - { relation: within, target: cop:dist:no-0301:... }
  - { relation: within, target: cop:dist:no-0301:... }   # spans two districts

lifecycle:
  status: in_service            # planned | under_construction | in_service
                                # | under_renovation | decommissioned | demolished
  commissioned: 1926-10-14
  design_life_years: 100
  last_inspection: 2029-04-02

ownership:
  owner: cop:inst:no-0301:...   # public body or legal entity — never a natural person
  tenure: public
  transferred_from: cop:inst:no:...
  transferred_on: 2011-01-01

responsibility:                 # who is accountable, now
  maintainer: cop:inst:no-0301:...
  regulator: cop:inst:no:...

finance:
  construction_cost:
    amount: 4200000
    currency: NOK
    year: 1926
    normalised_eur_2025: 18400000
    confidence: low             # historical conversion — say so
    source: cop:src:...
  annual_maintenance:
    amount: 210000
    currency: NOK
    year: 2029

projects:                       # planned and in-flight work
  - id: cop:proj:no-0301:...
    title: "Deck resurfacing and railing replacement"
    status: approved
    approved_on: 2029-11-20
    scheduled: { start: 2030-04-01, end: 2030-09-30 }
    budget: { amount: 31000000, currency: NOK }
    contractor: cop:org:no:...
    tender: cop:src:...          # link to the procurement record
    milestones:
      - { name: "Contract awarded", planned: 2030-01-15, actual: 2030-02-03 }

attributes:                     # type-specific, schema-validated per type
  span_m: 148
  lanes: 4
  load_rating_t: 60

provenance:
  sources: [ cop:src:..., cop:src:... ]
  verification: authoritative   # see §7
  completeness: 0.78            # fraction of expected fields populated

revision:
  id: 8f3a...                   # content hash
  parent: 1c92...
  valid_from: 2029-11-20
  recorded_at: 2029-11-24T09:12:03Z
```

**Absent fields are declared absent.** A missing cost is `{ status: unknown, reason: not_published }` — not silence. Silence is indistinguishable from zero, and the difference matters.

---

## 3. Institution & office passports

Two distinct record types. Conflating them is the most common modelling error we expect.

**Institution** — the body. Durable across the people who staff it.

```yaml
id: cop:inst:no-0301:...
type: municipal_department
name: "Oslo Bymiljøetaten"
mandate: "Maintenance of public roads, parks, and urban environment."
jurisdiction: cop:dist:no-0301:*      # spatial + functional scope
parent: cop:inst:no-0301:...
budget:
  - { year: 2030, allocated: 4.1e9, spent: 3.87e9, currency: NOK, source: cop:src:... }
responsible_for: [ ... ]              # inverse of object.responsibility
legal_basis: cop:src:...              # the statute that creates it
```

**Office** — the seat. **Occupancy** — the person in it, for a period.

```yaml
id: cop:office:no-0301:...
title: "Byrådsleder (Governing Mayor)"
institution: cop:inst:no-0301:...
powers: [ budget_proposal, executive_appointment, ... ]
term_length_years: 4

occupancies:
  - id: cop:occ:no-0301:...
    person_name: "..."                # public name only
    from: 2027-10-25
    to: null
    source: cop:src:...               # official appointment record

    # DERIVED — never written directly. Computed from projects and decisions
    # whose responsibility chain intersects this office during this term.
    record:
      projects_under_authority: [ cop:proj:no-0301:..., ... ]
      inherited: [ cop:proj:no-0301:... ]      # began before `from`
      bequeathed: [ cop:proj:no-0301:... ]     # unfinished at `to`
      decisions: [ cop:dec:no-0301:..., ... ]
      aggregates:                              # computed, reproducible, no editorial weighting
        projects_completed_on_schedule: 11
        projects_completed_late: 6
        projects_abandoned: 2
        median_cost_variance: +0.34
        complaints_responded_within_statutory_period: 0.61
      method: cop:doc:aggregation-v1           # the published formula
```

**The occupancy record is a derived view, not an editable one.** Nobody writes to it. It is computed from the projects and decisions whose responsibility chain intersects that office during that term, using a published, reproducible method. Two people running the computation independently must get the same numbers, or it is a bug.

This is how an individual is held to account here. Not with a star rating typed at them, but with the sum of what happened under their authority — including what they inherited and what they left unfinished, because the dates say so and the DAG says so. A governor who took over a failing project shows as inheriting it. A governor who left one half-built shows as bequeathing it. Responsibility is usually shared, and every party in the chain — commissioning office, approving council, delivering department, contractor — is attributed.

**No free-text commentary on the occupancy record.** Complaints and ratings are filed against a **project, decision, or object** ([§6](#6-civic-feedback)) — a concrete thing with a date, a budget, and a documented chain of responsibility. They propagate *upward* into the occupancy aggregate through that chain. They do not attach to the person directly.

The distinction is load-bearing:

- A complaint attached to a person invites "I don't like him."
- A complaint attached to a project invites "this cost 3× estimate and finished two years late" — which is checkable, contestable, and survives a defamation suit.

The second is more damaging to a bad official than the first, because it is specific. The first is just noise that discredits the platform.

**Hard scope boundary.** An occupancy record contains: public name, office, term, and the derived record of decisions and projects under that authority. It contains nothing else. Not a home address, not a family, not a biography, not private finances, not a photograph beyond an official portrait, not a movement, and not a comment section. These fields do not exist in the schema and cannot be added without a Constitutional change ([GOVERNANCE.md § 3](GOVERNANCE.md#3-change-classes)) — a process designed to make that addition impossible to sneak through.

The first time an official's passport contains someone's home address, the project is over. The schema is the defence, not moderation.

---

## 4. The hierarchy

```
World → Country → Region → City → District → Street → Object
```

Read as the intended *reading* order. It is **not** a strict tree in the data.

- An object may sit in multiple districts (a bridge across a boundary).
- A street may cross districts and change name mid-way.
- Jurisdictions overlap: a water utility's service area does not respect municipal borders, and a national heritage regulator has authority over a specific building inside a city it otherwise does not govern.

So containment is a **labelled DAG of edges**, not a parent pointer:

| Edge | Meaning |
|---|---|
| `within` | Geometric containment, possibly multiple |
| `located_on` | Object → Street |
| `governs` | Institution → spatial extent (may overlap other institutions) |
| `responsible_for` | Institution → object (functional, ignores geometry) |
| `adjacent_to` | Spatial neighbour |
| `supersedes` | This object replaced that one |

Queries name the edge they traverse. "What is in this district" and "who is responsible for what is in this district" are different traversals and routinely produce different answers — which is itself an accountability finding worth surfacing.

---

## 5. Revisions

Append-only. Content-addressed. Bitemporal.

```
revision {
  id, object_id, parent,
  payload,                      # full state after the change (not a diff)
  change_summary,               # machine-generated field-level diff, for display
  provenance { source, adapter, adapter_version, verification },
  valid_from,                   # when it became true in the world
  recorded_at,                  # when we learned it
  author                        # ingestion run ID, or terminal write receipt
}
```

Full payloads, not diffs. Storage is cheap; reconstructing state by replaying ten thousand diffs across a schema migration is not.

**Bitemporality.** `valid_from` and `recorded_at` are independent. This lets us answer both "what was true in March 2030" and "what did we *believe* in March 2030" — and the gap between those two is often the story.

**Nothing is deleted.** A withdrawn record is tombstoned: `status: withdrawn`, with a reason and an authority, still readable. Hard deletion happens only under legal order, is itself logged as a public event, and the *fact* of removal is never concealed.

---

## 6. Civic feedback

Written only through the physical terminal path ([ARCHITECTURE.md § 4](ARCHITECTURE.md#4-the-write-path)).

```yaml
id: cop:fb:no-0301:...
kind: complaint                # complaint | rating | contest
subject: cop:proj:no-0301:...  # project | decision | object | institution
                               # NOT an occupancy. Never a person.
handle: "K. Nordmann"          # self-chosen; may be a nickname or absent
epoch_pseudonym: a91f...       # rotating; enables per-epoch Sybil detection only
body: "..."                    # complaint text; ratings carry a scalar
receipt: { terminal, jurisdiction, ts, signature, key_serial: no-0301-004417 }
status: open                   # open | acknowledged | resolved | rejected
responses: [ ... ]             # institutional replies, themselves revisions
issuance_flag: null            # set to `contested_issuance` if the issuing
                               # office is later found compromised — see §8
```

**Subject must be a thing, not a person.** The schema will not accept `cop:occ:` as a subject. Feedback lands on a project, a decision, an object, or an institution, and **propagates upward** through the responsibility chain into the aggregates of every occupancy that authority passed through. That is how an individual's record accumulates: through what they did, attributed by date and by chain.

`contest` is how a citizen disputes a record. It does not overwrite the record. It attaches a contest, marks the record `contested`, and obliges the responsible institution to respond or be visibly non-responsive — which is itself published, and which itself lands in the responsiveness aggregate of whoever held the office.

`epoch_pseudonym` rotates per jurisdiction epoch. Within an epoch, ten complaints from one key are detectable as one key. Across epochs, no permanent per-person history accumulates. This is deliberate: Sybil resistance without building a dossier.

---

## 7. Verification tiers

Every record carries one. It is the single most important field for a downstream user deciding whether to trust a number.

| Tier | Meaning |
|---|---|
| `authoritative` | Direct feed from the system of record (cadastre, procurement portal), cryptographically or contractually attested. |
| `official_document` | Extracted from a published official document; source URI retained. |
| `cross_referenced` | Two or more independent non-authoritative sources agree. |
| `single_source` | One non-authoritative source. |
| `machine_extracted` | Produced by OCR/NLP from unstructured source. Never promoted without human review. |
| `contributed` | Human contribution, not yet corroborated. |
| `contested` | Actively disputed; positions and evidence both shown, not adjudicated. |

Tiers never silently upgrade. A promotion is a revision, with an author and a reason, like everything else.

---

## 8. The issuance ledger

Every key ever minted is a public record. This is the primary defence against the corrupt clerk ([SECURITY.md](SECURITY.md#the-corrupt-clerk)).

```yaml
id: cop:key:no-0301:...
serial: no-0301-004417         # monotonic, per office, never reused
office: cop:inst:no-0301:...   # the issuing office
clerk: c7f2a1                  # clerk pseudonym — stable per office per epoch
event: issue                   # issue | reissue | void
at: 2030-03-14T11:02:19Z
reissue_of: no-0301-003980     # for reissues; null otherwise
void_reason: damaged           # for voids; null otherwise
```

**The citizen side of this record is empty and stays empty.** No name, no document number, no address, no hash of any of those. The ledger records that *a* key was issued, by whom, when, and with what number. It does not record to whom. That fact does not exist anywhere in the platform.

**What the serial gives us, for free:**

| Signal | Detection |
|---|---|
| Ghost keys | Serials are monotonic per office. A gap is a key minted and never accounted for. The office answers publicly, or does not. |
| Clerk anomaly | Serials 4,401–4,830 in one week, one clerk pseudonym, against an office median of 40/week. Visible without knowing a single citizen's identity. |
| Reissue farming | Reissue rate per clerk, published. A Sybil operation shows up as an implausible loss rate. |
| Blast radius | If a range is later found fraudulent, flag exactly that range. No guessing, no over-deletion. |

**Clerk pseudonyms, not clerk names.** The public needs to see that *one clerk* did this — not who they are. A pseudonym is stable within an office and epoch, which is all that anomaly detection requires. It resolves to a named person only through the office's own oversight body, under process. Publishing civic staff names turns them into targets, which is the same harassment failure the occupancy model exists to avoid ([§3](#3-institution--office-passports)).

**Compromised issuance does not delete writes.** If an office or a serial range is found compromised, affected feedback records receive `issuance_flag: contested_issuance` from that finding forward. The record survives — append-only means append-only. Its weight in aggregates does not. The finding itself is a public revision, with an author and a date, like everything else.
