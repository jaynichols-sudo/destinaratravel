#!/usr/bin/env python3
"""
Self-host every Unsplash image used on the site.

Scans all .html files for https://images.unsplash.com/... references, downloads
each unique image into assets/img/, and rewrites the HTML to point at the local
copy. Safe to run repeatedly: already-downloaded files are skipped and any
references that are already local are ignored.

Run by the "Self-host images" GitHub Action (.github/workflows/self-host-images.yml),
which then commits the downloaded images + rewritten HTML in a single commit.
"""
import re, os, glob, hashlib, urllib.request, html

os.makedirs('assets/img', exist_ok=True)
files = glob.glob('**/*.html', recursive=True)

# Matches a full Unsplash CDN URL incl. its query string. The query character
# class deliberately covers &amp; (HTML-encoded ampersands) as well as &.
rx = re.compile(r'https://images\.unsplash\.com/photo-[0-9a-zA-Z]+-[0-9a-zA-Z]+(?:\?[A-Za-z0-9=&;%_,.\-]+)?')

urls = set()
for f in files:
    with open(f, encoding='utf-8') as fh:
        for m in rx.findall(fh.read()):
            urls.add(m)
print('Unique Unsplash URLs found:', len(urls))

mapping = {}
for u in sorted(urls):
    download_url = html.unescape(u)                 # &amp; -> & for the actual request
    slug = re.search(r'photo-[0-9a-zA-Z]+-[0-9a-zA-Z]+', u).group(0)
    digest = hashlib.md5(download_url.encode()).hexdigest()[:8]   # unique per size/crop
    filename = f'{slug}-{digest}.jpg'
    path = f'assets/img/{filename}'
    if not os.path.exists(path):
        try:
            req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=90).read()
            with open(path, 'wb') as out:
                out.write(data)
            print(f'Downloaded {filename}  ({len(data):,} bytes)')
        except Exception as e:
            print(f'FAILED  {download_url}  ->  {e}')
            continue
    mapping[u] = f'/assets/img/{filename}'

rewritten = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    original = s
    for u, local in mapping.items():
        s = s.replace(u, local)
    if s != original:
        open(f, 'w', encoding='utf-8').write(s)
        rewritten += 1

print(f'HTML files rewritten: {rewritten}')
print(f'Images downloaded into assets/img/ : {len(mapping)} mapped')
print('Done. The site now serves images from your own repo, not Unsplash.')
