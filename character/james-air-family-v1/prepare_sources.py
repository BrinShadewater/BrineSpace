from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];base=R/'character/chief-engineer-branforth-v2'
catalog=json.loads((base/'catalog.json').read_text());retained={}
for rel in catalog['body']:
 file=base/rel;m=json.loads(file.read_text())
 for state in m['states']:
  if state['id'].startswith(('swim-distress-','recover-air-')):retained[state['id']]=dict(state=state,pack={k:v for k,v in m.items() if k!='states'},folder=file.parent.relative_to(R).as_posix())
(P/'retained-contracts.json').write_text(json.dumps(retained,indent=2)+'\n')
for d in ['east','south','west','north']:
 folder=P.parent/('james-air-'+d+'-v1');folder.mkdir(exist_ok=True)
 shutil.copy2(P.parent/('james-water-'+d+'-v1')/'standing-master-reference.png',folder/'standing-master-reference.png')
 water=P.parent/('james-water-'+d+'-v1');m=json.loads((water/'bare-manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='tread-'+d)
 image=Image.open(water/s['frameFiles'][0]).convert('RGBA');crop=image.crop(image.getbbox());crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST).save(folder/'tread-master-reference.png')
 board=Image.new('RGB',(1536,600),'#303b40');draw=ImageDraw.Draw(board)
 for row,action in enumerate(['swim-distress','recover-air']):
  record=retained[action+'-'+d];pack=record['pack'];draw.text((8,row*300+8),action+' '+d+' retained geometry and timing only',fill='white')
  for i,rel in enumerate(record['state']['frameFiles']):
   im=Image.open(R/record['folder']/rel).convert('RGBA');pos=(i*256+int(128-pack['pivot'][0]),row*300+int(220-pack['pivot'][1]));board.paste(im,pos,im)
 board.save(folder/'retained-motion-reference.png')
print([(k,len(v['state']['frameFiles']),v['state']['frameDurationsMs'],v['state']['loop'],v['pack']['pivot'],v['state'].get('waterKinds')) for k,v in retained.items()])
