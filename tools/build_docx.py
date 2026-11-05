"""Regenerate Mathew_Garcia_Resume_Updated.docx from index.html.

    python tools/build_docx.py                      # rewrites the .docx next to index.html
    python tools/build_docx.py out=C:/tmp/test.docx # write elsewhere (for checking a layout)
    python tools/build_docx.py h_before=240         # override a layout tunable (see OPTS)

The existing .docx is the template: every part except word/document.xml, its
relationships and the core properties is carried over unchanged (styles, bullet
numbering, fonts, settings), so the look stays the same and only the content and
the page setup come from this script. Content is parsed from index.html, so the
site stays the source of truth; run this after any content change to the site.

Word-only decisions live here, not on the site:
  - the header shows the city, not the street address or phone (the file is public)
  - section order is Summary, Certifications, Key Skills, Experience, Shipped Apps, Military
  - skill cards become "Category: items" bullets; store links become the Shipped Apps list
"""
import datetime
import html
import os
import re
import sys
import zipfile
from xml.sax.saxutils import escape

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = os.path.join(REPO, 'Mathew_Garcia_Resume_Updated.docx')
LOCATION = 'Anaheim, CA'

# Layout tunables: twips for spacing and margins, half-points for type size.
OPTS = {
    'margin': 1080,          # 0.75 in
    'h_before': 200,         # section heading spacing
    'h_after': 100,
    'company_after': 80,     # gap between the company line and its bullets
    'summary_after': 160,
    'body': 22,              # 11 pt
    'keep_lines': 0,         # 1 = never split a bullet across pages (costs a fourth page with the 2026 content)
}
out_path = DOCX
for arg in sys.argv[1:]:
    key, value = arg.split('=', 1)
    if key == 'out':
        out_path = value
    elif key in OPTS:
        OPTS[key] = int(value)
    else:
        raise SystemExit(f'unknown option {key}; known: out, ' + ', '.join(OPTS))

src = open(os.path.join(REPO, 'index.html'), encoding='utf-8').read()
body = src[src.index('<main class="container">'):src.index('</main>')]


# ---------------------------------------------------------------- parse the site
def clean(fragment):
    """Strip tags, unescape entities, collapse whitespace."""
    text = re.sub(r'<[^>]+>', '', fragment)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def one(pattern, text):
    m = re.search(pattern, text, re.S)
    if not m:
        raise SystemExit('pattern not found in index.html: ' + pattern)
    return m.group(1)


name = clean(one(r'<h1 class="name">(.*?)</h1>', body))
tagline = clean(one(r'<p class="tagline">(.*?)</p>', body))
contacts = [(href, clean(label)) for href, label in
            re.findall(r'<a class="contact-item" href="([^"]+)"[^>]*>.*?<span>(.*?)</span>', body, re.S)]
summary = clean(one(r'<p class="summary">(.*?)</p>', body))
skills = [(clean(t), clean(l)) for t, l in
          re.findall(r'<div class="skill-category-title">(.*?)</div>.*?<div class="skill-list">(.*?)</div>', body, re.S)]
jobs = []
for chunk in body.split('<div class="experience-item">')[1:]:
    item = chunk[:chunk.index('</ul>')]
    jobs.append({
        'title': clean(one(r'<h3 class="job-title">(.*?)</h3>', item)),
        'company': clean(one(r'<div class="company">(.*?)</div>', item)),
        'dates': clean(one(r'<span class="date-range">(.*?)</span>', item)),
        'bullets': [clean(li) for li in re.findall(r'<li>(.*?)</li>', item, re.S)],
    })
