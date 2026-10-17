from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
OUT=HERE/(sys.argv[1] if len(sys.argv)>1 else 'height-audit-v1');OUT.mkdir(exist_ok=True)
def read_master(mode,direction):
 folder=ROOT/'character'/('crew-runtime-matte-v1/branforth' if mode=='bare' else 'james-shared-helmet-runtime-v1')
 m=json.loads((folder/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='idle-'+direction)
 im=Image.open(folder/s['frameFiles'][0]).convert('RGBA');canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(128-int(m['pivot'][0]),224-int(m['pivot'][1])));return canvas,(folder/s['frameFiles'][0]).relative_to(ROOT).as_posix()
def measure(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>180);return dict(crownY=int(y.min()),lowestOpaqueY=int(y.max()),heightPx=int(y.max()-y.min()+1),threshold=180)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
board=Image.new('RGB',(1680,990),'#303b40');d=ImageDraw.Draw(board)
d.text((16,12),'James height comparison — same authored scale, common foot pivot; no per-frame resizing',font=font,fill='white')
report=dict(method='Alpha >180 bounds, exact PNGs at standingHeight148, masters translated by pivot difference only',masters={},turns={},runtimeChanged=False)
for row,mode in enumerate(['bare','helmet']):
 east,ep=read_master(mode,'east');north,npth=read_master(mode,'north');turns=[Image.open(HERE/f'frames/{mode}/carry-turn-east-north/{i:03}.png').convert('RGBA') for i in range(6)]
 report['masters'][mode]={'east':dict(source=ep,**measure(east)),'north':dict(source=npth,**measure(north))};report['turns'][mode]=[dict(pose=i,**measure(im)) for i,im in enumerate(turns)]
 images=[east]+turns+[north];labels=['EAST MASTER']+['Turn '+str(i) for i in range(6)]+['NORTH MASTER'];top=65+row*420
 for col,(im,name) in enumerate(zip(images,labels)):
  x=col*210;crop=im.crop((76,55,181,232)).resize((210,354),Image.Resampling.BILINEAR);board.paste(crop,(x,top+45),crop);metrics=measure(im)
  d.text((x+8,top),mode+' / '+name,font=small,fill='white');d.text((x+8,top+22),str(metrics['heightPx'])+'px | top '+str(metrics['crownY']),font=small,fill='#c7d7df')
  floor=top+45+(223-55)*2;d.line((x,floor,x+209,floor),fill='#829ba7',width=1)
  cy=top+45+(metrics['crownY']-55)*2;d.line((x+78,cy,x+140,cy),fill='#ecce83',width=2)
  guide=76 if mode=='bare' else (68 if col<4 else 74);gy=top+45+(guide-55)*2
  for dx in range(0,210,10):d.line((x+dx,gy,x+dx+4,gy),fill='#668995')
d.text((16,915),'Solid gold: measured crown. Dashed: master crown (bare76; helmet east68 / north74). Ground guide: y223.',font=small,fill='white')
d.text((16,941),'Bare turn147-148px versus148px masters. Equipped crown68-74 follows east/north master fit.',font=small,fill='white')
d.text((16,963),'Bounds describe silhouette height; matching body landmarks still needs visual review. Artwork unchanged.',font=small,fill='white')
board.save(OUT/'comparison.png')
frames=[]
for i in range(6):
 panel=Image.new('RGB',(1000,750),'#303b40');dr=ImageDraw.Draw(panel)
 for row,mode in enumerate(['bare','helmet']):
  east,_=read_master(mode,'east');north,_=read_master(mode,'north');turn=Image.open(HERE/f'frames/{mode}/carry-turn-east-north/{i:03}.png').convert('RGBA')
  for j,(im,name) in enumerate([(east,'EAST MASTER'),(turn,'TURN '+str(i)),(north,'NORTH MASTER')]):
   x=70+j*330;y=row*365+38;crop=im.crop((76,55,181,232)).resize((189,319),Image.Resampling.BILINEAR);panel.paste(crop,(x,y),crop);dr.text((x,y-28),mode+' '+name+' / '+str(measure(im)['heightPx'])+'px',font=small,fill='white');dr.line((x,y+302,x+188,y+302),fill='#829ba7')
 frames.append(panel)
frames[0].save(OUT/'comparison.gif',save_all=True,append_images=frames[1:],duration=[400,250,250,250,250,600],loop=0)
(OUT/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
(OUT/'index.html').write_text('<style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>James corrected turn height comparison</h1><p>Exact selected standing masters, aligned by foot pivot. Comparison does not change artwork.</p><img src="comparison.gif"><img src="comparison.png"><p>Current bounds and source paths are recorded in measurements.json.</p>')
print('Height audit:2 modes,6 turn poses,4 masters; comparison images and metrics saved')
