from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from radar.render import ROOT, all_records, load_yaml
from radar.labels import effective_labels
from radar.methods import method_catalog, method_metadata


OUTPUT = ROOT / "docs" / "index.html"


def payload() -> list[dict]:
    records = []
    for paper in all_records():
        score = int(paper.get("rule_score", 99 if not paper.get("discovery_candidate") else 0))
        confidence = "curated" if not paper.get("discovery_candidate") else "high" if score >= 8 else "medium" if score >= 5 else "broad"
        records.append(
            {
                "id": paper["id"],
                "title": paper["title"],
                "date": str(paper["date"]),
                "direction": paper["direction"],
                "status": "discovery" if paper.get("discovery_candidate") else "curated",
                "url": paper["url"],
                "code": paper.get("code"),
                "keyIdea": paper.get("key_idea"),
                "tags": paper.get("tags", []),
                "labels": effective_labels(paper),
                "confidence": confidence,
                "score": score,
                "authors": paper.get("authors", []),
                "institutions": paper.get("institutions", []),
                "venue": paper.get("venue"),
                "venueType": paper.get("venue_type"),
                "venueUrl": paper.get("venue_url"),
                "methodFamily": method_metadata(paper)["id"],
                "methodFamilyTitle": method_metadata(paper)["title"],
                "methodFamilyColor": method_metadata(paper)["color"],
                "predecessors": paper.get("predecessors", []),
                "changeAxes": paper.get("change_axes", []),
                "transferIdeas": paper.get("transfer_ideas", []),
            }
        )
    return sorted(records, key=lambda paper: paper["date"], reverse=True)


def analytics(records: list[dict], directions: list[dict]) -> dict:
    direction_map = {direction["id"]: direction["title"] for direction in directions}
    paper_index = {paper["id"]: paper for paper in records}
    direction_rows = []
    for direction in directions:
        selected = [paper for paper in records if paper["direction"] == direction["id"]]
        curated = sum(paper["status"] == "curated" for paper in selected)
        direction_rows.append(
            {
                "id": direction["id"],
                "title": direction["title"],
                "count": len(selected),
                "total": len(selected),
                "curated": curated,
                "discovery": len(selected) - curated,
            }
        )
    year_counts: dict[str, int] = {}
    month_counts: dict[str, int] = {}
    for paper in records:
        year = paper["date"][:4]
        month = paper["date"][:7]
        year_counts[year] = year_counts.get(year, 0) + 1
        month_counts[month] = month_counts.get(month, 0) + 1
    families = method_catalog()
    family_rows = []
    axis_counts: dict[str, int] = {}
    family_timeline: dict[str, list[dict]] = {family_id: [] for family_id in families}
    for paper in records:
        family_id = paper.get("methodFamily")
        if not family_id or family_id not in families:
            continue
        for axis in paper.get("changeAxes", []):
            axis_counts[axis] = axis_counts.get(axis, 0) + 1
        family_timeline[family_id].append(
            {
                "id": paper["id"],
                "title": paper["title"],
                "date": paper["date"],
                "url": paper["url"],
                "changeAxes": paper.get("changeAxes", []),
                "transferIdeas": paper.get("transferIdeas", []),
                "predecessors": [
                    {
                        "id": predecessor,
                        "title": paper_index.get(predecessor, {}).get("title", predecessor),
                        "url": paper_index.get(predecessor, {}).get("url"),
                    }
                    for predecessor in paper.get("predecessors", [])
                ],
            }
        )
    for family_id, family in families.items():
        papers = family_timeline.get(family_id, [])
        family_rows.append(
            {
                "id": family_id,
                "title": family["title"],
                "color": family.get("color"),
                "description": family.get("description"),
                "transferIdeas": family.get("transfer_ideas", []),
                "count": len(papers),
            }
        )
    return {
        "directions": sorted(direction_rows, key=lambda row: row["count"], reverse=True),
        "years": [{"key": year, "count": year_counts[year]} for year in sorted(year_counts)],
        "months": [{"key": month, "count": month_counts[month]} for month in sorted(month_counts)],
        "families": sorted(family_rows, key=lambda row: row["count"], reverse=True),
        "familyTimeline": {key: sorted(value, key=lambda row: row["date"]) for key, value in family_timeline.items()},
        "axes": sorted(({"key": key, "count": value} for key, value in axis_counts.items()), key=lambda row: row["count"], reverse=True),
        "directionNames": direction_map,
    }


