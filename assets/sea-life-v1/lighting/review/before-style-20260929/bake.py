"""Deterministic lighting bake: extends existing code-native light shapes.

Only the caustic uses imagegen. Its preserved source is periodized and resized;
all other shapes extend the game's Bayer halo, arc bubbles and directional blob.
Run with Python, Pillow and NumPy. No network or provider calls.
"""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
FILES = []
BAYER = np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])

def save(name, image, pivot=None, **extra):
    path = ROOT / name
    image.save(path)
    meta=dict(path=name, dimensions=list(image.size), pivot=pivot,
        fps=0, frames=1, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    meta.update(extra)
    FILES.append(meta)
    return image

def rgba(alpha):
    data = np.full((*alpha.shape,4),255,dtype=np.uint8)
    data[:,:,3] = np.uint8(np.clip(alpha,0,1)*255+.5)
    return Image.fromarray(data)

def halo():
    y,x=np.mgrid[:128,:128]
    # Exact 64px fallback profile expanded 2x; no extra world-space light.
    d=np.hypot((x//2+.5-32)/32,(y//2+.5-32)/32)
    v=np.maximum(0,1-d)**2
    threshold=(BAYER[(y//2)%4,(x//2)%4]+.5)/16-.5
    return rgba(np.floor(v*5+.5+threshold*.6)/5)

warm=save('lamp-glow-warm-128.png',halo(),[64,64],tintable=True)
# Warm/cool are intentionally identical luminance; existing runtime tint governs.
save('lamp-glow-cool-128.png',halo(),[64,64],tintable=True)
y,x=np.mgrid[:128,:128]
d=np.hypot((x+.5-64)/62,(y+.5-64)/27)
v=np.maximum(0,1-d)**2
threshold=(BAYER[y%4,x%4]+.5)/16-.5
save('lamp-glow-wide-128.png',rgba(np.floor(v*7+.5+threshold*.5)/7),[64,64],tintable=True,usage='review-only floor-pool variant')

for i in range(3):
    y,x=np.mgrid[:1024,:256]
    t=(y+.5)/1024
    centre=54+i*17+t*(140-i*23)
    width=12+26*t+i*6
    beam=np.exp(-((x-centre)/width)**2)*np.sin(np.pi*t)**2
    # Fine dim threads keep a painted, dithered falloff at actual source pixels.
    beam*=.90+.10*np.sin(x*.37+y*.021+i)
    threshold=(BAYER[y%4,x%4]+.5)/16-.5
    beam=np.clip(np.floor(beam*24+threshold*.4)/24,0,1)*.6
    beam[:2]=0;beam[-2:]=0;beam[:,:2]=0;beam[:,-2:]=0
    name='light-shaft-256x1024.png' if i==0 else f'light-shaft-256x1024-v{i+1}.png'
    save(name,rgba(beam),[128,512],tintable=True,usage='review-only; procedural shafts remain active')

source=Image.open(ROOT/'sources/caustics-generated.png').convert('L').resize((512,512),Image.Resampling.LANCZOS)
a=np.array(source,dtype=float)/255
# Blend original and half-period translations with zero derivative at boundaries.
# Edge correction guarantees equal opposite texels; review includes 2x2 repeat.
for axis in (0,1):
    w=np.sin(np.pi*np.arange(512)/512)**2
    w=w[:,None] if axis==0 else w[None,:]
    a=a*w+np.roll(a,256,axis=axis)*(1-w)
a=(np.maximum(0,a-.08)/.92)**1.55
a[-1,:]=a[0,:];a[:,-1]=a[:,0]
caustic=save('caustics-tile-512.png',Image.fromarray(np.uint8(np.clip(a,0,1)*255)).convert('RGBA'),[0,0],tintable=True,seamless=True,world_period_cells=6)

atlas=Image.new('RGBA',(128,32),(255,255,255,0))
for i in range(4):
    y,x=np.mgrid[:32,:32]
    # Same registered radius makes destination scaling match existing arc radius.
    d=np.hypot(x+.5-16,y+.5-16)
    angle=np.arctan2(y+.5-16,x+.5-16)
    rim=np.maximum(0,1-np.abs(d-12)/(.75+i*.10))
    rim*=.60+.25*np.cos(angle+2.3)
    spot=np.exp(-((x+.5-12.4)**2+(y+.5-12.4)**2)/(1.6+i*.15)**2)
    # White tintable rim: runtime keeps .42 fade, highlight ratio .50/.42.
    cell=rgba(np.maximum(rim*.84,spot))
    pixels=np.array(cell)
    pixels[:,:,:3]=np.uint8(np.where((spot>rim*.84)[:,:,None],
        np.array([255,255,255]),np.array([184,235,250])))
    cell=Image.fromarray(pixels)
    atlas.paste(cell,(i*32,0))
save('hull-bubbles-atlas.png',atlas,[16,16],frames=4,cell=[32,32],grid=[4,1],rim_radius=12,tintable=True)

y,x=np.mgrid[:128,:128]
dx=(x+.5-64)/64;dy=(y+.5-64)/64
r=np.hypot(dx,dy)
base=np.maximum(0,1-r)**2
# Lobe faces +X and stays inside the original circular extent.
lobe=np.exp(-((dx-.30)/.30)**2-(dy/.17)**2)*np.maximum(0,1-r)
beacon=rgba(np.minimum(1,.38*base+.62*lobe))
save('beacon-glow-128.png',beacon,[64,64],tintable=True,direction='+x')

(ROOT/'manifest.json').write_text(json.dumps(dict(version=1,files=FILES,
    source=dict(path='sources/caustics-generated.png',sha256=hashlib.sha256((ROOT/'sources/caustics-generated.png').read_bytes()).hexdigest()),
    density='Lamp halo retains existing 2 world-unit Bayer pixels; bubble rims use 32px registered cells. Shader maps scale in world cells.'),indent=2)+'\n')

review=Image.new('RGB',(1200,920),(10,24,31));draw=ImageDraw.Draw(review)
draw.text((24,16),'BRINESPACE / LIGHTING BATCH 2 / white luminance, runtime tint',fill=(180,213,215))
for i,name in enumerate(['lamp-glow-warm-128.png','lamp-glow-cool-128.png','lamp-glow-wide-128.png','beacon-glow-128.png']):
    im=Image.open(ROOT/name)
    color=(255,230,178) if i==0 else ((235,247,255) if i<3 else (255,45,25))
    tint=Image.new('RGBA',im.size,(*color,255));tint.putalpha(im.getchannel('A'))
    review.paste(tint,(30+i*290,58),tint)
    draw.text((24+i*290,203),name,fill=(180,213,215))
im=atlas.resize((512,128),Image.Resampling.NEAREST)
review.paste(im,(24,245),im);draw.text((24,385),'Hull rims / 4 cells / enlarged 4x',fill=(180,213,215))
for i in range(3):
    name='light-shaft-256x1024.png' if i==0 else f'light-shaft-256x1024-v{i+1}.png'
    im=Image.open(ROOT/name).resize((112,448),Image.Resampling.LANCZOS)
    review.paste(im,(24+i*170,425),im)
    draw.text((24+i*170,888),f'Shaft {i+1} / REVIEW ONLY',fill=(180,213,215))
tile=caustic.convert('RGB').resize((280,280))
for yy in range(2):
    for xx in range(2): review.paste(tile,(610+xx*280,310+yy*280))
draw.text((610,888),'Caustics / 2 x 2 repeat / shader tint applied at runtime',fill=(180,213,215))
review.save(ROOT/'review/contact-sheet.jpg',quality=94)
print('Baked',len(FILES),'lighting PNGs')
