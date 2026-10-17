from pathlib import Path
from PIL import Image
import numpy as np,json
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'review-evidence.json').read_text());cache={}
def image(path):
    if path not in cache:cache[path]=np.array(Image.open(R/path).convert('RGBA'))
    return cache[path]
def sample(a):
    rgb=a[:,:,:3].astype(float);y=np.indices(a.shape[:2])[0];lum=rgb.mean(2)
    mask=(a[:,:,3]>240)&(y>90)&(y<165)&(np.ptp(rgb,axis=2)<35)&(lum>20)&(lum<150)
    x=rgb[mask];green=x[:,1]-(x[:,0]+x[:,2])/2
    return {'pixels':len(x),'medianRGB':np.median(x,axis=0).tolist(),'greenExcessMedian':float(np.median(green)),'greenExcessOver4':int((green>4).sum()),'greenExcessOver4Fraction':float((green>4).mean())}
C=json.loads((P/'source-bindings.json').read_text())['coverage'];masters={}
for mode in ['bare','helmet']:
    for direction in ['east','north','south','west']:
        manifest=R/C['body' if mode=='bare' else 'equipment']['idle-'+direction]['path'];m=json.loads(manifest.read_text());s=next(s for s in m['states'] if s['id']=='idle-'+direction);f=s['frameFiles'][0]
        path=R/f.removeprefix('res://') if f.startswith('res://') else manifest.parent/f
        masters[(mode,direction)]=path.relative_to(R).as_posix()
samples=[];joins=[]
for r in e['records']:
    a=image(r['path']);direction=r['key'].split('-')[-1];samples.append({'mode':r['mode'],'key':r['key'],'index':r['index'],**sample(a),'master':sample(image(masters[(r['mode'],direction)]))})
for mode in ['bare','helmet']:
    for direction in ['east','north','south','west']:
        groups={key:[r for r in e['records'] if r['mode']==mode and r['key']==key+'-'+direction] for key in ['torch-draw','weld','torch-stow']}
        source=[masters[(mode,direction)],groups['torch-draw'][0]['path'],groups['torch-draw'][-1]['path'],groups['weld'][0]['path'],groups['weld'][-1]['path'],groups['torch-stow'][0]['path'],groups['torch-stow'][-1]['path'],masters[(mode,direction)]]
        for i,label in enumerate(['idle→draw','draw→weld','weld→stow','stow→idle']):
            a,b=image(source[i*2]),image(source[i*2+1]);joins.append({'mode':mode,'direction':direction,'join':label,'exactRGBA':bool(np.array_equal(a,b)),'changedPixels':int(np.any(a!=b,axis=2).sum())})
summary=[]
for mode in ['bare','helmet']:
    for direction in ['east','north','south','west']:
        rows=[s for s in samples if s['mode']==mode and s['key'].endswith('-'+direction)];master=rows[0]['master'];worst=max(rows,key=lambda s:s['greenExcessOver4Fraction'])
        summary.append({'mode':mode,'direction':direction,'masterGreenFraction':master['greenExcessOver4Fraction'],'worstKey':worst['key'],'worstIndex':worst['index'],'worstGreenFraction':worst['greenExcessOver4Fraction'],'medianGreenFraction':float(np.median([s['greenExcessOver4Fraction'] for s in rows]))})
(P/'material-and-joins.json').write_text(json.dumps({'sourceReferences':len(samples),'joins':joins,'samples':samples,'summary':summary,'scope':'Low-chroma opaque lower-suit sample y90..165. Green excess is a diagnostic flag, not an automatic grading target or identity proof; pose sampling differs from master. Exact pixel joins compare whole current sources.'},indent=2))
print(json.dumps({'references':len(samples),'exactJoins':sum(r['exactRGBA'] for r in joins),'joins':len(joins),'summary':summary}))
