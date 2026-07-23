#!/usr/bin/env python3
# Cities On Palm — prototype data.
# RULE: no invented values. Every populated field has a source.
#       Unfindable fields are {"status":"unknown","reason":...}.

import json, os, hashlib

def U(reason, note=None):
    d = {"status": "unknown", "reason": reason}
    if note: d["note"] = note
    return d

def V(value, src, tier, note=None):
    d = {"value": value, "source": src, "tier": tier}
    if note: d["note"] = note
    return d

def C(positions, note=None):
    """A contested field: sources disagree. Both shown, neither adjudicated."""
    d = {"status": "contested", "positions": positions}
    if note: d["note"] = note
    return d

# ---------------------------------------------------------------- SOURCES
SOURCES = {
  "rioc-status":   {"name":"RIOC — Status & Jurisdiction","uri":"https://rioc.ny.gov/166/Status-Jurisdiction","org":"Roosevelt Island Operating Corporation","kind":"official"},
  "rioc-tram":     {"name":"RIOC — Tram","uri":"https://www.rioc.ny.gov/community/transportation/tram","org":"RIOC","kind":"official"},
  "rioc-board":    {"name":"RIOC — Board of Directors","uri":"https://rioc.ny.gov/149/Board-of-Directors","org":"RIOC","kind":"official"},
  "rioc-meetings": {"name":"RIOC — Meetings & Notices","uri":"https://rioc.ny.gov/336/Meetings-Notices","org":"RIOC","kind":"official"},
  "rioc-news":     {"name":"RIOC — News & Press Releases","uri":"https://rioc.ny.gov/453/News","org":"RIOC","kind":"official"},
  "nysa-rioc":     {"name":"NY State Archives — RIOC President/CEO files (agency history)","uri":"https://findingaids.nysed.gov/do/6270cf61-417d-5639-b8c2-b8f4ca2f6e74","org":"New York State Archives","kind":"official"},
  "nycdot-bridges":{"name":"NYC DOT — Bridges over Smaller Waterways","uri":"https://www.nyc.gov/html/dot/html/infrastructure/bridges-misc.shtml","org":"NYC Department of Transportation","kind":"official"},
  "poma":          {"name":"POMA — AirTram Roosevelt Island (project page)","uri":"https://www.poma.net/en/work/airtram-roosevelt-island/","org":"POMA (contractor)","kind":"contractor"},
  "envac-50":      {"name":"Envac — 50 Years Underground","uri":"https://www.envacgroup.com/news/50-years-underground-envac-celebrates-five-decades-of-innovation-beneath-roosevelt-island/","org":"Envac (contractor)","kind":"contractor"},
  "soury-avac":    {"name":"AVAC to Get Major Upgrade (RIOC/Envac release, 1 May 2019)","uri":"https://www.soury.com/avac-roosevelt-islands-automated-vacuum-waste-collection-system-to-get-major-upgrade-after-more-than-40-years-of-service/","org":"Soury Communications for RIOC/Envac","kind":"press_release"},
  "waste360":      {"name":"Waste360 — Roosevelt Island AVAC Gets Upgrade","uri":"https://www.waste360.com/waste-collection-transfer/nyc-s-roosevelt-island-avac-waste-collection-system-gets-upgrade-after-40-plus-years","org":"Waste360","kind":"trade_press"},
  "wp-tram":       {"name":"Wikipedia — Roosevelt Island Tramway","uri":"https://en.wikipedia.org/wiki/Roosevelt_Island_Tramway","org":"Wikipedia","kind":"tertiary"},
  "wp-bridge":     {"name":"Wikipedia — Roosevelt Island Bridge","uri":"https://en.wikipedia.org/wiki/Roosevelt_Island_Bridge","org":"Wikipedia","kind":"tertiary"},
  "wp-smallpox":   {"name":"Wikipedia — Smallpox Hospital","uri":"https://en.wikipedia.org/wiki/Smallpox_Hospital","org":"Wikipedia","kind":"tertiary"},
  "wp-ri":         {"name":"Wikipedia — Roosevelt Island","uri":"https://en.wikipedia.org/wiki/Roosevelt_Island","org":"Wikipedia","kind":"tertiary"},
  "wp-rioc":       {"name":"Wikipedia — Roosevelt Island Operating Corporation","uri":"https://en.wikipedia.org/wiki/Roosevelt_Island_Operating_Corporation","org":"Wikipedia","kind":"tertiary"},
  "wp-cornell":    {"name":"Wikipedia — Cornell Tech","uri":"https://en.wikipedia.org/wiki/Cornell_Tech","org":"Wikipedia","kind":"tertiary"},
  "newtown-tram":  {"name":"Newtown Pentacle — Roosevelt Island Tram work (Apr 2010)","uri":"https://newtownpentacle.com/2010/04/10/roosevelt-island-tram-work/","org":"The Newtown Pentacle","kind":"press"},
  "almanack":      {"name":"New York Almanack — Roosevelt Island Opens New Aerial Tramway (Nov 2010)","uri":"https://www.newyorkalmanack.com/2010/12/roosevelt-island-opens-new-aerial-tramway/","org":"New York Almanack","kind":"press"},
  "6sqft-tram":    {"name":"6sqft — The History of the Roosevelt Island Tramway","uri":"https://www.6sqft.com/the-history-of-the-roosevelt-island-tramway/","org":"6sqft","kind":"press"},
  "wbmelvin":      {"name":"Walter B. Melvin Architects — Smallpox Hospital / Renwick Ruin","uri":"https://wbmelvin.com/portfolio-item/smallpox-hospital-renwick/","org":"Walter B. Melvin Architects (consultant)","kind":"contractor"},
  "nylandmarks":   {"name":"NY Landmarks Conservancy — Renwick Ruin","uri":"https://nylandmarks.org/celebrate-50-at-50/renwick-ruin/","org":"New York Landmarks Conservancy","kind":"ngo"},
  "untapped-ruin": {"name":"Untapped New York — Inside the Abandoned Smallpox Hospital","uri":"https://www.untappedcities.com/photos-inside-the-abandoned-smallpox-hospital-on-roosevelt-island/","org":"Untapped New York","kind":"press"},
  "rihs-smallpox": {"name":"Roosevelt Island Historical Society — Smallpox Ruin","uri":"https://rihs.us/riwalk/Tour_South_6__Smallpox_Ruin.html","org":"Roosevelt Island Historical Society","kind":"ngo"},
  "fasttrash":     {"name":"Fast Trash — Roosevelt Island's AVAC","uri":"https://fasttrash.org/exhibition/roosevelt-islands-avac/","org":"Center for Urban Pedagogy","kind":"ngo"},
  "npr-avac":      {"name":"NPR — How Roosevelt Island Sucks Away Summer Trash Stink","uri":"https://www.npr.org/2017/07/26/539304811/how-new-york-s-roosevelt-island-sucks-away-summer-trash-stink","org":"NPR","kind":"press"},
  "rilighthouse":  {"name":"RI Lighthouse — Roosevelt Island's Underground Trash System","uri":"https://www.ri-lighthouse.com/p/roosevelt-islands-underground-trash","org":"RI Lighthouse","kind":"press"},
  "ridaily-avac":  {"name":"Roosevelt Island Daily — AVAC System: History and Challenges (Apr 2025)","uri":"https://rooseveltislanddaily.news/2025/04/07/avac-system-roosevelt-island/","org":"Roosevelt Island Daily","kind":"press"},
  "cornell-open":  {"name":"Cornell Tech — Campus Opens on Roosevelt Island","uri":"https://tech.cornell.edu/news/cornell-tech-campus-opens-on-roosevelt-island-marking-transformational-mile/","org":"Cornell Tech","kind":"official"},
  "constrdive":    {"name":"Construction Dive — NYC's $2B Cornell Tech campus opens","uri":"https://www.constructiondive.com/news/nycs-2b-cornell-tech-academic-campus-opens/505024/","org":"Construction Dive","kind":"trade_press"},
  "structurae":    {"name":"Structurae — Roosevelt Island Bridge","uri":"https://structurae.net/en/structures/roosevelt-island-bridge","org":"Structurae","kind":"tertiary"},
  "som":           {"name":"SOM — Cornell Tech Campus Framework Plan","uri":"https://www.som.com/projects/cornell-tech-campus-framework-plan/","org":"SOM (architect)","kind":"contractor"},
}

