"""Record source-only East trials without expanding prior native acceptance."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
MARKER='## Marsh East opposite-half source trials — October 2, 2026'
LESSON='''
## Marsh East opposite-half source trials — October 2, 2026

East remains UNSELECTED. Complete opposite-half02 contact/flight show clearer
near/far arm-leg relationships, but its passing still plants the foreground near
foot. Source exec-810937e2-e0b9-4e4e-869a-4c050585c377 retained with frozen exact
prompt/ordered selected-walk3, selected-idle0, original-East reference hashes.
The two selected single-figure guides are unchanged whole nearest4x references,
not edited limbs. One neutral BOX scale .22720247295208656; four complete frames
101x146/53x147/90x140/36x147. Contact/passing/ruler bottom172; flight source-relative.
All184canvas p92/172; selected idle32x147,metadataH148. Complete first-half vs
opposite contact/flight/rulers board visually inspected: clearer opposition but
more upright pose, higher head/torso and different compression/profile density.
Matching neutral heights do not prove smooth joins; occupied bounds do not tell
whether the change is natural pose compression or anatomy drift. No forced fit.

Three complete two-figure passing attempts retained unselected:
03 exec-708e30dd-16c4-4c05-9991-5df7c09b4e0d: high knee instead of low passing,
added ankle hardware. One neutral scale .17093023255813952;80x144/ruler35x147.
04 exec-2dee63bb-6b7c-4990-a042-59410dfe64d6: front boot planted/rear raised,
but foreground near thigh still supports, added buckles; scale .18036809815950922,
80x145/ruler36x148. Correct left/right screen position is not near/far leg identity.
05 exec-a7e3d08a-7adb-4438-a3b8-aac531ce1500: explicit foreground trailing/far
support request and positive plain ankle-band wording still produces near support
and ankle buckles; scale .1678082191780822,75x144/ruler34x148. Positive wording
alone did not resolve this result; no causal claim that negative wording caused it.
All three raw sources and packed selected-idle/passing/ruler boards inspected.

Every request frozen before built-in image generation; raw/original paths,
execution IDs, source/ref/prompt/frame hashes retained. Complete cells, alpha128,
one neutral scale per authored sheet, whole translations and no-clipping pixel
counts checked. No mirroring, limb patches, recolour, per-pose fitting or gameplay
changes. Ten new packed figures across four sources are held source studies;
no new runnable sequence, catalog admission, native test or fullSave/Continue.
Earlier444-check staged East proof covers candidate01 only, not these new figures.
No owner-save access or Godot process was needed for this source-only milestone.

Lesson: verify foreground thigh-to-knee-to-boot continuity, not just which screen
boot touches the floor. Explicit text, correct whole-pose references and distinct
frame files do not establish anatomical alternation. Removing generated pose
guides or using positive suit descriptions is an experiment, not a proven remedy.
Keep failed complete sources and inspect body/head density and compression across
the whole cycle before combining independently authored halves. Matching ruler
calibration does not remove the need for common camera/proportion/motion review.

Next: author a coherent complete East cycle with true far-support passing and
matching head/suit/pose joins; refresh staged normal movement proof, then normal
selection/fullSave/Continue if accepted. West/North run, carry and remaining
held families/full-set consistency and polish remain. Full master/style/camera/
size/height/proportion/grade goal ACTIVE/INCOMPLETE.
'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    attempts=[]
    for name,folder in [('half-02','half-02-unselected'),('farpass-03','farpass-03-unselected'),('farpass-04','farpass-04-unselected'),('farpass-05','farpass-05-unselected')]:
        request=json.loads((BASE/'sources'/f'{name}.request.json').read_text())
        assert sha(BASE/'sources'/f'{name}.prompt.txt')==request['promptSha256']
        for ref in request['orderedReferences']:assert sha(ROOT/ref['path'])==ref['sha256']
        recipe=json.loads((BASE/folder/'recipe.json').read_text());assert recipe['normalAdmission'] is False
        assert sha(BASE/'sources'/f'{name}.raw.png')==recipe['rawSha256']
        for record in recipe['records']:assert sha(BASE/folder/record['file'])==record['sha256']
        attempts.append({'source':name,'generationId':request['generationId'],'commonNeutralScale':recipe['commonNeutralScale'],'sizes':[r['size'] for r in recipe['records']],'comparisonVisuallyInspected':True})
    assessment={'normalAdmission':False,'fullGoalComplete':False,'attempts':attempts,'joinComparisonVisuallyInspected':True,'phaseFinding':'Half02 contact/flight show clearer opposite relationships; true far-support passing remains absent. Front planted screen position is insufficient.','joinFinding':'Half02 poses more upright and head/torso higher than candidate01; coherent cycle compression/proportion continuity unaccepted.','limits':'Source-only studies. Earlier444check native interval covers candidate01, no new native or normal selection proof.'}
    (BASE/'half-02-unselected/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh East opposite-half trials

## Objective and acceptance
Full master-matched set, consistency and polish active/incomplete. East sources
held unselected. Clearer opposite contact/flight; true far-support passing absent.

## Accepted decisions and constraints
Selected East idle and original master control anatomy/material/camera, correct
whole walk reference controls stance. One neutral BOX scale per authored source,
whole184canvas p92/172 figures, alpha128, no mirror/patch/recolour/per-pose fit.
Whole source preservation and exact frozen prompt/reference provenance mandatory.

## Current state and changed files
character/marsh-east-run-material-v1: half02 and farpass03/04/05 exact requests,
raws, execution IDs/hashes, ten packed whole figures/rulers/recipes/comparisons,
first-half-join-comparison and visual-assessment. Sources held unselected.
tools: prepare_marsh_east_run_half02,build_marsh_east_run_half02,
prepare_marsh_east_run_farpass03,prepare_marsh_east_farpass04/05,
pack_marsh_east_farpass_drafts,compare_marsh_east_run_halves,
record_marsh_east_run_half02. Pipeline/bible/status/master-repair mirror appended.
No normal catalog, gameplay or controller changes.

## Verification and limits
Four frozen prompts/twelve ordered refs/four raws/ten frame hashes verified;
builders checked complete alpha column cells and no-clipping pixel preservation.
Raw/packed attempts and six-figure join comparison visually inspected. Half02
more upright/higher torso-head than01; neutral calibration alone not motion
consistency proof.03high knee,04/05wrong near support; added ankle buckles recur.
No Godot/native/save tests this source-only milestone. Prior444check candidate01
proof remains scoped to that source; these drafts are not covered by it.

## Remaining work and next action
Coherent complete East cycle with far-support passing, correct hardware and
matched head/torso/pose joins. Review whole motion, refresh staged native proof,
then normal admission/fullSave/Continue if accepted. West/North run/carry, held
family review and full-set consistency/polish remain. No live process.
'''
    (ROOT/'docs/MARSH_EAST_RUN_HALF_TRIALS_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded four unselected sources/ten figures and reviewed joins; skills mirrored; full goal active/incomplete.')
if __name__=='__main__':main()
