#!/usr/bin/env python3
"""Write the web shelf for axi0.tech/f0store from the picks register and the live repository index.

    python3 tools/web-shelf.py <axi0.tech site dir> [index-v2.json path or URL]

Writes <site>/f0store/index.html and <site>/f0store/licences.html. The download facts (version, size, SHA-256)
come from the signed repository's index-v2.json (default: the live one), so the page always names the file that is
actually served. The stylesheet <site>/f0store/f0store.css is linked with its own hash so a change reaches visitors.
"""
import hashlib
import html
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = 'https://axi0.tech/f0store/repo'
APK_CERT = '75920807E60E2896C2F9DD3799FA3C26BAAC7A66C0E72311E94EF469C315DE31'
REPO_FPR = 'F6C7C97F6DB494B837FB2633FA8F744DB935E8D5DAC65BBFC79E4855CD031205'
SOURCE = 'https://github.com/AngelM1015/f0store'
E = html.escape

ICON = ('<svg viewBox="0 0 64 64" aria-hidden="true" focusable="false"><rect width="64" height="64" rx="14" fill="#000"/>'
        '<g fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M18 24h28l-2 24a3 3 0 0 1-3 3H23a3 3 0 0 1-3-3z"/><path d="M25 24v-3a7 7 0 0 1 14 0v3"/></g>'
        '<circle cx="32" cy="37" r="4" fill="#f6a04d"/></svg>')


def load_index(src):
    if src.startswith('http'):
        with urllib.request.urlopen(urllib.request.Request(src, headers={'User-Agent': 'f0store-web/1'}), timeout=60) as r:
            return json.load(r)
    return json.load(open(src, encoding='utf-8'))


def head(title, desc, path, css):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://axi0.tech{path}">
<meta name="color-scheme" content="dark light">
<meta name="theme-color" content="#0e1012" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#f8f9fb" media="(prefers-color-scheme: light)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="axi0">
<meta property="og:url" content="https://axi0.tech{path}">
<meta property="og:title" content="{E(title.split(' · axi0')[0])}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="https://axi0.tech/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The axi0 concept drawn as three outlines around one orange dot.">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/instrument-sans-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/f0store/f0store.css?v={css}">
'''


def foot():
    return '''  <footer class="foot">
    <span>© 2026 axi0</span>
    <a href="/">axi0.tech</a>
    <a href="/f0store">F0Store</a>
    <a href="/f0store/licences">Credits and licences</a>
    <a href="/privacy">Privacy</a>
  </footer>
</main>
</body>
</html>
'''


def main():
    site = sys.argv[1]
    src = sys.argv[2] if len(sys.argv) > 2 else REPO + '/index-v2.json'
    picks = json.load(open(os.path.join(ROOT, 'docs/picks.json'), encoding='utf-8'))
    ix = load_index(src)
    app = ix['packages']['tech.axi0.f0store']
    v = max(app['versions'].values(), key=lambda x: x['manifest']['versionCode'])
    version, code = v['manifest']['versionName'], v['manifest']['versionCode']
    apk = v['file']['name'].lstrip('/')
    size, sha = v['file']['size'], v['file']['sha256'].upper()
    url = f'{REPO}/{apk}'
    mb = f'{size / 1048576:.1f} MB'
    out = os.path.join(site, 'f0store')
    css = hashlib.sha256(open(os.path.join(out, 'f0store.css'), 'rb').read()).hexdigest()[:10]

    rows = []
    for p in picks['picks']:
        af = ', '.join(p['antiFeatures'])
        mark = f' <span class="mark">marked {E(af)}</span>' if af else ''
        rows.append(f'        <tr><th scope="row">{E(p["instead_of"])}</th><td><a href="{E(p["source"])}">{E(p["name"])}</a>{mark}</td>'
                    f'<td>{E(p["role"])}</td><td><code>{E(p["license"])}</code></td></tr>')
    ld = {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication', '@id': 'https://axi0.tech/f0store#f0store',
        'name': 'F0Store', 'description': "axi0's store of free and open-source Android apps.",
        'applicationCategory': 'UtilitiesApplication', 'operatingSystem': 'Android 6.0 or newer',
        'softwareVersion': version, 'fileSize': mb, 'downloadUrl': url, 'url': 'https://axi0.tech/f0store',
        'license': 'https://www.gnu.org/licenses/gpl-3.0.html', 'isAccessibleForFree': True,
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
        'publisher': {'@type': 'Organization', '@id': 'https://axi0.site/#organization', 'name': 'axi0', 'url': 'https://axi0.site/'},
    }
    page = head('F0Store · Free and open-source apps for Android · axi0',
                "F0Store is axi0's app store for Android: only free and open-source apps, each with its licence and its "
                "repository's warnings, ready from the first start, with a shelf of free picks for everyday Google apps.",
                '/f0store', css)
    page += '<script type="application/ld+json">\n' + json.dumps(ld, indent=1) + '\n</script>\n</head>\n<body>\n'
    page += f'''<a class="skip" href="#content">Skip to the content</a>
