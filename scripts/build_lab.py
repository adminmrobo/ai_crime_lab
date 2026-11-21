# -*- coding: utf-8 -*-
"""content/*.md + scripts/lab_data.py → 루트 *.html (GitHub Pages)."""
import os, re, glob, html, json
import markdown
from lab_data import CH, TOOLS

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_URL = "https://adminmrobo.github.io/ai_crime_lab/"
AUTHOR_URL = "https://adminmrobo.github.io/who_am_i/who_am_i.html"
BOOK = ("『AI 범죄와 자기 방어』 — AI가 범죄에 쓰이는 실제 사례를 모으고, 범죄자가 왜 AI를 고르는지를 범죄경제학의 눈으로 묻는 책. "
        "범죄자도 비용과 이익을 따진다는 관점에서, AI가 범죄의 비용 구조와 수익 모델을 어떻게 바꾸었는지 풀어낸다. 이 사이트는 그 책을 사례와 함께 풀어 쓴 보충본이다.")

CAST = {  # 이름: (표시, 역할, 폴더, 기본 표정)
    "박사": ("박사", "해설자", "doctor", "E07"),
    "하루": ("조수(하루)", "추적 팀 · 대응 설계", "haru", "E10"),
    "시아": ("인턴1 시아", "추적 팀 · 현장 사례", "sia", "E09"),
    "모아": ("인턴2 모아", "추적 팀 · 제도·법", "moa", "E07"),
    "주판봇": ("주판봇", "계산 담당", "jupanbot", "E16"),
    "초파리": ("초파리 연구원", "데이터·모델 분석", "fruitfly", "E09"),
    "X1": ("X1", "범죄자 대역 · 사기·사칭", "x1", "E13"),
    "X2": ("X2", "범죄자 대역 · 자동화 공격·랜섬", "x2", "E13"),
    "X3": ("X3", "범죄자 대역 · 세탁·정보 브로커", "x3", "E13"),
}
XOK = {"E01", "E02", "E03", "E04", "E09", "E13", "E15", "E16", "E24"}
BOX = {
    "econ": ("범죄자의 계산서", "#fff4f2", "#d6453d"), "flip": ("계산서 뒤집기 — 대응", "#effaf4", "#1f8a5b"),
    "data": ("주판봇·초파리 분석실", "#f3f1fd", "#7a5bd1"), "case": ("사례 분석", "#f4f7fd", "#3d63c9"),
    "key": ("핵심 정리", "#fffaf0", "#c98318"), "note": ("박사 노트", "#f6f8fb", "#1f3a6b"),
    "warn": ("주의", "#fff8e6", "#b7791f"),
}
md = markdown.Markdown(extensions=["tables", "sane_lists"])
PROMPTS = []


def mdc(t):
    md.reset()
    return md.convert(t)


def img(who, expr=None, pre=""):
    name, role, d, e = CAST[who]
    e = expr or e
    if who.startswith("X") and e not in XOK:
        e = "E13"
    return f'<img src="{pre}assets/chars/{d}/{e}.webp" alt="{name}" loading="lazy" width="58" height="58">'


def bubble(who, text, expr=None, pre=""):
    name, role, *_ = CAST[who]
    x = who.startswith("X")
    body = mdc(text).removeprefix("<p>").removesuffix("</p>")
    return (f'<div class="say {"right x" if x else "left"}">{img(who, expr, pre)}<div class="bub"><div class="who">{name}<span>{role}</span></div>'
            f'<div class="txt">{body}</div></div></div>')


def chart(name, cap):
    svg = open(os.path.join(ROOT, "assets", "charts", name + ".svg"), encoding="utf-8").read()
    return f'<figure class="chart">{svg}<figcaption>{html.escape(cap)}</figcaption></figure>'


def convert(body, slug="", pre=""):
    out, buf = [], []
    lines = body.split("\n")
    i = 0
    def flush():
        if buf:
            out.append(mdc("\n".join(buf))); buf.clear()
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^@(\S+?)(?:\((E\d\d)\))?:\s*(.*)$", ln)
        if m and m.group(1) in CAST:
            flush(); out.append(bubble(m.group(1), m.group(3), m.group(2), pre)); i += 1; continue
        m = re.match(r"^!chart\s+(\S+)\s*\|\s*(.*)$", ln)
        if m:
            flush(); out.append(chart(m.group(1), m.group(2))); i += 1; continue
        m = re.match(r"^:::(\w+)\s*(.*)$", ln)
        if m:
            flush()
            kind, title = m.group(1), m.group(2).strip()
            j = i + 1; inner = []
            while j < len(lines) and lines[j].strip() != ":::":
                inner.append(lines[j]); j += 1
            if kind == "prompt":
                PROMPTS.append((slug, title, "\n".join(inner).strip()))
            else:
                lab, bg, bd = BOX[kind]
                out.append(f'<aside class="box {kind}" style="background:{bg};border-color:{bd}"><div class="bt" style="color:{bd}">{lab}'
                           f'{" · " + html.escape(title) if title else ""}</div>{convert(chr(10).join(inner), slug, pre)}</aside>')
            i = j + 1; continue
        buf.append(ln); i += 1
    flush()
    return "\n".join(out)


