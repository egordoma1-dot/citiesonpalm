#!/usr/bin/env python3
"""Replace placeholder geometry with recognisable footprints.

Roosevelt Island runs SSW->NNE. We work in an island-local frame:
  u = metres along the island axis from the southern tip (0 .. ~2800)
  v = metres across  (negative = west / Manhattan side, positive = east / Queens)
and convert to lat/lon so the stored data stays geographic.

Still approximate. Still hand-placed, not surveyed. Every geom keeps
confidence:"approximate" — see GAPS.md. But shapes and positions now
correspond to the real layout well enough to be recognisable.
"""
import json, math

LAT_S, LON_S = 40.7495, -73.9588          # southern tip
BEARING = math.radians(28.4)              # island axis, east of north
CN, CE = math.cos(BEARING), math.sin(BEARING)
M_LAT = 111320.0
M_LON = 111320.0 * math.cos(math.radians(40.76))

def ll(u, v):
    """island-local metres -> [lat, lon]"""
    north = u * CN - v * CE
    east  = u * CE + v * CN
    return [round(LAT_S + north / M_LAT, 6), round(LON_S + east / M_LON, 6)]

def rect(u0, u1, v0, v1):
    return [ll(u0, v0), ll(u1, v0), ll(u1, v1), ll(u0, v1)]

def poly(pts):
    return [ll(u, v) for u, v in pts]

def line(pts):
    return [ll(u, v) for u, v in pts]

# ---------------------------------------------------------------- shoreline
# half-width of the island at a given u
PROFILE = [(0,12),(80,42),(180,78),(320,104),(500,118),(700,126),(900,130),
           (1100,134),(1300,138),(1500,140),(1700,138),(1900,134),(2100,128),
           (2300,116),(2500,96),(2650,66),(2760,34),(2800,10)]

def half_width(u):
    for i in range(len(PROFILE) - 1):
        u0, w0 = PROFILE[i]; u1, w1 = PROFILE[i + 1]
        if u0 <= u <= u1:
            t = (u - u0) / (u1 - u0)
            return w0 + (w1 - w0) * t
    return PROFILE[-1][1]

def shoreline():
    us = [p[0] for p in PROFILE]
    west = [ll(u, -half_width(u)) for u in us]
    east = [ll(u,  half_width(u)) for u in reversed(us)]
    return west + east

# ---------------------------------------------------------------- footprints
# Laid out south -> north. Cross-island: Main St ~v=-15, West Rd ~v=-85, East Rd ~v=+70.
FP = {
 # --- southern tip -------------------------------------------------------
 "four-freedoms-park":  ("poly", poly([(0,10),(60,-52),(180,-74),(200,74),(60,52)])),
 "renwick-ruin":        ("poly", rect(268, 300, -22, 20)),
 "southpoint-park":     ("poly", poly([(200,-76),(560,-116),(560,110),(200,74)])),
 "strecker-lab":        ("poly", rect(470, 496, 34, 66)),

 # --- Cornell Tech (south-west) -----------------------------------------
 "cornell-tech":        ("poly", poly([(430,-120),(800,-128),(800,84),(560,96),(430,20)])),

 # --- tram + transit -----------------------------------------------------
 "tram-plaza":          ("poly", rect(930, 1000, -118, -58)),
 "tram":                ("line", line([(965,-88),(880,-340),(840,-560)])),
 "ri-subway":           ("poly", rect(1150, 1198, -66, -26)),

 # --- Southtown / Riverwalk (9 towers, both sides of Main St) ------------
 "southtown":           ("poly", poly([(880,-126),(1290,-126),(1290,96),(880,60)])),

 # --- civic core ---------------------------------------------------------
 "chapel-good-shepherd":("poly", rect(1336, 1382, -66, -26)),
 "ps-is-217":           ("poly", rect(1300, 1372, 20, 84)),
 "blackwell-house":     ("poly", rect(1392, 1428, -62, -28)),
 "sportspark":          ("poly", rect(1004, 1054, 30, 82)),

 # --- the four WIRE buildings -------------------------------------------
 "rivercross":          ("poly", rect(1418, 1494, -122, -62)),
 "island-house":        ("poly", rect(1508, 1596, -124, -64)),
 "westview":            ("poly", rect(1614, 1706, -126, -66)),
 "roosevelt-landings":  ("poly", poly([(1430,26),(1680,26),(1680,104),(1560,110),(1430,92)])),

 # --- bridge + garage ----------------------------------------------------
 "motorgate":           ("poly", rect(1786, 1874, 40, 122)),
 "ri-bridge":           ("line", line([(1830,120),(1830,300),(1826,470)])),

 # --- Manhattan Park (6 buildings, north-central) ------------------------
 "manhattan-park":      ("poly", poly([(1900,-124),(2160,-124),(2160,110),(1900,104)])),

 # --- north end ----------------------------------------------------------
 "octagon":             ("poly", rect(2196, 2262, -96, -30)),
 "octagon-park":        ("poly", poly([(2170,-118),(2420,-108),(2420,40),(2170,26)])),
 "coler":               ("poly", poly([(2300,44),(2520,44),(2520,104),(2300,110)])),
 "lighthouse-park":     ("poly", poly([(2540,-92),(2800,-10),(2800,10),(2540,88)])),
 "blackwell-lighthouse":("poly", rect(2748, 2768, -12, 8)),

 # --- linear infrastructure ---------------------------------------------
 "main-street":         ("line", line([(900,-16),(1200,-14),(1600,-16),(2000,-14),(2320,-18)])),
 "avac":                ("line", line([(940,-36),(1300,-34),(1700,-36),(2100,-34),(2300,-38)])),
 "promenade":           ("line", line([(240,-70),(900,-118),(1500,-128),(2100,-122),(2600,-72),
                                       (2760,-24),(2600,64),(2100,116),(1500,128),(900,118),(300,66)])),
 "seawall":             ("line", shoreline()),
}

