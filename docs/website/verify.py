"""Offline checks. Does not send mail, execute browser UI or publish."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,sys,xml.etree.ElementTree as ET
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'previews/candidate-v3'
class Page(HTMLParser):
 def __init__(self,text):self.tags=[];super().__init__();self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
 def of(self,t):return [a for tag,a in self.tags if tag==t]
parsed={p.name:Page(p.read_text()) for p in root.glob('*.html')}
assert len(parsed)==8,'Expected home, six systems and privacy'
for name,p in parsed.items():
 ids=[a['id'] for _,a in p.tags if 'id'in a];assert len(ids)==len(set(ids)),name+' duplicate id'
 assert len(p.of('h1'))==1,name+' H1 count'
 assert any(a.get('rel')=='canonical' for a in p.of('link')),name+' canonical'
 assert any(a.get('property')=='og:title' for a in p.of('meta')),name+' OG title'
 assert any(a.get('name')=='robots' for a in p.of('meta')),name+' robots'
 assert any(a.get('type')=='application/ld+json' for a in p.of('script')),name+' schema'
 for tag,a in p.tags:
  for attr in ['href','src','poster']:
   value=a.get(attr)
   if not value:continue
   url=urlsplit(value)
   if url.scheme or url.netloc:continue
   target=url.path or name
   assert (root/target).exists(),f'{name}: missing {target}'
   if url.fragment:
    assert target in parsed,f'{name}: unknown HTML target'
    target_ids=[x.get('id') for _,x in parsed[target].tags]
    assert url.fragment in target_ids,f'{name}: missing #{url.fragment}'
  if tag=='a' and a.get('target')=='_blank':assert 'noopener' in a.get('rel',''),name+' unsafe target'
 # Validate JSON-LD syntax, not external claims.
 import re
 for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>',(root/name).read_text(),re.S):json.loads(data)
home=parsed['index.html'];assert len([a for a in home.of('article') if a.get('class')=='card'])==6,'No-JS product cards'
form=home.of('form')[0];assert form['method']=='POST' and form['action']=='https://formsubmit.co/emir@wedocare-global.com'
assert any(a.get('name')=='consent' and 'required'in a for a in home.of('input'))
assert all('autoplay' not in a for a in home.of('video')),'Video should not autoplay before reduced-motion check'
assert not home.of('dialog'),'Products need persistent pages'
ET.parse(root/'sitemap.xml')
print('PASS: 8 pages; six no-JS cards; all local links/assets/fragments; single H1s; canonical/OG/JSON-LD; native POST + consent; motion defaults; sitemap XML. No mail sent.')
