from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2]
frames=[np.array(Image.open(P/f'full-clip-frames-v2/{n:03}.png').convert('RGBA')) for n in range(142)]
scores=[]
for lag in range(10,49):
 errors=[]
 for n in range(12,80):
  a,b=frames[n][155:231,65:190],frames[n+lag][155:231,65:190]
  mask=(a[:,:,3]>128)|(b[:,:,3]>128)
  errors.append(float(np.abs(a.astype(float)-b.astype(float))[mask].mean()))
 scores.append({'lag':lag,'meanLowerBodyRGBAError':float(np.mean(errors))})
scores.sort(key=lambda r:r['meanLowerBodyRGBAError'])
selected=[0,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48]
board=Image.new('RGB',(1800,1152),(32,43,49));d=ImageDraw.Draw(board)
for j,n in enumerate(selected):
 im=Image.fromarray(frames[n]).crop((65,150,190,231)).resize((300,194),Image.Resampling.NEAREST)
 xy=((j%6)*300,(j//6)*288);board.paste(im,(xy[0],xy[1]+30),im);d.text((xy[0]+4,xy[1]+6),f'raw{n}: whole lower body',fill='white')
board.save(P/'leg-phase-review.png')
(P/'leg-phase-diagnostic.json').write_text(json.dumps({'rankedAppearanceLags':scores,'scope':'Read-only complete lower-body appearance recurrence and enlarged phase board. Similarity is not near/far anatomical identity, support/loop/stride admission. Original142source poses and frozen native inputs untouched.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'bestAppearanceLags':scores[:6]}))
