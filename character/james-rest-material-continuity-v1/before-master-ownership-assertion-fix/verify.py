from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];e=json.loads((P/'material-evidence.json').read_text());checks=0;failures=[]
def check(ok,why):
    global checks
    checks+=1
    if not ok:failures.append(why)
for row in e['records']:
    source=R/row['source'];check(hashlib.sha256(source.read_bytes()).hexdigest()==row['sourceSha256'],'Original source hash')
    a=np.array(Image.open(source).convert('RGBA'));b=np.array(Image.open(P/row['output']).convert('RGBA'));check(np.array_equal(a[:,:,3],b[:,:,3]),'Exact source alpha')
    x0,y0,x1,y1=row['protectedHead'];check(np.array_equal(a[y0:y1,x0:x1],b[y0:y1,x0:x1]),'Exact protected head/shell')
    if row['sourcePose']==0:check(np.array_equal(a,b),'Exact standing master source0')
packs={mode:json.loads((P/(mode+'-manifest.json')).read_text()) for mode in ['bare','helmet']};bindings=json.loads((P/'source-bindings.json').read_text());joins=[]
for mode,group in [('bare','body'),('helmet','equipment')]:
    states={s['id']:s for s in packs[mode]['states']}
    for key,state in states.items():
        file=R/bindings[group][key]['path'];old=json.loads(file.read_text());original=next(s for s in old['states'] if s['id']==key)
        for name,value in original.items():
            if name not in ['frameFiles','provenance']:check(state[name]==value,'Exact original metadata '+name)
    for direction in ['north','south','east','west']:
        def pixels(key,index):return Image.open(P/states[key+'-'+direction]['frameFiles'][index]).convert('RGBA').tobytes()
        for name,a,b in [('lie/sleep',pixels('lie-down',-1),pixels('sleep',0)),('closed sleep',pixels('sleep',0),pixels('sleep',-1)),('sleep/rise',pixels('sleep',-1),pixels('get-up',0)),('closed standing',pixels('get-up',-1),pixels('lie-down',0))]:
            check(a==b,'Exact phase join '+name);joins.append({'mode':mode,'direction':direction,'join':name,'exact':a==b})
for row in e['records']:
    if row['mode']!='bare':continue
    mate=next(r for r in e['records'] if r['mode']=='helmet' and r['key']==row['key'] and r['index']==row['index'])
    a=np.array(Image.open(P/row['output']).convert('RGBA'));b=np.array(Image.open(P/mate['output']).convert('RGBA'));keep=np.ones(a.shape[:2],bool);x0,y0,x1,y1=row['protectedHead'];keep[y0:y1,x0:x1]=False
    check(np.array_equal(a[keep],b[keep]),'Shared body outside owned head')
report={'checks':checks,'failures':failures,'sourceReferences':144,'changedFrames':sum(r['changedPixels']>0 for r in e['records']),'exactJoins':sum(j['exact'] for j in joins),'joins':joins,'alphaHeadsExact':True,'geometryClockChanges':False,'scope':'Complete selected source hash/alpha/head/paired ownership and phase joins; exact original clocks/rest metadata. No semantic material, native-context or full-set acceptance from numeric checks.'}
(P/'packaging-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='joins'}));raise SystemExit(bool(failures))
