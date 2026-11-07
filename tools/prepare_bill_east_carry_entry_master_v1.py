from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-carry-entry-master-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'character/bill-carry-start-east-v4/bare-manifest.json';m=json.loads(old.read_text());s=m['states'][0]
pickup=R/'character/bill-east-cargo-handoffs-master-v1/frames/pickup-east/010.png';carry=R/'character/bill-east-carry-master-v1/frames/000.png';master=R/'character/bill-east-walk-master-pilot-v1/original-master.png'
protected={p.relative_to(R).as_posix():sha(p) for p in [old,pickup,carry,master]}
for slot in range(6):
 src=R/s['frameFiles'][slot].replace('res://','');protected[src.relative_to(R).as_posix()]=sha(src)
 if slot not in [1,2,3]:continue
 P=D/f'pose-{slot:03}';P.mkdir()
 refs=[]
 for name,p,role in [('edit-target',src,'Exact whole first-step pose'),('pickup-reference',pickup,'Current held-crate endpoint and identity'),('carry-reference',carry,'Current matte carry identity')]:
  out=P/(name+'.png');Image.open(p).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(out);refs.append({'path':str(out),'sha256':sha(out),'source':p.relative_to(R).as_posix(),'sourceSha256':sha(p),'role':role})
 refs.append({'path':str(master),'sha256':sha(master),'source':master.relative_to(R).as_posix(),'sourceSha256':sha(master),'role':'Original Bill identity'})
 prompt=f'''Edit image1 into one complete East-facing Bill first carry step, pose{slot}. Preserve image1 exact whole pose, foot locations and angles, height, slim build, stride/step, head angle, shoulder/elbow/wrist continuity, two hands and crate grip. Preserve its exact crate size, perspective, handle, latch and location. Images2/3/4 are identity and material references only, never substitute their stance. Match their detailed matte charcoal diamond quilted suit, muted red patches, belt/harness/pouches, worn stitching and subdued metal; warm readable bearded angular face, medium brown hair. No chest-grown sleeve, spare hand, bigger torso, head/helmet changes, gloss or dark face. Keep original planted floor and exact bounding scale/position. One whole figure and original crate, no parts/stamping. Transparent RGBA background, no shadow/halo/text/checkerboard. All pose references1024square pivot512,896 standingH592. Original pose geometry has priority; only restore matching material and identity.'''
 (P/'prompt.txt').write_text(prompt,encoding='utf-8');(P/'references.json').write_text(json.dumps(refs,indent=2)+'\n')
(D/'contract.json').write_text(json.dumps({'originalManifest':old.relative_to(R).as_posix(),'originalState':s,'pickup':pickup.relative_to(R).as_posix(),'carry':carry.relative_to(R).as_posix(),'protected':protected},indent=2)+'\n')
print('Three intermediate whole poses prepared; endpoints remain exact whole aliases')
