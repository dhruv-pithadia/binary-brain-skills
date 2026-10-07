// In-page audit for mockups. Evaluates to a JSON-able report (no side effects).
// Run via scripts/run.mjs, or paste into preview_evaluate / a browser console.
(() => {
  const issues = [];
  const perRule = {};
  const MAX_PER_RULE = 8;
  const skipChrome = (el) => !!el.closest('[data-mockup-chrome]');

  const sel = (el) => {
    const parts = [];
    for (let n = el, d = 0; n && n.nodeType === 1 && n !== document.body && d < 3; n = n.parentElement, d++) {
      let s = n.tagName.toLowerCase();
      if (n.id) { parts.unshift(`${s}#${n.id}`); break; }
      const c = [...n.classList].slice(0, 2).join('.');
      if (c) s += '.' + c;
      parts.unshift(s);
    }
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 24);
    return parts.join(' > ') + (t ? ` "${t}"` : '');
  };
  const add = (rule, el, detail, sev = 'error') => {
    perRule[rule] = (perRule[rule] || 0) + 1;
    if (perRule[rule] <= MAX_PER_RULE) issues.push({ rule, sev, el: el ? sel(el) : '', detail });
  };

  const visible = (el) => {
    if (skipChrome(el)) return false;
    const r = el.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return false;
    const cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0;
  };

  // ---- color helpers (canvas resolves any CSS color syntax, including oklch) ----
  const cv = document.createElement('canvas').getContext('2d', { willReadFrequently: true });
  cv.canvas.width = cv.canvas.height = 1;
  const cache = new Map();
  const rgba = (str) => {
    if (cache.has(str)) return cache.get(str);
    cv.clearRect(0, 0, 1, 1);
    cv.fillStyle = '#000';
    cv.fillStyle = str;
    cv.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = cv.getImageData(0, 0, 1, 1).data;
    const v = [r, g, b, a / 255];
    cache.set(str, v);
    return v;
  };
  const over = (top, bottom) => {
    const a = top[3] + bottom[3] * (1 - top[3]);
    if (a === 0) return [0, 0, 0, 0];
    return [0, 1, 2].map((i) => (top[i] * top[3] + bottom[i] * bottom[3] * (1 - top[3])) / a).concat(a);
  };
  const lum = ([r, g, b]) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => {
    const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
    return (x + 0.05) / (y + 0.05);
  };
  let unknownContrast = 0;
  const effectiveBg = (el) => {
    const layers = [];
    for (let n = el; n; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage !== 'none') return null; // gradient or image: cannot judge
      const c = rgba(cs.backgroundColor);
      if (c[3] > 0) layers.push(c);
      if (c[3] === 1) break;
    }
    let out = [255, 255, 255, 1];
    for (let i = layers.length - 1; i >= 0; i--) out = over(layers[i], out);
    return out;
  };
  const effOpacity = (el) => {
    let o = 1;
    for (let n = el; n; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity);
    return o;
  };

  // ---- contrast ----
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let t; (t = walker.nextNode()); ) {
    if (!t.nodeValue.trim()) continue;
    const el = t.parentElement;
    if (!el || seen.has(el) || ['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName) || !visible(el)) continue;
    seen.add(el);
    if (el.closest(':disabled,[aria-disabled="true"]')) continue;
    const cs = getComputedStyle(el);
    const bg = effectiveBg(el);
    if (!bg) { unknownContrast++; continue; }
    let fg = rgba(cs.color);
    const op = effOpacity(el);
    fg = over([fg[0], fg[1], fg[2], fg[3] * op], bg);
    const r = ratio(fg, bg);
    const size = parseFloat(cs.fontSize);
    const large = size >= 24 || (size >= 18.66 && parseInt(cs.fontWeight, 10) >= 700);
    const need = large ? 3 : 4.5;
    if (r < need) add('contrast', el, `${r.toFixed(2)}:1, needs ${need}:1 (${size}px)`);
  }

  // ---- horizontal overflow and clipping ----
  const vw = window.innerWidth;
  if (document.documentElement.scrollWidth > vw + 1) {
    add('horizontal-scroll', document.documentElement, `page is ${document.documentElement.scrollWidth}px wide in a ${vw}px viewport`);
  }
  for (const el of document.body.querySelectorAll('*')) {
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    if (cs.position !== 'fixed' && el.getBoundingClientRect().right > vw + 1 && !el.closest('[style*="overflow-x"],.overflow-x-auto')) {
      let scroller = false;
      for (let n = el.parentElement; n && n !== document.body; n = n.parentElement) {
        const ox = getComputedStyle(n).overflowX;
        if (ox === 'auto' || ox === 'scroll' || ox === 'hidden') { scroller = true; break; }
      }
      if (!scroller) add('past-viewport', el, `right edge at ${Math.round(el.getBoundingClientRect().right)}px of ${vw}px`);
    }
    if ((cs.overflowX === 'hidden' || cs.overflow === 'hidden') && el.scrollWidth > el.clientWidth + 1 && cs.textOverflow !== 'ellipsis' && el.children.length === 0) {
      add('clipped-text', el, `content ${el.scrollWidth}px in ${el.clientWidth}px box`, 'warn');
    }
  }

  // ---- interactive controls ----
  const INTERACTIVE = 'a[href],button,input:not([type=hidden]),select,textarea,summary,[role=button],[role=link],[role=tab],[role=switch],[role=checkbox],[role=menuitem],[tabindex]:not([tabindex="-1"])';
  const touch = vw <= 480;
  const textOf = (el) => (el.innerText || el.textContent || '').trim();
  const accName = (el) => {
    const lb = el.getAttribute('aria-labelledby');
    if (lb) { const s = lb.split(/\s+/).map((id) => document.getElementById(id)?.textContent || '').join(' ').trim(); if (s) return s; }
    const al = el.getAttribute('aria-label');
    if (al && al.trim()) return al.trim();
    if (el.labels && el.labels.length) return [...el.labels].map(textOf).join(' ').trim();
    if (el.tagName === 'INPUT' && ['button', 'submit', 'reset'].includes(el.type) && el.value) return el.value;
    const t = textOf(el);
    if (t) return t;
    const img = el.querySelector('img[alt]');
    if (img && img.alt.trim()) return img.alt.trim();
    return (el.getAttribute('title') || '').trim();
  };
  for (const el of document.querySelectorAll(INTERACTIVE)) {
    if (!visible(el)) continue;
    const isCheck = el.tagName === 'INPUT' && ['checkbox', 'radio'].includes(el.type);
    const box = (isCheck && el.closest('label')) || el;
    const r = box.getBoundingClientRect();
    const inline = el.tagName === 'A' && getComputedStyle(el).display === 'inline' && el.closest('p,li,span,td,dd');
    if (!inline && (r.width < 24 || r.height < 24)) add('target-size-preference', el, `${Math.round(r.width)}x${Math.round(r.height)}px; review spacing and WCAG exceptions before calling this a conformance failure`, 'warn');
    else if (touch && !inline && (r.width < 44 || r.height < 44)) add('target-size-touch', el, `${Math.round(r.width)}x${Math.round(r.height)}px on a phone, aim for 44`, 'warn');
    if (!accName(el)) {
      const isField = ['INPUT', 'SELECT', 'TEXTAREA'].includes(el.tagName);
      add(isField ? 'no-label' : 'no-name', el, isField ? 'form control has no label' : 'control has no accessible name');
    } else if (['INPUT', 'TEXTAREA'].includes(el.tagName) && !el.labels?.length && !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby') && el.placeholder) {
      add('placeholder-only-label', el, 'placeholder is the only label', 'warn');
    }
  }
  for (const img of document.querySelectorAll('img')) {
    if (skipChrome(img)) continue;
    if (!img.hasAttribute('alt')) add('img-alt', img, 'img has no alt attribute');
    if (img.complete && img.naturalWidth === 0) add('broken-image', img, 'image failed to load');
  }
  for (const el of document.querySelectorAll('div[onclick],span[onclick],li[onclick],td[onclick]')) {
    if (!el.getAttribute('role') && !el.closest('button,a')) add('non-semantic-control', el, 'clickable element is not a button or link', 'warn');
  }

  // ---- document structure ----
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(visible);
  const h1s = hs.filter((h) => h.tagName === 'H1').length;
  if (h1s !== 1) add('h1-count', null, `${h1s} h1 elements, expected 1`, 'warn');
  for (let i = 1; i < hs.length; i++) {
    const a = +hs[i - 1].tagName[1], b = +hs[i].tagName[1];
    if (b > a + 1) add('heading-skip', hs[i], `h${a} followed by h${b}`, 'warn');
  }
  if (!document.querySelector('main,[role=main]')) add('no-main', null, 'no main landmark', 'warn');
  if (!document.documentElement.lang) add('no-lang', null, 'html has no lang attribute', 'warn');
  if (!document.querySelector('meta[name=viewport]')) add('no-viewport', null, 'missing viewport meta, phones will render it zoomed out');
  if (!document.title.trim()) add('no-title', null, 'empty title', 'warn');

  // Static CSS inspection cannot establish visible keyboard focus. Browser defaults
  // may be sufficient, and an outline reset may be replaced by another indicator.
  let hasFocusRule = false, unreadableStyles = false, outlineReset = false;
  const inspectRules = (rules) => {
    for (const rule of rules) {
      if (rule.selectorText && /:focus(-visible|-within)?\b/.test(rule.selectorText)) {
        hasFocusRule = true;
        if (rule.style && (rule.style.outlineStyle === 'none' || rule.style.outlineWidth === '0px')) outlineReset = true;
      }
      if (rule.cssRules) inspectRules(rule.cssRules);
    }
  };
  for (const sheet of document.styleSheets) {
    try { inspectRules(sheet.cssRules); } catch { unreadableStyles = true; }
  }
  const focusDetail = outlineReset ? 'focus outline reset detected; confirm a visible replacement by keyboard' :
    unreadableStyles ? 'some stylesheets cannot be inspected; verify focus visibility by keyboard' :
    hasFocusRule ? 'focus selectors exist but visibility is unverified; check every control by keyboard' :
    'no custom focus selector detected; browser-default indicators may be sufficient, verify by keyboard';
  add('focus-review', null, focusDetail, 'warn');

  const pageBg = effectiveBg(document.body) || [255, 255, 255, 1];
  if (lum(pageBg) < 0.2 && !/dark/.test(getComputedStyle(document.documentElement).colorScheme)) {
    add('color-scheme', document.documentElement, 'dark page without color-scheme: dark, so native controls and scrollbars render light', 'warn');
  }

  // ---- content realism ----
  const body = document.body.innerText || '';
  const ph = body.match(/lorem ipsum|dolor sit|\bItem \d\b|sample text|john doe|jane doe|foo bar|\btest (user|data)\b|placeholder text|\bTODO\b|\bTBD\b/gi);
  if (ph) add('placeholder-content', null, `placeholder copy found: ${[...new Set(ph.map((s) => s.toLowerCase()))].slice(0, 5).join(', ')}`, 'warn');

  // ---- states and fonts (information) ----
  const states = [...new Set([...document.querySelectorAll('[data-state-view]')].flatMap((e) => e.dataset.stateView.split(/\s+/)))];
  if (!states.length) add('no-states', null, 'no [data-state-view] found; confirm empty, loading and error states are truly not applicable', 'warn');
  const fams = new Map();
  for (const el of seen) {
    const f = getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim();
    fams.set(f, (fams.get(f) || 0) + 1);
  }
  if (fams.size > 3) add('many-families', null, `${fams.size} font families in use: ${[...fams.keys()].join(', ')}`, 'warn');

  const more = Object.fromEntries(Object.entries(perRule).filter(([, n]) => n > MAX_PER_RULE).map(([k, n]) => [k, n - MAX_PER_RULE]));
  return {
    viewport: [vw, window.innerHeight],
    state: document.documentElement.dataset.state || null,
    states,
    fonts: Object.fromEntries(fams),
    unknownContrast,
    counts: { error: issues.filter((i) => i.sev === 'error').length, warn: issues.filter((i) => i.sev === 'warn').length },
    issues,
    truncated: more,
  };
})()
