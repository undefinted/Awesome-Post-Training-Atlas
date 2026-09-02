from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from radar.render import ROOT, all_records, load_yaml
from radar.labels import effective_labels


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
            }
        )
    return sorted(records, key=lambda paper: paper["date"], reverse=True)


def render() -> str:
    directions = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    labels = load_yaml(ROOT / "config" / "labels.yaml")["labels"]
    data = json.dumps(payload(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    direction_data = json.dumps(directions, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    label_data = json.dumps(labels, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="A searchable atlas of foundation-model post-training research.">
  <title>Awesome Post-Training Atlas</title>
  <style>
    :root{--bg:#f5f7fb;--card:#fff;--ink:#172033;--muted:#667085;--line:#dfe4ec;--accent:#3157d5;--soft:#eef2ff;--candidate:#fff7e8}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}header{background:linear-gradient(135deg,#172554,#3157d5);color:white;padding:52px max(24px,calc((100vw - 1180px)/2)) 40px}h1{margin:0 0 8px;font-size:clamp(30px,5vw,52px);letter-spacing:-.04em}header p{max-width:780px;margin:0;color:#dbe5ff;font-size:17px}.shell{max-width:1180px;margin:auto;padding:24px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:-44px}.stat,.filters,.paper,.directory,.label-picker{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:0 5px 18px #263b6410}.stat{padding:17px}.stat b{display:block;font-size:27px}.stat span{color:var(--muted)}.directory,.label-picker{padding:14px 16px;margin:18px 0}.directory summary,.label-picker summary{cursor:pointer;font-weight:700}.directory nav,.label-options{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.directory button,.label-options button{border:1px solid var(--line);background:var(--soft);color:var(--ink);border-radius:999px;padding:6px 10px;cursor:pointer}.label-options button.active{background:var(--accent);border-color:var(--accent);color:white}.label-tools{display:flex;gap:10px;align-items:center;margin-top:12px}.label-tools select{max-width:220px}.label-tools button{border:0;background:none;color:var(--accent);cursor:pointer}.filters{display:grid;grid-template-columns:2fr repeat(5,1fr);gap:10px;padding:14px;margin:18px 0}input,select{width:100%;border:1px solid var(--line);border-radius:9px;padding:10px 12px;background:white;color:var(--ink)}#summary{color:var(--muted);margin:10px 2px}.papers{display:grid;gap:10px}.paper{padding:17px}.paper.discovery{background:var(--candidate)}.paper h2{font-size:17px;line-height:1.35;margin:0 0 8px}.paper h2 a{color:var(--ink);text-decoration:none}.paper h2 a:hover{color:var(--accent)}.meta{display:flex;flex-wrap:wrap;gap:7px;color:var(--muted);font-size:13px}.pill{background:var(--soft);color:#3349a3;border-radius:999px;padding:2px 8px}.pill.label{border:1px solid #c7d2fe}.discovery .pill.status{background:#ffe5ad;color:#7a4c00}.idea,.people{margin:10px 0 0;color:#3b4558}.people{font-size:13px}.links{margin-left:auto}.links a{color:var(--accent);text-decoration:none}.empty{text-align:center;padding:60px;color:var(--muted)}footer{text-align:center;color:var(--muted);padding:36px}footer a{color:var(--accent)}@media(max-width:760px){.stats{grid-template-columns:1fr 1fr}.filters{grid-template-columns:1fr}.links{margin-left:0}}@media(prefers-color-scheme:dark){:root{--bg:#0d1320;--card:#151d2d;--ink:#edf2ff;--muted:#9eabc1;--line:#2b3548;--soft:#232e52;--candidate:#292315}input,select{background:#111827;color:var(--ink)}}
  </style>
</head>
<body>
<header><h1>Post-Training Atlas</h1><p>Search and filter curated research plus directly discovered academic candidates across language, agents, multimodal models, generative media, and embodied intelligence.</p></header>
<main class="shell">
  <section class="stats"><div class="stat"><b id="total">0</b><span>papers indexed</span></div><div class="stat"><b id="curated">0</b><span>curated</span></div><div class="stat"><b id="discovery">0</b><span>awaiting review</span></div><div class="stat"><b id="months">0</b><span>months represented</span></div></section>
  <details class="directory" open><summary>Browse directory</summary><nav id="directory"></nav></details>
  <section class="filters"><input id="q" type="search" placeholder="Search title, key idea, or tag…"><select id="direction"><option value="">All directions</option></select><select id="year"><option value="">All years</option></select><select id="month"><option value="">All months</option></select><select id="status"><option value="">All evidence levels</option><option value="curated">Curated</option><option value="discovery">Discovery candidate</option></select><select id="confidence"><option value="reliable">Curated + medium/high</option><option value="high">High-confidence only</option><option value="medium">Medium only</option><option value="broad">Broad recall only</option><option value="all">All confidence levels</option></select></section>
  <details class="label-picker" open><summary>Labels — select one or more (<span id="selectedCount">0</span> selected)</summary><div class="label-tools"><select id="labelMode"><option value="any">Match ANY selected label</option><option value="all">Match ALL selected labels</option></select><button id="clearLabels" type="button">Clear labels</button></div><div id="labelOptions" class="label-options"></div></details>
  <div id="summary"></div><section id="papers" class="papers"></section>
</main>
<footer>Generated from the <a href="https://github.com/undefinted/Awesome-Post-Training-Atlas">Awesome Post-Training Atlas</a> · __GENERATED__</footer>
<script>
const PAPERS=__PAPERS__, DIRECTIONS=__DIRECTIONS__, LABELS=__LABELS__, names=Object.fromEntries(DIRECTIONS.map(x=>[x.id,x.title])), labelNames=Object.fromEntries(LABELS.map(x=>[x.id,x.title])), selectedLabels=new Set();
const $=id=>document.getElementById(id), controls=['q','direction','year','month','status','confidence','labelMode'];
for(const d of DIRECTIONS){const o=document.createElement('option');o.value=d.id;o.textContent=d.title;$('direction').append(o)}
for(const y of [...new Set(PAPERS.map(p=>p.date.slice(0,4)))].sort().reverse()){const o=document.createElement('option');o.value=y;o.textContent=y;$('year').append(o)}
for(let m=1;m<=12;m++){const v=String(m).padStart(2,'0'),o=document.createElement('option');o.value=v;o.textContent=new Date(2000,m-1).toLocaleString('en',{month:'long'});$('month').append(o)}
for(const d of DIRECTIONS){const b=add('button','',`${d.title} (${PAPERS.filter(p=>p.direction===d.id).length})`,$('directory'));b.onclick=()=>{$('direction').value=d.id;render();scrollTo({top:$('summary').offsetTop-20,behavior:'smooth'})}}for(const y of [...new Set(PAPERS.map(p=>p.date.slice(0,4)))].sort().reverse()){const b=add('button','',`${y} (${PAPERS.filter(p=>p.date.startsWith(y)).length})`,$('directory'));b.onclick=()=>{$('year').value=y;render();scrollTo({top:$('summary').offsetTop-20,behavior:'smooth'})}}
function add(tag,cls,text,parent){const x=document.createElement(tag);if(cls)x.className=cls;if(text!==undefined)x.textContent=text;parent.append(x);return x}
for(const label of LABELS){const count=PAPERS.filter(p=>p.labels.includes(label.id)).length;if(!count)continue;const b=add('button','',`${label.title} (${count})`,$('labelOptions'));b.type='button';b.title=label.description;b.onclick=()=>{selectedLabels.has(label.id)?selectedLabels.delete(label.id):selectedLabels.add(label.id);b.classList.toggle('active',selectedLabels.has(label.id));$('selectedCount').textContent=selectedLabels.size;render()}}
$('clearLabels').onclick=()=>{selectedLabels.clear();for(const b of $('labelOptions').children)b.classList.remove('active');$('selectedCount').textContent=0;render()};
function render(){const q=$('q').value.trim().toLowerCase(),d=$('direction').value,y=$('year').value,m=$('month').value,s=$('status').value,cf=$('confidence').value,lm=$('labelMode').value,chosen=[...selectedLabels];const confidenceOK=p=>cf==='all'||cf==='reliable'&&p.confidence!=='broad'||cf==='high'&&(p.confidence==='curated'||p.confidence==='high')||cf===p.confidence,labelOK=p=>!chosen.length||(lm==='all'?chosen.every(x=>p.labels.includes(x)):chosen.some(x=>p.labels.includes(x)));const list=PAPERS.filter(p=>(!d||p.direction===d)&&(!y||p.date.startsWith(y))&&(!m||p.date.slice(5,7)===m)&&(!s||p.status===s)&&confidenceOK(p)&&labelOK(p)&&(!q||[p.title,p.keyIdea,...p.tags,...p.labels.map(x=>labelNames[x]||x),...p.authors,...p.institutions].join(' ').toLowerCase().includes(q)));$('summary').textContent=`Showing ${list.length.toLocaleString()} of ${PAPERS.length.toLocaleString()} papers${chosen.length?` · labels: ${chosen.map(x=>labelNames[x]).join(lm==='all'?' + ':' / ')}`:''}`;$('papers').replaceChildren();if(!list.length){add('div','empty','No papers match these filters.',$('papers'));return}for(const p of list){const card=add('article','paper '+p.status,undefined,$('papers')),h=add('h2','',undefined,card),a=add('a','',p.title,h);a.href=p.url;a.target='_blank';a.rel='noopener';const meta=add('div','meta',undefined,card);add('span','pill status',p.status==='curated'?'Curated':`🔎 ${p.confidence} confidence`,meta);add('span','',p.date,meta);add('span','pill',names[p.direction]||p.direction,meta);for(const t of p.labels.slice(0,8))add('span','pill label',labelNames[t]||t,meta);if(p.code){const links=add('span','links',undefined,meta),c=add('a','', 'Code ↗',links);c.href=p.code;c.target='_blank';c.rel='noopener'}if(p.authors.length)add('p','people',`Authors: ${p.authors.slice(0,8).join(', ')}${p.authors.length>8?', et al.':''}`,card);if(p.institutions.length)add('p','people',`Institutions*: ${p.institutions.slice(0,5).join('; ')}`,card);if(p.keyIdea)add('p','idea',p.keyIdea,card)}}
$('total').textContent=PAPERS.length.toLocaleString();$('curated').textContent=PAPERS.filter(p=>p.status==='curated').length.toLocaleString();$('discovery').textContent=PAPERS.filter(p=>p.status==='discovery').length.toLocaleString();$('months').textContent=new Set(PAPERS.map(p=>p.date.slice(0,7))).size;for(const id of controls)$(id).addEventListener(id==='q'?'input':'change',render);render();
</script></body></html>'''
    return template.replace("__PAPERS__", data).replace("__DIRECTIONS__", direction_data).replace("__LABELS__", label_data).replace("__GENERATED__", dt.date.today().isoformat())


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
