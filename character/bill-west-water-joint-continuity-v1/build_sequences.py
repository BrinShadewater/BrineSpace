from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={};records=[];preserved=decoded=0
selection=json.loads((OUT/'source-selection.json').read_text(encoding='utf-8'))
for kind,pose,state,index in [('entry','ready','land-swim-west',1),('exit','rise','swim-land-west',6)]:
 for gear in ['bare','helmet']:
  prior=ROOT/f'character/bill-west-active-gait-water-audit-v2/staged-{kind}/{gear}'
  mp=prior/'manifest.json';inputs[mp.relative_to(ROOT).as_posix()]=sha(mp)
  m=json.loads(mp.read_text(encoding='utf-8'));s=m['states'][0]
  assert m['pivot']==[160,224] and m['standingHeight']==148 and sum(s['frameDurationsMs'])==500 and not s['loop']
  dest=OUT/f'staged-{kind}/{gear}';frames=[];original=[]
  for n,name in enumerate(s['frameFiles']):
   src=prior/name;inputs[src.relative_to(ROOT).as_posix()]=sha(src)
   replaced=n==index and f'{gear}-{pose}' in selection['provisional']
   chosen=OUT/f'{gear}-{pose}-candidate.png' if replaced else src
   inputs[chosen.relative_to(ROOT).as_posix()]=sha(chosen)
   dst=dest/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(chosen,dst)
   im=Image.open(dst).convert('RGBA');assert im.size==(352,320)
   old=Image.open(src).convert('RGBA');original.append(old);frames.append(im)
   if not replaced: assert im.tobytes()==old.tobytes();preserved+=1
  m['name']='Bill West whole-source joint continuity '+kind+' candidate';m['status']='source_candidate_unselected'
  s['provenance']='Joint continuity builtin imagegen source candidate. Shared neutral from auditV2 and all other interiors exact. Physical contact, motion and native acceptance pending.'
  (dest/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
  frames[0].save(dest/'source-preview.png',save_all=True,append_images=frames[1:],duration=s['frameDurationsMs'],loop=1,disposal=0,blend=0)
  with Image.open(dest/'source-preview.png') as ap:
   assert ap.n_frames==len(frames) and ap.info['loop']==1
   for n,im in enumerate(frames):ap.seek(n);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==s['frameDurationsMs'][n];decoded+=1
  board=Image.new('RGB',(len(frames)*360,730),(31,35,40));draw=ImageDraw.Draw(board)
  for n,(old,new) in enumerate(zip(original,frames)):
   for row,im in enumerate([old,new]):
    x=n*360;draw.text((x+5,row*365+5),f'{gear} {kind} {n:03} '+('prior' if row==0 else 'candidate'),fill='white')
    board.paste(im,(x+4,row*365+30),im)
  board.save(OUT/f'{gear}-{kind}-sequence-review.png')
  records.append({'kind':kind,'gear':gear,'revisedFrame':index if f'{gear}-{pose}' in selection['provisional'] else None,'frames':len(frames),'totalMs':500,'normalAdmission':False})
assert inputs=={n:sha(ROOT/n) for n in inputs}
(OUT/'staged-sequences-assessment.json').write_text(json.dumps({'banks':records,'preservedPriorFramesExact':preserved,'decodedAPNGFramesExact':decoded,'inputSHA256':inputs,'nativeAcceptance':False,'normalAdmission':False},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'banks':len(records),'preserved':preserved,'decoded':decoded,'frozenInputs':len(inputs)}))
