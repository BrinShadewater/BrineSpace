"""Freeze a whole-source foreshortening correction; retain rejected raw01."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-loaded-swim-material-v1/sources'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'north-loop-01.request.json').read_text())
r['status']='Rejected whole-source camera projection: near-upright swimmers clip old-root canvas at one neutral scale. No native fixture run or normal selection.'
(S/'north-loop-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
prompt=(S/'north-loop-01.prompt.txt').read_text()+'''
CRITICAL WHOLE-SHEET CORRECTION: Reference5 is the rejected whole sheet to reauthor, NOT an accepted camera. Its swimmers project nearly as tall as standing and resemble people walking with raised arms. Correct this by actually rotating the physical adult body into a horizontal prone swim posture, moving AWAY into the image depth. The game camera views this body at about35 degrees above the water plane, not nearly overhead; torso and thighs shorten naturally in projection, crown and shoulders partly occlude upper back, and knees fold in depth. Each projected swimmer should occupy about90-100 units top-to-bottom and75-85 units across bent elbows relative to the unchanged146-unit standing neutral. Standing stays exactly the original physical adult. Head size stays21-22 units; do NOT shrink the whole swimmer, enlarge standing neutral or squash a flat upright sprite. Preserve organic volume and articulated anatomy under camera foreshortening. Reference3 shows the intended foreshortened water-plane pose and projected extent. Four kick phases must remain distinct. Keep forward-held case beyond the head/shoulders, proper rear armor unchanged. Redraw all four whole connected swimmers consistently; leave no elongated upright swimmer in the sheet.'''
p=S/'north-loop-02.prompt.txt';p.write_text(prompt,encoding='utf-8')
r={k:v for k,v in r.items() if k not in ['rawSha256','generationId','originalGeneratedPath']}
r.update(status='frozen before whole-source correction',promptSha256=sha(p))
r['orderedReferences'].append({'path':(S/'north-loop-01.raw.png').relative_to(ROOT).as_posix(),'sha256':sha(S/'north-loop-01.raw.png')})
(S/'north-loop-02.request.json').write_text(json.dumps(r,indent=2)+'\n')
print('Rejected raw01 retained; whole North02 foreshortening request frozen.')
