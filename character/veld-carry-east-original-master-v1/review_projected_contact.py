"""Compare projected near/far floor levels; never alter source anatomy."""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np,json
P=Path(__file__).resolve().parent;R=P.parents[1]
paths=[R/'character/veld-east-held-original-master-v1/frames/bare/000.png',P/'touchdown-source-v1/transition-candidate.png',P/'touchdown-source-v2/transition-candidate.png']
labels=['Original held master','Touchdown v1','Original-only touchdown v2']
board=Image.new('RGB',(1140,400),(32,43,49));d=ImageDraw.Draw(board);rows=[]
for i,(p,label) in enumerate(zip(paths,labels)):
 im=Image.open(p).convert('RGBA');a=np.array(im);crop=im.crop((100,185,180,232)).resize((320,188),Image.Resampling.NEAREST)
 x=20+i*380;y=80;board.paste(crop,(x,y),crop)
 d.text((x,20),label,fill='white')
 for level,color,name in [(223,(235,174,99),'near master floor223'),(220,(116,187,229),'far master floor220')]:
  yy=y+(level-185)*4+2;d.line((x,yy,x+319,yy),fill=color,width=1);d.text((x,280+(223-level)*8),name,fill=color)
 # Distal far boot region excludes overlapping near boot; this is only extent.
 mask=a[211:225,143:180,3]>200;ys,xs=np.where(mask)
 rows.append({'source':str(p.relative_to(R)).replace('\\','/'),'distalFarBootOpaqueBottom':int(ys.max()+211),'nearMasterFloor':223,'farMasterFloor':220,'scope':'Distal far-foot extent, not heel landmark or calibrated physical support.'})
board.save(P/'projected-contact-source-review.png')
(P/'projected-contact-source-review.json').write_text(json.dumps({'rows':rows,'interpretation':'Original master projects far boot three pixels above near boot. Screen-height difference alone cannot establish airborne foot. V2 visibly extends the far leg with heel low and toe raised; retain as provisional contact source pending native material/proportion and moving root calibration. Same-horizontal-floor prompt conflicts with original depth convention; future sources should follow projected far floor. No anatomy/grade patches.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows))
