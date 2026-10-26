// f0store-repo: serves the F0Store repository (F-Droid format: entry.jar, index-v2.json, APKs, icons) from R2 at
// axi0.tech/f0store/repo/<file>, with ranges and conditional requests, and lets the publish job upload behind a
// secret. No logs, no cookies, nothing about the visitor is kept.
const PREFIX = '/f0store/repo/';
const TYPES = {
  '.apk': 'application/vnd.android.package-archive', '.jar': 'application/java-archive',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.txt': 'text/plain; charset=utf-8', '.sha256': 'text/plain; charset=utf-8', '.xml': 'application/xml',
};
// Index files change on every publish: clients revalidate (ETag / Last-Modified) instead of trusting a cache.
const INDEX = /^(entry\.(jar|json)|index-v1\.(jar|json)|index-v2\.json|index\.(jar|xml)|diff\/[0-9]+\.json)$/;

function keyOf(url) {
  let k;
  try { k = decodeURIComponent(url.pathname.slice(PREFIX.length)); } catch { return null; }
  if (!/^[A-Za-z0-9._/=-]{1,200}$/.test(k) || k.includes('..') || k.startsWith('/') || k.endsWith('/')) return null;
  return k;
}
function typeOf(k) {
  const m = /\.[a-z0-9]+$/.exec(k);
  return (m && TYPES[m[0]]) || 'application/octet-stream';
}
function same(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}
const text = (s, status) => new Response(s + '\n', { status, headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff' } });

async function serve(req, env, key) {
  const head = req.method === 'HEAD';
  const obj = head ? await env.BUCKET.head(key) : await env.BUCKET.get(key, { range: req.headers, onlyIf: req.headers });
  if (!obj) return text('Not found', 404);
  const h = new Headers();
  h.set('content-type', typeOf(key));
  h.set('etag', obj.httpEtag);
  h.set('accept-ranges', 'bytes');
  h.set('cache-control', INDEX.test(key) ? 'no-cache' : 'public, max-age=86400');
  h.set('x-content-type-options', 'nosniff');
  h.set('last-modified', obj.uploaded.toUTCString());
  h.set('access-control-allow-origin', '*');
  if (key.endsWith('.apk')) h.set('content-disposition', `attachment; filename="${key.split('/').pop()}"`);
  if (head) { h.set('content-length', String(obj.size)); return new Response(null, { headers: h }); }
  if (!obj.body) return new Response(null, { status: 304, headers: h });
  if (obj.range && req.headers.get('range')) {
    const r = obj.range;
    const start = r.offset !== undefined ? r.offset : obj.size - r.suffix;
    const len = r.length !== undefined ? r.length : obj.size - start;
    h.set('content-range', `bytes ${start}-${start + len - 1}/${obj.size}`);
    h.set('content-length', String(len));
    return new Response(obj.body, { status: 206, headers: h });
  }
  h.set('content-length', String(obj.size));
  return new Response(obj.body, { headers: h });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (!url.pathname.startsWith(PREFIX)) return text('Not found', 404);
    const key = keyOf(url);
    if (!key) return text('Not found', 404);
    if (req.method === 'GET' || req.method === 'HEAD') return serve(req, env, key);
    const auth = req.headers.get('authorization') || '';
    if (!env.UPLOAD_SECRET || !same(auth, 'Bearer ' + env.UPLOAD_SECRET)) return text('Forbidden', 403);
    if (req.method === 'PUT') {
      const o = await env.BUCKET.put(key, req.body, { httpMetadata: { contentType: typeOf(key) } });
      return Response.json({ key, size: o.size, etag: o.etag });
    }
    if (req.method === 'DELETE') { await env.BUCKET.delete(key); return text('Deleted', 200); }
    return text('Method not allowed', 405);
  },
};