RET = "2026-07-13"

# ---------------------------------------------------------------- OBJECTS
# Geometry is APPROXIMATE throughout — hand-placed, not surveyed.
# Real geometry requires OSM/PLUTO extracts (see GAPS.md #geometry).

OBJECTS = []

def obj(**kw):
    kw.setdefault("tier", 1)
    OBJECTS.append(kw)

# ---- THE TRAM -------------------------------------------------------------
obj(
  id="cop:obj:us-ny-36061:tram",
  type="aerial_tramway",
  name="Roosevelt Island Tramway",
  also=["The Tram", "AirTram"],
  geom={"kind":"line","pts":[[40.7573,-73.9539],[40.7590,-73.9583],[40.7614,-73.9640]],"confidence":"approximate"},
  containment=[
    {"rel":"within","target":"cop:dist:us-ny-36061:roosevelt-island"},
    {"rel":"within","target":"cop:dist:us-ny-36061:upper-east-side","note":"Manhattan terminal + one tower stand off-island"},
    {"rel":"crosses","target":"cop:obj:us-ny-36061:east-river-west-channel"},
  ],
  lifecycle={
    "status": V("in_service","rioc-tram","official_document"),
    "opened": V("1976-05-17","wp-tram","cross_referenced","Opened May 1976; sources vary between 17 May and July 1976."),
    "design_life": V("17 years (original system, as designed)","newtown-tram","single_source",
                     "The original system ran 34 years — double its design life."),
  },
  ownership={
    "owner": V("Roosevelt Island Operating Corporation (RIOC)","poma","authoritative",
               "POMA, the contractor, names RIOC as owner."),
    "tenure": V("public — NY State public benefit corporation","rioc-status","official_document"),
  },
  responsibility={
    "operator": V("Leitner-Poma of America, under contract to RIOC","poma","official_document",
                  "5-year operating agreement from 2010, renewed 2019."),
    "fare_system": V("MTA — OMNY / MetroCard integrated since 2005; OMNY from 24 Aug 2023","wp-tram","cross_referenced"),
    "note": "SPLIT RESPONSIBILITY: RIOC owns it, a French contractor runs it, the MTA collects the fare. No single body is accountable end-to-end.",
  },
  finance={
    "construction_cost": U("not_published","Original 1976 construction cost not found in any public source. Built by the NY State Urban Development Corporation; UDC records are at the NY State Archives and are not online."),
    "annual_maintenance": U("not_published","RIOC publishes an operating budget but does not break out tram maintenance as a line item in any document found."),
  },
  projects=[{
    "id":"cop:proj:us-ny-36061:tram-modernization",
    "title":"Roosevelt Island Tram Modernization Project",
    "status":"completed",
    "authorised_by":"RIOC Board of Directors",
    "contractor": V("POMA / Leitner-Poma of America (design-build)","6sqft-tram","cross_referenced",
                    "Contract awarded by RIOC Board, November 2008."),
    "engineers": V("LiRo Engineering; Thornton Tomasetti; Shea, Carr & Jewell","almanack","single_source"),
    "budget_history":[
      {"date":"2006","amount":15000000,"label":"Announced after the April 2006 breakdown","src":"wp-tram"},
      {"date":"2008-mid","amount":25000000,"label":"Revised before contract award","src":"wp-tram"},
      {"date":"2010","amount":25000000,"label":"Final","src":"newtown-tram"},
    ],
    "funding": V("$10M RIOC + $15M New York State","newtown-tram","single_source"),
    "cost_variance": {"from":15000000,"to":25000000,"pct":66.7},
    "milestones":[
      {"name":"Contract awarded to POMA","planned":None,"actual":"2008-11"},
      {"name":"Service suspended","planned":"2010-03-01","actual":"2010-03-01"},
      {"name":"Service restored","planned":"2010-09-01","actual":"2010-11-30",
       "note":"Announced as a six-month closure. Took nine."},
    ],
    "schedule_variance": {"planned_months":6,"actual_months":9,"pct":50.0},
    "src":"wp-tram",
  }],
  inspections=U("not_published","No inspection reports for the tram are published by RIOC. Cable and haul-rope inspection records exist (they are required) but are not public."),
  attributes={
    "span_m": V(960,"poma","official_document"),
    "cabins": V(2,"poma","official_document"),
    "cabin_capacity": C([
      {"value":"125 passengers","src":"6sqft-tram"},
      {"value":"109 passengers plus one attendant","src":"wp-tram"},
    ],"Contractor and encyclopaedic sources disagree on cabin capacity."),
    "annual_ridership": V("~2.5M (2016); RIOC estimated 2.6–2.7M subsequently","wp-tram","single_source"),
    "max_height_m": V("~76 m (250 ft) above the East River","newtown-tram","single_source"),
    "availability": V("99.8% (contractor's figure)","poma","single_source",
                      "Self-reported by the contractor. No independent audit found."),
  },
  connected=["cop:obj:us-ny-36061:tram-plaza","cop:obj:us-ny-36061:motorgate"],
  history=[
    {"t":"1971","what":"Aerial tramway proposed as a temporary measure after the 63rd St subway line fell behind schedule.","src":"wp-tram"},
    {"t":"1976-05","what":"Opens. First commuter aerial tramway in the United States.","src":"wp-tram"},
    {"t":"2005-09-03","what":"Power failure strands two cabins over the East River for hours.","src":"wp-tram"},
    {"t":"2006-04-20","what":"Electrical failure strands 69 passengers up to 250 ft above the river for ~12 hours. Backup generators fail to start.","src":"wp-tram"},
    {"t":"2006","what":"RIOC spends $500,000 on power system upgrades; service resumes 1 September.","src":"wp-tram"},
    {"t":"2008-11","what":"RIOC Board awards design-build contract to POMA.","src":"6sqft-tram"},
    {"t":"2010-03-01","what":"Service suspended for a stated six-month modernization.","src":"newtown-tram"},
    {"t":"2010-11-30","what":"Service restored. Nine months, not six.","src":"wp-tram"},
    {"t":"2023-08-24","what":"OMNY tap-to-pay accepted.","src":"wp-tram"},
    {"t":"2024","what":"Ridership exceeds pre-COVID levels. Residents request priority boarding; RIOC declines, citing a state law against 'undue or unreasonable preference'.","src":"wp-tram"},
  ],
  flag="The published cost rose 67% between announcement and award, and the closure ran 50% long. Both facts are public. Neither is presented together anywhere but here.",
)

