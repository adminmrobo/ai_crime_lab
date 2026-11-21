"""간단한 SVG 차트 도구 (외부 라이브러리 없이 흰 배경용)."""
from html import escape

PAL = {
    "crime": "#d6453d",   # 범죄자 쪽
    "crime2": "#f08a5d",
    "defense": "#1f8a5b",  # 방어 쪽
    "defense2": "#6cc08b",
    "neutral": "#4a6fd1",
    "neutral2": "#93a9e8",
    "gray": "#9aa3ad",
    "violet": "#7a5bd1",
    "amber": "#d9902b",
}
W, H = 720, 380
ML, MR, MT, MB = 70, 24, 46, 64


def _fmt(v):
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    if abs(v) >= 10 or float(v).is_integer():
        return f"{v:.0f}"
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _nice(lo, hi, n=5):
    import math
    if hi == lo:
        hi = lo + 1
    span = hi - lo
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    step = min([1, 2, 2.5, 5, 10], key=lambda s: abs(s * mag - raw)) * mag
    start = math.floor(lo / step) * step
    ticks = []
    t = start
    while t <= hi + step * 0.001:
        ticks.append(round(t, 10))
        t += step
    if ticks[-1] < hi - 1e-9:
        ticks.append(round(ticks[-1] + step, 10))
    return ticks


def _frame(title, xlab, ylab, ticks, ymap, pw):
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="{escape(title)}" font-family="Pretendard, Noto Sans KR, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{ML}" y="26" font-size="16" font-weight="700" fill="#1d2430">{escape(title)}</text>',
         f'<text x="{W-MR}" y="26" font-size="11" text-anchor="end" fill="#8a93a0">모의 데이터(가상)</text>']
    for t in ticks:
        y = ymap(t)
        s.append(f'<line x1="{ML}" x2="{ML+pw}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e8ecf1"/>')
        s.append(f'<text x="{ML-8}" y="{y+4:.1f}" font-size="11" text-anchor="end" fill="#5b6572">{_fmt(t)}</text>')
    s.append(f'<text x="{ML+pw/2}" y="{H-12}" font-size="12" text-anchor="middle" fill="#3b4450">{escape(xlab)}</text>')
    s.append(f'<text transform="translate(16,{MT+(H-MT-MB)/2}) rotate(-90)" font-size="12" '
             f'text-anchor="middle" fill="#3b4450">{escape(ylab)}</text>')
    return s


def _legend(s, names, colors, dashes=None):
    x = ML
    y = H - 34
    for i, (n, c) in enumerate(zip(names, colors)):
        d = (dashes or [None] * len(names))[i]
        dash = f' stroke-dasharray="{d}"' if d else ""
        s.append(f'<line x1="{x}" x2="{x+22}" y1="{y}" y2="{y}" stroke="{c}" stroke-width="4"{dash}/>')
        s.append(f'<text x="{x+28}" y="{y+4}" font-size="11.5" fill="#3b4450">{escape(n)}</text>')
        x += 40 + len(n) * 11.5


def line_chart(title, xs, series, xlab, ylab, ymin=None, ymax=None, xticks=None, hline=None, vline=None):
    """series: list of (name, ys, color, dash)"""
    pw, ph = W - ML - MR, H - MT - MB - 18
    allv = [v for _, ys, _, _ in series for v in ys]
    lo = min(allv) if ymin is None else ymin
    hi = max(allv) if ymax is None else ymax
    ticks = _nice(lo, hi)
    lo, hi = ticks[0], ticks[-1]
    xlo, xhi = min(xs), max(xs)
    xmap = lambda x: ML + (x - xlo) / (xhi - xlo) * pw
    ymap = lambda y: MT + ph - (y - lo) / (hi - lo) * ph
    s = _frame(title, xlab, ylab, ticks, ymap, pw)
    for xt in (xticks or _nice(xlo, xhi, 6)):
        if xlo <= xt <= xhi:
            s.append(f'<text x="{xmap(xt):.1f}" y="{MT+ph+16}" font-size="11" text-anchor="middle" fill="#5b6572">{_fmt(xt)}</text>')
    if hline is not None:
        y = ymap(hline[0])
        s.append(f'<line x1="{ML}" x2="{ML+pw}" y1="{y:.1f}" y2="{y:.1f}" stroke="#1d2430" stroke-dasharray="4 4"/>')
        s.append(f'<text x="{ML+pw-4}" y="{y-6:.1f}" font-size="11" text-anchor="end" fill="#1d2430">{escape(hline[1])}</text>')
    if vline is not None:
        x = xmap(vline[0])
        s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{MT}" y2="{MT+ph}" stroke="#7a5bd1" stroke-dasharray="4 4"/>')
        s.append(f'<text x="{x+5:.1f}" y="{MT+12}" font-size="11" fill="#7a5bd1">{escape(vline[1])}</text>')
    for name, ys, col, dash in series:
        pts = " ".join(f"{xmap(x):.1f},{ymap(y):.1f}" for x, y in zip(xs, ys))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3" stroke-linejoin="round"{d}/>')
    _legend(s, [n for n, *_ in series], [c for _, _, c, _ in series], [d for *_, d in series])
    s.append("</svg>")
    return "\n".join(s)


