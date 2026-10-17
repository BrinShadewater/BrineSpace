from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0;failures=[];bounds={}
def check(ok,what):
    global checks
    checks+=1
    if not ok:failures.append(what)
for mode,masterpath in [('bare','character/crew-runtime-matte-v1/branforth/manifest.json'),('helmet','character/james-shared-helmet-runtime-v1/manifest.json')]:
    masterpack=json.loads((R/masterpath).read_text());ms=next(s for s in masterpack['states'] if s['id']=='idle-east');master=Image.open((R/masterpath).parent/ms['frameFiles'][0]).convert('RGBA')
    pack=json.loads((P/(mode+'-manifest.json')).read_text());rows=[]
    for state in pack['states']:
        full=state['id'].startswith(('inspect-','interact-'))
        if full:
            check(state['frameCount']==141 and len(state['frameFiles'])==141,mode+' full141 motion')
            check(state['provenance']['sourceFrames']==list(range(141)),mode+' every source index')
            check(sum(state['frameDurationsMs'])==(6000 if state['id'].startswith('inspect') else 5500),mode+' clock')
        else:
            check(mode=='helmet' and state['frameCount']==6 and len(state['frameFiles'])==6,'Sealed-meal compatibility count')
            check(state['provenance']['sourcePoses']==[0,32,60,86,123,140],'Sealed-meal updated source indices')
            check(sum(state['frameDurationsMs'])==(1500 if state['id']=='eat-east' else 3000),'Sealed-meal preserved compatibility clock')
        for i,f in enumerate(state['frameFiles']):
            im=Image.open(P/f).convert('RGBA');a=np.array(im);y,x=np.where(a[:,:,3]>192)
            check(im.size==(184,184),mode+' canvas '+str(i));check(len(y)>0 and y.min()>0 and y.max()<183 and x.min()>0 and x.max()<183,mode+' crop '+str(i))
            if i in [0,len(state['frameFiles'])-1]:check(im.tobytes()==master.tobytes(),mode+' exact master endpoint '+str(i))
            if state['id'].startswith('inspect'):rows.append({'index':i,'crown':int(y.min()),'sole':int(y.max())})
    bounds[mode]={'crownRange':[min(r['crown'] for r in rows),max(r['crown'] for r in rows)],'soleRange':[min(r['sole'] for r in rows),max(r['sole'] for r in rows)],'maxAdjacentCrownStep':max(abs(a['crown']-b['crown']) for a,b in zip(rows,rows[1:]))}
with Image.open(P/'paired-candidate.gif') as gif:
    ms=0
    for i in range(gif.n_frames):gif.seek(i);ms+=gif.info['duration']
    check(ms==6000,'Actual encoded GIF duration')
report={'checks':checks,'failures':failures,'bounds':bounds,'gifMs':ms,'productionInstalled':False,'scope':'Candidate package only: complete141 source indices, clocks, canvas/crop and exact endpoints. Does not assert native behavior, owner acceptance, semantic prop identity or smoothness.'}
(P/'candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));raise SystemExit(bool(failures))
