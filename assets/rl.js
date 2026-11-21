/* 강화학습 시뮬레이션 — 모든 장 공통 마지막 단계.
   에이전트는 도덕을 배우지 않는다. 보상(제도가 만든 인센티브·디스인센티브)만 보고 행동을 고른다. */
{
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const fmt = v => (Math.abs(v) >= 100 ? Math.round(v) : +v.toFixed(1)).toLocaleString();

// 보상 규칙 (단위: 만 원, 한 번의 선택)
function rewardFn(cfg, k, R) {
  if (cfg.kind === 'crime') {
    const p = k.enforce ? 0.35 : 0.05;                 // 강제력: 실제로 잡히는 확률
    const f = k.rule ? (k.stick ? 1500 : 600) : 0;      // 규칙이 없으면 잡혀도 처벌할 근거가 없다
    const legal = 100 + (k.carrot ? 120 : 0);           // 인센티브: 합법 선택의 보상
    const acts = [() => legal + (R() - 0.5) * 40];
    acts.push(() => (R() < 0.10 ? 1000 : 0) - 50 - (R() < p ? f : 0));            // 수작업 범죄
    acts.push(() => k.ai ? (R() < 0.30 ? 1000 : 0) - 20 - (R() < p ? f : 0) : -50); // AI 범죄(도구가 막히면 헛수고)
    return acts;
  }
  // 방어자: 성실히 지킨다(비용) vs 생략한다(가끔 사고 + 감사에 걸리면 제재)
  const audit = k.enforce ? 0.40 : 0.05, F = k.stick ? 100 : 40;
  return [() => -30 + (k.carrot ? 25 : 0) + (R() - 0.5) * 10,
          () => (R() < 0.10 ? -150 : 0) - (k.rule && R() < audit ? F : 0)];
}
function expected(cfg, k) {
  if (cfg.kind === 'crime') {
    const p = k.enforce ? .35 : .05, f = k.rule ? (k.stick ? 1500 : 600) : 0;
    return [100 + (k.carrot ? 120 : 0), 100 - 50 - p * f * 1, k.ai ? 300 - 20 - p * f : -50];
  }
  const audit = k.enforce ? .4 : .05, F = k.stick ? 100 : 40;
  return [-30 + (k.carrot ? 25 : 0), -15 - (k.rule ? audit * F : 0)];
}
function train(cfg, k, seed, episodes = 3000) {
  const R = rng(seed), acts = rewardFn(cfg, k, R), n = acts.length;
  const Q = new Array(n).fill(0), cnt = new Array(n).fill(0), hist = [], win = new Array(n).fill(0);
  for (let e = 0; e < episodes; e++) {
    const eps = Math.max(0.02, 0.3 * (1 - e / (episodes * 0.7)));
    let a; if (R() < eps) a = Math.floor(R() * n); else { a = 0; for (let i = 1; i < n; i++) if (Q[i] > Q[a]) a = i; }
    const r = acts[a](); cnt[a]++; Q[a] += (r - Q[a]) / cnt[a]; win[a]++;
    if ((e + 1) % 100 === 0) { hist.push(win.map(w => w / 100)); win.fill(0); }
  }
  return { Q, hist, last: hist.slice(-2).reduce((s, h) => s.map((v, i) => v + h[i] / 2), new Array(n).fill(0)) };
}
function chart(el, hist, names, cols) {
  const W = 640, H = 260, ml = 44, mr = 12, mt = 14, mb = 36, n = hist.length;
  const X = i => ml + i / Math.max(1, n - 1) * (W - ml - mr), Y = v => mt + (1 - v) * (H - mt - mb);
  let s = `<svg class="g" viewBox="0 0 ${W} ${H}" role="img" aria-label="학습 중 행동 선택 비율">`;
  [0, .25, .5, .75, 1].forEach(t => s += `<line x1="${ml}" x2="${W - mr}" y1="${Y(t)}" y2="${Y(t)}" stroke="#eef1f5"/><text x="${ml - 6}" y="${Y(t) + 4}" font-size="11" text-anchor="end" fill="#5b6572">${t * 100}%</text>`);
  names.forEach((nm, j) => { s += `<polyline fill="none" stroke="${cols[j]}" stroke-width="3" points="${hist.map((h, i) => X(i) + ',' + Y(h[j])).join(' ')}"/>`; });
  s += `<text x="${ml}" y="${H - 10}" font-size="11.5" fill="#3b4450">학습 회차(100회 단위) →</text>`;
  let lx = ml + 170; names.forEach((nm, j) => { s += `<rect x="${lx}" y="${H - 20}" width="14" height="8" fill="${cols[j]}"/><text x="${lx + 18}" y="${H - 12}" font-size="11.5" fill="#3b4450">${nm}</text>`; lx += 30 + nm.length * 11.5; });
  el.innerHTML = s + '</svg>';
}
const PRESETS = [['제도 없음', {}], ['규칙만', { rule: 1 }], ['규칙 + 처벌(집행 없음)', { rule: 1, stick: 1 }], ['집행만(규칙 없음)', { enforce: 1 }],
  ['규칙 + 집행', { rule: 1, enforce: 1 }], ['규칙 + 집행 + 처벌', { rule: 1, enforce: 1, stick: 1 }], ['인센티브만', { carrot: 1 }], ['네 가지 모두', { rule: 1, enforce: 1, stick: 1, carrot: 1 }]];

document.querySelectorAll('[data-rl]').forEach(box => {
  const cfg = JSON.parse(box.dataset.rl);
  const crime = cfg.kind === 'crime';
  const names = crime ? cfg.actions : cfg.actions, cols = crime ? ['#1f8a5b', '#9aa3ad', '#d6453d'] : ['#1f8a5b', '#d6453d'];
  const bad = crime ? [1, 2] : [1];
  const K = [['rule', '규칙', cfg.inst.rule], ['carrot', '인센티브', cfg.inst.carrot], ['stick', '디스인센티브', cfg.inst.stick], ['enforce', '강제력(집행)', cfg.inst.enforce]];
  box.innerHTML = `<div class="chk" style="flex-direction:column;gap:2px">${K.map(([k, t, d]) => `<label><input type="checkbox" data-k="${k}"> <b>${t}</b> — ${d}</label>`).join('')}
    ${crime ? '<label><input type="checkbox" data-k="ai" checked> <b>AI 도구 사용 가능</b> — 끄면 AI 범죄 선택이 헛수고가 된다</label>' : ''}</div>
    <p><button type="button" class="copy run">학습 시작 (3,000회)</button> <button type="button" class="copy cmp">제도별 비교 실험</button></p>
    <div class="out"></div><div class="cmpout"></div>`;
  const get = () => { const k = {}; box.querySelectorAll('input[data-k]').forEach(i => k[i.dataset.k] = i.checked); return k; };
  const out = box.querySelector('.out'), cmpout = box.querySelector('.cmpout');
  function report(k, res) {
    const share = bad.reduce((s, i) => s + res.last[i], 0);
    const pol = res.Q.indexOf(Math.max(...res.Q));
    const good = !bad.includes(pol);
    const lines = [
      ['doctor', good ? 'E16' : 'E09', '박사', good ? `학습이 끝났어요. ${cfg.agentName}은(는) '${names[pol]}'을(를) 골랐어요. 도덕을 가르친 적은 없습니다. 보상 구조가 바뀌었을 뿐이에요.` : `${cfg.agentName}은(는) 여전히 '${names[pol]}'을(를) 골라요. 어떤 제도가 빠졌는지 보세요. 규칙만 있고 집행이 없지는 않나요?`],
      ['jupanbot', 'E16', '주판봇', good ? '이제 범죄는 영원히 0이에요!' : '처벌만 더 세게 하면 바로 해결돼요!'],
      ['fruitfly', 'E09', '초파리 연구원', `마지막 200회 중 ${crime ? '범죄' : '생략'} 선택은 ${fmt(share * 100)}%예요. 이건 이 모형 안의 숫자일 뿐이라, 제도를 끄면 바로 되돌아가요. 비교 실험으로 확인해 보세요.`]];
    out.innerHTML = `<div class="res">마지막 200회의 ${crime ? '범죄' : '생략'} 선택 비율: <span class="big ${share > .5 ? 'pos' : 'neg'}">${fmt(share * 100)}%</span></div><div class="fig-rl"></div>
      <table class="parts"><tr><th>행동</th><th>배운 가치 Q(만 원)</th><th>기댓값(검산)</th></tr>${names.map((n, i) => `<tr><td>${n}</td><td>${fmt(res.Q[i])}</td><td>${fmt(expected(cfg, k)[i])}</td></tr>`).join('')}</table>` +
      lines.map(([d, e, n, t]) => `<div class="say"><img src="assets/chars/${d}/${e}.webp" alt="${n}" width="58" height="58"><div class="bub"><div class="who">${n}</div><div class="txt">${t}</div></div></div>`).join('');
    const fig = out.querySelector('.fig-rl');
    if (RM) { chart(fig, res.hist, names, cols); return; }
    let i = 1; const step = () => { chart(fig, res.hist.slice(0, i), names, cols); if (i++ < res.hist.length) requestAnimationFrame(step); }; step();
  }
  box.querySelector('.run').addEventListener('click', () => { const k = get(); report(k, train(cfg, k, 20261122)); });
  box.querySelector('.cmp').addEventListener('click', () => {
    const ai = crime ? box.querySelector('input[data-k=ai]').checked : false;
    const rows = PRESETS.map(([n, k]) => { const kk = { ...k, ai }; const r = train(cfg, kk, 20261122); return [n, bad.reduce((s, i) => s + r.last[i], 0)]; });
    cmpout.innerHTML = `<table class="parts"><tr><th>제도 조합</th><th>마지막 200회 ${crime ? '범죄' : '생략'} 선택 비율</th></tr>${rows.map(([n, v]) => `<tr><td>${n}</td><td style="color:${v > .5 ? '#d6453d' : '#1f8a5b'};font-weight:700">${fmt(v * 100)}%</td></tr>`).join('')}</table>
      <p class="mute">같은 난수 시드로 돌렸다. 규칙만 있거나 집행만 있을 때는 거의 바뀌지 않고, 규칙과 집행이 함께 있을 때 바뀌는지 확인해 보세요. 1~3% 정도 남는 값은 에이전트가 일부러 다른 행동을 해 보는 탐색(ε) 때문입니다.</p>`;
  });
});
}
