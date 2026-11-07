"""Prepare six whole-figure run repairs against matching physical master references."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-run-master-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((R/'character/bill-east-interact-master-consistency-v1/native/corrected-source-audit.json').read_text(encoding='utf-8'));state=audit['selected']['bare']['run-east']
idle=R/'character/bill-east-idle-master-motion-v1/frames/idle-east/000.png';reference=Image.new('RGBA',(256,256));reference.alpha_composite(Image.open(idle).convert('RGBA'),(36,52));reference.resize((1024,1024),Image.Resampling.NEAREST).save(D/'idle-reference.png')
master=R/'character/bill-east-walk-master-pilot-v1/original-master.png'
protected={p:sha(R/p) for p in [state['manifest']]+state['files']}
for slot,source in enumerate(state['files']):
 S=D/f'pose-{slot:03}';S.mkdir();p=R/source
 Image.open(p).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(S/'edit-target.png')
 refs=[dict(path=str(path),sha256=sha(path),source=str(src),sourceSha256=sha(src),role=role) for path,src,role in [(S/'edit-target.png',p,'Exact running pose, placement, build and limb silhouette'),(D/'idle-reference.png',idle,'Current idle: warm face, matte suit detail and consistent identity'),(master,master,'Original Bill master identity and worn material construction')]]
 prompt=f'''Edit image1 ONLY: one complete East-facing running Bill, phase {slot} of six. Repair visual identity and material detail to match images2 and3, while preserving the exact running pose and physical registration of image1. Keep the same forward body lean, head placement/size, spine, narrow build, arm swing, shoulder/elbow connection, hand count, knee bend, boot positions, near/far limb order and entire silhouette. Do not stand him up, change stride, crop, scale, move or redesign the figure. All references use the same1024square physical canvas, fixed foot pivot(512,896); retain image1 silhouette and pose height rather than imposing upright idle height. Restore the master's worn matte charcoal-grey quilted padded suit: fine diamond stitching, modest seams, harness straps, red muted shoulder insignia and chest patch, belt pouches, silver kneepad/boot/strap hardware, glove anatomy. Match current idle's warm readable skin, angular brown-haired bearded face and medium brown hair. Suit should match the current idle midtones, not image1's near-black flattened fabric. Keep small worn diffuse highlights, no glossy sheen, bright silver suit, airbrushed smoothing or comic simplification. Render a single coherent whole person including the correctly joined neck/collar/shoulders and anatomically connected swinging arms, never a pasted face or isolated components. Transparent RGBA background, no shadow, halo, checkerboard, blur, text, montage, extra limb or equipment. East-facing profile, existing camera and hand orientation exactly. Change only master consistency and suit/face detail, preserving all pose geometry.'''
 (S/'prompt.txt').write_text(prompt,encoding='utf-8');(S/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8')
(D/'protected-inputs.json').write_text(json.dumps(protected,indent=2)+'\n',encoding='utf-8');(D/'selected-contract.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
print('Six source-preserving East run edit targets and exact master references prepared.')
