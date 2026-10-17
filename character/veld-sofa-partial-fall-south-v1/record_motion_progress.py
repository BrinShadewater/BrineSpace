from pathlib import Path
import json,hashlib,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1]
path=P/'motion-review-evidence.json';d=json.loads(path.read_text(encoding='utf-8'))
for name,digest in d['bindings'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,name
reviewed=[f'{gear}-sit-pose{pose}-motion-contact-sheet.png' for gear in ['bare','helmet'] for pose in range(6)]
assert all(name in d['boards'] for name in reviewed)
d['reviewedBoards']=reviewed;d['reviewedNativePresentations']=588
d['visualReview']='All12sit boards/588native30fpspresentations inspected. Both gear versions/all6partial sit entrances retain sampled body/material/shared-shell/contact through finite collapse. Remaining12rise boards/588presentations and continuous playback assessment pending; normal admission pending.'
path.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
url='http://127.0.0.1:8791/character/veld-sofa-partial-fall-south-v1/motion-review.html?v=lossless-partial-v1'
with urllib.request.urlopen(url,timeout=10) as response:
    assert response.status==200 and response.read()==(P/'motion-review.html').read_bytes()
block='''## Veld partial South native motion capture — October 2, 2026

Paired staged actual world mortality30fpsrun passes5111checks0fail/289.05s/
engine0/cleanlog. All24partial sit/rise cases49presentations each:1176source-native
pairs.84targeted inputs/2931owner non-log files unchanged with scratch APPDATA.
24lossless APNG/contact sheets preserve every source/native PNG.2400decoded
checks0fail:1176room crops exact RGB,48intervals1600ms perpreview,800msviewer
terminalhold. Repeating preview resets viewer, not authored finite death.

All12sit boards/both gears/all6entrances/588native presentations inspected:
body/material/shared-shell/contact retained through sampled finite sequence.
Remaining12rise boards/588presentations and continuous playback assessment pending;
no normal partial admission or final motion acceptance. Source/ordinary Continue
evidence remains separate; normal reader/bunk/North paths unchanged.

Current furniture scope clarified from code and prior side-context evidence:
lounge sit is North; observation read is South. Earlier staged East/West sitting/
breathing exists; default side eligibility is absent. Generic South life_sit is a
future compatibility branch; actual South dispatch uses observation stages.
Do not add furniture or fabricate stages merely to admit source art. This does
not waive full directional source/master polish. Static inventory is not dispatch.

Next finish remaining reverse-context motion review, guarded paired normal
selection and relevant normal-world continuation; continue current eligible
family/context gaps and complete cross-library master/perspective/material polish.
Full goal active/incomplete. Review:character/veld-sofa-partial-fall-south-v1/
motion-review.html. Scope:character/veld-animation-coverage-audit-v1/CONTEXT_SCOPE.md.
No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=path.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:path.write_text(block+old,encoding='utf-8')
handoff=P/'HANDOFF.md';old=handoff.read_text(encoding='utf-8')
old+='''
## Native motion terminal — supersedes running notes above
Session83958 completed:5111checks0fail/1176nativecaptures/289.05s/engine0;
84targeted inputs and2931owner files unchanged. No live native process. Generator
session35656 and decoded checker66810 also terminal engine0;2400checks0fail,
24losslessAPNGs/1176exact native room crops. GET200/exact reviewHTML verified;
open_in_codex queued, no claim of visible browser/playback review.
Only all12sit contact sheets/588nativepresentations reviewed this turn; evidence
lists them. Next view bare-rise-pose0..5 and helmet-rise-pose0..5 motion sheets,
then actual playback assessment; do not mark unviewed rise sequences reviewed.
Normal partial admission remains absent. Existing actual default seats are North
sit and South observationread; no invented side furniture/genericSouthlife stage.
Full directional source polish still required. Current scope note in coverage audit.
'''
handoff.write_text(old,encoding='utf-8')
print('Recorded1176nativeframes/2400losslesschecks,12reviewedboards; remaining12explicit')
