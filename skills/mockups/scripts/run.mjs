#!/usr/bin/env node
// Bounded headless rendering and heuristic audit. Node 22+ and Chrome required.
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const usage = 'usage: node run.mjs <file.html> [--widths 375,768,1280] [--out dir] [--timeout-ms 15000] [--max-height 12000] [--report-only]';
let chrome, ws, profile;
const pending = new Map();
const eventWaiters = new Set();
let nextId = 0;
let timeoutMs = 15000;
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const bounded = (promise, label, ms = timeoutMs) => new Promise((resolve, reject) => {
  const timer = setTimeout(() => reject(new Error(`${label} timed out after ${ms}ms`)), ms);
  Promise.resolve(promise).then(resolve, reject).finally(() => clearTimeout(timer));
});
const rejectPending = (error) => {
  for (const entry of pending.values()) { clearTimeout(entry.timer); entry.reject(error); }
  pending.clear();
  for (const waiter of eventWaiters) { clearTimeout(waiter.timer); waiter.reject(error); }
  eventWaiters.clear();
};
function send(method, params = {}) {
  return new Promise((resolve, reject) => {
    if (ws?.readyState !== WebSocket.OPEN) { reject(new Error('Chrome connection is closed')); return; }
    const id = ++nextId;
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`${method} timed out after ${timeoutMs}ms`)); }, timeoutMs);
    pending.set(id, { resolve, reject, timer });
    try { ws.send(JSON.stringify({ id, method, params })); }
    catch (error) { clearTimeout(timer); pending.delete(id); reject(error); }
  });
}
function once(method) {
  let waiter;
  const promise = new Promise((resolve, reject) => {
    waiter = { method, resolve, reject, timer: setTimeout(() => {
      eventWaiters.delete(waiter); reject(new Error(`${method} timed out after ${timeoutMs}ms`));
    }, timeoutMs) };
    eventWaiters.add(waiter);
  });
  return { promise, cancel() { clearTimeout(waiter.timer); eventWaiters.delete(waiter); } };
}
async function evaluate(expression) {
  const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || 'Page evaluation failed');
  return r.result.value;
}
async function ready() {
  await evaluate(`(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(img => img.complete ? Promise.resolve() : new Promise(resolve => {
      img.addEventListener('load', resolve, { once: true });
      img.addEventListener('error', resolve, { once: true });
    })));
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  })()`);
}
async function cleanup() {
  rejectPending(new Error('Renderer stopped'));
  ws?.close();
  if (chrome && chrome.exitCode === null && chrome.signalCode === null) {
    const exited = new Promise(resolve => chrome.once('exit', resolve));
    chrome.kill('SIGTERM');
    await bounded(exited, 'Chrome shutdown', 1500).catch(() => {});
    if (chrome.exitCode === null && chrome.signalCode === null) {
      chrome.kill('SIGKILL');
      await bounded(exited, 'Chrome shutdown', 1500).catch(() => {});
    }
  }
  // Remove only the isolated browser profile created by this invocation.
  if (profile && (!chrome || chrome.exitCode !== null || chrome.signalCode !== null)) rmSync(profile, { recursive: true, force: true });
}
for (const [signal, code] of [['SIGINT', 130], ['SIGTERM', 143]]) {
  process.once(signal, () => { cleanup().finally(() => process.exit(code)); });
}

