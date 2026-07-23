# GAPS

**This is the deliverable.** The map is a demo. This is the finding.

Below is every field we could not populate for the seven researched objects, why, and where the data probably lives. It is a map of how opaque a two-mile island in New York City actually is — an island with a modern, well-resourced operator, a published board calendar, and a FOIL portal.

If the record is this thin *here*, consider what it looks like in a jurisdiction that is not trying.

---

## The headline

We asked five questions of each object. Question 3 — **who paid for it** — could not be answered for most of them.

| Object | Construction cost | Maintenance cost | Inspection record |
|---|---|---|---|
| Roosevelt Island Tramway | **not published** | **not published** | **not published** |
| AVAC (pneumatic waste) | **not published** | **not published** | **not published** |
| Renwick Ruin | $38,000 (1856) | — | partial |
| Renwick stabilisation | **contested — 4 figures** | — | 2019 survey not published |
| Roosevelt Island Bridge | $6.5M (1955) | **not published** | **not retrievable** |
| Cornell Tech | $2bn headline | — | n/a |
| — of which public money | **not found** | | |
| Four Freedoms Park | **not found** | **not found** | n/a |
| Southpoint shoreline | **not published** (award publicised, cost not) | — | — |

The 1955 bridge and the 1856 ruin have public construction costs. The 1976 tram and the 1975 AVAC do not. **Older public infrastructure is better documented than newer public infrastructure.** That is not a data-collection artefact; it is a finding.

---

## Gap by gap

### 1. Tram — original construction cost
**Missing:** what it cost to build the tramway in 1976.
**Why:** built by the New York State Urban Development Corporation, a body that no longer exists in that form.
**Where it probably lives:** UDC records at the New York State Archives. Not digitised. Not online. Would require an in-person archive visit or a records request.
**Adapter target:** none exists. This is a paper-archive problem, not a software problem.

### 2. Tram — maintenance and inspection
**Missing:** annual maintenance spend; cable and haul-rope inspection reports.
**Why:** RIOC publishes an operating budget, but not a line-item breakdown. Inspection records for an aerial tramway carrying 2.5M passengers a year certainly exist — they are legally required — but are not published.
**Where it probably lives:** RIOC internal; the Leitner-Poma operating agreement; possibly NY State Department of Labor (which regulates aerial passenger tramways).
**Route:** FOIL request to RIOC. RIOC has a FOIL portal.

### 3. Tram — the operating contract
**Missing:** the RIOC–Leitner-Poma agreement itself.
**Why:** not published. We know it exists (5-year term from 2010, renewed 2019) only because the contractor's marketing page says so.
**Consequence:** a French cable-car manufacturer operates a piece of New York's public transit under terms no member of the public has read.
**Route:** FOIL. Contracts of state authorities are generally subject to disclosure.

### 4. AVAC — everything financial
**Missing:** 1975 construction cost; annual operating cost; the RIOC–DSNY agreement; the status and final cost of the 2019 upgrade.
**Why:** the 2019 upgrade was announced by press release ($1.7M, Envac Iberia, six months, "at least 30 more years"). **No completion notice exists.** Seven years later, local press reports the system failing and RIOC silent since January 2025.
**Where it probably lives:** RIOC procurement records; NY State Authorities Budget Office (RIOC files as a state authority and its procurement is reportable); DSNY.
**Route:** ABO filings are the strongest lead — a state authority must report contracts. This is the single highest-value adapter to build first.

### 5. AVAC — the network geometry
**Missing:** where the pipes actually run.
**Why:** not in any public dataset. Not in OSM. Not in NYC Open Data.
**Consequence:** the map shows a dashed placeholder line along Main Street. It is not the real route and the passport says so.
**Note:** this is also a *schema* problem — see SCHEMA_NOTES.md #3.

### 6. AVAC — the capacity question
**Missing:** any engineering evaluation of whether a 1975 system built for four buildings can serve twenty.
**Why:** as a local journalist put it, there is no public record showing the system was ever evaluated for that expansion.
**This is the most important gap in the pilot.** It is not a missing number. It is a missing *decision*. Somebody, at some point, connected Southtown and Manhattan Park and The Octagon to a vacuum backbone sized for Northtown, and there is no public trace of anyone checking first.

### 7. Renwick Ruin — the stabilisation cost
**Missing:** what was actually spent, by whom, and when.
**What we have:** $4.5M (cited repeatedly, 2009–2020s), $5M (retrospective), $3M "needed" (2008 estimate), $17,000 (a Landmarks Conservancy grant for an engineering study), >$1.2M (raised by Friends of the Ruin by 2022).
**Why it's contested:** none of these figures traces to a published RIOC contract or budget line. They are press figures, repeated.
**Also missing:** whether the project is *finished*. One source says a $4.5M stabilisation "was completed in the 2020s". Another says RIOC installed only "temporary stabilization … still not secure enough for general public access". A third says drawings reached design development in 2019.
**Route:** RIOC capital programme documents; RIOC board minutes 2009–2024. The minutes are published. Nobody has read them all. **A machine could.**

