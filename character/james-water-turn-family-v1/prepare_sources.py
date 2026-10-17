from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageOps
P=Path(__file__).resolve().parent;R=P.parents[1];base=R/'character/chief-engineer-branforth-v2';catalog=json.loads((base/'catalog.json').read_bytes());retained={}
for rel in catalog['body']:
 mf=base/rel;m=json.loads(mf.read_bytes())
 for s in m['states']:
  if s['id'].startswith('swim-turn-'):retained[s['id']]={'state':s,'pack':{k:v for k,v in m.items() if k!='states'},'manifest':mf.relative_to(R).as_posix()}
for a,b in [('east','south'),('south','west'),('west','north'),('north','east')]:
 pair=a+'-'+b;p=R/'character'/('james-water-turn-'+pair+'-v1');p.mkdir(exist_ok=True)
 for mode in ['bare','helmet']:
  board=Image.new('RGBA',(1536,828));records=[]
  for col,d in enumerate([a,b]):
   folder=R/'character'/('james-water-'+d+'-v1');m=json.loads((folder/(mode+'-manifest.json')).read_bytes());s=next(s for s in m['states'] if s['id']=='swim-'+d);file=folder/s['frameFiles'][0];im=Image.open(file).convert('RGBA');board.alpha_composite(im.resize((768,828),Image.Resampling.NEAREST),(col*768,0));records.append({'direction':d,'file':file.relative_to(R).as_posix(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'pivot':m['pivot'],'standingHeight':m['standingHeight']})
  board.save(p/(mode+'-endpoint-reference.png'));(p/(mode+'-endpoints.json')).write_text(json.dumps(records,indent=2)+'\n')
 old=retained['swim-turn-'+pair];mf=R/old['manifest'];board=Image.new('RGB',(1536,312),'#303b40');draw=ImageDraw.Draw(board)
 for i,rel in enumerate(old['state']['frameFiles']):
  im=Image.open(mf.parent/rel).convert('RGBA');alpha=im.getchannel('A');im=ImageOps.grayscale(im).convert('RGBA');im.putalpha(alpha);at=(i*256+round(128-old['pack']['pivot'][0]),26+round(128-old['pack']['pivot'][1]));board.paste(im,at,im);draw.text((i*256+8,5),pair+' geometry only '+str(i),fill='white')
 board.save(p/'geometry-guide.png');(p/'retained-contracts.json').write_text(json.dumps({k:v for k,v in retained.items() if k in ['swim-turn-'+pair,'swim-turn-'+b+'-'+a]},indent=2)+'\n')
(P/'retained-contracts.json').write_text(json.dumps(retained,indent=2)+'\n');print('Four paired exact-water endpoint references, independent quarter geometry guides,12 retained state contracts')
