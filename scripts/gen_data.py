"""장별 모의 데이터(가상) 생성 + SVG 차트 출력. 시드 고정으로 누구나 같은 결과를 재현할 수 있다."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from charts import line_chart, bar_chart, hbar_chart, PAL as P

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "charts")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(20261121)
NUM = {}


def save(name, svg):
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------- 서장: 전통 사기 vs AI 사기 하루 손익 (만원) ----------------
def day_pl(N, pi, g, c, p, f):
    succ = N * pi
    return dict(시도=N, 성공=succ, 수익=succ * g, 비용=N * c, 처벌기대=succ * p * f,
                순이익=succ * g - N * c - succ * p * f)

trad = day_pl(N=30, pi=0.004, g=500, c=2, p=0.25, f=3000)
ai = day_pl(N=3000, pi=0.003, g=300, c=0.03, p=0.03, f=3000)
NUM["ch0"] = {"trad": trad, "ai": ai}
save("ch0_daily_pl", bar_chart("X1의 하루 계산서: 전통 사기 vs AI 사기", ["기대 수익", "직접 비용", "처벌 기대비용", "순이익"],
     [("전통 수작업 사기", [trad["수익"], -trad["비용"], -trad["처벌기대"], trad["순이익"]], P["gray"]),
      ("AI 자동화 사기", [ai["수익"], -ai["비용"], -ai["처벌기대"], ai["순이익"]], P["crime"])],
     "항목", "만 원/일"))

# ---------------- 1장: 메시지 1만 건 퍼널 ----------------
def funnel(rates):
    n = 10000
    out = [n]
    for r in rates:
        n = rng.binomial(n, r)
        out.append(int(n))
    return out

gen = funnel([0.21, 0.15, 0.19, 0.15])
per = funnel([0.54, 0.27, 0.28, 0.22])
stages = ["발송", "열람", "링크 클릭", "정보 입력", "송금"]
NUM["ch1"] = {"generic": gen, "ai": per, "human_per_day": 8, "ai_per_day": 5000}
save("ch1_funnel", hbar_chart("메시지 1만 건이 송금까지 가는 길", stages,
     [("일반 대량 문자", gen, P["gray"]), ("AI 맞춤 메시지", per, P["crime"])], "단계별 인원(명)"))

# ---------------- 2장: 베커 모형 ----------------
Y = 3000  # 연 합법 소득(만원)
U = lambda w: math.log(max(w, 1))
def ce_gain(p, g, f):
    eu = p * U(Y - f) + (1 - p) * U(Y + g)
    return math.exp(eu) - Y  # 확실성 등가 - 합법 소득

ps = [i / 100 for i in range(0, 61)]
tr = [ce_gain(p, 2000, 2500) for p in ps]
aic = [ce_gain(p, 4000, 1500) for p in ps]
def breakeven(g, f):
    lo, hi = 0, 1
    for _ in range(60):
        m = (lo + hi) / 2
        if ce_gain(m, g, f) > 0:
            lo = m
        else:
            hi = m
    return lo
pt, pa = breakeven(2000, 2500), breakeven(4000, 1500)
NUM["ch2"] = {"p_star_trad": round(pt, 3), "p_star_ai": round(pa, 3)}
save("ch2_becker", line_chart("검거 확률 p가 오를 때 범죄의 매력(확실성 등가 기준)", ps,
     [("전통 범죄 (g=2,000 · f=2,500)", tr, P["gray"], None), ("AI 범죄 (g=4,000 · f=1,500)", aic, P["crime"], None)],
     "검거 확률 p", "합법 소득 대비 이득(만 원)", ymin=-2000, hline=(0, "손익분기선"), xticks=[0, .1, .2, .3, .4, .5, .6]))

# 예비 범죄자 1,000명: 소득 10분위별 참여율
n = 1000
inc = np.sort(rng.lognormal(mean=np.log(3000), sigma=0.55, size=n))
moral = rng.lognormal(mean=np.log(2000), sigma=1.0, size=n)
hours = 200  # 연간 투입 시간
def particip(pi, g, c, p, f, tcost):
    wage = inc / 2000  # 시간당 합법 임금(만원)
    opp = wage * hours * tcost
    gain = pi * g - c - p * f - opp - moral
    return gain > 0
pt_ = particip(0.40, 2500, 200, 0.20, 2000, 1.0)
pa_ = particip(0.45, 2200, 40, 0.08, 1500, 0.25)
dec = np.array_split(np.arange(n), 10)
rt = [float(pt_[d].mean() * 100) for d in dec]
ra = [float(pa_[d].mean() * 100) for d in dec]
NUM["ch2"].update({"part_trad": float(pt_.mean() * 100), "part_ai": float(pa_.mean() * 100),
                   "top3_trad": float(np.mean(rt[7:])), "top3_ai": float(np.mean(ra[7:]))})
save("ch2_participation", bar_chart("예비 범죄자 1,000명의 참여율: 소득 분위별", [f"{i+1}분위" for i in range(10)],
     [("전통 범죄", rt, P["gray"]), ("AI 범죄", ra, P["crime"])], "합법 소득 분위(1=낮음, 10=높음)", "범죄 참여율(%)", ymax=40, labels=False))

# ---------------- 3장: 생성자·판별자 경쟁 / 판별률 ----------------
r = np.arange(1, 31)
genq = 100 / (1 + np.exp(-(r - 12) / 4))
disc = 55 + 40 * np.exp(-r / 9) + 6 * np.sin(r / 2.2)
human = 50 + 45 * np.exp(-r / 7)
save("ch3_gan", line_chart("위조지폐범(생성자)과 형사(판별자)의 30라운드", r.tolist(),
     [("생성자 위조 품질 지수", genq.tolist(), P["crime"], None),
      ("판별자 탐지 정확도(%)", disc.tolist(), P["neutral"], None),
      ("사람 눈 판별 정확도(%)", human.tolist(), P["gray"], "6 4")],
     "학습 라운드", "지수 / 정확도(%)", ymin=0, ymax=100, hline=(50, "동전 던지기 수준(50%)")))

ages = ["20대", "30대", "40대", "50대", "60대 이상"]
base = [62, 59, 56, 53, 51]
sv = []
for b in base:
    k = rng.binomial(240, b / 100)
    sv.append(round(k / 240 * 100, 1))
rule = [round(rng.binomial(240, 0.9) / 240 * 100, 1) for _ in ages]
NUM["ch3"] = {"survey": sv, "rule": rule}
save("ch3_survey", bar_chart("가족 목소리 딥페이크, 귀로만 가려낼 수 있을까 (1,200명)", ages,
     [("귀로만 판별", sv, P["gray"]), ("가족 확인 질문 규칙 사용", rule, P["defense"])], "연령대", "정답률(%)", ymax=100))

# ---------------- 4장: 임직원 2,000명 모의 피싱 훈련 ----------------
months = list(range(1, 7))
def clickpath(start, decay, n=1000):
    out = []
    for m in months:
        rate = start * math.exp(-decay * (m - 1))
        out.append(round(rng.binomial(n, rate) / n * 100, 1))
    return out
gen_untr = clickpath(0.08, 0.0)
ai_untr = clickpath(0.27, 0.0)
ai_tr = clickpath(0.27, 0.27)
NUM["ch4"] = {"gen": gen_untr, "ai_untr": ai_untr, "ai_tr": ai_tr}
save("ch4_training", line_chart("임직원 2,000명 모의 피싱: 6개월 클릭률", months,
     [("일반 피싱 · 훈련 없음", gen_untr, P["gray"], "6 4"),
      ("AI 맞춤 피싱 · 훈련 없음", ai_untr, P["crime"], None),
      ("AI 맞춤 피싱 · 월 1회 시나리오 훈련", ai_tr, P["defense"], None)],
     "개월", "링크 클릭률(%)", ymin=0, ymax=35, xticks=months))

# 심리 요소별 클릭률
levers = ["권위", "긴급성", "호기심", "신뢰(지인)", "보상"]
lv = [round(rng.binomial(400, q) / 4, 1) for q in [0.22, 0.26, 0.17, 0.34, 0.14]]
NUM["ch4"]["levers"] = dict(zip(levers, lv))
save("ch4_levers", bar_chart("미끼의 심리 요소별 클릭률 (요소당 400명)", levers, [("", lv, P["crime2"])],
     "메시지에 쓴 심리 요소", "클릭률(%)", ymax=40))

# ---------------- 5장: 적응형 공격 vs 방어 ----------------
rounds = list(range(1, 21))
static = [83 * math.exp(-(k - 1) / 7) + 12 for k in rounds]
behav = [86 - 6 * (1 - math.exp(-(k - 1) / 5)) + rng.normal(0, 1.2) for k in rounds]
shared = [88 + 6 * (1 - math.exp(-(k - 1) / 6)) + rng.normal(0, 1.0) for k in rounds]
NUM["ch5"] = {"static_end": round(static[-1], 1), "behav_end": round(behav[-1], 1), "shared_end": round(shared[-1], 1)}
save("ch5_adaptive", line_chart("공격이 학습할 때 방어 차단율은 어떻게 변할까 (20라운드)", rounds,
     [("고정 규칙(시그니처) 필터", static, P["gray"], None),
      ("행위 기반 이상 탐지", behav, P["neutral"], None),
      ("행위 탐지 + 조직 간 위협 정보 공유", shared, P["defense"], None)],
     "공격 라운드(공격자가 매번 수법을 바꿈)", "차단율(%)", ymin=0, ymax=100, xticks=[1, 5, 10, 15, 20]))

# 로그인 5,000건 이상 탐지 (초파리)
normal_h = rng.normal(14, 2.5, 4900) % 24
attack_h = rng.normal(3.5, 1.2, 100) % 24
fail_n = np.concatenate([rng.poisson(0.3, 4900), rng.poisson(4.5, 100)])
hour = np.concatenate([normal_h, attack_h])
lab = np.concatenate([np.zeros(4900), np.ones(100)])
z = (np.abs(hour - 14) / 2.5) + fail_n / 1.2
pred = z > 4.0
tp = int(((pred == 1) & (lab == 1)).sum()); fp = int(((pred == 1) & (lab == 0)).sum())
fn = int(((pred == 0) & (lab == 1)).sum())
NUM["ch5"].update({"tp": tp, "fp": fp, "fn": fn, "recall": round(tp / 100 * 100, 1), "precision": round(tp / (tp + fp) * 100, 1)})

# ---------------- 6장: 10만 명 재식별 ----------------
import pandas as pd
N6 = 100000
df = pd.DataFrame({
    "시군구": rng.integers(0, 250, N6),
    "출생연도": rng.integers(1950, 2008, N6),
    "성별": rng.integers(0, 2, N6),
    "직업군": rng.choice(20, N6, p=np.array([.15, .12, .1, .08, .08, .07, .06, .05, .05, .04, .04, .03, .03, .02, .02, .02, .01, .01, .01, .01]) / 1.0),
    "출생월": rng.integers(1, 13, N6),
    "차종": rng.integers(0, 30, N6),
})
cols = ["시군구", "출생연도", "성별", "출생월", "직업군", "차종"]
uniq = []
for i in range(1, len(cols) + 1):
    g = df.groupby(cols[:i]).size()
    u = (g == 1).sum() / N6 * 100
    uniq.append(round(float(u), 1))
NUM["ch6"] = dict(zip(["+" + c for c in cols], uniq))
save("ch6_reident", bar_chart("10만 명 중 '세상에 나 하나뿐'인 사람의 비율", ["시군구", "+출생연도", "+성별", "+출생월", "+직업군", "+차종"],
     [("", uniq, P["violet"])], "공개 정보 조각을 하나씩 더할 때", "유일하게 특정되는 비율(%)", ymax=100))

# ---------------- 7장: 세탁 추적 / 랜섬 전략 ----------------
hops = list(range(0, 21))
manual = [100 * math.exp(-h / 4.5) for h in hops]
ml = [100 * (0.25 + 0.75 * math.exp(-h / 14)) for h in hops]
mix = [100 * (0.25 + 0.75 * math.exp(-h / 14)) * (0.45 if h >= 6 else 1) for h in hops]
NUM["ch7"] = {"manual10": round(manual[10], 1), "ml10": round(ml[10], 1), "mix10": round(mix[10], 1)}
save("ch7_trace", line_chart("쪼개고 옮길수록 추적 확률은 얼마나 떨어질까", hops,
     [("수작업 추적", manual, P["gray"], None), ("머신러닝 군집 분석 추적", ml, P["neutral"], None),
      ("머신러닝 추적 · 6번째 이동에서 믹서 경유", mix, P["crime"], "6 4")],
     "자금 이동 횟수(홉)", "출처까지 이어 갈 확률(%)", ymin=0, ymax=100, xticks=[0, 5, 10, 15, 20]))

A = dict(n=10, ransom=200000, pay=0.20, cost_per=30000)   # 만원 단위가 아니라 천원? -> 만원
B = dict(n=300, ransom=3000, pay=0.30, cost_per=150)
def rev(d):
    r_ = d["n"] * d["ransom"] * d["pay"] / 10000  # 억 원
    c_ = d["n"] * d["cost_per"] / 10000
    return round(r_, 1), round(c_, 1), round(r_ - c_, 1)
ra_, rb_ = rev(A), rev(B)
NUM["ch7"].update({"A": ra_, "B": rb_})
save("ch7_ransom", bar_chart("X2의 두 가지 영업 전략 (1년)", ["기대 몸값 수입", "운영 비용", "순이익"],
     [("대형 표적 10곳 · 건당 20억", list(ra_), P["gray"]), ("AI 자동화 300곳 · 건당 3,000만", list(rb_), P["crime"])],
     "항목", "억 원"))

# ---------------- 8장: 생활유형별 연간 기대손실 ----------------
personas = ["SNS 활동형", "온라인 금융형", "재택 비즈니스형"]
threats = {  # (연간 발생확률, 손실 만원)
    "SNS 활동형": [(0.06, 300), (0.03, 150), (0.02, 800)],
    "온라인 금융형": [(0.04, 1500), (0.05, 400), (0.02, 2500)],
    "재택 비즈니스형": [(0.05, 900), (0.03, 3000), (0.02, 1200)],
}
reduce = [0.25, 0.30, 0.35]  # 대책 적용 후 남는 비율
before = [round(sum(p * l for p, l in threats[k]), 1) for k in personas]
after = [round(sum(p * l * r for (p, l), r in zip(threats[k], reduce)), 1) for k in personas]
NUM["ch8"] = {"before": before, "after": after}
save("ch8_personas", bar_chart("생활유형별 연간 기대손실: 방패 전과 후", personas,
     [("방패 전", before, P["crime2"]), ("기본 방패 5종 적용 후", after, P["defense"])], "생활유형", "연간 기대손실(만 원)"))

# ---------------- 9장: 집단 면역 시뮬레이션 ----------------
def ba_graph(n, m, seed):
    rr = np.random.default_rng(seed)
    edges = [(i, j) for i in range(m) for j in range(i)]
    deg = [m - 1] * m
    adj = [set(j for j in range(m) if j != i) for i in range(m)]
    for v in range(m, n):
        tot = sum(deg)
        targets = set()
        while len(targets) < m:
            targets.add(int(rr.choice(len(deg), p=np.array(deg) / tot)))
        adj.append(set())
        deg.append(0)
        for t in targets:
            adj[v].add(t); adj[t].add(v); deg[t] += 1; deg[v] += 1
    return adj
G = ba_graph(500, 3, 7)
def spread(secure_rate, beta, runs=30):
    res = []
    for k in range(runs):
        rr = np.random.default_rng(1000 + k)
        secure = rr.random(500) < secure_rate
        infected = {int(rr.integers(500))}
        frontier = list(infected)
        while frontier:
            nf = []
            for u in frontier:
                for v in G[u]:
                    if v in infected:
                        continue
                    b = beta * (0.08 if secure[v] else 1.0)
                    if rr.random() < b:
                        infected.add(v); nf.append(v)
            frontier = nf
        res.append(len(infected) / 5)
    return float(np.mean(res))
rates = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9]
s_alone = [spread(x, 0.30) for x in rates]
s_share = [spread(x, 0.18) for x in rates]
NUM["ch9"] = {"alone": [round(v, 1) for v in s_alone], "share": [round(v, 1) for v in s_share]}
save("ch9_herd", line_chart("기업 500곳 연결망: 보안을 갖춘 기업 비율과 피해 확산", [int(x * 100) for x in rates],
     [("각자 방어", s_alone, P["crime"], None), ("위협 정보 공유(전파력 40% 감소)", s_share, P["defense"], None)],
     "기본 보안을 갖춘 기업 비율(%)", "최종 피해 기업 비율(%)", ymin=0, ymax=100, xticks=[0, 20, 40, 60, 80, 90]))

# ---------------- 10장: 탐지 지연 vs 손실 / 계산서 뒤집기 ----------------
days = list(range(0, 61))
loss_full = [10 / (1 + math.exp(-(d - 20) / 5)) for d in days]  # 억 원
NUM["ch10"] = {"d1": round(loss_full[1], 2), "d7": round(loss_full[7], 2), "d30": round(loss_full[30], 2)}
save("ch10_dwell", line_chart("침입을 알아차리기까지 걸린 날과 피해액", days,
     [("백업 없음", loss_full, P["crime"], None), ("분리 백업 + 복구 훈련", [v * 0.35 for v in loss_full], P["defense"], None)],
     "탐지까지 걸린 날", "누적 피해액(억 원)", ymin=0, ymax=10, xticks=[0, 7, 14, 30, 45, 60], vline=(3, "골든타임 3일")))

base_profit = ai["순이익"]
steps = [("AI 사기 기본", 0)]
pi_, p_, g_, N_ = 0.003, 0.03, 300, 3000
def prof(pi, p, g, N, c=0.03, f=3000):
    s = N * pi
    return s * g - N * c - s * p * f
vals = [prof(pi_, p_, g_, N_)]
labels = ["AI 사기 기본값"]
for lab_, kw in [("속도 제한·이상 탐지", dict(N=900)), ("별도 채널 확인 습관", dict(pi=0.0012)),
                 ("피싱 내성 인증·패스키", dict(pi=0.0006)), ("지급정지·출금 지연", dict(g=120)),
                 ("국제 공조·위협 정보 공유", dict(p=0.06))]:
    pi_ = kw.get("pi", pi_); p_ = kw.get("p", p_); g_ = kw.get("g", g_); N_ = kw.get("N", N_)
    vals.append(prof(pi_, p_, g_, N_)); labels.append("+" + lab_)
NUM["ch10"]["flip"] = [round(v, 1) for v in vals]
save("ch10_flip", bar_chart("X1의 하루 순이익: 방어를 하나씩 더할 때", ["기본", "+속도 제한", "+확인 습관", "+패스키", "+지급정지", "+국제 공조"],
     [("", [round(v, 1) for v in vals], P["crime"])], "누적 대응", "순이익(만 원/일)"))

with open(os.path.join(OUT, "numbers.json"), "w", encoding="utf-8") as f:
    json.dump(NUM, f, ensure_ascii=False, indent=1, default=float)
print(json.dumps(NUM, ensure_ascii=False, indent=1, default=float))