def snapshot_date(records: list[dict]) -> str:
    """Return a deterministic date for the data snapshot shown in the footer."""
    return max((str(paper["date"]) for paper in records), default=dt.date.today().isoformat())


def render() -> str:
    directions = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    labels = load_yaml(ROOT / "config" / "labels.yaml")["labels"]
    papers = payload()
    data = json.dumps(papers, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    direction_data = json.dumps(directions, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    label_data = json.dumps(labels, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    analytics_data = json.dumps(analytics(papers, directions), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="A searchable atlas of foundation-model post-training research.">
  <title>Awesome Post-Training Atlas</title>
  <style>
    :root{--bg:#f5f7fb;--card:#fff;--ink:#172033;--muted:#667085;--line:#dfe4ec;--accent:#3157d5;--soft:#eef2ff;--candidate:#fff7e8}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}header{background:linear-gradient(135deg,#172554,#3157d5);color:white;padding:52px max(24px,calc((100vw - 1180px)/2)) 40px}h1{margin:0 0 8px;font-size:clamp(30px,5vw,52px);letter-spacing:-.04em}header p{max-width:780px;margin:0;color:#dbe5ff;font-size:17px}.shell{max-width:1180px;margin:auto;padding:24px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:-44px}.stat,.filters,.paper,.directory,.label-picker,.insights,.chart-card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 5px 18px #263b6410}.stat{padding:17px}.stat b{display:block;font-size:27px}.stat span{color:var(--muted)}.directory,.label-picker,.insights{padding:14px 16px;margin:18px 0}.directory summary,.label-picker summary{cursor:pointer;font-weight:700}.directory nav,.label-options{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.directory button,.label-options button,.family-options button{border:1px solid var(--line);background:var(--soft);color:var(--ink);border-radius:999px;padding:6px 10px;cursor:pointer}.label-options button.active,.family-options button.active{background:var(--accent);border-color:var(--accent);color:white}.label-tools{display:flex;gap:10px;align-items:center;margin-top:12px}.label-tools select{max-width:220px}.label-tools button{border:0;background:none;color:var(--accent);cursor:pointer}.filters{display:grid;grid-template-columns:2fr repeat(6,1fr);gap:10px;padding:14px;margin:18px 0}input,select{width:100%;border:1px solid var(--line);border-radius:9px;padding:10px 12px;background:white;color:var(--ink)}#summary{color:var(--muted);margin:10px 2px}.papers{display:grid;gap:10px}.paper{padding:17px}.paper.discovery{background:var(--candidate)}.paper h2{font-size:17px;line-height:1.35;margin:0 0 8px}.paper h2 a{color:var(--ink);text-decoration:none}.paper h2 a:hover{color:var(--accent)}.meta{display:flex;flex-wrap:wrap;gap:7px;color:var(--muted);font-size:13px}.pill{background:var(--soft);color:#3349a3;border-radius:999px;padding:2px 8px}.pill.label{border:1px solid #c7d2fe}.pill.family{background:#e0e7ff;color:#253e9c}.pill.axis{background:#f1f5f9;color:#475569}.discovery .pill.status{background:#ffe5ad;color:#7a4c00}.idea,.people,.evolution{margin:10px 0 0;color:#3b4558}.people,.evolution{font-size:13px}.people a,.evolution a{color:var(--accent);text-decoration:none}.links{margin-left:auto}.links a{color:var(--accent);text-decoration:none}.empty{text-align:center;padding:60px;color:var(--muted)}footer{text-align:center;color:var(--muted);padding:36px}footer a{color:var(--accent)}.insight-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;margin-bottom:14px}.eyebrow{margin:0;color:var(--accent);font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.insight-head h2{margin:3px 0 0;font-size:22px}.insight-note{margin:0;color:var(--muted);font-size:12px}.insight-grid{display:grid;grid-template-columns:1.35fr 1fr 1fr;gap:12px}.chart-card{padding:15px;box-shadow:none}.chart-card.wide{min-width:0}.chart-title{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:10px}.chart-title h3{margin:0;font-size:15px}.chart-title span{color:var(--muted);font-size:11px}.bar-chart{display:grid;gap:8px}.bar-row{display:grid;grid-template-columns:minmax(110px,1fr) 2fr auto;gap:8px;align-items:center;font-size:12px}.bar-label{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.bar-track{height:8px;background:var(--soft);border-radius:999px;overflow:hidden}.bar-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#3157d5,#7c3aed)}.bar-value{color:var(--muted);font-variant-numeric:tabular-nums}.trend{width:100%;height:146px;display:block}.trend-grid{stroke:var(--line);stroke-width:1}.trend-area{fill:url(#trendFill);opacity:.45}.trend-line{fill:none;stroke:var(--accent);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}.trend-labels{display:flex;justify-content:space-between;color:var(--muted);font-size:11px}.family-card{margin-top:12px}.family-options{display:flex;flex-wrap:wrap;gap:7px;margin:4px 0 13px}.family-options button{font-size:12px}.family-description{margin:0 0 12px;color:var(--muted);font-size:13px}.family-timeline{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:9px}.timeline-item{border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:11px;background:linear-gradient(135deg,var(--card),var(--soft))}.timeline-date{color:var(--muted);font-size:11px}.timeline-item a{display:block;margin:4px 0;color:var(--ink);font-weight:700;text-decoration:none;line-height:1.35}.timeline-item a:hover{color:var(--accent)}.timeline-axes{display:flex;flex-wrap:wrap;gap:4px}.timeline-axes span{font-size:10px;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:1px 6px;color:var(--muted)}.timeline-idea,.timeline-relation{margin:8px 0 0;color:var(--muted);font-size:12px}.timeline-relation a{display:inline;font-weight:600;color:var(--accent)}.no-timeline{padding:18px;color:var(--muted);text-align:center}@media(max-width:900px){.insight-grid{grid-template-columns:1fr 1fr}.chart-card.wide{grid-column:1/-1}}@media(max-width:760px){.stats{grid-template-columns:1fr 1fr}.filters{grid-template-columns:1fr}.links{margin-left:0}.insight-grid{grid-template-columns:1fr}.insight-head{display:block}.insight-note{margin-top:6px}}@media(prefers-color-scheme:dark){:root{--bg:#0d1320;--card:#151d2d;--ink:#edf2ff;--muted:#9eabc1;--line:#2b3548;--soft:#232e52;--candidate:#292315}input,select{background:#111827;color:var(--ink)}.pill.family{background:#252e62;color:#dbe5ff}.timeline-item{background:linear-gradient(135deg,var(--card),var(--soft))}}
  </style>
</head>
<body>
<header><h1>Post-Training Atlas</h1><p>Track how post-training methods evolve across language, agents, multimodal models, generative media, and embodied intelligence — then explore the ideas that may transfer across settings.</p></header>
<main class="shell">
  <section class="stats"><div class="stat"><b id="total">0</b><span>papers indexed</span></div><div class="stat"><b id="curated">0</b><span>curated</span></div><div class="stat"><b id="discovery">0</b><span>awaiting review</span></div><div class="stat"><b id="months">0</b><span>months represented</span></div></section>
  <section class="insights"><div class="insight-head"><div><p class="eyebrow">Method evolution</p><h2>Research pulse</h2></div><p class="insight-note">Volume uses all indexed records; method timelines use curated, annotated entries.</p></div><div class="insight-grid"><article class="chart-card wide"><div class="chart-title"><h3>Direction volume</h3><span>indexed records</span></div><div id="directionChart" class="bar-chart"></div></article><article class="chart-card"><div class="chart-title"><h3>Monthly activity</h3><span>all records</span></div><svg id="trendChart" class="trend" viewBox="0 0 720 170" role="img" aria-label="Monthly paper activity chart"></svg><div id="trendLabels" class="trend-labels"></div></article><article class="chart-card"><div class="chart-title"><h3>What methods change</h3><span>curated entries</span></div><div id="axisChart" class="bar-chart"></div></article></div><article class="chart-card family-card"><div class="chart-title"><h3>Method family timeline</h3><span id="familyCount"></span></div><div id="familyOptions" class="family-options"></div><p id="familyDescription" class="family-description"></p><div id="familyTimeline" class="family-timeline"></div></article></section>
  <details class="directory" open><summary>Browse directory</summary><nav id="directory"></nav></details>
  <section class="filters"><input id="q" type="search" placeholder="Search title, key idea, method, or tag…"><select id="direction"><option value="">All directions</option></select><select id="family"><option value="">All method families</option></select><select id="year"><option value="">All years</option></select><select id="month"><option value="">All months</option></select><select id="status"><option value="">All evidence levels</option><option value="curated">Curated</option><option value="discovery">Discovery candidate</option></select><select id="confidence"><option value="reliable">Curated + medium/high</option><option value="high">High-confidence only</option><option value="medium">Medium only</option><option value="broad">Broad recall only</option><option value="all">All confidence levels</option></select></section>
  <details class="label-picker" open><summary>Labels — select one or more (<span id="selectedCount">0</span> selected)</summary><div class="label-tools"><select id="labelMode"><option value="any">Match ANY selected label</option><option value="all">Match ALL selected labels</option></select><button id="clearLabels" type="button">Clear labels</button></div><div id="labelOptions" class="label-options"></div></details>
  <div id="summary"></div><section id="papers" class="papers"></section>
</main>
<footer>* Institutions and publication venues are displayed only when sourced from academic metadata; author-profile affiliations may differ from publication-time affiliations.<br>Data snapshot through __GENERATED__ · Generated from the <a href="https://github.com/undefinted/Awesome-Post-Training-Atlas">Awesome Post-Training Atlas</a></footer>
<script>
const PAPERS=__PAPERS__, DIRECTIONS=__DIRECTIONS__, LABELS=__LABELS__, ANALYTICS=__ANALYTICS__, names=Object.fromEntries(DIRECTIONS.map(x=>[x.id,x.title])), labelNames=Object.fromEntries(LABELS.map(x=>[x.id,x.title])), selectedLabels=new Set();
const $=id=>document.getElementById(id), controls=['q','direction','family','year','month','status','confidence','labelMode'];
for(const d of DIRECTIONS){const o=document.createElement('option');o.value=d.id;o.textContent=d.title;$('direction').append(o)}
for(const family of ANALYTICS.families.filter(x=>x.count)){const o=document.createElement('option');o.value=family.id;o.textContent=family.title;$('family').append(o)}
for(const y of [...new Set(PAPERS.map(p=>p.date.slice(0,4)))].sort().reverse()){const o=document.createElement('option');o.value=y;o.textContent=y;$('year').append(o)}
for(let m=1;m<=12;m++){const v=String(m).padStart(2,'0'),o=document.createElement('option');o.value=v;o.textContent=new Date(2000,m-1).toLocaleString('en',{month:'long'});$('month').append(o)}
for(const d of DIRECTIONS){const b=add('button','',`${d.title} (${PAPERS.filter(p=>p.direction===d.id).length})`,$('directory'));b.onclick=()=>{$('direction').value=d.id;render();scrollTo({top:$('summary').offsetTop-20,behavior:'smooth'})}}for(const y of [...new Set(PAPERS.map(p=>p.date.slice(0,4)))].sort().reverse()){const b=add('button','',`${y} (${PAPERS.filter(p=>p.date.startsWith(y)).length})`,$('directory'));b.onclick=()=>{$('year').value=y;render();scrollTo({top:$('summary').offsetTop-20,behavior:'smooth'})}}
function add(tag,cls,text,parent){const x=document.createElement(tag);if(cls)x.className=cls;if(text!==undefined)x.textContent=text;parent.append(x);return x}
const axisNames={data:'Data',objective:'Objective',feedback:'Feedback',reward:'Reward',verifier:'Verifier',sampling:'Sampling',optimization:'Optimization',efficiency:'Efficiency','credit-assignment':'Credit assignment',tokenization:'Tokenization','long-horizon':'Long horizon','self-improvement':'Self-improvement',environment:'Environment','cross-modal':'Cross-modal',safety:'Safety'};
let selectedFamily=(ANALYTICS.families.find(x=>x.count)||{}).id||'';
function drawBars(id,rows,label){const box=$(id);box.replaceChildren();if(!rows.length){add('div','no-timeline','No annotated records yet.',box);return}const max=Math.max(...rows.map(x=>x.count),1);for(const row of rows){const line=add('div','bar-row',undefined,box);add('span','bar-label',label(row),line);const track=add('span','bar-track',undefined,line),fill=add('span','bar-fill',undefined,track);fill.style.width=`${Math.max(3,100*row.count/max)}%`;add('span','bar-value',row.count.toLocaleString(),line)}}
function drawTrend(){const svg=$('trendChart'),rows=ANALYTICS.months;svg.replaceChildren();if(!rows.length){return}const width=720,height=170,left=10,right=10,top=14,bottom=20,max=Math.max(...rows.map(x=>x.count),1),step=(width-left-right)/Math.max(rows.length-1,1),points=rows.map((row,i)=>`${left+i*step},${height-bottom-(row.count/max)*(height-top-bottom)}`).join(' '),area=`${left},${height-bottom} ${points} ${left+(rows.length-1)*step},${height-bottom}`;svg.innerHTML=`<defs><linearGradient id="trendFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#3157d5" stop-opacity=".34"/><stop offset="100%" stop-color="#3157d5" stop-opacity="0"/></linearGradient></defs><line class="trend-grid" x1="${left}" y1="${top}" x2="${width-right}" y2="${top}"/><line class="trend-grid" x1="${left}" y1="${(height-top-bottom)/2+top}" x2="${width-right}" y2="${(height-top-bottom)/2+top}"/><line class="trend-grid" x1="${left}" y1="${height-bottom}" x2="${width-right}" y2="${height-bottom}"/><polygon class="trend-area" points="${area}"/><polyline class="trend-line" points="${points}"/>`;$('trendLabels').replaceChildren();add('span','',rows[0].key,$('trendLabels'));if(rows.length>2)add('span','',rows[Math.floor(rows.length/2)].key,$('trendLabels'));add('span','',rows[rows.length-1].key,$('trendLabels'))}
function renderFamilyTimeline(){const family=ANALYTICS.families.find(x=>x.id===selectedFamily),timeline=$('familyTimeline');timeline.replaceChildren();if(!family){$('familyDescription').textContent='Method-family annotations will appear as the atlas is reviewed.';$('familyCount').textContent='';return}$('familyDescription').textContent=family.description;$('familyCount').textContent=`${family.count.toLocaleString()} annotated papers`;for(const item of (ANALYTICS.familyTimeline[family.id]||[])){const card=add('div','timeline-item',undefined,timeline);card.style.borderLeftColor=family.color||'var(--accent)';add('div','timeline-date',item.date,card);const link=add('a','',item.title,card);link.href=item.url;link.target='_blank';link.rel='noopener';const axes=add('div','timeline-axes',undefined,card);for(const axis of item.changeAxes.slice(0,5))add('span','',axisNames[axis]||axis,axes);if(item.predecessors.length){const relation=add('p','timeline-relation','Related precedent: ',card);item.predecessors.forEach((pred,index)=>{const link=add(pred.url?'a':'span','',pred.title,relation);if(pred.url){link.href=pred.url;link.target='_blank';link.rel='noopener'}if(index<item.predecessors.length-1)add('span','',', ',relation)})}if(item.transferIdeas.length)add('p','timeline-idea',`Idea surface: ${item.transferIdeas[0]}`,card)}if(!timeline.children.length)add('div','no-timeline','No annotated papers in this family yet.',timeline)}
function renderInsights(){drawBars('directionChart',ANALYTICS.directions,label=>label.title);drawTrend();drawBars('axisChart',ANALYTICS.axes.slice(0,8),row=>axisNames[row.key]||row.key);const options=$('familyOptions');options.replaceChildren();for(const family of ANALYTICS.families.filter(x=>x.count)){const button=add('button',family.id===selectedFamily?'active':'',`${family.title} (${family.count})`,options);button.type='button';button.style.borderColor=family.color||'';button.onclick=()=>{selectedFamily=family.id;for(const child of options.children)child.classList.toggle('active',child===button);renderFamilyTimeline()}}renderFamilyTimeline()}
renderInsights();
for(const label of LABELS){const count=PAPERS.filter(p=>p.labels.includes(label.id)).length;if(!count)continue;const b=add('button','',`${label.title} (${count})`,$('labelOptions'));b.type='button';b.title=label.description;b.onclick=()=>{selectedLabels.has(label.id)?selectedLabels.delete(label.id):selectedLabels.add(label.id);b.classList.toggle('active',selectedLabels.has(label.id));$('selectedCount').textContent=selectedLabels.size;render()}}
$('clearLabels').onclick=()=>{selectedLabels.clear();for(const b of $('labelOptions').children)b.classList.remove('active');$('selectedCount').textContent=0;render()};
function render(){const q=$('q').value.trim().toLowerCase(),d=$('direction').value,f=$('family').value,y=$('year').value,m=$('month').value,s=$('status').value,cf=$('confidence').value,lm=$('labelMode').value,chosen=[...selectedLabels];const confidenceOK=p=>cf==='all'||cf==='reliable'&&p.confidence!=='broad'||cf==='high'&&(p.confidence==='curated'||p.confidence==='high')||cf===p.confidence,labelOK=p=>!chosen.length||(lm==='all'?chosen.every(x=>p.labels.includes(x)):chosen.some(x=>p.labels.includes(x)));const list=PAPERS.filter(p=>(!d||p.direction===d)&&(!f||p.methodFamily===f)&&(!y||p.date.startsWith(y))&&(!m||p.date.slice(5,7)===m)&&(!s||p.status===s)&&confidenceOK(p)&&labelOK(p)&&(!q||[p.title,p.keyIdea,p.venue,p.methodFamilyTitle,...p.changeAxes,...p.transferIdeas,...p.tags,...p.labels.map(x=>labelNames[x]||x),...p.authors,...p.institutions].join(' ').toLowerCase().includes(q)));$('summary').textContent=`Showing ${list.length.toLocaleString()} of ${PAPERS.length.toLocaleString()} papers${chosen.length?` · labels: ${chosen.map(x=>labelNames[x]).join(lm==='all'?' + ':' / ')}`:''}`;$('papers').replaceChildren();if(!list.length){add('div','empty','No papers match these filters.',$('papers'));return}for(const p of list){const card=add('article','paper '+p.status,undefined,$('papers')),h=add('h2','',undefined,card),a=add('a','',p.title,h);a.href=p.url;a.target='_blank';a.rel='noopener';const meta=add('div','meta',undefined,card);add('span','pill status',p.status==='curated'?'Curated':`🔎 ${p.confidence} confidence`,meta);add('span','',p.date,meta);add('span','pill',names[p.direction]||p.direction,meta);if(p.methodFamilyTitle)add('span','pill family',p.methodFamilyTitle,meta);for(const axis of p.changeAxes.slice(0,4))add('span','pill axis',axisNames[axis]||axis,meta);for(const t of p.labels.slice(0,8))add('span','pill label',labelNames[t]||t,meta);if(p.code){const links=add('span','links',undefined,meta),c=add('a','', 'Code ↗',links);c.href=p.code;c.target='_blank';c.rel='noopener'}if(p.authors.length)add('p','people',`Authors: ${p.authors.slice(0,8).join(', ')}${p.authors.length>8?', et al.':''}`,card);if(p.institutions.length)add('p','people',`Institutions*: ${p.institutions.slice(0,5).join('; ')}`,card);if(p.venue){const row=add('p','people','Venue: ',card),v=add(p.venueUrl?'a':'span','',`${p.venue}${p.venueType?` (${p.venueType})`:''}`,row);if(p.venueUrl){v.href=p.venueUrl;v.target='_blank';v.rel='noopener'}}if(p.transferIdeas.length)add('p','evolution',`Transferable idea: ${p.transferIdeas[0]}`,card);if(p.keyIdea)add('p','idea',p.keyIdea,card)}}
$('total').textContent=PAPERS.length.toLocaleString();$('curated').textContent=PAPERS.filter(p=>p.status==='curated').length.toLocaleString();$('discovery').textContent=PAPERS.filter(p=>p.status==='discovery').length.toLocaleString();$('months').textContent=new Set(PAPERS.map(p=>p.date.slice(0,7))).size;for(const id of controls)$(id).addEventListener(id==='q'?'input':'change',render);render();
</script></body></html>'''
    return template.replace("__PAPERS__", data).replace("__DIRECTIONS__", direction_data).replace("__LABELS__", label_data).replace("__ANALYTICS__", analytics_data).replace("__GENERATED__", snapshot_date(papers))


def update(check: bool = False) -> None:
    content = render()
    if check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Static site is stale; run python -m radar.site")
        return
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    update(args.check)


if __name__ == "__main__":
    main()
