"""AI 범죄 연구실 · 리포트·뉴스 검증 INDEX 만들기
사용: python scripts/build_reports_index.py  (reports/registry.json → reports/index.html)
"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = json.loads((ROOT / "reports" / "registry.json").read_text(encoding="utf-8"))
V = REG["verdicts"]
CH = [("ch00", "서장", "진화하는 사이버 범죄"), ("ch01", "1장", "AI 범죄, 새로운 디지털 위험의 시대"), ("ch02", "2장", "범죄자의 경제학"),
      ("ch03", "3장", "딥페이크의 위협"), ("ch04", "4장", "완벽한 사기꾼 — 피싱과 사회공학"), ("ch05", "5장", "끊임없는 진화 — 자동화 공격"),
      ("ch06", "6장", "보이지 않는 눈 — 감시와 프라이버시"), ("ch07", "7장", "보이지 않는 손의 조작 — 금융 범죄"),
      ("ch08", "8장", "나만의 디지털 방패"), ("ch09", "9장", "함께 만드는 안전한 AI 사회"), ("ch10", "10장", "미래를 준비하는 디지털 생존 전략")]
VCLS = {"same": "v-same", "new": "v-new", "upd": "v-upd", "diff": "v-diff", "book": "v-book"}
e = html.escape
reports = sorted(REG["reports"], key=lambda r: (r["date"], r["no"]), reverse=True)

# 장별 집계
agg = {c[0]: {k: 0 for k in V} for c in CH}
links = {c[0]: [] for c in CH}
for r in reports:
    for m in r["matches"]:
        for c in m["ch"]:
            agg[c][m["v"]] += 1
            links[c].append(f'<a href="{r["folder"]}/#{m["id"]}">R{r["no"]}·{m["id"]}</a>')

cards = "".join(
    f'<a class="card" href="{e(r["folder"])}/"><img class="thumb" src="{e(r["folder"])}/thumb.webp" alt="" width="600" height="400" loading="lazy">'
    f'<div class="cno">No.{e(r["no"])} · {e(r["date"])} · {e(r["kind"])}</div><div class="ct">{e(r["title"])}</div>'
    f'<div class="cs">{e(r["summary"])}</div><div class="cf">{e(r["source"])}</div>'
    f'<div class="vrow">' + " ".join(f'<span class="vf {VCLS[k]}">{e(V[k])} {sum(m["v"] == k for m in r["matches"])}</span>'
                                    for k in V if any(m["v"] == k for m in r["matches"])) + '</div></a>'
    for r in reports)

head = "<tr><th>장</th>" + "".join(f'<th><span class="vf {VCLS[k]}">{e(V[k])}</span></th>' for k in V) + "<th>대조 항목</th></tr>"
rows = "".join(
    f'<tr><td><a href="../{c}.html"><b>{e(n)}</b></a><br><small>{e(t)}</small></td>'
    + "".join(f'<td class="num">{agg[c][k] or "·"}</td>' for k in V)
    + f'<td><small>{" ".join(links[c]) or "아직 없음"}</small></td></tr>'
    for c, n, t in CH)
total = sum(len(r["matches"]) for r in reports)

page = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>리포트·뉴스 검증 INDEX · AI 범죄 연구실</title>
<meta name="description" content="새로 나온 보고서와 뉴스를 『AI 범죄와 자기 방어』의 장별 내용과 대조해, 책의 분석이 현장에서 어떻게 확인되는지 쌓아 가는 목록.">
<meta property="og:title" content="리포트·뉴스 검증 INDEX · AI 범죄 연구실"><meta property="og:image" content="https://adminmrobo.github.io/ai_crime_lab/{e(reports[0]['folder'])}/og.webp">
<link rel="stylesheet" href="../assets/lab.css">
<style>
main{{max-width:900px}}
.vf{{font-size:12px;font-weight:800;border-radius:999px;padding:1px 8px;white-space:nowrap;display:inline-block;margin:2px 0}}
.v-same{{background:#effaf4;color:#1f6b46;border:1px solid #bfe3cf}}.v-new{{background:#f3f1fd;color:#5b3fb0;border:1px solid #cfc3f3}}
.v-upd{{background:#fff8e6;color:#8a5a10;border:1px solid #ecd39c}}.v-diff{{background:#fff4f2;color:#a3322b;border:1px solid #f0c4bf}}
.v-book{{background:#eef3fb;color:#1f3a6b;border:1px solid #c7d5ee}}
.vrow{{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px}}
td.num{{text-align:center;font-weight:800}}
.rule{{background:var(--soft);border-radius:12px;padding:12px 18px;font-size:14.5px}}
.rule code{{font-size:13px}}
.memo{{display:flex;gap:14px;align-items:flex-start;background:#f7f9fc;border:1px solid #e3e8ee;border-radius:14px;padding:12px 16px;margin:22px 0}}
.memo img{{width:80px;height:80px;flex:none;border-radius:50%;image-rendering:pixelated;background:#fff;border:1px solid var(--line)}}
@media(max-width:700px){{.memo img{{width:56px;height:56px}}}}
</style></head><body>
<header class="top"><a class="brand" href="../index.html">AI 범죄 연구실</a><a href="../index.html#chapters">책 목차</a><a href="../ontology.html">온톨로지 지도</a><a href="../practice/index.html">실전 연습장</a><a href="../references.html">참고문헌</a></header>
<div class="wrap"><main>
<section class="hero" style="grid-template-columns:minmax(0,1fr)"><div>
<div class="no">AI 범죄 연구실 · 리포트·뉴스 검증</div>
<h1>책의 계산서는 현장에서 통할까</h1>
<p class="sub">새로 나온 보고서와 뉴스를 한 편씩 가져와 『AI 범죄와 자기 방어』의 장과 나란히 놓고 읽습니다</p>
<div class="meta">등록 {len(reports)}편 · 대조 항목 {total}개 · 마지막 갱신 {e(reports[0]['date'])}</div></div></section>

<div class="memo"><img src="../assets/chars/doctor/E13.webp" alt="박사 얼굴"><div><b style="font-size:13.5px;color:#1f3a6b">박사의 안내</b><p style="margin:0">각 리포트는 박사가 소식을 전하는 방식으로 사실을 정리하고, 끝에 책과의 대조표를 둡니다. 아래 장별 집계에서 숫자를 누르면 해당 대조 항목으로 바로 갑니다.</p></div></div>

<h2 id="list">리포트 목록 (최신순)</h2>
<div class="cards">{cards}</div>

<h2 id="coverage" style="margin-top:40px">장별 검증 현황</h2>
<p class="mute">한 대조 항목이 두 장에 걸치면 두 장 모두에 셉니다. 분야 전체에서 어디가 채워졌는지는 <a href="../ontology.html">AI 범죄학 온톨로지 지도</a>에서, 지식 노드가 쌓여 온 과정은 <a href="https://adminmrobo.github.io/ahnboat_lab_cover_status/growth_crime.html?view=full">AI 범죄학 지식 노드 현황</a>에서 봅니다.</p>
<table>{head}{rows}</table>

<h2 id="legend" style="margin-top:40px">대조 표시 읽는 법</h2>
<table><tr><th>표시</th><th>뜻</th></tr>
<tr><td><span class="vf v-same">같은 방향</span></td><td>책(모의 데이터 포함)과 보고서가 같은 구조를 설명한다. 숫자 크기까지 같다는 뜻은 아니다.</td></tr>
<tr><td><span class="vf v-new">책에 더할 내용</span></td><td>보고서에만 있는 사실·신호·사례</td></tr>
<tr><td><span class="vf v-upd">갱신 후보</span></td><td>책의 시점이나 표현이 보고서의 최신 집계와 다르다</td></tr>
<tr><td><span class="vf v-diff">처방이 다름</span></td><td>진단은 같고 대응 방법이 다르다</td></tr>
<tr><td><span class="vf v-book">책에만 있음</span></td><td>보고서가 다루지 않은 책의 내용</td></tr></table>

<h2 id="howto" style="margin-top:40px">새 리포트를 더하는 방법</h2>
<div class="rule"><ol>
<li>폴더를 <code>reports/YYYY-MM-DD_발행처-주제/</code>로 만든다(날짜는 연구실 검토일, 이름은 영문 소문자·하이픈).</li>
<li>페이지는 연구실 리포트(동향) 형식으로 쓰고, 마지막 장에 책 대조표(<code>id="m-번호"</code>)를 둔다.</li>
<li>지식 색인·꾸러미는 <code>kg/</code>에 JSON으로 두고 조립 도구로 붙인다.</li>
<li><code>reports/registry.json</code>에 한 줄을 더하고 <code>python scripts/build_reports_index.py</code>를 실행한다.</li>
<li>원본 PDF는 재배포 허락이 확인될 때만 올리고, 아니면 공식 링크만 적는다.</li></ol></div>

<footer class="foot">글 · 안상선 (<a href="https://adminmrobo.github.io/who_am_i/who_am_i.html">https://adminmrobo.github.io/who_am_i/who_am_i.html</a>) · (주)M-Robo 대표<br>『AI 범죄와 자기 방어』(커뮤니케이션북스, 2025)의 현장 검증 기록 · 각 리포트의 사실은 해당 페이지의 출처 목록을 따른다.</footer>
</main></div></body></html>"""
(ROOT / "reports" / "index.html").write_text(page, encoding="utf-8")
print("ok", len(reports), total)
