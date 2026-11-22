"""AI 범죄학 분야(crime) 온톨로지 — 책 11개 장의 개념을 뼈대(backbone_crime.json)에 건다.

- build_lab.py가 장마다 kg_raw(slug)를 불러 페이지에 <script id="kg-raw">를 넣는다(ahnboat.xyz 지도가 모은다).
- build_crime_map.py가 이 목록 + 리포트 kg.json + 뼈대로 ontology.html의 데이터를 만든다.
뼈대: github.com/adminmrobo/ahnboat_lab_explainer data/backbone_crime.json (작성자 초안 v0.1) — 사본 data/backbone_crime.json
"""
import json

# (장, id, type, ko, en, 정의, anchor, [뼈대 주제], 범죄자의 계산서 변수)
C = [
    ("ch00", "lab:concept/expected-utility-crime", "Concept", "기대이익", "Expected gain from crime", "확률을 곱해 평균적으로 남는 이익", "#s2", ["expected-utility-crime"], "g p"),
    ("ch00", "lab:concept/economics-of-crime", "Concept", "범죄경제학", "Economics of crime", "범죄를 비용과 편익의 선택으로 분석하는 경제학", "#s4", ["expected-utility-crime"], ""),
    ("ch00", "lab:concept/conditions-for-crime", "Concept", "범죄가 되는 세 조건", "Three conditions for a technology to become crime", "중립인 기술이 범죄가 되려면 갖춰지는 조건", "#s2", ["tech-neutrality-crime"], ""),
    ("ch00", "lab:concept/ai-crime-six-features", "Concept", "AI 범죄의 여섯 가지 특징", "Six features of AI crime", "자동화·은폐·정보 활용·수익 은닉·적발 곤란·사업화", "#s3", ["ai-crime-features"], "c p pi"),
    ("ch00", "lab:concept/crime-as-a-service", "Concept", "서비스형 범죄(CaaS)", "Crime as a service", "범죄 도구를 구독·임대로 파는 구조", "#s3", ["crime-as-a-service"], "c"),
    ("ch01", "lab:concept/conversational-automated-crime", "Concept", "대화형 자동범죄", "Conversational automated crime", "AI가 사람처럼 대화하며 수행하는 범죄", "#s1", ["attack-automation", "ai-crime-features"], "c"),
    ("ch01", "lab:concept/one-to-n-production", "Concept", "1:N 생산함수", "One-to-N production function", "한 공격자가 다수를 동시에 상대하는 구조", "#s3", ["crime-cost-structure"], "c"),
    ("ch01", "lab:concept/scam-funnel", "Concept", "퍼널", "Scam funnel", "단계별로 줄어드는 전환 과정", "#s3", ["scam-funnel"], "pi"),
    ("ch01", "lab:method/idsgan", "Method", "IDSGAN", "IDSGAN", "GAN으로 침입 탐지를 속이는 트래픽을 만든 연구", "#s4", ["adaptive-evasion"], "p"),
    ("ch01", "lab:concept/deepfake-sexual-abuse-material", "Concept", "딥페이크 성착취물", "Deepfake sexual abuse material", "합성 성적 영상물 범죄", "#s4", ["deepfake-crime"], ""),
    ("ch02", "lab:theory/becker-model", "Theory", "베커 모형", "Becker model of crime", "기대효용으로 범죄 선택을 설명하는 모형(1968)", "#s1", ["expected-utility-crime"], "p f g"),
    ("ch02", "lab:concept/breakeven-arrest-probability", "Concept", "손익분기 검거 확률", "Break-even probability of apprehension", "범죄와 합법적 삶이 같아지는 검거 확률 p*", "#s3", ["breakeven-arrest-probability"], "p"),
    ("ch02", "lab:concept/certainty-of-punishment", "Concept", "처벌의 확실성", "Certainty of punishment", "처벌 강도보다 억제력이 크다고 보고되는 요소", "#s4", ["deterrence-certainty"], "p"),
    ("ch02", "lab:concept/opportunity-cost", "Concept", "기회비용", "Opportunity cost", "범죄를 위해 포기한 합법 소득", "#s4", ["crime-opportunity-cost"], "c"),
    ("ch03", "lab:concept/deepfake", "Concept", "딥페이크", "Deepfake", "딥러닝으로 만든 합성 영상·음성", "#s1", ["deepfake-crime"], "pi"),
    ("ch03", "lab:method/gan", "Method", "GAN", "Generative adversarial network", "생성자와 판별자가 겨루며 학습하는 구조", "#s1", ["deepfake-crime"], ""),
    ("ch03", "lab:concept/voice-cloning-scam", "Concept", "목소리 복제 금융사기", "Voice-cloning financial scam", "합성한 목소리로 송금을 요구하는 사기", "#s3", ["voice-cloning-scam"], "pi"),
    ("ch03", "lab:concept/signaling-game", "Concept", "신호 게임", "Signaling game", "정보가 없는 쪽이 상대의 신호로 유형을 추론하는 게임", "#tool", ["signaling-game-crime"], "pi"),
    ("ch03", "lab:concept/liars-dividend", "Concept", "거짓말쟁이의 배당", "Liar's dividend", "진짜 증거를 가짜라고 우기는 이득", "#s3", ["liars-dividend"], "f"),
    ("ch03", "lab:concept/verification-question", "Method", "가족 확인 질문", "Pre-agreed verification question", "미리 정한 질문으로 상대를 확인하는 절차", "#s4", ["verification-procedure"], "pi"),
    ("ch04", "lab:concept/social-engineering", "Concept", "사회공학", "Social engineering", "기술 대신 사람의 심리를 공격하는 기법", "#s1", ["impersonation", "phishing"], "pi"),
    ("ch04", "lab:concept/inspection-game", "Concept", "검사 게임", "Inspection game", "감시자와 위반자의 혼합 전략 게임", "#tool", ["inspection-game"], "p"),
    ("ch04", "lab:method/membership-inference", "Method", "멤버십 추론", "Membership inference", "모델 출력으로 학습 데이터 포함 여부를 알아내는 공격", "#s3", ["personal-data-raw-material"], ""),
    ("ch04", "lab:concept/spear-phishing", "Concept", "스피어피싱", "Spear phishing", "특정인을 겨냥한 맞춤 피싱", "#s2", ["phishing"], "pi"),
    ("ch05", "lab:concept/attack-automation-stages", "Concept", "공격 자동화의 5단계", "Five stages of attack automation", "정찰에서 흔적 감추기까지 공격 단계의 자동화", "#s1", ["attack-automation"], "c"),
    ("ch05", "lab:concept/adaptive-evasion", "Concept", "적응형 탐지 회피", "Adaptive detection evasion", "방어 반응을 학습해 수법을 바꾸는 공격", "#s2", ["adaptive-evasion"], "p"),
    ("ch05", "lab:concept/false-flag", "Concept", "거짓 깃발", "False flag", "다른 조직의 흔적을 흉내 내 수사를 속이는 전술", "#s3", ["adaptive-evasion", "enforcement-cooperation"], "p f"),
    ("ch05", "lab:method/behavioral-anomaly-detection", "Method", "행위 기반 이상 탐지", "Behavior-based anomaly detection", "공격 코드 대신 평소와 다른 행동을 잡는 탐지", "#s4", ["behavioral-detection", "crime-anomaly-detection"], "p"),
    ("ch05", "lab:metric/precision-recall", "Metric", "정밀도·재현율", "Precision and recall", "경보 중 진짜 비율과 공격 중 잡은 비율", "#s4", ["crime-anomaly-detection"], ""),
    ("ch05", "lab:method/zero-trust", "Method", "제로 트러스트", "Zero trust", "내부도 믿지 않고 매번 확인하는 보안 모델", "#s5", ["layered-defense"], "pi"),
    ("ch06", "lab:concept/ai-surveillance", "Concept", "일상이 된 AI 감시", "Everyday AI surveillance", "생활 곳곳의 수집 장치와 알고리즘 감시", "#s1", ["ai-surveillance"], ""),
    ("ch06", "lab:concept/reidentification", "Concept", "재식별", "Re-identification", "가명 데이터에서 개인을 다시 특정하는 것", "#s3", ["reidentification"], "pi"),
    ("ch06", "lab:concept/data-broker", "Concept", "데이터 브로커", "Data broker", "여러 출처의 개인정보를 모아 파는 사업자", "#s2", ["personal-data-raw-material"], "c"),
    ("ch06", "lab:concept/proportionality-principle", "Concept", "비례성 원칙", "Proportionality principle", "감시 강도는 목적의 중요성에 비례해야 한다는 원칙", "#s4", ["data-protection-law", "ai-surveillance"], ""),
    ("ch06", "lab:method/differential-privacy", "Method", "차분 프라이버시", "Differential privacy", "결과에 잡음을 넣어 개인 노출을 막는 기법", "#s4", ["reidentification"], "pi"),
    ("ch07", "lab:concept/crypto-theft-process", "Concept", "AI 기반 암호화폐 탈취", "AI-driven crypto theft", "정찰·침투·탈취로 이어지는 암호화폐 탈취 공정", "#s2", ["crypto-theft"], "g"),
    ("ch07", "lab:concept/raas", "Concept", "RaaS", "Ransomware as a service", "랜섬웨어를 빌려주고 수익을 나누는 구조", "#s4", ["ransomware-economy", "crime-as-a-service"], "c"),
    ("ch07", "lab:concept/mixing-service", "Concept", "믹싱 서비스", "Mixing service", "여러 사람의 코인을 섞어 경로를 끊는 서비스", "#s3", ["money-laundering"], "p"),
    ("ch07", "lab:standard/travel-rule", "Standard", "트래블룰", "Travel rule", "가상자산 이전 시 송·수신인 정보를 전달하는 규칙", "#s5", ["money-laundering", "ai-crime-regulation"], "p"),
    ("ch07", "lab:concept/double-extortion", "Concept", "이중 협박", "Double extortion", "암호화와 유출 위협을 동시에 쓰는 랜섬웨어", "#s4", ["ransomware-economy"], "g"),
    ("ch07", "lab:concept/ransom-negotiation", "Concept", "랜섬 협상 게임", "Ransom bargaining game", "몸값 지급 여부를 둔 공격자와 피해 조직의 협상", "#tool", ["ransom-bargaining"], "g"),
    ("ch08", "lab:method/passkey", "Method", "패스키", "Passkey", "비밀번호 없이 기기 인증으로 로그인하는 방식", "#s2", ["verification-procedure", "layered-defense"], "pi"),
    ("ch08", "lab:method/identity-lock", "Method", "명의도용 차단", "Identity theft blocking services", "엠세이퍼·여신거래·비대면 계좌개설 안심차단", "#s4", ["identity-lock"], "pi"),
    ("ch08", "lab:method/incident-response-5-steps", "Method", "사고 대응 5단계", "Five-step incident response", "지급정지→계정 회수→명의 잠금→증거→신고", "#s4", ["incident-response"], "g"),
    ("ch08", "lab:concept/optimal-security-investment", "Concept", "최적 보안 투자", "Optimal security investment", "추가 투자의 효과가 비용과 같아지는 지점", "#tool", ["layered-defense"], ""),
    ("ch08", "lab:concept/layered-defense", "Concept", "다층 방어", "Layered defense", "여러 겹의 장치가 함께 작동하는 방어", "#s1", ["layered-defense"], "pi"),
    ("ch09", "lab:concept/externality", "Concept", "외부성", "Externality", "거래에 참여하지 않은 제3자에게 미치는 이익·피해", "#s1", ["security-cooperation-dilemma"], ""),
    ("ch09", "lab:concept/prisoners-dilemma", "Concept", "죄수의 딜레마", "Prisoner's dilemma", "각자의 최선이 모두의 손해가 되는 게임", "#tool", ["security-cooperation-dilemma"], ""),
    ("ch09", "lab:concept/cyber-herd-immunity", "Concept", "사이버 집단 면역", "Cyber herd immunity", "사회 전체 보안 수준이 문턱을 넘으면 확산이 멈춤", "#s2", ["threat-intel-sharing", "security-cooperation-dilemma"], "pi"),
    ("ch09", "lab:concept/nash-equilibrium", "Concept", "내쉬 균형", "Nash equilibrium", "아무도 혼자 전략을 바꿀 이유가 없는 상태", "#tool", ["security-cooperation-dilemma", "inspection-game"], ""),
    ("ch09", "lab:concept/cross-border-cooperation", "Concept", "국경을 넘는 협력", "Cross-border cooperation", "수사·정보 공유를 위한 국제 원칙과 법", "#s4", ["enforcement-cooperation", "threat-intel-sharing"], "p"),
    ("ch10", "lab:concept/resilience", "Concept", "회복력", "Resilience", "피해를 빨리 알아차리고 줄이고 되살리는 능력", "#s2", ["resilience"], "g"),
    ("ch10", "lab:concept/golden-time", "Concept", "골든타임", "Golden time", "피해가 급증하기 전 대응 가능한 시간", "#s2", ["incident-response", "resilience"], "g"),
    ("ch10", "lab:concept/synthetic-identity", "Concept", "합성 신원", "Synthetic identity", "존재하지 않는 사람의 신원을 AI로 만든 것", "#s1", ["synthetic-identity"], "p pi"),
    ("ch10", "lab:concept/autonomous-attack-agent", "Concept", "자율형 공격 에이전트", "Autonomous attack agent", "정찰→침투→협박을 스스로 이어 가는 공격", "#s1", ["autonomous-attack-agent", "agentic-crime"], "c"),
    ("ch10", "lab:concept/xr-iot-threats", "Concept", "메타버스·XR·IoT 위협", "XR and IoT threats", "가상공간과 보안 없는 기기가 여는 새 위협", "#s1", ["xr-iot-threats"], ""),
    ("ch10", "lab:standard/post-quantum-cryptography", "Standard", "양자 내성 암호", "Post-quantum cryptography", "양자 컴퓨터로도 풀기 어려운 암호", "#s1", ["post-quantum-risk"], ""),
]
INST = ("lab:concept/incentive-enforcement-design", "Concept", "제도 설계(인센티브·강제력)", "Institutional design with enforcement",
        "규칙·인센티브·디스인센티브와 이를 적용하는 강제력의 설계", "#inst", ["incentive-design"], "p f")
