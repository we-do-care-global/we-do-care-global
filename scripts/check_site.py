"""Validate the deployed static site's links, resources and progressive enhancement."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json,re,sys,xml.etree.ElementTree as ET
root=Path(sys.argv[1] if len(sys.argv)>1 else 'docs')
class Document(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.duplicates=[];self.refs=[];self.card_count=0;self.h1=0;self.title=False;self.canonical=False;self.csp=False;self.description=False;self.inline=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   if a['id'] in self.ids:self.duplicates.append(a['id'])
   self.ids.add(a['id'])
  for k in ['href','src','poster']:
   if a.get(k):self.refs.append(a[k])
  if tag=='article' and 'card' in a.get('class','').split():self.card_count+=1
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='link' and a.get('rel')=='canonical':self.canonical=True
  if tag=='meta' and a.get('name')=='description':self.description=True
  if tag=='meta' and a.get('http-equiv')=='Content-Security-Policy':self.csp=True
  if 'style' in a or any(k.startswith('on') for k in a):self.inline.append(tag)
files={p:Document(p.read_text()) for p in root.glob('*.html') if not p.name.startswith('google')}
errors=[];checked=0
for p,doc in files.items():
 if doc.duplicates:errors.append(f'{p}: duplicate IDs {doc.duplicates}')
 if doc.h1!=1:errors.append(f'{p}: expected one H1, got {doc.h1}')
 missing=[name for name,present in [('title',doc.title),('canonical URL',doc.canonical),('meta description',doc.description),('Content-Security-Policy',doc.csp)] if not present]
 if missing:errors.append(f"{p}: missing metadata/security policy: {', '.join(missing)}")
 if doc.inline:errors.append(f'{p}: inline styles or event handlers blocked by CSP')
 for ref in doc.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)) if u.path else p
  if target.is_dir():target/='index.html'
  if not target.exists():errors.append(f'{p}: missing {ref}');continue
  if u.fragment and target in files and unquote(u.fragment) not in files[target].ids:errors.append(f'{p}: missing fragment {ref}')
  checked+=1
for css in root.glob('*.css'):
 if 'fonts.googleapis.com' in css.read_text() or '&family=' in css.read_text():errors.append(f'{css}: leftover external font import')
 for ref in re.findall(r'url\([\"\x27]?([^\)\"\x27]+)',css.read_text()):
  if not urlsplit(ref).scheme and not (css.parent/ref).exists():errors.append(f'{css}: missing resource {ref}')
if files[root/'index.html'].card_count!=6:errors.append('Home must have six static cards')
for loc in ET.parse(root/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
 path=urlsplit(loc.text).path.lstrip('/') or 'index.html'
 if not(root/path).exists():errors.append(f'Sitemap missing {path}')
for p in files:
 text=p.read_text()
 if 'wdcg-analytics' in text or 'Math.random' in text or 'Nothing is simulated' in text:errors.append(f'{p}: obsolete tracking or misleading demo content')
print(json.dumps({'pages':len(files),'local_references_checked':checked,'errors':errors},indent=2))
sys.exit(bool(errors))
