from pathlib import Path
import json,hashlib,subprocess,sys,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'candidate-v7'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
package=list((D/'frames').rglob('*.png'))+[D/'bare-manifest.json',D/'helmet-manifest.json',D/'registration.json',D/'paired-turn-contact.png']
before={str(p):sha(p) for p in package};assert len(before)==16
subprocess.run([sys.executable,str(P/'build_candidate.py')],check=True,capture_output=True)
assert before=={str(p):sha(p) for p in package},'Non-deterministic local package rebuild'
native=D/'native-review-evidence.json';e=json.loads(native.read_text(encoding='utf-8'))
assert e['validation']['passed'] and e['sourceNativePairs']==104 and e['decodedNativeSamplesExact']==104
e.update(visualReview='All4chronologicalboards/104source-native pairs viewed; complete12pairedsource/contact and6enlarged shared helmet views reviewed. Compact West head/case reach and asymmetric hip equipment improved; held endpoint uses exact corrected whole frame. Static sampled source/registration review accepted for continued candidate work.',
         continuousNativeMotionReviewed=False,normalAdoption=False,deterministicPackageFiles=16)
native.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
source=P/'v7-study/review-evidence.json';s=json.loads(source.read_text(encoding='utf-8'))
s['visualReview']='All6whole figures and head/grip/equipment details viewed; scanner/cylinder handedness consistent, leftwardorder/plantedfeet retained, Westheadproxy28. Whole held endpoint alias in paired candidate; source-only review not runtime acceptance.'
source.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
heading='## Veld paired South–West master turn candidate — October 2, 2026'
block=heading+'''

Unselected character/veld-cargo-turns-master-family-v1/candidate-v7 repairs
complete bare turn proportions/case reach/equipment continuity. V5 fixes3but
stillwrong2; V6 narrow thirdfigure repair keeps cyan scanner on near hip;
V7 authored whole-source case/head repair retains correct leftward order,
single148ruler and planted adjacent feet. Westhead proxy28 (originalmaster27,
correctedheld28), other projections23/24/28/29/29. No per-pose anatomy scaling.

Paired12exports/4finite quarterstates reuse existing shared angular helmet
sources/recipe and exact South shell; whole corrected Westheld bare/equipped
frames reused at endpoint. Original800ms/reverse metadata exact. Source32checks,
paired22checks and16deterministic package files unchanged on local rebuild.
Standalone actualCrewSpritePlayer649native checks0fail/8.4s/104samples, both
directions/gears, terminal holds/sourcepixels/47/93/148rulers.107targetedinputs
and2931owner non-logfiles unchanged/scratchAPPDATA;engine0/cleanlog.

All4chronologicalboards/104source-native pairs and12pairedsource/6enlargedhelmet
views inspected.104native RGB samples/866ms previews losslessly checked; viewer
resets/terminal hold do not change800msfinite runtime. No full continuous-motion,
natural cadence/controller/world/ownership/Continue/normal acceptance claim.
First8.13s/second8.35s baseline-fixture4fail intervals preserved: equipment
library needs allbarequarters plus append=true; source/metadata unchanged.

Lesson: repair a stubborn atlas semantic mistake narrowly by explicit ordinal
figure/visible edge; inspect every angle again. Shared helmet library validation
requires corresponding appended bare coverage; baseline failures are separate
from candidate fidelity. Keep whole canonical endpoints rather than anatomy
strips, and review incoming full pose before adoption. Next independent
North–West, shared halfturn joins and actual cargo controller/room handoffs;
remaining family/library master polish still required. Full Veld goal active.
Review/HANDOFF: character/veld-cargo-turns-master-family-v1.

'''
refs=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for p in refs:
    original=p.read_bytes();text=original.decode('utf-8')
    if heading in text:continue
    tmp=p.with_name(p.name+'.veld-turn-candidate.tmp');tmp.write_text(block+text,encoding='utf-8')
    assert p.read_bytes()==original,'Concurrent change: inspect before retrying '+str(p)
    tmp.replace(p)
review='''
## Later paired candidate milestone
V5/V6 fix scanner continuity; V7 whole authored case/head repair yields West
proxy28 and coherent smaller head/body/case compared with master. Six graded
source/detail views,12paired whole figures,6enlarged shared helmet views and all
4native chronologicalboards/104source-native presentations reviewed. Candidate
source/sample review accepted for continued work; prior V4 failure remains
historical. Exact corrected whole Westheld frame endpoint aliases, original
South shared shell, pre-existing angular helmet recipe, protected body pixels.
32source/22pair checks,16deterministicfiles,649nativechecks0fail8.4s,104exact native
RGB decode bindings.107inputs/2931owner non-logfiles unchanged/scratchAPPDATA.
First two4fail comparison-fixture runs retained (baseline needs full appended
barequartercoverage). No normal selection or continuous/allworld motion proof.
Next North–West authoredturn and halfturn/shared endpoint/controller/room cargo
handoffs, then wider master polish. Current candidate remains unselected.
'''
p=P/'SOURCE_REVIEW.md';old=p.read_text(encoding='utf-8')
if '## Later paired candidate milestone' not in old:p.write_text(old+review,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld paired cargo turns

## Objective and acceptance
Complete full Veld set matching masters/proportions/matte grade, then full
library consistency/polish. Preserve anatomical/equipment/helmet/case joins
and actual room/controller/save lifecycle before normal admission.

## Accepted decisions and constraints
Authored complete figures, one148ruler, planted adjacent feet, original800ms
finite/reverse timing; no mirrored equipment or procedural anatomy strips.
Existing shared helmet engineering/recipe and whole canonical endpoints.

## Current state
Seven raws/prompts/refs/execution records preserved. V5/6 equipment fix andV7
case/head repair supersede failedV4source gate. candidate-v7 contains12paired
exports/4quarterstates, registration, source/helmet/native boards/APNG/HTML.
Corrected whole Westheld pair reused exactly; candidate remains unselected.
New paired Godot fixture/UID and isolated runner in tests/tools. No normal
selection or production controller/room/owner geometry changes.

## Verification
32source/22pairchecks;16deterministicfiles stable.649nativechecks0fail8.4s/
104standalone player captures at30Hz prescribed times, all6slots/terminal/both
directions/gears.107targetedinputs/2931owner non-logfiles unchanged,scratchAPPDATA.
All4chronologicalboards/104source-native pairs and12pairedsource/6helmet detail
views inspected.104exactRGB decode bindings;866msviewer includes finalhold/reset,
runtime800msfinite. No full continuousnative/naturalcadence/world/owner claim.
First8.13s/second8.35s4baselinefail intervals preserved; baseline fullbarelibrary
with append=true corrected, no candidateart/timing changes.

## Next action
Independent North–West whole-body repair matching Westheld/master, consistent
angular/equipment/helmet joins. Reconcile shared South/North/East endpoints,
halfturns, actual Veld cargo controller/room/caseownership/Continue before normal
selection. Full-library master polish still open; full goal active/incomplete.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
url='http://127.0.0.1:8791/character/veld-cargo-turns-master-family-v1/candidate-v7/?v=paired-master-v7'
response=urllib.request.urlopen(url,timeout=5);assert response.read()==(D/'index.html').read_bytes()
print('16deterministicpackagefiles/5maintainedrefs/HANDOFF recorded; previewHTTP200 exactbytes. Fullgoalactive/unselected.')
