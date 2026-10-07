import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync, existsSync, chmodSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { createServer } from 'node:http';

const chrome = [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find(p => p && existsSync(p));
if (process.env.REQUIRE_CHROME === '1' && !chrome) throw new Error('Chrome is required for renderer regression tests');
const runner = resolve('skills/mockups/scripts/run.mjs');
const states = readFileSync('skills/mockups/scripts/states.js', 'utf8');
const html = (body, css = '', script = '') => `<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mockup regression</title><style>body{margin:0;padding:24px;background:white;color:black;font:16px system-ui}button{min-width:44px;min-height:44px}main{max-width:600px}${css}</style></head><body><main><h1>Weekly planning</h1>${body}</main><script>${script}</script></body></html>`;
async function run(source, args = [], env = {}) {
  const dir = mkdtempSync(join(tmpdir(), 'mockup-test-'));
  const file = join(dir, 'index.html');
  writeFileSync(file, source);
  const child = spawn(process.execPath, [runner, file, '--widths', '375', '--out', join(dir, 'shots'), ...args], { env: { ...process.env, ...env } });
  let output = '';
  child.stdout.on('data', data => { output += data; });
  child.stderr.on('data', data => { output += data; });
  const kill = setTimeout(() => child.kill('SIGTERM'), 25000);
  try {
    const code = await new Promise((resolve, reject) => { child.once('error', reject); child.once('exit', resolve); });
    return { code, output, dir };
  } finally { clearTimeout(kill); }
}
const browserTest = (name, fn) => test(name, { skip: !chrome, timeout: 30000 }, async () => {
  const results = [];
  try { await fn(async (...args) => { const r = await run(...args); results.push(r); return r; }); }
  finally { for (const r of results) rmSync(r.dir, { recursive: true, force: true }); }
});

browserTest('captures long pages and preserves browser-default focus as manual review', async run => {
  const r = await run(html('<button>View session</button>', 'main{min-height:4500px}'));
  assert.equal(r.code, 0, r.output);
  assert.match(r.output, /browser-default indicators may be sufficient/);
  const png = readFileSync(join(r.dir, 'shots/375.png'));
  assert.ok(png.readUInt32BE(20) > 4000, 'page must not silently crop at 4000px');
});
browserTest('reports focus resets and small targets as qualified warnings', async run => {
  const r = await run(html('<button>View session</button>', 'button{min-width:0;min-height:0;width:20px;height:20px;font-size:6px}button:focus{outline:none}'));
  assert.equal(r.code, 0, r.output);
  assert.match(r.output, /focus outline reset detected/);
  assert.match(r.output, /target-size-preference/);
  assert.match(r.output, /WCAG exceptions/);
});
browserTest('audit and script errors fail, while report-only is explicit', async run => {
  const source = html('<button></button>', '', "throw new Error('fixture exception')");
  const failure = await run(source);
  assert.equal(failure.code, 1, failure.output);
  assert.match(failure.output, /ERROR no-name/);
  assert.match(failure.output, /fixture exception/);
  const report = await run(source, ['--report-only']);
  assert.equal(report.code, 0, report.output);
});
browserTest('reports repeated omitted findings and explicitly clipped screenshots', async run => {
  const r = await run(html('<button></button>'.repeat(12), 'main{min-height:1500px}'), ['--max-height', '1000']);
  assert.equal(r.code, 1, r.output);
  assert.match(r.output, /TRUNCATED findings: .*no-name: 4 additional/);
  assert.match(r.output, /INCOMPLETE screenshot: .*captured 1000px/);
});
browserTest('renders each state at each requested width with safely named outputs', async run => {
  const r = await run(html('<section data-state-view="ideal"><button>View session</button></section><section data-state-view="empty"><button>Schedule session</button></section>', '', states), ['--widths', '375,768']);
  assert.equal(r.code, 0, r.output);
  for (const width of [375, 768]) for (const [index, state] of ['ideal', 'empty'].entries()) {
    assert.ok(existsSync(join(r.dir, `shots/${width}-${index + 1}-${state}.png`)));
  }
});
browserTest('a stalled page load fails within its deadline, even in report-only mode', async run => {
  const sockets = new Set();
  const server = createServer((_req, res) => { res.writeHead(200, { 'Content-Type': 'image/png' }); res.write(Buffer.from([137, 80])); });
  server.on('connection', socket => { sockets.add(socket); socket.on('close', () => sockets.delete(socket)); });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  try {
    const r = await run(html(`<img alt="Session chart" src="http://127.0.0.1:${server.address().port}/hang">`), ['--timeout-ms', '5000', '--report-only']);
    assert.equal(r.code, 2, r.output);
    assert.match(r.output, /timed out/);
  } finally { for (const socket of sockets) socket.destroy(); await new Promise(resolve => server.close(resolve)); }
});
test('invalid invocation fails without launching a browser', async () => {
  const r = await run(html('<p>Ready</p>'), ['--widths', '0']);
  try { assert.equal(r.code, 2, r.output); assert.match(r.output, /positive integers/); }
  finally { rmSync(r.dir, { recursive: true, force: true }); }
});
test('early browser exit rejects startup without hanging', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'mockup-fake-browser-'));
  const fake = join(dir, 'chrome');
  writeFileSync(fake, '#!/bin/sh\nexit 1\n'); chmodSync(fake, 0o755);
  const r = await run(html('<p>Ready</p>'), [], { CHROME_PATH: fake });
  try { assert.equal(r.code, 2, r.output); assert.match(r.output, /Chrome exited during startup/); }
  finally { rmSync(r.dir, { recursive: true, force: true }); rmSync(dir, { recursive: true, force: true }); }
});
