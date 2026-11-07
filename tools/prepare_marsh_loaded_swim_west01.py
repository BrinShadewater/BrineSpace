"""Freeze own-West body/case/motion authorities before whole-source generation."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';S=B/'sources';S.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for state in json.loads(p.read_text())['states']:selected[state['id']]=(p,state)
motion=selected['swim-carry-west'];frames=[resolve(motion[0],n) for n in motion[1]['frameFiles']]
board=Image.new('RGB',(224*len(frames),232),'#293b40');d=ImageDraw.Draw(board)
for i,p in enumerate(frames):
    im=Image.open(p).convert('RGBA');board.paste(im,(224*i,24),im);d.text((224*i+4,4),'MOTION ONLY '+str(i),fill='white')
guide=S/'west-selected-motion-only.png';board.save(guide)
refs=[ROOT/'character/marsh-cargo-held-material-v1/sources/west-body-primary.png',ROOT/'character/marsh-cargo-held-material-v1/sources/west-cargo-endpoint.png',guide,ROOT/'character/marsh-motion-polish-v1/sources/west-standing-identity-01.png']
prompt='''Create a production sprite atlas on genuine transparent background, five separate COMPLETE figures in one horizontal row with wide transparent separation and no text, labels, grid, background, shadows or bubbles. Four loaded swimmers plus one standing neutral scale ruler, all same camera and physical adult.
Reference roles: FIRST is PRIMARY whole-West body/face/proportions/quiet matte material authority. SECOND is rigid carry-case hardware/size authority only. THIRD is older swim MOTION ONLY: do not copy its bulky anatomy, head size or old case design. FOURTH is original West directional identity, secondary detail. Own WEST facing LEFT throughout; near LEFT temple is BARE, the RIGHT temple implant is far side and must NOT appear on visible left temple. Never mirror East artwork.
Match the fitted slim adult android botanist in the first reference: muted off-white ivory and greyed sage fabric, restrained dark outlines, sandy short hair, small adult head, narrow torso/waist, compact joints, no bulky spacesuit, added seams, packs or equipment helmet. Head dimensions remain the SAME across all swimming figures and standing neutral. Against standing height147 units, neutral complete profile width about31 units and adult head height about21-22 units. Do not enlarge head/shoulder pads to make swimming readable; preserve full adult trunk and legs, not miniature swimmer or giant face. Quiet matte grade, no glossy gold/yellow ivory or saturated hair.
Cells1-4: swimming horizontally LEFT, head/upper chest gently lifted, same slightly overhead side camera as game sources, BOTH bent arms and connected hands secure the SAME small rigid dark rectangular case close in front of upper chest. Case has inset sidepanel and ONE ivory latch at its LEFT edge; no handle, no second edge latch, no front-view divided panel. Approximately34wide x23high relative to147standing adult, same rigid dimensions all poses; never independently enlarge the case. Both articulated near/far legs and separate boots visible.
Four genuinely distinct successive propulsion phases: 1 near leg extended and far knee folded; 2 near knee beginning to fold while far leg begins extending, both partially bent; 3 near knee folded and far leg extended; 4 near leg beginning extension while far knee starts folding, intermediate angles distinct from2. Make asymmetrical near/far motion readable, correct knees/boots, no duplicated pose, no disconnected fingers/limbs, no extra legs. Body and case maintain the same scale/density/materials through each kick.
Cell5: SAME adult upright neutral West profile facingLEFT, both feet flat, arms relaxed and empty hands, exact fitted slim proportions of reference1. This is the common scale ruler for ALL five complete figures; do not scale it separately or widen it. One complete figure strictly inside each cell, no clipped boots or case, no overlap. Newly author whole connected figures organically, no pasted smaller heads, cut-and-paste limbs, mirror, per-pose anatomy scaling or independently fitted prop. Transparent empty space between all five bodies.'''
p=S/'west-loop-01.prompt.txt';p.write_text(prompt,encoding='utf-8')
r={'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(p),'orderedReferences':[ref(q) for q in refs],'sourceFrames':[ref(q) for q in frames]+[ref(ROOT/'character/marsh-v2/frames/bare/idle-west/000.png'),ref(ROOT/'character/marsh-west-carry-material-v1/candidate-03/000.png')],'selectedMotionManifest':ref(motion[0]),'selectedMotionState':motion[1],'catalogue':ref(cat),'rules':'Whole figures, common own-West neutral147 ruler, no mirror/patch/recolour/opaque clipping or per-part/per-pose fit. Source proportions/grade and linked joins require review.'}
(S/'west-loop-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
print('Own-West whole-source request and selected six-slot motion frozen; near LEFT temple bare.')
