from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-breathing-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed']
records=json.loads((O/'captures.json').read_text());evidence=[]
for rotation in range(4):
 board=Image.new('RGB',(1232,560),'#202a30');d=ImageDraw.Draw(board)
 for row,gear in enumerate(('bare','helmet')):
  frames=[]
  for slot in range(7):
   record=next(r for r in records if r['rotation']==rotation and r['gear']==gear and r['slot']==slot)
   point=[float(n) for n in re.findall(r'-?\d+(?:\.\d+)?',record['station']['rest_point'])]
   cx=454+point[0];cy=494+point[1]
   path=O/record['screenshot'];frame=Image.open(path).convert('RGB').crop((round(cx-44),round(cy-100),round(cx+44),round(cy+30))).resize((176,260),Image.Resampling.NEAREST)
   board.paste(frame,(slot*176,row*280+20));d.text((slot*176+3,row*280+3),f'{gear} {slot%6}',fill='white');frames.append(frame);evidence.append(path)
  frames[0].save(P/f'native-rotation-{rotation}-{gear}.gif',save_all=True,append_images=frames[1:],duration=600,loop=0)
 out=P/f'native-rotation-{rotation}.png';board.save(out);evidence.append(out)
evidence += [O/'captures.json',O/'native.log',O/'validation.json',O/'profile-before.json',O/'profile-after.json',O/'final.png',R/'tests/test_veld_seated_breathing.gd',R/'tests/test_veld_seated_breathing.gd.uid',R/'tools/run_veld_seated_breathing.py',P/'fit_breathing.py',P/'fitted-registration.json',P/'fitted-verification.json']
files={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in evidence}
(P/'native-evidence.json').write_text(json.dumps({'scope':'fixture-only held breathing, four configured actual lounge rotations, selected architect, paired gear,56 prescribed native slots/loop seams, pause/contact/depth; no natural entry/exit/interruptions/Continue/owner acceptance','normalSelection':False,'files':files},indent=2)+'\n')
print(json.dumps({'captures':len(records),'evidenceFiles':len(files),'runtimePassed':v['passed']}))