# 장 안의 개념끼리 (출발, 관계, 도착)
REL = [
    ("lab:theory/becker-model", "derivedFrom", "lab:concept/economics-of-crime"),
    ("lab:concept/breakeven-arrest-probability", "derivedFrom", "lab:theory/becker-model"),
    ("lab:concept/certainty-of-punishment", "relatedTo", "lab:theory/becker-model"),
    ("lab:concept/opportunity-cost", "partOf", "lab:theory/becker-model"),
    ("lab:concept/expected-utility-crime", "partOf", "lab:concept/economics-of-crime"),
    ("lab:concept/crime-as-a-service", "partOf", "lab:concept/ai-crime-six-features"),
    ("lab:concept/conditions-for-crime", "prerequisiteOf", "lab:concept/ai-crime-six-features"),
    ("lab:concept/one-to-n-production", "relatedTo", "lab:concept/conversational-automated-crime"),
    ("lab:concept/scam-funnel", "relatedTo", "lab:concept/conversational-automated-crime"),
    ("lab:method/idsgan", "relatedTo", "lab:concept/conversational-automated-crime"),
    ("lab:concept/deepfake-sexual-abuse-material", "relatedTo", "lab:concept/conversational-automated-crime"),
    ("lab:method/gan", "prerequisiteOf", "lab:concept/deepfake"),
    ("lab:concept/voice-cloning-scam", "partOf", "lab:concept/deepfake"),
    ("lab:concept/liars-dividend", "relatedTo", "lab:concept/deepfake"),
    ("lab:concept/signaling-game", "relatedTo", "lab:concept/deepfake"),
    ("lab:concept/verification-question", "addressedBy", "lab:concept/voice-cloning-scam"),
    ("lab:concept/spear-phishing", "partOf", "lab:concept/social-engineering"),
    ("lab:concept/inspection-game", "relatedTo", "lab:concept/social-engineering"),
    ("lab:method/membership-inference", "relatedTo", "lab:concept/social-engineering"),
    ("lab:concept/attack-automation-stages", "prerequisiteOf", "lab:concept/adaptive-evasion"),
    ("lab:concept/adaptive-evasion", "addressedBy", "lab:method/behavioral-anomaly-detection"),
    ("lab:method/behavioral-anomaly-detection", "evaluatedBy", "lab:metric/precision-recall"),
    ("lab:concept/false-flag", "relatedTo", "lab:concept/adaptive-evasion"),
    ("lab:method/zero-trust", "contrastsWith", "lab:concept/adaptive-evasion"),
    ("lab:concept/data-broker", "relatedTo", "lab:concept/reidentification"),
    ("lab:concept/reidentification", "addressedBy", "lab:method/differential-privacy"),
    ("lab:concept/proportionality-principle", "relatedTo", "lab:concept/ai-surveillance"),
    ("lab:concept/ai-surveillance", "relatedTo", "lab:concept/data-broker"),
    ("lab:concept/raas", "relatedTo", "lab:concept/double-extortion"),
    ("lab:concept/ransom-negotiation", "relatedTo", "lab:concept/double-extortion"),
    ("lab:concept/mixing-service", "addressedBy", "lab:standard/travel-rule"),
    ("lab:concept/crypto-theft-process", "prerequisiteOf", "lab:concept/mixing-service"),
    ("lab:method/passkey", "partOf", "lab:concept/layered-defense"),
    ("lab:method/identity-lock", "partOf", "lab:concept/layered-defense"),
    ("lab:method/incident-response-5-steps", "partOf", "lab:concept/layered-defense"),
    ("lab:concept/optimal-security-investment", "relatedTo", "lab:concept/layered-defense"),
    ("lab:concept/externality", "prerequisiteOf", "lab:concept/prisoners-dilemma"),
    ("lab:concept/nash-equilibrium", "partOf", "lab:concept/prisoners-dilemma"),
    ("lab:concept/cyber-herd-immunity", "relatedTo", "lab:concept/externality"),
    ("lab:concept/cross-border-cooperation", "relatedTo", "lab:concept/prisoners-dilemma"),
    ("lab:concept/golden-time", "partOf", "lab:concept/resilience"),
    ("lab:concept/synthetic-identity", "relatedTo", "lab:concept/autonomous-attack-agent"),
    ("lab:concept/xr-iot-threats", "relatedTo", "lab:concept/autonomous-attack-agent"),
    ("lab:standard/post-quantum-cryptography", "relatedTo", "lab:concept/xr-iot-threats"),
]
FIRST = {}
for r in C:
    FIRST.setdefault(r[0], r[1])