# ---- THE RENWICK RUIN -----------------------------------------------------
obj(
  id="cop:obj:us-ny-36061:renwick-ruin",
  type="ruin",
  name="Smallpox Hospital (Renwick Ruin)",
  also=["Renwick Smallpox Hospital","Maternity and Charity Hospital Training School","Riverside Hospital"],
  geom={"kind":"poly","pts":[[40.7528,-73.9576],[40.7531,-73.9572],[40.7528,-73.9568],[40.7525,-73.9572]],"confidence":"approximate"},
  containment=[
    {"rel":"within","target":"cop:obj:us-ny-36061:southpoint-park"},
    {"rel":"within","target":"cop:dist:us-ny-36061:roosevelt-island"},
  ],
  lifecycle={
    "status": V("ruin — structurally stabilised, closed to the public","untapped-ruin","single_source"),
    "built": V("1854–1856","wp-smallpox","cross_referenced"),
    "opened": V("1856-12-18","wp-smallpox","official_document","Under the NYC Commission of Charities and Correction."),
    "closed": V("1950s","wp-smallpox","cross_referenced"),
    "architect": V("James Renwick Jr.","wp-smallpox","authoritative","Also architect of St Patrick's Cathedral."),
    "wings_added": V("1903–1905 (York & Sawyer; Renwick, Aspinwall & Owen)","wbmelvin","official_document"),
  },
  ownership={
    "owner": V("Roosevelt Island Operating Corporation (RIOC)","untapped-ruin","cross_referenced"),
    "tenure": V("public","rioc-status","official_document"),
  },
  responsibility={
    "maintainer": V("RIOC","untapped-ruin","cross_referenced"),
    "regulator": V("NYC Landmarks Preservation Commission (individual landmark, 1976)","wp-smallpox","official_document"),
    "federal": V("National Register of Historic Places (listed 1972)","wp-smallpox","official_document"),
    "note":"The only landmarked ruin in New York City.",
  },
  finance={
    "construction_cost": V({"amount":38000,"currency":"USD","year":1856},"rihs-smallpox","single_source",
      "Roughly $158,000 in a later year's money, per RIHS. Built with inmate labour from the island's penitentiary — which is why it was so cheap."),
    "stabilisation_cost": C([
      {"value":"$4.5 million (project figure, repeatedly cited 2009–2021)","src":"wp-smallpox"},
      {"value":"$5 million (retrospective account)","src":"nylandmarks"},
      {"value":"$3 million 'needed' (preservationists' estimate, 2008)","src":"wp-smallpox"},
    ],"Four figures across four sources, spanning 2008–2020s, none traceable to a published RIOC contract or budget line. It is not clear from any public document what was actually spent, by whom, or when."),
    "other_funding": V("$17,000 grant from the NY Landmarks Conservancy to Four Freedoms Park for an engineering study; Friends of the Ruin reported raising >$1.2M by 2022","nylandmarks","single_source"),
  },
  projects=[{
    "id":"cop:proj:us-ny-36061:renwick-stabilisation",
    "title":"Structural stabilisation",
    "status": C([
      {"value":"completed (a '$4.5M stabilization project was completed in the 2020s')","src":"wp-smallpox"},
      {"value":"partial — RIOC 'installed temporary stabilization … still not secure enough for general public access'","src":"untapped-ruin"},
      {"value":"ongoing — consultant advanced stabilisation drawings to design development in 2019","src":"wbmelvin"},
    ],"Whether this project is finished is genuinely unclear from the public record."),
    "consultant": V("Walter B. Melvin Architects (existing conditions survey, stabilisation drawings, cost estimate)","wbmelvin","official_document"),
    "budget_history":[],
    "milestones":[
      {"name":"North wing partially collapses","planned":None,"actual":"2007-12-26"},
      {"name":"Groundbreaking on Four Freedoms Park incl. stabilisation plans","planned":None,"actual":"2009-05-28"},
      {"name":"Conditions survey addendum; drawings to design development","planned":None,"actual":"2019"},
      {"name":"Open to the public","planned":"unknown","actual":None,"note":"Still closed."},
    ],
    "src":"wp-smallpox",
  }],
  inspections=V("Giorgio Cavaglieri inspected the structure in the 1970s and planned wall reinforcement. Walter B. Melvin Architects produced an existing-conditions survey and a prioritisation plan; the 2019 addendum is not published.","wbmelvin","official_document"),
  attributes={
    "material": V("Island gneiss, quarried on Blackwell's Island","wbmelvin","official_document"),
    "original_beds": V(100,"wp-smallpox","cross_referenced"),
    "dimensions": V("104 ft × 45 ft (original block)","wp-smallpox","single_source"),
    "style": V("Gothic Revival","wbmelvin","authoritative"),
    "illuminated": V("Nightly since 1995","wp-smallpox","single_source"),
  },
  connected=["cop:obj:us-ny-36061:southpoint-park","cop:obj:us-ny-36061:four-freedoms-park"],
  history=[
    {"t":"1854-04-01","what":"Construction begins on the southern tip of Blackwell's Island. Labour is supplied by inmates of the island's penitentiary.","src":"wp-smallpox"},
    {"t":"1856-12-18","what":"Opens. The first hospital in the United States built for smallpox patients.","src":"wp-smallpox"},
    {"t":"1875","what":"Smallpox operations move to North Brother Island. Building becomes a nurses' training school.","src":"wp-smallpox"},
    {"t":"1903-1905","what":"Two Gothic Revival wings added.","src":"wbmelvin"},
    {"t":"1950s","what":"Closed. Abandoned. Roof, floors and stairs are lost over the following decades.","src":"wp-smallpox"},
    {"t":"1972","what":"Listed on the National Register of Historic Places.","src":"wp-smallpox"},
    {"t":"1976","what":"Designated a New York City landmark — the city's only landmarked ruin.","src":"wp-smallpox"},
    {"t":"2007-12-26","what":"A section of the north wing collapses.","src":"wp-smallpox"},
    {"t":"2009-05-28","what":"Ground broken on Four Freedoms Park; stabilisation of the ruin is folded into the plan.","src":"wp-smallpox"},
    {"t":"2019","what":"Consultant advances stabilisation drawings to design development.","src":"wbmelvin"},
    {"t":"present","what":"Fenced. Closed to the public. Illuminated nightly.","src":"untapped-ruin"},
  ],
  flag="Ask the simplest possible question — what did it cost to stabilise this ruin, and is the work finished — and the public record cannot answer either. This single object is the argument for the project.",
)

