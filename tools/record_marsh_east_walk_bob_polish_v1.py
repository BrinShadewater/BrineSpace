"""Record bounded bob/source/native review; keep tested inputs immutable."""
from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-east-walk-bob-contact-v1'
SOURCE=ROOT/'character/marsh-east-walk-bob-polish-v1'
RUN=ROOT/'output/marsh-animation-audit/east-walk-bob-world-v1-2026-10-03'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
vpath=OUT/'world-review/verification.json';v=json.loads(vpath.read_text())
assert (v['checks'],v['failures'],v['inputsStable'],v['ownerNonLogStable'])==(1653,0,5419,2931)
for b in v['boards']:
    assert sha(ROOT/b['path'])==b['sha256'];b['reviewed']=True
v['visualReview']='All eight complete928wide source/native boards and first full1600x900native actually inspected; body/detail/face grade improved at station scale. Held samples, not continuous cadence acceptance.'
vpath.write_text(json.dumps(v,indent=2)+'\n')
frozen=json.loads((RUN/'inputs-after.json').read_text())
assert all(sha(ROOT/p)==h for p,h in frozen.items())
bounds=[]
for i in range(6):
    a=np.asarray(Image.open(OUT/f'{i:03}.png').convert('RGBA'))[:,:,3]>=128
    bounds.append(Image.fromarray(a.astype('uint8')*255).getbbox())
receipt={'normalAdmission':False,'fullGoalComplete':False,'sourceReviewSha256':sha(SOURCE/'review.json'),'nativeVerificationSha256':sha(vpath),'allTestedInputHashesStillExact':len(frozen),'registeredOpaqueBounds':bounds,'crowns':[b[1] for b in bounds],'visualFindings':['Three complete raw whole-pose figures, native family/joins board and2xhead board inspected.','Original first-half bob recovered toward original geometry; phase5 face darker and more consistent. Registered crowns24,23,22,24,22,22; original23,22,21,23,22,21. Small asymmetry/residual remains.','Phase1 sole1pixel high corrected with wholeRGBA Y+1/no visible loss. All six same-root source sole depths pass actual normal actor/main/grid routes.','Earlier enlarged colored edge samples all alpha1/255, not evidence of opaque fringe. Raw alpha preserved; no threshold cleanup.'],'reviewedSourceBoards':[{'path':(SOURCE/n).relative_to(ROOT).as_posix(),'sha256':sha(SOURCE/n)} for n in ['family-joins-native.png','heads-2x.png']],'browser':{'url':'http://127.0.0.1:8764/marsh-east-walk-bob-contact-v1/motion-review.html','htmlSha256':sha(OUT/'motion-review.html'),'screenshotSha256':sha(OUT/'browser-quarter.png'),'observations':['normal phase0clock83draw6','quarter phase5clock6276draw384','screenshot quarter phase3clock8682draw961','quarter phase4clock10538draw1406','paused phase2clock12126draw1798'],'scope':'Sampled advancing browser and controls; no continuously watched full-loop cadence acceptance.'},'next':'Resolve remaining bob symmetry/head grade against idle/start/stop; continuously reviewed cadence and broader natural/save/full-set checks remain.'}
(OUT/'acceptance-review.json').write_text(json.dumps(receipt,indent=2)+'\n')
note='''

## Marsh East walking bob/face polish — October 3, 2026

Three built-in whole-pose edits (1/2/5) separate original selected gait geometry
from registered detail/grade and ownidle facial authority. Raw requests, reference
hashes and immediate copies retained in character/marsh-east-walk-bob-polish-v1.
Three raw figures, complete1104x1498family/idle/master/start/stop/run board and
exact2xhead board inspected. First-half head rise restored toward original;
phase5 face grade closer to neighboring phases. No anatomy splice/pose fitting,
recolour or alpha cleanup. Enlarged saturated fringe samples all alpha1/255;
do not mistake an inspection display for opaque edge contamination.

Phase1 sole1px high after whole184/1254resampling, corrected by proved fullRGBA
Y+1/no alpha loss in character/marsh-east-walk-bob-contact-v1. Five other sources
byte-exact. Registered crowns[24,23,22,24,22,22], original[23,22,21,23,22,21];
small asymmetry remains. All six native same-root sole depths pass. Entire bank
PROVISIONAL/UNSELECTED; normal228states/1190slots/89body manifests unchanged.

Actual normal controller/main/grid staged instance, prescribed96/112East dry
routes:1653checks/0failures,270movement samples,43source/native pairs,3moving
actor restores.5419bounded inputs/2931owner non-log files unchanged in scratch
APPDATA,engine0,no errors/warnings; terminal session89595. All eight complete
928wide boards and first full1600x900native inspected. Full sources retained.
Native depth/contact proof remains bounded; no complete2D planted-foot, natural
jobs, paid building, other rooms/rotations or fullSave/TitleContinue acceptance.
Browser exact tested family at native/station density, sampled normal/quarter
advancement and pause; saved screenshot. Not continuous watched cadence.

Lesson: give original gait geometry and matched material separate authority;
after every whole-pose edit remeasure both crown and sole, then reverify native
contact. A bob repair can lose a support pixel. Lossless registration moves crown
too, so retain explicit residuals and compare both half-cycles before admission.
Next remaining bob/head/idle/start/stop seam and continuous cadence review, then
broader full-library natural/save polish. Full goal remains active and incomplete.
Handoff:docs/MARSH_EAST_WALK_BOB_POLISH_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('Provisional source/native/browser evidence recorded;5419existing tested hashes exact; four append-only notes/skill mirror updated.')