def parse(path):
    raw = open(path, encoding="utf-8").read()
    head, body = raw.split("\n---\n", 1)
    meta = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in head.strip().split("\n"))}
    return meta, body


def quiz(q, opts, a, ex):
    bs = "".join(f"<button type=\"button\">{chr(9312 + k)} {html.escape(o)}</button>" for k, o in enumerate(opts))
    return f'<div class="quiz" data-a="{a}"><div class="q">확인 퀴즈 · {html.escape(q)}</div>{bs}<div class="ex" hidden><b></b>{html.escape(ex)}</div></div>'


def head(title, desc, pre="", jsonld=None, path=""):
    og = SITE_URL + "assets/lineup.webp"
    jl = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · AI 범죄 연구실</title><meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)} · AI 범죄 연구실"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{og}"><meta property="og:url" content="{SITE_URL}{path}"><meta property="og:type" content="article">
<link rel="stylesheet" href="{pre}assets/lab.css">{jl}</head><body>
<header class="top"><a class="brand" href="{pre}index.html">AI 범죄 연구실 — 범죄자의 계산서를 뒤집어라</a>
<a href="{pre}index.html#chapters">목차</a><a href="{pre}practice/index.html">실전 연습장</a><a href="{pre}workbook.html">통합 작업본</a><a href="{pre}references.html">참고문헌</a><a href="{pre}data.html">모의 데이터</a></header>"""


def foot(pre=""):
    return (f'<footer class="foot">글 · 안상선 (<a href="{AUTHOR_URL}">{AUTHOR_URL}</a>) · (주)M-Robo 대표<br>'
            f"이 사이트는 『AI 범죄와 자기 방어』의 사례 보충본이다. '모의 데이터(가상)'는 설명용 가상의 수치이며 실제 통계가 아니다. "
            f"X1~X3는 범죄자 역할을 맡은 대역이다. 범죄 수법은 작동 원리까지만 다룬다. · "
            f'<a href="{pre}references.html">참고문헌</a> · <a href="{pre}data.html">모의 데이터와 재현 코드</a> · <a href="{pre}workbook.html">통합 작업본</a></footer>')


def tool_step(slug, d, n):
    t = d["tool"]; w = t["why"]; m = t["math"]
    parts = "".join(f"<tr><td><b>{html.escape(a)}</b></td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>" for a, b, c in m["parts"])
    esc = lambda x: x.replace("*", "\\*")
    talk = "".join(bubble(who, esc(txt), ex) for who, ex, txt in t["talk"])
    code = t.get("code")
    codebox = (f'<details><summary>교안의 파이썬 코드로 보면 (몰라도 됩니다)</summary><p><code>{html.escape(code[0])}</code><br>{html.escape(code[1])}</p></details>' if code else "")
    q = t["quiz"]
    return f"""<section class="step" id="tool"><div class="lab">단계 {n} · 분석 도구 — {TOOLS[t['kind']]}</div><h2>{html.escape(t['title'])}</h2><span class="tag">{html.escape(t['tag'])}</span>
{bubble('박사', '현장 질문부터 해 볼게요. ' + esc(w['problem']))}
<div class="duo"><div class="whybox"><h4>왜 이 방법을 쓰나</h4><dl><dt>문제 상황</dt><dd>{html.escape(w['problem'])}</dd><dt>앞 방법의 한계</dt><dd>{html.escape(w['limit'])}</dd><dt>해법</dt><dd>{html.escape(w['solution'])}</dd><dt>쉽게 말하면</dt><dd>{html.escape(w['easy'])}</dd></dl></div>
<div class="mathbox"><h4>수식을 어려워하는 조수가 대신 물어봅니다</h4><div class="mini">{img('하루','E04')}<div><b>하루</b> {html.escape(m['q'])}</div></div>
<dl><dt>학교 수학으로 보면</dt><dd>{html.escape(m['school'])}</dd></dl><table class="parts"><tr><th>식 조각</th><th>읽는 법</th><th>뜻</th></tr>{parts}</table>
<dl><dt>숫자로 한 번 해 보기</dt><dd>{html.escape(m['tr'])}</dd></dl><div class="mini">{img('하루','E01')}<div><b>하루</b> {html.escape(m['comment'])}</div></div></div></div>
<div class="pair"><div><b>일상으로 치면</b>{html.escape(t['daily'])}</div><div><b>현장에서는</b>{html.escape(t['field'])}</div></div>
<h3>AI 판단 코너 — 주판봇의 확신, 맞을까?</h3>{talk}
<div class="panel"><h4>실험: 직접 바꿔 보기</h4><div data-w="w-{slug}" data-k="{t['widget']}"></div></div>
{bubble('박사', '풀이: ' + esc(t['solve']), 'E10')}
<aside class="box warn" style="background:#fff8e6;border-color:#b7791f"><div class="bt" style="color:#b7791f">이 단계의 한계 — 여기서는 단순하게 봤어요</div><p>{html.escape(t['limit'])}</p></aside>
{codebox}{quiz(*q)}</section>"""


def chapter_page(slug, meta, body, idx, chapters):
    d = CH[slug]
    # 단계로 나누기
    secs = re.split(r"\n(?=## )", "\n" + body)
    intro, steps = secs[0], secs[1:]
    html_steps = []
    for k, s in enumerate(steps, 1):
        title, rest = s.strip().split("\n", 1)
        title = title[3:].strip()
        t_clean = re.sub(r"^\d+\.\s*", "", title)
        html_steps.append(f'<section class="step" id="s{k}"><div class="lab">단계 {k}</div><h2>{html.escape(t_clean)}</h2>{convert(rest, slug)}</section>')
    n_tool = len(steps) + 1
    toc = (f"<b>{html.escape(meta['no'])}</b><a href='#three'>처음 오신 분께</a><a href='#why'>왜 · 큰 그림</a>"
           + "".join(f'<a href="#s{k}">단계 {k}</a>' for k in range(1, len(steps) + 1))
           + f"<a href='#tool'>단계 {n_tool} · 분석 도구</a><a href='#duel'>대결</a><a href='#wrap'>정리 퀴즈</a><a href='#outro'>아웃트로</a><a href='#kg'>지식 색인</a><a href='#export'>꾸러미</a>")
    abbr = "".join(f"<li><b>{html.escape(a)}</b> — {html.escape(b)}</li>" for a, b in d["abbr"])
    three = (f'<section class="three" id="three"><h2>처음 오신 분께 — 이 페이지를 3줄로</h2><ol><li><b>무엇을</b>: {html.escape(d["three"][0])}</li>'
             f'<li><b>왜 중요한가</b>: {html.escape(d["three"][1])}</li><li><b>생활·업무에서는</b>: {html.escape(d["three"][2])}</li></ol>'
             f'<p class="note">코드와 수식을 몰라도 됩니다. 수식은 조수(하루)가 대신 묻고, 박사가 숫자로 한 번 풀어 드립니다.</p>'
             f'<details><summary>영어 약어 풀이</summary><ul>{abbr}</ul></details></section>')
    cast = '<div class="cast">' + "".join(f'<figure>{img(k)}<b>{CAST[k][0]}</b><span>{CAST[k][1]}</span></figure>' for k in CAST) + "</div>"
    p, c, nx = d["big"]
    why = (f'<section class="why" id="why"><h2>왜 이 장이 필요한가</h2>{bubble("박사", d["why"], "E09")}</section>'
           f'<section class="big"><h3>큰 그림 — 지금 어디쯤인가</h3><div class="bigrow"><div><small>앞에서</small>{html.escape(p)}</div>'
           f'<div class="now"><small>이 장</small>{html.escape(c)}</div><div><small>다음에</small>{html.escape(nx)}</div></div>'
           f'<p class="mute">이 장의 분석 도구: {TOOLS[d["tool"]["kind"]]}. 여기서 한 번 멈춰도 괜찮아요. 처음엔 다들 계산서 기호에서 오래 봅니다.</p></section>')
    du = d["duel"]
    wtxt = {"team": "추적 팀 승", "x": "범죄자 대역 승", "draw": "무승부"}[du["winner"]]
    duel = (f'<section class="step" id="duel"><div class="lab">대결</div><h2>{du["x"]} vs 추적 팀 — 계산서 공방</h2><div class="duel"><div class="vs">'
            f'<div class="side xs">{img(du["x"], "E16" if du["winner"] == "x" else "E09")}<b>{du["x"]}의 수</b><br>{html.escape(du["xmove"])}</div><div class="v">VS</div>'
            f'<div class="side ts">{img(du["team"], "E16" if du["winner"] != "x" else "E02")}<b>{CAST[du["team"]][0]}의 수</b><br>{html.escape(du["tmove"])}</div></div>'
            f'<div class="verdict">{img("박사", "E10")}<div>심판 박사 · {wtxt}<br><span style="font-weight:400">{html.escape(du["verdict"])}</span></div></div></div></section>')
    wrapq = f'<section class="step" id="wrap"><div class="lab">정리</div><h2>정리 퀴즈</h2>' + "".join(quiz(*q) for q in d["quiz"]) + "</section>"
    outro = f'<section class="step" id="outro"><div class="lab">아웃트로</div><h2>오늘의 연구실을 마치며</h2>' + "".join(bubble(w, t, e) for w, e, t in d["outro"]) + "</section>"
    kgrows = "".join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>' + " ".join(f'<a href="{c}.html">{c.replace("ch", "")}장</a>' if c != "ch00" else '<a href="ch00.html">서장</a>' for c in cs.split()) + "</td></tr>" for a, b, cs in d["kg"])
    kg = f'<section class="step kg" id="kg"><div class="lab">지식 색인</div><h2>이 장의 개념 지도</h2><table><tr><th>개념</th><th>뜻</th><th>함께 보는 장</th></tr>{kgrows}</table></section>'
    jsonld = {"@context": "https://schema.org", "@type": "LearningResource", "name": meta["title"], "description": d["three"][0],
              "inLanguage": "ko", "isPartOf": {"@type": "Book", "name": "AI 범죄와 자기 방어"},
              "author": {"@type": "Person", "name": "안상선", "url": AUTHOR_URL},
              "teaches": [k[0] for k in d["kg"]], "educationalLevel": "입문", "url": SITE_URL + slug + ".html",
              "about": [TOOLS[d["tool"]["kind"]], "범죄경제학", "AI 범죄"]}
    bib = (f"@misc{{ahn2026aicrime_{slug},\n  author = {{안상선}},\n  title = {{AI 범죄 연구실 — {meta['no']} {meta['title']}}},\n"
           f"  note = {{『AI 범죄와 자기 방어』 보충본}},\n  year = {{2026}},\n  url = {{{SITE_URL}{slug}.html}}\n}}")
    export = (f'<section class="step export" id="export"><div class="lab">꾸러미</div><h2>온톨로지·서지 꾸러미</h2><p class="mute">강의 자료나 지식 그래프에 옮길 때 쓰세요.</p>'
              f'<details><summary>JSON-LD (schema.org)</summary><button class="copy" data-t="jl-{slug}">복사</button><pre id="jl-{slug}">{html.escape(json.dumps(jsonld, ensure_ascii=False, indent=1))}</pre></details>'
              f'<details><summary>BibTeX</summary><button class="copy" data-t="bib-{slug}">복사</button><pre id="bib-{slug}">{html.escape(bib)}</pre></details></section>')
    prev_ = f'<a href="{chapters[idx-1][0]}.html">← {chapters[idx-1][1]["no"]} {chapters[idx-1][1]["title"]}</a>' if idx else '<a href="index.html">← 목차</a>'
    next_ = (f'<a href="{chapters[idx+1][0]}.html">{chapters[idx+1][1]["no"]} {chapters[idx+1][1]["title"]} →</a>' if idx + 1 < len(chapters)
             else '<a href="practice/index.html">마지막 장 · 실전 연습장 →</a>')
    hero = (f'<section class="hero"><div><div class="no">{meta["no"]}</div><h1>{html.escape(meta["title"])}</h1><p class="sub">{html.escape(meta["subtitle"])}</p>'
            f'<div class="meta">원고 대응: {html.escape(meta["source"])}<br>범죄경제학 초점: {html.escape(meta["focus"])}</div></div>'
            f'<img class="cover" src="assets/lineup.webp" alt="연구실 식구 단체 사진 — 박사, 조수 하루, 인턴 시아·모아, 주판봇, 초파리 연구원" width="1200" height="678"></section>')
    intro_html = convert(intro, slug)
    inner = (hero + three + "<h2 style='margin-top:30px'>등장인물</h2>" + cast + why + intro_html + "".join(html_steps)
             + tool_step(slug, d, n_tool) + duel + wrapq + outro + kg + export + f'<div class="pn">{prev_}{next_}</div>' + foot())
    page = (head(meta["title"], meta["subtitle"], "", jsonld, slug + ".html") + f'<div class="wrap"><nav class="toc">{toc}</nav><main>{inner}</main></div>'
            + '<script src="assets/lab.js"></script></body></html>')
    open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8").write(page)


def simple_page(name, title, txt, extra=""):
    body = mdc(txt)
    page = head(title, title, "", None, name + ".html") + f'<div class="wrap"><main>{body}{extra}{foot()}</main></div><script src="assets/lab.js"></script></body></html>'
    open(os.path.join(ROOT, name + ".html"), "w", encoding="utf-8").write(page)


def build():
    files = sorted(glob.glob(os.path.join(ROOT, "content", "ch*.md")))
    chapters = [(os.path.basename(f)[:-3], *parse(f)) for f in files]
    cards = []
    for idx, (slug, meta, body) in enumerate(chapters):
        chapter_page(slug, meta, body, idx, chapters)
        cards.append(f'<a class="card" href="{slug}.html"><div class="cno">{meta["no"]}</div><div class="ct">{html.escape(meta["title"])}</div>'
                     f'<div class="cs">{html.escape(meta["subtitle"])}</div><div class="cf">분석 도구 · {TOOLS[CH[slug]["tool"]["kind"]]}</div></a>')
    cards.append('<a class="card practice" href="practice/index.html"><div class="cno">마지막 장</div><div class="ct">실전 연습장</div>'
                 '<div class="cs">콜센터·검사 게임·랜섬 협상·기업 연결망 네 사업장을 직접 운영해 범죄자의 계산서를 뒤집어 본다.</div><div class="cf">시뮬레이터 · 미션 3개씩</div></a>')
    imeta, ibody = parse(os.path.join(ROOT, "content", "index.md"))
    inner = convert(ibody, "index").replace("{{CARDS}}", '<div class="cards" id="chapters">' + "".join(cards) + "</div>").replace("{{BOOK}}", html.escape(BOOK))
    jl = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "AI 범죄 연구실", "description": BOOK,
          "author": {"@type": "Person", "name": "안상선", "url": AUTHOR_URL}, "inLanguage": "ko", "url": SITE_URL}
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(
        head("목차", "AI 범죄와 자기 방어 보충본 — 범죄경제학·게임이론·AI로 읽는 AI 범죄", "", jl, "") + f'<div class="wrap"><main>{inner}{foot()}</main></div><script src="assets/lab.js"></script></body></html>')
    simple_page("workbook", "통합 작업본", open(os.path.join(ROOT, "content", "workbook.md"), encoding="utf-8").read())
    simple_page("references", "참고문헌과 출처", open(os.path.join(ROOT, "content", "references.md"), encoding="utf-8").read())
    code = "".join(open(os.path.join(ROOT, "scripts", f), encoding="utf-8").read() + "\n\n" for f in ["charts.py", "gen_data.py"])
    dtxt = open(os.path.join(ROOT, "content", "data.md"), encoding="utf-8").read().replace("{{CODE}}", "")
    simple_page("data", "모의 데이터와 재현 코드", dtxt, f'<button class="copy" data-t="src">코드 복사</button><pre id="src" style="background:#f6f8fb;padding:14px;border-radius:10px;font-size:12.5px;line-height:1.5;max-height:600px">{html.escape(code)}</pre>')
    # 그림 지시문 모음
    with open(os.path.join(ROOT, "images", "PROMPTS.md"), "w", encoding="utf-8") as f:
        f.write("# 그림 지시문 모음 (16비트 RPG 픽셀아트, 낮의 연구실·흰 배경)\n\n")
        f.write("- 만드는 순서: 시리즈 표지 → 서장~10장 장면 → 실전 연습장 표지\n- 비율: 표지 1600×900, 장면 1200×800 → WebP로 변환해 `assets/covers/`에 저장\n"
                "- 캐릭터는 fruitfly-lab-expressions 정본(박사·하루·시아·모아·주판봇·초파리·X1~X3 실루엣)을 참고 그림으로 함께 올린다.\n"
                "- 지금은 모든 장에 단체 사진(`assets/lineup.webp`)을 임시 표지로 쓴다.\n\n")
        for slug, title, p in PROMPTS:
            f.write(f"## {slug} · {title or '장면'}\n\n저장 이름: `assets/covers/{slug}.webp`\n\n```\n{p}\n```\n\n")
    print("built", len(chapters), "chapters,", len(PROMPTS), "prompts")


if __name__ == "__main__":
    build()