# ---- AVAC -----------------------------------------------------------------
obj(
  id="cop:obj:us-ny-36061:avac",
  type="waste_network",
  name="AVAC — Automated Vacuum Collection System",
  also=["The pneumatic tubes","Envac system"],
  geom={"kind":"network","pts":[[40.7545,-73.9560],[40.7573,-73.9539],[40.7600,-73.9520],[40.7640,-73.9490],[40.7680,-73.9455]],"confidence":"approximate",
        "note":"NETWORK GEOMETRY IS NOT PUBLISHED. This line is a placeholder along Main Street. The actual routing of ~3 miles of buried 20-inch pipe is not in any public dataset found. See SCHEMA_NOTES.md."},
  containment=[{"rel":"within","target":"cop:dist:us-ny-36061:roosevelt-island"}],
  lifecycle={
    "status": V("in service — reported failing","ridaily-avac","single_source",
                "Residents and local press report repeated failures through 2025."),
    "installed": C([
      {"value":"1975","src":"rioc-status"},
      {"value":"1972 (in one line of the contractor's own 50th-anniversary release, which is otherwise dated to 1975)","src":"envac-50"},
    ],"Even the contractor's anniversary announcement contradicts itself."),
    "design_life": U("not_published"),
  },
  ownership={
    "owner": V("RIOC","rioc-status","official_document"),
    "tenure": V("public","rioc-status","official_document"),
  },
  responsibility={
    "operator": C([
      {"value":"NYC Department of Sanitation (DSNY) — 'has operated AVAC for 40-plus years'","src":"soury-avac"},
      {"value":"RIOC — 'RIOC operates the island's high-tech sanitation system'","src":"wp-rioc"},
      {"value":"'Technically, RIOC oversees AVAC.'","src":"ridaily-avac"},
    ],"A city agency and a state corporation are each described as running it. The residents cannot tell who to call."),
    "note":"This is the clearest accountability gap on the island: a state-owned system operated by a city agency, with neither presenting itself as the responsible party.",
  },
  finance={
    "construction_cost": U("not_published","No public figure for the original 1975 installation was found. It was built under the NY State Urban Development Corporation."),
    "annual_maintenance": U("not_published"),
    "upgrade_2019": V({"amount":1700000,"currency":"USD","year":2019},"soury-avac","official_document",
                      "Contract awarded to Envac Iberia by RIOC."),
  },
  projects=[{
    "id":"cop:proj:us-ny-36061:avac-upgrade-2019",
    "title":"AVAC modernization",
    "status": U("not_published","Announced May 2019 as a six-month upgrade. No completion notice, no final cost, and no status update found in any RIOC publication."),
    "contractor": V("Envac Iberia","soury-avac","official_document"),
    "budget_history":[{"date":"2019-05","amount":1700000,"label":"Contract awarded","src":"soury-avac"}],
    "milestones":[
      {"name":"Contract awarded","planned":None,"actual":"2019-05-01"},
      {"name":"Upgrade complete","planned":"2019-11 (six months, as announced)","actual":None,
       "note":"No completion announcement found. Seven years on."},
    ],
    "promised":"'At least 30 more years of automated waste collection.'",
    "src":"soury-avac",
  }],
  inspections=U("not_published"),
  attributes={
    "pipe_length": V("~3 miles (nearly 5 km) of buried pipe","envac-50","official_document"),
    "pipe_diameter": V("20 inches","soury-avac","official_document"),
    "annual_capacity": V("~2,555 tonnes of waste per year","envac-50","official_document"),
    "throughput": V("~5 tons of trash per day, moving at ~60 mph","npr-avac","single_source"),
    "designed_for": V("The four original WIRE buildings: Westview, Island House, Rivercross, Eastwood (now Roosevelt Landings)","rilighthouse","single_source"),
    "currently_serving": V("The four original buildings plus six in Manhattan Park, nine in Southtown, and The Octagon. Island population has roughly doubled.","rilighthouse","single_source"),
    "capacity_evaluation": U("not_found","'There is no public record showing whether the system was ever evaluated for that kind of expansion.' — journalist David Stone, quoted in RI Lighthouse."),
    "peer_systems": V("One of only two city-scale AVAC systems in the US. The other serves Walt Disney World.","rioc-status","official_document"),
  },
  connected=["cop:obj:us-ny-36061:westview","cop:obj:us-ny-36061:island-house","cop:obj:us-ny-36061:rivercross","cop:obj:us-ny-36061:roosevelt-landings","cop:obj:us-ny-36061:octagon"],
  history=[
    {"t":"1970","what":"Pneumatic collection for Welfare Island made public in the 'Interim Report' exhibition.","src":"fasttrash"},
    {"t":"1975","what":"Installed. The second AVAC in the United States, after Walt Disney World, and the first at urban scale.","src":"rioc-status"},
    {"t":"2010-2011","what":"During the winter blizzards, when NYC garbage trucks are redeployed to plough snow and refuse sits uncollected on city sidewalks for up to three weeks, Roosevelt Island is the only sanitation district in New York with uninterrupted collection.","src":"soury-avac"},
    {"t":"2012","what":"Continues operating through Hurricane Sandy.","src":"soury-avac"},
    {"t":"2019-05-01","what":"RIOC awards Envac Iberia a $1.7M modernization contract. Announced as a six-month project promising 30 more years of service.","src":"soury-avac"},
    {"t":"2025-01-14","what":"Last official RIOC update on AVAC found in the public record.","src":"ridaily-avac"},
    {"t":"2025-04","what":"Local press reports repeated failures and 'minimal' communication from RIOC since January.","src":"ridaily-avac"},
  ],
  flag="Built in 1975 for four buildings. The island has since roughly doubled and the same vacuum backbone now serves twenty. No public record shows the system was ever evaluated for that load. A $1.7M upgrade was announced in 2019 as a six-month job; there is no completion notice seven years later.",
)

