from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/james-rest-material-continuity-v1'
e=json.loads((S/'material-evidence.json').read_bytes()); rows=[]
atlas=Image.new('RGBA',(1800,1200),(0,0,0,0));masters=Image.new('RGBA',(600,300),(0,0,0,0))
for row,(mode,action) in enumerate([('bare','lie-down'),('bare','sleep'),('helmet','lie-down'),('helmet','sleep')]):
    for index in range(6):
        entry=next(r for r in e['records'] if r['mode']==mode and r['key']==action+'-south' and r['index']==index)
        source=S/entry['output'];im=Image.open(source).convert('RGBA');x0,y0,x1,y1=entry['protectedHead'];cx=(x0+x1)//2;cy=(y0+y1)//2
        box=(cx-25,cy-25,cx+25,cy+25);crop=im.crop(box).resize((300,300),Image.Resampling.NEAREST)
        atlas.paste(crop,(index*300,row*300))
        if action=='lie-down' and index==0:masters.paste(crop,(0 if mode=='bare' else 300,0))
        rows.append({'row':row,'column':index,'mode':mode,'key':action+'-south','index':index,'source':str(source.relative_to(R)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'canonicalCrop':box,'atlasCell':[index*300,row*300,(index+1)*300,(row+1)*300],'protectedHead':entry['protectedHead']})
atlas.save(P/'head-atlas-edit-target.png');masters.save(P/'head-master-reference.png')
(P/'head-atlas-inputs.json').write_text(json.dumps({'atlasSize':[1800,1200],'canonicalCellSize':[50,50],'nearestEnlargement':6,'rows':rows,'reference':'head-master-reference.png'},indent=2)+'\n')
print('Prepared24 South head crops and two exact master references, canonical positions frozen.')
