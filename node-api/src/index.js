import http from "node:http";
import { URL } from "node:url";

const PORT = process.env.PORT || 3000;
const PY_BASE = process.env.PY_BASE || "http://127.0.0.1:8000";

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host}`);
    if (url.pathname === "/health") {
      res.writeHead(200, { "content-type": "application/json" });
      res.end(JSON.stringify({ ok: true, service: "node-api" }));
      return;
    }

    if (url.pathname.startsWith("/api/py")) {
      const targetPath = url.pathname.replace("/api/py", "") || "/";
      const targetUrl = `${PY_BASE}${targetPath}${url.search}`;
      const init = { method: req.method, headers: { ...req.headers } };
      delete init.headers["host"];
      if (req.method !== "GET" && req.method !== "HEAD") {
        const body = await new Promise((resolve, reject) => {
          const chunks = [];
          req.on("data", (c) => chunks.push(c));
          req.on("end", () => resolve(Buffer.concat(chunks)));
          req.on("error", reject);
        });
        init.body = body;
      }
      const resp = await fetch(targetUrl, init);
      res.writeHead(resp.status, Object.fromEntries(resp.headers));
      const buf = Buffer.from(await resp.arrayBuffer());
      res.end(buf);
      return;
    }

    res.writeHead(404, { "content-type": "application/json" });
    res.end(JSON.stringify({ error: "Not Found" }));
  } catch (err) {
    res.writeHead(500, { "content-type": "application/json" });
    res.end(JSON.stringify({ error: "Internal Server Error", detail: `${err}` }));
  }
});

server.listen(PORT, () => {
  console.log(`node-api listening on http://127.0.0.1:${PORT}`);
});
