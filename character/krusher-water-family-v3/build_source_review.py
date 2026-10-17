from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
P=Path(__file__).resolve().parent;R=P.parent.parent;qs=json.loads((P/'revision.json').read_text())['records'];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),20)
changed=[q for q in qs if q['changedPixels']]
for start in range(0,len(changed),16):
 rows=changed[start:start+16];board=Image.new('RGB',(1024,1210),'#252b2e');draw=ImageDraw.Draw(board);draw.text((15,12),'KRUSHER / FULL HEAD AND NECK / REVISED E-S-W',font=font,fill='white')
 for j,q in enumerate(rows):
  x=j%4*256;y=50+j//4*290;im=Image.open(P/q['output']).convert('RGBA');board.paste(im,(x,y),im);draw.text((x+3,y+263),q['gear']+' '+q['state']+' '+str(q['frame']),font=font,fill='#c1d5d5')
 board.save(P/f'changed-heads-{start//16:02}.png')
views=[(g,d) for d in ['east','west','south'] for g in ['bare','helmet']];board=Image.new('RGB',(1000,60+len(views)*350),'#252b2e');draw=ImageDraw.Draw(board);draw.text((15,12),'KRUSHER / SAME NATIVE SCALE / ORIGINAL SUIT BODIES',font=font,fill='white')
for row,(g,d) in enumerate(views):
 q=next(q for q in qs if q['gear']==g and q['state']=='swim-'+d and q['frame']==2);images=[Image.open(R/q['previousSource'][6:]).convert('RGBA'),Image.open(P/q['output']).convert('RGBA')];alpha=np.array(images[0])[:,:,3]>0;alpha|=np.array(images[1])[:,:,3]>0;yy,xx=np.where(alpha);box=(max(0,int(xx.min())-8),max(0,int(yy.min())-8),min(256,int(xx.max())+9),min(276,int(yy.max())+9));y=60+row*350
 for col,im in enumerate(images):
  crop=im.crop(box);crop=crop.resize((crop.width*3,crop.height*3),Image.Resampling.NEAREST);x=col*500+(500-crop.width)//2;board.paste(crop,(x,y+35),crop);draw.text((col*500+20,y+4),g.upper()+' '+d.upper()+' / '+('PREVIOUS' if col==0 else 'REVISED'),font=font,fill='white')
board.save(P/'fit-comparison.png');print('Reviewed-board set updated:84changed drawings, six equal-scale before/after views.')
