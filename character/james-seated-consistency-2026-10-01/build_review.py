"""Read-only selected seated source and neighboring-master review."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
coverage=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text())
records=[];joins=[]
def load(mode,key):
    f=R/coverage['body' if mode=='bare' else 'equipment'][key]['path'];m=json.loads(f.read_text());s=next(x for x in m['states'] if x['id']==key)
    paths=[R/x[6:] if x.startswith('res://') else (f.parent/x).resolve() for x in s['frameFiles']]
    return m,s,paths
def plane(path,m):
    assert m['standingHeight']==148
    im=Image.open(path).convert('RGBA');out=Image.new('RGBA',(256,256));out.alpha_composite(im,(128-int(m['pivot'][0]),224-int(m['pivot'][1])));return out
for direction in ['south','east','west','north']:
    for mode in ['bare','helmet']:
        b=Image.new('RGB',(7*256,4*280),'#303b40');d=ImageDraw.Draw(b)
        idle_m,idle_s,idle_paths=load(mode,'idle-'+direction);idle=plane(idle_paths[0],idle_m)
        states={}
        for row,action in enumerate(['sit-down','sit-idle','sit-rise','read-seated']):
            key=action+'-'+direction;m,s,paths=load(mode,key);states[action]=[plane(f,m) for f in paths]
            b.paste(idle,(0,row*280+24),idle);d.text((4,row*280+4),mode+' master '+direction,fill='white')
            for i,path in enumerate(paths):
                im=plane(path,m);a=np.array(im);yy,xx=np.where(a[:,:,3]>192);x=(i+1)*256;y=row*280
                b.paste(im,(x,y+24),im);d.text((x+4,y+4),key+' '+str(i),fill='white')
                records.append({'mode':mode,'key':key,'index':i,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pivot':m['pivot'],'standingHeight':m['standingHeight'],'alpha192Bounds':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'durationMs':s['frameDurationsMs'][i]})
        for name,a,z in [('idle-down',idle,states['sit-down'][0]),('down-held',states['sit-down'][-1],states['sit-idle'][0]),('held-rise',states['sit-idle'][-1],states['sit-rise'][0]),('rise-idle',states['sit-rise'][-1],idle),('read-entry',states['sit-idle'][0],states['read-seated'][0]),('read-exit',states['read-seated'][-1],states['sit-idle'][0])]:
            joins.append({'mode':mode,'direction':direction,'join':name,'exactPixels':np.array_equal(np.array(a),np.array(z)),'changedPixels':int(np.any(np.array(a)!=np.array(z),axis=2).sum())})
        b.save(P/(direction+'-'+mode+'-all-poses.png'))
(P/'review-evidence.json').write_text(json.dumps({'references':len(records),'records':records,'joins':joins,'scope':'Current ordered selection, all192 seated source references at fixed148px ruler beside directional idle. Pixel joins are diagnostic: read entry may include tablet. No native furniture/cadence/Continue or visual acceptance claim.'},indent=2)+'\n')
print(json.dumps({'references':len(records),'joins':len(joins),'inexactJoins':[j for j in joins if not j['exactPixels']]}))
