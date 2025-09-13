import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

// シンプルな Python モック（/hello のみ）
function startStubPython(port = 4010) {
  const server = http.createServer((req, res) => {
    try {
      const url = new URL(req.url, 'http://localhost');
      if (url.pathname === '/hello') {
        const name = url.searchParams.get('name') ?? 'world';
        const body = { message: `Hello, ${name} from python-api!` };
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify(body));
        return;
      }
      if (url.pathname === '/health') {
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({ ok: true, service: 'python-mock' }));
        return;
      }
      res.writeHead(404, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'Not Found' }));
    } catch (e) {
      res.writeHead(500, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: 'stub error', detail: String(e) }));
    }
  });
  return new Promise((resolveListen) => {
    server.listen(port, '127.0.0.1', () => resolveListen({ server, port }));
  });
}

async function waitForHttpOk(url, { timeoutMs = 5000 } = {}) {
  const start = Date.now();
  for (;;) {
    try {
      const resp = await fetch(url);
      if (resp.ok) return resp;
    } catch {}
    if (Date.now() - start > timeoutMs) throw new Error(`Timeout: ${url}`);
    await wait(150);
  }
}

const __dirname = dirname(fileURLToPath(import.meta.url));
const PKG_ROOT = resolve(__dirname, '..');

let stub;
let nodeProc;

before(async () => {
  // 1) Python モック起動
  stub = await startStubPython(4010);

  // 2) Node(BFF) を子プロセスで起動（テスト専用の固定ポート）
  nodeProc = spawn(process.execPath, ['src/index.js'], {
    cwd: PKG_ROOT,
    env: { ...process.env, PORT: '3031', PY_BASE: 'http://127.0.0.1:4010' },
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  // 3) 起動待ち（/health が 200 になるまで）
  await waitForHttpOk('http://127.0.0.1:3031/health', { timeoutMs: 8000 });
});

after(() => {
  try { nodeProc?.kill(); } catch {}
  try { stub?.server?.close(); } catch {}
});

test('GET /health returns 200 JSON', async () => {
  const resp = await fetch('http://127.0.0.1:3031/health');
  assert.equal(resp.status, 200);
  const json = await resp.json();
  assert.deepEqual(json, { ok: true, service: 'node-api' });
});

test('GET /api/py/hello proxies to python', async () => {
  const resp = await fetch('http://127.0.0.1:3031/api/py/hello?name=masan');
  assert.equal(resp.status, 200);
  const json = await resp.json();
  assert.deepEqual(json, { message: 'Hello, masan from python-api!' });
});

