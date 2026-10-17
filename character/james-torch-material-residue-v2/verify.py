from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'build-evidence.json').read_text());frozen=json.loads((P/'source-bindings.json').read_text());checks=0
def check(ok,message):
    global checks
    checks+=1
    assert ok,message
def image(path):return np.array(Image.open(path).convert('RGBA'))
joins=[]
for mode in ['bare','helmet']:
    m=json.loads((P/f'{mode}-manifest.json').read_text());check(m['pivot']==[92,172] and m['standingHeight']==148,'Original ruler/pivot')
    for s in m['states']:
        original=R/frozen['coverage']['body' if mode=='bare' else 'equipment'][s['id']]['path'];oldm=json.loads(original.read_text());old=next(x for x in oldm['states'] if x['id']==s['id'])
        for key in old:
            if key not in ['frameFiles','provenance']:check(s[key]==old[key],'Original metadata '+key)
        for index,file in enumerate(s['frameFiles']):
            r=next(x for x in e['records'] if x['mode']==mode and x['key']==s['id'] and x['index']==index)
            source=R/r['source'];a=image(source);b=image(R/r['destination']);check(hashlib.sha256(source.read_bytes()).hexdigest()==r['sourceSha256'],'Frozen source bytes')
            check(file.startswith('res://') and len(s['frameFiles'])==old['frameCount'],'Whole path/frame count')
            check(np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[:60],b[:60]),'Exact silhouette/head/shell')
            check(r['maxLumaRoundingDifference']<=.5,'Brightness retained within byte rounding')
            rgb=a[:,:,:3].astype(float);red,green,blue=rgb.transpose(2,0,1)
            warm=(red-blue>12)&(green-blue>8)&(red>=green-2)
            flame=(blue>red+25)&(green>red+15)
            check(np.array_equal(a[warm|flame],b[warm|flame]),'Engineering yellow and blue/cyan exact')
    for direction in ['east','north','south','west']:
        def state(name):return next(x for x in m['states'] if x['id']==name+'-'+direction)
        masterpath=R/frozen['coverage']['body' if mode=='bare' else 'equipment']['idle-'+direction]['path'];masterm=json.loads(masterpath.read_text());master=next(x for x in masterm['states'] if x['id']=='idle-'+direction)['frameFiles'][0];masterpath=R/master.removeprefix('res://') if master.startswith('res://') else masterpath.parent/master
        paths=[masterpath,R/state('torch-draw')['frameFiles'][0].removeprefix('res://'),R/state('torch-draw')['frameFiles'][-1].removeprefix('res://'),R/state('weld')['frameFiles'][0].removeprefix('res://'),R/state('weld')['frameFiles'][-1].removeprefix('res://'),R/state('torch-stow')['frameFiles'][0].removeprefix('res://'),R/state('torch-stow')['frameFiles'][-1].removeprefix('res://'),masterpath]
        for i in range(4):check(np.array_equal(image(paths[2*i]),image(paths[2*i+1])),'Exact whole-source transition');joins.append({'mode':mode,'direction':direction,'join':i,'exact':True})
report={'checks':checks,'failures':0,'references':len(e['records']),'exactJoins':len(joins),'changedReferences':e['changedReferences'],'maxLumaRoundingDifference':max(x['maxLumaRoundingDifference'] for x in e['records'])}
(P/'package-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
