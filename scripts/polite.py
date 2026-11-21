# -*- coding: utf-8 -*-
"""대사 존댓말 변환기 — 문장 끝을 '~습니다/~요'로 바꾼다. 지문에는 쓰지 않는다."""
import re

B0 = 0xAC00


def _split(ch):
    c = ord(ch) - B0
    if not (0 <= c < 11172):
        return None
    return c // 588, (c % 588) // 28, c % 28


def _join(i, m, f):
    return chr(B0 + i * 588 + m * 28 + f)


def _da(stem_last):
    """'X다'의 X(마지막 음절)를 받아 존댓말 어미로 바꾼 문자열을 돌려준다."""
    s = _split(stem_last)
    if s is None:
        return stem_last + "습니다"
    i, m, f = s
    if f == 0:                       # 크다→큽니다, 이다→입니다
        return _join(i, m, 17) + "니다"
    if f == 4:                       # 한다→합니다, 된다→됩니다
        return _join(i, m, 17) + "니다"
    return stem_last + "습니다"       # 있다→있습니다, 했다→했습니다


NOUNS = [" 예", "정찰대", "포장지", "문제", "방패", "관계", "구조", "근거", "증거", "차례", "데이터", "공공재", "계산서", "크기", "인센티브", "투자", "이야기",
         "그대로", "초", "원리", "심리", "자리", "장치", "하나", "이유", "도구", "과제", "기회", "구매", "가치", "무기", "비용", "확률", "수익", "처벌"]
OVR = [  # 먼저 적용하는 고정 치환(문장 끝)
    ("하시라", "하세요"), ("아니야", "아니에요"), ("는가", "는 걸까요"),
    ("는다", "습니다"), ("거야", "거예요"), ("이야", "이에요"), ("겠군", "겠군요"), ("구나", "군요"),
    ("다니", "다니요"), ("거든", "거든요"), ("잖아", "잖아요"), ("는데", "는데요"), ("인데", "인데요"),
    ("말고", "말고요"), ("라고", "라고요"),
]
SIMPLE = {"해": "해요", "봐": "보세요", "돼": "돼요", "줘": "줘요", "둬": "둬요", "와": "와요", "가": "가요", "져": "져요",
          "지": "죠", "군": "군요", "네": "네요", "어": "어요", "아": "아요", "워": "워요", "래": "래요", "게": "게요", "까": "까요",
          "나": "나요", "니": "나요", "야": "예요", "자": "죠", "고": "고요", "서": "서요", "도": "도요", "며": "며요",
          "쳐": "쳐요", "여": "여요", "라": "라요", "혀": "혀요", "춰": "춰요", "켜": "켜요", "새": "새요", "려": "려요", "퍼": "퍼요", "떠": "떠요",
          "써": "써요", "꿔": "꿔요", "눠": "눠요", "겨": "겨요", "내": "내요", "개": "개요", "세": "세요", "해서": "해서요"}
POLITE_END = ("요", "니다", "죠", "세요", "습니까", "까요")


def _end(sent):
    pm = re.match(r"^(.*?)(\([^()]*\))([.!?]*)(\s*)$", sent, re.S)
    if pm and pm.group(1).strip():
        return _end(pm.group(1)) + pm.group(2) + pm.group(3) + pm.group(4)
    m = re.match(r"^(.*?)([.!?…]*)(\s*)$", sent, re.S)
    body, punct, sp = m.group(1), m.group(2), m.group(3)
    b = body.rstrip()
    tail = body[len(b):]
    if b.endswith("아니다"):
        return b[:-3] + "아닙니다" + tail + punct + sp
    if not b or b.endswith(POLITE_END) or not ("가" <= b[-1] <= "힣"):
        return sent
    for a, r in OVR:
        if b.endswith(a):
            return b[: -len(a)] + r + tail + punct + sp
    if b.endswith("다") and len(b) >= 2:
        stem = b[:-1]
        if not ("가" <= stem[-1] <= "힣") or any(stem.endswith(n) for n in NOUNS):
            return stem + "입니다" + tail + punct + sp
        return b[:-2] + _da(b[-2]) + tail + punct + sp
    last = b[-1]
    if last in SIMPLE:
        if last == "야":
            prev = _split(b[-2]) if len(b) >= 2 else None
            rep = ("이에요" if prev and prev[2] else "예요")
            return b[:-1] + rep + tail + punct + sp
        return b[:-1] + SIMPLE[last] + tail + punct + sp
    if b.endswith("같이"):
        return b + "요" + tail + punct + sp
    if last in "서로에도만지게면고럼말요걸":
        return b + "요" + tail + punct + sp
    fin = _split(last)
    return b + ("이에요" if fin and fin[2] else "예요") + tail + punct + sp  # 명사로 끝나는 문장


PRON = [("나는 ", "저는 "), ("나도 ", "저도 "), ("나에게", "저에게"), ("내가 ", "제가 "), ("내 계산", "제 계산"), ("내 사업", "제 사업"),
        ("내 담당", "제 담당"), ("내 쪽", "제 쪽"), ("내 선택", "제 선택"), ("나를 ", "저를 "), ("나한테", "저한테"), ("우리는 범죄자", "저희는 범죄자")]


def polite(text):
    if not text:
        return text
    t = text
    for a, b in PRON:
        t = t.replace(a, b)
    # 마크다운 굵게 표시 안의 문장 끝도 처리되도록, 문장 단위로 나눈다
    parts = re.split(r"(?<=[.!?])(\s+)", t)
    out = []
    for p in parts:
        if p.strip() == "":
            out.append(p)
            continue
        # 문장이 ** 또는 ) 로 끝나면 그 앞을 기준으로 바꾼다
        m = re.match(r"^(.*?)((?:\*\*|'|\")*)([.!?]*)$", p, re.S)
        core, wrap, pun = m.group(1), m.group(2), m.group(3)
        if pun or p is parts[-1]:
            out.append(_end(core) + wrap + pun if wrap else _end(core + pun))
        else:
            out.append(p)
    return "".join(out)


if __name__ == "__main__":
    for s in ["서장은 두 장면에서 출발한다. 둘 다 피해자가 '피싱을 알고 있었고, 의심도 했다'는 공통점이 있다. 그런데도 속았다. 이 장은 그 이유를 묻는다.",
              "나는 계산한다. 남으면 하고, 안 남으면 안 한다.", "정말 무조건일까? 아래 계산기에서 눌러 봐.", "목소리는 이제 몇 초 녹음으로 복제돼. 확실한 건 '다시 걸어 보기'뿐이야.",
              "다섯 명을 만들었는데 콜백 한 통에 끝나다니.", "모양을 바꿔도 하는 짓은 못 바꾸는군.", "공짜 정찰대가 사라지는군.", "**계산은 진짜처럼 한다.**", "그럼 나는 돈을 옮길 일도 없겠지."]:
        print(polite(s))
