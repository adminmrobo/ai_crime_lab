# -*- coding: utf-8 -*-
"""content/*.md + scripts/lab_data.py → 루트 *.html (GitHub Pages)."""
import os, re, glob, html, json
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crime_onto  # AI 범죄학(crime) 지식 색인 데이터
import markdown
from lab_data import CH, TOOLS
from steps_data import STEPS, REVIEW, INST, RL
from polite import polite

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_URL = "https://adminmrobo.github.io/ai_crime_lab/"
AUTHOR_URL = "https://adminmrobo.github.io/who_am_i/who_am_i.html"
BOOK = ("『AI 범죄와 자기 방어』 — AI가 범죄에 쓰이는 실제 사례를 모으고, 범죄자가 왜 AI를 고르는지를 범죄경제학의 눈으로 묻는 책. "
        "범죄자도 비용과 이익을 따진다는 관점에서, AI가 범죄의 비용 구조와 수익 모델을 어떻게 바꾸었는지 풀어낸다. 이 사이트는 그 책을 사례와 함께 풀어 쓴 보충본이다.")

GB_URL = "https://books.google.co.kr/books/about/AI_%EB%B2%94%EC%A3%84%EC%99%80_%EC%9E%90%EA%B8%B0_%EB%B0%A9%EC%96%B4.html?id=FimKEQAAQBAJ"
BOOKINFO = {"title": "AI 범죄와 자기 방어", "subtitle": "AI 범죄 시대, 자기 방어의 지혜", "author": "안상선",
            "publisher": "커뮤니케이션북스", "series": "인공지능총서", "date": "2025-10-10", "isbn": "9791143009050"}
BOOK_BOX = (
    '<section class="bookinfo" id="book"><h2>책 소개 — 『AI 범죄와 자기 방어』</h2>'
    '<p class="mute">AI 범죄 시대, 자기 방어의 지혜 · 안상선 지음 · 커뮤니케이션북스(인공지능총서) · 2025년 10월 10일 · ISBN 9791143009050</p>'
    '<ol><li><b>무엇을 다루나</b>: 친구를 사칭하는 메신저 피싱, 가족 목소리를 흉내 내는 보이스피싱처럼 이미 일상에 들어온 AI 범죄를 살펴봅니다.</li>'
    '<li><b>어떤 눈으로 보나</b>: 범죄자가 왜 AI를 고르는지를 범죄경제학으로 묻습니다. 공격자의 비용·이익 계산을 알아야 제대로 막을 수 있다는 관점입니다.</li>'
    '<li><b>무엇을 제안하나</b>: 개인에게 맞춘 보안 수칙과 함께, 기술 대책을 넘어 윤리·제도 차원의 사회적 대응을 제안합니다.</li></ol>'
    '<p>이 사이트는 그 책을 사례·모의 데이터·시뮬레이션으로 풀어 쓴 보충본입니다. '
    f'<a href="{GB_URL}" target="_blank" rel="noopener">Google 도서에서 보기</a> · '
    '<a href="https://adminmrobo.github.io/who_am_i/who_am_i.html" target="_blank" rel="noopener">저자 소개</a></p></section>')

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
    body = mdc(polite(text)).removeprefix("<p>").removesuffix("</p>")
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
    import hashlib
    rot = int(hashlib.md5(q.encode()).hexdigest(), 16) % len(opts)
    opts = opts[rot:] + opts[:rot]
    a = (a - rot) % len(opts)
    bs = "".join(f"<button type=\"button\">{chr(9312 + k)} {html.escape(o)}</button>" for k, o in enumerate(opts))
    return f'<div class="quiz" data-a="{a}"><div class="q">확인 퀴즈 · {html.escape(q)}</div>{bs}<div class="ex" hidden><b></b>{html.escape(ex)}</div></div>'


