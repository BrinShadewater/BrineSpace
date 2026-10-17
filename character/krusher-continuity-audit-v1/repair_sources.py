from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
import numpy as np
from scipy import ndimage
from scipy.spatial import ConvexHull
H=Path(__file__).resolve().parent;R=H.parents[1];B=R/'character/krusher-style-neck-bank-v1';read=lambda p:json.loads(p.read_text());idx=read(H/'audit-index.json');maps=read(R/'character/krusher-style-neck-v1/bank-mapping.json')['records'];records={q['source']:q for q in read(B/'revision.json')['records']};out=H/'pilot';out.mkdir(exist_ok=True);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),17)
def pad(im,q):
 size=tuple(map(int,q['canvas']))
 if im.size==size:return im
 result=Image.new('RGBA',size);offset=tuple(np.array(q['pivot'],int)-[92,172]) if maps[q['source']].get('paddedCanonical') else (36,52) if im.size==(184,184) else (0,96);result.alpha_composite(im,offset);return result
def cyan(a):
 a=a.copy();r,g,b=[a[:,:,i].astype(float) for i in range(3)];m=(a[:,:,3]>0)&(r>g*.85)&(r<g*1.85)&(g>b*1.12)&(g>32);lum=(r*.2126+g*.7152+b*.0722)/145;colour=np.clip(lum[:,:,None]*[82,124,128],0,190).astype('uint8');a[m,:3]=colour[m];return a
rear=[3378,3383,3386,3395,3400]
polygons={3109:[[174,114],[180,113],[184,114],[184,123],[181,129],[177,128],[173,122]],3137:[[128,87],[141,87],[144,90],[144,99],[141,104],[131,104],[127,100],[126,91]],3207:[[121,108],[132,108],[136,112],[135,120],[131,124],[123,123],[119,118],[119,112]],3379:[[138,105],[145,105],[147,108],[146,115],[142,120],[137,118],[135,113],[135,108]]}
# Native-pixel polygons are inside the observed original visor, excluding its rim/highlights.
