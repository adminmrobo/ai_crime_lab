# AI 범죄 연구실 — 그림 지시문 (16비트 RPG 픽셀아트)

## 0. 공통 규칙

- **화풍**: 16-bit SNES RPG pixel art, 낮의 연구실, **흰 배경**(밤 장면 금지), 선명한 외곽선, 제한된 팔레트
- **비율·크기**: 표지 1600×900(16:9), 장면 1200×800(3:2), 연습장 표지 1600×900
- **저장**: PNG로 받아 WebP(품질 82)로 변환 → `assets/covers/` · 한 편 600KB 이하
- **글자**: 그림 안의 한글은 깨지기 쉬우므로 넣지 않습니다. 필요한 기호(₩, %, −, ✓, ✗, ?)와 짧은 영문만 씁니다.
- **캐릭터 참고 그림**: 요청할 때마다 `assets/chars/` 기본 표정 4장(박사 E01, 하루 E01, 시아 E01, 모아 E01)을 함께 올립니다. X1~X3은 **검은 실루엣**으로만 그립니다(얼굴 묘사 금지).
- **만드는 순서**: ① 시리즈 표지를 먼저 받아 그림체 확인 → ② 그 표지를 참고 그림으로 함께 올려 장면 11장(3~5장씩, 같은 비율끼리 한 대화) → ③ 강화학습 공통 그림 → ④ 실전 연습장 표지

### 공통 꼬리말 (모든 지시문 끝에 붙임)

```
16-bit SNES RPG pixel art, bright daytime, clean white background, crisp 1px outlines, limited palette, no Korean text, no gore, no real logos, no real people.
```

### 캐릭터 고정 묘사 (지시문에 그대로 복사)

| 이름 | 고정 묘사 |
|---|---|
| 박사 | middle-aged professor in a white lab coat, round glasses, gray-streaked hair, calm smile |
| 하루(조수) | young assistant with pink hair in a white lab coat, holding a clipboard |
| 시아(인턴1) | maid-uniform intern with long black hair, magnifying glass |
| 모아(인턴2) | maid-uniform intern with beige hair, holding a notebook |
| 주판봇 | small box-shaped robot with an abacus on its chest |
| 초파리 연구원 | tiny fruit fly in a lab coat with big red eyes, standing on a terminal |
| X1 | black silhouette, ponytail with a pink bow (fraud·impersonation) |
| X2 | black silhouette, beret and round glasses (automated attacks) |
| X3 | black silhouette, cat ears (laundering·data broker) |

---

## 1. 시리즈 표지 — `assets/covers/index.webp` (1600×900)

```
Wide 16:9 scene of a bright white research lab. Center: the professor points at a giant abacus-shaped scoreboard showing three bars "COST", "RISK", "PROFIT". Right side: three black silhouettes X1 (ponytail with pink bow), X2 (beret, round glasses), X3 (cat ears) each holding a long paper receipt with a plus sign. Left side: pink-haired assistant Haru with a clipboard, black-haired maid intern Sia with a magnifying glass, beige-haired maid intern Moa holding a small shield. Foreground: box robot with an abacus chest and a tiny fruit-fly researcher at a data terminal. 
+ 공통 꼬리말
```

대체 표지(선택) — `assets/covers/index_alt.webp`

```
Same lab, overhead view of a long table like a board game: on the left side the criminals' receipts turn from green "+" to red "−" as four blocks are placed in a row (rule, carrot, stick, gavel icons). The team watches; the professor holds a gavel and an abacus.
+ 공통 꼬리말
```

## 2. 장면 그림 (1200×800)

### 서장 · 진화하는 사이버 범죄 — `assets/covers/ch00.webp`
```
Two-panel scene. Left: an office worker frowning at a smartphone chat bubble with a suspicious link icon, a question mark above their head. Right: the same worker holding a phone that shows a waveform and a heart icon (a familiar voice). Behind both panels, the X1 silhouette holds a receipt with "COST ↓  PROFIT ↑".
+ 공통 꼬리말
```

### 1장 · AI 범죄, 새로운 디지털 위험의 시대 — `assets/covers/ch01.webp`
```
Left: one small scammer silhouette at a desk with a single phone. Right: a tall server rack shooting out hundreds of chat bubbles like a fountain, the X1 silhouette leaning on it with a smile. Bottom: intern Sia with a magnifying glass reading a funnel chart that narrows from wide to thin.
+ 공통 꼬리말
```

### 2장 · 범죄자의 경제학 — `assets/covers/ch02.webp`
```
Classroom-style lab. The professor at a whiteboard writing "E(U) = p·U(Y−f) + (1−p)·U(Y+g)". The abacus robot slides three beads labeled p, f, g. The three silhouettes X1, X2, X3 sit at student desks raising hands. Assistant Haru holds a balance scale: a coin bag on one side, a small jail-bar icon on the other.
+ 공통 꼬리말
```

### 3장 · 진짜인 듯 가짜인 세상 — 딥페이크 — `assets/covers/ch03.webp`
```
Meeting room with a big video-call screen showing five faces; three faces glitch into pixel noise at the edges. A finance worker hesitates with a cursor over a "SEND" button. Assistant Haru stands beside holding a card with a phone icon and a return arrow (call back). Small X1 silhouette visible only as a reflection on the screen.
+ 공통 꼬리말
```

