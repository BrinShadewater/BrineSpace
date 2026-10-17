"""Compare effective water poses to selected dry masters with a shared physical scale."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

H=Path(__file__).resolve().parent; R=H.parents[1]
selection=json.loads((H/'candidate-selection.json').read_text())
effective={}
for entry in selection['manifests']:
    manifest=json.loads((R/entry['path']).read_text())
    for state in manifest['states']:
        effective[entry['variant'],state['id']]=(R/entry['path'],manifest,state)
cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text())
board=Image.new('RGBA',(1440,1360),'#202a30'); draw=ImageDraw.Draw(board)
records=[]
for row,direction in enumerate(['north','east','south','west']):
    items=[]
    for variant in ['bare','helmet']:
        selected=cov['selected'][variant]['idle-'+direction]
        master=json.loads((R/selected['manifest']).read_text())
        items.append((variant+' selected idle',R/selected['files'][0],master))
    for key in ['tread-'+direction,'swim-'+direction]:
        for variant in ['bare','helmet']:
            path,manifest,state=effective[variant,key]
            items.append((variant+' '+key,path.parent/state['frameFiles'][0],manifest))
    for col,(title,path,manifest) in enumerate(items):
        im=Image.open(path).convert('RGBA'); factor=148/manifest['standingHeight']
        resized=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS)
        pivot=manifest['pivot']; anchor=(col*240+120,row*340+210)
        pos=(round(anchor[0]-pivot[0]*factor),round(anchor[1]-pivot[1]*factor))
        board.alpha_composite(resized,pos)
        draw.text((col*240+5,row*340+8),title,fill='white')
        # Same physical scale. Water pivots intentionally differ from dry foot pivots.
        records.append({'title':title,'path':path.relative_to(R).as_posix(),'standingHeight':manifest['standingHeight'],'canvas':list(im.size),'pivot':pivot,'displayFactor':factor,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
board.save(H/'direction-master-audit-v8.png')
(H/'direction-master-audit-v8.json').write_text(json.dumps({'scope':'four-direction selected idle vs effective staged tread/swim slot0; shared standingHeight148 physical scale; no per-pose bounding box normalization','records':records},indent=2)+'\n')
N=R/'character/veld-water-north-coherent-v1'; checks=0; changed=0
for old in (N/'revisions/patch-ownership-v1/frames').rglob('*.png'):
    new=N/'frames'/old.relative_to(N/'revisions/patch-ownership-v1/frames')
    a=np.array(Image.open(old));b=np.array(Image.open(new))
    assert a.shape==b.shape and np.array_equal(a[:,:,3],b[:,:,3]);checks+=1
    changed+=int(np.any(a!=b,axis=2).sum())
(N/'patch-rebuild-checks-v2.json').write_text(json.dumps({'checks':checks,'failures':0,'changedPixelReferences':changed,'scope':'all48 frames keep exact alpha/geometry after source-owned patch grade correction'},indent=2)+'\n')
print(f'{checks} alpha/geometry checks PASS; {changed} changed pixel references.24 master/pose audit panels saved.')
