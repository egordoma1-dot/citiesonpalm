# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

This changelog tracks the **specification**. The reference implementation, once it exists, will version separately.

---

## [0.2.0] — 2026-07-23

First pilot. Documentation is unchanged; this release adds a working prototype and the findings from building it.

### Added
- **Roosevelt Island pilot** (`/prototype/roosevelt-island/`). 29 objects, 6 institutions, 2 offices, 32 sources. Single-file build (`citiesonpalm.html`) plus a split build with a pre-rendered, script-free `table.html` for the no-JS surface required by `PRINCIPLES.md` §6. Read-only; no code capable of writing.
- **`GAPS.md`** — the pilot's primary output. Construction and maintenance costs are unpublished for most researched objects. The 1955 bridge and the 1856 ruin have public construction costs; the 1976 tram and the 1975 waste network do not. The derived officeholder record is not computable for any of four RIOC presidents, because no dated, attributed project register is published.
- **`SCHEMA_NOTES.md`** — nine schema breakages. Predicted and confirmed: responsibility modelled as a property rather than a relation with a term and an instrument; no network primitive; binary public/private tenure. New and unpredicted: no type for public commitments made to secure consent or funding; the derived occupancy record is sound but starved of data; `contested` conflates three distinct situations; absence reason codes are ad hoc.

### Changed
- Serving-plane constraint: **the map may not fetch tiles from a third party.** A tile server observes every pan and zoom, which reconstructs exactly the reader-behaviour log `PRINCIPLES.md` §3 forbids the platform to hold. The pilot draws its map locally from bundled geometry and makes no external request of any kind. This makes the Phase 3 3D work materially harder than `ROADMAP.md` currently budgets for.

### Notes
- Geometry is approximate throughout — hand-placed in an island-local frame, not surveyed. No OSM or PLUTO extract was available at build time. Every geometry field is marked `confidence: approximate`.
- 7 objects are fully researched; 22 are stubs and declare themselves as such.
- Schema breakages are **not fixed**. Fixing them here would overfit the schema to one island. They feed v0.3 after a second area — a grid slice of the East Village — establishes which are general.

---

## [0.1.1] — 2026-07-13

Two changes to the trust model, both from review of 0.1.0.

### Added
- **Public issuance ledger** (`DATA_MODEL.md § 8`). Every key ever minted is published: monotonic per-office serial, issuing office, clerk pseudonym, timestamp, event type. Nothing about the citizen. Gaps, rate anomalies, and reissue farming become publicly detectable without any personal data.
- **Split trust at issuance** (`ARCHITECTURE.md § 4`). Clerk verifies the person; a tamper-evident reader derives the commitment from the document's issuer-attested value. Two-person issuance for reissues and for flagged offices.
- **Blast-radius scoping.** Compromised serial ranges receive `issuance_flag: contested_issuance`. Records survive; their weight in aggregates does not. No deletion.
- `SECURITY.md § The corrupt clerk` — full treatment, with the honest ceiling stated.

### Changed
- **Officeholder accountability model** (`DATA_MODEL.md § 3`, `PRINCIPLES.md § 2`, `FAQ.md`). 0.1.0 barred rating individuals, which was an over-correction: it made the platform unable to hold power to account. Individuals are now accountable as individuals, but **through their decisions**. Feedback attaches to a project, decision, or object and propagates upward through the responsibility chain into a **derived, reproducible** occupancy record — projects completed, late, abandoned, cost variance, responsiveness, plus what was inherited and what was bequeathed. Nobody writes to an occupancy record; it is computed from a published formula.
- Free-text commentary on a person's record remains prohibited at the schema level. The subject of a complaint cannot be `cop:occ:`.

---

## [0.1.0] — 2026-07-13

First public release. **Specification only. No production code.**

### Added

**Foundational**
- `VISION.md` — problem statement, staged success conditions, named failure modes (capture, surveillance drift, weaponisation, rot, irrelevance), rationale for the physical write path.
- `PRINCIPLES.md` — six binding principles: transparency, public accountability, privacy, neutrality, data integrity, accessibility. Explicit conflict-resolution order, privacy first.
- `GOVERNANCE.md` — federated Steward model, Assembly (one vote per Steward), Technical Steering Group, Principles Council. Four change classes up to Constitutional. Capture-and-fork as the enforcement mechanism.

**Technical**
- `ARCHITECTURE.md` — three-plane topology with asymmetric trust; serving plane has no write path to the canonical store. Ingestion adapters, append-only bitemporal revision log, geographic sharding, 3D Tiles and vector-tile serving, air-gapped civic write path, constrained AI scope.
- `DATA_MODEL.md` — object passports, institution/office/occupancy passports with hard scope boundary, containment as a labelled DAG rather than a tree, bitemporal revisions with full payloads, civic feedback with rotating epoch pseudonyms, seven verification tiers.
- `ROADMAP.md` — Phase 0 (spec) through Phase 5 (constrained AI). Phase 1 success criterion stated in advance. Explicit non-goals.

**Process**
- `CONTRIBUTING.md` — contribution types, verification tiers for data, review classes, prohibited sources.
- `SECURITY.md` — threat model by adversary class, disclosure policy, write-path physical security, residual risks stated plainly.
- `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1 plus project-specific prohibitions.
- `LICENSE.md` — AGPL-3.0 (code), ODbL 1.0 (data), CC BY-SA 4.0 (docs). DCO, no CLA.
- `README.md`, `FAQ.md`.

### Notes

- Schema is **draft**, not frozen. It will change. Do not build against it yet.
- No implementation, no adapters, no reference deployment.
- Seeking adversarial review of the privacy model and jurisdictional stress-testing of the schema. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Unreleased

### Planned for 0.2.0
- Schema formalised as JSON Schema + reference validator
- Federation protocol draft
- Address and administrative-division model validated against non-Latin-script, non-Western-ordered jurisdictions
- Key-issuance procedure specification, reviewed by hardware-security practitioners
