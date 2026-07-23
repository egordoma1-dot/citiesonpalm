# Cities On Palm — prototype 0.1

**Roosevelt Island, Manhattan.** The first artefact of the project specified in the main repository.

Open **`citiesonpalm.html`** — one self-contained file. No server, no build step, no install, no sibling files.

---

## What this is

A working object-passport reader for one island. 29 objects, 6 institutions, 2 offices, 32 sources.

- **`citiesonpalm.html`** — **start here.** Everything in one file: map, passports, institutions, full record. Data inlined.
- **`index.html` + `data/passports.js` + `table.html`** — the same thing split across files, as it would be deployed. `table.html` is pre-rendered static HTML that **works with JavaScript disabled** — not a fallback, the surface a researcher would actually use. These need to sit in the same folder to work.
- **`data/passports.json`** — the data, as an API would serve it.
- **`GAPS.md`** — **read this one.** The map is a demo. This is the finding.
- **`SCHEMA_NOTES.md`** — nine places DATA_MODEL v0.1.1 broke.

Rebuild: `python3 build_data.py && python3 build_geom.py && python3 build_table.py && python3 build_single.py`

---

## What it proves

**Nothing here is invented.** Every populated field carries a source link and a verification tier. Where the public record has no answer, the field says `UNKNOWN` and names what is missing. Where sources disagree, it says `CONTESTED` and shows both without adjudicating.

That rule was the whole experiment, and it produced the result:

- **The Renwick Ruin.** Ask what it cost to stabilise New York's only landmarked ruin, and whether the work is finished. Four figures across four sources. No traceable contract. No clear answer to either question.
- **The Tram.** $15M announced (2006) → $25M at contract award (2008). Promised a six-month closure; took nine. Both facts public. Never presented together.
- **AVAC.** Built in 1975 for four buildings. The island has doubled; the same vacuum backbone now serves twenty. No public record shows it was ever evaluated for that load. A $1.7M upgrade announced in 2019 as a six-month job has no completion notice seven years on.
- **The RIOC board.** At least three members' terms had expired in the most recent public listing — one over two years ago. Whether they were reappointed, replaced, or are simply still sitting is not stated anywhere. **This took one query.**

---

## The success criterion, judged honestly

Stated before the build:

> A person who has never seen this project can open the file, click the Renwick Ruin, and in under ten seconds know what it is, who owns it, who's responsible, what its stabilisation cost — *or that nobody will say* — and everything that has happened to it since 1856, with a source on every claim.

**Met.** And the most useful thing on that passport is the red `CONTESTED` block where the cost should be.

The Phase 1 criterion in ROADMAP is harder — *a working journalist finds something they could not previously find, without our help* — and is not met, because no journalist has used it. The RIOC board finding suggests it is reachable.

---

## Honest limitations

- **All geometry is approximate.** Hand-placed in an island-local coordinate frame (metres along and across the island axis), then converted to lat/lon. Not surveyed, not traced from any dataset — the build environment had no network access, so no OSM or PLUTO extract. Footprints correspond to the real layout well enough to be recognisable and no further. Every geometry field is marked `confidence: approximate`; the schema has a slot for exactly this, which is the point.
- **Manhattan, Queens, the river channels and the Queensboro Bridge are rendering context only.** They are stored under `basemap`, not as passport records, and are marked as such. They exist so the island reads as an island.
- **7 objects researched. 22 are stubs** and say so on their face. A visible gap beats an invisible one.
- **AVAC's network route is a placeholder.** The real routing is not published anywhere. That is a finding, not a shortcut.
- **No write path.** None. There is no code here capable of writing. The physical-terminal path is out of scope.
- **Data is inlined, not fetched.** `file://` blocks cross-origin fetch, and a split-file build breaks the moment someone opens `index.html` on its own — which is exactly what happened to the first cut of this prototype. In production this is a static JSON endpoint. `table.html` is pre-rendered and needs no JS at all.

---

## Two deliberate departures from the brief

**No 3D.** The brief asked for it; the data model is the harder problem and it consumed the budget. 3D is deferred, as ROADMAP always said it should be. What is here instead is a plan view that renders every object and opens every passport, which is the part that had to work.

**No map library, no tile server.** This began as "no third-party CDN" and became a privacy finding — see SCHEMA_NOTES #9:

> A tile server sees every pan and every zoom. If a journalist explores the objects around a particular contractor's projects, a third-party tile provider — and anyone who subpoenas it — watches them do it, in order, in real time.

PRINCIPLES §3 says the platform holds no record of who read what. Fetching tiles means someone *else* holds exactly that record. So the map is inline SVG, drawn locally. **Nothing in this prototype makes a single third-party request.** No fonts, no analytics, no CDN, no tiles.

That constraint is now a hard requirement on the serving plane, and it makes Phase 3 materially harder than the roadmap currently budgets for.

---

## Next

1. **Build the three adapters** in GAPS.md — MapPLUTO, the federal National Bridge Inventory, and the NY State Authorities Budget Office. The third is the key to this island, because RIOC is a *state* body sitting inside a *city* open-data regime, and that seam is why the island is dark.
2. **Do not fix the schema yet.** Take the nine breakages to a six-block slice of the East Village first, and find out which are general and which are Roosevelt Island being strange.
3. **Take the RIOC board finding to a journalist.** That is the Phase 1 exit criterion, and it is one phone call away.