### 4장 · 완벽한 사기꾼 — 피싱과 사회공학 — `assets/covers/ch04.webp`
```
Open office floor, envelope icons popping above every desk; some envelopes glow red with a fishing hook. Intern Moa runs a short training at a whiteboard with three icons in a row: magnifying glass → stop hand → bell. The X1 silhouette fishes from a ceiling hatch with a long rod. One employee holds the phone and dials back, green check above.
+ 공통 꼬리말
```

### 5장 · 끊임없는 진화 — 자동화 공격 — `assets/covers/ch05.webp`
```
White server room. The X2 silhouette controls a shape-shifting slime that changes color in three frames. A wall of old rule signs crumbles. Assistant Haru and the fruit-fly researcher watch a monitor with a behavior graph showing one red spike at 3:00. The abacus robot prints a short alert ticket.
+ 공통 꼬리말
```

### 6장 · 보이지 않는 눈 — 감시와 프라이버시 — `assets/covers/ch06.webp`
```
City street at noon. Translucent floating eyes above camera poles. A citizen walks while small puzzle pieces (cake, car, ID badge, map pin) slip out of their pocket. The X3 silhouette quietly collects the pieces and assembles a jigsaw portrait. Intern Sia covers one piece with a blur sticker.
+ 공통 꼬리말
```

### 7장 · 보이지 않는 손의 조작 — 금융 범죄 — `assets/covers/ch07.webp`
```
Bank-like hall. A giant invisible glove (outlined with dotted pixels) moves coins along glowing chain links. The X3 silhouette splits a gold coin into many small coins that fall into a mixer machine. Intern Sia follows the coin trail with a lantern; the abacus robot counts. In a corner, a server is locked with a padlock and a ransom note shaped like a receipt; a backup drive beside it shines green.
+ 공통 꼬리말
```

### 8장 · 나만의 디지털 방패 만들기 — `assets/covers/ch08.webp`
```
Cozy white home interior. A family builds a large shield from five tiles, each with an icon: key (passkey), cloud with arrow (backup), stop hand (block), phone with return arrow (call back), vault (password manager). Grandma holds a phone with a green check. Outside the window the X1 silhouette shrugs and walks away.
+ 공통 꼬리말
```

### 9장 · 함께 만드는 안전한 AI 사회 — `assets/covers/ch09.webp`
```
Top-down town map with many tiny buildings linked by glowing lines. Some buildings wear green shields and stop a red wave from spreading. The professor plants a flag at the threshold where the wave stops. Two company buildings shake hands over a coin labeled "+". The X2 silhouette looks frustrated at a blocked hub building.
+ 공통 꼬리말
```

### 10장 · 미래를 준비하는 디지털 생존 전략 (마지막 장) — `assets/covers/ch10.webp`
```
Bright white lab in morning light. The three silhouettes X1, X2, X3 tear up a giant red receipt showing a minus sign. The whole team stands behind a four-layer shield; the layers show icons: rulebook, carrot, stick, gavel. The professor holds a gavel in one hand and an abacus in the other. Pixel-square confetti.
+ 공통 꼬리말
```

## 3. 강화학습 시뮬레이션 공통 그림 — `assets/covers/rl.webp` (1200×800)

모든 장 마지막 단계(강화학습)에 같은 그림을 씁니다.

```
Game-board style lab table. A small agent token (a black silhouette pawn) stands at a fork with three paths: a green path to a "work desk", a gray path to an old phone, a red path to a server. Above each path floats a score number that changes. On the side, four toggle switches with icons (rulebook, gavel, stick, carrot); when the rulebook and gavel switches are ON, the red path's score turns negative and the pawn turns toward the green path. The fruit-fly researcher holds a stopwatch; the abacus robot plots a rising curve.
+ 공통 꼬리말
```

## 4. 실전 연습장 표지 — `practice/cover.webp` (1600×900)

```
Wide control-room scene in a white lab. Four tabs on a big wall screen, each a small scene: a call center with many phones, an office desk with an envelope, a server with a padlock, two buildings with shields. In front, intern Sia and intern Moa turn dials on a control panel (green dials and blue dials). The professor watches with arms crossed; the abacus robot shows a scoreboard with a green check and a red cross.
+ 공통 꼬리말
```

## 5. 표지에서 자를 것 (새로 그리지 않음)

| 용도 | 원본 | 크기 | 저장 이름 |
|---|---|---|---|
| 목차 썸네일 | 각 장 장면 | 600×400 | `assets/thumbs/chNN.webp` |
| 공유 미리보기(og:image) | 시리즈 표지 | 1200×630 | `assets/og/index.webp` |
| 장별 og:image | 각 장 장면 | 1200×630 | `assets/og/chNN.webp` |

## 6. 저장 이름 체크리스트

- [x] assets/covers/index.webp
- [x] assets/covers/ch00.webp ~ ch10.webp (11장)
- [x] assets/covers/rl.webp
- [x] practice/cover.webp
- [x] assets/thumbs/, assets/og/ (자르기)