certs = [clean(c) for c in re.findall(r'<p class="cert-title">(.*?)</p>', body, re.S)]
military_title = clean(one(r'<div class="military-title">(.*?)</div>', body))
military_branch, military_dates = [s.strip() for s in clean(one(r'<div class="military-branch">(.*?)</div>', body)).split('•')]
footer_html = one(r'<footer class="footer">(.*?)</footer>', body)
footer = [(href, clean(label)) for href, label in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', footer_html, re.S)]

if not (contacts and skills and jobs and certs and footer and all(j['bullets'] for j in jobs)):
    raise SystemExit('index.html parsed incompletely; check the markup conventions in CLAUDE.md')

# Store links from the footer, grouped by product; the GitHub link is already in the header.
apps = {}
for href, label in footer:
    m = re.match(r'(.+?) on (the App Store|Google Play)$', label)
    if m:
        apps.setdefault(m.group(1), []).append(('App Store' if 'App Store' in m.group(2) else 'Google Play', href))

# ---------------------------------------------------------------- WordprocessingML
FONT = '<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>'
rels = []  # (rId, url) hyperlink relationships to add


def run(text, size=None, bold=False, italic=False, style=None):
    size = OPTS['body'] if size is None else size
    rpr = (f'<w:rStyle w:val="{style}"/>' if style else '') + FONT
    if bold:
        rpr += '<w:b/><w:bCs/>'
    if italic:
        rpr += '<w:i/><w:iCs/>'
    rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def link(url, text, size=None):
    rid = f'rId{100 + len(rels)}'
    rels.append((rid, url))
    return f'<w:hyperlink r:id="{rid}">{run(text, size, style="Hyperlink")}</w:hyperlink>'


def para(runs, ppr=''):
    return f'<w:p><w:pPr>{ppr}</w:pPr>{"".join(runs)}</w:p>'


def heading(text):
    ppr = ('<w:keepNext/><w:pBdr><w:bottom w:val="single" w:color="000000" w:sz="6" w:space="1"/></w:pBdr>'
           f'<w:spacing w:before="{OPTS["h_before"]}" w:after="{OPTS["h_after"]}"/>')
    return para([run(text, 24, bold=True)], ppr)


def bullet(runs):
    keep = '<w:keepLines/>' if OPTS['keep_lines'] else ''
    return para(runs, f'<w:pStyle w:val="ListParagraph"/>{keep}<w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>')


def subhead(text):
    return para([run(text, bold=True)], '<w:keepNext/><w:spacing w:before="120" w:after="60"/>')


paras = []
paras.append(para([run(name, 36, bold=True)], '<w:spacing w:after="60"/><w:jc w:val="center"/>'))
paras.append(para([run(tagline, 20)], '<w:spacing w:after="60"/><w:jc w:val="center"/>'))
contact_runs = [run(LOCATION, 20)]
for href, label in contacts:
    contact_runs += [run('  |  ', 20), link(href, label, 20)]
paras.append(para(contact_runs, '<w:spacing w:after="200"/><w:jc w:val="center"/>'))

paras.append(heading('Professional Summary'))
paras.append(para([run(summary)], f'<w:spacing w:after="{OPTS["summary_after"]}"/>'))

paras.append(heading('Certifications'))
for c in certs:
    paras.append(bullet([run(c)]))

paras.append(heading('Key Skills'))
for title, items in skills:
    paras.append(bullet([run(title + ': ', bold=True), run(items)]))

paras.append(heading('Professional Experience'))
for j in jobs:
    paras.append(subhead(j['title']))
    paras.append(para([run(f"{j['company']} ({j['dates']})", italic=True)],
                      f'<w:keepNext/><w:spacing w:after="{OPTS["company_after"]}"/>'))
    for b in j['bullets']:
        paras.append(bullet([run(b)]))

if apps:
    paras.append(heading('Shipped Apps'))
    for product, stores in apps.items():
        runs = [run(product + ': ', bold=True)]
        for i, (store, url) in enumerate(stores):
            if i:
                runs.append(run('  ·  '))
            runs.append(link(url, store))
        paras.append(bullet(runs))

paras.append(heading('Military Service'))
paras.append(subhead(f'{military_title}, {military_branch}'))
paras.append(para([run(f'({military_dates})', italic=True)], '<w:spacing w:after="120"/>'))

m = OPTS['margin']
sect = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840" w:orient="portrait"/>'
        f'<w:pgMar w:top="{m}" w:right="{m}" w:bottom="{m}" w:left="{m}" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:pgNumType/><w:docGrid w:linePitch="360"/></w:sectPr>')

# ---------------------------------------------------------------- pack, using the current file as the template
with zipfile.ZipFile(DOCX) as z:
    template = [(info.filename, z.read(info.filename)) for info in z.infolist() if not info.is_dir()]
parts = dict(template)

old_doc = parts['word/document.xml'].decode('utf-8')
root_open = re.match(r'.*?<w:document[^>]*>', old_doc, re.S).group(0)
new_doc = root_open + '<w:body>' + ''.join(paras) + sect + '</w:body></w:document>'

old_rels = re.sub(r'<Relationship [^>]*relationships/hyperlink"[^>]*/>', '', parts['word/_rels/document.xml.rels'].decode('utf-8'))
hyper = ''.join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                f'Target="{escape(url, {chr(34): "&quot;"})}" TargetMode="External"/>' for rid, url in rels)
new_rels = old_rels.replace('</Relationships>', hyper + '</Relationships>')

now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
created = re.search(r'<dcterms:created[^>]*>([^<]+)</dcterms:created>', parts.get('docProps/core.xml', b'').decode('utf-8'))
core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f'<dc:title>{escape(name)} Resume</dc:title><dc:creator>{escape(name)}</dc:creator>'
        f'<cp:lastModifiedBy>{escape(name)}</cp:lastModifiedBy><cp:revision>2</cp:revision>'
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{created.group(1) if created else now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>')

replaced = {'word/document.xml': new_doc, 'word/_rels/document.xml.rels': new_rels, 'docProps/core.xml': core}
tmp = out_path + '.tmp'
with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
    for filename, data in template:
        z.writestr(filename, replaced[filename].encode('utf-8') if filename in replaced else data)
os.replace(tmp, out_path)

print(f'wrote {out_path}: {len(paras)} paragraphs, {len(rels)} hyperlinks, '
      f'{sum(len(j["bullets"]) for j in jobs)} bullets across {len(jobs)} roles, '
      f'{len(skills)} skill groups, {len(certs)} certifications, apps: {", ".join(apps) or "none"}')
