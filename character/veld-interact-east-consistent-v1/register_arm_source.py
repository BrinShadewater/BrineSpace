"""Register four generated arm-source poses; no generation call on rebuild."""
from pathlib import Path
from PIL import Image
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
im=Image.open(HERE/'arm-repair-source-v3.png').convert('RGBA')
w,h=im.size
ref=np.array(Image.open(ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png').convert('RGBA'))
ys,xs=np.where(ref[:,:,3]>200)
lo,hi=ys.min(),ys.max()
foot_reference=np.where(ref[hi-5:hi+1,:,3]>200)[1].mean()
canvas=Image.new('RGBA',(736,184))
for i in range(4):
    cell=im.crop((round(i*w/4),0,round((i+1)*w/4),h))
    a=np.array(cell);y,x=np.where(a[:,:,3]>200)
    scale=(hi-lo+1)/(y.max()-y.min()+1)
    foot=np.where(a[y.max()-5:y.max()+1,:,3]>200)[1].mean()
    left=round(foot_reference-(foot-x.min())*scale)
    crop=cell.crop((x.min(),y.min(),x.max()+1,y.max()+1))
    crop=crop.resize((round(crop.width*scale),hi-lo+1),Image.Resampling.LANCZOS)
    reg=Image.new('RGBA',(184,184));reg.alpha_composite(crop,(left,lo))
    reg.save(HERE/f'pose-arm-source-v3-{i+1:03}.png')
    canvas.alpha_composite(reg,(i*184,0))
canvas.save(HERE/'arm-source-registered-v3.png')