# 리포트 지식 색인의 개념 → 뼈대 주제 (리포트로 '현장 확인'된 주제)
REPORT_MAP = {
    "lab:concept/synthetic-identity": ["synthetic-identity"],
    "lab:concept/true-identity-theft": ["impersonation"],
    "lab:concept/first-party-fraud": ["first-party-fraud"],
    "lab:concept/scalable-identity": ["crime-as-a-service"],
    "lab:concept/adaptive-identity": ["adaptive-evasion"],
    "lab:concept/patient-identity": ["synthetic-identity"],
    "lab:concept/synthetic-farm": ["synthetic-identity"],
    "lab:concept/deepfake": ["deepfake-crime"],
    "lab:concept/injection-replay-attack": ["deepfake-crime"],
    "lab:concept/proof-of-life": ["identity-verification"],
    "lab:indicator/zero-noise": ["crime-anomaly-detection"],
    "lab:concept/denominator": ["crime-statistics-literacy"],
    "lab:method/point-in-time-verification": ["identity-verification"],
    "lab:method/lifecycle-trust": ["identity-verification"],
    "lab:method/orchestration": ["defense-orchestration"],
    "lab:method/step-up": ["verification-procedure"],
    "lab:method/liveness-check": ["identity-verification"],
    "lab:concept/expected-utility-crime": ["expected-utility-crime"],
    "lab:concept/arrest-probability": ["deterrence-certainty"],
    "lab:concept/crime-gain": ["expected-utility-crime"],
    "lab:concept/success-probability": ["expected-utility-crime"],
    "lab:concept/crime-unit-cost": ["crime-cost-structure"],
    "lab:limitation/human-deepfake-detection": ["verification-procedure"],
    "lab:indicator/synthetic-share": ["crime-statistics-literacy"],
    "lab:claim/position-biometric-necessity": ["data-protection-law"],
    "lab:claim/ebook-footnote-mismatch": ["industry-report-reading"],
}


