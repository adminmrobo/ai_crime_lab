# AI 범죄 연구실 — 범죄자의 계산서를 뒤집어라

『AI 범죄와 자기 방어』의 사례 보충본이다. 책은 AI가 범죄에 쓰이는 실제 사례를 모으고, 범죄자가 왜 AI를 고르는지를 범죄경제학의 눈으로 묻는다. 범죄자도 비용과 이익을 따진다는 관점에서, AI가 범죄의 비용 구조와 수익 모델을 어떻게 바꾸었는지 풀어낸다.
이 사이트는 그 내용을 연구실 식구들이 장마다 사례·모의 데이터·실험으로 풀어 쓴다.

- 사이트: https://adminmrobo.github.io/ai_crime_lab/
- 저자: 안상선 ((주)M-Robo 대표) · https://adminmrobo.github.io/who_am_i/who_am_i.html

## 구성

| 페이지 | 내용 | 분석 도구 |
|---|---|---|
| `index.html` | 목차·등장인물·분석 틀 | — |
| `ch00.html` | 서장 진화하는 사이버 범죄 | 범죄경제학(기대이익) |
| `ch01.html` | 1장 AI 범죄, 새로운 디지털 위험의 시대 | AI(퍼널 확률) |
| `ch02.html` | 2장 범죄자의 경제학 | 범죄경제학(베커 모형·p*) |
| `ch03.html` | 3장 딥페이크의 위협 | 게임이론(신호 게임·베이즈) |
| `ch04.html` | 4장 완벽한 사기꾼 — 피싱과 사회공학 | 게임이론(검사 게임) |
| `ch05.html` | 5장 끊임없는 진화 — 자동화 공격 | AI(이상 탐지·정밀도/재현율) |
| `ch06.html` | 6장 보이지 않는 눈 — 감시와 프라이버시 | AI(재식별) |
| `ch07.html` | 7장 보이지 않는 손의 조작 — 금융 범죄 | 게임이론(랜섬 협상) |
| `ch08.html` | 8장 나만의 디지털 방패 | 범죄경제학(최적 보안 투자) |
| `ch09.html` | 9장 함께 만드는 안전한 AI 사회 | 게임이론(죄수의 딜레마) |
| `ch10.html` | 10장 미래를 준비하는 디지털 생존 전략 | 범죄경제학(다섯 겹 계산서 뒤집기) |
| `practice/index.html` | 마지막 장 · 실전 연습장(콜센터·검사 게임·랜섬 협상·기업 연결망) | 시뮬레이터 |
| `workbook.html` · `references.html` · `data.html` | 통합 작업본 · 참고문헌 · 모의 데이터와 재현 코드 | — |

결론: 범죄를 줄이는 것은 도덕적 원칙의 선언이 아니라 **규칙·인센티브·디스인센티브와 이를 실제로 적용하는 강제력**이다. 모든 장의 마지막 단계에 강화학습 시뮬레이션(`assets/rl.js`)을 두어, 제도를 켜고 끄며 에이전트가 배우는 행동을 확인한다.

장마다 흐름: 처음 오신 분께 3줄 → 왜 · 큰 그림 · 30초 복습 → 본문 단계(박사 현장 질문 · 일상/현장 · 단계 대화 · 해석 · 확인 퀴즈) → 분석 도구 단계 → 제도 설계 단계 → 강화학습 시뮬레이션 → 대결 · 정리 퀴즈 · 아웃트로 · 지식 색인 · 꾸러미.

등장인물: 범죄자 대역 X1·X2·X3 / 추적 팀 인턴1 시아·인턴2 모아·조수(하루) / 해설 박사 / 분석 주판봇·초파리 연구원.
캐릭터 그림은 [fruitfly-lab-expressions](https://github.com/adminmrobo/fruitfly-lab-expressions) 정본을 줄여 썼다. 장면 그림 지시문은 `images/PROMPTS.md`.

## 리포트·뉴스 검증 (현장 검증)

새로 나온 보고서와 뉴스를 책의 장과 나란히 놓고 읽는 기록이다. 목록과 장별 집계는 `reports/index.html`.

| 번호 | 폴더 | 자료 |
|---|---|---|
| 001 | `reports/2026-11-23_lnrs-synthetic-identity-deepfake/` | LexisNexis Risk Solutions, 『Stopping Synthetic Identity and Deepfake Fraud』 전자책(2026) |

- 폴더 이름: `YYYY-MM-DD_발행처-주제` (날짜는 연구실 검토일, 영문 소문자·하이픈)
- 페이지 형식: 박사의 동향 소개(사실·출처·기준 시점) + 마지막에 책 장별 대조표
- 지식 색인·꾸러미 원본은 각 폴더의 `kg/` (조립: `sh scripts/assemble_report_001.sh`, 도구는 ahnboat_lab_explainer)
- 새 리포트 등록: `reports/registry.json`에 추가 → `python scripts/build_reports_index.py`
- 원본 PDF는 재배포 허락이 확인될 때만 올리고, 아니면 공식 링크만 적는다.

## 다시 만들기

```bash
pip install numpy pandas markdown
python scripts/gen_data.py     # 모의 데이터·차트(assets/charts)
python scripts/build_lab.py    # content/*.md + scripts/lab_data.py → *.html
```

## 주의

- '모의 데이터(가상)'는 설명용 가상의 수치이며 실제 통계가 아니다.
- 범죄 수법은 작동 원리 수준까지만 다루며, 실행 절차는 싣지 않는다.
- 일부 사실은 원문 대조가 남아 있다(참고문헌의 '확인 필요').