<main class="doc" id="content">
  <header class="masthead">
    <a class="wordmark" href="/">axi<span class="zero">0</span></a>
    <span class="meta">F0Store {E(version)}</span>
  </header>

  <div class="hero">{ICON}<h1>F0Store: free and open-source apps for Android.</h1></div>
  <p class="lede">F0Store is axi0's app store for Android. Every app in it is free and open-source software, shown with its licence and with every warning its repository gives. It is ready from the first start, with a shelf of picks: one free app for each everyday Google app.</p>
  <p class="jump"><a href="#download">Download</a><a href="#picks">axi0 picks</a><a href="#sends">What it sends</a><a href="#check">Check a download</a><a href="#repo">Our repository</a></p>

  <h2 id="download">Download F0Store {E(version)}</h2>
  <div class="get">
    <a class="button" href="{E(url)}" download>Download the APK ({E(mb)})</a>
    <dl class="facts">
      <dt>Version</dt><dd>{E(version)} (code {code})</dd>
      <dt>Runs on</dt><dd>Android 6.0 or newer</dd>
      <dt>Size</dt><dd>{size:,} bytes</dd>
      <dt>SHA-256</dt><dd class="hash">{sha}</dd>
      <dt>Signed by</dt><dd class="hash">{APK_CERT}</dd>
    </dl>
    <p>Open the file on your phone. Android asks once whether your browser may install apps; after that F0Store keeps itself and your apps up to date from its signed repositories.</p>
  </div>

  <h2>What F0Store is</h2>
  <ul class="cards">
    <li><strong>FOSS only.</strong> Every app comes from a repository of free and open-source software, with its licence on its page. Never apps copied out of Google Play: those are other people's builds, and Play's terms do not allow it.</li>
    <li><strong>Honest marks.</strong> When a repository marks an app (it tracks you, it needs a non-free service, it has ads), F0Store shows the mark exactly as given, before you install.</li>
    <li><strong>Ready from the first start.</strong> The two largest community repositories of free Android apps and ours are on from the start; any other repository in the same format can be added by link or QR code.</li>
    <li><strong>No account, no tracking.</strong> No sign-in, no analytics, no crash reports, no ads. Updates in the background, Material You colours, light and dark.</li>
    <li><strong>Open source too.</strong> F0Store is GPL-3.0, built and tested in public. <a href="{SOURCE}">Source code</a> · <a href="/f0store/licences">what it is built on</a>.<span class="tag">FluxOS for phones will ship it preinstalled</span></li>
  </ul>

  <h2 id="picks">axi0 picks</h2>
  <p>The first shelf in F0Store: one free app for each everyday Google app, each one checked for its licence and its repository's marks on {E(picks["checked"])}. Names link to each app's own source code.</p>
  <div class="wrap">
    <table>
      <caption>{len(picks["picks"])} picks, with the licence each one is published under</caption>
      <thead><tr><th scope="col">Instead of</th><th scope="col">Pick</th><th scope="col">What it does</th><th scope="col">Licence</th></tr></thead>
      <tbody>
{chr(10).join(rows)}
      </tbody>
    </table>
  </div>

  <h2 id="sends">What the app sends, and to whom</h2>
  <ul>
    <li>To each repository you have on (three at first): ordinary HTTPS requests for its signed list of apps, for icons and screenshots, and for the apps you choose to install. Like every web request they carry your IP address. No account, no device identifier, no list of your apps.</li>
    <li>To our repository at axi0.tech: the same requests, and nothing more. Our server code keeps no logs.</li>
    <li>One community repository publishes which of its apps are verified reproducible builds; F0Store fetches that public list from the same repository, to mark those apps.</li>
    <li>Download counts that one repository offers stay off unless you turn them on in the settings.</li>
    <li>Links you tap (source code, licence, donations) open in your browser.</li>
  </ul>
  <p>Every repository, with its address and its terms: <a href="/f0store/licences">credits and licences</a>.</p>

  <h2 id="check">Check a download</h2>
  <p>Compare the file's SHA-256 with the one above, then the signing certificate with the one above:</p>
