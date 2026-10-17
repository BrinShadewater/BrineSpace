from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];base=R/'character/chief-engineer-branforth-v2';catalog=json.loads((base/'catalog.json').read_text());retained={}
for rel in catalog['body']:
 file=base/rel;m=json.loads(file.read_text())
 for s in m['states']:
  if s['id'].startswith(('death-ground-','death-water-')):retained[s['id']]=dict(state=s,pack={k:v for k,v in m.items() if k!='states'},folder=file.parent.relative_to(R).as_posix())
(P/'retained-contracts.json').write_text(json.dumps(retained,indent=2)+'\n')
air=P.parent/'james-air-family-v1';endpoints=json.loads((air/'endpoint-sources.json').read_text());records={}
for d in ['east','south','west','north']:
 folder=P.parent/('james-death-'+d+'-v1');folder.mkdir(exist_ok=True)
 for action in ['idle','swim']:
  im=Image.open(air/'endpoints/bare'/(action+'-'+d+'.png')).convert('RGBA');im=im.crop(im.getbbox());im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(folder/(action+'-master-reference.png'));records[d+'-'+action]=endpoints['bare-'+action+'-'+d]
 board=Image.new('RGB',(1536,640),'#303b40');draw=ImageDraw.Draw(board)
 for row,action in enumerate(['death-ground','death-water']):
  record=retained[action+'-'+d];pack=record['pack'];draw.text((8,row*320+8),action+' '+d+' retained geometry only',fill='white')
  for i,rel in enumerate(record['state']['frameFiles']):
   im=Image.open(R/record['folder']/rel).convert('RGBA');pos=(i*256+round(128-pack['pivot'][0]),row*320+round(220-pack['pivot'][1]));board.paste(im,pos,im)
 board.save(folder/'retained-motion-reference.png')
(P/'reference-sources.json').write_text(json.dumps(records,indent=2)+'\n')
print([(key,s['state']['frameDurationsMs'],s['state']['loop'],s['state']['waterPoses']) for key,s in retained.items()])
