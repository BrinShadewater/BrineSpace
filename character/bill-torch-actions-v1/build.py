"""Freeze all four independently authored torch candidates into one runtime pack."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
manifest={'name':'Bill new blowtorch actions','status':'owner_visual_accepted_2026_09_29_axial_v2','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','states':[]}
hashes={}
tips={}
for direction in ['east','west','south','north']:
    source=HERE.parent/f'bill-torch-{direction}-coherent-v1'
    pack=json.loads((source/'manifest.json').read_text())
    for state in pack['states']:
        for rel in state['frameFiles']:
            target=HERE/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/rel,target)
            hashes[rel]=hashlib.sha256(target.read_bytes()).hexdigest()
        manifest['states'].append(state)
        if state['id'].startswith('weld-'):
            points=[]
            for rel in state['frameFiles']:
                a=np.asarray(Image.open(HERE/rel).convert('RGBA'));yy,xx=np.indices(a.shape[:2])
                outside=xx<108 if direction=='west' else (xx>145 if direction=='east' else (((yy>60)&(yy<100)&(xx>135)) if direction=='north' else ((yy>130)&(yy<190))))
                mask=(a[:,:,3]>180)&(a[:,:,0]>210)&(a[:,:,1]>110)&(a[:,:,2]<150)&outside
                y,x=np.where(mask);assert len(x)>0,rel
                points.append([(float(np.mean(x))-128)*65.28/148,(float(np.mean(y))-224)*65.28/148+384*.038])
            tips[direction]=np.mean(points,axis=0).round(4).tolist()
for name,data in [('manifest.json',manifest),('frame-hashes.json',hashes)]:
    (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
(HERE/'torch-tip-offsets.json').write_text(json.dumps(tips,indent=2)+'\n')
print('Bill torch runtime pack: 12 clips,72 frame references')
