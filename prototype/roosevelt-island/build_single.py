#!/usr/bin/env python3
"""Emit ONE self-contained HTML file. Data inlined. No relative paths.
No fonts, no CDN, no tiles, no analytics. Nothing phones home."""
import json

D = json.load(open("data/passports.json"))
BLOB = json.dumps(D, separators=(",", ":"))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>Cities On Palm — Roosevelt Island</title>
<style>
:root{
  /* panel / document identity */
  --vellum:#DEE0DA;--paper:#FFFFFF;--ink:#202124;--gneiss:#5F6368;
  --rule:#DADCE0;--hair:#E8EAED;--tram:#D93025;--verified:#188038;
  /* Google Maps roadmap palette */
  --g-land:#F8F7F4;--g-water:#A2C8F0;--g-land2:#EEEDE8;
  --g-park:#C9E5B4;--g-park-ink:#3F7A3F;
  --g-bldg:#E9E6E1;--g-bldg-line:#DCD8D1;
  --g-poi:#EFEDE7;--g-poi-line:#E1DED7;
  --g-road:#FFFFFF;--g-road-case:#D6D3CD;
  --g-hwy:#F9D26B;--g-hwy-case:#E8BC55;
  --g-label:#3C4043;--g-label-sub:#5F6368;--g-water-ink:#5A87B0;
  --g-red:#EA4335;--g-blue:#1A73E8;
  --mono:ui-monospace,"SF Mono","Cascadia Mono","Roboto Mono",Menlo,Consolas,monospace;
  --sans:Roboto,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{background:var(--vellum);color:var(--ink);font-family:var(--sans);font-size:15px;
 line-height:1.5;display:flex;flex-direction:column;-webkit-font-smoothing:antialiased}
a{color:inherit}
button{font:inherit;color:inherit;background:none;border:none;cursor:pointer}

header{border-bottom:1px solid var(--rule);padding:10px 16px;display:flex;
 align-items:baseline;gap:14px;flex-wrap:wrap;flex:0 0 auto}
.wordmark{font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase;font-weight:600}
.scope{font-family:var(--mono);font-size:11px;color:var(--gneiss)}
nav{display:flex;gap:2px;margin-left:auto}
nav button{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;
 padding:4px 9px;border:1px solid var(--rule);color:var(--gneiss)}
nav button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}

main{flex:1;display:grid;grid-template-columns:1fr minmax(360px,460px);min-height:0;position:relative}
main.nopanel{grid-template-columns:1fr}
main.nopanel #panel{display:none}
main.wide{grid-template-columns:1fr}
main.wide #mapwrap{display:none}
@media(max-width:860px){
  main{grid-template-columns:1fr;grid-template-rows:1fr 52vh}
  main.nopanel{grid-template-rows:1fr}
}

#mapwrap{position:relative;overflow:hidden;background:var(--g-water);min-height:200px}
svg#map{width:100%;height:100%;display:block;touch-action:none;cursor:grab;background:var(--g-water)}
svg#map:active{cursor:grabbing}

/* ---- basemap: Google roadmap ---- */
.bm-land{fill:var(--g-land2);stroke:none}
.bm-island{fill:var(--g-land);stroke:none}
.bm-qb-case{fill:none;stroke:var(--g-hwy-case);stroke-width:11;stroke-linecap:round;vector-effect:non-scaling-stroke}
.bm-qb{fill:none;stroke:var(--g-hwy);stroke-width:8;stroke-linecap:round;vector-effect:non-scaling-stroke}
.bm-road-case{fill:none;stroke:var(--g-road-case);stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}
.bm-road{fill:none;stroke:var(--g-road);stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}