ALT = {
    "ch00": "두 장면 그림 — 의심스러운 링크 메시지와 익숙한 목소리 전화를 받는 직장인, 뒤에서 비용↓ 수익↑ 영수증을 든 X1 실루엣",
    "ch01": "한 대의 전화로 일하는 사기범과 말풍선을 수백 개 쏟아내는 서버, 깔때기 그래프를 돋보기로 읽는 인턴 시아",
    "ch02": "화이트보드에 기대효용 식을 쓰는 박사, p·f·g 구슬을 옮기는 주판봇, 손을 든 X1·X2·X3 실루엣",
    "ch03": "다섯 얼굴이 뜬 영상회의 화면 앞에서 송금 버튼을 망설이는 직원과 콜백 카드를 든 조수 하루",
    "ch04": "봉투 알림이 뜬 사무실, 확인·멈춤·신고 순서를 교육하는 인턴 모아, 천장에서 낚싯대를 드리운 X1 실루엣",
    "ch05": "색을 바꾸는 슬라임을 부리는 X2 실루엣, 무너지는 규칙 표지판, 새벽 3시 이상 신호를 보는 하루와 초파리 연구원",
    "ch06": "카메라 기둥 위에 뜬 눈, 주머니에서 흘린 정보 조각을 맞추는 X3 실루엣, 조각 하나를 가리는 인턴 시아",
    "ch07": "점선 장갑이 옮기는 동전 사슬, 동전을 쪼개 섞는 X3 실루엣, 등불로 흔적을 쫓는 시아와 잠긴 서버 옆 초록 백업",
    "ch08": "패스키·백업·차단·콜백·비밀번호 관리자 조각으로 방패를 만드는 가족, 창밖에서 돌아서는 X1 실루엣",
    "ch09": "초록 방패를 쓴 건물들이 붉은 파동을 막는 마을 지도, 문턱에 깃발을 꽂는 박사, 막힌 허브 앞의 X2 실루엣",
    "ch10": "마이너스가 찍힌 붉은 영수증을 찢는 X1·X2·X3 실루엣, 규칙·당근·채찍·의사봉 네 겹 방패 앞의 연구실 식구",
}


def head(title, desc, pre="", jsonld=None, path="", og_img="assets/og/index.webp"):
    og = SITE_URL + og_img
    jl = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{"AI 범죄 연구실 — 『AI 범죄와 자기 방어』 보충본" if title == "목차" else html.escape(title) + " · AI 범죄 연구실"}</title><meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)} · AI 범죄 연구실"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{og}"><meta property="og:url" content="{SITE_URL}{path}"><meta property="og:type" content="article">
