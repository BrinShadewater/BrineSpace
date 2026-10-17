from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw,ImageOps
P=Path(__file__).resolve().parent;R=P.parents[1];base=R/'character/chief-engineer-branforth-v2';catalog=json.loads((base/'catalog.json').read_text());states={}
for rel in catalog['body']:
 folder=base/rel;pack=json.loads(folder.read_text())
 for state in pack['states']:states[state['id']]=(state,pack,folder.parent)
for d in ['east','south','west','north']:
 folder=R/'character'/('james-water-'+d+'-v1');folder.mkdir(exist_ok=True);shutil.copy2(R/'character'/('james-lying-'+d+'-v1')/'standing-master-reference.png',folder/'standing-master-reference.png')
 board=Image.new('RGB',(1536,936),'#303b40');draw=ImageDraw.Draw(board);contracts=[]
 for row,action in enumerate(['tread','swim','swim-start']):
  state,pack,root=states[action+'-'+d];contracts.append(dict(state=state,pack={k:v for k,v in pack.items() if k!='states'},folder=str(root.relative_to(R)).replace('\\','/')))
  for i,f in enumerate(state['frameFiles']):
   im=Image.open(root/f).convert('RGBA');a=ImageOps.grayscale(im).convert('RGBA');a.putalpha(im.getchannel('A'));at=(i*256+round(128-pack['pivot'][0]),row*312+36+round(128-pack['pivot'][1]));board.paste(a,at,a);draw.text((i*256+8,row*312+8),action+' '+d+' '+str(i)+' geometry only',fill='white')
 board.save(folder/'geometry-guide.png');(folder/'retained-contracts.json').write_text(json.dumps(contracts,indent=2)+'\n')
print('Four independent master/geometry references; 18 source poses per direction')
