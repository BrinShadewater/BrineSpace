from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from matte import registered,metrics
P=Path(__file__).resolve().parent
master=Image.open(P/'registered-reference.png').convert('RGBA');candidate=registered(Image.open(P/'master-input.png'));candidate.save(P/'input-alpha-control.png')
a=np.array(master);b=np.array(candidate);ma=a[:,:,3]>128;mb=b[:,:,3]>128
report={'master':metrics(master),'control':metrics(candidate),'alphaIoU':float((ma&mb).sum()/(ma|mb).sum()),'opaqueIntersectionRgbMAE':float(np.abs(a[:,:,:3].astype(int)-b[:,:,:3].astype(int))[ma&mb].mean()),'fixedBackgroundRGB':[12,18,24],'fixedLInfinityTolerance':8,'globalErosionRawPixels':1,'scope':'Preflight on known authored input only. One frozen alpha rule and fixed1/3 mapping; no RGB decontamination/grading/body patches. Does not prove returned video matte/background stability.'}
(P/'matte-preflight.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(768,610),(32,43,49));d=ImageDraw.Draw(board)
for i,(im,label) in enumerate([(master,'Original native'),(candidate,'Dark-input alpha control')]):
 board.paste(im,(i*384+64,25),im);d.text((i*384+5,5),label,fill='white');crop=im.crop((98,70,170,165)).resize((216,285),Image.Resampling.NEAREST);board.paste(crop,(i*384+40,300),crop)
board.save(P/'alpha-control-master-review.png');print(json.dumps(report))
