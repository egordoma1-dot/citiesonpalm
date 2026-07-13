# Governance

## 1. Design goal

Governance exists to answer one question: **when this project becomes worth capturing, what stops it being captured?**

A civic accountability platform that succeeds will, by construction, hold data that powerful people would prefer altered or removed. Assume the pressure. Design for it.

Four defences:

1. **No centre to seize.** Federated stewardship; no single canonical store.
2. **No single point of decision.** Schema and principle changes require supermajority across independent stewards.
3. **Forkability as a live threat.** Open licences and continuous bulk dumps mean a captured steward loses the data rather than controlling it.
4. **Immutability.** Even a fully captured steward cannot quietly rewrite history; they can only append, and appends are visible.

---

## 2. Structure

**Stewards.** Each jurisdiction (typically national) is operated by a Steward: a legally independent non-profit entity running a canonical store for its territory, conforming to the shared schema. Stewards hold their own data. There is no central database. There is a shared schema, a discovery layer, and a federation protocol.

**The Assembly.** All Stewards, one vote each, regardless of size. Norway and India have equal votes. This is intentional: weighting by population or data volume would hand control to whoever has the most cities, which is exactly the concentration we are avoiding.

**Technical Steering Group (TSG).** 5–9 members, elected by the Assembly for staggered two-year terms. Owns the reference implementation, schema, and protocol. Cannot change Principles.

**Principles Council.** 7 members. Sole custodian of [PRINCIPLES.md](PRINCIPLES.md). Deliberately hard to constitute and deliberately slow. Membership is barred to anyone holding public office, employed by a government body, or employed by a company deriving material revenue from public procurement in a participating jurisdiction — during their term and for two years after.

---

## 3. Change classes

| Class | Examples | Requires |
|---|---|---|
| **Routine** | Bug fix, adapter, docs, additive optional field | TSG lazy consensus, 72h |
| **Substantial** | New object type, new edge type, API change, LOD strategy | TSG vote + 14-day public comment |
| **Breaking** | Schema major version, federation protocol, identifier format | Assembly 2/3 + 30-day comment + published migration path |
| **Constitutional** | Any change to PRINCIPLES.md, scope boundary, or write-path model | Principles Council unanimous **and** Assembly 3/4 **and** 90-day public comment **and** a published dissent record |

The Constitutional bar is set at a height where legitimate change is possible and quiet change is not. If a scope expansion into private individuals is ever proposed, it must survive 90 days of daylight and near-unanimity. That is the mechanism.

---

## 4. Data governance

**Ingestion.** Any Steward may add adapters for sources in its jurisdiction without Assembly approval. Adapters are open-source and auditable; a Steward that ingests from an unpublished or unattributed source is in breach.

**Takedowns.** Legal orders are honoured where legally binding, and:
- The removal is logged as a public event.
- The *fact* of removal, the ordering authority, and the legal basis are published.
- The order itself is published where publishing it is lawful; where it is not, that constraint is published.
- Other Stewards are notified and are **not** obliged to remove. A takedown in one jurisdiction does not propagate.

**Warrant canary.** Each Steward maintains one, signed, on a fixed schedule.

**Correction, not deletion.** An entity that believes a record is wrong files a contest, which is published alongside the record. Being contested is public. Being wrong is public. Removal is not the remedy for either.

---

## 5. Conflict of interest

- Every TSG and Council member publishes an interests declaration, updated annually.
- Steward funding sources are published in full, per year, per source.
- No Steward may accept funding constituting more than 25% of its annual budget from any single government body, or more than 10% from any entity holding public contracts in its jurisdiction.
- A Steward that breaches funding limits is suspended from the Assembly until remedied. Its data remains published — the point is to remove its *vote*, not the public record.

---

## 6. Capture and forking

The fork is not a failure mode. It is the enforcement mechanism.

All data is licensed ODbL and published as bulk dumps on a fixed schedule, mirrored by other Stewards. If a Steward is captured — by a government, a party, or a funder — the following happens by design:

1. The captured Steward's records diverge from its mirrors. The divergence is detectable, because everything is content-addressed and mirrors are continuous.
2. The Assembly may suspend the Steward by simple majority.
3. A successor Steward is constituted and adopts the last-known-good state from the mirrors.
4. The captured store keeps serving. It just stops being the one anyone federates with.

This project is designed so that its own institution can die without the record dying. If Cities On Palm as an organisation is corrupted, the correct outcome is that someone forks it and continues. Everything in this repository — the licences, the dumps, the content addressing, the federation model — exists to make that outcome cheap.
