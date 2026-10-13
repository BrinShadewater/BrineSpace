"""Retain correct opposite thigh posture; boot support/crate joins remain open."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-east-carry-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
gid='exec-1661ff9f-b710-4f30-ae90-3b6dc30c659a';original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(gid+'.png');raw=S/'contact-03.raw.png';shutil.copy2(original,raw)
p=S/'contact-03.request.json';r=json.loads(p.read_text());assert sha(S/'contact-03.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
r.update(generationId=gid,originalGeneratedPath=str(original),rawSha256=sha(raw),status='Retained unselected: foreground thigh correctly backward/left, boot contact projection and crate variant remain provisional');p.write_text(json.dumps(r,indent=2)+'\n')
source=(ROOT/'tools/build_marsh_north_passing03.py').read_text().replace('marsh-north-run-material-v1','marsh-east-carry-material-v1').replace('passing-03','contact-03').replace('right-passing.png','far-contact.png').replace("req['orderedReferences'] + [req['poseSourceFrame']]","req['orderedReferences'] + req['sourceFrames']").replace('scale = 146/','scale = 147/').replace("'neutralOccupiedTargetHeight':146","'neutralOccupiedTargetHeight':147")
source=source.replace('Selected North idle','Selected East idle').replace('Raw right leg supports and left sole raised. Arms remain asymmetrical like contact reference, left knee/sole lift stronger than requested. Packed body/grade and phase joins pending.','Foreground near thigh correctly goes backward LEFT, darker far thigh forward RIGHT. Far front boot angled and projects above rear near boot; supporting sole not certified. Crate single-latch broad recessed panel differs from source01 rounded box; cannot assume cross-half consistency. Whole body/grade/crate/contact joins pending.')
exec(compile(source,str(ROOT/'tools/build_marsh_east_carry_contact03.py'),'exec'),{'__file__':str(ROOT/'tools/build_marsh_east_carry_contact03.py'),'__name__':'__main__'})