### 8. Bridge — condition rating
**Missing:** the current structural condition rating.
**Why:** NYC DOT publishes an annual Bridges & Tunnels Condition Report, as a PDF. The per-structure rating is in there. It is not in a machine-readable form and we could not retrieve the current edition.
**Where it lives:** NYC DOT annual report; also the federal National Bridge Inventory (FHWA), which is machine-readable and *would* have this.
**Route:** NBI is the answer. It's a national dataset. This is an easy, high-value adapter and it would cover every bridge in the United States.

### 9. Cornell Tech — the public contribution
**Missing:** how much of the $2bn is public money, and what the city-owned land was worth.
**Why:** the $2bn headline is everywhere. The composition is nowhere. The land was city-owned; a public hospital (Goldwater) was demolished to clear it; the city–Cornell agreement is referenced constantly and published nowhere we could find.
**Also missing:** any accounting against the winning bid's promises — 28,000 jobs, 600 companies, $23bn in economic benefit, $1.4bn in taxes over 30 years. The bid is nine years old. Nobody appears to be keeping score.
**Route:** the ULURP record; NYC EDC; the Applied Sciences Competition award documents. Likely the hardest and most valuable dig in the pilot.

### 10. Four Freedoms Park — cost
**Missing:** what a 4-acre state park designed by Louis Kahn cost to build.
**Why:** not found in any source. It is operated by a separate LLC — "Franklin D. Roosevelt Four Freedoms Park, LLC" — whose finances and governance we could not locate.
**Note:** an LLC operating a state park is itself worth a passport. We could not build one.

### 11. RIOC — the project register
**Missing:** a complete, dated, attributed list of RIOC capital projects.
**Why:** RIOC publishes board minutes and approves capital programmes (a $40.8M programme was approved in 2019, per its own press release). It does not publish a project register.
**Consequence — and this is the big one:** the **derived occupancy record for every RIOC president is empty.** We cannot compute projects-on-schedule, projects-late, or cost variance for any officeholder, because the underlying project data does not exist in public form.

The accountability model works. The data beneath it is not there. **That is precisely the gap this platform exists to close, and the pilot demonstrates it by failing honestly rather than by inventing numbers.**

### 12. RIOC board — the term dates
**Missing:** current, authoritative board membership with term dates.
**What we found:** in the most recent public listing retrieved, at least three board members' terms had already expired — one in June 2024, more than two years ago. Whether they were reappointed, replaced, or are simply still sitting is not stated anywhere we could find.
**This took one query.** It is the most concrete finding in the pilot and it was almost accidental.
**Route:** RIOC board page; NY State Senate confirmation records; ABO filings.

---

## Geometry

**All geometry in this prototype is approximate and hand-placed.** Nothing is surveyed. Nothing is traced from a real dataset.

**Why:** the build environment had no network access. Real geometry needs an OSM extract (ODbL, free) and NYC MapPLUTO (open, free). Both are one-time downloads and would take an afternoon.

**Every geometry field is marked `confidence: approximate`.** The schema has a slot for exactly this, which is the point — a system that could not represent its own uncertainty would have had to lie here.

---

## What we did not even attempt

- **Street trees.** NYC has an individual-tree census: species, diameter, health, per tree. Roosevelt Island has thousands. They are Tier 2 and they are not in this build.
- **DOB permits.** Every permit, every violation, per building. Public, machine-readable, and untouched here.
- **NYC Checkbook.** Every city contract and payment. This is the richest single source for "who paid for it" and we did not connect it. It would not, however, cover RIOC — a state body — which is exactly why the accountability gap on this island is as wide as it is.
- **PLUTO.** Every lot, owner, year built, assessed value. The single highest-value adapter for buildings.

---

## The three adapters to build first

Ranked by value per unit of effort:

1. **NYC MapPLUTO** — ownership, year built, lot geometry, assessed value, for every building. Open, bulk, machine-readable. Would populate the twenty-two stubs almost entirely.
2. **Federal National Bridge Inventory** — condition ratings for every bridge in the country, machine-readable. Solves gap #8 nationally, not just here.
3. **NY State Authorities Budget Office** — RIOC's contracts, budget, and board filings. This is the key to the island, because RIOC is a state authority and therefore *outside* NYC's otherwise excellent open-data ecosystem. That mismatch is the whole reason this island is dark.

---

## The finding behind all the findings

Roosevelt Island sits inside New York City, which has one of the best municipal open-data programmes in the world — PLUTO, Checkbook, DOB, the Capital Projects Dashboard, all of it.

None of it covers the island's own operator.

RIOC is a **New York State** public benefit corporation. It is not a city agency. So it falls outside the city's open-data mandate, while sitting geographically in the middle of it. Twelve thousand people live in a jurisdictional seam, governed by a board they do not elect, appointed by a governor in Albany, running a $39M budget with no published project register.

**The opacity here is not caused by anyone hiding anything. It is caused by a boundary.** Nobody drew it to conceal; it just fell that way, and nobody has had a reason to fix it.

That is the entropic opacity described in VISION.md, and this pilot is the first evidence that the diagnosis is right.