# ---- THE BRIDGE -----------------------------------------------------------
obj(
  id="cop:obj:us-ny-36061:ri-bridge",
  type="bridge",
  name="Roosevelt Island Bridge",
  also=["Welfare Island Bridge (1955–1973)"],
  geom={"kind":"line","pts":[[40.7645,-73.9484],[40.7649,-73.9440],[40.7652,-73.9405]],"confidence":"approximate"},
  containment=[
    {"rel":"within","target":"cop:dist:us-ny-36061:roosevelt-island"},
    {"rel":"within","target":"cop:dist:us-ny-36081:astoria","note":"The Queens end. The bridge is in two boroughs."},
    {"rel":"crosses","target":"cop:obj:us-ny-36061:east-river-east-channel"},
  ],
  lifecycle={
    "status": V("in_service","nycdot-bridges","authoritative"),
    "construction_began": V("1952-03-17","wp-bridge","cross_referenced"),
    "opened": V("1955-05-18","wp-bridge","cross_referenced"),
    "renamed": V("1973 — from Welfare Island Bridge","wp-bridge","cross_referenced"),
  },
  ownership={
    "owner": V("City of New York","nycdot-bridges","authoritative"),
    "tenure": V("public","nycdot-bridges","authoritative"),
  },
  responsibility={
    "maintainer": V("NYC Department of Transportation","nycdot-bridges","authoritative"),
    "note":"Note the boundary: NYC DOT owns and maintains the only road onto an island that a New York STATE corporation otherwise runs.",
  },
  finance={
    "construction_cost": V({"amount":6500000,"currency":"USD","year":1955},"wp-bridge","cross_referenced",
                           "There was opposition in the City Council at the time over whether the traffic justified the cost."),
    "annual_maintenance": U("not_published","NYC DOT publishes an annual Bridges & Tunnels Condition Report but does not break out per-bridge maintenance spend in a machine-readable form."),
  },
  projects=[],
  inspections=U("not_found","NYC DOT publishes an annual Bridges & Tunnels Condition Report. The per-structure condition rating for this bridge was not retrievable without the PDF. See GAPS.md."),
  attributes={
    "bridge_type": V("Tower-drive vertical lift","nycdot-bridges","authoritative"),
    "main_span": V("418 ft (127 m)","nycdot-bridges","authoritative"),
    "total_length": V("2,877 ft (877 m) including approaches","wp-bridge","cross_referenced"),
    "tower_height": V("170 ft","structurae","single_source"),
    "clearance_closed": V("40 ft above mean high water","structurae","single_source"),
    "clearance_open": V("100 ft above mean high water","wp-bridge","cross_referenced"),
    "lift_cables": V("48 cables, each with a 200-ton breaking strength","structurae","single_source"),
    "lifts_per_year": V("4–5, mostly during the UN General Assembly in September","wp-bridge","single_source"),
    "significance": V("The only vehicular access to Roosevelt Island.","nycdot-bridges","authoritative"),
  },
  connected=["cop:obj:us-ny-36061:motorgate","cop:obj:us-ny-36061:main-street"],
  history=[
    {"t":"1930","what":"Before the bridge, vehicles reach the island only by a four-cab elevator from the Queensboro Bridge.","src":"structurae"},
    {"t":"1952-03-17","what":"Construction begins, over City Council objections about the $6.5M cost.","src":"structurae"},
    {"t":"1955-05-18","what":"Opens as the Welfare Island Bridge.","src":"wp-bridge"},
    {"t":"1970","what":"The Queensboro Bridge elevator is demolished.","src":"wp-bridge"},
    {"t":"1973","what":"Renamed the Roosevelt Island Bridge.","src":"wp-bridge"},
    {"t":"2001","what":"NYC DOT considers converting it to a fixed bridge to cut maintenance cost. It does not happen; no public record found of why.","src":"wp-bridge"},
  ],
  flag="A single point of failure: one 1955 lift bridge is the only way to drive onto an island of 12,000 people. No published condition rating was retrievable.",
)

# ---- CORNELL TECH ---------------------------------------------------------
obj(
  id="cop:obj:us-ny-36061:cornell-tech",
  type="campus",
  name="Cornell Tech Campus",
  also=["Cornell NYC Tech"],
  geom={"kind":"poly","pts":[[40.7540,-73.9565],[40.7560,-73.9550],[40.7552,-73.9535],[40.7532,-73.9550]],"confidence":"approximate"},
  containment=[{"rel":"within","target":"cop:dist:us-ny-36061:roosevelt-island"}],
  lifecycle={
    "status": V("in_service — phased build-out continuing","wp-cornell","official_document"),
    "site_selected": V("2011 — winner of the Bloomberg administration's Applied Sciences Competition","cornell-open","official_document"),
    "construction_began": V("2015","wp-cornell","cross_referenced"),
    "phase_1_opened": V("2017-09-13","cornell-open","authoritative"),
    "full_buildout": C([
      {"value":"12 acres by 2037","src":"wp-cornell"},
      {"value":"final phase scheduled for 2045","src":"wp-ri"},
    ],"Two different completion horizons, eight years apart."),
  },
  ownership={
    "owner": V("Cornell University (with Technion — Israel Institute of Technology)","wp-cornell","authoritative"),
    "tenure": V("private institution on city-owned land","wp-cornell","cross_referenced",
                "SCHEMA PROBLEM: is this a public object or a private one? See SCHEMA_NOTES.md."),
    "land": V("Site of the former Goldwater Memorial Hospital, a city facility that closed in 2013 and was demolished.","wp-ri","cross_referenced"),
  },
  responsibility={
    "operator": V("Cornell University","wp-cornell","authoritative"),
    "land_agreement": U("not_found","The city–Cornell agreement governing the land is referenced everywhere and published nowhere we could find."),
  },
  finance={
    "construction_cost": V({"amount":2000000000,"currency":"USD","year":2017},"constrdive","cross_referenced",
      "$2 billion is the figure used consistently by the city, the press and Cornell. What is NOT public is the breakdown: how much is public money, how much philanthropic, how much Cornell's own."),
    "public_contribution": U("not_found","The city's contribution — in land value, tax treatment, and infrastructure — is not stated in any source found. The land was city-owned and is worth a great deal."),
    "largest_gift": V("$350M from Atlantic Philanthropies (Charles Feeney)","wp-cornell","cross_referenced"),
    "promised_benefit": V("The winning bid promised 28,000 jobs, 600 incubated companies, $23bn in economic benefit and $1.4bn in taxes over 30 years.","wp-cornell","single_source",
      "No public accounting against these promises was found. The bid is nine years old."),
  },
  projects=[],
  inspections=U("not_applicable"),
  attributes={
    "site_area": C([
      {"value":"12.4 acres (master plan)","src":"som"},
      {"value":"11 acres","src":"wp-ri"},
      {"value":"12 acres","src":"constrdive"},
    ]),
    "phase_1_area": V("5 acres, opened 2017","wp-cornell","cross_referenced"),
    "planned_floor_area": V("~2 million sq ft at full build-out","som","official_document"),
    "master_architect": V("SOM (Skidmore, Owings & Merrill), with James Corner Field Operations","som","authoritative"),
    "bloomberg_center": V("4 storeys, 160,000 sq ft; designed as one of the largest net-zero-energy buildings in the country","constrdive","cross_referenced"),
  },
  connected=["cop:obj:us-ny-36061:tram","cop:obj:us-ny-36061:southpoint-park"],
  history=[
    {"t":"2011","what":"Cornell/Technion win the city's Applied Sciences Competition. Stanford withdraws.","src":"wp-cornell"},
    {"t":"2013","what":"Goldwater Memorial Hospital — a public hospital — closes to make way for the campus.","src":"wp-ri"},
    {"t":"2015","what":"Construction begins.","src":"wp-cornell"},
    {"t":"2017-09-13","what":"Phase 1 opens. Attended by the Governor, the Mayor, and the former Mayor who initiated it.","src":"cornell-open"},
  ],
  flag="A public hospital was demolished to build a private university on public land, for $2 billion, against promises of 28,000 jobs. The promises are public. Any accounting against them is not.",
)

