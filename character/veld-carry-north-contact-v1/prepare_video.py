from pathlib import Path
import hashlib,json
from PIL import Image
import numpy as np
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1];D=R/'character/veld-carry-north-contact-video-v1'
assert not (D/'generation.json').exists(),'Do not alter frozen generation input'
D.mkdir(exist_ok=True)
source=R/'character/veld-cargo-north-original-master-v3/raw-unload-v6.png'
a=np.array(Image.open(source).convert('RGBA'));lab,n=ndimage.label(a[:,:,3]>200);cells=[]
for k in range(1,n+1):
    yy,xx=np.where(lab==k)
    if len(xx)>10000:cells.append((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1),k))
cells.sort();assert len(cells)==6
x0,y0,x1,y1,k=cells[0];box=(max(0,x0-5),max(0,y0-5),min(a.shape[1],x1+5),min(a.shape[0],y1+5))
lo,up,hi,down=box;cell=a[up:down,lo:hi].copy();keep=ndimage.binary_dilation((lab==k)[up:down,lo:hi],iterations=3);cell[~keep]=0
fig=Image.fromarray(cell);fig.save(D/'whole-held-source.png')
assert fig.height<700 and fig.width<700
bg=Image.new('RGBA',(768,768),(0,255,0,255));offset=((768-fig.width)//2,700-fig.height);bg.alpha_composite(fig,offset);dest=D/'master-input.png';bg.convert('RGB').save(dest)
prompt='''Locked camera, isolated game character animation on unchanged solid green background. The same woman seen straight from behind, facing NORTH away from viewer, walks forward at a calm natural cargo-carrying pace while remaining centered for a sprite loop. Keep exact original body height, compact head and brown bun, shoulder and hip breadth, limb lengths, dark matte charcoal quilted suit, blue patches and muted metal straps/cuffs/boots throughout. Arms remain bent holding an unseen case in FRONT; do not invent backpack or case behind her. Cyan belt tool on screenLEFT, three silver cylinders screenRIGHT, never mirror. Show at least three complete balanced alternating walk cycles. Each supporting foot stays planted on the implied ground while hips move over it: stance foot travels from forward/up-screen to trailing/down-screen RELATIVE TO THE HIPS; the other foot lifts, passes forward and lands, then switches support. Natural connected hips/knees/ankles, quiet body bob, relaxed carry gait, no stationary alternating knee lifts, no skating, running or shuffling. Keep head/torso registration stable with tiny natural bob. Same elevated straight rear orthographic camera, no turn, zoom, pan, shrink, growth, lighting change, gray hair, shiny fabric, halo or ground shadow. Whole silhouette always visible with margins; background exactly solid green throughout.'''
(D/'prompt.txt').write_text(prompt+'\n')
(D/'input-registration.json').write_text(json.dumps({'source':source.relative_to(R).as_posix(),'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceBox':box,'sourceScale':1,'wholeSourceSize':list(fig.size),'offset':offset,'videoInputSHA256':hashlib.sha256(dest.read_bytes()).hexdigest(),'scope':'Whole first held pose extraction; original RGB untouched; solid matte backdrop for video. No per-limb edits or source scaling.'},indent=2)+'\n')
print(json.dumps({'size':list(fig.size),'offset':offset,'input':dest.relative_to(R).as_posix(),'promptCharacters':len(prompt)}))
