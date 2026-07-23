# Schema notes

Where DATA_MODEL v0.1.1 failed on contact with 150 objects and two miles of rock.

**These are not fixed in the prototype.** They are written down. Fixing them here would overfit the schema to one island. They feed v0.2, after the East Village slice confirms which breakages are general and which are Roosevelt Island being strange.

Predictions from the build prompt are marked ✅ (predicted, broke as expected) or ❌ (predicted, didn't break). Unpredicted breakages are marked **NEW** — and those are the valuable ones.

---

## 1. ✅ Ownership ≠ operation ≠ jurisdiction. The schema conflates two of the three.

**Predicted, and worse than predicted.**

Current schema: `ownership.owner` and `responsibility.maintainer`. Two slots.

The tram needs **four**:
- RIOC **owns** it.
- Leitner-Poma (a French company) **operates** it, under a contract nobody has read.
- The MTA **collects the fare**.
- New York State **regulates** aerial passenger tramways.

AVAC needs four too, and one of them is contested: RIOC owns it, DSNY may or may not operate it (sources flatly disagree), and no published agreement governs the relationship.

**The failure is not that we lack fields. It's that we modelled responsibility as a property of the object.** It isn't. Responsibility is a *relation with a term and an instrument* — a contract, a statute, a lease — and it has a start date, an end date, and a document that establishes it.

**Proposed v0.2:**
```yaml
responsibility:
  - role: owner | operator | maintainer | regulator | fare_authority | funder
    party: cop:inst:... | cop:org:...
    from: 2010-11-30
    to: null
    instrument: cop:src:...        # the contract/statute — NULLABLE, and null is a finding
    instrument_public: false       # ← the accountability bit
```
That last flag is the one that matters. `instrument_public: false` is publishable, aggregable, and damning. "How much of this island is run under agreements nobody can read" becomes a query.

---

## 2. ✅ The tram spans two jurisdictions. Containment handled it. Barely.

**Predicted; the DAG held.** The tram sits `within` Roosevelt Island *and* `within` the Upper East Side — its Manhattan terminal and one tower stand off-island. A parent pointer would have forced a lie. The labelled-edge DAG absorbed it without complaint.

Same for the bridge: it is in Manhattan **and** Queens. Two boroughs, one object, no problem.

**This is the schema decision that most clearly paid for itself,** and it is worth saying so, because it was the one that looked like over-engineering when we wrote it.

---

## 3. ✅ AVAC is a network. The schema has no network primitive.

**Predicted, and it is the sharpest structural gap.**

AVAC is ~3 miles of buried 20-inch pipe connecting twenty buildings to a central plant. It is not a point. It is not a polygon. It is not a line. It is a **graph with a topology, a capacity, and a load** — and the load has roughly doubled since it was built.

`connected_infrastructure` (a flat list of object IDs) is not adequate. It can say "these twenty buildings touch AVAC". It cannot say:
- which segment serves which building,
- what each segment's capacity is,
- where the bottleneck is,
- what happens downstream when a valve at Westview fails.

**Every utility is like this.** Water, sewer, power, gas, fibre, district heating. We built an object model and the world is full of networks. This is not an AVAC problem; AVAC just found it first.

**Proposed v0.2:** a `network` object type with `nodes[]`, `edges[]` (each with capacity and a `serves[]` list), and `plant[]`. Objects gain `attached_to: {network, node}`.

**And the harder half:** the network geometry is not published *anywhere*. So we would have the schema and no data. Which raises a question worth putting to the project: **is an unpublished utility network a gap, or is it a security exemption?** Roosevelt Island's waste pipes, plausibly not sensitive. A city's water mains — a different argument, and one we have not had. This belongs in PRINCIPLES, not in the schema.

---

## 4. ✅ Cornell Tech. Is it public?

**Predicted. Still unresolved.**

A private university, on land the city owned, cleared by demolishing a public hospital, built for $2bn of unknown public/private composition, under an agreement that is not published.

The schema forces a choice — `tenure: public | private` — and every available answer is wrong:
- `private` and it drops out of scope, which is absurd: a public hospital was demolished for it.
- `public` and we mis-state ownership.

We recorded `tenure: "private institution on city-owned land"` as a free-text string. **That is a schema failure wearing a raincoat.** A free-text tenure field is unqueryable, and "show me every private object built on public land" is one of the most important queries this platform could ever answer.

**Proposed v0.2:** decompose tenure.
```yaml
tenure:
  land_owner: cop:inst:us-ny:nyc
  structure_owner: cop:org:us-ny:cornell
  arrangement: ground_lease | concession | ppp | outright
  instrument: cop:src:...          # null here — and that is the finding
  public_contribution:
    land_value: {status: unknown, reason: not_found}
    direct_funding: {status: unknown, reason: not_found}
```
Public-private objects are not an edge case. They are how a great deal of the built environment now gets made, and the schema currently cannot see them.

---

## 5. **NEW** — Promises are not projects, and nothing holds them.

**Unpredicted. Possibly the most important finding in the build.**

The Cornell Tech bid promised 28,000 jobs, 600 incubated companies, $23bn in economic benefit, $1.4bn in taxes over thirty years. The AVAC upgrade promised "at least 30 more years of automated waste collection". The tram modernization was announced as six months.

These are **public commitments made to secure public consent or public money**, and the schema has nowhere to put them. They live in press releases and then evaporate.

`projects[].milestones[]` captures planned-vs-actual for *delivery dates*. It cannot capture a promise about the world made ten years before anyone could check it.

**Proposed v0.2:** a first-class `commitment` type.
```yaml
commitment:
  made_by: cop:org:...            # or cop:office:...
  made_on: 2011-12-19
  in_support_of: cop:proj:...
  claim: "28,000 jobs over 30 years"
  measurable: true
  horizon: 2041
  verification: {status: never_measured, reason: no_public_accounting}
```
`verification.status: never_measured` — aggregated across a city, across a decade — may be the single most useful number this platform could ever produce.

Nobody is keeping score. The schema should make the absence of scorekeeping visible.

---

## 6. **NEW** — The derived occupancy record is only as good as the project register. There is no project register.

**Unpredicted, and it is a direct hit on the 0.1.1 accountability model.**

We rewrote the officeholder model specifically so individuals *are* accountable — through their decisions, via a derived record computed from projects whose responsibility chain intersects their term.

We then tried to compute it for four RIOC presidents.

**We could not compute a single aggregate.** Not projects-completed-on-schedule, not cost variance, not responsiveness. Because RIOC does not publish a dated, attributed project register, and there is no way to derive one from press releases.

**The model is not wrong. It is starved.** And that is worth stating plainly, because the temptation at this exact moment — the moment where the elegant model produces an empty table — is to soften it: to allow a free-text rating, to let a human "just enter what they know."

**Do not.** The empty table *is* the output. It says: this officeholder cannot be held to account with public data, and here is exactly which dataset is missing. That is a truer and more actionable finding than any number we could have fabricated.

The prototype renders the empty aggregate, in red, with the reason. That is the correct behaviour and it should ship that way.

---

## 7. **NEW** — Contested is not one thing.

We used `contested` for three genuinely different situations and they should not share a tier:

| What happened | Example |
|---|---|
| **Sources disagree on a fact** | Tram cabin capacity: 125 (contractor) vs 109+1 (encyclopaedia). Someone is wrong. |
| **The fact changed and sources are stale** | Renwick stabilisation cost: $3M (2008) → $4.5M (2009–21) → $5M (retrospective). These may all be correct, at different times. |
| **Nobody knows who is responsible** | AVAC: RIOC and DSNY are each described as the operator. This is not a disagreement about a fact — it is a *real* ambiguity in the world. |

The third is the most important and it is currently indistinguishable from the first. A reader sees `CONTESTED` and cannot tell whether two journalists made an error or whether nobody actually knows who runs the trash system.

**Proposed v0.2:** split into `disputed` (sources conflict; one is wrong), `superseded` (bitemporal — use `valid_from`, not a contest), and `ambiguous` (the world itself is unclear; this is a finding about governance, not about data quality).

Note that `superseded` is not a new tier at all — it's what bitemporality is *for*, and we reached for `contested` because the pilot has one revision per object and no history to hang the versions on. **That is a prototype limitation masquerading as a schema gap.** Worth flagging so v0.2 doesn't "fix" something that isn't broken.

---

## 8. **NEW** — Absence has kinds, and the reason codes are ad hoc.

We used `not_published`, `not_found`, `not_yet_researched`, `not_applicable`, `not_computable`, `not_researched`. Six codes, invented as we went, with no controlled vocabulary.

They mean genuinely different things and the difference is the entire product:

- `not_published` — **the institution has it and does not publish it.** An accountability finding. Points at a FOIL request.
- `not_found` — we looked and failed. Points at our own incompleteness.
- `not_yet_researched` — we did not look. Honest, and a backlog item.
- `not_computable` — the field is derived and its inputs are missing. Points at a *different* missing dataset.
- `not_applicable` — the field does not apply. Not a gap at all.

Aggregating `not_published` across a city gives you an opacity index. Aggregating `not_found` gives you a to-do list. Conflating them gives you neither.

**Proposed v0.2:** controlled vocabulary for `reason`, validated at the schema level. This is a small change with a large payoff and it should land first.

---

## 9. **NEW** — Privacy: the map itself leaks.

**Not a schema issue. An architecture issue, and it was not on anyone's list.**

We built the map as inline SVG, drawn locally from our own geometry, with no map library and no tile server.

The reason was originally just "no third-party CDN". But partway through it became clear this is a **privacy requirement**, not a dependency preference:

> A tile server sees every pan and every zoom. Viewport requests are a behavioural log. If a journalist explores the objects surrounding a particular contractor's projects, a third-party tile provider — and anyone who subpoenas it — can watch them do it, in real time, in order.

PRINCIPLES.md §3 says the platform holds no record of who read what. **Fetching tiles from someone else's server means someone else holds exactly that record.** We would have quietly outsourced the surveillance we swore off.

**Consequence for ROADMAP Phase 3 (3D):** a privacy-preserving map may have to **ship its tiles**, not fetch them — bundled, cached, served from the same origin, or generated client-side from bulk geometry. That is a materially harder engineering problem than "use MapLibre", and the roadmap currently does not budget for it.

**This should go into ARCHITECTURE §5 as a hard constraint on the serving plane, and into SECURITY as a threat.** It is the kind of mistake that would have been very easy to ship and very embarrassing to discover afterwards.

---

## Verdict on v0.1.1

**Held:** containment as a labelled DAG (#2). Verification tiers. Declared absence as a first-class state — it did more work than anything else in the schema, and the prototype is legible *because* of it. Append-only revisions (untested at one revision per object, but nothing about the build strained them).

**Broke:** responsibility-as-property (#1). No network primitive (#3). Binary tenure (#4). No commitment type (#5). Undifferentiated contest (#7). Ad-hoc absence reasons (#8).

**Starved:** the derived occupancy record (#6). Model sound; data absent. Do not soften it.

**Missed entirely:** the map is a privacy surface (#9).

None of these are fatal. All of them are cheaper to fix now, on 29 objects, than later on 29 million. Which was the point of building the pilot before the platform.
