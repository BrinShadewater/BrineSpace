from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parents[2];N=R/'output/veld-east-grounded-source-v1'
data=json.loads((N/'records.json').read_text(encoding='utf-8'));checks=0;boards=[]
for gear in ['bare','helmet']:
 rows=[r for r in data['records'] if r['gear']==gear];assert len(rows)==142
 frames=[Image.open(N/(r['name']+'-native.png')).convert('RGBA') for r in rows]
 durations=[r['durationMs'] for r in rows]
 path=P/f'{gear}-native-full-source.png'
 frames[0].save(path,save_all=True,append_images=frames[1:],duration=durations,loop=1,disposal=0,blend=0)
 replay=Image.open(path);assert replay.n_frames==142
 for i,im in enumerate(frames):
  replay.seek(i);assert np.array_equal(np.array(replay.convert('RGBA')),np.array(im));checks+=1
  assert round(replay.info['duration'])==durations[i];checks+=1
 for start in range(0,142,48):
  board=Image.new('RGB',(990,1520),(32,43,49));d=ImageDraw.Draw(board)
  for j,im in enumerate(frames[start:start+48]):
   xy=((j%6)*165,(j//6)*190);crop=im.crop((145,395,310,570)).convert('RGB')
   board.paste(crop,(xy[0],xy[1]+15));d.text((xy[0]+3,xy[1]+1),f'{gear} raw{start+j}',fill='white')
  dest=P/f'native-{gear}-chronology-{start//48:02}.png';board.save(dest);boards.append(dest.name)
before=json.loads((N/'inputs-after.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((R/name).read_bytes()).hexdigest()==sha for name,sha in before.items())
report={'checks':checks,'failures':0,'frameCountPerGear':142,'durationMs':sum(durations),'nativeInputsStillStable':len(before),'chronologyBoards':boards,'scope':'Exact complete native paired replay at source durations; no world movement/contact, selected loop, final identity/alpha or normal controller acceptance. Native148px chronology crops have fixed bounds; whole images retain all47/93/148 presentations.'}
(P/'native-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