# ---------------------------------------------------------------- basemap
# Context so the island reads as an island. Not part of the passport record —
# a rendering aid, stored separately and marked as such.
BASEMAP = {
  "_note": "Rendering context only. Not passport data. Approximate shapes for orientation.",
  "island":   shoreline(),
  "manhattan": poly([(-400,-300),(-400,-1200),(3400,-1200),(3400,-300),
                     (2600,-330),(1800,-360),(1000,-340),(200,-320)]),
  "queens":    poly([(-400,300),(200,286),(1000,300),(1800,320),(2600,300),(3400,300),
                     (3400,1200),(-400,1200)]),
  "queensboro_bridge": line([(1010,-1150),(1030,-330),(1046,-130),(1052,0),
                             (1058,130),(1070,300),(1090,1150)]),
  "roads": {
    "main_street": line([(900,-16),(1200,-14),(1600,-16),(2000,-14),(2320,-18)]),
    "west_road":   line([(760,-96),(1200,-104),(1700,-108),(2150,-100),(2480,-70)]),
    "east_road":   line([(900,64),(1300,72),(1700,78),(2100,80),(2430,60)]),
    "loop_north":  line([(2430,60),(2560,40),(2600,-20),(2480,-70)]),
    "bridge_ramp": line([(1830,120),(1790,60),(1740,20)]),
  },
}

# ---------------------------------------------------------------- patch
D = json.load(open("data/passports.json"))
patched, missed = 0, []

for o in D["objects"]:
    key = o["id"].split(":")[-1]
    if key in FP:
        kind, pts = FP[key]
        o["geom"] = {"kind": kind, "pts": pts, "confidence": "approximate"}
        if key == "avac":
            o["geom"]["note"] = ("NETWORK GEOMETRY IS NOT PUBLISHED. This line follows Main Street "
                                 "as a placeholder. The actual routing of ~3 miles of buried 20-inch "
                                 "pipe is not in any public dataset found. See SCHEMA_NOTES.md #3.")
        patched += 1
    else:
        missed.append(o["id"])

D["basemap"] = BASEMAP
D["meta"]["warning"] = ("Manually compiled. No automated ingestion. Geometry is approximate throughout — "
                        "hand-placed in an island-local frame, not surveyed. Read GAPS.md before trusting "
                        "any number here.")

json.dump(D, open("data/passports.json", "w"), indent=2)
print(f"patched {patched}/{len(D['objects'])} geometries")
if missed:
    print("no footprint for:", ", ".join(m.split(":")[-1] for m in missed))