def bar_chart(title, cats, series, xlab, ylab, ymin=None, ymax=None, labels=True):
    """series: list of (name, values, color). 묶음 막대."""
    pw, ph = W - ML - MR, H - MT - MB - 18
    allv = [v for _, vs, _ in series for v in vs] + [0]
    lo = min(allv) if ymin is None else ymin
    hi = max(allv) * 1.08 if ymax is None else ymax
    ticks = _nice(lo, hi)
    lo, hi = ticks[0], ticks[-1]
    ymap = lambda y: MT + ph - (y - lo) / (hi - lo) * ph
    s = _frame(title, xlab, ylab, ticks, ymap, pw)
    n, k = len(cats), len(series)
    gw = pw / n
    bw = min(46, gw * 0.75 / k)
    for i, c in enumerate(cats):
        cx = ML + gw * i + gw / 2
        s.append(f'<text x="{cx:.1f}" y="{MT+ph+16}" font-size="11.5" text-anchor="middle" fill="#3b4450">{escape(c)}</text>')
        for j, (name, vs, col) in enumerate(series):
            v = vs[i]
            x = cx - bw * k / 2 + j * bw
            y0, y1 = ymap(max(v, 0)), ymap(min(v, 0))
            s.append(f'<rect x="{x+1:.1f}" y="{y0:.1f}" width="{bw-2:.1f}" height="{max(y1-y0,0.5):.1f}" rx="3" fill="{col}"/>')
            if labels:
                ty = y0 - 5 if v >= 0 else y1 + 13
                s.append(f'<text x="{x+bw/2:.1f}" y="{ty:.1f}" font-size="10.5" text-anchor="middle" fill="#1d2430">{_fmt(v)}</text>')
    if lo < 0:
        s.append(f'<line x1="{ML}" x2="{ML+pw}" y1="{ymap(0):.1f}" y2="{ymap(0):.1f}" stroke="#1d2430"/>')
    if k > 1 or series[0][0]:
        _legend(s, [n for n, *_ in series], [c for *_, c in series])
    s.append("</svg>")
    return "\n".join(s)


def hbar_chart(title, cats, series, xlab):
    """가로 막대(퍼널용). series: list of (name, values, color)"""
    lw = 150
    pw = W - lw - MR - 40
    rowh = (H - MT - 70) / len(cats)
    hi = max(v for _, vs, _ in series for v in vs)
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(title)}" '
         f'font-family="Pretendard, Noto Sans KR, sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="20" y="26" font-size="16" font-weight="700" fill="#1d2430">{escape(title)}</text>',
         f'<text x="{W-MR}" y="26" font-size="11" text-anchor="end" fill="#8a93a0">모의 데이터(가상)</text>']
    k = len(series)
    bh = rowh * 0.8 / k
    for i, c in enumerate(cats):
        y = MT + rowh * i
        s.append(f'<text x="{lw-8}" y="{y+rowh/2+4:.1f}" font-size="12" text-anchor="end" fill="#3b4450">{escape(c)}</text>')
        for j, (name, vs, col) in enumerate(series):
            w = max(vs[i] / hi * pw, 1)
            yy = y + rowh * 0.1 + j * bh
            s.append(f'<rect x="{lw}" y="{yy:.1f}" width="{w:.1f}" height="{bh-2:.1f}" rx="3" fill="{col}"/>')
            s.append(f'<text x="{lw+w+5:.1f}" y="{yy+bh/2+3:.1f}" font-size="10.5" fill="#1d2430">{_fmt(vs[i])}</text>')
    s.append(f'<text x="{lw+pw/2}" y="{H-12}" font-size="12" text-anchor="middle" fill="#3b4450">{escape(xlab)}</text>')
    x = lw
    for name, _, col in series:
        s.append(f'<rect x="{x}" y="{H-44}" width="18" height="10" fill="{col}" rx="2"/>'
                 f'<text x="{x+24}" y="{H-35}" font-size="11.5" fill="#3b4450">{escape(name)}</text>')
        x += 40 + len(name) * 11.5
    s.append("</svg>")
    return "\n".join(s)
