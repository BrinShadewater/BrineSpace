"""Reproducible card-art registration and native UI symbol extension.

Imagegen supplies painted frame/back sources. Tiny emblems extend the existing
code-native UI symbol language with deterministic silhouettes and matte tones.
Pillow/NumPy only; no provider calls. Runtime scale is preserved at 200x284.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageOps,ImageFont
ROOT=Path(__file__).resolve().parent
FILES=[]
def save(name,im,**meta):
    p=ROOT/name;im.save(p)
    row=dict(path=name,dimensions=list(im.size),pivot=[im.width/2,im.height/2],fps=0,frames=1,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    row.update(meta);FILES.append(row)
    return im
def registered(name):
    im=Image.open(ROOT/'sources'/name).convert('RGBA')
    bbox=im.getchannel('A').point(lambda x:255 if x>8 else 0).getbbox()
    return im.crop(bbox).resize((200,284),Image.Resampling.LANCZOS)

frame=registered('frame-generated.png')
# Register the perimeter inside existing 8px content margins. The native source
# is reduced once; fine metal variation survives, with no artificial pixel filter.
outer=Image.new('L',(800,1136));d=ImageDraw.Draw(outer)
d.rounded_rectangle((0,0,799,1135),48,fill=255)
inner=Image.new('L',(800,1136));d=ImageDraw.Draw(inner)
d.rounded_rectangle((24,24,775,1111),24,fill=255)
mask=np.array(outer.resize((200,284),Image.Resampling.LANCZOS),dtype=float)-np.array(inner.resize((200,284),Image.Resampling.LANCZOS),dtype=float)
a=np.array(frame);lum=np.array(ImageOps.grayscale(frame),dtype=float)
# Preserve charcoal seams instead of lifting every source tone toward white.
# Calibrate the source's matte midrange to a readable raised-metal/recess split.
tone=np.clip((lum/255-.06)/.52,0,.96)
for c in range(3):a[:,:,c]=np.uint8(tone*255+.5)
a[:,:,3]=np.uint8(np.clip(mask,0,255))
save('card-frame.png',Image.fromarray(a),slice_margins=[16,16,16,16],content_margins=[8,8,8,7],tintable=True)
save('card-back.png',registered('back-generated.png'),tintable=False,usage='retained pile renderer only; live piles remain hidden')

def symbol(name,size,draw):
    scale=4;mask=Image.new('L',(size*scale,size*scale));d=ImageDraw.Draw(mask)
    # Work on a common 64-unit drawing surface, then reduce exactly once.
    def poly(points,fill=255):d.polygon([(int(x*size/64*scale),int(y*size/64*scale)) for x,y in points],fill=fill)
    def ellipse(box,fill=255):d.ellipse(tuple(int(x*size/64*scale) for x in box),fill=fill)
    def rect(box,fill=255):d.rectangle(tuple(int(x*size/64*scale) for x in box),fill=fill)
    draw(poly,ellipse,rect)
    alpha=mask.resize((size,size),Image.Resampling.LANCZOS)
    y,x=np.mgrid[:size,:size]
    tone=216+12*np.sin(x*.19+y*.09)+7*np.sin(y*.43-x*.17)
    out=np.zeros((size,size,4),dtype=np.uint8)
    for c in range(3):out[:,:,c]=np.uint8(tone)
    out[:,:,3]=np.array(alpha)
    return save(name,Image.fromarray(out),tintable=True)
def operations(p,e,r):
    p([(32,6),(38,25),(58,32),(38,39),(32,58),(26,39),(6,32),(26,25)])
    e((26,26,38,38),0)
def engineering(p,e,r):
    e((14,14,50,50))
    for i in range(8):
        a=i*math.pi/4;p([(32+math.cos(a+s)*rad,32+math.sin(a+s)*rad) for s,rad in [(-.2,20),(-.2,28),(.2,28),(.2,20)]])
    e((24,24,40,40),0)
def science(p,e,r):
    r((25,7,39,13));r((29,13,35,29));p([(29,26),(35,26),(53,54),(11,54)])
    p([(25,39),(39,39),(44,48),(20,48)],0)
def support(p,e,r):
    p([(11,11),(35,12),(51,28),(47,46),(31,51),(16,37)])
    p([(20,20),(24,20),(53,54),(49,57)],0)
    p([(24,28),(38,24),(40,28),(27,32)],0)
def recreation(p,e,r):
    r((10,24,54,42));r((7,22,15,48));r((49,22,57,48));r((17,12,47,31));r((12,45,18,54));r((46,45,52,54));r((19,29,45,32),0)
def anomaly(p,e,r):
    p([(32,5),(57,32),(32,59),(7,32)])
    p([(34,9),(25,28),(38,32),(28,56),(43,29),(30,25)],0)
def robotics(p,e,r):
    r((17,17,47,47));r((24,24,40,40),0)
    for i in range(4):
        q=19+i*7;r((q,8,q+3,16));r((q,48,q+3,56));r((8,q,16,q+3));r((48,q,56,q+3))
def derelict(p,e,r):
    p([(9,16),(25,8),(41,10),(56,23),(51,52),(35,57),(10,49)])
    p([(24,17),(37,18),(46,27),(42,43),(26,47),(18,41),(17,25)],0)
    p([(40,8),(31,29),(39,32),(28,56),(45,33),(37,28),(50,17)],0)
for key,draw in [('operations',operations),('engineering',engineering),('science',science),('life-support',support),('recreation',recreation),('anomaly',anomaly),('robotics',robotics),('derelict',derelict)]:symbol('emblem-'+key+'.png',64,draw)
def core(p,e,r):e((8,8,56,56));e((14,14,50,50),0);e((24,24,40,40));r((30,6,35,21),0)
def common(p,e,r):p([(32,12),(52,32),(32,52),(12,32)]);p([(32,22),(42,32),(32,42),(22,32)],0)
def uncommon(p,e,r):p([(23,8),(38,28),(23,48),(8,28)]);p([(42,18),(57,38),(42,58),(27,38)])
def rare(p,e,r):p([(32,5),(43,20),(32,35),(21,20)]);p([(16,27),(27,43),(16,59),(5,43)]);p([(48,27),(59,43),(48,59),(37,43)])
for key,draw in [('core',core),('common',common),('uncommon',uncommon),('rare',rare),('derelict',derelict)]:symbol('rarity-'+key+'.png',48,draw)
sources=[dict(path='sources/'+p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),dimensions=list(Image.open(p).size)) for p in sorted((ROOT/'sources').glob('*.png'))]
(ROOT/'manifest.json').write_text(json.dumps(dict(schema=1,files=FILES,sources=sources,logical_card_size=[200,284],sampling='plain linear; emblems 16px and rarity marks 12px; no UI resize'),indent=2)+'\n')

board=Image.new('RGB',(1200,670),'#101e26');d=ImageDraw.Draw(board)
d.text((24,15),'BRINESPACE / CARD ART / painted frame + printed monochrome marks',fill='#d5e3e3')
for i,name in enumerate(['card-frame.png','card-back.png']):
    im=Image.open(ROOT/name);board.paste(im,(24+i*240,55),im);d.text((24+i*240,352),name,fill='#d5e3e3')
for i,entry in enumerate(FILES[2:]):
    col=i%7;row=i//7;im=Image.open(ROOT/entry['path'])
    x=24+col*165;y=425+row*115
    board.paste(im,(x,y),im);d.text((x,y+65),entry['path'].replace('emblem-','').replace('rarity-','mark-').replace('.png',''),fill='#d5e3e3')
d.text((530,75),'200 x 284 / 16px nine-slice corners',fill='#d5e3e3')
d.text((530,103),'Content margins unchanged: 8 / 8 / 8 / 7',fill='#d5e3e3')
d.text((530,131),'Icons render beside existing text; no label shift',fill='#d5e3e3')
d.text((530,159),'Back delivered; hidden deck controls stay hidden',fill='#d5e3e3')
board.save(ROOT/'review/contact-sheet.jpg',quality=95)
print('Baked',len(FILES),'card PNGs')
