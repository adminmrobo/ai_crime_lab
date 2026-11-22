"""AI 범죄학 온톨로지 지도 만들기 — data/backbone_crime.json + scripts/crime_onto.py(책) + reports/*/kg/kg.json(리포트) → ontology.html
사용: python scripts/build_crime_map.py
뼈대 원본: github.com/adminmrobo/ahnboat_lab_explainer data/backbone_crime.json (작성자 초안 v0.1)
"""
import json, html, pathlib
import crime_onto as CO

ROOT = pathlib.Path(__file__).resolve().parent.parent
BB = json.loads((ROOT / "data" / "backbone_crime.json").read_text(encoding="utf-8"))
REG = json.loads((ROOT / "reports" / "registry.json").read_text(encoding="utf-8"))
CHNO = {"ch00": "서장", **{f"ch{i:02d}": f"{i}장" for i in range(1, 11)}}
e = html.escape

areas = [n for n in BB["nodes"] if n["type"] == "Area"]
topics = {n["id"].split("/", 1)[1]: n for n in BB["nodes"] if n["type"] == "Topic"}
t_area = {s.split("/", 1)[1]: o for s, p, o in ((x["s"], x["p"], x["o"]) for x in BB["edges"]) if p == "lab:broader"}

book = {t: [] for t in topics}      # 주제 → [(장, 개념 ko, url)]
report = {t: [] for t in topics}    # 주제 → [(No, 개념 ko, url)]
concepts = []                       # 지도 점
seen = {}
for ch, i, t, ko, en, d, anc, tops, var in CO.C + [(s,) + CO.INST for s in CO.FIRST]:
    url = f"{ch}.html{anc}"
    for tp in tops:
        book[tp].append((CHNO[ch], ko, url))
    if i in seen:
        seen[i]["src"].add("book"); seen[i]["pages"].append([CHNO[ch], url]); continue
    seen[i] = {"id": i, "ko": ko, "def": d, "topics": list(tops), "src": {"book"}, "pages": [[CHNO[ch], url]], "var": var}
for r in REG["reports"]:
    kgp = ROOT / "reports" / r["folder"] / "kg" / "kg.json"
    if not kgp.exists():
        continue
    kg = json.loads(kgp.read_text(encoding="utf-8"))
    for n in kg["nodes"]:
        tops = CO.REPORT_MAP.get(n["id"])
        if not tops:
            continue
        url = f'reports/{r["folder"]}/{n["anchor"]}'
        ko = n["label"]["ko"]
        for tp in tops:
            report[tp].append((f'R{r["no"]}', ko, url))
        if n["id"] in seen:
            seen[n["id"]]["src"].add("report"); seen[n["id"]]["pages"].append([f'R{r["no"]}', url])
            for tp in tops:
                if tp not in seen[n["id"]]["topics"]:
                    seen[n["id"]]["topics"].append(tp)
        else:
            d = (n.get("definition") or {}).get("ko", "")
            seen[n["id"]] = {"id": n["id"], "ko": ko, "def": d, "topics": list(tops), "src": {"report"}, "pages": [[f'R{r["no"]}', url]], "var": ""}
for c in seen.values():
    c["src"] = sorted(c["src"])
    concepts.append(c)


def status(t):
    b, r = bool(book[t]), bool(report[t])
    return "both" if b and r else "book" if b else "report" if r else "empty"


ST = {"both": ("책 + 현장 확인", "#1f8a5b"), "book": ("책에서 다룸", "#3d63c9"), "report": ("리포트에서만", "#7a5bd1"), "empty": ("아직 공란", "#b8c0ca")}
cnt = {k: sum(status(t) == k for t in topics) for k in ST}
DATA = {
    "areas": [{"id": a["id"], "ko": a["label"]["ko"], "lv": a["level"]} for a in areas],
    "topics": [{"id": "lab:topic/" + t, "ko": n["label"]["ko"], "area": t_area[t], "st": status(t),
                "book": book[t], "report": report[t]} for t, n in topics.items()],
    "concepts": concepts,
    "pre": [[x["s"], x["o"]] for x in BB["edges"] if x["p"] == "lab:prerequisiteOf"],
    "status": {k: {"label": v[0], "color": v[1], "n": cnt[k]} for k, v in ST.items()},
}