<pre><code>shasum -a 256 {E(apk)}
apksigner verify --print-certs {E(apk)}</code></pre>
  <p>Updates come only from repositories whose signature F0Store checks against the fingerprint it ships with, and Android installs an update only when it is signed by the same key as the app on your phone.</p>

  <h2 id="repo">Our repository</h2>
  <p>F0Store's own updates come from our repository. Any client for the same format can add it:</p>
  <pre><code>{REPO}?fingerprint={REPO_FPR}</code></pre>
  <p>Coming to it: our browser for Android and the other axi0 apps for phones, built in public and signed by us.</p>

{foot()}'''
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)

    lic = head('F0Store credits and licences · axi0',
               'What F0Store is built on, the repositories it ships with and what each one receives, and the licences '
               'of the apps and their descriptions.', '/f0store/licences', css)
    lic += '</head>\n<body>\n'
    lic += f'''<a class="skip" href="#content">Skip to the content</a>
<main class="doc" id="content">
  <header class="masthead">
    <a class="wordmark" href="/">axi<span class="zero">0</span></a>
    <span class="meta">F0Store {E(version)}</span>
  </header>

  <h1>F0Store credits and licences</h1>
  <p class="lede">F0Store stands on other people's free software and talks to other people's servers. This page names them, says what each one receives, and gives the licences.</p>

  <h2>Built on</h2>
  <ul>
    <li><strong>Droid-ify</strong> 0.7.8, GPL-3.0: F0Store is a modified version of it. <a href="https://github.com/Droid-ify/client">Droid-ify source</a> · <a href="{SOURCE}">F0Store source</a> (GPL-3.0, with the full history and a <a href="{SOURCE}/blob/main/NOTICE.md">notice of every change</a>).</li>
    <li><strong>Foxy Droid</strong>, GPL-3.0: the client Droid-ify grew from. <a href="https://github.com/kitsunyan/foxy-droid">Foxy Droid source</a>.</li>
    <li>The libraries inside the app keep their own licences (Apache-2.0 and others); they are listed in the source repository's build files.</li>
  </ul>

  <h2>The repositories F0Store ships with, and what each receives</h2>
  <div class="wrap">
    <table>
      <thead><tr><th scope="col">Repository</th><th scope="col">Address</th><th scope="col">What F0Store asks it for</th></tr></thead>
      <tbody>
        <tr><th scope="row">F-Droid</th><td><code>https://f-droid.org/repo</code></td><td>Its signed index, icons, screenshots, and the apps you install. On by default.</td></tr>
        <tr><th scope="row">IzzyOnDroid</th><td><code>https://apt.izzysoft.de/fdroid/repo</code></td><td>The same, plus its public reproducible-build log (setting on by default). Its download counts (<code>dlstats.izzyondroid.org</code>) only if you turn them on. On by default.</td></tr>
        <tr><th scope="row">F0Store (ours)</th><td><code>{REPO}</code></td><td>Its signed index and F0Store's own updates. On by default; no logs.</td></tr>
        <tr><th scope="row">F-Droid Archive</th><td><code>https://f-droid.org/archive</code></td><td>Older app versions. Off unless you turn it on.</td></tr>
      </tbody>
    </table>
  </div>
  <p>Every request is ordinary HTTPS and carries your IP address, as any web request does; F0Store adds no identifier. A repository may answer from a mirror it lists.</p>

  <h2>Names and terms</h2>
  <ul>
    <li>F-Droid is a trademark of the F-Droid project. F0Store is not made, endorsed or checked by F-Droid; the name appears here and in the app only to say which repository is which. We use no F-Droid logo. The F-Droid site and community content are AGPL-3.0-or-later; app descriptions and graphics carry each app's own licence (<a href="https://f-droid.org/docs/Licenses/">F-Droid licences</a>).</li>
    <li>IzzyOnDroid recommends clients that come with its repository already set up, and keeps no personal data (<a href="https://izzyondroid.org/contact">IzzyOnDroid privacy</a>).</li>
    <li>The app metadata collected for the F-Droid repository is AGPL-3.0 (<a href="https://gitlab.com/fdroid/fdroiddata">fdroiddata</a>). F0Store shows it unchanged inside the app; this site writes its own descriptions.</li>
    <li>Each app's own licence is on its page in F0Store; the axi0 picks and their licences are on the <a href="/f0store#picks">F0Store page</a>.</li>
  </ul>

  <h2>This site</h2>
  <p>Instrument Sans is under the SIL Open Font License. Everything else on this page © 2026 axi0.</p>

{foot()}'''
    open(os.path.join(out, 'licences.html'), 'w', encoding='utf-8').write(lic)
    print(f'web shelf: F0Store {version} ({code}), {apk}, {size} bytes, sha256 {sha[:16]}..., css v={css}, {len(picks["picks"])} picks')


if __name__ == '__main__':
    main()
