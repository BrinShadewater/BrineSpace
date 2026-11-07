"""Cargo-preserving airlock drainage poses, reproducible without generation."""
from pathlib import Path
import argparse,hashlib,json,shutil
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-cargo-drain-v1'
DIRECTIONS=['east','west','north','south']
CONFIG={
 'east':dict(scale=.27,edges=[0,710,1210,1690,2170],centers=[476,965,1390,1885],targets=[120,117,114,112],bottom=[178,176,172,172]),
 'west':dict(scale=.28,edges=[0,670,1200,1700,2172],centers=[258,882,1462,1955],targets=[104,107,110,112],bottom=[178,176,172,172]),
 'north':dict(scale=.27,edges=[0,543,1086,1629,2172],centers=[274,816,1354,1898],targets=[112]*4,bottom=[194,184,172,172]),
 'south':dict(scale=.265,edges=[0,542,1085,1628,2170],centers=[290,816,1350,1880],targets=[112]*4,bottom=[178,176,172,172]),
}
def build(install=False,direction='south'):
 cfg=CONFIG[direction];out=BASE/f'review/{direction}-01';out.mkdir(parents=True,exist_ok=True);poses=[];records=[];sources={}
 for i in range(4):
  name=f'{direction}-{"02" if direction=="north" and i>=2 else "01"}.png';p=BASE/'sources'/name
  sources[name]=hashlib.sha256(p.read_bytes()).hexdigest();raw=Image.open(p).convert('RGBA')
  left,right=cfg['edges'][i:i+2];tile=raw.crop((left,0,right,raw.height))
  labels,_=label(np.asarray(tile)[:,:,3]>=192);sizes=np.bincount(labels.ravel());sizes[0]=0
  tile.putalpha(Image.fromarray(((labels==sizes.argmax())*255).astype('uint8')))
  scale=cfg['scale'];dense=tile.resize((round(tile.width*scale),round(tile.height*scale)),Image.Resampling.BOX)
  dense.putalpha(dense.getchannel('A').point(lambda a:255 if a>=128 else 0))
  offset=(round(cfg['targets'][i]-(cfg['centers'][i]-left)*scale),cfg['bottom'][i]-dense.getbbox()[3])
  frame=Image.new('RGBA',(224,208));frame.alpha_composite(dense,offset);box=frame.getbbox()
  assert box and 0<box[0] and 0<box[1] and box[2]<224 and box[3]<208,(direction,i,box)
  poses.append(frame);records.append(dict(source=name,cell=[left,0,right,raw.height],scale=scale,center=cfg['centers'][i],target=cfg['targets'][i],bottom=cfg['bottom'][i],offset=offset))
 endpoints=[]
 for state in ['swim-carry','carry']:
  name=f'{state}-{direction}-endpoint.png';p=BASE/'sources'/name;sources[name]=hashlib.sha256(p.read_bytes()).hexdigest()
  frame=Image.new('RGBA',(224,208));frame.alpha_composite(Image.open(p).convert('RGBA'),(20,0) if state=='carry' else (0,0));endpoints.append(frame)
 row=[endpoints[0],*poses,endpoints[1]];key=f'cargo-drain-{direction}';files=[]
 for i,frame in enumerate(row):name=f'{key}-{i:03}.png';frame.save(out/name);files.append(name)
 state=dict(id=key,frameFiles=files,frameDurationsMs=[120,180,220,220,180,120],loop=False,facings=[direction]*6,waterKinds=['transition']*4+['carry']*2,waterPoses=[True]*4+[False]*2,depthOffsets=[0.0]*6)
 (out/'manifest.json').write_text(json.dumps(dict(frameWidth=224,frameHeight=208,pivot=[112,172],standingHeight=148,states=[state]),indent=2)+'\n')
 (out/'provenance.json').write_text(json.dumps(dict(sources=sources,registration=records,derived='Exact registered loaded/standing endpoints; four independently authored intermediates. North last two cells use corrected low grip source02.'),indent=2)+'\n')
 board=Image.new('RGB',(224*6,232),'#17212a')
 for i,f in enumerate(row):board.paste(f,(i*224,24),f)
 board.save(out/'contact.png');preview=[]
 for f in row:
  b=Image.new('RGB',(280,244),'#17212a');ImageDraw.Draw(b).text((8,6),key,fill='white');b.paste(f,(28,28),f);preview.append(b)
 preview[0].save(out/'motion.gif',save_all=True,append_images=preview[1:],duration=[500,180,220,220,180,700],loop=0)
 if install:
  runtime=ROOT/'character/marsh-v2';relative=f'supplemental/cargo-drain-{direction}';folder=runtime/relative;folder.mkdir(parents=True,exist_ok=True)
  for n in [*files,'manifest.json','provenance.json']:shutil.copyfile(out/n,folder/n)
  p=runtime/'catalog.json';catalog=json.loads(p.read_text())
  if relative+'/manifest.json' not in catalog['body']:catalog['body'].append(relative+'/manifest.json')
  p.write_text(json.dumps(catalog,indent=2)+'\n')
 return row
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--install',action='store_true');p.add_argument('--direction',choices=DIRECTIONS,default='south');a=p.parse_args();build(a.install,a.direction)
