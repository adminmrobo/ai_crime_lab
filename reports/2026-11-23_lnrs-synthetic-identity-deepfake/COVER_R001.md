# 표지 지시문 — 리포트 검증 No.001 만들어진 신원과 딥페이크 사기

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_R001 · L (16:9, 1920 이상) |
| 그림체 | 16비트 RPG풍 픽셀아트 (필수, 고정) |
| 등장 | 박사 한 명 (연구실 리포트 동향편 규칙: 조수·초파리·주판봇·인턴·X1~X3 없음) |
| 장소 | 낮의 연구실 한쪽 벽, 큰 소식 게시판 앞 |
| 주제 은유 | 책상 위 작은 빈집 모형 하나에 얼굴 없는 종이 인형 카드 수십 장이 실로 이어져 있고, 우편함에는 편지가 넘친다(합성 신원·합성 주택). 게시판 옆 액자 화면에는 퍼즐 조각으로 맞춘 얼굴(딥페이크) |
| 박사 포즈 | 한 손에 접은 신문(글자 없음)을 들고 다른 손 검지로 빈집 모형을 가리키며 독자 쪽을 본다. 차분하게 설명하는 표정(E07 계열) |
| 대체 글 (alt) | 박사가 종이 인형 카드가 실로 이어진 빈집 모형과 퍼즐 얼굴 화면 앞에서 소식을 전하는 장면 |
| 다른 표지와 다른 점 | 책 장 표지는 연구실 식구 전원이 나오는 대결 전 장면 — 이 표지는 박사 혼자, 소식 게시판 앞 |

**참고 이미지 (함께 올리기):** 박사 기본 그림 1장(`assets/chars/doctor/E13.webp`)과 설명 표정 1장(`E07.webp`). 원본 기준: GitHub `adminmrobo/fruitfly-lab-expressions`.

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- 비율 16:9, 가로 1920px 이상
- 그림체는 반드시 16비트 RPG풍 픽셀아트 (네모 픽셀이 보이게, 매끈한 일러스트·벡터·수채화·3D 금지)
- 첨부한 참고 이미지의 박사 캐릭터를 같은 외형으로, 박사 한 명만 픽셀아트로 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것 (신문·게시판 종이도 글자 없이 회색 줄 무늬로만)
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게
아래 영어 프롬프트를 그대로 써 줘.

Website top cover illustration, wide 16:9.
Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2-3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.
Match the character's proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.
Bright daytime laboratory mood, soft natural sunlight through large windows, clean white walls, light lavender, mint and pink accents.
Scene: one corner of a tidy research lab, a large cork news board on the white wall with pinned blank papers and a few colored strings connecting them, a wooden desk in front.
Only one character: chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie; standing slightly right of center, holding a folded blank newspaper in one hand and pointing with the index finger of the other hand at the desk, looking toward the viewer with a calm explaining expression.
Visual metaphor of the topic: on the desk a small toy house with an empty window and an overflowing mailbox; dozens of faceless paper-doll cards are tied to the little house with thin red threads, like many invented people registered at one empty address; on the news board a framed screen shows a human face assembled from jigsaw puzzle pieces with one piece missing.
Composition: keep the face and hands inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain, bright and simple; the sunlight falls on the toy house and the paper-doll cards.
Mood: calm, factual news briefing, curious.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

**고칠 때 (같은 대화에서):** `Same character, same 16-bit pixel-art style and composition. Change only: {고칠 점}. Still pixel art, still no text.`

**받은 뒤 반영:** 원래 픽셀 격자를 찾아 정수배로만 키운 무손실 WebP `cover.webp`(가로 1600 이상, 300 KB 이하)로 이 폴더에 넣는다. 목록 카드용 `thumb.webp`는 표지에서 3:2로 잘라 만들고, 공유 미리보기 `og.webp`도 표지에서 만든다. 페이지 맨 위 소식 게시판 상자 자리를 그림으로 바꾼다.