# ---- FOUR FREEDOMS PARK ---------------------------------------------------
obj(
  id="cop:obj:us-ny-36061:four-freedoms-park",
  type="park",
  name="Franklin D. Roosevelt Four Freedoms Park",
  geom={"kind":"poly","pts":[[40.7500,-73.9590],[40.7512,-73.9582],[40.7506,-73.9572],[40.7496,-73.9581]],"confidence":"approximate"},
  containment=[{"rel":"within","target":"cop:dist:us-ny-36061:roosevelt-island"}],
  lifecycle={
    "status": V("open","wp-ri","cross_referenced"),
    "designed": V("1974, by Louis Kahn","wp-ri","authoritative","Kahn died in 1974. The park was built 38 years later."),
    "groundbreaking": V("2009-05-28","wp-smallpox","cross_referenced"),
    "opened": V("2012","wp-ri","cross_referenced"),
  },
  ownership={
    "owner": V("New York State Park","wp-ri","cross_referenced"),
    "tenure": V("public","wp-ri","cross_referenced"),
  },
  responsibility={
    "operator": V("Franklin D. Roosevelt Four Freedoms Park, LLC","almanack","single_source",
                  "A separate LLC operates a state park. Its governance and finances were not found."),
  },
  finance={
    "construction_cost": U("not_found","No construction cost for the park was found in any public source. It is a state park built by an LLC after a 38-year gap."),
    "annual_maintenance": U("not_found"),
  },
  projects=[],
  inspections=U("not_applicable"),
  attributes={
    "area": V("4 acres (1.6 ha)","wp-ri","cross_referenced"),
    "architect": V("Louis Kahn","wp-ri","authoritative"),
    "form": V("Two converging rows of trees leading to a granite 'room' at the island's southern tip.","wp-ri","cross_referenced"),
  },
  connected=["cop:obj:us-ny-36061:southpoint-park","cop:obj:us-ny-36061:renwick-ruin"],
  history=[
    {"t":"1974","what":"Louis Kahn completes the design. He dies the same year. The project stalls for a generation.","src":"wp-ri"},
    {"t":"2009-05-28","what":"Ground broken, 35 years later.","src":"wp-smallpox"},
    {"t":"2012","what":"Opens.","src":"wp-ri"},
  ],
  flag=None,
)

# ---- SOUTHPOINT PARK ------------------------------------------------------
obj(
  id="cop:obj:us-ny-36061:southpoint-park",
  type="park",
  name="Southpoint Park",
  geom={"kind":"poly","pts":[[40.7512,-73.9582],[40.7535,-73.9568],[40.7528,-73.9556],[40.7506,-73.9572]],"confidence":"approximate"},
  containment=[{"rel":"within","target":"cop:dist:us-ny-36061:roosevelt-island"}],
  lifecycle={
    "status": V("open","wp-ri","cross_referenced"),
    "reopened": V("2011","wp-ri","cross_referenced"),
  },
  ownership={"owner": V("RIOC","rioc-status","official_document"), "tenure": V("public","rioc-status","official_document")},
  responsibility={"maintainer": V("RIOC","rioc-status","official_document")},
  finance={
    "construction_cost": U("not_found"),
    "shoreline_restoration_cost": U("not_published",
      "RIOC publicised the Southpoint Park Shoreline Restoration as an award-winning project (ACEC New York, 2024 Platinum). The award is public. The cost is not."),
  },
  projects=[{
    "id":"cop:proj:us-ny-36061:southpoint-shoreline",
    "title":"Southpoint Park Shoreline Restoration",
    "status":"completed",
    "contractor": V("Langan (design)","rioc-news","official_document"),
    "budget_history":[],
    "milestones":[{"name":"ACEC New York Engineering Excellence Platinum Award","planned":None,"actual":"2024"}],
    "note":"RIOC's own account: the seawall 'was failing'.",
    "src":"rioc-news",
  }],
  inspections=U("not_applicable"),
  attributes={
    "area": V("7 acres (2.8 ha)","wp-ri","cross_referenced"),
    "contains": V("Strecker Memorial Laboratory and the Smallpox Hospital ruin","wp-ri","cross_referenced"),
  },
  connected=["cop:obj:us-ny-36061:renwick-ruin","cop:obj:us-ny-36061:four-freedoms-park"],
  history=[{"t":"2011","what":"Reopens, redesigned alongside the Four Freedoms Park works.","src":"wp-ri"}],
  flag="A press release for the award. No figure for the work.",
)

# ---- STUBS: rendered, honest, unresearched --------------------------------
STUBS = [
  ("blackwell-house","Blackwell House","landmark_building",[40.7597,-73.9518],"NYC landmark. Restored by RIOC; restoration cost not researched."),
  ("blackwell-lighthouse","Blackwell Island Light","lighthouse",[40.7712,-73.9428],"NYC landmark, 1872. Restored by RIOC; cost not researched."),
  ("strecker-lab","Strecker Memorial Laboratory","landmark_building",[40.7522,-73.9563],"NYC landmark. Now an MTA power conversion substation — a landmark repurposed as infrastructure."),
  ("chapel-good-shepherd","Chapel of the Good Shepherd","landmark_building",[40.7605,-73.9512],"NYC landmark, 1889. Now the Good Shepherd Community Center — where the RIOC board meets."),
  ("octagon","The Octagon","residential",[40.7688,-73.9450],"Former Lunatic Asylum rotunda, 1839. NYC landmark, converted to housing by Becker+Becker."),
  ("westview","Westview","residential",[40.7616,-73.9527],"One of the four original WIRE buildings. Mitchell-Lama."),
  ("island-house","Island House","residential",[40.7607,-73.9516],"One of the four original WIRE buildings."),
  ("rivercross","Rivercross","residential",[40.7600,-73.9508],"One of the four original WIRE buildings."),
  ("roosevelt-landings","Roosevelt Landings","residential",[40.7622,-73.9515],"Formerly Eastwood. One of the four original WIRE buildings."),
  ("manhattan-park","Manhattan Park","residential",[40.7650,-73.9478],"Six buildings. Northtown II, completed 1989."),
  ("southtown","Southtown (Riverwalk)","residential",[40.7570,-73.9548],"Nine buildings, developed in the 2000s–2010s."),
  ("ri-subway","Roosevelt Island Station (F)","subway_station",[40.7591,-73.9530],"MTA. One of the deepest stations in the system."),
  ("motorgate","Motorgate Garage","parking",[40.7641,-73.9491],"RIOC. The island's main garage, at the bridge landing."),
  ("main-street","Main Street","street",[40.7610,-73.9510],"The island's spine. RIOC-maintained."),
  ("tram-plaza","Tramway Plaza","public_space",[40.7573,-73.9539],"RIOC."),
  ("lighthouse-park","Lighthouse Park","park",[40.7705,-73.9435],"RIOC. Northern tip."),
  ("octagon-park","Octagon Park","park",[40.7675,-73.9460],"RIOC. 15 acres."),
  ("ps-is-217","PS/IS 217 Roosevelt Island School","school",[40.7628,-73.9503],"NYC Department of Education. The island's only public school."),
  ("coler","Coler Hospital","hospital",[40.7695,-73.9448],"NYC Health + Hospitals. Long-term care."),
  ("sportspark","Sportspark","recreation",[40.7560,-73.9545],"RIOC. Pool and fitness facility."),
  ("seawall","The Seawall","coastal_defence",[40.7600,-73.9500],"RIOC. Encircles the island. Sections reported as failing."),
  ("promenade","Waterfront Promenade","public_space",[40.7620,-73.9495],"RIOC. Circles the island."),
]
for sid, name, typ, pt, note in STUBS:
    obj(
      id=f"cop:obj:us-ny-36061:{sid}", type=typ, name=name, tier=2,
      geom={"kind":"point","pts":[pt],"confidence":"approximate"},
      containment=[{"rel":"within","target":"cop:dist:us-ny-36061:roosevelt-island"}],
      lifecycle={"status": U("not_yet_researched")},
      ownership={"owner": U("not_yet_researched")},
      responsibility={},
      finance={"construction_cost": U("not_yet_researched"), "annual_maintenance": U("not_yet_researched")},
      projects=[], inspections=U("not_yet_researched"), attributes={}, connected=[],
      history=[], flag=None, stub_note=note,
    )

