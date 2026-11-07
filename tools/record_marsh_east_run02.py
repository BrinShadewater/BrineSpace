"""Record clearer whole near/far cycle and native proof, correcting hardware notes."""
from pathlib import Path
import json,runpy,hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
MARKER='## Marsh East alternating run02 and original ankle hardware correction — October 2, 2026'
LESSON='''
## Marsh East alternating run02 and original ankle hardware correction — October 2, 2026

CORRECTION to preceding East passing03/04/05 notes: the ORIGINAL East standing
master visibly contains small ankle buckles. Calling their existence newly added
hardware was incorrect. Original master re-inspected directly this milestone;
selected low-resolution idle makes these small details less conspicuous. Judge
buckle size/density and boot geometry against BOTH original and selected body,
not absence inferred from small sprites. Keep exact historical prompts/raws and
rejections; their leg stance/high-knee findings remain valid. Presence of authentic
hardware is no longer a rejection reason. This later correction governs.

Farpass06 exec-fa9027c7-2f60-4fb3-8fbc-72a3f45d7d8f used TWO unchanged complete
selected walk3/idle figures at nearest4x/same registration as one edit guide,
original identity second. Correct foreground ivory thigh trailing LEFT/rear,
but rear sole still reaches below front sole. Complete passing82x144/ruler35x147,
one neutral scale .20445062586926285. Farpass07
exec-ef6a23dc-f80c-4a27-8060-44bae9988d33 ordered selected idle PRIMARY then06
whole overlap guide then original; raises rear boot but reverses foreground thigh
to front support again.77x143/ruler38x148,scale .17253521126760563,unselected.
Farpass08 exec-c04b7103-7fb0-49f3-b484-a6225ffa76b4 directly edits WHOLE06 first,
selected idle anatomy second, original third. Foreground ivory thigh stays left
into rear knee/raised rear boot; far thigh partly hidden descends to front flat
boot.68x144/ruler36x147,scale .2053072625698324. Complete figures alpha128,
one neutral scale, whole registration/no-clipping counts checked. All exact frozen
prompts/ordered reference hashes/raw IDs/original paths retained; no limb patch,
mirroring, recolour or per-pose fit. All three raw and packed boards inspected.

Enlarged complete first-source001/002/005 plus new opposite contact/flight/pass08
board confirms first-source near-support passing/far-knee flight, new far-contact/
far-support passing/near-knee flight. Candidate02 is six unchanged complete files
from01[0,1,2],half02contact,pass08,half02flight, byte-identical to packed originals.
Sizes114x135/71x137/95x127/101x146/68x144/90x140. Six100msloop,184canvas,p92/172,
H148 and explicit existing0.11027027027027027cell East stride retained. Source
APNG sixdecodedframes exactly match,loop0 is illustrative. Common foot pivot;
independently authored halves retain different compression/head/body positions.
Full six-pose board reviewed. CLEARER anatomical alternation, not full art
acceptance. Second half is more upright; head/torso/hip/arm joins need refinement.
Do not normalize each pose to standing height or squeeze occupied widths.

Fresh staged ACTUAL normal Marsh.move/main/grid/player/native East02 study:
444checks/8exactsource-native pairs/95controlled20ms samples/2wraps/6actor-player
restores and pause holds, normal slowing to selected walk;0fail/engine0/exit0.
103bounded inputs stable during interval,2931owner nonlogfiles unchanged using
scratchAPPDATA. Dedicated furnished room route retained from validated Eastv2
fixture; no movement/navigation/art runtime or normal catalog changes. Fixture
UIDcr8ehrun02v85 paired. Console label now correctly EAST02. Site authors free
room via place_room(...,true); normal global free-build/failure flags false does
not prove paid room construction. All8 source/native CROPS in two boards inspected;
actor readable with furniture, no full-scene occlusion or continuous-film claim.
Native evidence covers candidate02 only. No fullSave/TitleContinue or articulated
foot-contact/complete animation family acceptance. Review actor-review-v2/index.html.

Lesson: a whole pose can establish thigh overlap yet fail contact-plane identity;
track each leg through knee/shin/boot and compare sole heights. Direct editing a
complete correctly overlapped sheet preserved this order in08; reference ordering
may affect results, but one success is not a general reliability guarantee.
Re-open the original master before labeling a small detail invented. Retain
failed generations and correct conclusions transparently rather than rewriting
their exact prompts. Native controller proof and held crops do not settle body
compression/coherence across independently generated half cycles.

Next refine whole first-half contact/passing/flight compression and head/torso/
profile joins against selected idle/original and second half; inspect complete
cycle, refresh native proof after source changes, then normal admission/fullSave/
Continue if accepted. West/North run/carry and held families/full-set consistency/
polish remain. Full Marsh goal ACTIVE/INCOMPLETE; normal East selection unchanged.
'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    attempts=[]
    for n in ['06','07','08']:
        request=json.loads((BASE/'sources'/f'farpass-{n}.request.json').read_text());recipe=json.loads((BASE/f'farpass-{n}-unselected/recipe.json').read_text())
        assert sha(BASE/'sources'/f'farpass-{n}.prompt.txt')==request['promptSha256']
        for ref in request['orderedReferences']:assert sha(ROOT/ref['path'])==ref['sha256']
        assert sha(BASE/'sources'/f'farpass-{n}.raw.png')==recipe['rawSha256']
        for r in recipe['records']:assert sha(BASE/f'farpass-{n}-unselected'/r['file'])==r['sha256']
        attempts.append({'attempt':n,'generationId':request['generationId'],'scale':recipe['commonNeutralScale'],'sizes':[r['size'] for r in recipe['records']],'rawAndPackedInspected':True})
    assessment={'normalAdmission':False,'fullGoalComplete':False,'allEightViewsInspected':True,'inspectedViewScope':'Exact source and framebuffer crops in paired-0/paired-1, not full scene coverage or continuous film','sourceComparisonsInspected':['candidate-02/comparison.png','half-02-unselected/leg-continuity-review.png','farpass-06-unselected/comparison.png','farpass-07-unselected/comparison.png','farpass-08-unselected/comparison.png'],'phaseReview':'Near/far contact, support passing and knee-forward flight now visually distinct; whole thigh-to-boot continuity inspected. No continuous articulated contact acceptance.','appearance':'Second half more upright and head/torso higher, first half more compressed. Head/torso/hip/arm joins need whole-source refinement before normal selection.','hardwareCorrection':'Original own East standing master visibly includes ankle buckles; preceding existence-based rejection incorrect. Density/size compared separately.','attempts':attempts,'limits':'Staged normal movement only. No fullSave/TitleContinue/realtime film/full-family art acceptance.'}
    review=BASE/'actor-review-v2';(review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n');(BASE/'candidate-02/review.json').write_text(json.dumps(assessment,indent=2)+'\n')
    for n in ['03','04','05']:
        path=BASE/f'farpass-{n}-unselected/recipe.json';data=json.loads(path.read_text());data['limits']='Held source only. Original East master DOES contain ankle buckles; previous existence-based rejection incorrect. High-knee03 or wrong near-support04/05 and body/profile joins remain unaccepted. No native or normal admission.';path.write_text(json.dumps(data,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_east_run02_actor.py'),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh East run02

## Objective and acceptance
Full master-matched set/consistency/polish active/incomplete. Unselected East02
has clearer six-phase near/far alternation. First vs second half compression and
head/torso/hip/arm joins remain unaccepted. Normal East catalog unchanged.

## Accepted decisions and constraints
Original master DOES include ankle buckles; earlier existence-based rejection
incorrect and superseded. Judge size/density. Whole authored sprites only, one
neutral scale per sheet, no patch/mirror/recolour/per-pose fitting.184canvas,
p92/172,H148,six100msloop,existing0.11027027027027027cell stride.

## Current state and changed files
character/marsh-east-run-material-v1: complete06/07/08 exact frozen requests/raws/
original paths/IDs, passing/ruler recipes and comparison boards, complete leg
continuity board,candidate02 six byte-identical source figures/manifest/APNG/
recipe/comparison/review, actor-review-v2 eight exact captures/crops/two boards/
scoped verification/visual assessment.03/04/05recipe conclusions corrected;
historical prompt/raw provenance preserved. New prepare06/07/08,review-legs,
build02,native fixture/fingerprint/publisher/recorder tools; fixture UID paired.
Pipeline/bible/status/master-repair and installed skill mirror appended.

## Verification and scope
444checks/8source-crop pairs/95controlled20ms samples/2wraps/6restores+pauseholds/
normal walk slowing;0fail/engine0/exit0.103bounded inputs stable in native interval,
2931owner nonlogfiles unchanged scratchAPPDATA. Eight source/native crops in two
boards and complete phase/attempt boards inspected. No continuous film, fullscene
occlusion, articulated contact, fullSave/TitleContinue or full-set art acceptance.
Free fixture-room authoring allowed; false normal testing flags not paid-site proof.

## Remaining work and next action
Refine complete first half against original/selected idle and second-half anatomy,
camera, grade and compression; inspect whole motion, refresh native after changes,
then normal admission/fullSave/Continue if accepted. West/North run/carry, held
family review, full consistency and polish remain. Native session97720 terminal0.
'''
    (ROOT/'docs/MARSH_EAST_RUN_02_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded East02 staged444 proof, clearer alternation/remaining joins, original hardware correction; goal incomplete.')
if __name__=='__main__':main()