/* ---- labels: Roboto, white halo, Google greys ---- */
.bm-label{font-family:var(--sans);fill:var(--g-label-sub);pointer-events:none;font-weight:400;
 paint-order:stroke;stroke:#FFFFFF;stroke-width:3.5;stroke-linejoin:round;letter-spacing:.04em}
.bm-label.water{fill:var(--g-water-ink);stroke:none;font-style:italic;letter-spacing:.08em}
.bm-label.place{letter-spacing:.14em;font-weight:400;fill:#6E7276}

/* ---- objects ---- */
.obj{cursor:pointer}
.obj .hit{fill:transparent;stroke:transparent;stroke-width:18;vector-effect:non-scaling-stroke}
.obj .mark{vector-effect:non-scaling-stroke}

.obj.building .mark{fill:var(--g-bldg);stroke:var(--g-bldg-line);stroke-width:1}
.obj.civic   .mark{fill:var(--g-poi);stroke:var(--g-poi-line);stroke-width:1}
.obj.park    .mark{fill:var(--g-park);stroke:none}
.obj.ruin    .mark{fill:#E2DCD2;stroke:#C9C2B6;stroke-width:1}
.obj.water_edge .mark{fill:none;stroke:#CFCCC5;stroke-width:1.2}
.obj.roadline   .mark{fill:none;stroke:var(--g-road);stroke-width:6;stroke-linecap:round}
.obj.cable      .mark{fill:none;stroke:#9AA0A6;stroke-width:1.8;stroke-dasharray:6 5}
.obj.buried     .mark{fill:none;stroke:#B9B4AA;stroke-width:3;stroke-dasharray:5 4}
.obj.bridgeline .mark{fill:none;stroke:var(--g-hwy);stroke-width:7;stroke-linecap:round}
.obj.node       .mark{fill:#FFFFFF;stroke:#9AA0A6;stroke-width:1.6}

.obj.flagged .mark{stroke:var(--g-red);stroke-width:1.6}
.obj.flagged.park .mark{stroke:var(--g-red)}
.obj:hover .mark{stroke:var(--g-red);stroke-width:2.2}
.obj.on .mark{stroke:var(--g-red);stroke-width:3}
.obj.on.building .mark,.obj.on.civic .mark{fill:#F6DEDB}
.obj.on.park .mark{fill:#D9E8C4}

.olabel{font-family:var(--sans);font-size:11px;fill:var(--g-label);pointer-events:none;
 paint-order:stroke;stroke:#FFFFFF;stroke-width:3.2;stroke-linejoin:round;font-weight:400}
.obj.park .olabel{fill:var(--g-park-ink)}
.obj.t2 .olabel{font-size:10px;fill:var(--g-label-sub);opacity:0}
svg.z2 .obj.t2 .olabel{opacity:1}
.obj:hover .olabel,.obj.on .olabel{fill:var(--g-red);font-weight:500;opacity:1}

/* ---- controls: Google chrome ---- */
.zoomer{position:absolute;right:10px;bottom:96px;display:flex;flex-direction:column;
 background:#FFFFFF;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.3);overflow:hidden}
.zoomer button{width:40px;height:40px;border:none;background:#FFFFFF;color:#666;
 font-family:var(--sans);font-size:22px;line-height:1;font-weight:300;display:flex;
 align-items:center;justify-content:center}
.zoomer button:hover{color:#111}
.zoomer button+button{border-top:1px solid #E6E6E6}
.attrib{position:absolute;left:0;bottom:0;right:0;background:rgba(255,255,255,.82);
 font-family:var(--sans);font-size:10px;color:#5F6368;padding:3px 10px;line-height:1.5;
 display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;pointer-events:none}
.attrib b{font-weight:500;color:#3C4043}

#grip{position:absolute;top:50%;right:0;transform:translateY(-50%);z-index:5;
 width:20px;height:56px;background:#FFFFFF;border:none;border-radius:6px 0 0 6px;
 font-family:var(--sans);font-size:12px;color:#5F6368;
 display:flex;align-items:center;justify-content:center;box-shadow:-1px 0 4px rgba(0,0,0,.22)}
#grip:hover{color:#111}
@media(max-width:860px){#grip{display:none}}

#panel{overflow-y:auto;background:var(--paper);padding:0 0 60px}
.empty{padding:32px 26px;color:var(--gneiss);max-width:48ch}
.empty h2{font-family:var(--mono);font-size:13px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--ink);margin-bottom:14px;font-weight:600}
.empty p{font-size:14px;margin-bottom:10px}
.five{font-family:var(--mono);font-size:12px;margin:16px 0 0;list-style:none}
.five li{padding:3px 0;border-bottom:1px dotted var(--hair);color:var(--ink)}

.pp{padding:20px 24px}
.pp-type{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--gneiss)}
.pp-name{font-size:26px;line-height:1.15;font-weight:600;letter-spacing:-.015em;margin:4px 0 6px}
.pp-id{font-family:var(--mono);font-size:10px;color:var(--gneiss);word-break:break-all}
.pp-also{font-size:12px;color:var(--gneiss);font-style:italic;margin-top:5px}

.flagbox{border-left:3px solid var(--tram);background:rgba(176,36,42,.055);
 padding:9px 12px;margin:16px 0 4px;font-size:13.5px;line-height:1.45}
.flagbox b{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--tram);display:block;margin-bottom:3px;font-weight:600}

h3.sec{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--gneiss);margin:26px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--rule);
 font-weight:600;display:flex;justify-content:space-between;align-items:baseline;gap:8px}
h3.sec .q{color:var(--ink);text-transform:none;letter-spacing:0;font-size:11px;font-weight:400;font-style:italic}

.f{display:grid;grid-template-columns:12px 116px 1fr;gap:0 10px;padding:5px 0;
 border-bottom:1px dotted var(--hair);align-items:start}
.f:last-child{border-bottom:none}
.g{font-family:var(--mono);font-size:11px;line-height:1.5;text-align:center;user-select:none;cursor:help}
.g.authoritative,.g.official_document{color:var(--verified)}
.g.cross_referenced,.g.single_source{color:var(--gneiss)}
.g.unknown,.g.contested{color:var(--tram);font-weight:700}
.k{font-family:var(--mono);font-size:11px;color:var(--gneiss);padding-top:2px}
.v{font-size:14px;min-width:0}
.v .num{font-family:var(--mono);font-weight:600;font-size:15px}
.src{display:block;font-family:var(--mono);font-size:10px;color:var(--gneiss);margin-top:2px}
.src a{text-decoration:underline;text-underline-offset:2px;text-decoration-color:var(--hair)}
.note{display:block;font-size:12.5px;color:var(--gneiss);margin-top:3px;line-height:1.4}
.unk{color:var(--tram);font-family:var(--mono);font-size:12px}
.unk .why{color:var(--gneiss);font-family:var(--sans);font-size:12.5px;display:block;margin-top:2px;line-height:1.4}
.cont{border-left:2px solid var(--tram);padding-left:9px}
.cont .pos{font-size:13.5px;padding:3px 0}
.cont .pos+.pos{border-top:1px dotted var(--hair)}
.cont .lead{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--tram);font-weight:600}

.var{margin:10px 0 4px;font-family:var(--mono);font-size:11px}
.bar{height:12px;background:var(--hair);position:relative;margin:5px 0 3px;border:1px solid var(--rule)}
.bar .planned{position:absolute;left:0;top:0;bottom:0;background:var(--gneiss)}
.bar .over{position:absolute;top:0;bottom:0;background:var(--tram)}
.varlab{display:flex;justify-content:space-between;color:var(--gneiss)}
.varlab b{color:var(--tram);font-weight:600}

.proj{border:1px solid var(--rule);padding:11px 13px;margin-bottom:12px;background:var(--vellum)}
.proj h4{font-size:15px;margin-bottom:2px}
.proj .pid{font-family:var(--mono);font-size:10px;color:var(--gneiss);margin-bottom:8px}
.ms{font-family:var(--mono);font-size:11.5px;margin-top:8px}
.ms .row{display:grid;grid-template-columns:1fr 76px 76px;gap:6px;padding:3px 0;border-top:1px dotted var(--hair)}
.ms .hd{color:var(--gneiss);border-top:none;font-size:10px;letter-spacing:.08em;text-transform:uppercase}
.ms .late{color:var(--tram);font-weight:600}
.ms .none{color:var(--tram)}

.tl{margin-top:6px}
.ev{display:grid;grid-template-columns:62px 1fr;gap:12px;padding:7px 0;border-left:1px solid var(--rule);
 margin-left:5px;padding-left:14px;position:relative}
.ev::before{content:"";position:absolute;left:-3.5px;top:14px;width:6px;height:6px;
 background:var(--paper);border:1px solid var(--gneiss);border-radius:50%}
.ev.hot::before{background:var(--tram);border-color:var(--tram)}
.ev .t{font-family:var(--mono);font-size:11px;color:var(--gneiss);padding-top:1px}
.ev .w{font-size:13.5px;line-height:1.42}
.ev .w .s{display:block;font-family:var(--mono);font-size:10px;color:var(--gneiss);margin-top:2px}

.rev{margin-top:22px;padding-top:10px;border-top:1px solid var(--rule);
 font-family:var(--mono);font-size:10.5px;color:var(--gneiss);line-height:1.6}
.rev b{color:var(--ink);font-weight:600}

.legend{padding:12px 24px;border-top:1px solid var(--rule);background:var(--vellum);
 font-family:var(--mono);font-size:10.5px;color:var(--gneiss)}
.legend div{padding:2px 0}
.legend .sym{display:inline-block;width:14px;color:var(--ink)}
.legend .sym.v{color:var(--verified)}
.legend .sym.r{color:var(--tram)}

.instlist{padding:20px 24px;max-width:860px}
.inst{border:1px solid var(--rule);padding:13px 15px;margin-bottom:12px;background:var(--vellum)}
.inst .nm{font-size:17px;font-weight:600}
.inst .ty{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
 color:var(--gneiss);margin-top:2px}
.occ{border-top:1px dotted var(--hair);padding:6px 0;display:grid;grid-template-columns:1fr auto;
 gap:10px;font-size:13.5px;align-items:baseline}
.occ .term{font-family:var(--mono);font-size:11px;color:var(--gneiss);white-space:nowrap}
.occ .term.exp{color:var(--tram);font-weight:700}
.derived{font-family:var(--mono);font-size:10.5px;color:var(--gneiss);background:var(--paper);
 border:1px dashed var(--rule);padding:7px 9px;margin-top:8px;line-height:1.5}
.lnk{text-decoration:underline;text-underline-offset:2px;cursor:pointer}

.tbl{padding:20px 24px;max-width:960px}
.tbl section{border-top:1px solid var(--rule);padding-top:14px;margin-top:22px}
.tbl h2{font-size:18px;margin-bottom:2px}
.tbl .id{font-family:var(--mono);font-size:10.5px;color:var(--gneiss);margin-bottom:8px}
.tbl table{border-collapse:collapse;width:100%;margin:6px 0}
.tbl th,.tbl td{text-align:left;vertical-align:top;padding:4px 8px 4px 0;
 border-bottom:1px dotted var(--hair);font-size:13px}
.tbl th{font:400 10.5px var(--mono);color:var(--gneiss);width:140px}
.tbl small{font:10px var(--mono);color:var(--gneiss)}
.tbl .u{color:var(--tram);font-weight:600}

:focus-visible{outline:2px solid var(--tram);outline-offset:2px}
</style>
</head>
<body>

<header>
  <span class="wordmark">Cities On Palm</span>
  <span class="scope">Roosevelt Island &middot; Manhattan CD8 &middot; pilot 0.1</span>
  <nav>
    <button id="tabMap" aria-pressed="true">Objects</button>
    <button id="tabInst" aria-pressed="false">Who governs</button>
    <button id="tabTbl" aria-pressed="false">Full record</button>
    <button id="tabHide" aria-pressed="false" title="Toggle the side panel">Hide panel</button>
  </nav>
</header>

<main id="shell">
  <div id="mapwrap">
    <svg id="map" role="img" aria-label="Map of Roosevelt Island. Click an object to open its passport."></svg>
    <button id="grip" title="Hide panel" aria-label="Hide panel">&#9656;</button>
    <div class="zoomer">
      <button id="zin" aria-label="Zoom in">+</button>
      <button id="zout" aria-label="Zoom out">&minus;</button>
      <button id="zrst" aria-label="Reset view">&middot;</button>
    </div>
    <div class="attrib"><span><b>Cities On Palm</b> &middot; red outline = finding</span><span>Geometry approximate, hand-placed &middot; drawn locally &mdash; no tile server sees your viewport</span></div>
  </div>
  <div id="panel"></div>
</main>

<script id="cop-data" type="application/json">__DATA__</script>
<script>
"use strict";
var D = JSON.parse(document.getElementById('cop-data').textContent);
var S = D.sources;
var P = document.getElementById('panel');
var shell = document.getElementById('shell');
var svg = document.getElementById('map');

/* ---------------- projection ---------------- */
var BM = D.basemap;
var W=1000, H=1000, BOUNDS=null;

function bounds(){
  var la0=90,la1=-90,lo0=180,lo1=-180;
  function eat(pts){ pts.forEach(function(p){
    if(p[0]<la0)la0=p[0]; if(p[0]>la1)la1=p[0];
    if(p[1]<lo0)lo0=p[1]; if(p[1]>lo1)lo1=p[1]; }); }
  eat(BM.island);
  var padLa=(la1-la0)*0.05, padLo=(lo1-lo0)*0.05;
  return {la0:la0-padLa, la1:la1+padLa, lo0:lo0-padLo, lo1:lo1+padLo};
}
BOUNDS = bounds();
/* keep aspect roughly true at this latitude */
(function(){
  var b=BOUNDS, kx=(b.lo1-b.lo0)*Math.cos(40.76*Math.PI/180), ky=(b.la1-b.la0);
  var ar=kx/ky;
  if(ar<1){ var need=ky*1 - kx; var add=need/2/Math.cos(40.76*Math.PI/180);
            b.lo0-=add; b.lo1+=add; }
})();
function px(p){
  var b=BOUNDS;
  return [ (p[1]-b.lo0)/(b.lo1-b.lo0)*W, (b.la1-p[0])/(b.la1-b.la0)*H ];
}
function pstr(pts){ return pts.map(px).map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1)}).join(' '); }
function dstr(pts){ return 'M'+pts.map(px).map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1)}).join('L'); }

var view={x:0,y:0,k:1};
function setVB(){
  var s=1/view.k;
  svg.setAttribute('viewBox', view.x.toFixed(1)+' '+view.y.toFixed(1)+' '+(W*s).toFixed(1)+' '+(H*s).toFixed(1));
  svg.classList.toggle('z2', view.k>2.2);
}
function ns(t){ return document.createElementNS('http://www.w3.org/2000/svg', t); }
function el(tag,attrs){ var e=ns(tag); for(var k in attrs) e.setAttribute(k,attrs[k]); return e; }

/* type -> visual class */
var STYLE={
  residential:'building', campus:'building', school:'civic', hospital:'civic',
  landmark_building:'civic', parking:'building', recreation:'building',
  lighthouse:'node', subway_station:'node',
  park:'park', public_space:'park',
  ruin:'ruin',
  street:'roadline', aerial_tramway:'cable', waste_network:'buried',
  bridge:'bridgeline', coastal_defence:'water_edge'
};

function drawMap(){
  while(svg.firstChild) svg.removeChild(svg.firstChild);

  /* --- basemap: surrounding land, island, bridge, roads --- */
  var g0=ns('g');
  g0.appendChild(el('polygon',{points:pstr(BM.manhattan),'class':'bm-land'}));
  g0.appendChild(el('polygon',{points:pstr(BM.queens),'class':'bm-land'}));
  g0.appendChild(el('polygon',{points:pstr(BM.island),'class':'bm-island'}));
  g0.appendChild(el('path',{d:dstr(BM.queensboro_bridge),'class':'bm-qb-case'}));
  g0.appendChild(el('path',{d:dstr(BM.queensboro_bridge),'class':'bm-qb'}));
  var RW={main_street:[9,7],west_road:[7.5,5.5],east_road:[7.5,5.5],loop_north:[6.5,4.5],bridge_ramp:[7,5]};
  Object.keys(BM.roads).forEach(function(r){
    g0.appendChild(el('path',{d:dstr(BM.roads[r]),'class':'bm-road-case','stroke-width':(RW[r]||[7,5])[0]}));
  });
  Object.keys(BM.roads).forEach(function(r){
    g0.appendChild(el('path',{d:dstr(BM.roads[r]),'class':'bm-road','stroke-width':(RW[r]||[7,5])[1]}));
  });
  svg.appendChild(g0);

  /* --- context labels --- */
  var ctx=ns('g');
  function ctxLabel(p,txt,size,kind,rot){
    var q=px(p), a={x:q[0].toFixed(1),y:q[1].toFixed(1),'class':'bm-label'+(kind?' '+kind:''),
      'font-size':size,'text-anchor':'middle'};
    if(rot) a.transform='rotate('+rot+' '+q[0].toFixed(1)+' '+q[1].toFixed(1)+')';
    var t=el('text',a); t.textContent=txt; ctx.appendChild(t);
  }
  ctxLabel([40.7556,-73.9655],'MANHATTAN',12.5,'place');
  ctxLabel([40.7648,-73.9382],'QUEENS',12.5,'place');
  ctxLabel([40.7530,-73.9605],'East River',10,'water',28);
  ctxLabel([40.7672,-73.9432],'East Channel',9.5,'water',28);
  ctxLabel([40.7597,-73.9606],'Queensboro Bridge',8.5,null,-62);
  ctxLabel([40.7515,-73.9560],'Roosevelt Island',11,'place',28);
  svg.appendChild(ctx);

  /* --- objects: areas first, then lines, then nodes --- */
  var order={park:1,ruin:2,building:3,civic:3,water_edge:4,roadline:5,buried:6,bridgeline:7,cable:8,node:9};
  var objs=D.objects.slice().sort(function(a,b){
    return (order[STYLE[a.type]]||5)-(order[STYLE[b.type]]||5);
  });

  objs.forEach(function(o){
    var cls=STYLE[o.type]||'building';
    var g=ns('g');
    g.setAttribute('class','obj '+cls+' '+(o.tier===1?'t1':'t2')+(o.flag?' flagged':''));
    g.setAttribute('data-id',o.id);
    var pts=o.geom.pts, mark, hit;

    if(o.geom.kind==='poly'){
      mark=el('polygon',{points:pstr(pts)});
      hit =el('polygon',{points:pstr(pts)});
    } else if(o.geom.kind==='point'){
      var q=px(pts[0]);
      mark=el('circle',{cx:q[0],cy:q[1],r:3.4});
      hit =el('circle',{cx:q[0],cy:q[1],r:11});
    } else {
      mark=el('path',{d:dstr(pts)});
      hit =el('path',{d:dstr(pts),fill:'none'});
    }
    mark.setAttribute('class','mark'); hit.setAttribute('class','hit');
    g.appendChild(hit); g.appendChild(mark);

    /* label at centroid for areas, midpoint for lines */
    var lp;
    if(o.geom.kind==='poly'){
      var sx=0,sy=0; pts.forEach(function(p){var q=px(p);sx+=q[0];sy+=q[1]});
      lp=[sx/pts.length, sy/pts.length];
    } else {
      lp=px(pts[Math.floor(pts.length/2)]);
      lp=[lp[0]+6, lp[1]-4];
    }
    var lab=el('text',{x:lp[0].toFixed(1),y:lp[1].toFixed(1),'class':'olabel','text-anchor':'middle'});
    var nm=o.name.replace(/ \(.*\)$/,'');
    lab.textContent = nm.length>26 ? nm.slice(0,25)+'\u2026' : nm;
    g.appendChild(lab);

    g.addEventListener('click',function(e){ e.stopPropagation(); openObj(o.id); });
    svg.appendChild(g);
  });
  setVB();
}

var drag=null;
svg.addEventListener('pointerdown',function(e){
  drag={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y,moved:false};
  try{ svg.setPointerCapture(e.pointerId); }catch(err){}
});
svg.addEventListener('pointermove',function(e){
  if(!drag) return;
  var r=svg.getBoundingClientRect(), s=(W/view.k)/r.width;
  var dx=e.clientX-drag.x, dy=e.clientY-drag.y;
  if(Math.abs(dx)+Math.abs(dy)>3) drag.moved=true;
  view.x=drag.vx-dx*s; view.y=drag.vy-dy*s;
  setVB();
});
svg.addEventListener('pointerup',function(){ drag=null; });
svg.addEventListener('pointercancel',function(){ drag=null; });
svg.addEventListener('wheel',function(e){ e.preventDefault(); zoomAt(e, e.deltaY<0?1.2:1/1.2); },{passive:false});

function zoomAt(e,f){
  var r=svg.getBoundingClientRect();
  var mx=(e.clientX-r.left)/r.width, my=(e.clientY-r.top)/r.height;
  var w=W/view.k, h=H/view.k;
  var gx=view.x+mx*w, gy=view.y+my*h;
  view.k=Math.min(18,Math.max(0.85,view.k*f));
  view.x=gx-mx*(W/view.k); view.y=gy-my*(H/view.k);
  setVB();
}
function zoom(f){
  var cx=view.x+(W/view.k)/2, cy=view.y+(H/view.k)/2;
  view.k=Math.min(18,Math.max(0.85,view.k*f));
  view.x=cx-(W/view.k)/2; view.y=cy-(H/view.k)/2;
  setVB();
}
document.getElementById('zin').onclick=function(){zoom(1.4)};
document.getElementById('zout').onclick=function(){zoom(1/1.4)};
document.getElementById('zrst').onclick=function(){view={x:0,y:0,k:1};setVB()};

/* fly to an object when its passport opens */
function flyTo(o){
  var pts=o.geom.pts.map(px);
  var x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;
  pts.forEach(function(p){ if(p[0]<x0)x0=p[0]; if(p[0]>x1)x1=p[0];
                           if(p[1]<y0)y0=p[1]; if(p[1]>y1)y1=p[1]; });
  var w=Math.max(x1-x0,40), h=Math.max(y1-y0,40);
  var k=Math.min(18, Math.max(1.6, Math.min(W/(w*3.2), H/(h*3.2))));
  var cx=(x0+x1)/2, cy=(y0+y1)/2;
  var from={x:view.x,y:view.y,k:view.k}, to={x:cx-(W/k)/2, y:cy-(H/k)/2, k:k};
  var t0=null, dur=280;
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    view=to; setVB(); return;
  }
  function step(ts){
    if(!t0) t0=ts;
    var t=Math.min(1,(ts-t0)/dur), e=t<.5?2*t*t:-1+(4-2*t)*t;
    view.x=from.x+(to.x-from.x)*e; view.y=from.y+(to.y-from.y)*e; view.k=from.k+(to.k-from.k)*e;
    setVB();
    if(t<1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

/* ---------------- rendering ---------------- */
var GLYPH={authoritative:'\u2713',official_document:'\u00b7',cross_referenced:'~',
 single_source:'~',machine_extracted:'m',contributed:'c'};
function esc(s){ return String(s).replace(/[&<>"]/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
function srcLink(k){
  var s=S[k]; if(!s) return '';
  return '<span class="src">\u21b3 <a href="'+esc(s.uri)+'" target="_blank" rel="noopener noreferrer">'+esc(s.name)+'</a></span>';
}
function money(v){
  if(typeof v!=='object'||v===null||!('amount' in v)) return esc(v);
  return '<span class="num">$'+v.amount.toLocaleString('en-US')+'</span> '+
    '<span style="color:var(--gneiss);font-family:var(--mono);font-size:11px">'+esc(v.currency)+' \u00b7 '+esc(v.year)+'</span>';
}
function row(g,k,v,cls){
  return '<div class="f"><div class="g '+cls+'" title="'+cls.replace(/_/g,' ')+'">'+g+'</div>'+
    '<div class="k">'+esc(k.replace(/_/g,' '))+'</div><div class="v">'+v+'</div></div>';
}
function field(key,val){
  if(val===undefined||val===null) return '';
  if(typeof val==='string') return row('~',key,esc(val),'cross_referenced');
  if(val.status==='unknown'){
    return row('?',key,'<span class="unk">UNKNOWN \u2014 '+esc(val.reason)+
      (val.note?'<span class="why">'+esc(val.note)+'</span>':'')+'</span>','unknown');
  }
  if(val.status==='contested'){
    var pos=val.positions.map(function(p){
      return '<div class="pos">'+esc(p.value)+' '+srcLink(p.src)+'</div>'; }).join('');
    return row('\u2260',key,'<div class="cont"><span class="lead">Contested \u2014 sources disagree</span>'+pos+'</div>'+
      (val.note?'<span class="note">'+esc(val.note)+'</span>':''),'contested');
  }
  return row(GLYPH[val.tier]||'~',key,
    money(val.value)+srcLink(val.source)+(val.note?'<span class="note">'+esc(val.note)+'</span>':''),
    val.tier||'cross_referenced');
}
function block(obj){
  if(!obj) return '';
  var out='';
  Object.keys(obj).forEach(function(k){ if(k!=='note') out+=field(k,obj[k]); });
  if(obj.note) out+='<div class="f"><div class="g contested">!</div><div class="k">note</div>'+
    '<div class="v"><span class="note" style="color:var(--ink)">'+esc(obj.note)+'</span></div></div>';
  return out;
}
function variance(p){
  var h='';
  if(p.cost_variance){
    var c=p.cost_variance, w=100/(1+c.pct/100);
    h+='<div class="var"><div class="bar"><div class="planned" style="width:'+w+'%"></div>'+
      '<div class="over" style="left:'+w+'%;right:0"></div></div><div class="varlab">'+
      '<span>announced $'+(c.from/1e6).toFixed(0)+'M</span><b>+'+c.pct.toFixed(0)+'% \u2192 $'+(c.to/1e6).toFixed(0)+'M</b></div></div>';
  }
  if(p.schedule_variance){
    var s=p.schedule_variance, w2=100/(1+s.pct/100);
    h+='<div class="var"><div class="bar"><div class="planned" style="width:'+w2+'%"></div>'+
      '<div class="over" style="left:'+w2+'%;right:0"></div></div><div class="varlab">'+
      '<span>promised '+s.planned_months+' months</span><b>+'+s.pct.toFixed(0)+'% \u2192 '+s.actual_months+' months</b></div></div>';
  }
  return h;
}
function project(p){
  var ms=(p.milestones||[]).map(function(m){
    var late=m.actual&&m.planned&&m.actual>m.planned;
    return '<div class="row"><span>'+esc(m.name)+
      (m.note?'<br><span style="color:var(--gneiss);font-size:10.5px">'+esc(m.note)+'</span>':'')+'</span>'+
      '<span>'+(m.planned?esc(m.planned):'\u2014')+'</span>'+
      '<span class="'+(m.actual?(late?'late':''):'none')+'">'+(m.actual?esc(m.actual):'never')+'</span></div>';
  }).join('');
  return '<div class="proj"><h4>'+esc(p.title)+'</h4><div class="pid">'+esc(p.id)+'</div>'+
    block({status:p.status,contractor:p.contractor,engineers:p.engineers,consultant:p.consultant,funding:p.funding})+
    variance(p)+
    (ms?'<div class="ms"><div class="row hd"><span>Milestone</span><span>Planned</span><span>Actual</span></div>'+ms+'</div>':'')+
    (p.promised?'<div class="note" style="margin-top:8px">Promised: '+esc(p.promised)+'</div>':'')+
    (p.note?'<div class="note" style="margin-top:6px">'+esc(p.note)+'</div>':'')+'</div>';
}
function timeline(h){
  if(!h||!h.length) return '<p style="color:var(--gneiss);font-size:13px">No history compiled. Not the same as no history.</p>';
  return '<div class="tl">'+h.map(function(e){
    var hot=/collaps|fail|strand|clos|expired|demolish|no completion|not secure/i.test(e.what);
    return '<div class="ev '+(hot?'hot':'')+'"><div class="t">'+esc(e.t)+'</div><div class="w">'+esc(e.what)+
      (e.src?'<span class="s">\u21b3 '+esc(S[e.src]?S[e.src].name:e.src)+'</span>':'')+'</div></div>';
  }).join('')+'</div>';
}

/* ---------------- views ---------------- */
var hidden=false, curView='map';
function applyShell(){
  shell.className = (curView==='map') ? (hidden?'nopanel':'') : 'wide';
  var g=document.getElementById('grip');
  g.innerHTML = hidden ? '\u25c2' : '\u25b8';
  g.title = hidden ? 'Show panel' : 'Hide panel';
  g.style.display = (curView==='map') ? 'flex' : 'none';
  var b=document.getElementById('tabHide');
  b.textContent = hidden ? 'Show panel' : 'Hide panel';
  b.setAttribute('aria-pressed', hidden);
}
function tabs(which){
  curView=which;
  document.getElementById('tabMap').setAttribute('aria-pressed', which==='map');
  document.getElementById('tabInst').setAttribute('aria-pressed', which==='inst');
  document.getElementById('tabTbl').setAttribute('aria-pressed', which==='tbl');
  applyShell();
}
function togglePanel(){
  hidden=!hidden;
  if(!hidden && curView!=='map') curView='map';
  applyShell();
}

function splash(){
  tabs('map');
  P.innerHTML='<div class="empty"><h2>Click any object</h2>'+
   '<p>Every object of public consequence on this island has a passport. A passport answers five questions, in this order:</p>'+
   '<ul class="five"><li>1 &nbsp;What is this?</li><li>2 &nbsp;Who is responsible for it?</li>'+
   '<li>3 &nbsp;Who paid for it?</li><li>4 &nbsp;What is happening to it now?</li>'+
   '<li>5 &nbsp;What has happened to it over its lifetime?</li></ul>'+
   '<p style="margin-top:18px">Seven objects are fully researched. Twenty-two are stubs, and say so. '+
   'Nothing is invented: where the public record has no answer, the passport says so and names what is missing.</p>'+
   '<p style="color:var(--tram)">Objects outlined in red have a finding. Start with the Renwick Ruin, the Tram, or AVAC.</p>'+
   '<p style="font-size:12.5px">Scroll to zoom, drag to pan. Hide this panel with the tab above, the handle on the edge, or Escape.</p></div>'+
   '<div class="legend">'+
   '<div><span class="sym v">\u2713</span> authoritative \u2014 system of record</div>'+
   '<div><span class="sym v">\u00b7</span> official document</div>'+
   '<div><span class="sym">~</span> cross-referenced / single source</div>'+
   '<div><span class="sym r">?</span> unknown \u2014 and the passport says why</div>'+
   '<div><span class="sym r">\u2260</span> contested \u2014 sources disagree; both shown, neither adjudicated</div></div>';
}

function openObj(id){
  var o=null;
  for(var i=0;i<D.objects.length;i++) if(D.objects[i].id===id) o=D.objects[i];
  if(!o) return;
  hidden=false;
  tabs('map');
  flyTo(o);
  var nodes=svg.querySelectorAll('.obj');
  for(var n=0;n<nodes.length;n++)
    nodes[n].classList.toggle('on', nodes[n].getAttribute('data-id')===id);

  var vals=[];
  ['ownership','responsibility','finance','lifecycle','attributes'].forEach(function(g){
    var b=o[g]; if(b) Object.keys(b).forEach(function(k){
      if(b[k]&&typeof b[k]==='object') vals.push(b[k]); });
  });
  var unk=vals.filter(function(v){return v.status==='unknown'}).length;
  var con=vals.filter(function(v){return v.status==='contested'}).length;

  var h='<div class="pp"><div class="pp-type">'+esc(o.type.replace(/_/g,' '))+(o.tier===2?' \u00b7 stub':'')+'</div>'+
    '<div class="pp-name">'+esc(o.name)+'</div><div class="pp-id">'+esc(o.id)+'</div>'+
    (o.also?'<div class="pp-also">also: '+o.also.map(esc).join(' \u00b7 ')+'</div>':'');

  if(o.tier===2){
    h+='<div class="flagbox"><b>Stub \u2014 not yet researched</b>'+esc(o.stub_note||'')+
      '<div style="margin-top:6px;font-size:12.5px;color:var(--gneiss)">This object is rendered and identified, and nothing more. '+
      'It is shown as a stub rather than omitted, because a gap you can see is worth more than one you cannot.</div></div>';
  }
  if(o.flag) h+='<div class="flagbox"><b>Finding</b>'+esc(o.flag)+'</div>';
  if(unk||con){
    h+='<div style="font-family:var(--mono);font-size:11px;color:var(--gneiss);margin-top:14px">'+
      (unk?'<span style="color:var(--tram)">'+unk+' field'+(unk>1?'s':'')+' unknown</span>':'')+
      (unk&&con?' \u00b7 ':'')+(con?'<span style="color:var(--tram)">'+con+' contested</span>':'')+
      '&nbsp;\u2014 scan the left margin.</div>';
  }

  h+='<h3 class="sec">Identity <span class="q">What is this?</span></h3>'+block(o.lifecycle)+block(o.attributes)+
    '<h3 class="sec">Responsibility <span class="q">Who is accountable?</span></h3>'+block(o.ownership)+block(o.responsibility)+
    '<h3 class="sec">Money <span class="q">Who paid for it?</span></h3>'+block(o.finance)+
    '<h3 class="sec">Now <span class="q">What is happening to it?</span></h3>'+
    (o.projects&&o.projects.length?o.projects.map(project).join(''):
      '<p style="color:var(--gneiss);font-size:13px">No active or recorded project.</p>')+
    field('inspections',o.inspections)+
    '<h3 class="sec">Lifetime <span class="q">What has happened to it?</span></h3>'+timeline(o.history);

  if(o.containment&&o.containment.length){
    h+='<h3 class="sec">Containment</h3>'+o.containment.map(function(c){
      return '<div class="f"><div class="g cross_referenced">\u2191</div><div class="k">'+esc(c.rel)+'</div>'+
        '<div class="v"><span style="font-family:var(--mono);font-size:12px">'+esc(c.target)+'</span>'+
        (c.note?'<span class="note">'+esc(c.note)+'</span>':'')+'</div></div>';
    }).join('');
  }
  if(o.connected&&o.connected.length){
    h+='<h3 class="sec">Connected infrastructure</h3><div style="font-family:var(--mono);font-size:12px;line-height:1.9">'+
      o.connected.map(function(c){
        var t=null; for(var j=0;j<D.objects.length;j++) if(D.objects[j].id===c) t=D.objects[j];
        return t?'<span class="lnk" data-go="'+esc(c)+'">'+esc(t.name)+'</span>':esc(c);
      }).join(' \u00b7 ')+'</div>';
  }

  var r=o.revision;
  h+='<div class="rev"><b>revision '+esc(r.id)+'</b> \u00b7 parent: none (genesis)<br>'+
    'valid_from '+esc(r.valid_from)+' \u00b7 recorded_at '+esc(r.recorded_at)+'<br>'+
    'author '+esc(r.author)+'<br>'+esc(r.note)+'</div></div>';

  P.innerHTML=h; P.scrollTop=0;
}

function institutions(){
  tabs('inst');
  var h='<div class="instlist"><div class="empty" style="padding:0 0 18px;max-width:56ch">'+
    '<h2>Who governs this island</h2><p>Six bodies hold authority over 12,000 people on two miles of rock. '+
    'Their jurisdictions overlap. Shown overlapping, not flattened.</p></div>';

  D.institutions.forEach(function(i){
    h+='<div class="inst"><div class="nm">'+esc(i.name)+'</div>'+
      '<div class="ty">'+esc(i.type.replace(/_/g,' '))+' \u00b7 '+esc(i.short)+'</div>'+
      block({mandate:i.mandate,legal_basis:i.legal_basis,jurisdiction:i.jurisdiction,
             governing_document:i.governing_document,funding:i.funding});
    (i.budget||[]).forEach(function(b){
      h+=row('~','budget '+b.year, esc(b.figure)+srcLink(b.src), b.tier||'single_source');
    });
    if(i.responsible_for&&i.responsible_for.length){
      h+='<div style="font-family:var(--mono);font-size:11px;color:var(--gneiss);margin-top:9px">responsible for: '+
        i.responsible_for.map(function(id){
          var t=null; for(var j=0;j<D.objects.length;j++) if(D.objects[j].id===id) t=D.objects[j];
          return t?'<span class="lnk" data-go="'+esc(id)+'" style="color:var(--ink)">'+esc(t.name)+'</span>':esc(id);
        }).join(' \u00b7 ')+'</div>';
    }
    if(i.flag) h+='<div class="flagbox" style="margin:12px 0 0"><b>Finding</b>'+esc(i.flag)+'</div>';
    h+='</div>';
  });

  h+='<h3 class="sec" style="margin-top:30px">Offices <span class="q">Accountable as individuals \u2014 through their decisions</span></h3>';
  D.offices.forEach(function(o){
    h+='<div class="inst"><div class="nm">'+esc(o.title)+'</div>'+block({appointed_by:o.appointed_by})+
      '<div style="font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;'+
      'color:var(--gneiss);margin:12px 0 2px">Occupancy</div>';
    o.occupancies.forEach(function(c){
      var fr=(c.from&&c.from.status)?'?':(c.from||'?');
      var to=(c.to&&c.to.status)?'\u2014':(c.to||'present');
      var expired=/expired/.test(String(to));
      h+='<div class="occ"><span>'+esc(c.name)+'</span>'+
        '<span class="term '+(expired?'exp':'')+'">'+esc(fr)+' \u2192 '+esc(to)+'</span></div>';
    });
    h+='<div class="derived">DERIVED RECORD \u2014 computed, never written.<br>'+
      'Aggregates (projects on schedule, late, abandoned, cost variance, responsiveness) require a complete, '+
      'dated, attributed project register. RIOC does not publish one. '+
      '<span style="color:var(--tram)">The aggregate is therefore empty, and the emptiness is the finding.</span></div>';
    if(o.flag) h+='<div class="flagbox" style="margin:12px 0 0"><b>Finding</b>'+esc(o.flag)+'</div>';
    h+='</div>';
  });
  P.innerHTML=h+'</div>'; P.scrollTop=0;
}

function fullTable(){
  tabs('tbl');
  var h='<div class="tbl"><div class="empty" style="padding:0 0 14px;max-width:60ch">'+
    '<h2>Full record</h2><p>Every object, every field, every source. '+
    D.objects.filter(function(o){return o.tier===1}).length+' researched \u00b7 '+
    D.objects.filter(function(o){return o.tier===2}).length+' stubs \u00b7 '+
    Object.keys(S).length+' sources.</p>'+
    '<p>Nothing here is invented. Where the public record has no answer, the field reads UNKNOWN and names '+
    'what is missing. Where sources disagree, it reads CONTESTED and shows both.</p></div>';

  D.objects.forEach(function(o){
    var rows='';
    ['lifecycle','ownership','responsibility','finance','attributes'].forEach(function(grp){
      var b=o[grp]; if(!b) return;
      Object.keys(b).forEach(function(k){
        if(k==='note'){ rows+='<tr><th>note</th><td><i>'+esc(b[k])+'</i></td></tr>'; return; }
        rows+='<tr><th>'+esc(k.replace(/_/g,' '))+'</th><td>'+tcell(b[k])+'</td></tr>';
      });
    });
    rows+='<tr><th>inspections</th><td>'+tcell(o.inspections)+'</td></tr>';
    var hist=(o.history||[]).map(function(e){
      return '<tr><td style="width:70px">'+esc(e.t)+'</td><td>'+esc(e.what)+'</td></tr>'; }).join('');
    h+='<section><h2>'+esc(o.name)+'</h2><p class="id">'+esc(o.id)+' \u00b7 '+esc(o.type)+
      ' \u00b7 geometry: '+esc(o.geom.confidence)+'</p>'+
      (o.tier===2?'<div class="flagbox"><b>Stub</b>'+esc(o.stub_note||'')+'</div>':'')+
      (o.flag?'<div class="flagbox"><b>Finding</b>'+esc(o.flag)+'</div>':'')+
      '<table>'+rows+'</table>'+
      (hist?'<h3 class="sec">Lifetime</h3><table>'+hist+'</table>':'')+'</section>';
  });
  P.innerHTML=h+'</div>'; P.scrollTop=0;
}
function tcell(v){
  if(v===undefined||v===null) return '\u2014';
  if(typeof v==='string') return esc(v);
  if(v.status==='unknown')
    return '<span class="u">UNKNOWN</span> \u2014 '+esc(v.reason)+(v.note?'<br><small>'+esc(v.note)+'</small>':'');
  if(v.status==='contested')
    return '<span class="u">CONTESTED</span><br>'+v.positions.map(function(p){
      return '\u00b7 '+esc(p.value)+' <small>'+(S[p.src]?esc(S[p.src].name):'')+'</small>'; }).join('<br>')+
      (v.note?'<br><small>'+esc(v.note)+'</small>':'');
  var val=v.value;
  if(val&&typeof val==='object'&&'amount' in val)
    val='$'+val.amount.toLocaleString('en-US')+' '+val.currency+' ('+val.year+')';
  return esc(String(val))+'<br><small>['+esc(v.tier||'')+'] '+(S[v.source]?esc(S[v.source].name):'')+'</small>'+
    (v.note?'<br><small>'+esc(v.note)+'</small>':'');
}

/* delegated navigation — survives innerHTML replacement */
P.addEventListener('click',function(e){
  var t=e.target.closest('[data-go]');
  if(t){ e.preventDefault(); openObj(t.getAttribute('data-go')); }
});
document.getElementById('tabHide').onclick=togglePanel;
document.getElementById('grip').onclick=togglePanel;
document.addEventListener('keydown',function(e){
  if(e.key==='Escape' && curView==='map') togglePanel();
});
document.getElementById('tabMap').onclick=function(){ hidden=false; splash(); };
document.getElementById('tabInst').onclick=institutions;
document.getElementById('tabTbl').onclick=fullTable;

drawMap();
splash();
</script>
</body>
</html>
"""

open("citiesonpalm.html", "w").write(HTML.replace("__DATA__", BLOB))
print("citiesonpalm.html written — single file, data inlined")
