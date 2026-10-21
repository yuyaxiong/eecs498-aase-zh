#!/usr/bin/env python3
"""Structural checks without external packages or network calls."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=set(); self.links=[]; self.lang=None; self.has_h1=False; self.notices=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if tag=='h1': self.has_h1=True
        if 'id' in a:
            assert a['id'] not in self.ids, f"duplicate id: {a['id']}"
            self.ids.add(a['id'])
        if a.get('class')=='notice': self.notices+=1
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag in ('link','script'):
            self.links.append(a.get('href',a.get('src','')))

pages={p:Document(p.read_text()) for p in DOCS.rglob('*.html')}
assert len(pages)==6
links=0
external=set()
for p,doc in pages.items():
    assert doc.lang=='zh-Hans' and doc.has_h1 and doc.notices==1, p
    for raw in doc.links:
        u=urlsplit(raw)
        if u.scheme in ('https','mailto'):
            external.add(raw); continue
        assert not u.scheme and not raw.startswith('//'), (p,raw)
        target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
        if u.path.startswith('/eecs498-aase-zh/'):
            target=(DOCS/unquote(u.path[len('/eecs498-aase-zh/'):])).resolve()
        if target.is_dir(): target=target/'index.html'
        assert target.exists(), (p,raw,target)
        if u.fragment:
            assert target in pages and unquote(u.fragment) in pages[target].ids, (p,raw,'missing anchor')
        links+=1
source_file=ROOT/'source-links.json'
if source_file.exists():
    originals=json.loads(source_file.read_text())['functionalExternalLinks']
    assert set(originals)<=external, 'lost external URLs: '+str(set(originals)-external)
data=json.loads((DOCS/'data/course.json').read_text())
assert len(data['weeks'])==15 and len(data['episodes'])==7 and data['faqCount']==25
assert set(re.findall(r'L(\d{2})', (DOCS/'syllabus.html').read_text()))=={f'{i:02}' for i in range(1,29)}
assert (DOCS/'faq.html').read_text().count('class="faq-item"')==25
assert sum('Lab '+f'{i:02}' in str(data['weeks']) for i in range(13))==13
assert data['timezone']=='America/Detroit'
print(f'PASS: {len(pages)} pages; {links} local targets/anchors; {len(external)} external URLs; 15 weeks; 28 lectures; 13 labs; 25 FAQs; 7 episodes.')
