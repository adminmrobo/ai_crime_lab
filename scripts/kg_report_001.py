"""리포트 검증 No.001 — 지식 색인(kg.json)·참고문헌(refs.json)·페이지 정보(meta.json)를 만든다."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "reports" / "2026-11-23_lnrs-synthetic-identity-deepfake" / "kg"
PAGE = "r001_lnrs-synthetic-identity-deepfake"
AS = "2026-11-23"
nodes, edges = [], []


def N(id_, type_, ko, en, anchor, level=2, conf="high", cov="explained", family=None, defi=None, src=None, asOf=None, **kw):
    n = {"id": id_, "type": type_, "label": {"ko": ko, "en": en}, "page": PAGE, "anchor": anchor, "level": level,
         "status": "known", "confidence": conf, "coverage": cov, "match": [], "domain": ["econ", "ai"]}
    if family: n["family"] = family
    if defi: n["definition"] = {"ko": defi}
    if src: n["source"] = [{"ref": r, "loc": l} for r, l in src]
    if asOf: n["asOf"] = asOf
    n.update(kw)
    nodes.append(n)
    return id_


def E(s, p, o, anchor, conf="high"):
    edges.append({"s": s, "p": "lab:" + p, "o": o, "anchor": anchor, "confidence": conf})


# ── 개념·방법 ──
syn = N("lab:concept/synthetic-identity", "Concept", "합성 신원", "Synthetic identity", "#sec-2", 1, family="responsible",
        defi="진짜 정보 조각과 꾸민 정보를 섞어 만든, 실제로는 없는 사람의 신원", altLabel={"ko": ["만들어진 신원", "프랑켄슈타인 신원"]})
tit = N("lab:concept/true-identity-theft", "Concept", "실제 신원 도용", "True identity theft", "#sec-2", 1, family="responsible",
        defi="실제 사람의 신원·계정을 훔쳐 그 사람인 척하는 사기")
fpf = N("lab:concept/first-party-fraud", "Concept", "제1자 사기", "First-party fraud", "#sec-4", 1, family="responsible",
        defi="고객이 자기 이름으로 기관을 속이는 사기")
sca = N("lab:concept/scalable-identity", "Concept", "규모(대량 생산)", "Scalable", "#sec-3-1", 2, family="responsible",
        defi="신원을 공장처럼 만들고 시험·반복한다")
ada = N("lab:concept/adaptive-identity", "Concept", "적응(심사 통과 학습)", "Adaptive", "#sec-3-1", 2, family="responsible",
        defi="가입 심사를 통과할 때까지 시험하고 다듬는다")
pat = N("lab:concept/patient-identity", "Concept", "인내(숙성 후 현금화)", "Patient", "#sec-3-1", 2, family="responsible",
        defi="바로 쓰지 않고 오래 키운 뒤 돈으로 바꾼다")
farm = N("lab:concept/synthetic-farm", "Concept", "합성 농장·합성 주택", "Synthetic farm / synthetic house", "#fig-4-2", 3,
         family="responsible", defi="한 주소에 비정상적으로 많은 신원과 신용 흔적이 연결된 곳")
dfk = N("lab:concept/deepfake", "Concept", "딥페이크", "Deepfake", "#sec-3-3", 1, family="generative",
        defi="AI로 만든 가짜 얼굴·목소리·영상", cov="mentioned")
inj = N("lab:concept/injection-replay-attack", "Concept", "주입·재생 공격", "Injection and replay attacks", "#q-real", 3,
        family="responsible", defi="미리 만든 영상을 넣거나 녹화본을 다시 틀어 생체 확인을 속이는 방식", cov="mentioned")
pol = N("lab:concept/proof-of-life", "Concept", "생활 흔적(proof of life)", "Proof of life", "#sec-3-3", 3, family="responsible",
        defi="실제 사람이 오래 살아온 흔적을 뒷받침하는 폭넓은 기록")
noise = N("lab:indicator/zero-noise", "Indicator", "잡음 없음 신호", "Zero-noise signal", "#sec-3-3", 3, family="unsupervised",
          defi="기록이 지나치게 깨끗하거나 짧은 기간에 몰려 있는 상태")
denom = N("lab:concept/denominator", "Concept", "비율의 분모", "Denominator of a rate", "#memo-4", 1, family="math",
          defi="비율을 계산할 때 기준이 되는 전체 집단")

pit = N("lab:method/point-in-time-verification", "Method", "시점 검증", "Point-in-time verification", "#fig-2-1", 2,
        family="systems", defi="가입 같은 한 순간에만 신원을 확인하는 방식")
lct = N("lab:method/lifecycle-trust", "Method", "생애주기 신뢰 모형", "Lifecycle identity trust model", "#sec-3-3", 3,
        family="systems", defi="가입 뒤에도 신호를 모아 시점마다 신원의 위험을 다시 판단하는 틀")
orc = N("lab:method/orchestration", "Method", "오케스트레이션", "Orchestration", "#sec-3-3", 3, family="systems",
        defi="여러 확인 도구의 신호를 순서대로 엮어 하나의 판단으로 모으는 일")
stp = N("lab:method/step-up", "Method", "단계별 추가 확인", "Adaptive step-up", "#q-risk", 2, family="systems",
        defi="위험이 높을 때만 확인 절차를 하나 더 거치게 하는 방식")
liv = N("lab:method/liveness-check", "Method", "라이브니스 검사", "Liveness check", "#q-real", 2, family="responsible",
        defi="카메라 앞에 실제 살아 있는 사람이 있는지 확인하는 검사", cov="mentioned")
q1 = N("lab:concept/is-identity-real", "Concept", "질문 1 진짜 신원인가", "Is the identity real?", "#q-real", 2, family="systems")
q2 = N("lab:concept/is-identity-trusted", "Concept", "질문 2 믿을 만한 신원인가", "Is the identity trusted?", "#q-trust", 2, family="systems")
q3 = N("lab:concept/risk-now-and-over-time", "Concept", "질문 3 지금·앞으로의 위험", "Risk now and over time", "#q-risk", 2, family="systems")

lim1 = N("lab:limitation/onboarding-blind-spot", "Limitation", "가입 순간의 사각지대", "Onboarding blind spot", "#sec-3-2", 2,
         family="systems", defi="깨끗해 보이도록 설계된 신원은 한 시점 검사로 드러나지 않는다")
lim2 = N("lab:limitation/tool-seams", "Limitation", "도구 사이 이음새", "Seams between tools", "#sec-3-2", 2, family="systems",
         defi="문서·기기·행동·연결망 도구가 따로 돌면 빈틈이 생긴다")
lim3 = N("lab:limitation/human-deepfake-detection", "Limitation", "사람 눈의 딥페이크 판별 한계", "Limits of human deepfake detection",
         "#tbl-4-1", 2, family="generative")

# 책의 계산서 기호
eu = N("lab:concept/expected-utility-crime", "Concept", "범죄의 기대효용 E(U)", "Expected utility of crime", "#sec-6-2", 2,
       family="math", defi="잡힐 때의 손해와 안 잡힐 때의 이익을 확률로 가중 평균한 값(책 2장)")
pp = N("lab:concept/arrest-probability", "Concept", "검거 확률 p", "Probability of apprehension p", "#sec-6-2", 2, family="math")
gg = N("lab:concept/crime-gain", "Concept", "성공 시 이익 g", "Gain from crime g", "#sec-6-2", 2, family="math")
pi = N("lab:concept/success-probability", "Concept", "성공 확률 π", "Success probability π", "#tbl-6-2", 2, family="math")
cc = N("lab:concept/crime-unit-cost", "Concept", "건당 비용 c", "Unit cost of crime c", "#tbl-6-2", 2, family="math")
ana = N("lab:analogy/empty-house-nameplate", "Analogy", "빈집의 문패", "Nameplate on an empty house", "#sec-2", 1,
        defi="아무도 살지 않는 집에 문패를 달고 우편물을 받아 사는 집처럼 만드는 일")

# ── 지표 ──
i_syn = N("lab:indicator/synthetic-share", "Indicator", "합성 신원 사기 비중", "Share of synthetic identity fraud", "#fig-4-1", 2, family="evaluation")
i_tit = N("lab:indicator/true-identity-share", "Indicator", "실제 신원 도용 비중", "Share of true identity theft", "#fig-4-1", 2, family="evaluation")
i_fpf = N("lab:indicator/first-party-share", "Indicator", "제1자 사기 비중", "Share of first-party fraud", "#fig-4-1", 2, family="evaluation")
i_nac = N("lab:indicator/new-account-attack-rate", "Indicator", "가입 시도 중 공격 비율", "Attack rate at new account creation", "#sec-3-2", 2, family="evaluation")

# ── 출처 있는 사실 (Claim) ──
R = "lnrs2026stopping"
c_syn = N("lab:claim/synthetic-share-11pct-2025", "Claim", "2025년 합성 신원은 전체 보고 사기의 11%", "Synthetic identity was 11% of reported fraud in 2025",
          "#fig-4-1", 2, src=[("lnrs2026synthetic", ""), ("lexisnexis2026synthetic", ""), (R, "p.2")], asOf="2026-03-26")
c_syn0 = N("lab:claim/synthetic-share-1-4pct-2024", "Claim", "2024년 합성 신원은 전체 보고 사기의 1.4%", "Synthetic identity was 1.4% in 2024",
           "#fig-4-1", 2, src=[("lnrs2026synthetic", "")], asOf="2026-03-26")
c_tit = N("lab:claim/true-identity-6-4pct-2025", "Claim", "실제 신원 도용은 9.9%에서 6.4%로 감소", "True identity theft fell from 9.9% to 6.4%",
          "#fig-4-1", 2, src=[("lnrs2026synthetic", "")], asOf="2026-03-26")
c_fpf = N("lab:claim/first-party-38pct-2025", "Claim", "제1자 사기 38.3%로 2년 연속 최다", "First-party fraud 38.3%, most reported",
          "#fig-4-1", 2, src=[("ads2026lexisnexis", ""), ("lexisnexis2026top", "")], asOf="2026-03-31")
c_nac = N("lab:claim/new-account-1-in-11", "Claim", "새 계정 개설 11건 중 1건이 공격", "1 in 11 new account creations were attacks",
          "#sec-3-2", 2, src=[(R, "p.4"), ("lexisnexis2026top", "")], asOf="2026-03-26")
c_noalarm = N("lab:claim/no-victim-alarm", "Claim", "합성 사기는 피해자가 바로 경보를 울리지 않아 범죄자에게 매력적", "No victim raises the alarm",
              "#sec-2", 2, src=[("ads2026lexisnexis", "")], asOf="2026-03-31")
c_gen = N("lab:claim/genai-85pct-identity-fraud", "Claim", "신원 사기의 85%에 생성형 AI 도구가 쓰임(전자책 인용)", "85% of identity fraud cases leverage genAI (as cited)",
          "#tbl-4-1", 3, conf="medium", src=[(R, "p.4"), ("dhs2024impact", "")], asOf="2026-07-13")
c_57a = N("lab:claim/ai-forgeries-57pct-attacks", "Claim", "AI 생성 위조가 2024년 공격의 57%에 관여(전자책 표현)", "AI-generated forgeries in 57% of attacks (ebook wording)",
          "#chk-1", 3, conf="medium", src=[(R, "p.5")], asOf="2026-07-13")
c_57b = N("lab:claim/digital-forgeries-57pct-docs", "Claim", "2024년 문서 위조 중 디지털 위조가 57%", "Digital forgeries were 57% of document fraud in 2024",
          "#chk-1", 3, src=[("entrust2024deepfake", "")], asOf="2024-11-19")
c_hum = N("lab:claim/human-detect-deepfake-20pct", "Claim", "사람이 딥페이크를 맞게 알아보는 비율 약 20%", "People detect deepfakes ~20% of the time",
          "#tbl-4-1", 3, conf="medium", src=[(R, "p.5"), ("lexisnexis2026unmask", "")], asOf="2026-07-13")
c_85 = N("lab:claim/synthetic-85pct-unflagged", "Claim", "합성 신원의 85%가 다른 회사 모형에 걸리지 않음", "85% of synthetic identities not flagged by third-party models",
         "#tbl-4-1", 3, conf="medium", src=[(R, "p.7")], asOf="2026-07-13")
c_650 = N("lab:claim/synthetic-credit-650", "Claim", "합성 신원의 50% 이상이 신용 점수 650점 이상", "Over 50% had credit scores above 650",
          "#tbl-4-1", 3, conf="medium", src=[(R, "p.7")], asOf="2026-07-13")
c_lon = N("lab:claim/london-1653-identities", "Claim", "런던 한 주소에 1,653명, 정부 자료 확인 10명", "London address linked to 1,653 identities, 10 validated",
          "#fig-4-2", 3, src=[(R, "p.10")], asOf="2026-07-13")
c_chi = N("lab:claim/chichester-439-entities", "Claim", "치체스터 농장 1곳에 7년간 439명, 실제 흔적 22명", "Chichester farm: 439 entities over 7 years, 22 real",
          "#fig-4-2", 3, src=[(R, "p.10"), ("yahoo2024three", "")], asOf="2026-07-13")
c_oxf = N("lab:claim/oxford-9-properties", "Claim", "옥스퍼드 주택 9곳에 150명 이상·신용 기록 450건 이상", "Oxford 9-property network 150+ entities",
          "#fig-4-2", 3, src=[(R, "p.10")], asOf="2026-07-13")
c_uk = N("lab:claim/uk-2-8m-synthetic-profiles", "Claim", "영국 소비자 프로필 7,200만 건 중 280만 건에 합성 징후, 2027년 42억 파운드 추정",
         "2.8m of 72m UK profiles show synthetic signs; £4.2bn by 2027", "#tl-2024-06-12", 3,
         src=[("lexisnexis2024synthetics", ""), ("finextra2024uk", "")], asOf="2024-06-12")
c_400 = N("lab:claim/deepfakes-prevented-400k-2025", "Claim", "2025년 자사 서비스가 딥페이크 시도 약 40만 건 차단(하루 약 1,100건)",
          "~400,000 deepfake attempts prevented in 2025", "#sec-3-4", 3, conf="medium", src=[(R, "p.11")], asOf="2026-07-13")
c_53 = N("lab:claim/onboarding-pass-rate-5-3pct", "Claim", "한 금융회사의 가입 확인 통과율 5.3% 상승", "5.3% increase in verification pass rates",
         "#sec-3-4", 3, conf="medium", src=[(R, "p.11")], asOf="2026-07-13")
c_fn = N("lab:claim/ebook-footnote-mismatch", "Claim", "전자책 각주 4·5번이 본문의 보고서 이름과 어긋남", "Footnotes 4 and 5 appear swapped",
         "#chk-2", 3, conf="medium", src=[(R, "p.7, p.11, p.12")], asOf=AS)

# 입장
p_lc = N("lab:claim/position-lifecycle-monitoring", "Claim", "입장: 신호를 계속 모아 위험할 때만 확인을 더한다", "Position: continuous, risk-based trust",
         "#pos-lifecycle", 3, src=[(R, "p.8-9")], asOf="2026-07-13")
p_ne = N("lab:claim/position-biometric-necessity", "Claim", "입장: 생체 정보 처리는 덜 침해적인 대안이 없을 때만 필요", "Position: biometric processing only when necessary",
         "#pos-necessity", 3, conf="medium", src=[("scmedia2026spain", "")], asOf=AS)

# 책 대조 (Claim, 출처는 책)
B = "ahn2025aicrime"
m1 = N("lab:claim/book-ch10-synthetic-future-threat", "Claim", "책 10장: 합성 신원을 새로운 위협 목록에 둠", "Book ch.10 lists synthetic identity as an emerging threat",
       "#m-1", 2, src=[(B, "10장 §1")], asOf="2025-10-10")
m4 = N("lab:claim/book-ch05-rule-filter-decay", "Claim", "책 5장(모의): 고정 규칙 필터 95%→17.5%, 행위 탐지 82.2%", "Book ch.5 (simulated): rule filter decays",
       "#m-4", 2, conf="medium", src=[(B, "5장 §2")], asOf="2025-10-10")
m5 = N("lab:claim/book-ch03-procedure-over-ear", "Claim", "책 3장(모의): 귀 판별 52.9~63.7%, 확인 질문 약 90%", "Book ch.3 (simulated): procedure beats the ear",
       "#m-5", 2, conf="medium", src=[(B, "3장 §4")], asOf="2025-10-10")
m7 = N("lab:claim/book-ch10-five-layers", "Claim", "책 8·10장: 하나의 대응으로는 계산서를 뒤집지 못한다(다층 방어)", "Book ch.8/10: layered defence",
       "#m-7", 2, src=[(B, "8장 §1, 10장 §3")], asOf="2025-10-10")
m11 = N("lab:claim/book-ch08-lock-identity", "Claim", "책 8장: 비대면 계좌개설 안심차단 등 개인의 명의 잠금", "Book ch.8: personal identity locks",
        "#m-11", 2, src=[(B, "8장 §4")], asOf="2025-10-10")

# 질문
u1 = N("lab:question/korea-synthetic-scale", "Question", "한국 비대면 계좌의 합성 신원 규모는?", "Scale of synthetic identity in Korea?", "#unk-1", 3, conf="low")
u2 = N("lab:question/classification-effect", "Question", "11% 증가 중 분류 변경의 몫은?", "How much of the rise is reclassification?", "#unk-2", 3, conf="low")
u3 = N("lab:question/human-detection-conditions", "Question", "사람 판별 20%의 매체·조건은?", "Conditions behind the 20% figure?", "#unk-3", 3, conf="low")
u4 = N("lab:question/monitoring-cost", "Question", "지속 감시가 정상 고객에게 주는 비용은?", "Cost of continuous monitoring to genuine customers?", "#unk-4", 3, conf="low")
qz = N("lab:quiz/r001-sec7-1", "QuizItem", "11건 중 1건과 11%의 분모 구분", "Distinguish the two 11s", "#quiz-7-1", 1)

# ── Work (참고문헌) ──
REFS = [
    ("lnrs2026stopping", "report", "Stopping Synthetic Identity and Deepfake Fraud", "LexisNexis Risk Solutions", 2026, "primary",
     "https://risk.lexisnexis.com/global/en/insights-resources/e-book/stopping-synthetic-identity-and-deepfake-fraud-ebook", "사용자 제공 PDF 원문 대조 및 공식 소개 페이지 확인, 2026-11-23 접속"),
    ("lnrs2026synthetic", "webpage", "The Synthetic Identity Problem Is Getting Harder to Ignore", "LexisNexis Risk Solutions", 2026, "data",
     "https://lexisnexisrisk.com/en/business-services/insights-resources/synthetic-identity-theft-global-fraud-problem", "웹 원문 확인, 2026-11-23 접속"),
    ("lexisnexis2026synthetic", "webpage", "Synthetic Identities and Agentic Bots Posing as Human Contribute to 8% Global Rise in Fraud Attacks",
     "LexisNexis Risk Solutions", 2026, "primary",
     "https://risk.lexisnexis.com/global/en/about-us/press-room/press-release/20260326-ccr-global-fraud", "보도자료 검색 결과 확인(2026-03-26), 2026-11-23 접속"),
    ("ads2026lexisnexis", "webpage", "LexisNexis Risk Solutions releases Cybercrime Report", "ADS Group", 2026, "background",
     "https://www.adsgroup.org.uk/knowledge/industry-member-news/lexisnexis-risk-solutions-releases-cybercrime-report/", "웹 검색 결과 원문 확인, 2026-11-23 접속"),
    ("lexisnexis2024synthetics", "webpage", "UK synthetic identity research press release", "LexisNexis Risk Solutions UK", 2024, "data",
     "https://risk.lexisnexis.co.uk/about-us/press-room/press-release/20240612-synthetics", "보도자료 검색 결과 확인(2024-06-12), 2026-11-23 접속"),
    ("finextra2024uk", "article-newspaper", "UK home to 3m 'Frankenstein' identities, posing multi-billion pound threat", "Finextra", 2024, "background",
     "https://finextra.com/newsarticle/44296/uk-home-to-3m-frankenstein-identities-posing-multi-billion-pound-threat", "웹 검색 결과 확인, 2026-11-23 접속"),
    ("yahoo2024three", "article-newspaper", "Three million 'Frankenstein' identities pose a multi-billion pound fraud threat", "Yahoo Finance", 2024, "background",
     "https://au.finance.yahoo.com/news/three-million-frankenstein-identities-pose-080000206.html", "웹 검색 결과 확인, 2026-11-23 접속"),
    ("dhs2024impact", "report", "Impact of Artificial Intelligence (AI) on Criminal and Illicit Activities", "U.S. Department of Homeland Security", 2024, "background",
     "https://dhs.gov/sites/default/files/2024-10/24_0927_ia_aep-impact-ai-on-criminal-and-illicit-activities.pdf", "PDF 존재·제목 확인(85% 수치 위치는 미대조), 2026-11-23 접속"),
    ("entrust2024deepfake", "webpage", "Deepfake Attacks Strike Every Five Minutes Amid 244% Surge in Digital Document Forgeries", "Entrust", 2024, "data",
     "https://www.entrust.com/es/company/newsroom/deepfake-attacks-strike-every-five-minutes", "보도자료 원문 확인(2024-11-19), 2026-11-23 접속"),
    ("lexisnexis2026top", "report", "2026 Top Fraud Trends (infographic)", "LexisNexis Risk Solutions", 2026, "data",
     "https://risk.lexisnexis.com/-/media/files/government/infographics/ln%202026%20top%20fraud%20trends%20infographic%20w%20pdf.pdf", "PDF 검색 결과 확인, 2026-11-23 접속"),
    ("lexisnexis2026unmask", "webpage", "Unmask Deepfakes and Forged Documents with the Power of AI", "LexisNexis Risk Solutions", 2026, "background",
     "https://risk.lexisnexis.com/global/en/insights-resources/white-paper/unmask-deepfakes-with-the-power-of-ai", "소개 페이지 확인(85%·20% 표기), 2026-11-23 접속"),
    ("scmedia2026spain", "article-newspaper", "Spain's data protection regulator clarifies biometric risk and necessity", "SC Media", 2026, "background",
     "https://www.scworld.com/brief/spains-data-protection-regulator-clarifies-biometric-risk-and-necessity", "웹 검색 결과 확인(게시일 미확인), 2026-11-23 접속"),
    ("ahn2025aicrime", "book", "AI 범죄와 자기 방어", "안상선", 2025, "background",
     "https://adminmrobo.github.io/ai_crime_lab/", "저자 본인 책과 이 저장소의 장별 원고(content/*.md) 대조, 2026-11-23"),
]
work = {}
refs = []
for rid, typ, title, auth, yr, role, url, chk in REFS:
    wid = "lab:work/" + rid
    work[rid] = wid
    N(wid, "Work", f"{auth} ({yr}) {title}"[:120], title[:120], "#refs", 3, cov="mentioned")
    refs.append({"id": rid, "type": typ, "title": title, "author": [{"literal": auth}], "issued": {"date-parts": [[yr]]},
                 "URL": url, "accessed": {"date-parts": [[2026, 11, 23]]},
                 "lab": {"work": wid, "role": role, "supports": [], "locs": [],
                         "verified": {"title": True, "author": True, "year": True, "container": False, "pages": False, "doi": False},
                         "checkedBy": chk, "checkedSource": "web"}})
# Claim → assertedIn
for n in nodes:
    if n["type"] == "Claim":
        for s in n["source"]:
            E(n["id"], "assertedIn", work[s["ref"]], n["anchor"])
            for r in refs:
                if r["id"] == s["ref"]: r["lab"]["supports"].append(n["id"])

# ── 관계 ──
for x in (syn, tit, fpf, farm, inj, pol, liv): E(x, "broader", "lab:topic/ai-safety", "#sec-2")
E(syn, "broader", "lab:topic/privacy", "#sec-2"); E(tit, "broader", "lab:topic/privacy", "#sec-2")
E(dfk, "broader", "lab:topic/gan", "#sec-3-3"); E(lim3, "broader", "lab:topic/gan", "#tbl-4-1")
E(noise, "broader", "lab:topic/anomaly-detection", "#sec-3-3")
for x in (pit, lct, orc, stp, lim1, lim2, q1, q2, q3): E(x, "broader", "lab:topic/monitoring", "#sec-3-3")
for x in (sca, ada, pat): E(x, "partOf", syn, "#sec-3-1"); E(x, "broader", "lab:topic/ai-safety", "#sec-3-1")
E(denom, "broader", "lab:topic/probability-statistics", "#memo-4")
for x in (eu, pp, gg, pi, cc): E(x, "broader", "lab:topic/probability-statistics", "#sec-6-2")
E(syn, "contrastsWith", tit, "#sec-2"); E(ana, "analogyOf", syn, "#sec-2"); E(farm, "partOf", syn, "#fig-4-2")
E(dfk, "relatedTo", syn, "#sec-3-3"); E(inj, "relatedTo", dfk, "#q-real")
E(pit, "hasLimitation", lim1, "#sec-3-2"); E(lim1, "addressedBy", lct, "#sec-3-3")
E(lim2, "addressedBy", orc, "#sec-3-3"); E(lct, "contrastsWith", pit, "#fig-2-1")
E(q1, "partOf", lct, "#q-real"); E(q2, "partOf", lct, "#q-trust"); E(q3, "partOf", lct, "#q-risk")
E(q1, "prerequisiteOf", q2, "#sec-3-3"); E(q2, "prerequisiteOf", q3, "#sec-3-3")
E(liv, "partOf", q1, "#q-real"); E(liv, "hasLimitation", lim3, "#tbl-4-1"); E(stp, "partOf", q3, "#q-risk")
E(noise, "partOf", q2, "#sec-3-3"); E(pol, "partOf", q2, "#sec-3-3"); E(orc, "partOf", lct, "#sec-3-3")
E(syn, "measuredBy", i_syn, "#fig-4-1"); E(tit, "measuredBy", i_tit, "#fig-4-1"); E(fpf, "measuredBy", i_fpf, "#fig-4-1")
E(lim1, "measuredBy", i_nac, "#sec-3-2")
E(c_syn, "supports", i_syn, "#fig-4-1"); E(c_syn0, "supersededBy", c_syn, "#fig-4-1"); E(c_syn0, "supports", i_syn, "#fig-4-1")
E(c_tit, "supports", i_tit, "#fig-4-1"); E(c_fpf, "supports", i_fpf, "#fig-4-1"); E(c_nac, "supports", i_nac, "#sec-3-2")
E(c_noalarm, "supports", pp, "#sec-2"); E(c_gen, "supports", dfk, "#tbl-4-1"); E(c_hum, "supports", lim3, "#tbl-4-1")
E(c_57a, "contrastsWith", c_57b, "#chk-1"); E(c_57a, "supports", dfk, "#tbl-4-1"); E(c_57b, "supports", dfk, "#chk-1")
E(c_85, "supports", lim1, "#tbl-4-1"); E(c_650, "supports", lim1, "#tbl-4-1")
for c in (c_lon, c_chi, c_oxf): E(c, "supports", farm, "#fig-4-2")
E(c_uk, "supports", syn, "#tl-2024-06-12"); E(c_400, "supports", liv, "#sec-3-4"); E(c_53, "supports", orc, "#sec-3-4")
E(c_fn, "raises", u3, "#chk-2")
E(p_lc, "supports", lct, "#pos-lifecycle"); E(p_lc, "contrastsWith", p_ne, "#tbl-5-1")
E(pp, "partOf", eu, "#sec-6-2"); E(gg, "partOf", eu, "#sec-6-2"); E(pi, "partOf", eu, "#tbl-6-2"); E(cc, "partOf", eu, "#tbl-6-2")
E(pat, "relatedTo", gg, "#tbl-6-2"); E(sca, "relatedTo", cc, "#tbl-6-2"); E(lct, "relatedTo", pi, "#tbl-6-2")
E(m1, "supports", syn, "#m-1"); E(m1, "contrastsWith", c_syn, "#m-1")
E(m4, "supports", lim1, "#m-4"); E(m5, "supports", lim3, "#m-5"); E(m5, "contrastsWith", c_hum, "#m-5")
E(m7, "supports", orc, "#m-7"); E(m11, "contrastsWith", p_lc, "#m-11")
E(syn, "raises", u1, "#unk-1"); E(i_syn, "raises", u2, "#unk-2"); E(lim3, "raises", u3, "#unk-3"); E(lct, "raises", u4, "#unk-4")
E(qz, "assesses", denom, "#quiz-7-1"); E(denom, "prerequisiteOf", i_nac, "#memo-4"); E(denom, "prerequisiteOf", i_syn, "#memo-4")

kg = {"version": "1.0", "page": PAGE, "nodes": nodes, "edges": edges}
meta = {"title": "만들어진 신원과 딥페이크 사기 — LexisNexis 보고서를 책으로 읽기", "number": "R001",
        "series": "AI 범죄 연구실 · 리포트·뉴스 검증", "about": [syn, lct, orc, eu, lim1],
        "basedOn": ["lnrs2026stopping", "ahn2025aicrime"], "educationalLevel": "입문",
        "creator": [{"name": "안상선", "role": "author"}], "contributor": [{"name": "AI 보조 제작", "role": "assistant"}],
        "date": AS, "version": "1.0", "language": ["ko"], "license": "",
        "url": "https://adminmrobo.github.io/ai_crime_lab/reports/2026-11-23_lnrs-synthetic-identity-deepfake/",
        "registry": "KG_00_registry 0.2", "learningResourceType": "news report", "seeAlso": "",
        "suggestedCitation": "안상선 (2026). 만들어진 신원과 딥페이크 사기 — LexisNexis 보고서를 책으로 읽기. AI 범죄 연구실 리포트·뉴스 검증 R001, v1.0."}
for name, obj in (("kg.json", kg), ("refs.json", refs), ("meta.json", meta)):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
print("nodes", len(nodes), "edges", len(edges), "refs", len(refs),
      "relatedTo %.1f%%" % (100 * sum(e["p"] == "lab:relatedTo" for e in edges) / len(edges)))
