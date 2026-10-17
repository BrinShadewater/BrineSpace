from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
sources=[R/'character/veld-cargo-north-original-master-v2/diagnostic-frames/005.png',P/'diagnostic-frames/005.png',R/'character/veld-idle-north-original-master-v1/clean-idle-master.png']
board=Image.new('RGB',(768,550),'#202a30');d=ImageDraw.Draw(board);rows=[]
for i,(label,path) in enumerate(zip(['Previous V4 material','Repaired V6 material','Original-guided rest master'],sources)):
    im=Image.open(path).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float)
    sample=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<15)&(rgb.mean(2)>20)&(rgb.mean(2)<180)
    region=np.zeros((256,256),bool);region[142:175,108:149]=True;sample&=region
    rows.append({'label':label,'source':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'neutralUpperLegSampleCount':int(sample.sum()),'lumaQuantiles':np.percentile(rgb[sample].mean(1),[25,50,75]).round(2).tolist()})
    d.text((i*256+4,5),label,fill='white');board.paste(im,(i*256,30),im)
    detail=im.crop((100,135,158,220)).resize((174,255),Image.Resampling.NEAREST);board.paste(detail,(i*256+40,285),detail)
board.save(P/'material-master-comparison.png')
(P/'material-audit.json').write_text(json.dumps({'diagnosticOnly':'Neutral upper-leg region142:175,108:149; broad area statistic includes pose/texture differences, not a material acceptance gate. Visually compare all action interiors to master.','samples':rows},indent=2)+'\n')
print(json.dumps(rows))
