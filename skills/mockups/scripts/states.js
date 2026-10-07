// Inline this file in a <script> at the end of <body> in every mockup.
// Mark each state's markup with data-state-view="ideal", "empty loading", etc.
// Adds a small review switcher (not part of the design); #state=<name> deep-links a state.
(() => {
  const views = [...document.querySelectorAll('[data-state-view]')];
  const names = [...new Set(views.flatMap((e) => e.dataset.stateView.split(/\s+/)))];
  if (names.length < 2) return;
  const css = document.createElement('style');
  css.textContent = '[data-state-view][hidden]{display:none!important}';
  document.head.append(css);
  const bar = document.createElement('div');
  bar.setAttribute('data-mockup-chrome', '');
  bar.setAttribute('role', 'toolbar');
  bar.setAttribute('aria-label', 'Mockup state');
  bar.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:2147483647;display:flex;gap:2px;padding:3px;background:#111;border-radius:8px;font:12px/1 system-ui,sans-serif';
  const set = (n) => {
    views.forEach((e) => { e.hidden = !e.dataset.stateView.split(/\s+/).includes(n); });
    document.documentElement.dataset.state = n;
    bar.querySelectorAll('button').forEach((b) => {
      const on = b.dataset.n === n;
      b.setAttribute('aria-pressed', String(on));
      b.style.background = on ? '#fff' : 'transparent';
      b.style.color = on ? '#111' : '#fff';
    });
  };
  names.forEach((n) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = n;
    b.dataset.n = n;
    b.style.cssText = 'all:unset;cursor:pointer;color:#fff;padding:6px 9px;border-radius:5px';
    b.onclick = () => { set(n); history.replaceState(null, '', '#state=' + n); };
    bar.append(b);
  });
  document.body.append(bar);
  const want = (location.hash.match(/state=([\w-]+)/) || [])[1];
  set(names.includes(want) ? want : names[0]);
})();
