/* AI 범죄 연구실 — 단계 실험 위젯·퀴즈·복사 (외부 라이브러리 없음) */
{
const $ = (s, r = document) => r.querySelector(s);
const fmt = (v, d = 1) => (Math.abs(v) >= 1000 ? Math.round(v).toLocaleString() : (+v.toFixed(d)).toLocaleString());

function sliders(box, defs, onchange) {
  const vals = {};
  const res = document.createElement('div'); res.className = 'res';
  defs.forEach(([k, label, min, max, step, val, unit, kind]) => {
    const row = document.createElement('div');
    row.className = 'ctl ' + (kind || 'dec');
    const id = box.dataset.w + '-' + k;
    row.innerHTML = `<label for="${id}">${label}</label><input type="range" id="${id}" min="${min}" max="${max}" step="${step}" value="${val}"><output for="${id}"></output>`;
    box.appendChild(row);
    const inp = row.querySelector('input'), out = row.querySelector('output');
    const upd = () => { vals[k] = +inp.value; out.textContent = inp.value + (unit || ''); };
    inp.addEventListener('input', () => { upd(); onchange(vals, res); });
    upd();
  });
  box.appendChild(res);
  onchange(vals, res);
  return res;
}
function bars(items, max) {
  const W = 520, h = 26, H = items.length * (h + 10) + 10;
  const m = max || Math.max(...items.map(i => Math.abs(i[1])), 1);
  return `<svg class="g" viewBox="0 0 ${W} ${H}" role="img" aria-label="결과 막대">` + items.map(([lab, v, col], i) => {
    const w = Math.max(2, Math.abs(v) / m * (W - 230));
    const y = 10 + i * (h + 10);
    return `<text x="8" y="${y + 18}" font-size="13" fill="#3b4450">${lab}</text><rect x="150" y="${y}" width="${w}" height="${h}" rx="4" fill="${col}"/><text x="${156 + w}" y="${y + 18}" font-size="13" fill="#1d2430">${fmt(v)}</text>`;
  }).join('') + '</svg>';
}

const W = {};
// 서장: 범죄자의 계산서 계산기
W.calc = box => {
  const res = sliders(box, [
    ['N', '하루 시도 수 N', 10, 5000, 10, 3000, '건'],
    ['pi', '성공 확률 π', 0.02, 1, 0.01, 0.3, '%'],
    ['g', '성공 1건 수익 g(만 원)', 50, 1000, 10, 300, ''],
    ['c', '시도 1건 비용 c(만 원)', 0.01, 3, 0.01, 0.03, ''],
    ['p', '성공 1건당 검거 확률 p', 0, 60, 1, 3, '%'],
    ['f', '처벌 금전 환산 f(만 원)', 0, 10000, 100, 3000, ''],
  ], (v, res) => {
    const s = v.N * v.pi / 100, net = s * (v.g - v.p / 100 * v.f) - v.N * v.c;
    res.innerHTML = `예상 성공 ${fmt(s, 2)}건 · 하루 순이익 <span class="big ${net > 0 ? 'pos' : 'neg'}">${fmt(net)}만 원</span><br>${net > 0 ? 'X1은 범죄를 <b>고른다</b>.' : 'X1은 범죄를 <b>접는다</b>.'}` +
      bars([['기대 수익', s * v.g, '#d6453d'], ['시도 비용', v.N * v.c, '#9aa3ad'], ['처벌 기대비용', s * v.p / 100 * v.f, '#3d63c9']]);
  });
  const note = document.createElement('p'); note.className = 'mute';
  note.textContent = '전통 수작업 사기로 바꾸려면 N=30, π=0.4%, g=500, c=2, p=25%로 놓아 보세요.';
  box.appendChild(note);
};
// 1장: 퍼널 곱셈
W.funnel = box => {
  const res = sliders(box, [
    ['r1', '① 열람 확률', 1, 100, 1, 54, '%'], ['r2', '② 클릭 확률', 1, 100, 1, 27, '%'],
    ['r3', '③ 정보 입력 확률', 1, 100, 1, 28, '%'], ['r4', '④ 송금 확률', 1, 100, 1, 22, '%'],
  ], (v, res) => {
    const N = 10000; const st = [N, N * v.r1 / 100]; st.push(st[1] * v.r2 / 100); st.push(st[2] * v.r3 / 100); st.push(st[3] * v.r4 / 100);
    const base = 10000 * .21 * .15 * .19 * .15;
    res.innerHTML = `1만 건 중 끝까지 송금: <span class="big pos">${fmt(st[4])}명</span> · 일반 문자(약 ${fmt(base)}명)의 <b>${fmt(st[4] / base)}배</b>` +
      bars([['발송', st[0], '#9aa3ad'], ['열람', st[1], '#f08a5d'], ['클릭', st[2], '#f08a5d'], ['정보 입력', st[3], '#d6453d'], ['송금', st[4], '#d6453d']], N);
  });
};
// 2장: 베커 모형
W.becker = box => {
  const Y = 3000;
  const ce = (p, g, f) => Math.exp(p * Math.log(Y - f) + (1 - p) * Math.log(Y + g)) - Y;
  const res = sliders(box, [
    ['p', '검거 확률 p', 0, 90, 1, 30, '%'], ['g', '수익 g(만 원)', 500, 8000, 100, 4000, ''],
    ['f', '처벌 환산 f(만 원, 소득 3,000 미만)', 0, 2900, 50, 1500, ''],
  ], (v, res) => {
    const gain = ce(v.p / 100, v.g, v.f);
    let lo = 0, hi = 1; for (let i = 0; i < 50; i++) { const m = (lo + hi) / 2; ce(m, v.g, v.f) > 0 ? lo = m : hi = m; }
    res.innerHTML = `합법 소득 대비 이득(확실성 등가): <span class="big ${gain > 0 ? 'pos' : 'neg'}">${fmt(gain)}만 원</span> → ${gain > 0 ? '범죄를 고른다' : '범죄를 고르지 않는다'}<br>이 g·f에서 손익분기 검거 확률 p* ≈ <b>${fmt(lo * 100)}%</b>`;
  });
};
// 3장: 신호 게임(베이즈)
W.bayes = box => {
  const res = sliders(box, [
    ['q', '다급한 전화가 진짜 가족일 사전 확률 q', 1, 90, 1, 20, '%'],
    ['s', '사기꾼이 확인 질문을 맞힐 확률 s', 0, 100, 1, 5, '%'],
  ], (v, res) => {
    const q = v.q / 100, s = v.s / 100, post = q * .98 / (q * .98 + (1 - q) * s || 1e-9);
    res.innerHTML = `질문을 맞혔을 때 진짜 가족일 확률: <span class="big ${post > .9 ? 'neg' : 'pos'}">${fmt(post * 100)}%</span> (질문 전 ${v.q}%)<br>${s > .3 ? '답이 쉽게 알려지는 질문이라 신호의 힘이 약하다.' : '사기꾼에게 비싼 신호라 진짜와 가짜가 갈린다.'}` +
      bars([['질문 전', q * 100, '#9aa3ad'], ['맞힌 뒤', post * 100, '#1f8a5b']], 100);
  });
};
// 4장: 검사 게임
W.inspect = box => {
  const res = sliders(box, [
    ['g', '사기 성공 수익 g', 50, 1000, 10, 300, ''], ['f', '확인에 걸렸을 때 손실 f', 100, 9000, 100, 3000, ''],
    ['k', '직원 확인 비용 k', 0.5, 30, 0.5, 3, ''], ['L', '뚫렸을 때 회사 피해 L', 50, 1000, 10, 300, ''],
  ], (v, res) => {
    const y = v.g / (v.g + v.f), x = v.k / v.L;
    res.innerHTML = `균형 확인 비율 y* = <b>${fmt(y * 100)}%</b> · 균형 공격 비율 x* = <span class="big pos">${fmt(x * 100, 2)}%</span><br>처벌 f는 y*만, 확인 비용 k는 x*를 움직인다.` +
      bars([['직원 확인 y*', y * 100, '#1f8a5b'], ['사기 시도 x*', x * 100, '#d6453d']], 100);
  });
};
// 5장: 이상 탐지 기준점
W.detect = box => {
  const erf = x => { const t = 1 / (1 + .3275911 * Math.abs(x)); const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - .284496736) * t + .254829592) * t * Math.exp(-x * x); return x >= 0 ? y : -y; };
  const P = (x, m, s) => .5 * (1 - erf((x - m) / (s * Math.SQRT2)));
  const res = sliders(box, [['t', '경보 기준점(이상 점수)', 0.5, 7, 0.1, 4, '']], (v, res) => {
    const tp = 100 * P(v.t, 5, 1.2), fp = 4900 * P(v.t, 1.2, .8);
    const rec = tp, pre = tp / (tp + fp || 1e-9) * 100;
    res.innerHTML = `잡은 공격 ${fmt(tp)}건 / 100건 · 헛경보 ${fmt(fp)}건<br>재현율 <span class="big">${fmt(rec)}%</span> · 정밀도 <span class="big">${fmt(pre)}%</span>` +
      bars([['재현율', rec, '#d6453d'], ['정밀도', pre, '#3d63c9'], ['헛경보 수', fp, '#9aa3ad']], Math.max(100, fp));
  });
};
// 6장: 재식별
W.reid = box => {
  const attrs = [['시군구', 250], ['출생연도', 58], ['성별', 2], ['출생월', 12], ['직업군', 20], ['차종', 30]];
  const wrap = document.createElement('div'); wrap.className = 'chk';
  attrs.forEach(([n, k], i) => { wrap.insertAdjacentHTML('beforeend', `<label><input type="checkbox" data-k="${k}" ${i < 3 ? 'checked' : ''}> ${n}(${k}가지)</label>`); });
  box.appendChild(wrap);
  const res = document.createElement('div'); res.className = 'res'; box.appendChild(res);
  const run = () => {
    const K = [...wrap.querySelectorAll('input:checked')].reduce((a, c) => a * +c.dataset.k, 1);
    const u = Math.exp(-99999 / K) * 100;
    res.innerHTML = `가능한 조합 K = ${K.toLocaleString()}개 · 인구 10만 명 중 유일하게 특정될 비율 ≈ <span class="big pos">${fmt(u)}%</span>` + bars([['유일 비율', u, '#7a5bd1']], 100);
  };
  wrap.addEventListener('change', run); run();
};
// 7장: 랜섬 협상
W.ransom = box => {
  const res = sliders(box, [
    ['D', '복구 못 할 때 손실 D(억)', 1, 30, 1, 10, '', 'env'], ['E', '자료 유출 피해 E(억)', 0, 10, 0.5, 2, '', 'env'],
    ['t', '지급 시 약속을 지킬 확률 t', 10, 100, 5, 80, '%', 'env'], ['b', '백업으로 되살릴 비율 b', 0, 100, 5, 0, '%'],
  ], (v, res) => {
    const R = v.t / 100 * (v.D * (1 - v.b / 100) + v.E);
    res.innerHTML = `X2가 부를 수 있는 최대 몸값 R* ≈ <span class="big pos">${fmt(R, 2)}억 원</span><br>${v.b === 100 && v.E > 0 ? '백업 100%여도 유출 피해 E 때문에 몸값이 남는다.' : '백업 비율을 올리면 R*가 내려간다.'}` +
      bars([['복구 손실 몫', v.t / 100 * v.D * (1 - v.b / 100), '#d6453d'], ['유출 피해 몫', v.t / 100 * v.E, '#7a5bd1']], Math.max(1, v.t / 100 * (v.D + v.E)));
  });
};
// 8장: 보안 투자 최적점
W.invest = box => {
  const P = { 'SNS 활동형': 38.5, '온라인 금융형': 130, '재택 비즈니스형': 159 };
  const sel = document.createElement('div'); sel.className = 'chk';
  Object.keys(P).forEach((k, i) => sel.insertAdjacentHTML('beforeend', `<label><input type="radio" name="inv-p" value="${k}" ${i === 1 ? 'checked' : ''}> ${k}(L₀ ${P[k]}만 원)</label>`));
  box.appendChild(sel);
  let a = .05, L0 = 130;
  let res; sliders(box, [['a', '투자 효과 속도 a(1만 원당)', 0.01, 0.2, 0.01, 0.05, ''], ['x', '내 투자액 x(만 원)', 0, 100, 1, 20, '']], (v, r) => { res = r; a = v.a; draw(v.x); });
  function draw(x) {
    const xs = a * L0 > 1 ? Math.log(a * L0) / a : 0, tot = L0 * Math.exp(-a * x) + x, best = L0 * Math.exp(-a * xs) + xs;
    res.innerHTML = `최적 투자 x* ≈ <b>${fmt(xs)}만 원</b> (합계 ${fmt(best)}만 원) · 내 선택 합계 <span class="big ${tot - best < 2 ? 'neg' : 'pos'}">${fmt(tot)}만 원</span>` +
      bars([['아무것도 안 함', L0, '#9aa3ad'], ['내 선택', tot, '#3d63c9'], ['최적', best, '#1f8a5b']], L0);
  }
  sel.addEventListener('change', e => { L0 = P[e.target.value]; draw(+$('#' + box.dataset.w + '-x').value); });
};
// 9장: 죄수의 딜레마
W.pd = box => {
  const mat = document.createElement('div'); box.appendChild(mat);
  const res = sliders(box, [
    ['c', '투자 비용 c', 1, 20, 1, 10, '', 'env'], ['b', '나를 지키는 이익 b', 0, 20, 1, 6, '', 'env'],
    ['e', '상대에게 주는 이익 e', 0, 20, 1, 7, '', 'env'], ['s', '보조금 s', 0, 15, 0.5, 0, ''],
  ], (v, res) => {
    const pay = (me, ot) => (me ? v.b - v.c + v.s : 0) + (ot ? v.e : 0);
    const br = ot => pay(1, ot) >= pay(0, ot);
    const ne = [[1, 1], [1, 0], [0, 1], [0, 0]].filter(([a, b]) => br(b) === !!a && br(a) === !!b);
    const cell = (a, b) => `<div class="${ne.some(n => n[0] === a && n[1] === b) ? 'ne' : ''}">${fmt(pay(a, b))} , ${fmt(pay(b, a))}</div>`;
    mat.innerHTML = `<div class="mat"><div class="h">A \\ B</div><div class="h">B 투자</div><div class="h">B 안 함</div><div class="h">A 투자</div>${cell(1, 1)}${cell(1, 0)}<div class="h">A 안 함</div>${cell(0, 1)}${cell(0, 0)}</div>`;
    const ok = ne.some(n => n[0] && n[1]);
    res.innerHTML = `빨간 테두리가 내쉬 균형이다. ${ok ? '<span class="neg">둘 다 투자하는 균형</span>이 되었다.' : '<span class="pos">둘 다 투자하지 않는 균형</span>에 갇혀 있다.'} 투자가 언제나 나아지는 보조금: s ≥ c − b = <b>${fmt(Math.max(0, v.c - v.b))}</b>`;
  });
};
// 10장: 다섯 겹 계산서 뒤집기
W.flip = box => {
  const L = [['N', '속도 제한·이상 탐지 (N 3,000→900)'], ['pi1', '별도 채널 확인 습관 (π 0.3%→0.12%)'], ['pi2', '피싱 내성 인증·패스키 (π 절반)'], ['g', '지급정지·출금 지연 (g 300→120)'], ['p', '국제 공조·정보 공유 (p 3%→6%)']];
  const wrap = document.createElement('div'); wrap.className = 'chk';
  L.forEach(([k, n]) => wrap.insertAdjacentHTML('beforeend', `<label><input type="checkbox" data-k="${k}"> ${n}</label>`));
  box.appendChild(wrap);
  const res = document.createElement('div'); res.className = 'res'; box.appendChild(res);
  const run = () => {
    const on = k => wrap.querySelector(`[data-k=${k}]`).checked;
    const N = on('N') ? 900 : 3000; let pi = on('pi1') ? .0012 : .003; if (on('pi2')) pi /= 2;
    const g = on('g') ? 120 : 300, p = on('p') ? .06 : .03;
    const net = N * pi * (g - p * 3000) - N * .03;
    res.innerHTML = `X1의 하루 순이익: <span class="big ${net > 0 ? 'pos' : 'neg'}">${fmt(net)}만 원</span> → ${net > 0 ? '아직 남는 장사다.' : '밑지는 장사, 계산서가 뒤집혔다.'}` + bars([['순이익', net, net > 0 ? '#d6453d' : '#1f8a5b']], 1800);
  };
  wrap.addEventListener('change', run); run();
};

document.querySelectorAll('[data-w]').forEach(b => { const f = W[b.dataset.k]; if (f) try { f(b); } catch (e) { b.textContent = '실험을 불러오지 못했습니다.'; } });

// 퀴즈
document.querySelectorAll('.quiz').forEach(q => {
  const ans = +q.dataset.a, ex = q.querySelector('.ex');
  q.querySelectorAll('button').forEach((b, i) => b.addEventListener('click', () => {
    q.querySelectorAll('button').forEach((x, j) => { x.classList.remove('ok', 'no'); if (j === ans) x.classList.add('ok'); });
    if (i !== ans) b.classList.add('no');
    ex.hidden = false; ex.firstChild.textContent = i === ans ? '정답이에요. ' : '아쉬워요, 다시 볼까요? ';
  }));
});
// 복사
document.querySelectorAll('.copy').forEach(b => b.addEventListener('click', () => {
  const t = document.getElementById(b.dataset.t).innerText;
  navigator.clipboard.writeText(t).then(() => b.textContent = '복사됨').catch(() => b.textContent = '직접 선택해 복사하세요');
}));
}
