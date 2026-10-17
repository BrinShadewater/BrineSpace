from pathlib import Path
import json,hashlib,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
package=json.loads((P/'turn-head-v3-package-evidence.json').read_bytes());guard=json.loads((P/'package-turn-head-v3-validation.json').read_bytes())
assert package['failures']==0 and guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
frozen=json.loads((P/'east-turn-join-inputs.json').read_bytes());changed=[p for p,h in frozen.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert set(changed)<= {'scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json'},changed
files=['turn-head-prompt-v2.txt','turn-head-prompt-v3.txt','turn-head-generated-v2.png','turn-head-generated-v3.png','turn-head-only-target.png','turn-head-only-masters.png','turn-head-only-anchor.png','package-turn-head-v3.gd','turn-head-v3-package-evidence.json']+[r['candidate'] for r in package['records']]
report={'selected':False,'sourceSlotsReviewed':6,'fullBodyBoardsReviewed':2,'pixelChecks':package['checks'],'failures':0,'profileUnchanged':True,'changedPriorInputs':changed,'generationSources':['exec-7bcd7f19-18a7-49a3-885e-5330f100c0ad.png','exec-a8e2e108-7559-4adf-9bfb-ff14e9dd0aca.png'],'hashes':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in files},'nativePlayerAcceptance':False,'normalLoaderAdmission':False,'sharedAliasCoverage':False,'fullGoalComplete':False}
(P/'turn-head-v3-review-evidence.json').write_text(json.dumps(report,indent=2))
section=f'''## James six compact turn-head source candidates — October 2, 2026

`character/james-side-motion-review-2026-10-02` retains two more built-in attempts.
Second wider collar sheet still had halo and oversized goggles, unselected.
Third head-only target with three directional masters/revised East anchor returns
six cleaner distinct yaw sources,1629x965. Prompt/raw/target/provenance retained.
Native Godot explicitly extracts270x288 rectangles, clears generated alpha dust
below32/255, fits25x29 head/neck cutouts into original sources. No whole-body
replacement. First fixed128xwindow left old hair; widened fixed window removed
some fragments but heads still sat too far forward in turning poses. Final per-pose
head placement follows original head front/neck locations: x130,127,124,128,124,123,
y74; windows retained individually in turn-head-v3-package-evidence.json.
Rectangles include collar and possible backpack pixels, not semantic head masks.

All six full-body candidates and enlarged head/collar details reviewed in two
comparisons beside revised East carry and original turn. Compact cranial size and
distinct yaw are improved; reviewed final windows remove old cranial fragments.
Native packaging{package['checks']}outside-window RGBA checks0fail, engine0,
no timeout, strict scratch whole owner profile unchanged. These are packaging
invariants, not motion/gameplay tests. Prior changed inputs: {changed!r}; source
changes from this authoring stay confined to new candidates. No selected raster,
normal-loader, turn manifest, clock, pivot, body/crate/boot change from this work.

Lesson: narrow source to the actual authored feature when collar/body context
repeatedly induces haze or redesign. Uniform screen-space head placement is wrong
through yaw: follow each original neck/front anchor and the full old silhouette.
Check original versus candidate in full body before inferring success from pixel
protection. Keep rejected attempts and recorded extraction/alpha policy.
Six candidates remain UNSELECTED. Next prove exact shared quarter/half-turn and
reverse aliases, propagate coherent heads, then full paired turn/source-clock
native scale review and actual task/Continue. Master/cargo-head join, untouched
directional endpoints, West hand-edge cleanup and full cross-family polish remain
open. Full James objective active/incomplete; no owner acceptance/commit/export.
'''
def atomic(path,data):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data);assert path.read_bytes()==old;os.replace(tmp,path)
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old=path.read_bytes();assert section.splitlines()[0].encode() not in old
    atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
path=P/'HEAD_CANDIDATE_HANDOFF.md';atomic(path,path.read_bytes()+b'\n\n'+section.encode())
print(json.dumps({'candidateSlots':6,'pixelChecks':package['checks'],'failures':0,'guidesUpdated':5,'selected':False,'changedPriorInputs':changed}))
