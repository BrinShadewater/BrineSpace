"""Record full normal running checkpoints and current cross-facing review."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
MARKER='## Marsh South run05 normal selection and full visible Continue — October 2, 2026'
LESSON='''
## Marsh South run05 normal selection and full visible Continue — October 2, 2026

Normal ordered catalog now provisionally selects complete run-south candidate05:
../marsh-south-run-material-v1/candidate-05/manifest.json. Root selection.json
records current admission and verified checkpoint scope; historical source requests,
recipes and staged review flags retain original unselected provenance. No normal
Marsh/main/grid/player controller or save-schema edits. Existing six100ms loop,
0.11027027027027027cell distance stride,184canvas,p92/172,H148 retained. Revised
right passing and whole sole registration source/master scopes remain as preceding
05 milestone; normal admission is provisional, not owner/full motion acceptance.

Independent exact normal factory/catalog/main/grid/player test, no injected
manifest/subclass or custom gait hook:226checks/8full RunSave checkpoints/8fresh
actual visible TitleContinues/16native-source captures/8exact source-root pairs.
Idlebefore,sixphaseholds,normal slowingwalk; whole actor/player/source/root parity,
restoredpause and continued run route/distance phase after unpause. Actual full
actor.update drives this interval (preceding staged study used normal move).
Normal costs/failures, prescribed clear168world furnishedColdStore route and
pausedworld/peers. Startup and actual enabled transmissionContinue awaited before
press and overlay removal/capture. Reset run_save_path to scratch after loading.
124bounded source/controller/Save/Title inputs stable;2931owner non-log files
unchanged scratchAPPDATA.0fail/engine0/exit0; audit
south-run-normal-native-v1-2026-10-02 terminal. Earlier staged444checks scoped
to its own05interval; not reused as fullSave evidence.

New tests/test_marsh_south_run_production.gd and pairedUIDcp6shrunb2v83 registered
companions/native900s, classifier confirmed. tests/index.json metadata added after
launch, outside124input interval. Publisher verifies selected run-south manifest
and normal source pixels rather than old West catalog-tail assumption; copied
publisher's initial stale assertion fixed without any native/test/runtime change.
All8pairs on two boards inspected: complete actor unobscured, original/continued
held source and root match; warm ivory/sage/slate/charcoal remain. Held material/
head/torso joins improved, moving articulated contacts and entire family provisional.

Fresh selected four-facing run/idle source board inspected at commonH148metadata
and whole pivot registration, no artwork scaling. Sourceboard is current74body
manifests/228selectedstates/1190slots; counts only coverage. Old73manifest whole
inventory retains its historical source SHA scope, not overwritten to claim new
run05 review. East/West head/upperbody joins need own idle/master comparisons;
wide side running silhouettes include leg spread and are not width defects alone.
North exposed raised heel/sole remains legitimate charcoal, distinct from ivory
boot guards. Do not whiten soles or force profile widths equal front/rear.

Next East run refs frozen character/marsh-east-run-material-v1/sources:
four selected idle/gait and six existing run complete figures, frameSHAs/current
metadata. Guides whole-translated to256/p128224 and nearest2x with no clip;
not a runtime canvas change. Selected East idle32x147 actual occupied, metadata
H148; current run six100msloop. Primaryidle/gait board, motion-onlyrun board and
original own East standing master inspected. Old run carries broader head/upper
body and running lean; compare own anatomical head/collar/equipment density,
not total spread bbox. No East generation/request/candidate/native work yet.

Review:character/marsh-south-run-material-v1/normal-review-v1/index.html.
No realtimefilm/browser continuous review, natural routing/traffic, helmet joins,
moving articulated contact or full-family acceptance inferred from checkpoints.
Normal South sources remain provisional within full objective. Next author complete
East running cycle+neutral at selected147occupied anatomy/material scale using old
poses ONLY as motion guide, preserve actual cadence; then source/native/fullsave
evidence. West/North run/carry and68unreviewed boards in dated held pass remain,
followed by full-set consistency/contact/head/proportion/grade polish.
Full Marsh objective remains active/incomplete.
'''
def main():
    assessment={'allEightPairsInspected':True,'allFacingRunBoardsInspected':True,'pairedBoards':['paired-0.png','paired-1.png'],'normalAdmission':True,'fullGoalComplete':False,'nativeAppearance':'Complete unobscured whole actor in all8before/continued cases; source/root matching, warm ivory/sage/slate and charcoal upper/sole distinction preserved.','familyFindings':'Current selected run four facings held comparison reviewed. East/West own head/torso/master-density comparisons next; natural side leg spread is not by itself drift. North raised dark soles legitimate.','limits':'Native full normal checkpoint/TitleContinue/controller scope only; no realtimefilm, moving articulated contact, helmet or all-family art acceptance.'}
    out=BASE/'normal-review-v1';(out/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_south_run_normal.py'),run_name='__main__')
    evidence=json.loads((out/'verification.json').read_text());assert evidence['checks']==226 and evidence['nativeVisualReview'] and evidence['familyVisualReview']
    selection_path=BASE/'selection.json';selection=json.loads(selection_path.read_text());selection.update(status='provisional normal run05 selection; eight full visible checkpoint Continues verified',normalReview='normal-review-v1/index.html',normalEvidence={k:evidence[k] for k in ['checks','fullCheckpoints','freshVisibleTitleContinues','nativeSourceCaptures','exactOriginalContinuedPairs','stableBoundedInputs','unchangedOwnerNonLogFiles']},fullGoalComplete=False);selection_path.write_text(json.dumps(selection,indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh normal South run05

## Objective and acceptance
Full master-matched Marsh set/consistency/polish active/incomplete. Normal South
run05 selected provisionally; full checkpoint/visible Continue scope verified.

## Accepted decisions and constraints
Complete whole bodies/master-material scale147occupied,H148,p92/172,184canvas.
Six100ms loop/distance0.11027027027027027cell cadence, no mirror/patch/recolour/
perposefit. Contactbottom172runtimepivot, idle actualbottom171 unchanged. No
controller/schema/economy/failure changes or owner save testing.

## Current state
catalog body appends candidate05; rootselection full normal evidence recorded.
New independent tests/test_marsh_south_run_production.gd+UIDcp6shrunb2v83,
normal prep/install/fingerprint/publisher/recorder/native900registration tools.
normal-review-v1 has16captures,two8pairboards and currentfourfacingrun sourceboard.
Pipeline,bible,status and exact installedskill mirror appended. New East run
guides/provenance: four selectedidle/gait and6oldrunframes, originalmaster inspected;
no generation or candidate yet. Whole source guides use256registration only.

## Verification
226checks/8full saves/8fresh actual visibleTitleContinues/16views/8exactsource-root
pairs, wholeactor/player parity,pause and resumedrunroute/distancephase.0fail/engine0/
exit0;124bounded inputs stable,2931ownerfiles unchanged scratchAPPDATA. All8pairs
andfourfacingheldrunboard inspected. native classifier confirmscompanions/native900.
InitialpublisherstaleWestassert corrected only; passednative interval unchanged.
74body/228states/1190slots coverage, not complete quality. No continuousfilm,
articulated contacts/naturaltraffic/helmet/entirefamily art acceptance.

## Next action
Author complete East run sixphases+neutral at selected32x147idle anatomy/material,
using frozen oldrun only for motion; keep asymmetric ownEastmaster/righttemple.
Then source/native/cadence/fullsave checks. Other runfacings/carry and68remaining
datedheldinventoryboards/full consistency and movingcontact polish remain.
No liveprocess afterrecord milestone; South normal native terminalexit0.
'''
    (ROOT/'docs/MARSH_SOUTH_RUN_NORMAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8');print('Recorded normal South run05/full Continues, current family review and prepared East own-master references.')
if __name__=='__main__':main()
