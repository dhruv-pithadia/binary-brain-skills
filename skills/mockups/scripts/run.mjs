#!/usr/bin/env node
// Render a mockup in headless Chrome at several widths and states, run audit.js,
// save screenshots, print one deduplicated report. No dependencies (Node 22+, Chrome).
// Usage: node run.mjs <file.html> [--widths 375,768,1280] [--out <dir>]
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith('--') && !/^\d/.test(a));
const opt = (name, dflt) => { const i = args.indexOf(`--${name}`); return i >= 0 ? args[i + 1] : dflt; };
if (!file || !existsSync(file)) { console.error('usage: node run.mjs <file.html> [--widths 375,768,1280] [--out dir]'); process.exit(2); }
const widths = opt('widths', '375,768,1280').split(',').map(Number);
const outDir = resolve(opt('out', mkdtempSync(join(tmpdir(), 'mockup-shots-'))));
mkdirSync(outDir, { recursive: true });
const auditSrc = readFileSync(join(dirname(fileURLToPath(import.meta.url)), 'audit.js'), 'utf8');
const url = pathToFileURL(resolve(file)).href;

const chromePath = [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find((p) => p && existsSync(p));
if (!chromePath) { console.error('Chrome not found. Set CHROME_PATH, or run audit.js through the T3 preview_evaluate tool.'); process.exit(2); }

const profile = mkdtempSync(join(tmpdir(), 'mockup-chrome-'));
const port = 9300 + Math.floor(Math.random() * 600);
const chrome = spawn(chromePath, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, '--no-first-run', '--hide-scrollbars', '--allow-file-access-from-files', 'about:blank'], { stdio: 'ignore' });
const cleanup = () => { try { chrome.kill(); } catch {} setTimeout(() => rmSync(profile, { recursive: true, force: true }), 300); };
process.on('exit', cleanup);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function connect() {
  for (let i = 0; i < 50; i++) {
    try {
      const tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
      const page = tabs.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(200);
  }
  throw new Error('could not connect to Chrome');
}
const ws = new WebSocket(await connect());
await new Promise((r) => (ws.onopen = r));
let id = 0; const pending = new Map(); const waiters = [];
ws.onmessage = (m) => {
  const d = JSON.parse(m.data);
  if (d.id && pending.has(d.id)) { const { res, rej } = pending.get(d.id); pending.delete(d.id); d.error ? rej(new Error(d.error.message)) : res(d.result); }
  else if (d.method) waiters.filter((w) => w.m === d.method).forEach((w) => w.r(d.params));
};
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
const once = (m) => new Promise((r) => waiters.push({ m, r }));
const evaluate = async (expression) => {
  const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || 'evaluate failed');
  return r.result.value;
};

await send('Page.enable'); await send('Runtime.enable');
const consoleErrors = [];
ws.addEventListener('message', (m) => {
  const d = JSON.parse(m.data);
  if (d.method === 'Runtime.exceptionThrown') consoleErrors.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
});

async function open(width) {
  await send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: width <= 480 });
  const loaded = once('Page.loadEventFired');
  await send('Page.navigate', { url });
  await Promise.race([loaded, sleep(4000)]);
  await sleep(300);
}

await open(widths[widths.length - 1]);
const states = (await evaluate(auditSrc)).states;
const runs = states.length ? states : [null];

const merged = new Map(); let fonts = {}; let unknownContrast = 0; const shots = [];
for (const w of widths) {
  await open(w);
  for (const s of runs) {
    if (s) { await evaluate(`document.querySelector('[data-mockup-chrome] button[data-n="${s}"]')?.click()`); await sleep(150); }
    const rep = await evaluate(auditSrc);
    fonts = { ...fonts, ...rep.fonts }; unknownContrast = Math.max(unknownContrast, rep.unknownContrast);
    for (const i of rep.issues) {
      const key = `${i.rule}|${i.el}`;
      const e = merged.get(key) || { ...i, at: [] };
      e.at.push(`${w}${s ? '/' + s : ''}`); merged.set(key, e);
    }
    const m = await send('Page.getLayoutMetrics');
    const h = Math.min(Math.ceil(m.cssContentSize.height), 4000);
    const { data } = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: w, height: h, scale: 1 } });
    const p = join(outDir, `${w}${s ? '-' + s : ''}.png`);
    writeFileSync(p, Buffer.from(data, 'base64')); shots.push(p);
  }
}

const total = widths.length * runs.length;
const list = [...merged.values()].sort((a, b) => (a.sev === b.sev ? 0 : a.sev === 'error' ? -1 : 1));
const lines = [
  `file: ${file}`,
  `widths: ${widths.join(',')}  states: ${states.join(',') || 'none'}`,
  `fonts: ${Object.keys(fonts).join(', ') || 'none'}`,
  `errors: ${list.filter((i) => i.sev === 'error').length}  warnings: ${list.filter((i) => i.sev === 'warn').length}` + (unknownContrast ? `  (contrast not judged on ${unknownContrast} gradient/image backgrounds: check by eye)` : ''),
  ...list.map((i) => `${i.sev === 'error' ? 'ERROR' : 'warn '} ${i.rule} | ${i.el || 'page'} | ${i.detail} | ${i.at.length === total ? 'all' : i.at.join(' ')}`),
  ...(consoleErrors.length ? ['script errors:', ...consoleErrors.map((e) => '  ' + String(e).split('\n')[0])] : []),
  'screenshots:', ...shots.map((p) => '  ' + p),
];
console.log(lines.join('\n'));
ws.close(); cleanup();
setTimeout(() => process.exit(0), 400);
