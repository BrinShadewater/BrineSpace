from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((P/'provenance.json').read_text());checks=0;errors=[]
def check(ok,label):
    global checks
    checks+=1
    if not ok:errors.append(label)
for t in v['sources']:check(sha(R/t['source'])==t['sha256'],'manifest:'+t['source'])
for t in v['frames']:
    check(sha(P/t['file'])==t['sha256'] and sha(R/t['source'])==t['sha256'],'bytes:'+t['file'])
    check(Image.open(P/t['file']).size==(184,184),'canvas:'+t['file'])
for gear in ['bare','helmet']:
    m=json.loads((P/f'{gear}-manifest.json').read_text())
    originals=[]
    for t in v['sources']:
        if t['source'].endswith(f'{gear}-manifest.json'):originals+=json.loads((R/t['source']).read_text())['states']
    for s in m['states']:
        original=next(t for t in originals if t['id']==s['id'])
        for k,val in original.items():
            if k=='frameFiles':continue
            check(s[k]==val,'metadata:'+gear+'/'+s['id']+'/'+k)
        check(len(s['frameFiles'])==len(original['frameFiles']),'count:'+gear+'/'+s['id'])
    for direction in ['east','south','west','north']:
        action=next(s for s in m['states'] if s['id']=='interact-'+direction)
        idle=next(s for s in m['states'] if s['id']=='idle-'+direction)
        for index in [0,-1]:check(Image.open(P/action['frameFiles'][index]).tobytes()==Image.open(P/idle['frameFiles'][0]).tobytes(),'endpoint:'+gear+'/'+direction)

bare=json.loads((P/'bare-manifest.json').read_text());helmet=json.loads((P/'helmet-manifest.json').read_text())
for b,h in zip(bare['states'],helmet['states']):
    for k in ['id','frameDurationsMs','loop']:check(b[k]==h[k],'gear:'+k)
report={'checks':checks,'errors':errors,'scope':'Current source/frame bytes,184px canvas, exact source state metadata and paired canonical endpoints; not station integration or artistic acceptance'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));assert not errors
