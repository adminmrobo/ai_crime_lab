"""리포트 검증 No.001 — 그림(SVG)과 report-data를 원본 HTML에 채운다.
사용: python scripts/build_report_001.py  → reports/<slug>/kg/page.html (꼬리표 달기 전 본문)
"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "reports" / "2026-11-23_lnrs-synthetic-identity-deepfake"
INK, SUB, MUTE, LINE = "#1d2430", "#4a5562", "#7a8492", "#e3e8ee"
C24, C25, ONE = "#9db3e8", "#2f4fa8", "#3d63c9"

DATA = {
    "fig41": {"columns": ["유형", "2024년(%)", "2025년(%)", "출처"],
              "rows": [["제1자 사기", 36, 38.3, "[4][10]"], ["합성 신원", 1.4, 11, "[2]"], ["실제 신원 도용", 9.9, 6.4, "[2]"]]},
    "fig42": {"columns": ["사례", "연결된 신원(명)", "하한값 여부", "확인된 실제 사람(명)", "출처"],
              "rows": [["런던 주소 1곳", 1653, "아니오", 10, "[1]"], ["치체스터 농장 1곳(7년)", 439, "아니오", 22, "[1][7]"],
                       ["옥스퍼드 주택 9곳 연결망", 150, "예(150명 이상)", "", "[1]"]]},
    "fig61": {"columns": ["관계", "항목 수"],
              "rows": [["같은 방향", 5], ["책에 더할 내용", 3], ["갱신 후보", 1], ["처방이 다름", 1], ["책에만 있음", 1]]},
}


def t(x, y, s, size=13, anchor="start", fill=INK, weight="400"):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}" font-weight="{weight}">{html.escape(str(s))}</text>'


def bar(x, y, w, h, fill, tip):
    # 오른쪽 끝만 둥근 막대(기준선 쪽은 각짐)
    r = min(4, w / 2, h / 2)
    p = f"M{x},{y} H{x+w-r} Q{x+w},{y} {x+w},{y+r} V{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} H{x} Z"
    return f'<path d="{p}" fill="{fill}"><title>{html.escape(tip)}</title></path>'


def fig41():
    W, L, R = 760, 150, 70
    sx = lambda v: (W - L - R) * v / 40
    o = [f'<svg viewBox="0 0 {W} 250" role="img" aria-label="사기 유형별 비중 2024년 대 2025년 막대그래프"><rect width="{W}" height="250" fill="#fff"/>']
    o.append(f'<rect x="{L}" y="12" width="12" height="12" rx="2" fill="{C24}"/>' + t(L + 18, 23, "2024년", 12.5, fill=SUB))
    o.append(f'<rect x="{L+90}" y="12" width="12" height="12" rx="2" fill="{C25}"/>' + t(L + 108, 23, "2025년", 12.5, fill=SUB))
    for v in (0, 10, 20, 30, 40):
        x = L + sx(v)
        o.append(f'<line x1="{x}" y1="36" x2="{x}" y2="226" stroke="{LINE}"/>' + t(x, 242, v, 11.5, "middle", MUTE))
    y = 46
    for name, a, b, _ in DATA["fig41"]["rows"]:
        o.append(t(L - 10, y + 32, name, 13.5, "end", weight="700"))
        for v, c, lab in ((a, C24, "2024년"), (b, C25, "2025년")):
            o.append(bar(L, y, sx(v), 24, c, f"{name} {lab}: {v}%"))
            o.append(t(L + sx(v) + 6, y + 17, f"{v}%", 12.5, fill=INK))
            y += 26
        y += 12
    o.append(f'<line x1="{L}" y1="36" x2="{L}" y2="226" stroke="{SUB}" stroke-width="1.5"/></svg>')
    return "".join(o)


def fig42():
    W, L, R = 760, 200, 110
    sx = lambda v: (W - L - R) * v / 1800
    o = [f'<svg viewBox="0 0 {W} 210" role="img" aria-label="주소에 연결된 신원 수 막대그래프"><rect width="{W}" height="210" fill="#fff"/>']
    for v in (0, 500, 1000, 1500):
        x = L + sx(v)
        o.append(f'<line x1="{x}" y1="14" x2="{x}" y2="180" stroke="{LINE}"/>' + t(x, 198, f"{v:,}", 11.5, "middle", MUTE))
    x50 = L + sx(50)
    o.append(f'<line x1="{x50}" y1="10" x2="{x50}" y2="180" stroke="{SUB}" stroke-dasharray="4 3"/>' + t(x50 + 4, 12, "합성 주택 기준 50명", 11, fill=SUB))
    y = 28
    for name, v, lb, real, _ in DATA["fig42"]["rows"]:
        o.append(t(L - 10, y + 20, name, 13, "end", weight="700"))
        tip = f"{name}: {v:,}명{' 이상' if lb != '아니오' else ''}" + (f", 확인된 실제 사람 {real}명" if real != "" else "")
        o.append(bar(L, y, sx(v), 28, ONE, tip))
        lab = f"{v:,}{'+' if lb != '아니오' else ''}명" + (f" (실제 확인 {real})" if real != "" else "")
        o.append(t(L + sx(v) + 6, y + 19, lab, 12.5))
        y += 50
    o.append(f'<line x1="{L}" y1="14" x2="{L}" y2="180" stroke="{SUB}" stroke-width="1.5"/></svg>')
    return "".join(o)


def fig61():
    W, L, R = 760, 150, 60
    sx = lambda v: (W - L - R) * v / 6
    rows = DATA["fig61"]["rows"]
    H = 30 + 34 * len(rows)
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="대조 결과 집계 막대그래프"><rect width="{W}" height="{H}" fill="#fff"/>']
    y = 12
    for name, v in rows:
        o.append(t(L - 10, y + 17, name, 13, "end", weight="700"))
        o.append(bar(L, y, sx(v), 22, ONE, f"{name}: {v}개"))
        o.append(t(L + sx(v) + 6, y + 16, f"{v}개", 12.5))
        y += 34
    o.append(f'<line x1="{L}" y1="6" x2="{L}" y2="{y}" stroke="{SUB}" stroke-width="1.5"/></svg>')
    return "".join(o)


src = (D / "kg" / "page.src.html").read_text(encoding="utf-8")
out = (src.replace("{{FIG41}}", fig41()).replace("{{FIG42}}", fig42()).replace("{{FIG61}}", fig61())
       .replace("{{DATA}}", json.dumps(DATA, ensure_ascii=False)))
assert "{{" not in out
(D / "kg" / "page.html").write_text(out, encoding="utf-8")
print("ok", len(out))
