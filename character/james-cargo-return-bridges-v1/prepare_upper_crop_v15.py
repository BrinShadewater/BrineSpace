from pathlib import Path
import json,hashlib
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'upper-crop-v15';out.mkdir(exist_ok=True)
sources=[('target',p/'frames-v9/bare/002.png',(0,0)),('previous',p/'frames-v9/bare/001.png',(0,0)),('idle',r/'character/crew-runtime-matte-v1/branforth/frames/idle-west-breathing-v1/000.png',(36,52))]
records=[]
for label,path,translation in sources:
    im=Image.open(path).convert('RGBA');reg=Image.new('RGBA',(256,256));reg.alpha_composite(im,translation)
    crop=reg.crop((96,56,176,136));magnified=crop.resize((640,640),Image.Resampling.NEAREST)
    magnified.save(out/(label+'.png'))
    records.append({'label':label,'source':str(path.relative_to(r)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'crop':[96,56,80,80],'magnification':8,'registration':translation,'reference':str((out/(label+'.png')).relative_to(r)),'referenceSha256':hashlib.sha256((out/(label+'.png')).read_bytes()).hexdigest()})
(out/'references.json').write_text(json.dumps({'sources':records,'scope':'Deterministic reference crops/enlargement only; no repainted pixels.'},indent=2)+'\n')
print('Three enlarged upper-body reference crops, hashes and original registration retained.')
