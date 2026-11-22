"""ahnboat.xyz 카탈로그용 카드 목록 catalog_cards.json 만들기 (표지 현황 사이트의 series_cards가 받아 감)
사용: python scripts/build_catalog_cards.py
"""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE, REPO = "https://adminmrobo.github.io/ai_crime_lab/", "https://github.com/adminmrobo/ai_crime_lab"


def meta(slug):
    t = (ROOT / "content" / f"{slug}.md").read_text(encoding="utf-8")
    fm = dict(re.findall(r"^(\w+):\s*(.+)$", t.split("\n---")[0], re.M))
    return fm


items = [
    {"folder": "", "kind": "index", "chap": "목차", "order": 0, "title": "목차 · AI 범죄 연구실",
     "summary": "『AI 범죄와 자기 방어』 사례 보충본 — 범죄자의 계산서를 범죄경제학·게임이론·AI 분석으로 계산하고, 제도와 습관으로 다시 뒤집어 봅니다.",
     "langs": ["ko"], "site_url": SITE, "repo_url": REPO, "thumb": SITE + "assets/og/index.webp"},
    {"folder": "ontology.html", "kind": "map", "chap": "지도", "order": 1, "title": "AI 범죄학 온톨로지 지도",
     "summary": "책의 분석 틀로 짠 13개 영역·49개 주제 위에, 책이 다룬 개념과 리포트로 확인된 개념을 겹쳐 보는 3D 지도입니다.",
     "langs": ["ko"], "site_url": SITE + "ontology.html", "repo_url": REPO, "thumb": SITE + "assets/thumbs/ontology.webp"},
]
for i in range(11):
    s = f"ch{i:02d}"
    m = meta(s)
    no = "서장" if i == 0 else f"{i}장"
    items.append({"folder": f"{s}.html", "kind": "chapter", "chap": no, "order": 10 + i, "title": f"{no} · {m['title']}",
                  "summary": m.get("subtitle", ""), "langs": ["ko"], "site_url": SITE + f"{s}.html", "repo_url": REPO,
                  "thumb": SITE + f"assets/thumbs/{s}.webp"})
items.append({"folder": "practice/", "kind": "practice", "chap": "실전", "order": 30, "title": "마지막 장 · 실전 연습장",
              "summary": "콜센터·검사 게임·랜섬 협상·기업 연결망 네 사업장을 직접 운영해 범죄자의 계산서를 뒤집어 봅니다.",
              "langs": ["ko"], "site_url": SITE + "practice/", "repo_url": REPO, "thumb": SITE + "practice/cover.webp"})
reg = json.loads((ROOT / "reports" / "registry.json").read_text(encoding="utf-8"))
items.append({"folder": "reports/", "kind": "index", "chap": "리포트", "order": 40, "title": "리포트·뉴스 검증 INDEX",
              "summary": "새로 나온 보고서와 뉴스를 책의 장과 나란히 놓고, 책의 분석이 현장에서 어떻게 확인되는지 쌓아 갑니다.",
              "langs": ["ko"], "site_url": SITE + "reports/", "repo_url": REPO,
              "thumb": SITE + f"reports/{reg['reports'][-1]['folder']}/thumb.webp"})
for k, r in enumerate(sorted(reg["reports"], key=lambda r: r["no"])):
    items.append({"folder": f"reports/{r['folder']}/", "kind": "report", "chap": "리포트", "order": 41 + k,
                  "title": f"리포트 No.{r['no']} · {r['title']}", "summary": r["summary"], "langs": ["ko"],
                  "site_url": SITE + f"reports/{r['folder']}/", "repo_url": REPO, "thumb": SITE + f"reports/{r['folder']}/thumb.webp"})
out = {"series": "AI 범죄 연구실 — 『AI 범죄와 자기 방어』 보충본", "rule": "AI 범죄학(crime) 분야. chap 값으로 카탈로그 소분류를 묶는다.",
       "items": items, "related": []}
(ROOT / "catalog_cards.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("cards", len(items))
