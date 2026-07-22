import { createReadStream, existsSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = fileURLToPath(new URL("..", import.meta.url));
const distRoot = join(appRoot, "dist");
const host = process.env.WEB_HOST ?? "127.0.0.1";
const port = Number(process.env.WEB_PORT ?? "5173");
const contentTypes = {
  ".css": "text/css",
  ".html": "text/html",
  ".js": "text/javascript",
};

createServer((request, response) => {
  const path =
    request.url === "/"
      ? "index.html"
      : (request.url?.slice(1) ?? "index.html");
  const target = normalize(join(distRoot, path));
  if (!target.startsWith(distRoot) || !existsSync(target)) {
    response.writeHead(404, { "Content-Type": "text/plain" });
    response.end("Not found");
    return;
  }
  response.writeHead(200, {
    "Content-Type": contentTypes[extname(target)] ?? "application/octet-stream",
  });
  createReadStream(target).pipe(response);
}).listen(port, host, () => {
  console.log(`Tendy Spider web shell: http://${host}:${port}`);
});
