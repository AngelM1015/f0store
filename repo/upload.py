#!/usr/bin/env python3
"""Upload a built F0Store repository through the f0store-repo Worker.
usage: repo/upload.py <repo dir>      secret: $UPLOAD_SECRET (CI) or ~/.config/axi0/f0store-release/upload.secret

APKs and other files that are already live with the same size are skipped; the index files go last and entry.jar /
entry.json very last, so a client never sees an index that points at a file not uploaded yet."""
import hashlib
import os, sys, urllib.error, urllib.request

BASE = os.environ.get('F0STORE_REPO', 'https://axi0.tech/f0store/repo/')
SECRET = (os.environ.get('UPLOAD_SECRET') or open(os.path.expanduser('~/.config/axi0/f0store-release/upload.secret')).read()).strip()
# fdroidserver's own web page and build status are not part of what clients read: not published.
SKIP = ('index.html', 'index.css', 'index.png', 'status/')
LAST = ['index-v1.json', 'index-v1.jar', 'index-v2.json', 'entry.json', 'entry.jar']
UA = {'User-Agent': 'f0store-publish/1'}


def live_size(key):
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + key, method='HEAD', headers=UA), timeout=60) as r:
            return int(r.headers.get('content-length', -1))
    except urllib.error.HTTPError:
        return -1


def live_sha256(key):
    h = hashlib.sha256()
    with urllib.request.urlopen(urllib.request.Request(BASE + key, headers=UA), timeout=300) as r:
        for chunk in iter(lambda: r.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def put(key, path):
    data = open(path, 'rb').read()
    req = urllib.request.Request(BASE + key, data=data, method='PUT', headers={**UA, 'Authorization': 'Bearer ' + SECRET})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                r.read()
            break
        except Exception as e:  # noqa: BLE001 - retry any transport error
            if attempt == 3:
                raise
            print(f'  retry {key} ({e})', flush=True)
    print(f'{key}: {len(data)} bytes', flush=True)


def main(root):
    files = []
    for d, _, names in os.walk(root):
        for n in names:
            p = os.path.join(d, n)
            key = os.path.relpath(p, root).replace(os.sep, '/')
            if not key.startswith(SKIP):
                files.append((key, p))
    files.sort(key=lambda kp: (kp[0] in LAST and 1 + LAST.index(kp[0]) or 0, kp[0]))
    # Same size is not the same file: the index lists each file's SHA-256, so a skipped file must be the live bytes.
    # A different APK under a live name is refused before anything is sent (a version's file never changes); any
    # other changed file (an icon, a description) is sent again.
    todo, refused = [], []
    for key, path in files:
        if key not in LAST and not key.startswith('diff/') and live_size(key) == os.path.getsize(path):
            if live_sha256(key) == sha256(path):
                print(f'{key}: already live')
                continue
            if key.endswith('.apk'):
                refused.append(key)
                continue
        todo.append((key, path))
    if refused:
        sys.exit('refused: a different APK under a name that is already live: ' + ' '.join(refused))
    sent = 0
    for key, path in todo:
        put(key, path)
        sent += 1
    print(f'uploaded {sent} of {len(files)} files')


if __name__ == '__main__':
    main(sys.argv[1])
