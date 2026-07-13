# Roadmap

Phases are gated on outcomes, not dates. Dates are indicative and will be wrong.

---

## Phase 0 — Specification *(current)*

**Goal:** get the model right before writing code we cannot unwrite.

- [x] Principles, vision, governance
- [x] Data model v1.0 draft
- [x] Architecture, including the write path
- [ ] Schema formalised as JSON Schema + reference validator
- [ ] External review: geospatial, privacy, hardware-security, civic-data practitioners
- [ ] Two Stewards constituted (minimum for a meaningful federation test)

**Exit:** schema frozen at v1.0. Three independent reviewers sign off on the privacy model.

---

## Phase 1 — Single city pilot

**Goal:** prove one city, end to end, with one genuinely useful query.

- Adapters for one municipality: cadastre, procurement, planning, road maintenance, OSM extract
- Canonical store (Postgres + PostGIS), revision log, bitemporal queries
- Read-only API, bulk dumps
- 2D map + plain HTML surface. **No 3D.** 3D is a rendering problem; the data problem is harder and comes first.
- Two physical terminals in two civic offices; key issuance procedure; one complaint filed end to end

**Success criterion, stated in advance:** a working journalist uses the platform to find something they could not previously find, without our help. If that does not happen, the model is wrong and we stop and rethink rather than scaling a mistake.

---

## Phase 2 — Depth

**Goal:** make one city *complete*, not many cities shallow.

- Entity resolution at scale, with a public review queue
- Contest and response workflow, with institutional obligation to respond
- Historical backfill: the archive is the long-term value, and it starts accruing now
- Verification tiers enforced end to end
- Terminal network across all civic offices in the pilot jurisdiction
- Independent security audit of the write path — hardware, network segmentation, key issuance

---

## Phase 3 — 3D and scale

- 3D Tiles pipeline; LOD strategy that is semantic as well as geometric
- Geographic sharding; second and third city in the same jurisdiction
- Performance target: viewport passport fetch under 200ms at p95, cold cache
- Bulk dump infrastructure hardened for mirroring

---

## Phase 4 — Federation

- Federation protocol v1: discovery, cross-Steward query, mirror verification
- Second Steward operational in a different country, different legal system, different script
- Cross-border query working, and honestly slow
- Assembly constituted with real votes on real disputes

**The real test of Phase 4** is not technical. It is whether two Stewards under different governments, one of which is under political pressure, can hold a shared schema without one of them bending it.

---

## Phase 5 — Constrained AI

Only after federation is stable. Only in ingestion. Only as proposal, never as assertion. Scope per [ARCHITECTURE.md § 6](ARCHITECTURE.md#6-future-ai-integration).

- Entity resolution candidate generation
- Extraction from scanned/unstructured official documents at `machine_extracted` tier
- Anomaly flagging for human attention
- Natural-language → API query translation, with the generated query shown

---

## Explicit non-goals

| Not doing | Why |
|---|---|
| Mobile apps in Phase 1–3 | The web surface must work on a bad phone first. An app is a distribution channel, not a product. |
| A public write API | The write path is physical. This is the design. |
| Private property records beyond legally-public registries | Scope boundary. Permanent. |
| Editorial content, scoring, or rankings | [PRINCIPLES.md § Neutrality](PRINCIPLES.md#4-neutrality). |
| Real-time IoT sensor ingestion | Interesting, out of scope, and a distraction from the archive. |
| Being the map | OSM is the map. We reference it. |
