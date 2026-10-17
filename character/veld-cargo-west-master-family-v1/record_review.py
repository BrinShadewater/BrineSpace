from pathlib import Path
import json,hashlib,subprocess,sys
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-cargo-west-master-family-v1'
e=json.loads((P/'native-review-evidence.json').read_text(encoding='utf-8'))
for relative,digest in e['bindings'].items():assert hashlib.sha256((R/relative).read_bytes()).hexdigest()==digest,relative
e['reviewedBoards']=e['boards'];e['reviewedSourceNativePairs']=72
e['encodedNativeFrameGroups']={name:Image.open(P/name).n_frames for name in e['movies']}
e['visualReview']='All4chronological boards/all72native source presentations inspected. Corrected compact heads, connected shoulders/hips/case grip and rigid shared helmet tilt retained in these finite player samples. Clean authored prop remains fixed after release; selected idle body reused beneath it. Staged player/material review accepted. Turn source proportions and actual world/controller/prop ownership/save joins remain unverified; no continuously watched allclip or final owner acceptance claim.'
(P/'native-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
extraction=json.loads((P/'unload-extraction.json').read_text(encoding='utf-8'))
extraction['visualReview']='All6generated whole bodies, ungraded source comparisons, clean released case and final12paired source presentations inspected. Compact held head28px vs carry27–28/master27; bending envelopes30–31px retain projected collar/head tilt, not per-pose height normalization. First contact landmark initially included case; body boot-side exclusion fixes20pxfalse alignment. Raw idle case touches boot/body; packaged terminal uses exact selected body instead.'
(P/'unload-extraction.json').write_text(json.dumps(extraction,indent=2)+'\n',encoding='utf-8')
paths=list((P/'frames').rglob('*.png'))+[P/'bare-manifest.json',P/'helmet-manifest.json',P/'family-registration.json',P/'paired-unload-contact.png']
before={x.relative_to(P).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
with (P/'rebuild.log').open('w',encoding='utf-8') as log:subprocess.run([sys.executable,str(P/'build.py')],stdout=log,stderr=subprocess.STDOUT,check=True)
after={x.relative_to(P).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in paths};assert before==after
(P/'rebuild-checks.json').write_text(json.dumps({'deterministicFiles':len(paths),'before':before,'after':after,'failures':0,'providerCalls':0},indent=2)+'\n',encoding='utf-8')
block='''## Veld West unload/pickup master family candidate — October 2, 2026

New independently edited six-pose whole unload source/prompt/refs/raw/execution
retained at character/veld-cargo-west-master-family-v1. Shared148ruler, physical
boot registration, corrected compact head28px held (carry27–28/master27proxy),
natural30–31pxbending head/collar envelopes. Same fixed carry material recipe,
unchanged native44x46West helmet with rigid0/12/18/16/8degree bending tilt.12new
exports; pickup exact reverse source aliases; carry references reviewedcandidate
unchanged. Paired3states/36slots retain original840mscarry and520msfinite actions.
74packagechecks0fail;16packagefiles stable on local rebuild/no provider calls.

Native standalone actual CrewSpritePlayer finite-clock passes453checks0fail/7.78s,
72presentations (18/action/gear),all6slots/terminal holds at47/93/148standingrulers.
56targeted inputs/2931owner non-log files unchanged under scratchAPPDATA. All four
chronological boards/all72source-native presentations reviewed. LosslessAPNG
coalesces identical holds: all72original nativeRGBsamples and600mshold durations
verified against decoded groups. Preview repeats are viewer resets; runtime finite.
No normal loader/controller/world/prop ownership/Continue/natural cadence proof.

Contact lesson: hand/case may connect to body alpha at floor contact, so a connected
component is not a boot landmark. Boot-side contact exclusion fixes false20pxshift.
Old selected final-case crop includes occluding boot pixels; now isolate the clean
unobstructed authored case from raw release pose, one global source scale. Prop
fixed at75/196afterrelease3/4/5, rendered foreground over exact selected idle body;
visible idle pixels outside prop remain exact. Preserve occlusion when checking
source equality; do not claim transparent crop background is prop artwork.

First fixture copied carry-kind expectation and failed72checks; originals correctly
declare unload metadata even for derived pickup. Fixed fixture only, preserved
first-kind-check interval, same art/timing and owner/inputs unchanged in both runs.
Initial APNG18-frame expectation failed because identical holds coalesce; retained
firstpreview and corrected decoded duration/group mapping without pixel changes.

Source/player review accepted as staged evidence. Turn endpoint/intermediate bare
heads remain larger; actual cargo controller/room/foot/case handoffs still open.
Keep full-family sources unselected until those pass; broader directional source,
natural gameplay and library polish objective remains active/incomplete. No export/
commit. Handoff/index.html/native-review-evidence.json in candidate folder.

'''
for dest in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=dest.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:dest.write_text(block+old,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld West master cargo family

## Objective and acceptance
Full master-consistent Veld set, then library polish. Repair West carry/action/turn
proportions together, preserving anatomy, matte colours, helmet, timing and joins.

## Accepted decisions and constraints
Original West master governs compact proportions; authored whole-body sources,
single148ruler and one fixed carry colour recipe. Original840/520mstiming retained.
Pickup reuses reversed unload sources; selected idle anatomy reused at terminal.
No normal binding until source/native/controller/room/case joins establish fidelity.

## Current state
raw-unload-v1.png/prompt/refs/execution retained. extract_unload.py makes six bodies
and clean unobstructed case; build.py creates12exports and paired3-state family,
36slots: reviewedcarry refs plus unload and exactreverse pickup. Shared native
helmet rigid tilts0/12/18/16/8. Source/package/native review pages and evidence saved.
No selected image/production code/room/owner layout changes. Candidate unselected.

## Verification
74packagechecks0fail;16deterministic files stable. Native test/UID/runner453checks
0fail/7.78s/72finite presentations,all6slots/terminal/47/93/148rulers.56inputs and
2931ownerfiles unchanged,scratchAPPDATA. All4boards/72source-native presentations
viewed;72nativeRGB samples and600mspreview durations checked against coalescedAPNG
holds. Repeating preview resets viewer, not runtime action. No allclips continuous
watch/world/controller/case ownership/save/final owner acceptance claim.
Firstfixture72kind failures preserved in first-kind-check output; originals use
unload metadata for both actions, corrected fixture only. FirstAPNG18frame assumption
failed on identical holds; firstpreview retained, decoded hold mapping corrected.
Foot registration initially captured connected case; corrected boot-side landmark.
Old final crop had boot occlusion: pure authored rawcase now foreground at75/196;
exact idle outside prop, source unchanged under it. Avoid spurious extra boot pixels.

## Next action
Review/update original-master West held/turn endpoints and angular intermediates;
old bare turn heads still broader. Reconcile source aliases so facing/holding joins
match correctedcarry/actions, then actual normal Veld cargo controller/room/foot/
neck/case handoffs and interrupted/save/ownership lifecycle before adoption.
Current stage player proofs do not establish natural gameplay. East/Southcarry,
older side sit/read and full current library/natural gameplay polish remain open.
No active native job, no commit/export/full-goal completion.
''',encoding='utf-8')
prior=R/'character/veld-carry-west-master-proportions-v1/HANDOFF.md'
old=prior.read_text(encoding='utf-8');note='''\n## Neighboring action source milestone\nWest unload/pickup now repaired and paired-player reviewed in\ncharacter/veld-cargo-west-master-family-v1 (453checks/72nativepresentations).\nPrior missing action correction step superseded by that staged evidence. Turn\nproportions and actual full-family controller/room/case joins still pending.\n'''
if '## Neighboring action source milestone' not in old:prior.write_text(old+note,encoding='utf-8')
print('Native72review/source/diagnostics recorded;16rebuild files stable;five references updated')
