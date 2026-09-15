from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from radar.render import ROOT, all_records, load_yaml
from radar.labels import effective_labels
from radar.methods import method_catalog, method_metadata


OUTPUT = ROOT / "docs" / "index.html"
DATA_OUTPUT = ROOT / "docs" / "data" / "papers.json"


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
                "projectPage": paper.get("project_page"),
                "openAccessPdf": paper.get("open_access_pdf"),
                "sourceSignals": paper.get("source_signals", []),
                "sourceLinks": paper.get("source_links", {}),
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


def render(papers: list[dict] | None = None) -> str:
    directions = load_yaml(ROOT / "config" / "taxonomy.yaml")["directions"]
    labels = load_yaml(ROOT / "config" / "labels.yaml")["labels"]
    papers = payload() if papers is None else papers
    status = load_yaml(ROOT / "data" / "radar_status.yaml") or {}
    synced = str(status.get("last_successful_discovery_at", "not recorded"))
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
    :root{--bg:#f3f6fb;--card:#fff;--ink:#12213f;--muted:#6b7a93;--line:#dbe4f0;--accent:#3d5be8;--accent-2:#7757e8;--soft:#eef2ff;--candidate:#fff8eb;--shadow:0 18px 45px rgba(35,57,112,.09);--shadow-soft:0 8px 24px rgba(35,57,112,.07)}
    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{margin:0;background:radial-gradient(circle at 8% 0%,#eaf0ff 0,transparent 30%),var(--bg);color:var(--ink);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
    header{position:relative;overflow:hidden;background:linear-gradient(135deg,#101d4e 0%,#263c99 54%,#5268ed 100%);color:white;padding:62px max(24px,calc((100vw - 1240px)/2)) 78px;isolation:isolate}
    header:before,header:after{content:"";position:absolute;border-radius:50%;pointer-events:none;z-index:-1}
    header:before{width:420px;height:420px;right:-110px;top:-230px;background:radial-gradient(circle,rgba(157,181,255,.35),rgba(157,181,255,0) 68%)}
    header:after{width:520px;height:520px;left:42%;bottom:-450px;border:1px solid rgba(255,255,255,.15);box-shadow:0 0 0 34px rgba(255,255,255,.05),0 0 0 68px rgba(255,255,255,.035)}
    .header-inner{max-width:860px;min-width:0}
    .brand-row{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:20px;color:#cbd8ff;font-size:11px;font-weight:800;letter-spacing:.16em;text-transform:uppercase}
    .brand-mark{display:grid;place-items:center;width:30px;height:30px;border:1px solid rgba(255,255,255,.32);border-radius:9px;background:rgba(255,255,255,.13);color:white;font-size:11px;letter-spacing:-.05em}
    .lang-toggle{margin-left:auto;display:flex;gap:3px;padding:3px;border:1px solid rgba(255,255,255,.28);border-radius:999px;background:rgba(255,255,255,.1)}
    .lang-toggle button{border:0;border-radius:999px;background:transparent;color:#cbd8ff;padding:5px 11px;cursor:pointer;font:inherit;font-size:11px;font-weight:800;letter-spacing:.04em;transition:.18s ease}
    .lang-toggle button:hover{color:white}
    .lang-toggle button.active{background:white;color:#263c99}
    h1{margin:0 0 14px;font-size:clamp(38px,6vw,68px);letter-spacing:-.055em;line-height:.98}
    h1 span{background:linear-gradient(90deg,#fff,#cbd6ff);-webkit-background-clip:text;background-clip:text;color:transparent}
    header p{max-width:790px;margin:0;color:#dce5ff;font-size:18px;line-height:1.62}
    .header-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:25px}
    .header-meta span{padding:6px 10px;border:1px solid rgba(255,255,255,.2);border-radius:999px;background:rgba(255,255,255,.09);color:#e8edff;font-size:12px}
    .shell{max-width:1240px;margin:auto;padding:0 26px 70px}
    .stats{position:relative;z-index:2;display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:-39px}
    .stat,.filters,.paper,.directory,.label-picker,.insights,.chart-card,.featured{min-width:0;background:rgba(255,255,255,.92);border:1px solid rgba(207,218,235,.9);border-radius:20px;box-shadow:var(--shadow-soft)}
    .stat{position:relative;overflow:hidden;padding:22px 22px 20px;min-height:112px;transition:transform .2s ease,box-shadow .2s ease}
    .stat:before{content:"";position:absolute;left:0;right:0;top:0;height:4px;background:linear-gradient(90deg,var(--accent),var(--accent-2))}
    .stat:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
    .stat b{display:block;font-size:34px;line-height:1.05;letter-spacing:-.04em}
    .stat span{display:block;margin-top:8px;color:var(--muted);font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
    .featured{position:relative;overflow:hidden;margin:20px 0;padding:23px;background:linear-gradient(135deg,rgba(255,255,255,.98),rgba(239,243,255,.94))}
    .featured:after{content:"";position:absolute;width:230px;height:230px;right:-90px;top:-130px;border-radius:50%;background:radial-gradient(circle,rgba(99,120,240,.18),transparent 70%);pointer-events:none}
    .feature-head{position:relative;z-index:1;display:flex;justify-content:space-between;gap:20px;align-items:flex-end;margin-bottom:17px}
    .feature-head h2{margin:4px 0 3px;font-size:27px;letter-spacing:-.035em}.feature-description{margin:0;color:var(--muted);font-size:12px}
    .feature-controls{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:9px}.feature-tabs,.feature-nav{display:flex;gap:5px;padding:4px;border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.72)}
    .feature-tabs button,.feature-nav button{border:0;border-radius:8px;background:transparent;color:var(--muted);padding:7px 10px;cursor:pointer;font:inherit;font-size:12px;font-weight:750;transition:.18s ease}
    .feature-tabs button:hover,.feature-nav button:hover{background:var(--soft);color:var(--accent)}.feature-tabs button.active{background:linear-gradient(135deg,var(--accent),var(--accent-2));color:white;box-shadow:0 5px 13px rgba(61,91,232,.22)}
    .feature-grid{position:relative;z-index:1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px}
    .feature-card{display:flex;min-width:0;min-height:224px;flex-direction:column;padding:17px;border:1px solid #dce4f5;border-radius:16px;background:rgba(255,255,255,.88);box-shadow:0 8px 20px rgba(35,57,112,.06);animation:feature-in .38s ease both}
    .feature-card.discovery{border-color:#efd9a9;background:linear-gradient(145deg,#fffef9,#fff7e7)}.feature-top{display:flex;gap:7px;align-items:center;color:var(--muted);font-size:11px}.feature-top .feature-status{margin-left:auto}.feature-status{padding:3px 8px;border-radius:999px;background:#e8edff;color:#4055b2;font-weight:800}.feature-card.discovery .feature-status{background:#ffe7b5;color:#865600}
    .feature-card h3{margin:11px 0 8px;font-size:16px;line-height:1.38;letter-spacing:-.018em}.feature-card h3 a{color:var(--ink);text-decoration:none}.feature-card h3 a:hover{color:var(--accent)}
    .feature-idea{display:-webkit-box;overflow:hidden;margin:0 0 12px;color:#536078;font-size:12px;-webkit-line-clamp:3;-webkit-box-orient:vertical}.feature-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:auto}.feature-tags span{padding:3px 7px;border-radius:999px;background:var(--soft);color:#4659a8;font-size:10px;font-weight:700}.feature-links{display:flex;flex-wrap:wrap;gap:12px;margin-top:13px}.feature-links a{color:var(--accent);font-size:11px;font-weight:800;text-decoration:none}
    .feature-foot{position:relative;z-index:1;display:flex;justify-content:space-between;align-items:center;gap:15px;margin-top:14px;color:var(--muted);font-size:11px}.feature-progress{display:flex;gap:5px}.feature-progress button{width:19px;height:4px;padding:0;border:0;border-radius:999px;background:#d5dced;cursor:pointer;transition:.2s}.feature-progress button.active{width:34px;background:var(--accent)}
    @keyframes feature-in{from{opacity:0;transform:translateX(10px)}to{opacity:1;transform:none}}
    .directory,.label-picker,.insights{padding:21px 22px;margin:20px 0}
    .directory summary,.label-picker summary{cursor:pointer;font-weight:800;list-style:none}
    .directory summary::-webkit-details-marker,.label-picker summary::-webkit-details-marker{display:none}
    .directory summary:before,.label-picker summary:before{content:"＋";display:inline-grid;place-items:center;width:20px;height:20px;margin-right:7px;border-radius:50%;background:var(--soft);color:var(--accent);font-size:15px;line-height:1}
    details[open]>summary:before{content:"−"}
    .directory nav,.label-options{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
    .directory button,.label-options button,.family-options button{border:1px solid var(--line);background:linear-gradient(180deg,#f8faff,#eef2ff);color:#30436d;border-radius:999px;padding:7px 11px;cursor:pointer;font:inherit;font-size:12px;transition:all .18s ease}
    .directory button:hover,.label-options button:hover,.family-options button:hover{border-color:#aebdf5;background:#e3e9ff;transform:translateY(-1px)}
    .label-options button.active,.family-options button.active{background:linear-gradient(135deg,var(--accent),#6578f2);border-color:var(--accent);color:white;box-shadow:0 7px 16px rgba(61,91,232,.22)}
    .label-tools{display:flex;gap:10px;align-items:center;margin-top:14px}
    .label-tools select{max-width:235px}
    .label-tools button{border:0;background:none;color:var(--accent);cursor:pointer;font:inherit;font-size:12px}
    .filters{position:sticky;top:14px;z-index:10;display:grid;grid-template-columns:minmax(240px,2fr) repeat(6,minmax(115px,1fr));gap:9px;padding:12px;margin:20px 0;background:rgba(255,255,255,.82);backdrop-filter:blur(16px);box-shadow:0 12px 28px rgba(35,57,112,.1)}
    input,select{width:100%;border:1px solid var(--line);border-radius:11px;padding:10px 12px;background:#fbfcff;color:var(--ink);font:inherit;font-size:13px;outline:none;transition:border-color .18s ease,box-shadow .18s ease,background .18s ease}
    input:focus,select:focus{border-color:#8699f3;background:white;box-shadow:0 0 0 4px rgba(61,91,232,.12)}
    #summary{color:var(--muted);margin:14px 3px;font-size:13px;font-weight:600}
    .papers{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,500px),1fr));gap:14px;align-items:start}
    .load-more{display:flex;justify-content:center;margin:24px 0}.load-more button{border:1px solid #bdc9f1;border-radius:999px;background:linear-gradient(135deg,var(--accent),var(--accent-2));color:white;padding:11px 22px;cursor:pointer;font:inherit;font-size:13px;font-weight:800;box-shadow:0 9px 20px rgba(61,91,232,.2)}.load-more button:hover{transform:translateY(-2px);box-shadow:0 13px 26px rgba(61,91,232,.27)}.load-more button[hidden]{display:none}
    .paper{padding:19px 20px;transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
    .paper:hover{transform:translateY(-3px);border-color:#b9c6ef;box-shadow:var(--shadow)}
    .paper.discovery{background:linear-gradient(145deg,#fffdf7,var(--candidate));border-color:#f2dfb4}
    .paper h2{font-size:17px;line-height:1.4;margin:0 0 10px;letter-spacing:-.015em}
    .paper h2 a{color:var(--ink);text-decoration:none}
    .paper h2 a:hover{color:var(--accent)}
    .meta{display:flex;flex-wrap:wrap;gap:6px;color:var(--muted);font-size:12px;align-items:center}
    .pill{background:#eff3ff;color:#3b4fa5;border-radius:999px;padding:3px 9px;font-size:11px;font-weight:650}
    .pill.label{border:1px solid #c8d2fb}.pill.family{background:#e4e9ff;color:#3045a0}.pill.axis{background:#f2f5f9;color:#526176}.discovery .pill.status{background:#ffe8b8;color:#895800}
    .idea,.people,.evolution{margin:11px 0 0;color:#46546b}.people,.evolution{font-size:12px}.people a,.evolution a{color:var(--accent);text-decoration:none}.links{margin-left:auto}.links a{color:var(--accent);text-decoration:none;font-weight:700}.empty{text-align:center;padding:72px;color:var(--muted)}
    footer{text-align:center;color:var(--muted);padding:42px 20px;font-size:12px}footer a{color:var(--accent)}
    .insight-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;margin-bottom:17px}.eyebrow{margin:0;color:var(--accent);font-size:11px;font-weight:850;letter-spacing:.16em;text-transform:uppercase}.insight-head h2{margin:4px 0 0;font-size:27px;letter-spacing:-.035em}.insight-note{margin:0;color:var(--muted);font-size:12px}.insight-grid{display:grid;grid-template-columns:1.35fr 1fr 1fr;gap:14px}.chart-card{padding:17px;box-shadow:none;background:linear-gradient(145deg,#fff,#fafcff);border-radius:16px}.chart-card.wide{min-width:0}.chart-title{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:13px}.chart-title h3{margin:0;font-size:15px;letter-spacing:-.01em}.chart-title span{color:var(--muted);font-size:11px}.bar-chart{display:grid;gap:9px}.bar-row{display:grid;grid-template-columns:minmax(112px,1fr) 2fr auto;gap:9px;align-items:center;font-size:12px}.bar-label{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.bar-track{display:block;height:9px;background:#edf1fb;border-radius:999px;overflow:hidden}.bar-fill{display:block;height:100%;min-width:3px;border-radius:999px;background:linear-gradient(90deg,var(--accent),var(--accent-2));box-shadow:0 2px 7px rgba(61,91,232,.28);transform-origin:left center;animation:bar-grow .55s ease-out both}.bar-value{color:var(--muted);font-variant-numeric:tabular-nums;font-weight:750}@keyframes bar-grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}.trend{width:100%;height:146px;display:block}.trend-grid{stroke:#e4e9f2;stroke-width:1}.trend-area{fill:url(#trendFill);opacity:.5}.trend-line{fill:none;stroke:var(--accent);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}.trend-labels{display:flex;justify-content:space-between;color:var(--muted);font-size:11px}.family-card{margin-top:14px}.family-options{display:flex;flex-wrap:wrap;gap:7px;margin:5px 0 15px}.family-options button{font-size:12px}.family-description{margin:0 0 14px;color:var(--muted);font-size:13px}.family-timeline{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:11px}.timeline-item{border:1px solid #dbe3f5;border-left:4px solid var(--accent);border-radius:13px;padding:13px;background:linear-gradient(145deg,#fff,#f1f4ff);transition:transform .18s ease,box-shadow .18s ease}.timeline-item:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(45,63,124,.1)}.timeline-date{color:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}.timeline-item a{display:block;margin:5px 0 8px;color:var(--ink);font-weight:800;text-decoration:none;line-height:1.38;letter-spacing:-.012em}.timeline-item a:hover{color:var(--accent)}.timeline-axes{display:flex;flex-wrap:wrap;gap:4px}.timeline-axes span{font-size:10px;background:white;border:1px solid #dfe5f0;border-radius:999px;padding:2px 7px;color:#65728a}.timeline-idea,.timeline-relation{margin:9px 0 0;color:var(--muted);font-size:12px}.timeline-relation a{display:inline;font-weight:700;color:var(--accent)}.no-timeline{padding:22px;color:var(--muted);text-align:center}
    @media(max-width:1000px){.filters{position:static;grid-template-columns:repeat(3,1fr)}.filters input{grid-column:1/-1}.insight-grid{grid-template-columns:1fr 1fr}.chart-card.wide{grid-column:1/-1}.feature-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
    @media(max-width:720px){header{padding:44px 22px 64px}.shell{padding:0 16px 50px}.stats{grid-template-columns:1fr 1fr;gap:10px;margin-top:-30px}.stat{padding:17px;min-height:96px}.stat b{font-size:28px}.directory,.label-picker,.insights,.featured{padding:17px;margin:14px 0}.filters{grid-template-columns:1fr 1fr}.insight-grid{grid-template-columns:1fr}.insight-head,.feature-head{display:block}.insight-note{margin-top:7px}.feature-controls{justify-content:flex-start;margin-top:14px}.feature-grid{grid-template-columns:1fr}.family-timeline{grid-template-columns:1fr}.links{margin-left:0}}
    @media(max-width:440px){.stats{grid-template-columns:1fr}.filters{grid-template-columns:1fr}.label-tools{align-items:stretch;flex-direction:column}.label-tools select{max-width:none}.header-meta span{font-size:11px}}
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.feature-card,.bar-fill{animation:none}}
    @media(prefers-color-scheme:dark){:root{--bg:#0b1220;--card:#141d2f;--ink:#edf2ff;--muted:#9aa9c2;--line:#2b3850;--soft:#202d50;--candidate:#2a2517;--shadow:0 18px 45px rgba(0,0,0,.28);--shadow-soft:0 8px 24px rgba(0,0,0,.2)}body{background:radial-gradient(circle at 8% 0%,#17264a 0,transparent 32%),var(--bg)}.stat,.filters,.paper,.directory,.label-picker,.insights,.chart-card,.featured{background:rgba(20,29,47,.94);border-color:var(--line)}.featured{background:linear-gradient(135deg,rgba(20,29,47,.98),rgba(27,39,70,.94))}.feature-tabs,.feature-nav{background:rgba(13,21,37,.65)}.feature-card{background:rgba(23,34,56,.92);border-color:#30405e}.feature-card.discovery{background:linear-gradient(145deg,#2b2619,#302817);border-color:#5d4b28}.feature-idea{color:var(--muted)}.filters{background:rgba(20,29,47,.82)}input,select{background:#101827;color:var(--ink)}input:focus,select:focus{background:#141d2f}.chart-card{background:linear-gradient(145deg,#172238,#121b2d)}.bar-track{background:#202d50}.timeline-item{background:linear-gradient(145deg,#172238,#202d50);border-color:#2d3d5c}.timeline-axes span{background:#172238;border-color:#35445f}.paper.discovery{background:linear-gradient(145deg,#2b2619,#302817)}}
    .header-inner,.stats,.insight-grid,.papers,.stat,.chart-card,.paper{min-width:0}
    .brand-row{flex-wrap:wrap}
    .bar-row,.bar-label,.bar-track,.timeline-item{min-width:0}
  </style>
</head>
<body>
<header><div class="header-inner"><div class="brand-row"><span class="brand-mark">PT</span><span data-i18n="brand">Research intelligence · methods in motion</span><div class="lang-toggle" role="group" aria-label="Language / 语言"><button type="button" data-lang="en">EN</button><button type="button" data-lang="zh">中文</button></div></div><h1>Post-Training <span>Atlas</span></h1><p data-i18n="tagline">Track how post-training methods evolve across language, agents, multimodal models, generative media, and embodied intelligence — then explore the ideas that may transfer across settings.</p><div class="header-meta"><span><span data-i18n="meta_radar">Radar scanned</span> __SYNCED__ <span data-i18n="meta_radar_tz">CST</span></span><span data-i18n="meta_index">Curated + discovery index</span><span data-i18n="meta_pulse">Monthly research pulse</span><span data-i18n="meta_evolution">Method evolution map</span></div></div></header>
<main class="shell">
  <section class="stats"><div class="stat"><b id="total">0</b><span data-i18n="stat_total">papers indexed</span></div><div class="stat"><b id="curated">0</b><span data-i18n="stat_curated">curated</span></div><div class="stat"><b id="discovery">0</b><span data-i18n="stat_discovery">awaiting review</span></div><div class="stat"><b id="months">0</b><span data-i18n="stat_months">months represented</span></div></section>
  <section class="featured" id="featured"><div class="feature-head"><div><p class="eyebrow" data-i18n="feat_eyebrow">Latest &amp; noteworthy</p><h2 data-i18n="feat_title">Methods worth watching</h2><p class="feature-description" id="featureDescription"></p></div><div class="feature-controls"><div class="feature-tabs" id="featureTabs" role="tablist"><button class="active" data-mode="latest" role="tab" aria-selected="true" data-i18n="tab_latest">Latest</button><button data-mode="picks" role="tab" aria-selected="false" data-i18n="tab_picks">Editor's picks</button><button data-mode="signals" role="tab" aria-selected="false" data-i18n="tab_signals">Radar signals</button></div><div class="feature-nav"><button id="featurePrev" type="button" aria-label="Previous papers" data-i18n-aria="feat_prev">←</button><button id="featurePause" type="button" aria-label="Pause automatic rotation" data-i18n-aria="feat_pause">Ⅱ</button><button id="featureNext" type="button" aria-label="Next papers" data-i18n-aria="feat_next">→</button></div></div></div><div id="featureGrid" class="feature-grid" aria-live="polite"></div><div class="feature-foot"><span id="featurePage"></span><div id="featureProgress" class="feature-progress"></div><span data-i18n="feat_note">Discovery candidates remain clearly marked until reviewed.</span></div></section>
  <section class="insights"><div class="insight-head"><div><p class="eyebrow" data-i18n="ins_eyebrow">Method evolution</p><h2 data-i18n="ins_title">Research pulse</h2></div><p class="insight-note" data-i18n="ins_note">Volume uses all indexed records; method timelines use curated, annotated entries.</p></div><div class="insight-grid"><article class="chart-card wide"><div class="chart-title"><h3 data-i18n="chart_direction">Direction volume</h3><span data-i18n="chart_direction_sub">indexed records</span></div><div id="directionChart" class="bar-chart"></div></article><article class="chart-card"><div class="chart-title"><h3 data-i18n="chart_monthly">Monthly activity</h3><span data-i18n="chart_monthly_sub">all records</span></div><svg id="trendChart" class="trend" viewBox="0 0 720 170" role="img" data-i18n-aria="trend_aria" aria-label="Monthly paper activity chart"></svg><div id="trendLabels" class="trend-labels"></div></article><article class="chart-card"><div class="chart-title"><h3 data-i18n="chart_axes">What methods change</h3><span data-i18n="chart_axes_sub">curated entries</span></div><div id="axisChart" class="bar-chart"></div></article></div><article class="chart-card family-card"><div class="chart-title"><h3 data-i18n="chart_family">Method family timeline</h3><span id="familyCount"></span></div><div id="familyOptions" class="family-options"></div><p id="familyDescription" class="family-description"></p><div id="familyTimeline" class="family-timeline"></div></article></section>
  <details class="directory" open><summary data-i18n="dir_browse">Browse directory</summary><nav id="directory"></nav></details>
  <section class="filters"><input id="q" type="search" placeholder="Search title, key idea, method, or tag…" data-i18n-ph="search_ph"><select id="direction"><option value="" data-i18n="all_directions">All directions</option></select><select id="family"><option value="" data-i18n="all_families">All method families</option></select><select id="year"><option value="" data-i18n="all_years">All years</option></select><select id="month"><option value="" data-i18n="all_months">All months</option></select><select id="status"><option value="" data-i18n="all_status">All evidence levels</option><option value="curated" data-i18n="status_curated">Curated</option><option value="discovery" data-i18n="status_discovery">Discovery candidate</option></select><select id="confidence"><option value="reliable" data-i18n="conf_reliable">Curated + medium/high</option><option value="high" data-i18n="conf_high">High-confidence only</option><option value="medium" data-i18n="conf_medium">Medium only</option><option value="broad" data-i18n="conf_broad">Broad recall only</option><option value="all" data-i18n="conf_all">All confidence levels</option></select></section>
  <details class="label-picker" open><summary><span data-i18n="labels_pre">Labels — select one or more (</span><span id="selectedCount">0</span><span data-i18n="labels_post"> selected)</span></summary><div class="label-tools"><select id="labelMode"><option value="any" data-i18n="label_any">Match ANY selected label</option><option value="all" data-i18n="label_all">Match ALL selected labels</option></select><button id="clearLabels" type="button" data-i18n="label_clear">Clear labels</button></div><div id="labelOptions" class="label-options"></div></details>
  <div id="summary" data-i18n="loading">Loading the paper index…</div><section id="papers" class="papers"></section><div class="load-more"><button id="loadMore" type="button" hidden data-i18n="load_more">Load 40 more papers</button></div>
</main>
<footer><span data-i18n="footer_note">* Institutions and publication venues are displayed only when sourced from academic metadata; author-profile affiliations may differ from publication-time affiliations.</span><br><span data-i18n="footer_scan">Radar last scanned</span> __SYNCED__ <span data-i18n="footer_scan_tz">CST</span> · <span data-i18n="footer_latest">Latest indexed paper dated</span> __GENERATED__ · <span data-i18n="footer_from">Generated from the</span> <a href="https://github.com/undefinted/Awesome-Post-Training-Atlas">Awesome Post-Training Atlas</a><span data-i18n="footer_from_post"></span></footer>
<script>
let PAPERS=[];const DIRECTIONS=__DIRECTIONS__, LABELS=__LABELS__, ANALYTICS=__ANALYTICS__, names=Object.fromEntries(DIRECTIONS.map(x=>[x.id,x.title])), labelNames=Object.fromEntries(LABELS.map(x=>[x.id,x.title])), selectedLabels=new Set();
const $=id=>document.getElementById(id), controls=['q','direction','family','year','month','status','confidence','labelMode'];
const I18N={en:{
brand:'Research intelligence · methods in motion',tagline:'Track how post-training methods evolve across language, agents, multimodal models, generative media, and embodied intelligence — then explore the ideas that may transfer across settings.',meta_radar:'Radar scanned',meta_radar_tz:'CST',meta_index:'Curated + discovery index',meta_pulse:'Monthly research pulse',meta_evolution:'Method evolution map',
stat_total:'papers indexed',stat_curated:'curated',stat_discovery:'awaiting review',stat_months:'months represented',
feat_eyebrow:'Latest & noteworthy',feat_title:'Methods worth watching',tab_latest:'Latest',tab_picks:"Editor's picks",tab_signals:'Radar signals',feat_prev:'Previous papers',feat_next:'Next papers',feat_pause:'Pause automatic rotation',feat_resume:'Resume automatic rotation',feat_note:'Discovery candidates remain clearly marked until reviewed.',feat_radar:'Radar',
feat_desc_latest:'Recently indexed medium/high-confidence papers and curated entries.',feat_desc_picks:'Curated papers with method-evolution or transferable-idea annotations.',feat_desc_signals:'Recent, well-supported candidates ranked by Radar evidence signals — not popularity.',feat_pick:"Editor's pick",feat_idea_fallback:'Newly discovered candidate awaiting an editorial method summary.',feat_page:(n,cur,pages)=>`${n} papers · page ${cur} of ${pages}`,feat_progress_aria:i=>`Show featured page ${i}`,
ins_eyebrow:'Method evolution',ins_title:'Research pulse',ins_note:'Volume uses all indexed records; method timelines use curated, annotated entries.',chart_direction:'Direction volume',chart_direction_sub:'indexed records',chart_monthly:'Monthly activity',chart_monthly_sub:'all records',trend_aria:'Monthly paper activity chart',chart_axes:'What methods change',chart_axes_sub:'curated entries',chart_family:'Method family timeline',family_count:n=>`${n} annotated papers`,family_desc_fallback:'Method-family annotations will appear as the atlas is reviewed.',timeline_precedent:'Related precedent: ',timeline_idea:'Idea surface: ',no_family_papers:'No annotated papers in this family yet.',no_records:'No annotated records yet.',
dir_browse:'Browse directory',search_ph:'Search title, key idea, method, or tag…',all_directions:'All directions',all_families:'All method families',all_years:'All years',all_months:'All months',all_status:'All evidence levels',status_curated:'Curated',status_discovery:'Discovery candidate',conf_reliable:'Curated + medium/high',conf_high:'High-confidence only',conf_medium:'Medium only',conf_broad:'Broad recall only',conf_all:'All confidence levels',
labels_pre:'Labels — select one or more (',labels_post:' selected)',label_any:'Match ANY selected label',label_all:'Match ALL selected labels',label_clear:'Clear labels',loading:'Loading the paper index…',load_error:'The paper index could not be loaded. Please refresh the page.',no_match:'No papers match these filters.',load_more:'Load 40 more papers',summary:(shown,total,indexed,labelStr)=>`Showing ${shown} of ${total} matching papers · ${indexed} indexed${labelStr?` · labels: ${labelStr}`:''}`,
confShort_high:'high confidence',confShort_medium:'medium confidence',confShort_broad:'broad confidence',link_paper:'Paper',link_project:'Project',link_code:'Code',link_openpdf:'Open PDF',authors_pre:'Authors: ',et_al:', et al.',institutions_pre:'Institutions*: ',venue_pre:'Venue: ',transfer_pre:'Transferable idea: ',
footer_note:'* Institutions and publication venues are displayed only when sourced from academic metadata; author-profile affiliations may differ from publication-time affiliations.',footer_scan:'Radar last scanned',footer_scan_tz:'CST',footer_latest:'Latest indexed paper dated',footer_from:'Generated from the',footer_from_post:''
},zh:{
brand:'研究情报 · 方法演进',tagline:'追踪后训练方法在语言、智能体、多模态模型、生成式媒体与具身智能等方向的演进,并探索可跨场景迁移的思路。',meta_radar:'雷达扫描于',meta_radar_tz:'(CST)',meta_index:'精选 + 发现索引',meta_pulse:'月度研究脉搏',meta_evolution:'方法演进图谱',
stat_total:'已收录论文',stat_curated:'精选论文',stat_discovery:'待审核',stat_months:'覆盖月份',
feat_eyebrow:'最新与值得关注',feat_title:'值得关注的方法',tab_latest:'最新',tab_picks:'编辑推荐',tab_signals:'雷达信号',feat_prev:'上一批论文',feat_next:'下一批论文',feat_pause:'暂停自动轮播',feat_resume:'继续自动轮播',feat_note:'发现候选在人工审核前会一直明确标注。',feat_radar:'雷达',
feat_desc_latest:'最近收录的中/高置信论文与精选条目。',feat_desc_picks:'带有方法演进或可迁移思路标注的精选论文。',feat_desc_signals:'按雷达证据信号(而非热度)排序的近期优质候选。',feat_pick:'编辑推荐',feat_idea_fallback:'新发现的候选论文,等待编辑补充方法摘要。',feat_page:(n,cur,pages)=>`共 ${n} 篇 · 第 ${cur}/${pages} 页`,feat_progress_aria:i=>`显示第 ${i} 页精选`,
ins_eyebrow:'方法演进',ins_title:'研究脉搏',ins_note:'数量统计基于全部收录记录;方法时间线仅使用精选并标注的条目。',chart_direction:'各方向论文量',chart_direction_sub:'收录记录',chart_monthly:'月度活跃度',chart_monthly_sub:'全部记录',trend_aria:'月度论文活跃度图表',chart_axes:'方法改变了什么',chart_axes_sub:'精选条目',chart_family:'方法家族时间线',family_count:n=>`${n} 篇已标注论文`,family_desc_fallback:'随着图谱持续审核,方法家族标注将逐步补充。',timeline_precedent:'相关前序工作:',timeline_idea:'可迁移思路:',no_family_papers:'该家族暂无已标注论文。',no_records:'暂无已标注记录。',
dir_browse:'浏览目录',search_ph:'搜索标题、要点、方法或标签…',all_directions:'全部方向',all_families:'全部方法家族',all_years:'全部年份',all_months:'全部月份',all_status:'全部证据等级',status_curated:'精选',status_discovery:'发现候选',conf_reliable:'精选 + 中/高置信',conf_high:'仅高置信',conf_medium:'仅中置信',conf_broad:'仅广泛召回',conf_all:'全部置信等级',
labels_pre:'标签 — 可选择一个或多个(已选 ',labels_post:' 个)',label_any:'匹配任一已选标签',label_all:'匹配全部已选标签',label_clear:'清除标签',loading:'正在加载论文索引…',load_error:'论文索引加载失败,请刷新页面。',no_match:'没有符合筛选条件的论文。',load_more:'再加载 40 篇',summary:(shown,total,indexed,labelStr)=>`显示 ${shown} / ${total} 篇匹配论文 · 共收录 ${indexed} 篇${labelStr?` · 标签:${labelStr}`:''}`,
confShort_high:'高置信',confShort_medium:'中置信',confShort_broad:'广泛召回',link_paper:'论文',link_project:'项目',link_code:'代码',link_openpdf:'开放 PDF',authors_pre:'作者:',et_al:' 等',institutions_pre:'机构*:',venue_pre:'发表场所:',transfer_pre:'可迁移思路:',
footer_note:'* 机构与发表场所信息仅在来自学术元数据时展示;作者个人主页上的单位可能与论文发表时的单位不同。',footer_scan:'雷达最近扫描于',footer_scan_tz:'(CST)',footer_latest:'最新收录论文日期',footer_from:'由',footer_from_post:' 生成',
directionNames:{'supervised-adaptation':'监督适配与数据','preference-alignment':'偏好优化与对齐','reward-verifiers':'奖励模型与验证器','reinforcement-learning':'强化学习与可验证奖励','distillation':'蒸馏与策略迁移','reasoning-self-improvement':'推理与自我改进','agentic':'智能体与交互式后训练','multimodal':'多模态 / VLM / MLLM 后训练','generative-media':'生成式媒体后训练','embodied-vla':'具身智能与 VLA 后训练'},
labelNames:{'opd':'OPD','opsd':'OPSD','distillation':'蒸馏','counterfactual':'反事实','sft':'SFT','rejection-sampling':'拒绝采样','dpo':'DPO','preference-optimization':'偏好优化','rlhf':'RLHF','rlaif':'RLAIF','rlvr':'RLVR','grpo':'GRPO','ppo':'PPO','on-policy':'On-policy','off-policy':'Off-policy','reward-model':'奖励模型','prm':'PRM','verifier':'验证器','self-training':'自训练','self-improvement':'自我改进','self-play':'自博弈','synthetic-data':'合成数据','curriculum':'课程学习','agent':'智能体','tool-use':'工具使用','web-agent':'网页智能体','coding-agent':'编程智能体','multi-turn':'多轮','long-horizon':'长程任务','multimodal':'多模态','vlm':'VLM','diffusion':'扩散模型','image-generation':'图像生成','video-generation':'视频生成','vla':'VLA','robotics':'机器人','autonomous-driving':'自动驾驶','reasoning':'推理','math':'数学','code':'代码','safety':'安全','hallucination':'幻觉'},
labelDesc:{'opd':'同策略蒸馏','opsd':'同策略自蒸馏','distillation':'从教师模型迁移知识或策略','counterfactual':'反事实数据、推理或反馈','sft':'监督微调与指令微调','rejection-sampling':'拒绝采样微调或数据筛选','dpo':'直接偏好优化及其命名变体','preference-optimization':'直接从偏好比较中学习','rlhf':'基于人类反馈的强化学习','rlaif':'基于 AI 反馈的强化学习','rlvr':'基于可验证奖励的强化学习','grpo':'组相对策略优化','ppo':'近端策略优化','on-policy':'在当前策略生成的样本上训练','off-policy':'在来自其他或旧策略的数据上训练','reward-model':'学习得到的奖励或偏好模型','prm':'过程奖励模型或过程监督','verifier':'用于反馈的验证器或评判器','self-training':'在模型生成的监督信号上训练','self-improvement':'迭代式自主能力提升','self-play':'策略通过自博弈学习','synthetic-data':'模型生成的训练数据','curriculum':'课程式或自适应任务生成','agent':'智能体系统与智能体训练','tool-use':'学习调用工具或 API','web-agent':'网页导航与浏览器智能体','coding-agent':'软件工程与编程智能体','multi-turn':'多轮交互或训练','long-horizon':'长程任务与信用分配','multimodal':'结合多种模态的模型','vlm':'视觉语言模型','diffusion':'扩散与流生成模型','image-generation':'文生图与图像合成','video-generation':'文生视频与视频合成','vla':'视觉-语言-动作模型','robotics':'机器人策略与具身控制','autonomous-driving':'驾驶策略与世界模型','reasoning':'通用推理与思维链','math':'数学推理','code':'代码生成与编程','safety':'安全对齐与有害性降低','hallucination':'幻觉与事实性'},
familyNames:{'on-policy-distillation':'On-Policy 蒸馏','rlvr-grpo':'RL 优化与可验证奖励','preference-optimization':'偏好优化','reasoning-self-improvement':'推理与自我改进','agentic-feedback':'智能体反馈与工具使用','multimodal-alignment':'多模态对齐','generative-alignment':'生成式媒体对齐','embodied-transfer':'具身与 VLA 迁移','data-feedback':'数据与反馈构造'},
familyDesc:{'on-policy-distillation':'在学生策略生成的状态上蒸馏教师或自教师信号。','rlvr-grpo':'使用学习型或可编程奖励优化采样策略,包括组相对与基于验证器的信号。','preference-optimization':'利用成对、标量、人类或 AI 偏好信号改变模型行为,而无需相同的在线回路。','reasoning-self-improvement':'把生成的推理、批评、自我奖励或自博弈转化为额外的学习信号。','agentic-feedback':'用工具、浏览器、环境或多步交互(而非孤立回复)训练模型。','multimodal-alignment':'通过指令、偏好、奖励或跨模态反馈来适配或对齐感知-语言系统。','generative-alignment':'让扩散、图像、视频等生成模型对齐奖励、偏好与任务相关反馈。','embodied-transfer':'通过多模态后训练,把网页或语言知识迁移到真实场景的动作与控制中。','data-feedback':'通过构造、筛选、扩展或监督数据与反馈回路本身来改进后训练。'},
axisNames:{'data':'数据','objective':'目标','feedback':'反馈','reward':'奖励','verifier':'验证器','sampling':'采样','optimization':'优化','efficiency':'效率','credit-assignment':'信用分配','tokenization':'分词','long-horizon':'长程','self-improvement':'自我改进','environment':'环境','cross-modal':'跨模态','safety':'安全'}
}};
let lang=localStorage.getItem('atlas-lang')||((navigator.language||'en').toLowerCase().startsWith('zh')?'zh':'en');
const t=key=>(I18N[lang]&&I18N[lang][key])??I18N.en[key]??key;
const dirName=id=>lang==='zh'?(I18N.zh.directionNames[id]||names[id]||id):(names[id]||id);
const labelName=id=>lang==='zh'?(I18N.zh.labelNames[id]||labelNames[id]||id):(labelNames[id]||id);
const labelDesc=id=>lang==='zh'?(I18N.zh.labelDesc[id]||''):'';
const familyName=(id,title)=>lang==='zh'?(I18N.zh.familyNames[id]||title||id):(title||id);
const familyDesc=f=>lang==='zh'?(I18N.zh.familyDesc[f.id]||f.description):f.description;
const axisName=id=>lang==='zh'?(I18N.zh.axisNames[id]||axisNames[id]||id):(axisNames[id]||id);
function setOptions(sel,rows){const v=sel.value;sel.replaceChildren();for(const [value,text] of rows){const o=document.createElement('option');o.value=value;o.textContent=text;sel.append(o)}sel.value=v}
function renderFilterOptions(){setOptions($('direction'),[['',t('all_directions')],...DIRECTIONS.map(d=>[d.id,dirName(d.id)])]);setOptions($('family'),[['',t('all_families')],...ANALYTICS.families.filter(x=>x.count).map(f=>[f.id,familyName(f.id,f.title)])]);setOptions($('month'),[['',t('all_months')],...Array.from({length:12},(_,i)=>[String(i+1).padStart(2,'0'),new Date(2000,i).toLocaleString(lang==='zh'?'zh-CN':'en',{month:'long'})])])}
function add(tag,cls,text,parent){const x=document.createElement(tag);if(cls)x.className=cls;if(text!==undefined)x.textContent=text;parent.append(x);return x}
const axisNames={data:'Data',objective:'Objective',feedback:'Feedback',reward:'Reward',verifier:'Verifier',sampling:'Sampling',optimization:'Optimization',efficiency:'Efficiency','credit-assignment':'Credit assignment',tokenization:'Tokenization','long-horizon':'Long horizon','self-improvement':'Self-improvement',environment:'Environment','cross-modal':'Cross-modal',safety:'Safety'};
let selectedFamily=(ANALYTICS.families.find(x=>x.count)||{}).id||'';
function drawBars(id,rows,label){const box=$(id);box.replaceChildren();if(!rows.length){add('div','no-timeline',t('no_records'),box);return}const max=Math.max(...rows.map(x=>x.count),1);for(const row of rows){const line=add('div','bar-row',undefined,box);add('span','bar-label',label(row),line);const track=add('span','bar-track',undefined,line),fill=add('span','bar-fill',undefined,track);fill.style.width=`${Math.max(3,100*row.count/max)}%`;add('span','bar-value',row.count.toLocaleString(),line)}}
function drawTrend(){const svg=$('trendChart'),rows=ANALYTICS.months;svg.replaceChildren();if(!rows.length){return}const width=720,height=170,left=10,right=10,top=14,bottom=20,max=Math.max(...rows.map(x=>x.count),1),step=(width-left-right)/Math.max(rows.length-1,1),points=rows.map((row,i)=>`${left+i*step},${height-bottom-(row.count/max)*(height-top-bottom)}`).join(' '),area=`${left},${height-bottom} ${points} ${left+(rows.length-1)*step},${height-bottom}`;svg.innerHTML=`<defs><linearGradient id="trendFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#3157d5" stop-opacity=".34"/><stop offset="100%" stop-color="#3157d5" stop-opacity="0"/></linearGradient></defs><line class="trend-grid" x1="${left}" y1="${top}" x2="${width-right}" y2="${top}"/><line class="trend-grid" x1="${left}" y1="${(height-top-bottom)/2+top}" x2="${width-right}" y2="${(height-top-bottom)/2+top}"/><line class="trend-grid" x1="${left}" y1="${height-bottom}" x2="${width-right}" y2="${height-bottom}"/><polygon class="trend-area" points="${area}"/><polyline class="trend-line" points="${points}"/>`;$('trendLabels').replaceChildren();add('span','',rows[0].key,$('trendLabels'));if(rows.length>2)add('span','',rows[Math.floor(rows.length/2)].key,$('trendLabels'));add('span','',rows[rows.length-1].key,$('trendLabels'))}
function renderFamilyTimeline(){const family=ANALYTICS.families.find(x=>x.id===selectedFamily),timeline=$('familyTimeline');timeline.replaceChildren();if(!family){$('familyDescription').textContent=t('family_desc_fallback');$('familyCount').textContent='';return}$('familyDescription').textContent=familyDesc(family);$('familyCount').textContent=t('family_count')(family.count.toLocaleString());for(const item of (ANALYTICS.familyTimeline[family.id]||[])){const card=add('div','timeline-item',undefined,timeline);card.style.borderLeftColor=family.color||'var(--accent)';add('div','timeline-date',item.date,card);const link=add('a','',item.title,card);link.href=item.url;link.target='_blank';link.rel='noopener';const axes=add('div','timeline-axes',undefined,card);for(const axis of item.changeAxes.slice(0,5))add('span','',axisName(axis),axes);if(item.predecessors.length){const relation=add('p','timeline-relation',t('timeline_precedent'),card);item.predecessors.forEach((pred,index)=>{const link=add(pred.url?'a':'span','',pred.title,relation);if(pred.url){link.href=pred.url;link.target='_blank';link.rel='noopener'}if(index<item.predecessors.length-1)add('span','',', ',relation)})}if(item.transferIdeas.length)add('p','timeline-idea',`${t('timeline_idea')}${item.transferIdeas[0]}`,card)}if(!timeline.children.length)add('div','no-timeline',t('no_family_papers'),timeline)}
function renderInsights(){drawBars('directionChart',ANALYTICS.directions,row=>dirName(row.id));drawTrend();drawBars('axisChart',ANALYTICS.axes.slice(0,8),row=>axisName(row.key));const options=$('familyOptions');options.replaceChildren();for(const family of ANALYTICS.families.filter(x=>x.count)){const button=add('button',family.id===selectedFamily?'active':'',`${familyName(family.id,family.title)} (${family.count})`,options);button.type='button';button.style.borderColor=family.color||'';button.onclick=()=>{selectedFamily=family.id;for(const child of options.children)child.classList.toggle('active',child===button);renderFamilyTimeline()}}renderFamilyTimeline()}
const featureCopy=()=>t('feat_desc_'+featureMode);
let featureMode='latest',featurePage=0,featurePaused=false,featureTimer,featurePerPage=window.innerWidth<=720?1:window.innerWidth<=1000?2:3;
function featureScore(p){const recent=Math.max(0,18-Math.floor((new Date(PAPERS[0].date)-new Date(p.date))/86400000));return (p.status==='curated'?8:Math.min(p.score,14))+(p.code?3:0)+(p.projectPage?2:0)+Math.min((p.sourceSignals||[]).length,3)*2+recent+(p.keyIdea?2:0)}
function featurePapers(){const reliable=PAPERS.filter(p=>p.confidence!=='broad');if(featureMode==='picks')return PAPERS.filter(p=>p.status==='curated').sort((a,b)=>(Number(Boolean(b.transferIdeas.length||b.changeAxes.length))-Number(Boolean(a.transferIdeas.length||a.changeAxes.length)))||b.date.localeCompare(a.date)).slice(0,30);if(featureMode==='signals')return reliable.slice().sort((a,b)=>featureScore(b)-featureScore(a)||b.date.localeCompare(a.date)).slice(0,30);return reliable.slice(0,30)}
function featureLink(parent,label,url){if(!url)return;const a=add('a','',`${label} ↗`,parent);a.href=url;a.target='_blank';a.rel='noopener'}
function renderFeatured(){const papers=featurePapers(),pages=Math.max(1,Math.ceil(papers.length/featurePerPage));featurePage=(featurePage+pages)%pages;$('featureDescription').textContent=featureCopy();$('featureGrid').replaceChildren();for(const p of papers.slice(featurePage*featurePerPage,featurePage*featurePerPage+featurePerPage)){const card=add('article',`feature-card ${p.status}`,undefined,$('featureGrid')),top=add('div','feature-top',undefined,card);add('span','',p.date,top);add('span','',dirName(p.direction),top);add('span','feature-status',p.status==='curated'?t('feat_pick'):`${t('feat_radar')} · ${t('confShort_'+p.confidence)}`,top);const h=add('h3','',undefined,card),a=add('a','',p.title,h);a.href=p.url;a.target='_blank';a.rel='noopener';add('p','feature-idea',p.keyIdea||t('feat_idea_fallback'),card);const tags=add('div','feature-tags',undefined,card);for(const tag of p.labels.slice(0,3))add('span','',labelName(tag),tags);const links=add('div','feature-links',undefined,card);featureLink(links,t('link_paper'),p.url);featureLink(links,t('link_project'),p.projectPage);featureLink(links,t('link_code'),p.code)}$('featurePage').textContent=t('feat_page')(papers.length.toLocaleString(),featurePage+1,pages);const progress=$('featureProgress');progress.replaceChildren();for(let i=0;i<pages;i++){const b=add('button',i===featurePage?'active':'','',progress);b.type='button';b.setAttribute('aria-label',t('feat_progress_aria')(i+1));b.onclick=()=>{featurePage=i;renderFeatured();restartFeatureTimer()}}}
function stepFeatured(delta){featurePage+=delta;renderFeatured()}
function restartFeatureTimer(){clearInterval(featureTimer);if(!featurePaused&&!matchMedia('(prefers-reduced-motion: reduce)').matches)featureTimer=setInterval(()=>stepFeatured(1),7000)}
for(const button of $('featureTabs').children)button.onclick=()=>{featureMode=button.dataset.mode;featurePage=0;for(const tab of $('featureTabs').children){const active=tab===button;tab.classList.toggle('active',active);tab.setAttribute('aria-selected',String(active))}renderFeatured();restartFeatureTimer()};
$('featurePrev').onclick=()=>{stepFeatured(-1);restartFeatureTimer()};$('featureNext').onclick=()=>{stepFeatured(1);restartFeatureTimer()};$('featurePause').onclick=()=>{featurePaused=!featurePaused;$('featurePause').textContent=featurePaused?'▶':'Ⅱ';$('featurePause').setAttribute('aria-label',t(featurePaused?'feat_resume':'feat_pause'));restartFeatureTimer()};$('featured').addEventListener('mouseenter',()=>clearInterval(featureTimer));$('featured').addEventListener('mouseleave',restartFeatureTimer);window.addEventListener('resize',()=>{const n=window.innerWidth<=720?1:window.innerWidth<=1000?2:3;if(n!==featurePerPage){featurePerPage=n;featurePage=0;renderFeatured()}});
$('clearLabels').onclick=()=>{selectedLabels.clear();for(const b of $('labelOptions').children)b.classList.remove('active');$('selectedCount').textContent=0;render()};
let visibleLimit=40;
function render(reset=true){if(reset)visibleLimit=40;const q=$('q').value.trim().toLowerCase(),d=$('direction').value,f=$('family').value,y=$('year').value,m=$('month').value,s=$('status').value,cf=$('confidence').value,lm=$('labelMode').value,chosen=[...selectedLabels];const confidenceOK=p=>cf==='all'||cf==='reliable'&&p.confidence!=='broad'||cf==='high'&&(p.confidence==='curated'||p.confidence==='high')||cf===p.confidence,labelOK=p=>!chosen.length||(lm==='all'?chosen.every(x=>p.labels.includes(x)):chosen.some(x=>p.labels.includes(x)));const list=PAPERS.filter(p=>(!d||p.direction===d)&&(!f||p.methodFamily===f)&&(!y||p.date.startsWith(y))&&(!m||p.date.slice(5,7)===m)&&(!s||p.status===s)&&confidenceOK(p)&&labelOK(p)&&(!q||[p.title,p.keyIdea,p.venue,p.methodFamilyTitle,...p.changeAxes,...p.transferIdeas,...p.tags,...p.labels.map(x=>labelName(x)),...p.authors,...p.institutions].join(' ').toLowerCase().includes(q))),shown=list.slice(0,visibleLimit);$('summary').textContent=t('summary')(shown.length.toLocaleString(),list.length.toLocaleString(),PAPERS.length.toLocaleString(),chosen.length?chosen.map(x=>labelName(x)).join(lm==='all'?' + ':' / '):'');$('papers').replaceChildren();$('loadMore').hidden=shown.length>=list.length;if(!list.length){add('div','empty',t('no_match'),$('papers'));return}for(const p of shown){const card=add('article','paper '+p.status,undefined,$('papers')),h=add('h2','',undefined,card),a=add('a','',p.title,h);a.href=p.url;a.target='_blank';a.rel='noopener';const meta=add('div','meta',undefined,card);add('span','pill status',p.status==='curated'?t('status_curated'):`🔎 ${t('confShort_'+p.confidence)}`,meta);add('span','',p.date,meta);add('span','pill',dirName(p.direction),meta);if(p.methodFamilyTitle)add('span','pill family',familyName(p.methodFamily,p.methodFamilyTitle),meta);for(const axis of p.changeAxes.slice(0,4))add('span','pill axis',axisName(axis),meta);for(const tag of p.labels.slice(0,8))add('span','pill label',labelName(tag),meta);if(p.code||p.projectPage||p.openAccessPdf||Object.keys(p.sourceLinks||{}).length){const links=add('span','links',undefined,meta),items=[];if(p.projectPage)items.push([t('link_project'),p.projectPage]);if(p.code)items.push([t('link_code'),p.code]);if(p.openAccessPdf)items.push([t('link_openpdf'),p.openAccessPdf]);for(const [source,url] of Object.entries(p.sourceLinks||{})){if(url)items.push([source.replace('_',' '),url])}items.forEach(([label,url],index)=>{if(index)add('span','',' · ',links);const link=add('a','',`${label} ↗`,links);link.href=url;link.target='_blank';link.rel='noopener'})}if(p.authors.length)add('p','people',`${t('authors_pre')}${p.authors.slice(0,8).join(', ')}${p.authors.length>8?t('et_al'):''}`,card);if(p.institutions.length)add('p','people',`${t('institutions_pre')}${p.institutions.slice(0,5).join('; ')}`,card);if(p.venue){const row=add('p','people',t('venue_pre'),card),v=add(p.venueUrl?'a':'span','',`${p.venue}${p.venueType?` (${p.venueType})`:''}`,row);if(p.venueUrl){v.href=p.venueUrl;v.target='_blank';v.rel='noopener'}}if(p.transferIdeas.length)add('p','evolution',`${t('transfer_pre')}${p.transferIdeas[0]}`,card);if(p.keyIdea)add('p','idea',p.keyIdea,card)}}
function renderDirectory(){const nav=$('directory');nav.replaceChildren();for(const d of DIRECTIONS){const b=add('button','',`${dirName(d.id)} (${PAPERS.filter(p=>p.direction===d.id).length})`,nav);b.onclick=()=>{$('direction').value=d.id;render();scrollTo({top:$('summary').offsetTop-20,behavior:'smooth'})}}for(const y of [...new Set(PAPERS.map(p=>p.date.slice(0,4)))].sort().reverse()){const b=add('button','',`${y} (${PAPERS.filter(p=>p.date.startsWith(y)).length})`,nav);b.onclick=()=>{$('year').value=y;render();scrollTo({top:$('summary').offsetTop-20,behavior:'smooth'})}}}
function renderLabelOptions(){const box=$('labelOptions');box.replaceChildren();for(const label of LABELS){const count=PAPERS.filter(p=>p.labels.includes(label.id)).length;if(!count)continue;const b=add('button',selectedLabels.has(label.id)?'active':'',`${labelName(label.id)} (${count})`,box);b.type='button';b.title=labelDesc(label.id)||label.description;b.onclick=()=>{selectedLabels.has(label.id)?selectedLabels.delete(label.id):selectedLabels.add(label.id);b.classList.toggle('active',selectedLabels.has(label.id));$('selectedCount').textContent=selectedLabels.size;render()}}}
function applyLang(){document.documentElement.lang=lang==='zh'?'zh-CN':'en';for(const el of document.querySelectorAll('[data-i18n]')){const v=t(el.dataset.i18n);if(typeof v==='string')el.textContent=v}for(const el of document.querySelectorAll('[data-i18n-ph]'))el.placeholder=t(el.dataset.i18nPh);for(const el of document.querySelectorAll('[data-i18n-aria]'))el.setAttribute('aria-label',t(el.dataset.i18nAria));$('featurePause').setAttribute('aria-label',t(featurePaused?'feat_resume':'feat_pause'));for(const b of document.querySelectorAll('.lang-toggle button'))b.classList.toggle('active',b.dataset.lang===lang);renderFilterOptions();if(PAPERS.length){renderDirectory();renderLabelOptions();renderInsights();renderFeatured();render(false)}}
function setLang(next){lang=next;localStorage.setItem('atlas-lang',next);applyLang()}
async function initialize(){try{const response=await fetch('data/papers.json');if(!response.ok)throw new Error(`HTTP ${response.status}`);PAPERS=await response.json();for(const y of [...new Set(PAPERS.map(p=>p.date.slice(0,4)))].sort().reverse()){const o=document.createElement('option');o.value=y;o.textContent=y;$('year').append(o)}renderDirectory();renderLabelOptions();$('total').textContent=PAPERS.length.toLocaleString();$('curated').textContent=PAPERS.filter(p=>p.status==='curated').length.toLocaleString();$('discovery').textContent=PAPERS.filter(p=>p.status==='discovery').length.toLocaleString();$('months').textContent=new Set(PAPERS.map(p=>p.date.slice(0,7))).size;for(const id of controls)$(id).addEventListener(id==='q'?'input':'change',render);$('loadMore').onclick=()=>{visibleLimit+=40;render(false)};renderInsights();renderFeatured();restartFeatureTimer();render()}catch(error){$('summary').textContent=t('load_error');console.error(error)}}
for(const b of document.querySelectorAll('.lang-toggle button'))b.onclick=()=>setLang(b.dataset.lang);
applyLang();
initialize();
</script></body></html>'''
    return template.replace("__DIRECTIONS__", direction_data).replace("__LABELS__", label_data).replace("__ANALYTICS__", analytics_data).replace("__GENERATED__", snapshot_date(papers)).replace("__SYNCED__", synced)


def update(check: bool = False) -> None:
    papers = payload()
    content = render(papers)
    data_content = json.dumps(papers, ensure_ascii=False, separators=(",", ":")) + "\n"
    if check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Static site is stale; run python -m radar.site")
        if not DATA_OUTPUT.exists() or DATA_OUTPUT.read_text(encoding="utf-8") != data_content:
            raise SystemExit("Static paper index is stale; run python -m radar.site")
        return
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8", newline="\n")
    DATA_OUTPUT.parent.mkdir(exist_ok=True)
    DATA_OUTPUT.write_text(data_content, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    update(args.check)


if __name__ == "__main__":
    main()
