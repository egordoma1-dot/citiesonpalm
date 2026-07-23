#!/usr/bin/env python3
"""Pre-renders table.html as static HTML. Works with JavaScript disabled.
This is not a fallback. It is the surface a researcher will actually use,
and the one that works on a ten-year-old phone."""
import json, html

D = json.load(open("data/passports.json"))
S = D["sources"]
E = html.escape

def src(k):
    s = S.get(k)
    return f'<a href="{E(s["uri"])}">{E(s["name"])}</a>' if s else ""

def cell(v):
    if v is None: return "—"
    if isinstance(v, str): return E(v)
    if not isinstance(v, dict): return E(str(v))
    if v.get("status") == "unknown":
        n = f'<br><i>{E(v["note"])}</i>' if v.get("note") else ""
        return f'<b class="u">UNKNOWN</b> — {E(v["reason"])}{n}'
    if v.get("status") == "contested":
        ps = "".join(f'<li>{E(p["value"])} — {src(p["src"])}</li>' for p in v["positions"])
        n = f'<i>{E(v["note"])}</i>' if v.get("note") else ""
        return f'<b class="u">CONTESTED</b><ul>{ps}</ul>{n}'
    val = v.get("value")
    if isinstance(val, dict) and "amount" in val:
        val = f'${val["amount"]:,} {val["currency"]} ({val["year"]})'
    n = f'<br><i>{E(v["note"])}</i>' if v.get("note") else ""
    return f'{E(str(val))}<br><small>[{E(v.get("tier",""))}] {src(v.get("source"))}</small>{n}'

rows = []
for o in D["objects"]:
    fields = []
    for grp in ("lifecycle", "ownership", "responsibility", "finance", "attributes"):
        for k, v in (o.get(grp) or {}).items():
            if k == "note":
                fields.append(f"<tr><th>note</th><td><i>{E(v)}</i></td></tr>")
            else:
                fields.append(f"<tr><th>{E(k.replace('_',' '))}</th><td>{cell(v)}</td></tr>")
    fields.append(f'<tr><th>inspections</th><td>{cell(o.get("inspections"))}</td></tr>')

    projs = ""
    for p in o.get("projects", []):
        ms = "".join(
            f'<tr><td>{E(m["name"])}</td><td>{E(str(m.get("planned") or "—"))}</td>'
            f'<td>{E(str(m.get("actual") or "never"))}</td></tr>'
            for m in p.get("milestones", []))
        projs += (f'<h4>Project — {E(p["title"])}</h4>'
                  f'<table><tr><th>status</th><td>{cell(p.get("status"))}</td></tr>'
                  f'<tr><th>contractor</th><td>{cell(p.get("contractor"))}</td></tr></table>'
                  + (f'<table><tr><th>Milestone</th><th>Planned</th><th>Actual</th></tr>{ms}</table>' if ms else ""))

    hist = "".join(f'<tr><td>{E(e["t"])}</td><td>{E(e["what"])} <small>{src(e.get("src"))}</small></td></tr>'
                   for e in o.get("history", []))
    flag = f'<p class="flag"><b>Finding.</b> {E(o["flag"])}</p>' if o.get("flag") else ""
    stub = f'<p class="flag"><b>Stub — not yet researched.</b> {E(o.get("stub_note",""))}</p>' if o["tier"] == 2 else ""

    rows.append(f"""
<section id="{E(o['id'])}">
<h2>{E(o['name'])}</h2>
<p class="id">{E(o['id'])} · {E(o['type'])} · geometry: {E(o['geom']['confidence'])}</p>
{stub}{flag}
<table>{''.join(fields)}</table>
{projs}
{f'<h4>Lifetime</h4><table>{hist}</table>' if hist else ''}
<p class="rev">revision {E(o['revision']['id'])} · valid_from {E(o['revision']['valid_from'])} · recorded_at {E(o['revision']['recorded_at'])}</p>
</section>""")

insts = ""
for i in D["institutions"]:
    f = "".join(f'<tr><th>{E(k)}</th><td>{cell(i[k])}</td></tr>'
                for k in ("mandate", "legal_basis", "jurisdiction", "governing_document", "funding"))
    b = "".join(f'<tr><th>budget {E(x["year"])}</th><td>{E(x["figure"])} <small>{src(x["src"])}</small></td></tr>'
                for x in i.get("budget", []))
    fl = f'<p class="flag"><b>Finding.</b> {E(i["flag"])}</p>' if i.get("flag") else ""
    insts += f'<section><h2>{E(i["name"])}</h2><p class="id">{E(i["id"])}</p>{fl}<table>{f}{b}</table></section>'