<link rel="stylesheet" href="{pre}assets/lab.css">{jl}</head><body>
<header class="top"><a class="brand" href="{pre}index.html">AI 범죄 연구실 — 범죄자의 계산서를 뒤집어라</a>
<a href="{pre}index.html#chapters">목차</a><a href="{pre}practice/index.html">실전 연습장</a><a href="{pre}reports/index.html">리포트 검증</a><a href="{pre}ontology.html">온톨로지 지도</a><a href="{pre}workbook.html">통합 작업본</a><a href="{pre}references.html">참고문헌</a><a href="{pre}data.html">모의 데이터</a></header>"""


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


XLINE = {"X1": "규칙이 있어도 아무도 안 잡으면 나는 계속한다.", "X2": "처벌 조항만 무거우면 오히려 마음이 편하다. 어차피 안 잡히니까.", "X3": "현금화 창구에 감시가 없으면 규칙은 종이일 뿐이다."}


def inst_step(slug, n):
    I = INST[slug]; r = RL[slug]
    xs = r["who"] if r["who"].startswith("X") else "X1"
    rows = "".join(f"<tr><td><b>{a}</b></td><td>{html.escape(b)}</td><td>{c}</td></tr>" for a, b, c in [
        ("규칙", I["rule"], "무엇이 금지·의무인지 정한다"), ("인센티브", I["carrot"], "지키는 쪽을 이익으로 만든다"),
        ("디스인센티브", I["stick"], "어기는 쪽을 손해로 만든다"), ("강제력(집행)", I["enforce"], "실제로 찾아내고 적용한다")])
    opts = [I["enforce"], I["carrot"], I["rule"]]
    return (f'<section class="step" id="inst"><div class="lab">단계 {n} · 제도 설계</div><h2>도덕적 원칙이 아니라 제도로 — 이 장의 네 가지 손잡이</h2><span class="tag">방법: 규칙 · 인센티브 · 디스인센티브 · 강제력</span>'
            + bubble("박사", "현장 질문 하나로 시작할게요. '이러면 안 됩니다'라는 원칙을 모두에게 알리면, 이 장의 범죄는 줄어들까요?", "E07")
            + f'<table><tr><th>요소</th><th>이 장의 제도</th><th>하는 일</th></tr>{rows}</table>'
            + '<h3>단계 대화</h3>' + bubble("주판봇", "법만 만들면 다 지켜요! 규칙이 제일 중요해요.", "E16") + bubble(xs, XLINE[xs], "E16")
            + bubble("초파리", "규칙·처벌·집행·인센티브를 하나씩 켜고 끄면서 확인해 보자. 다음 단계 강화학습 실험에서 눌러 봐.", "E09")
            + bubble("모아", "네 가지가 서로를 받쳐요. 규칙이 없으면 잡아도 처벌 근거가 없고, 집행이 없으면 규칙은 종이에만 있어요.", "E07")
            + bubble("박사", "해석: 원칙은 출발점이에요. 의도한 효과는 이 네 가지가 함께 있을 때 나옵니다.", "E10")
            + quiz("이 장의 제도 가운데 '강제력(집행)'에 해당하는 것은?", opts, 0, "실제로 찾아내고 적용하는 장치가 강제력이다.") + "</section>")


def rl_step(slug, n):
    r = RL[slug]; I = INST[slug]
    cfg = dict(kind=r["kind"], agentName=r["agentName"], actions=r["actions"], inst=I)
    crime = r["kind"] == "crime"
    tr = ("α는 '그 행동을 해 본 횟수 분의 1'이다. 첫 시도에 성공해 +980(=1,000−20)을 받으면 α=1이라 Q = 0 + 1 × (980 − 0) = 980. "
          "두 번째에 실패하고 잡혀 −1,520(=−20−1,500)을 받으면 α=1/2이라 Q = 980 + ½ × (−1,520 − 980) = −270. 두 보상의 평균 (980 − 1,520) ÷ 2와 같다.") if crime else (
          "α는 '그 행동을 해 본 횟수 분의 1'이다. 첫 생략에서 사고 없이 0을 받으면 Q = 0. 두 번째에 감사에 걸려 −100을 받으면 α=1/2이라 Q = 0 + ½ × (−100 − 0) = −50. 두 보상의 평균과 같다.")
    who = r["who"]
    return f"""<section class="step" id="rl"><div class="lab">단계 {n} · 강화학습 시뮬레이션 (모든 장 공통 마지막 단계)</div><h2>{html.escape(r['agentName'])}는 무엇을 배울까 — 제도를 바꾸며 3,000번 학습</h2><span class="tag">방법: 강화학습(Q-러닝, 엡실론-탐욕)</span>
{bubble('박사', '현장 질문 하나로 시작할게요. ' + r['agentName'] + '에게 도덕을 가르치지 않고, 보상만 바꾸면 행동이 바뀔까요?', 'E07')}
<div class="duo"><div class="whybox"><h4>왜 이 방법을 쓰나</h4><dl><dt>문제 상황</dt><dd>앞 단계의 계산은 '한 번의 선택'이었다. 실제 행위자는 해 보고, 결과를 보고, 다음 선택을 고친다.</dd>
<dt>앞 방법의 한계</dt><dd>기댓값 계산은 행위자가 모든 확률을 안다고 가정한다. 현실의 행위자는 경험으로 배운다.</dd>
<dt>해법</dt><dd>강화학습 에이전트를 두고, 제도가 만든 보상만 주어 스스로 배우게 한다. 무엇을 배우는지 보면 제도의 효과가 보인다.</dd>
<dt>쉽게 말하면</dt><dd>강아지 훈련처럼, 잘하면 간식(인센티브)·잘못하면 간식 없음(디스인센티브)을 '매번 확실하게' 줄 때 행동이 바뀐다.</dd></dl></div>
<div class="mathbox"><h4>수식을 어려워하는 조수가 대신 물어봅니다</h4><div class="mini">{img('하루','E04')}<div><b>하루</b> Q는 뭐고, 화살표(←)는 왜 있어요?</div></div>
<dl><dt>학교 수학으로 보면</dt><dd>점화식(앞 값으로 다음 값을 만드는 식), 평균</dd></dl>
<table class="parts"><tr><th>식 조각</th><th>읽는 법</th><th>뜻</th></tr><tr><td><b>Q(행동)</b></td><td>큐</td><td>그 행동이 평균적으로 얼마를 주는지에 대한 지금까지의 짐작</td></tr>
<tr><td><b>r</b></td><td>알</td><td>이번에 실제로 받은 보상</td></tr><tr><td><b>α</b></td><td>알파</td><td>새 경험을 얼마나 반영할지(여기서는 해 본 횟수 분의 1 → Q는 평균이 된다)</td></tr>
<tr><td><b>Q ← Q + α × (r − Q)</b></td><td></td><td>짐작을 '실제 − 짐작'의 일부만큼 고친다</td></tr><tr><td><b>ε</b></td><td>엡실론</td><td>가끔 일부러 다른 행동을 해 보는 비율(처음 30% → 끝 2%)</td></tr></table>
<dl><dt>숫자로 한 번 해 보기</dt><dd>{html.escape(tr)}</dd></dl><div class="mini">{img('하루','E01')}<div><b>하루</b> 화살표는 '이렇게 고쳐 쓴다'는 뜻이군요. 보상이 확실히 나쁘면 Q가 금방 내려가고, 그 행동을 덜 고르게 돼요.</div></div></div></div>
<div class="pair"><div><b>일상으로 치면</b>벌금 고지서가 '가끔' 오면 습관이 안 바뀌고, '매번 확실히' 오면 바뀐다.</div><div><b>현장에서는</b>정책 실험(시범 사업)에서 제도를 바꾼 뒤 행동 변화를 재는 방식과 같다. 여기서는 그것을 가상 에이전트로 미리 해 본다.</div></div>
<h3>단계 대화 · AI 판단 코너</h3>{bubble('박사', '처벌을 아주 무겁게만 하면 ' + r['agentName'] + '의 행동이 바뀔까요?', 'E07')}{bubble('주판봇', '당연하죠! 처벌이 무거우면 아무도 안 해요.', 'E16')}{bubble('초파리', '집행이 없으면 처벌을 받을 일이 드물어. 아래에서 「규칙 + 처벌(집행 없음)」과 「규칙 + 집행」을 비교 실험으로 눌러 봐.', 'E09')}{bubble(who, ('처벌이 무거워도 잡을 사람이 없으면 내 계산은 그대로다.' if crime else '확인하라는 규정만 있고 아무도 안 보면, 나는 그냥 바로 처리한다.'), 'E09' if not who.startswith('X') else 'E16')}
<figure class="fig"><img src="assets/covers/rl.webp" alt="세 갈래 길 앞의 말과 길마다 바뀌는 점수, 규칙·의사봉·채찍·당근 스위치를 켜면 붉은 길 점수가 음수가 되어 말이 초록 길로 돌아서는 그림" width="1200" height="800" loading="lazy"><figcaption>규칙과 집행 스위치를 켜면 범죄 쪽 길의 점수가 음수로 바뀌고, 에이전트가 합법 쪽 길을 배웁니다.</figcaption></figure>
<div class="panel"><h4>실험: 제도를 켜고 끄며 학습시키기</h4><p class="mute">{'세 행동: ' + ' · '.join(r['actions'])}. 보상 단위는 만 원, 모든 숫자는 교육용 예시다.</p><div data-rl='{html.escape(json.dumps(cfg, ensure_ascii=False))}'></div></div>
{bubble('박사', '풀이: 에이전트는 도덕을 모릅니다. 규칙이 있어야 처벌할 근거가 생기고, 집행이 있어야 처벌이 실제 보상에 들어가며, 인센티브가 있어야 지키는 쪽이 이익이 됩니다. 이 네 가지가 함께 있을 때 학습된 행동이 바뀝니다. 해석: 이 숫자는 정책에서 «선언보다 집행 예산과 확인 절차의 비용이 더 중요하다»는 뜻입니다.', 'E10')}
<aside class="box warn" style="background:#fff8e6;border-color:#b7791f"><div class="bt" style="color:#b7791f">이 단계의 한계 — 여기서는 단순하게 봤어요</div><p>에이전트는 한 명이고 확률은 고정이며, 평판·양심·처벌 공포의 과대평가 같은 사람의 특성은 빠져 있다. 도덕이 쓸모없다는 뜻이 아니다. 도덕만으로는 의도한 효과를 보장할 수 없다는 뜻이다. 실제 정책 효과는 현장 데이터로 다시 재야 한다.</p></aside>
<details><summary>교안의 파이썬 코드로 보면 (몰라도 됩니다)</summary><p><code>n[a] += 1; Q[a] += (r - Q[a]) / n[a]</code><br>받은 보상과 짐작의 차이를 해 본 횟수로 나눠 고친다. 결과적으로 평균 보상이 된다.</p></details>
{quiz('강화학습 실험에서 범죄(또는 생략) 선택이 가장 확실히 줄어드는 조합은?', ['규칙만', '처벌만 무겁게(집행 없음)', '규칙 + 집행 + 처벌 또는 인센티브'], 2, '규칙·집행·처벌(또는 인센티브)이 함께 있어야 보상 구조가 바뀐다.')}</section>"""


def chapter_page(slug, meta, body, idx, chapters):
    d = CH[slug]
    # 단계로 나누기
    secs = re.split(r"\n(?=## )", "\n" + body)
    intro, steps = secs[0], secs[1:]
    html_steps = []
    sd = STEPS[slug]
    assert len(sd) == len(steps), (slug, len(sd), len(steps))
    for k, s in enumerate(steps, 1):
        title, rest = s.strip().split("\n", 1)
        title = title[3:].strip()
        t_clean = re.sub(r"^\d+\.\s*", "", title)
        st = sd[k - 1]
        talk = "".join(bubble(w, txt.replace("*", "\\*"), e) for w, e, txt in st["talk"])
        html_steps.append(
            f'<section class="step" id="s{k}"><div class="lab">단계 {k}</div><h2>{html.escape(t_clean)}</h2><span class="tag">{html.escape(st["tag"])}</span>'
            + bubble("박사", "현장 질문 하나로 시작할게요. " + st["sit"], "E07") + convert(rest, slug)
            + f'<div class="pair"><div><b>일상으로 치면</b>{html.escape(st["daily"])}</div><div><b>현장에서는</b>{html.escape(st["field"])}</div></div>'
            + '<h3>단계 대화</h3>' + talk + bubble("박사", "해석: " + st["interp"], "E10") + quiz(*st["quiz"]) + "</section>")
    n_tool = len(steps) + 1
    toc = (f"<b>{html.escape(meta['no'])}</b><a href='#three'>처음 오신 분께</a><a href='#why'>왜 · 큰 그림</a>"
           + "".join(f'<a href="#s{k}">단계 {k}</a>' for k in range(1, len(steps) + 1))
           + f"<a href='#tool'>단계 {n_tool} · 분석 도구</a><a href='#inst'>단계 {n_tool+1} · 제도 설계</a><a href='#rl'>단계 {n_tool+2} · 강화학습</a><a href='#duel'>대결</a><a href='#wrap'>정리 퀴즈</a><a href='#outro'>아웃트로</a><a href='#kg'>지식 색인</a><a href='#export'>꾸러미</a>")
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
           f'<p class="mute">이 장의 분석 도구: {TOOLS[d["tool"]["kind"]]} · 마지막 단계는 모든 장 공통의 강화학습 시뮬레이션입니다. 여기서 한 번 멈춰도 괜찮아요. 처음엔 다들 계산서 기호에서 오래 봅니다.</p>'
           f'<aside class="box note" style="background:#f6f8fb;border-color:#1f3a6b"><div class="bt" style="color:#1f3a6b">30초 복습 · {html.escape(REVIEW[slug][0])}</div><p>{html.escape(REVIEW[slug][1])}</p></aside></section>')
    du = d["duel"]
    wtxt = {"team": "추적 팀 승", "x": "범죄자 대역 승", "draw": "무승부"}[du["winner"]]
    duel = (f'<section class="step" id="duel"><div class="lab">대결</div><h2>{du["x"]} vs 추적 팀 — 계산서 공방</h2><div class="duel"><div class="vs">'
            f'<div class="side xs">{img(du["x"], "E16" if du["winner"] == "x" else "E09")}<b>{du["x"]}의 수</b><br>{html.escape(du["xmove"])}</div><div class="v">VS</div>'
            f'<div class="side ts">{img(du["team"], "E16" if du["winner"] != "x" else "E02")}<b>{CAST[du["team"]][0]}의 수</b><br>{html.escape(du["tmove"])}</div></div>'
            f'<div class="verdict">{img("박사", "E10")}<div>심판 박사 · {wtxt}<br><span style="font-weight:400">{html.escape(polite(du["verdict"]))}</span></div></div></div></section>')
    wrapq = f'<section class="step" id="wrap"><div class="lab">정리</div><h2>정리 퀴즈</h2>' + "".join(quiz(*q) for q in d["quiz"]) + "</section>"
    outro = f'<section class="step" id="outro"><div class="lab">아웃트로</div><h2>오늘의 연구실을 마치며</h2>' + "".join(bubble(w, t, e) for w, e, t in d["outro"]) + "</section>"
    kgrows = "".join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>' + " ".join(f'<a href="{c}.html">{c.replace("ch", "")}장</a>' if c != "ch00" else '<a href="ch00.html">서장</a>' for c in cs.split()) + "</td></tr>" for a, b, cs in d["kg"])
    kg = f'<section class="step kg" id="kg"><div class="lab">지식 색인</div><h2>이 장의 개념 지도</h2><table><tr><th>개념</th><th>뜻</th><th>함께 보는 장</th></tr>{kgrows}</table></section>'
    jsonld = {"@context": "https://schema.org", "@type": "LearningResource", "name": meta["title"], "description": d["three"][0],
              "inLanguage": "ko", "isPartOf": {"@type": "Book", "name": "AI 범죄와 자기 방어", "isbn": BOOKINFO["isbn"], "datePublished": BOOKINFO["date"], "publisher": {"@type": "Organization", "name": "커뮤니케이션북스"}, "url": GB_URL},
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
            f'<img class="cover" src="assets/covers/{slug}.webp" alt="{html.escape(ALT[slug])}" width="1200" height="800"></section>')
    intro_html = convert(intro, slug)
    inner = (hero + three + "<h2 style='margin-top:30px'>등장인물</h2>" + cast + why + intro_html + "".join(html_steps)
             + tool_step(slug, d, n_tool) + inst_step(slug, n_tool + 1) + rl_step(slug, n_tool + 2) + duel + wrapq + outro + kg + export + f'<div class="pn">{prev_}{next_}</div>' + foot())
    page = (head(meta["title"], meta["subtitle"], "", jsonld, slug + ".html", f"assets/og/{slug}.webp") + f'<div class="wrap"><nav class="toc">{toc}</nav><main>{inner}</main></div>'
            + '<script type="application/json" id="kg-raw">' + json.dumps(crime_onto.kg_raw(slug), ensure_ascii=False).replace("</", "<\\/") + '</script>'
            + '<script src="assets/lab.js"></script><script src="assets/rl.js"></script></body></html>')
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
        cards.append(f'<a class="card" href="{slug}.html"><img class="thumb" src="assets/thumbs/{slug}.webp" alt="" width="600" height="400" loading="lazy"><div class="cno">{meta["no"]}</div><div class="ct">{html.escape(meta["title"])}</div>'
                     f'<div class="cs">{html.escape(meta["subtitle"])}</div><div class="cf">분석 도구 · {TOOLS[CH[slug]["tool"]["kind"]]}</div></a>')
    cards.append('<a class="card practice" href="practice/index.html"><img class="thumb" src="practice/cover.webp" alt="" width="1600" height="900" loading="lazy"><div class="cno">마지막 장</div><div class="ct">실전 연습장</div>'
                 '<div class="cs">콜센터·검사 게임·랜섬 협상·기업 연결망 네 사업장을 직접 운영해 범죄자의 계산서를 뒤집어 본다.</div><div class="cf">시뮬레이터 · 미션 3개씩</div></a>')
    cards.append('<a class="card" href="reports/index.html" style="border:2px solid #3d63c9;background:#f8faff"><img class="thumb" src="reports/2026-11-23_lnrs-synthetic-identity-deepfake/thumb.webp" alt="" width="600" height="400" loading="lazy"><div class="cno">현장 검증</div><div class="ct">리포트·뉴스 검증 INDEX</div>'
                 '<div class="cs">새로 나온 보고서와 뉴스를 책의 장과 나란히 놓고, 책의 분석이 현장에서 어떻게 확인되는지 쌓아 간다.</div><div class="cf">박사의 뉴스 소개 · 장별 대조표</div></a>')
    cards.append('<a class="card" href="ontology.html" style="border:2px solid #1f8a5b;background:#f3fbf6"><div class="cno">분야 지도</div><div class="ct">AI 범죄학 온톨로지 지도</div>'
                 '<div class="cs">책의 분석 틀로 짠 13개 영역·49개 주제 위에, 책이 다룬 개념과 리포트로 확인된 개념을 겹쳐 본다.</div><div class="cf">3D 지도 · 영역별 커버리지</div></a>')
    imeta, ibody = parse(os.path.join(ROOT, "content", "index.md"))
    inner = convert(ibody, "index").replace("{{CARDS}}", '<div class="cards" id="chapters">' + "".join(cards) + "</div>").replace("{{BOOK}}", html.escape(BOOK)).replace("{{BOOKBOX}}", BOOK_BOX)
    jl = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "AI 범죄 연구실", "description": BOOK, "about": {"@type": "Book", "name": BOOKINFO["title"], "alternativeHeadline": BOOKINFO["subtitle"], "author": {"@type": "Person", "name": "안상선"}, "publisher": {"@type": "Organization", "name": "커뮤니케이션북스"}, "datePublished": BOOKINFO["date"], "isbn": BOOKINFO["isbn"], "url": GB_URL},
          "author": {"@type": "Person", "name": "안상선", "url": AUTHOR_URL}, "inLanguage": "ko", "url": SITE_URL}
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(
        head("목차", "AI 범죄와 자기 방어 보충본 — 범죄경제학·게임이론·AI로 읽는 AI 범죄", "", jl, "") + f'<div class="wrap"><main>{inner}{foot()}</main></div><script src="assets/lab.js"></script></body></html>')
    simple_page("workbook", "통합 작업본", open(os.path.join(ROOT, "content", "workbook.md"), encoding="utf-8").read())
    simple_page("references", "참고문헌과 출처", open(os.path.join(ROOT, "content", "references.md"), encoding="utf-8").read())
    code = "".join(open(os.path.join(ROOT, "scripts", f), encoding="utf-8").read() + "\n\n" for f in ["charts.py", "gen_data.py"])
    dtxt = open(os.path.join(ROOT, "content", "data.md"), encoding="utf-8").read().replace("{{CODE}}", "")
    simple_page("data", "모의 데이터와 재현 코드", dtxt, f'<button class="copy" data-t="src">코드 복사</button><pre id="src" style="background:#f6f8fb;padding:14px;border-radius:10px;font-size:12.5px;line-height:1.5;max-height:600px">{html.escape(code)}</pre>')
    # 그림 지시문 모음
    with open(os.devnull, "w", encoding="utf-8") as f:
        f.write("# 그림 지시문 모음 (16비트 RPG 픽셀아트, 낮의 연구실·흰 배경)\n\n")
        f.write("- 만드는 순서: 시리즈 표지 → 서장~10장 장면 → 실전 연습장 표지\n- 비율: 표지 1600×900, 장면 1200×800 → WebP로 변환해 `assets/covers/`에 저장\n"
                "- 캐릭터는 fruitfly-lab-expressions 정본(박사·하루·시아·모아·주판봇·초파리·X1~X3 실루엣)을 참고 그림으로 함께 올린다.\n"
                "- 지금은 모든 장에 단체 사진(`assets/lineup.webp`)을 임시 표지로 쓴다.\n\n")
        for slug, title, p in PROMPTS:
            f.write(f"## {slug} · {title or '장면'}\n\n저장 이름: `assets/covers/{slug}.webp`\n\n```\n{p}\n```\n\n")
    print("built", len(chapters), "chapters,", len(PROMPTS), "prompts")


if __name__ == "__main__":
    build()