async function main() {
  const options = {};
  let file, reportOnly = false;
  for (let i = 2; i < process.argv.length; i++) {
    const arg = process.argv[i];
    if (arg === '--report-only') reportOnly = true;
    else if (['--widths', '--out', '--timeout-ms', '--max-height'].includes(arg)) {
      const value = process.argv[++i];
      if (!value || value.startsWith('--')) throw new Error(usage);
      options[arg] = value;
    } else if (arg.startsWith('--') || file) throw new Error(usage);
    else file = arg;
  }
  if (!file || !existsSync(file)) throw new Error(usage);
  timeoutMs = Number(options['--timeout-ms'] || 15000);
  const maxHeight = Number(options['--max-height'] || 12000);
  const widths = (options['--widths'] || '375,768,1280').split(',').map(Number);
  if (![timeoutMs, maxHeight, ...widths].every(n => Number.isSafeInteger(n) && n > 0)) throw new Error('Widths, timeout and maximum height must be positive integers');
  const chromePath = [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find(p => p && existsSync(p));
  if (!chromePath) throw new Error('Chrome not found. Set CHROME_PATH, or use the in-page audit with the available browser.');
  const outDir = resolve(options['--out'] || mkdtempSync(join(tmpdir(), 'mockup-shots-')));
  mkdirSync(outDir, { recursive: true });
  const auditSrc = readFileSync(join(dirname(fileURLToPath(import.meta.url)), 'audit.js'), 'utf8');
  const url = pathToFileURL(resolve(file)).href;
  profile = mkdtempSync(join(tmpdir(), 'mockup-chrome-'));
  let startupError;
  chrome = spawn(chromePath, ['--headless=new', '--remote-debugging-port=0', '--remote-debugging-address=127.0.0.1', `--user-data-dir=${profile}`, '--no-first-run', '--hide-scrollbars', '--allow-file-access-from-files', 'about:blank'], { stdio: 'ignore' });
  chrome.on('error', error => { startupError = error; rejectPending(error); });
  chrome.on('exit', () => rejectPending(new Error('Chrome exited before rendering completed')));
  const deadline = Date.now() + timeoutMs;
  let socketUrl;
  while (Date.now() < deadline && !socketUrl) {
    if (startupError) throw startupError;
    if (chrome.exitCode !== null || chrome.signalCode !== null) throw new Error('Chrome exited during startup');
    try {
      const port = readFileSync(join(profile, 'DevToolsActivePort'), 'utf8').split('\n')[0];
      const tabs = await (await fetch(`http://127.0.0.1:${port}/json`, { signal: AbortSignal.timeout(Math.max(1, deadline - Date.now())) })).json();
      socketUrl = tabs.find(tab => tab.type === 'page')?.webSocketDebuggerUrl;
    } catch { /* Browser may still be starting. */ }
    if (!socketUrl) await sleep(100);
  }
  if (!socketUrl) throw new Error('Chrome startup timed out');
  ws = new WebSocket(socketUrl);
  ws.addEventListener('close', () => rejectPending(new Error('Chrome connection closed')));
  ws.addEventListener('error', () => rejectPending(new Error('Chrome connection failed')));
  await bounded(new Promise((resolve, reject) => {
    ws.addEventListener('open', resolve, { once: true });
    ws.addEventListener('error', () => reject(new Error('Chrome connection failed')), { once: true });
    ws.addEventListener('close', () => reject(new Error('Chrome connection closed')), { once: true });
  }), 'Chrome connection');
  const consoleErrors = new Set();
  ws.addEventListener('message', message => {
    const data = JSON.parse(message.data);
    const entry = pending.get(data.id);
    if (entry) {
      clearTimeout(entry.timer); pending.delete(data.id);
      data.error ? entry.reject(new Error(data.error.message)) : entry.resolve(data.result);
    } else if (data.method) {
      for (const waiter of eventWaiters) if (waiter.method === data.method) {
        clearTimeout(waiter.timer); eventWaiters.delete(waiter); waiter.resolve(data.params);
      }
      if (data.method === 'Runtime.exceptionThrown') consoleErrors.add(data.params.exceptionDetails.exception?.description || data.params.exceptionDetails.text);
    }
  });
  await send('Page.enable');
  await send('Runtime.enable');
  async function open(width) {
    await send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: width <= 480 });
    const loaded = once('Page.loadEventFired');
    try {
      await Promise.all([loaded.promise, send('Page.navigate', { url }).then(result => {
        if (result.errorText) throw new Error(`Navigation failed: ${result.errorText}`);
      })]);
      await ready();
    } finally { loaded.cancel(); }
  }
  await open(widths[widths.length - 1]);
  const states = (await evaluate(auditSrc)).states;
  const runs = states.length ? states : [null];
  const merged = new Map(), truncations = new Map(), shots = [], clipped = [];
  let fonts = {}, unknownContrast = 0;
  for (const width of widths) {
    await open(width);
    for (const [index, state] of runs.entries()) {
      if (state !== null) {
        await evaluate(`(() => {
          const state = ${JSON.stringify(state)};
          const button = [...document.querySelectorAll('[data-mockup-chrome] button[data-n]')].find(b => b.dataset.n === state);
          if (button) button.click();
          else if (document.documentElement.dataset.state !== state) throw new Error('State switcher missing for ' + state);
        })()`);
        await ready();
      }
      const report = await evaluate(auditSrc);
      const at = `${width}${state === null ? '' : '/' + state}`;
      fonts = { ...fonts, ...report.fonts }; unknownContrast = Math.max(unknownContrast, report.unknownContrast);
      for (const issue of report.issues) {
        const key = `${issue.rule}|${issue.el}|${issue.sev}`;
        const entry = merged.get(key) || { ...issue, at: [] };
        entry.at.push(at); merged.set(key, entry);
      }
      for (const [rule, count] of Object.entries(report.truncated)) truncations.set(`${at}/${rule}`, count);
      const metrics = await send('Page.getLayoutMetrics');
      const fullHeight = Math.ceil(metrics.cssContentSize.height);
      const height = Math.min(fullHeight, maxHeight);
      if (height < fullHeight) clipped.push(`${at}: captured ${height}px of ${fullHeight}px; increase --max-height`);
      const { data } = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width, height, scale: 1 } });
      const suffix = state === null ? '' : `-${index + 1}-${state.replace(/[^a-zA-Z0-9_-]/g, '_')}`;
      const path = join(outDir, `${width}${suffix}.png`);
      writeFileSync(path, Buffer.from(data, 'base64')); shots.push(path);
    }
  }
  const total = widths.length * runs.length;
  const list = [...merged.values()].sort((a, b) => a.sev === b.sev ? 0 : a.sev === 'error' ? -1 : 1);
  const errors = list.filter(issue => issue.sev === 'error').length;
  const lines = [
    `file: ${file}`, `widths: ${widths.join(',')}  states: ${states.join(',') || 'none'}`,
    `fonts: ${Object.keys(fonts).join(', ') || 'none'}`,
    `errors: ${errors}  warnings: ${list.length - errors}` + (unknownContrast ? `  (contrast unknown on ${unknownContrast} gradient/image backgrounds; check manually)` : ''),
    ...list.map(issue => `${issue.sev === 'error' ? 'ERROR' : 'warn '} ${issue.rule} | ${issue.el || 'page'} | ${issue.detail} | ${issue.at.length === total ? 'all' : issue.at.join(' ')}`),
    ...[...truncations].map(([key, count]) => `TRUNCATED findings: ${key}: ${count} additional findings omitted`),
    ...clipped.map(detail => `INCOMPLETE screenshot: ${detail}`),
    ...(consoleErrors.size ? ['script errors:', ...[...consoleErrors].map(error => '  ' + String(error).split('\n')[0])] : []),
    'screenshots:', ...shots.map(path => '  ' + path),
  ];
  console.log(lines.join('\n'));
  // Report-only suppresses findings failures, never navigation/connection failures.
  return !reportOnly && (errors || consoleErrors.size || clipped.length) ? 1 : 0;
}
try { process.exitCode = await main(); }
catch (error) { console.error(`Renderer failed: ${error.message}`); process.exitCode = 2; }
finally { await cleanup(); }