offs = ""
for o in D["offices"]:
    occ = ""
    for c in o["occupancies"]:
        fr = c["from"]["reason"] if isinstance(c["from"], dict) else c["from"]
        to = c["to"]["reason"] if isinstance(c.get("to"), dict) else (c.get("to") or "present")
        cls = ' class="u"' if "expired" in str(to) else ""
        occ += f'<tr><td>{E(c["name"])}</td><td{cls}>{E(str(fr))} → {E(str(to))}</td></tr>'
    fl = f'<p class="flag"><b>Finding.</b> {E(o["flag"])}</p>' if o.get("flag") else ""
    offs += (f'<section><h2>{E(o["title"])}</h2><p class="id">{E(o["id"])}</p>{fl}'
             f'<table><tr><th>appointed by</th><td>{cell(o["appointed_by"])}</td></tr></table>'
             f'<h4>Occupancy</h4><table>{occ}</table>'
             f'<p class="rev">DERIVED RECORD — computed, never written. Aggregates are not computable: '
             f'no complete, dated, attributed project register is published. The emptiness is the finding.</p></section>')

out = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cities On Palm — Roosevelt Island — full record</title>
<meta name="referrer" content="no-referrer">
<style>
:root{{--ink:#14171A;--grey:#6E736C;--rule:#B4B8B0;--paper:#E7E9E3;--red:#B0242A}}
body{{background:var(--paper);color:var(--ink);max-width:56em;margin:0 auto;padding:24px 18px 90px;
 font:15px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}
h1{{font:600 22px/1.2 ui-monospace,Menlo,monospace;letter-spacing:.06em;text-transform:uppercase}}
.lede{{color:var(--grey);max-width:60ch;margin:10px 0 26px}}
section{{border-top:1px solid var(--rule);padding-top:16px;margin-top:26px}}
h2{{font-size:19px;margin-bottom:2px}}
h4{{font:600 11px/1 ui-monospace,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;
 color:var(--grey);margin:18px 0 6px}}
.id{{font:11px ui-monospace,Menlo,monospace;color:var(--grey);margin-bottom:10px}}
.rev{{font:10.5px ui-monospace,Menlo,monospace;color:var(--grey);margin-top:12px}}
.flag{{border-left:3px solid var(--red);background:rgba(176,36,42,.05);padding:8px 11px;margin:10px 0;font-size:14px}}
table{{border-collapse:collapse;width:100%;margin:8px 0}}
th,td{{text-align:left;vertical-align:top;padding:5px 9px 5px 0;border-bottom:1px dotted var(--rule);font-size:13.5px}}
th{{font:400 11px ui-monospace,Menlo,monospace;color:var(--grey);width:150px;white-space:nowrap}}
small{{font:10.5px ui-monospace,Menlo,monospace;color:var(--grey)}}
i{{color:var(--grey);font-size:12.5px}}
.u{{color:var(--red)}}
a{{color:inherit}}
ul{{margin:4px 0 4px 18px}} li{{font-size:13px;padding:2px 0}}
nav a{{font:11px ui-monospace,Menlo,monospace;text-transform:uppercase;letter-spacing:.1em}}
</style></head><body>
<nav><a href="index.html">← map</a></nav>
<h1>Roosevelt Island — full record</h1>
<p class="lede">Every object, every field, every source. This page contains no JavaScript, makes no third-party
requests, and sets no cookies. It works with scripting disabled. It is not a fallback — it is the surface
a researcher will actually use.</p>
<p class="lede"><b>{sum(1 for o in D['objects'] if o['tier']==1)} researched objects · {sum(1 for o in D['objects'] if o['tier']==2)} stubs ·
{len(D['institutions'])} institutions · {len(D['offices'])} offices · {len(S)} sources.</b><br>
Nothing here is invented. Where the public record has no answer, the field reads UNKNOWN and names what is missing.
Where sources disagree, the field reads CONTESTED and shows both.</p>
<h1 style="font-size:14px;margin-top:34px">Objects</h1>
{''.join(rows)}
<h1 style="font-size:14px;margin-top:44px">Institutions</h1>
{insts}
<h1 style="font-size:14px;margin-top:44px">Offices</h1>
{offs}
</body></html>"""

open("table.html", "w").write(out)
print(f"table.html — {len(out):,} bytes, {len(D['objects'])} objects, no JS")
