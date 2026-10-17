from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];p.mkdir(exist_ok=True)
sources={'master':r/'character/branforth-west-direct-v2/master-input.png','cargo':r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png','selection':r/'character/branforth-west-direct-v2/selection.json','ledger':r/'character/branforth-west-direct-v2/generation.json','idleManifest':r/'character/crew-runtime-matte-v1/branforth/manifest.json'}
Image.open(sources['master']).save(p/'master-input.png')
Image.open(sources['cargo']).resize((1024,1024),Image.Resampling.LANCZOS).save(p/'case-pose-reference.png')
m=json.loads(sources['idleManifest'].read_bytes());s=next(s for s in m['states'] if s['id']=='idle-west');idle=sources['idleManifest'].parent/s['frameFiles'][0];sources['idle']=idle
registered=Image.new('RGBA',(256,256));registered.alpha_composite(Image.open(idle).convert('RGBA'),(128-round(m['pivot'][0]),224-round(m['pivot'][1])))
registered.resize((1024,1024),Image.Resampling.LANCZOS).save(p/'matte-idle-reference.png')
prompt='''Edit IMAGE 1, the original high-resolution WEST James master, into ONE standing CARRYING pose. Image 1 is the sole anatomy/face/identity/equipment authority. Preserve its exact full-body framing, crown and sole positions, total height, head-to-body ratio, face angle, small mature grey-haired head, horseshoe moustache, forehead goggles, torso/backpack, planted boots and legs. Do NOT enlarge his head, widen cheeks, change haircut/goggles or copy another reference's face. Keep his anatomical-left diagnostic meter on the near belt and his right-hip wrench on the far side, never in his hands. Keep full original square canvas and margins. Feet remain at exactly the original standing positions; no stride or stepping.

Only raise both forearms naturally from the master standing pose to hold one small horizontal dark grey equipment case in front at waist level, like IMAGE 2. Image 2 is ONLY case/hand-placement reference; its head/face/body proportions must NOT be copied. Case is compact, two-handed, horizontal, dark graphite with subdued worn silver fittings, no coloured markings. Preserve master shoulder/backpack shape while elbows bend and hands grip case. No clipping through chest, wrist, belt or case. No wrench/tablet/torch in his hands during carrying.

IMAGE 3 specifies the accepted subdued MATTE runtime material: neutral graphite quilted fabric, restrained grey-brown hair, muted engineering ochre-yellow patches, natural warm skin and worn neutral silver fittings. Retain image 1's fine painted illustrated detail and recognisable grey gear emblems. No purple/magenta cast, orange skin, glossy shine, bright exposure, expanded black shadows or blur. Genuinely TRANSPARENT background replacing green, with clean antialiased silhouette and real grey/silver retained; no green residue, halo, checkerboard, shadow, text or backdrop. One complete full-body sprite only. Match original master geometry and scale throughout; change only arm/hand carrying pose, case insertion and subdued runtime finish.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
ledger=json.loads(sources['ledger'].read_bytes());assert ledger['imageSha256']==hashlib.sha256(sources['master'].read_bytes()).hexdigest()
selection=json.loads(sources['selection'].read_bytes());assert selection['status']=='owner_approved_installed'
inventory={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sources.values()}
for n in ['master-input.png','case-pose-reference.png','matte-idle-reference.png','prompt.txt']:inventory[(p/n).relative_to(r).as_posix()]=hashlib.sha256((p/n).read_bytes()).hexdigest()
(p/'inputs.json').write_text(json.dumps({'preCallSha256':inventory,'selected':False,'lineage':'Original direct West2 input hash matches terminal provider ledger; adjacent selection records owner approval for resulting walk revision. This is shape/identity reference lineage, not exact generated-source or current portrait acceptance. Department yellow supersedes historical orange.'},indent=2)+'\n',encoding='utf-8')
print('Original West input hash verified against ledger; owner-approved walk record inspected; master/case/matte references and prompt frozen.')