# ---------------------------------------------------------------- INSTITUTIONS
INSTITUTIONS = [
 {
  "id":"cop:inst:us-ny-36061:rioc",
  "name":"Roosevelt Island Operating Corporation",
  "short":"RIOC",
  "type":"state_public_benefit_corporation",
  "mandate": V("To plan, design, develop, operate and maintain Roosevelt Island.","wp-rioc","official_document"),
  "legal_basis": V("Created by the New York State Legislature in 1984 (Chapter 899). Amended 2002 (Chapter 493), which moved the NYS Homes & Community Renewal Commissioner from chief executive to board chair.","nysa-rioc","authoritative"),
  "jurisdiction": V("Roosevelt Island — but not exclusively. NYPD remains the primary police agency; DSNY, MTA, NYC DOT and NYC H+H all retain authority over parts of the island.","wp-rioc","official_document"),
  "governing_document": V("The 1969 General Development Plan, which accompanied the ground lease between New York City and New York State.","almanack","official_document"),
  "budget":[
    {"year":"2017","figure":"$26.09M operating expenses; 175 staff","src":"wp-rioc","tier":"single_source"},
    {"year":"2025–26","figure":"$39.3M projected operating revenue (+1.1%)","src":"wp-rioc","tier":"single_source"},
  ],
  "funding": V("Ground-lease rents from the island's residential developments, residential service fees, and transport/parking fees. Reported as operating without direct state or municipal subsidy.","wp-rioc","single_source"),
  "responsible_for":["cop:obj:us-ny-36061:tram","cop:obj:us-ny-36061:avac","cop:obj:us-ny-36061:renwick-ruin","cop:obj:us-ny-36061:southpoint-park","cop:obj:us-ny-36061:motorgate","cop:obj:us-ny-36061:seawall"],
  "flag":"A New York STATE corporation runs an island that is, for every other purpose — courts, elections, the post office — in New York CITY. Its board is appointed by the Governor. Nobody on Roosevelt Island elects it.",
 },
 {
  "id":"cop:inst:us-ny:nyc-dot",
  "name":"New York City Department of Transportation",
  "short":"NYC DOT",
  "type":"city_agency",
  "mandate": V("Owns and maintains the Roosevelt Island Bridge.","nycdot-bridges","authoritative"),
  "legal_basis": U("not_researched"),
  "jurisdiction": V("The bridge only. A city agency's asset inside a state corporation's territory.","nycdot-bridges","authoritative"),
  "governing_document": U("not_researched"),
  "budget":[],
  "funding": U("not_researched"),
  "responsible_for":["cop:obj:us-ny-36061:ri-bridge"],
  "flag":None,
 },
 {
  "id":"cop:inst:us-ny:dsny",
  "name":"New York City Department of Sanitation",
  "short":"DSNY",
  "type":"city_agency",
  "mandate": V("Described in multiple sources as the operator of AVAC for 40+ years — a system RIOC owns.","soury-avac","official_document"),
  "legal_basis": U("not_researched"),
  "jurisdiction": V("Contested. See the AVAC passport.","ridaily-avac","contested"),
  "governing_document": U("not_found","No published agreement between RIOC and DSNY governing AVAC operation was found."),
  "budget":[],
  "funding": U("not_researched"),
  "responsible_for":["cop:obj:us-ny-36061:avac"],
  "flag":"DSNY operates a system it does not own, under an agreement that is not published.",
 },
 {
  "id":"cop:inst:us-ny:mta",
  "name":"Metropolitan Transportation Authority",
  "short":"MTA",
  "type":"state_authority",
  "mandate": V("Operates the Roosevelt Island subway station (F). Collects the tram fare via OMNY. Does NOT operate the tram.","wp-tram","official_document"),
  "legal_basis": U("not_researched"),
  "jurisdiction": V("The subway station; the fare system; the Strecker Lab substation.","wp-ri","cross_referenced"),
  "governing_document": U("not_researched"),
  "budget":[],
  "funding": U("not_researched"),
  "responsible_for":["cop:obj:us-ny-36061:ri-subway","cop:obj:us-ny-36061:strecker-lab"],
  "flag":"A common error: the MTA does not run the tram. It takes the fare.",
 },
 {
  "id":"cop:org:fr:leitner-poma",
  "name":"Leitner-Poma of America (POMA Group)",
  "short":"Leitner-Poma",
  "type":"private_contractor",
  "mandate": V("Design-build contractor for the 2010 tram modernization; operator of the tram under contract to RIOC since 2010, renewed 2019.","poma","official_document"),
  "legal_basis": U("not_applicable"),
  "jurisdiction": V("Operates a piece of American public transit infrastructure under a renewable commercial contract. The contract is not published.","poma","official_document"),
  "governing_document": U("not_found","The RIOC–Leitner-Poma operating agreement was not found in public sources."),
  "budget":[],
  "funding": U("not_applicable"),
  "responsible_for":["cop:obj:us-ny-36061:tram"],
  "flag":"A French cable-car manufacturer operates New York's aerial tramway under a contract nobody outside RIOC has read.",
 },
 {
  "id":"cop:org:se:envac",
  "name":"Envac (Envac Iberia)",
  "short":"Envac",
  "type":"private_contractor",
  "mandate": V("Installed AVAC in 1975. Awarded a $1.7M modernization contract by RIOC in 2019.","soury-avac","official_document"),
  "legal_basis": U("not_applicable"),
  "jurisdiction": U("not_applicable"),
  "governing_document": U("not_found"),
  "budget":[],
  "funding": U("not_applicable"),
  "responsible_for":["cop:obj:us-ny-36061:avac"],
  "flag":None,
 },
]

