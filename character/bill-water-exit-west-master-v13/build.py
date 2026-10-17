"""Bind calibrated swimming Extend to the six calibrated exit interiors and current idle context."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent;PREV=R/'bill-water-exit-west-master-v12';SWIM=R/'bill-swim-west-calibrated-v1'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=[Path(__file__),PREV/'build.py',PREV/'review.json',SWIM/'build.py',SWIM/'review.json',R/'crew-side-masters-v1/bill-side-master-01.png']+[PREV/g/'manifest.json' for g in ['bare','helmet']]+[SWIM/g/'manifest.json' for g in ['bare','helmet']]+[PREV/g/f'frames/swim-land-west/{i:03}.png' for g in ['bare','helmet'] for i in range(8)]+[SWIM/g/'frames/swim-west/000.png' for g in ['bare','helmet']]
inputs += [PREV/f for f in ['master-comparison.png','prior-comparison.png','neck-review.png']]
before={f.relative_to(R).as_posix():sha(f) for f in inputs};banks={};preserved=0;decoded=0
for g in ['bare','helmet']:
 m=json.loads((PREV/g/'manifest.json').read_text(encoding='utf-8'));sm=json.loads((SWIM/g/'manifest.json').read_text(encoding='utf-8'))
 for k in ['frameWidth','frameHeight','pivot','standingHeight']:assert m[k]==sm[k]
 old=[Image.open(PREV/g/f'frames/swim-land-west/{i:03}.png').convert('RGBA') for i in range(8)];new=Image.open(SWIM/g/'frames/swim-west/000.png').convert('RGBA');bank=[new]+old[1:];files=[]
 for i,im in enumerate(bank):
  if i>0:assert im.tobytes()==old[i].tobytes();preserved+=1
  f=P/g/f'frames/swim-land-west/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P/g).as_posix())
 assert bank[0].tobytes()==new.tobytes();m['name']='Bill West calibrated swim-to-standing comparison';m['status']='source_candidate_unselected';s=m['states'][0];s['frameFiles']=files;s['provenance']='Calibrated swim Extend0 exact; six calibrated exit interiors and current configured idle endpoint exact fromV12. Full motion/contact/grade/native admission pending.'
 assert s['frameDurationsMs']==[60,40,50,60,70,80,80,60] and len(s['facings'])==8 and s['loop'] is False
 (P/g/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');dur=s['frameDurationsMs'];bank[0].save(P/g/'source-leave.png',save_all=True,append_images=bank[1:],duration=dur,loop=1,disposal=0,blend=0)
 with Image.open(P/g/'source-leave.png') as ap:
  assert ap.n_frames==8 and ap.info['loop']==1
  for i,im in enumerate(bank):ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==dur[i];decoded+=1
 banks[g]=bank
names=['Swimming','Lower hands','Low elbow','Palm push','Knee tuck','Half kneel','Rise','Standing'];board=Image.new('RGB',(2816,720),'#182932');d=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
 for i,im in enumerate(banks[g]):board.paste(im,(i*352,row*360+25),im);d.text((i*352+4,row*360+4),g+' / '+names[i],fill='white')
board.save(P/'full-exit-review.png')
# The fully preserved interior comparison and source-fit closeups remain available in V12.
import shutil
for f in ['master-comparison.png','prior-comparison.png','neck-review.png']:shutil.copy2(PREV/f,P/f)
html=(PREV/'index.html').read_text(encoding='utf-8').replace('Six interior poses now use shared standing calibrations against the original master. The bare standing endpoint matches the current idle source. Swimming, grade and contact joins still need review.','Revised swim-to-standing sequence, bare and helmeted. The swimming pose now matches the corrected body scale. Shoulder, footing and color joins remain under review.')
(P/'index.html').write_text(html,encoding='utf-8')
assert before=={f.relative_to(R).as_posix():sha(f) for f in inputs}
review={'inputSHA256':before,'frozenInputsStable':len(before),'priorCompletePosesExact':preserved,'swimEndpointsExact':2,'decodedAPNGFramesExact':decoded,'durationsMs':dur,'totalMs':sum(dur),'loop':1,'canvas':[352,320],'pivot':[160,224],'standingHeight':148,'normalSelected':False,'nativeAcceptance':False,'scope':'Current calibrated source join, not native loaded/control/contact/grade acceptance.'}
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8');print(json.dumps({'frozenInputs':len(before),'priorPosesExact':preserved,'swimEndpointsExact':2,'APNGFramesExact':decoded}))