rows = []
for a in areas:
    ts = [t for t in topics if t_area[t] == a["id"]]
    chips = []
    for t in ts:
        s = status(t)
        def first(lst):
            out = {}
            for no, ko, u in lst:
                out.setdefault(no, (ko, u))
            return sorted(out.items(), key=lambda x: (len(x[0]), x[0]))
        src = " ".join(f'<a href="{e(u)}" title="{e(ko)}">{e(no)}</a>' for no, (ko, u) in first(book[t])[:6])
        src += (" " if src and report[t] else "") + " ".join(f'<a class="rp" href="{e(u)}" title="{e(ko)}">{e(no)}</a>' for no, (ko, u) in first(report[t]))
        chips.append(f'<div class="tp st-{s}"><b>{e(topics[t]["label"]["ko"])}</b><span class="sl">{e(ST[s][0])}</span><span class="src">{src or "—"}</span></div>')
    rows.append(f'<section class="area" id="a-{e(a["family"])}"><h3>{e(a["label"]["ko"])} <small>level {a["level"]}</small></h3><div class="tps">{"".join(chips)}</div></section>')

empties = [topics[t]["label"]["ko"] for t in topics if status(t) == "empty"]
bookonly = [topics[t]["label"]["ko"] for t in topics if status(t) == "book"]

page = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 범죄학 온톨로지 지도 · AI 범죄 연구실</title>
<meta name="description" content="『AI 범죄와 자기 방어』의 분석 틀로 만든 AI 범죄학 뼈대(13개 영역·49개 주제)에 책 11개 장과 리포트 검증의 개념을 건 지도. 책이 다룬 곳, 현장 보고서로 확인된 곳, 아직 공란인 곳을 보여 준다.">
<meta property="og:title" content="AI 범죄학 온톨로지 지도 · AI 범죄 연구실"><meta property="og:image" content="https://adminmrobo.github.io/ai_crime_lab/assets/og/index.webp">
<link rel="stylesheet" href="assets/lab.css">
<style>
main{{max-width:1040px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;margin:16px 0}}
.tile{{border:1px solid var(--line);border-radius:12px;padding:10px 14px}}.tile b{{display:block;font-size:26px;line-height:1.2}}.tile span{{font-size:13px;color:var(--sub)}}
#g{{height:560px;border:1px solid var(--line);border-radius:14px;background:#f7f9fc;position:relative;overflow:hidden}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}}
.chips button{{font:inherit;font-size:14px;min-height:36px;padding:4px 12px;border-radius:999px;border:1px solid #c8d0da;background:#fff;cursor:pointer}}
.chips button[aria-pressed=true]{{background:var(--ink);color:#fff;border-color:var(--ink)}}
.legend{{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:13.5px;color:var(--sub);margin:8px 0}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:5px;vertical-align:-1px}}
.legend i.hollow{{background:#fff!important;border:2px solid #b8c0ca}}
#info{{border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:12px 0;min-height:64px;font-size:15px}}
.area{{margin:18px 0}}.area h3{{margin:0 0 8px;font-size:17px}}.area small{{color:var(--mute);font-weight:400;font-size:12px}}
.tps{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}}
.tp{{border-radius:10px;padding:8px 12px;font-size:14px;line-height:1.5;border:1.5px solid}}
.tp .sl{{display:block;font-size:12px;font-weight:700}}.tp .src{{display:block;font-size:12.5px}}.tp .src a{{margin-right:6px}}.tp .src a.rp{{color:#5b3fb0;font-weight:700}}
.st-both{{border-color:#1f8a5b;background:#effaf4}}.st-both .sl{{color:#1f6b46}}
.st-book{{border-color:#3d63c9;background:#f3f6fd}}.st-book .sl{{color:#2f4fa8}}
.st-report{{border-color:#7a5bd1;background:#f3f1fd}}.st-report .sl{{color:#5b3fb0}}
.st-empty{{border-color:#b8c0ca;border-style:dashed;background:#fff}}.st-empty .sl{{color:var(--mute)}}
.memo{{display:flex;gap:14px;align-items:flex-start;background:#f7f9fc;border:1px solid #e3e8ee;border-radius:14px;padding:12px 16px;margin:22px 0}}
.memo img{{width:80px;height:80px;flex:none;border-radius:50%;image-rendering:pixelated;background:#fff;border:1px solid var(--line)}}
@media(max-width:700px){{#g{{height:420px}}.memo img{{width:56px;height:56px}}}}
</style></head><body>
<header class="top"><a class="brand" href="index.html">AI 범죄 연구실</a><a href="index.html#chapters">책 목차</a><a href="reports/index.html">리포트 검증</a><a href="practice/index.html">실전 연습장</a><a href="references.html">참고문헌</a></header>
<div class="wrap"><main>
<section class="hero" style="grid-template-columns:minmax(0,1fr)"><div>
<div class="no">AI 범죄 연구실 · 분야 온톨로지</div>
<h1>AI 범죄학 온톨로지 지도</h1>
<p class="sub">책의 분석 틀로 짠 뼈대 위에, 책이 다룬 개념과 현장 보고서로 확인된 개념을 겹쳐 봅니다</p>
<div class="meta">뼈대: AI 범죄학(crime) v0.1 — 작성자 초안이며 공식 분류 체계가 아닙니다 · 영역 {len(areas)} · 주제 {len(topics)} · 개념 {len(concepts)}</div></div></section>

<div class="memo"><img src="assets/chars/doctor/E07.webp" alt="박사 얼굴"><div><b style="font-size:13.5px;color:#1f3a6b">박사의 안내</b><p style="margin:0">큰 점은 영역, 중간 점은 주제, 작은 점은 책과 리포트에 나온 개념입니다. 주제의 색은 그 주제가 책에서 다뤄졌는지, 새 보고서로 현장에서 확인됐는지를 나타냅니다. 점을 누르면 아래에 설명과 바로가기가 나옵니다.</p></div></div>

<div class="tiles">
<div class="tile"><b>{cnt['both']}</b><span>책 + 현장 확인</span></div>
<div class="tile"><b>{cnt['book']}</b><span>책에서 다룸</span></div>
<div class="tile"><b>{cnt['report']}</b><span>리포트에서만</span></div>
<div class="tile"><b>{cnt['empty']}</b><span>아직 공란</span></div>
<div class="tile"><b>{len(REG['reports'])}</b><span>검증한 리포트</span></div>
</div>

<h2 id="map">3D 지도</h2>
<div class="chips" id="modes" role="group" aria-label="보기 선택"></div>
<div class="legend"><span><i style="background:#1d2430"></i>영역</span><span><i style="background:#1f8a5b"></i>책 + 현장 확인</span><span><i style="background:#3d63c9"></i>책에서 다룸</span><span><i style="background:#7a5bd1"></i>리포트에서만</span><span><i class="hollow"></i>아직 공란</span><span><i style="background:#9db3e8"></i>개념(책)</span><span><i style="background:#c3b4ee"></i>개념(리포트)</span></div>
<div id="g"></div>
<div id="info" aria-live="polite">점을 눌러 보세요. 끌어서 돌리고, 굴려서 확대합니다.</div>

<h2 id="coverage" style="margin-top:36px">영역별 커버리지</h2>
<p class="mute">주제 아래 링크는 그 주제를 다룬 장(파란 글씨)과 리포트(보라 굵은 글씨)입니다. 3D 지도가 보이지 않는 환경에서도 이 표로 같은 내용을 볼 수 있습니다.</p>
{"".join(rows)}

<h2 id="next" style="margin-top:36px">다음 리포트로 채울 곳</h2>
<p><b>아직 공란인 주제 ({len(empties)})</b>: {e(", ".join(empties)) or "없음"}</p>
<p><b>책에서만 다룬 주제 ({len(bookonly)})</b> — 현장 보고서로 확인할 후보: {e(", ".join(bookonly))}</p>

<h2 id="about" style="margin-top:36px">이 지도에 대해</h2>
<ul>
<li>뼈대는 『AI 범죄와 자기 방어』(안상선, 2025)의 분석 틀(범죄경제학·게임이론·AI 분석)과 장 구성을 바탕으로 만든 작성자 초안 v0.1입니다. 원본은 <a href="https://github.com/adminmrobo/ahnboat_lab_explainer/blob/main/data/backbone_crime.json">ahnboat_lab_explainer의 backbone_crime.json</a>, 분야 규칙은 같은 저장소의 <code>packs/domain/DOMAIN_crime.md</code>입니다.</li>
<li>책 개념은 각 장 페이지의 지식 색인 데이터(<code>kg-raw</code>)와 같습니다. 리포트 개념은 <a href="reports/index.html">리포트·뉴스 검증</a> 페이지의 지식 색인에서 가져와 뼈대 주제에 대응시켰습니다.</li>
<li>'현장 확인'은 업계·기관 보고서에 같은 주제의 사실이 나왔다는 뜻이며, 책의 모의 수치가 그대로 맞았다는 뜻은 아닙니다. 항목별 관계는 각 리포트의 대조표에서 확인하세요.</li>
<li>지식 노드가 쌓여 온 과정은 <a href="https://adminmrobo.github.io/ahnboat_lab_cover_status/growth_crime.html?view=full">AI 범죄학 지식 노드 현황</a>(ahnboat.xyz)에서 날짜 순서로 볼 수 있습니다. 그 데이터는 이 저장소의 <code>data/crime_kg.json</code>입니다.</li>
<li>다시 만들기: <code>python scripts/build_crime_map.py</code> (새 리포트를 등록한 뒤)</li>
</ul>
<footer class="foot">글 · 안상선 (<a href="https://adminmrobo.github.io/who_am_i/who_am_i.html">https://adminmrobo.github.io/who_am_i/who_am_i.html</a>) · (주)M-Robo 대표<br>AI 범죄학 뼈대 v0.1(작성자 초안) · 『AI 범죄와 자기 방어』(커뮤니케이션북스, 2025) 보충 자료</footer>
</main></div>
<script type="application/json" id="crime-map">{json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")}</script>
<script src="assets/vendor/3d-force-graph.min.js"></script>
<script>
(function(){{
var D=JSON.parse(document.getElementById('crime-map').textContent);
var TOP={{}};D.topics.forEach(function(t){{TOP[t.id]=t;}});
var mode='all',G=null,sel=null,fitted=false;
function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
function data(){{
  var nodes=[],links=[],have={{}};
  function add(n){{if(!have[n.id]){{have[n.id]=n;nodes.push(n);}}}}
  D.areas.forEach(function(a){{add({{id:a.id,k:'area',ko:a.ko,lv:a.lv}});}});
  D.topics.forEach(function(t){{
    if(mode==='empty'&&t.st!=='empty')return;
    if(mode==='report'&&!(t.st==='both'||t.st==='report'))return;
    if(mode==='book'&&!(t.st==='both'||t.st==='book'))return;
    add({{id:t.id,k:'topic',ko:t.ko,st:t.st,ref:t}});links.push({{source:t.area,target:t.id,k:'at'}});
  }});
  if(mode!=='empty')D.concepts.forEach(function(c){{
    if(mode==='report'&&c.src.indexOf('report')<0)return;
    if(mode==='book'&&c.src.indexOf('book')<0)return;
    var ts=c.topics.map(function(t){{return 'lab:topic/'+t;}}).filter(function(t){{return have[t];}});
    if(!ts.length)return;
    add({{id:'c:'+c.id,k:'c',ko:c.ko,ref:c}});ts.forEach(function(t){{links.push({{source:t,target:'c:'+c.id,k:'tc'}});}});
  }});
  D.pre.forEach(function(p){{links.push({{source:p[0],target:p[1],k:'pre'}});}});
  return {{nodes:nodes,links:links}};
}}
function col(n){{
  if(sel&&sel!==n.id&&!(n.k==='c'&&sel.indexOf('lab:topic/')===0&&n.ref.topics.indexOf(sel.slice(10))>=0))return n.k==='area'?'#9aa3ad':'#dfe4ea';
  if(n.k==='area')return '#1d2430';
  if(n.k==='topic')return D.status[n.st].color;
  return n.ref.src.indexOf('report')>=0&&n.ref.src.indexOf('book')<0?'#c3b4ee':'#9db3e8';
}}
function val(n){{return n.k==='area'?22:n.k==='topic'?6:2;}}
function show(n){{
  var b=document.getElementById('info'),h='';
  if(n.k==='area'){{h='<b>영역 · '+esc(n.ko)+'</b> <span class="mute">level '+n.lv+'</span><br>'+D.topics.filter(function(t){{return t.area===n.id;}}).map(function(t){{return esc(t.ko)+' ('+esc(D.status[t.st].label)+')';}}).join(' · ');}}
  else if(n.k==='topic'){{var t=n.ref;h='<b>주제 · '+esc(t.ko)+'</b> — '+esc(D.status[t.st].label)+'<br>';
    h+=t.book.map(function(x){{return '<a href="'+esc(x[2])+'">'+esc(x[0])+' · '+esc(x[1])+'</a>';}}).join(' · ');
    if(t.report.length)h+=(t.book.length?'<br>':'')+t.report.map(function(x){{return '<a href="'+esc(x[2])+'" style="color:#5b3fb0;font-weight:700">'+esc(x[0])+' · '+esc(x[1])+'</a>';}}).join(' · ');
    if(!t.book.length&&!t.report.length)h+='아직 다룬 페이지가 없습니다.';}}
  else{{var c=n.ref;h='<b>개념 · '+esc(c.ko)+'</b>'+(c.def?' — '+esc(c.def):'')+'<br>'+c.pages.map(function(p){{return '<a href="'+esc(p[1])+'">'+esc(p[0])+'에서 보기</a>';}}).join(' · ');}}
  b.innerHTML=h;
}}
function chips(){{
  var m=document.getElementById('modes');m.innerHTML='';
  [['all','전체'],['book','책이 다룬 것'],['report','리포트로 확인된 것'],['empty','공란만']].forEach(function(x){{
    var b=document.createElement('button');b.type='button';b.textContent=x[1];b.setAttribute('aria-pressed',String(mode===x[0]));
    b.addEventListener('click',function(){{mode=x[0];sel=null;fitted=false;chips();draw();}});m.appendChild(b);}});
}}
function draw(){{
  var el=document.getElementById('g');
  if(typeof ForceGraph3D!=='function'){{el.innerHTML='<p style="padding:20px">이 브라우저에서는 3D 지도를 그릴 수 없습니다. 아래 영역별 커버리지 표를 이용해 주세요.</p>';return;}}
  try{{
  if(!G){{G=ForceGraph3D({{controlType:'orbit'}})(el).backgroundColor('#f7f9fc').width(el.clientWidth).height(el.clientHeight)
    .nodeLabel(function(n){{return '<div style="background:#fff;color:#1d2430;border:1px solid #c8d0da;border-radius:6px;padding:3px 8px;font-size:13px">'+esc(n.ko)+'</div>';}})
    .nodeVal(val).nodeColor(col).nodeOpacity(0.95).linkOpacity(0.35)
    .linkColor(function(l){{return l.k==='pre'?'#d6453d':l.k==='at'?'#7a8492':'#c8d0da';}})
    .linkWidth(function(l){{return l.k==='pre'?1.2:0;}}).linkDirectionalArrowLength(function(l){{return l.k==='pre'?4:0;}}).linkDirectionalArrowRelPos(1)
    .onNodeClick(function(n){{sel=n.id;show(n);G.nodeColor(col);}}).cooldownTicks(120).onEngineStop(function(){{if(!fitted){{fitted=true;G.zoomToFit(400,30);}}}});
    window.addEventListener('resize',function(){{G.width(el.clientWidth).height(el.clientHeight);}});}}
  G.graphData(data());
  }}catch(err){{el.innerHTML='<p style="padding:20px">3D 지도를 그리지 못했습니다(WebGL). 아래 영역별 커버리지 표를 이용해 주세요.</p>';G=null;}}
}}
chips();draw();
}})();
</script></body></html>"""
(ROOT / "ontology.html").write_text(page, encoding="utf-8")

# ── 지식 노드 현황(ahnboat.xyz growth_crime)용 내보내기: data/crime_kg.json ──
import re as _re
def _title(slug):
    t = (ROOT / "content" / f"{slug}.md").read_text(encoding="utf-8").split("\n---")[0]
    return dict(_re.findall(r"^(\w+):\s*(.+)$", t, _re.M)).get("title", slug)
xpages = [{"file": f"{s}.html", "title": f"{CHNO[s]} · {_title(s)}"} for s in CHNO]
xnodes, xedges = {}, []
area_of = {t: t_area[t] for t in topics}
for ch, i, t, ko, en, d, anc, tops, var in CO.C + [(s,) + CO.INST for s in CO.FIRST]:
    n = xnodes.setdefault(i, {"id": i, "ko": ko, "en": en, "area": area_of[tops[0]], "files": []})
    if f"{ch}.html" not in n["files"]:
        n["files"].append(f"{ch}.html")
for s_, p_, o_ in CO.REL:
    xedges.append([s_, o_, p_])
for s in CO.FIRST:
    xedges.append([CO.INST[0], CO.FIRST[s], "relatedTo"])
for r in REG["reports"]:
    kgp = ROOT / "reports" / r["folder"] / "kg" / "kg.json"
    if not kgp.exists():
        continue
    f = f'reports/{r["folder"]}/index.html'
    xpages.append({"file": f, "title": f'리포트 No.{r["no"]} · {r["title"]}'})
    kg = json.loads(kgp.read_text(encoding="utf-8"))
    for nd in kg["nodes"]:
        tops = CO.REPORT_MAP.get(nd["id"])
        if not tops or nd["type"] == "Claim":
            continue
        n = xnodes.setdefault(nd["id"], {"id": nd["id"], "ko": nd["label"]["ko"], "en": nd["label"]["en"], "area": area_of[tops[0]], "files": []})
        if f not in n["files"]:
            n["files"].append(f)
    for ed in kg["edges"]:
        if ed["s"] in xnodes and ed["o"] in xnodes and ed["p"] != "lab:broader":
            xedges.append([ed["s"], ed["o"], ed["p"].replace("lab:", "")])
xedges = [e_ for e_ in xedges if e_[0] in xnodes and e_[1] in xnodes]
export = {"version": "1.0", "domain": "crime", "repo": "ai_crime_lab", "backbone": "backbone_crime " + BB["version"],
          "site": "https://adminmrobo.github.io/ai_crime_lab/", "map": "https://adminmrobo.github.io/ai_crime_lab/ontology.html",
          "areas": [{"id": a["id"], "ko": a["label"]["ko"], "en": a["label"]["en"]} for a in areas],
          "pages": xpages, "nodes": list(xnodes.values()), "edges": xedges}
(ROOT / "data" / "crime_kg.json").write_text(json.dumps(export, ensure_ascii=False, indent=1), encoding="utf-8")
print("crime_kg.json nodes", len(xnodes), "edges", len(xedges), "pages", len(xpages))
print("ok topics", len(topics), cnt, "concepts", len(concepts))
