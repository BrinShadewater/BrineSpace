from pathlib import Path
import json,hashlib,shutil
from PIL import Image
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={};records=[];preserved=decoded=0
for kind,bank,state,endpoint,count in [('entry','bill-land-water-west-v15','land-swim-west',0,7),('exit','bill-water-exit-west-master-v13','swim-land-west',7,8)]:
 for gear in ['bare','helmet']:
  prior=ROOT/f'character/{bank}/{gear}';mp=prior/'manifest.json';inputs[mp.relative_to(ROOT).as_posix()]=sha(mp);m=json.loads(mp.read_text());s=m['states'][0];assert len(s['frameFiles'])==count and sum(s['frameDurationsMs'])==500 and not s['loop'];assert [m['frameWidth'],m['frameHeight']]==[352,320] and m['pivot']==[160,224]
  dest=OUT/f'staged-{kind}/{gear}';frames=[]
  for n in range(count):
   src=prior/f'frames/{state}/{n:03}.png';inputs[src.relative_to(ROOT).as_posix()]=sha(src);chosen=OUT/f'{gear}-neutral-candidate.png' if n==endpoint else src;inputs[chosen.relative_to(ROOT).as_posix()]=sha(chosen);dst=dest/f'frames/{state}/{n:03}.png';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(chosen,dst);im=Image.open(dst).convert('RGBA');assert im.size==(352,320)
   if n!=endpoint:assert im.tobytes()==Image.open(src).convert('RGBA').tobytes();preserved+=1
   frames.append(im)
  m['name']='Bill West revised neutral '+kind+' source candidate';m['status']='source_candidate_unselected';s['provenance']='Original calibrated interiors retained exactly; shared neutral endpoint authored with builtin imagegen in active gait water auditV2. Native/contact/identity acceptance pending.';(dest/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
  frames[0].save(dest/'source-preview.png',save_all=True,append_images=frames[1:],duration=s['frameDurationsMs'],loop=1,disposal=0,blend=0)
  with Image.open(dest/'source-preview.png') as ap:
   assert ap.n_frames==count and ap.info['loop']==1
   for n,im in enumerate(frames):ap.seek(n);assert ap.convert('RGBA').tobytes()==im.tobytes() and ap.info['duration']==s['frameDurationsMs'][n];decoded+=1
  records.append({'kind':kind,'gear':gear,'frames':count,'totalMs':500,'revisedEndpoint':endpoint,'manifest':(dest/'manifest.json').relative_to(OUT).as_posix(),'normalAdmission':False})
assert inputs=={n:sha(ROOT/n) for n in inputs};report={'banks':records,'preservedOriginalFramesExact':preserved,'decodedAPNGFramesExact':decoded,'inputSHA256':inputs,'nativeAcceptance':False,'normalAdmission':False};(OUT/'staged-sequences-assessment.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'banks':len(records),'preserved':preserved,'decoded':decoded,'frozenInputs':len(inputs)}))
