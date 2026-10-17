from pathlib import Path
import json,hashlib
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'upper-crop-v16';out.mkdir(exist_ok=True)
sources=[('target',p/'frames-v9/helmet/002.png',(0,0)),('previous',p/'frames-v9/helmet/001.png',(0,0)),('idle',r/'character/james-shared-helmet-runtime-v1/frames/idle-west/000.png',(36,52)),('bare-paired',p/'upper-v15-bare.png',(0,0))]
records=[]
for label,path,translation in sources:
    im=Image.open(path).convert('RGBA');reg=Image.new('RGBA',(256,256));reg.alpha_composite(im,translation)
    reg.crop((96,56,176,136)).resize((640,640),Image.Resampling.NEAREST).save(out/(label+'.png'))
    records.append({'label':label,'source':str(path.relative_to(r)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'crop':[96,56,80,80],'magnification':8,'registration':translation,'reference':str((out/(label+'.png')).relative_to(r)),'referenceSha256':hashlib.sha256((out/(label+'.png')).read_bytes()).hexdigest()})
(out/'references.json').write_text(json.dumps({'sources':records,'scope':'Deterministic reference crops only, paired bare trial is not selected.'},indent=2)+'\n')
print('Four registered helmet/paired bare references preserved.')
