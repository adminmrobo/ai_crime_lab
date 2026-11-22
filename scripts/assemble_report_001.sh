#!/bin/sh
# 리포트 No.001 다시 만들기: 본문 → 꼬리표(지식 색인·꾸러미) → 점검
# 도구: github.com/adminmrobo/ahnboat_lab_explainer (packs/task/onto-retrofit, data/) 를 $ALE 에 받아 둔다.
set -e
ALE=${ALE:-/tmp/ale}; T=$ALE/packs/task/onto-retrofit/tools
R=reports/2026-11-23_lnrs-synthetic-identity-deepfake
python3 scripts/build_report_001.py
python3 scripts/kg_report_001.py
python3 $T/retrofit.py $R/kg/page.html --kg $R/kg/kg.json --refs $R/kg/refs.json --meta $R/kg/meta.json \
  --backbone $ALE/data/backbone_ai.json --js ../../assets/kgx.js -o $R/index.html
python3 $T/check.py $R/kg/page.html $R/index.html --backbone $ALE/data/backbone_ai.json \
  --registry $ALE/data/KG_00_registry.json --report $R/kg/check_report.md
