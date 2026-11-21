title: 목차
---
<section class="hero"><div><div class="no">AI 범죄 연구실 · 보충본</div><h1>범죄자의 계산서를 뒤집어라</h1><p class="sub">AI는 왜 범죄자에게 '남는 장사'가 되었을까. 범죄경제학·게임이론·AI 분석으로 계산하고, 대응책으로 다시 계산한다.</p><div class="book">{{BOOK}} <a href="https://adminmrobo.github.io/who_am_i/who_am_i.html">저자 소개</a></div></div><img class="cover" src="assets/lineup.webp" alt="연구실 식구 단체 사진" width="1200" height="678"></section>

<section class="three"><h2>처음 오신 분께 — 이 사이트를 3줄로</h2><ol><li><b>무엇을</b>: AI가 범죄에 쓰인 실제 사례를 서장과 10개 장에 걸쳐 풀어 본다.</li><li><b>왜 중요한가</b>: 범죄자도 비용과 이익을 따진다. 그 계산을 알면 막을 곳이 보인다.</li><li><b>생활·업무에서는</b>: 장마다 '계산서 뒤집기'로 개인·조직·정책이 할 일을 정리한다.</li></ol><p class="note">코드와 수식을 몰라도 됩니다. 마지막 장 '실전 연습장'에서 직접 운영해 볼 수 있습니다.</p></section>

@박사(E07): 이 연구실에서는 범죄를 도덕 이야기로만 읽지 않는다. 범죄자도 손익을 따지는 사람이라는 가정에서 출발한다. AI가 무엇을 바꿨는지 알려면 **범죄자의 계산서**를 먼저 펼쳐 봐야 한다.
@X1(E16): 우리는 범죄자 역할을 맡은 대역이다. 진짜 범죄자가 아니니 안심하시라. 다만 계산은 진짜처럼 한다.
@X2(E09): 나는 자동화 공격과 랜섬웨어를 맡는다. 막히면 배우고 다시 온다.
@X3(E13): 나는 정보를 사고, 돈을 옮긴다. 보이지 않는 곳에서.
@하루(E01): 그리고 우리 추적 팀은 그 계산서의 숫자를 하나씩 바꿔서, 범죄가 '밑지는 장사'가 되게 만드는 방법을 찾아요.
@시아(E09): 저는 현장 사례를 쫓아요.
@모아(E07): 저는 제도와 법을 쫓아요.
@주판봇(E16): 계산은 제가 해요! 가끔 너무 빨리 확신하지만요.
@초파리(E09): 그럴 땐 내가 의심하고 데이터를 다시 돌린다.

## 세 가지 분석 도구

| 도구 | 묻는 질문 | 대표 장 |
|---|---|---|
| **범죄경제학** | 범죄 한 번의 기대이익은 얼마인가, 어느 숫자를 바꾸면 0 아래로 내려가나 | 서장·2·8·10장 |
| **게임이론** | 범죄자와 방어자가 서로의 수를 읽을 때 어디서 멈추나(균형) | 3·4·7·9장 |
| **AI·데이터 분석** | AI는 공격과 탐지에서 무엇을 계산하나, 그 한계는 어디인가 | 1·5·6장 |

:::econ 책 전체를 꿰는 한 줄
베커(1968)의 기대효용 모형: **E(U) = p × U(Y − f) + (1 − p) × U(Y + g)**. 범죄자는 이 값이 합법적 삶의 효용 U(Y)보다 클 때 범죄를 고른다. 계산을 쉽게 하려고 시도 1건의 기대이익 **π × (g − p × f) − c**도 함께 쓴다(π 성공 확률, g 성공 1건 수익, p 성공 1건당 검거 확률, f 처벌, c 시도 비용).
:::

## 장마다 같은 흐름

1. **처음 오신 분께 3줄** → **왜 이 장이 필요한가** → **큰 그림**
2. **단계 1~5** — 원고의 논지를 박사가 풀고, 시아·모아가 사례와 제도를 추적한다. X1~X3는 '범죄자의 계산서'를, 주판봇·초파리는 모의 데이터 분석을 들고 나온다.
3. **분석 도구 단계** — 범죄경제학·게임이론·AI 중 하나를 골라, 왜 쓰는지와 수식을 조수(하루)가 대신 묻고, 직접 바꿔 보는 실험을 한다.
4. **대결** — X와 추적 팀이 한 수씩 두고 박사가 판정한다.
5. **정리 퀴즈 · 아웃트로 · 지식 색인 · 꾸러미**

## 장 목록

{{CARDS}}

[통합 작업본](workbook.html)에서 원고와 프로젝트 챕터 원고를 합친 장 구성 대응표와 사실 확인 메모를, [참고문헌과 출처](references.html)에서 장별 출처를, [모의 데이터와 재현 코드](data.html)에서 모든 차트의 가정과 코드를 볼 수 있다.

:::warn 읽기 전에
- '모의 데이터(가상)'라고 적힌 수치는 개념을 설명하려고 시드 고정 코드로 만든 가상의 값이다. 실제 통계로 인용하면 안 된다.
- 실제 사건과 수치는 원고와 공개 보도·보고서를 따랐다. 일부는 원문 대조가 남아 있다(참고문헌의 '확인 필요').
- 범죄 수법은 작동 원리 수준까지만 다룬다. 도구 사용법이나 우회 문구 같은 실행 절차는 싣지 않는다.
:::

:::prompt 시리즈 표지
16-bit pixel art, bright daytime research lab with white walls, 박사 pointing at a big abacus-shaped scoreboard showing "COST · RISK · PROFIT", three black-silhouette characters X1 (ponytail with pink bow) X2 (beret and round glasses) X3 (cat ears) holding receipts on the right, two maid interns 시아 (black hair) and 모아 (beige hair) and assistant 하루 (pink hair, lab coat) holding magnifying glasses and a shield on the left, abacus robot 주판봇 and fly researcher 초파리 at a data terminal, SNES RPG style, white background.
:::
