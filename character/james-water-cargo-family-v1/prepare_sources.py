from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw,ImageOps
P=Path(__file__).resolve().parent;R=P.parents[1];base=R/'character/chief-engineer-branforth-v2';catalog=json.loads((base/'catalog.json').read_bytes());states={}
for rel in catalog['body']:
 mf=base/rel;m=json.loads(mf.read_bytes())
 for s in m['states']:
  if s['id'].startswith(('swim-carry','swim-pickup','salvage')):states[s['id']]={'state':s,'pack':{k:v for k,v in m.items() if k!='states'},'manifest':mf.relative_to(R).as_posix()}
(P/'retained-contracts.json').write_text(json.dumps(states,indent=2)+'\n')
for d in ['east','south','west','north']:
 p=P.parent/('james-water-cargo-'+d+'-v1');p.mkdir(exist_ok=True);water=P.parent/('james-water-'+d+'-v1');shutil.copyfile(water/'standing-master-reference.png',p/'standing-master-reference.png')
 for mode in ['bare','helmet']:
  m=json.loads((water/(mode+'-manifest.json')).read_bytes());records=[];board=Image.new('RGBA',(1536,828))
  for col,action in enumerate(['tread','swim']):
   s=next(s for s in m['states'] if s['id']==action+'-'+d);f=water/s['frameFiles'][0];im=Image.open(f).convert('RGBA');board.alpha_composite(im.resize((768,828),Image.Resampling.NEAREST),(col*768,0));records.append(dict(action=action,file=f.relative_to(R).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
  board.save(p/(mode+'-water-reference.png'));(p/(mode+'-water-reference.json')).write_text(json.dumps(records,indent=2)+'\n')
 board=Image.new('RGB',(1536,936),'#303b40');dr=ImageDraw.Draw(board)
 for row,action in enumerate(['salvage','swim-pickup','swim-carry']):
  s=states[action+'-'+d];root=(R/s['manifest']).parent
  for i,rel in enumerate(s['state']['frameFiles']):
   im=Image.open(root/rel).convert('RGBA');gray=ImageOps.grayscale(im).convert('RGBA');gray.putalpha(im.getchannel('A'));pos=(i*256+round(128-s['pack']['pivot'][0]),row*312+35+round(128-s['pack']['pivot'][1]));board.paste(gray,pos,gray);dr.text((i*256+5,row*312+7),action+' '+d+' geometry only '+str(i),fill='white')
 board.save(p/'geometry-guide.png')
print('Four directional master/water/cargo geometry references; retained cargo, pickup, salvage and turn contracts preserved')
