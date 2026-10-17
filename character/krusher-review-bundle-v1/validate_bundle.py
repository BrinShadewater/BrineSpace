from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,zipfile
P=Path(__file__).resolve().parent;R=P.parent.parent;errors=[];checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
class Resources(HTMLParser):
    def __init__(self):super().__init__();self.paths=[];self.fragments=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for key in ['src','href']:
            if key not in a:continue
            value=a[key]
            if value.startswith('#'):self.fragments.append(value[1:])
            elif 'archive-download' not in a.get('class',''):self.paths.append(value)
html=(P/'index.html').read_text();resources=Resources();resources.feed(html);resources.paths+=re.findall(r'url\(([^)]+)\)',html)
for fragment in resources.fragments:check(fragment in resources.ids,'section link '+fragment)
source_map=json.loads((P/'source-map.json').read_text())
for record in source_map['files']:
    check(hashlib.sha256((P/record['file']).read_bytes()).hexdigest()==record['sha256'],'delivery source bytes '+record['file'])
    check(hashlib.sha256((R/record['projectSource']).read_bytes()).hexdigest()==record['sha256'],'project source unchanged '+record['projectSource'])
archives={}
for name,full in [('Krusher-Dom-review.zip',True),('Krusher-Dom-preview.zip',False)]:
    with zipfile.ZipFile(P/name) as z:
        names=z.namelist();check(len(names)==len(set(names)),'unique archive names '+name);check(not any(p.startswith('/') or '..' in Path(p).parts for p in names),'safe relative archive paths '+name);check(z.testzip() is None,'ZIP CRC '+name)
        m=json.loads(z.read('source-map.json'))
        for record in m['files']:check(hashlib.sha256(z.read(record['file'])).hexdigest()==record['sha256'],'archive source bytes '+name+'/'+record['file'])
        for path in resources.paths:check(path in names,'offline review resource '+name+'/'+path)
        if full:
            for gear in ['bare','helmet']:
                manifest=json.loads(z.read(f'runtime/{gear}-manifest.json'))
                for state in manifest['states']:
                    for frame in state['frameFiles']:check('runtime/'+frame in names,'self-contained runtime frame '+gear+'/'+state['id'])
        else:check(not any(p.startswith('runtime/') for p in names),'preview excludes runtime frames')
        archives[name]={'files':len(names),'bytes':(P/name).stat().st_size}
# Chapter starts must reflect the copied manifest, not an unrelated preview clock.
manifest=json.loads((P/'runtime/bare-manifest.json').read_text());starts=[];elapsed=0
for state in manifest['states']:starts.append((state['id'].replace('-',' '),elapsed/1000));elapsed+=sum(state['frameDurationsMs'])
for title,start in starts:check(f"['{title}',{start:g}]" in html,'chapter source boundary '+title)
result={'checks':checks,'errors':errors,'archives':archives,'scope':'Delivery source preservation, ZIP integrity, local review resources, self-contained runtime references and source chapter boundaries; not artistic motion acceptance'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({**result,'errors':errors[:20],'errorCount':len(errors)}));raise SystemExit(bool(errors))