# ---------------------------------------------------------------- OFFICES
OFFICES = [
 {
  "id":"cop:office:us-ny-36061:rioc-president",
  "title":"President & Chief Executive Officer, RIOC",
  "institution":"cop:inst:us-ny-36061:rioc",
  "appointed_by": V("The RIOC Board of Directors, in accordance with its bylaws.","nysa-rioc","authoritative"),
  "powers":["Executive management of all island operations","Capital project delivery","Procurement","Public Safety Department"],
  "occupancies":[
    {"name":"B.J. Jones","from":"2024-08","to":None,
     "src":"wp-rioc",
     "record":{
       "projects_under_authority":[],
       "inherited":["cop:proj:us-ny-36061:avac-upgrade-2019","cop:proj:us-ny-36061:renwick-stabilisation"],
       "bequeathed":[],
       "aggregates":{
         "projects_completed_on_schedule": U("not_computable"),
         "projects_completed_late": U("not_computable"),
         "note":"NOT COMPUTABLE. The aggregate requires a complete, dated, attributed project register. RIOC does not publish one. This emptiness is the finding — the derived record is only as good as the project data beneath it, and there is none.",
       },
       "method":"cop:doc:aggregation-v1 (not yet implemented — see SCHEMA_NOTES.md)",
     }},
    {"name":"Shelton J. Haynes","from":U("not_found"),"to":"2024 (approx.)",
     "src":"rioc-news",
     "record":{
       "projects_under_authority":["cop:proj:us-ny-36061:southpoint-shoreline","cop:proj:us-ny-36061:avac-upgrade-2019"],
       "inherited":[], "bequeathed":["cop:proj:us-ny-36061:avac-upgrade-2019"],
       "aggregates":{"note":"NOT COMPUTABLE — see above."},
       "method":"cop:doc:aggregation-v1",
     }},
    {"name":"Susan Rosenthal","from":U("not_found"),"to":U("not_found"),
     "src":"cornell-open",
     "record":{"projects_under_authority":[],"inherited":[],"bequeathed":[],
               "aggregates":{"note":"NOT COMPUTABLE — see above."},"method":"cop:doc:aggregation-v1"}},
    {"name":"Leslie Torres","from":U("not_found"),"to":U("not_found"),
     "src":"almanack",
     "record":{"projects_under_authority":["cop:proj:us-ny-36061:tram-modernization"],
               "inherited":[],"bequeathed":[],
               "aggregates":{"note":"NOT COMPUTABLE — see above."},"method":"cop:doc:aggregation-v1"}},
  ],
  "flag":"Four presidents are identifiable from press releases. Their term dates are not published anywhere as a series. To attribute a project to a president, you must reconstruct the timeline from news items — which is exactly the work this platform exists to make unnecessary.",
 },
 {
  "id":"cop:office:us-ny-36061:rioc-board",
  "title":"RIOC Board of Directors",
  "institution":"cop:inst:us-ny-36061:rioc",
  "appointed_by": V("Nominated by the Governor of New York, with the advice and consent of the State Senate. The Chair sits ex officio as Commissioner of NYS Homes & Community Renewal.","rioc-board","authoritative"),
  "powers":["Appoints the President/CEO","Approves the capital programme","Approves contracts","Approves the budget"],
  "occupancies":[
    {"name":"RuthAnne Visnauskas — Chair (ex officio, Commissioner, NYS Homes & Community Renewal)","from":U("not_found"),"to":None,"src":"rioc-board",
     "record":{"projects_under_authority":[],"inherited":[],"bequeathed":[],"aggregates":{"note":"NOT COMPUTABLE."},"method":"cop:doc:aggregation-v1"}},
    {"name":"Blake G. Washington (ex officio, Director of the State Budget)","from":U("not_found"),"to":None,"src":"rioc-board",
     "record":{"projects_under_authority":[],"inherited":[],"bequeathed":[],"aggregates":{"note":"NOT COMPUTABLE."},"method":"cop:doc:aggregation-v1"}},
    {"name":"Fay Christian","from":U("not_found"),"to":"term expires 2026-05-19","src":"rioc-board",
     "record":{"projects_under_authority":[],"inherited":[],"bequeathed":[],"aggregates":{"note":"NOT COMPUTABLE."},"method":"cop:doc:aggregation-v1"}},
    {"name":"Conway Ekpo","from":U("not_found"),"to":"term expired 2025-06-10","src":"rioc-board",
     "record":{"projects_under_authority":[],"inherited":[],"bequeathed":[],"aggregates":{"note":"NOT COMPUTABLE."},"method":"cop:doc:aggregation-v1"}},
    {"name":"Prof. Lydia W. Tang","from":U("not_found"),"to":"term expired 2025-07-01","src":"rioc-board",
     "record":{"projects_under_authority":[],"inherited":[],"bequeathed":[],"aggregates":{"note":"NOT COMPUTABLE."},"method":"cop:doc:aggregation-v1"}},
    {"name":"Dr. Michal L. Melamed","from":U("not_found"),"to":"term expired 2024-06-10","src":"rioc-board",
     "record":{"projects_under_authority":[],"inherited":[],"bequeathed":[],"aggregates":{"note":"NOT COMPUTABLE."},"method":"cop:doc:aggregation-v1"}},
    {"name":"Marc Jonas Block","from":U("not_found"),"to":U("not_found"),"src":"rioc-board",
     "record":{"projects_under_authority":[],"inherited":[],"bequeathed":[],"aggregates":{"note":"NOT COMPUTABLE."},"method":"cop:doc:aggregation-v1"}},
  ],
  "flag":"Read the term dates. As recorded in the most recent public listing found, at least three board members' terms had already expired — one in June 2024, over two years ago. Whether they have been reappointed, replaced, or are simply still sitting is not stated in any public document we could find. This is the single most concrete accountability finding in the pilot, and it took one query.",
 },
]

# ---------------------------------------------------------------- REVISION
def revision(payload):
    h = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:12]
    return {"id":h,"parent":None,"valid_from":"2026-07-13","recorded_at":"2026-07-13T00:00:00Z",
            "author":"cop:ingest:manual-pilot-001",
            "note":"Genesis revision. Manually compiled from public sources. Tier: mixed. No automated adapter exists yet."}

for o in OBJECTS:
    o["revision"] = revision(o)
    o["retrieved"] = RET

DATA = {
  "meta":{
    "name":"Cities On Palm — Roosevelt Island pilot",
    "version":"prototype-0.1",
    "built":RET,
    "jurisdiction":"cop:dist:us-ny-36061:roosevelt-island",
    "warning":"Manually compiled. No automated ingestion. Geometry is approximate throughout. Read GAPS.md before trusting any number here.",
  },
  "sources":SOURCES,
  "objects":OBJECTS,
  "institutions":INSTITUTIONS,
  "offices":OFFICES,
}

os.makedirs("data", exist_ok=True)
with open("data/passports.js","w") as f:
    f.write("// Cities On Palm — pilot data. Stands in for the read-only API.\n")
    f.write("// In production this is a fetch() against a static JSON endpoint.\n")
    f.write("window.COP = ")
    json.dump(DATA, f, indent=1, default=str)
    f.write(";\n")

with open("data/passports.json","w") as f:
    json.dump(DATA, f, indent=2, default=str)

print(f"objects: {len(OBJECTS)} (tier1: {sum(1 for o in OBJECTS if o['tier']==1)}, tier2: {sum(1 for o in OBJECTS if o['tier']==2)})")
print(f"institutions: {len(INSTITUTIONS)}  offices: {len(OFFICES)}  sources: {len(SOURCES)}")