def kg_raw(slug):
    """장 페이지에 넣을 지식 그래프(retrofit kg.json과 같은 틀). 뼈대 주제는 broader로 건다."""
    rows = [r for r in C if r[0] == slug]
    nodes, edges, ids = [], [], set()
    for ch, i, t, ko, en, d, anc, tops, var in rows + [(slug,) + INST]:
        nodes.append({"id": i, "type": t, "label": {"ko": ko, "en": en}, "page": slug, "anchor": anc, "level": 2,
                      "status": "known", "confidence": "high", "coverage": "explained", "definition": {"ko": d},
                      "family": "crime", "domain": ["crime"], "crimeVar": var.split(), "match": []})
        ids.add(i)
        for tp in tops:
            edges.append({"s": i, "p": "lab:broader", "o": "lab:topic/" + tp, "anchor": anc, "confidence": "high"})
    for s, p, o in REL:
        if s in ids and o in ids:
            edges.append({"s": s, "p": "lab:" + p, "o": o, "anchor": "#kg", "confidence": "high"})
    edges.append({"s": INST[0], "p": "lab:relatedTo", "o": FIRST[slug], "anchor": "#inst", "confidence": "high"})
    return {"version": "1.0", "page": slug, "domain": "crime", "backbone": "backbone_crime 0.1", "nodes": nodes, "edges": edges}


if __name__ == "__main__":
    print(len(C), sum(len(kg_raw(s)["edges"]) for s in FIRST))
