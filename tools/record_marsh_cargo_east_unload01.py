"""Record whole East lowering source review, not runtime or visual acceptance."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';S=B/'sources';O=B/'east-unload-01-unselected'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'east-unload-01.request.json').read_text());recipe=json.loads((O/'recipe.json').read_text())
assert r['generationId']=='exec-6127a987-1f8c-45b1-a92e-9e7aca541beb'
assert sha(S/'east-unload-01.prompt.txt')==r['promptSha256']
assert sha(S/'east-unload-01.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
for q in r['orderedReferences']+r['sourceFrames']+r['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
assert recipe['exactCarryEndpoint'] and recipe['exactIdleEndpoint'] and recipe['exactPickupReversal'] and recipe['decodedApngFrames']==8
assert [q['occupiedSize'] for q in recipe['records']]==[[80,113],[86,91],[34,147]]
assessment={'normalAdmission':False,'fullGoalComplete':False,'nativeActionReviewed':False,'rawSourceSeen':True,'allFourOrderedReferencesSeenBeforeGeneration':True,'wholeMotionBoardInspected':True,'neutralBoardInspected':True,'findings':'Whole right-facing lowering figures preserve side-case inset panel/single ivory edge latch, authentic right temple and connected gloves. Neutral34x147 vs selected32x147 width+2; heads read slightly larger in crouches. Floor case is close to boot floor but physical contact, exact case dimensions, arm/leg lengths and camera/grade joins remain provisional. Exact endpoints do not prove intermediate continuity.','limits':'Eight exact decoded review-APNG frames and whole reversed pickup are source parity only. No native normal workshop/expedition action, full Save/TitleContinue, contact film, normal selection or full-set acceptance.'}
(O/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
r['status']='generated, retained and whole-packed; source/neutral boards inspected; unselected and native action pending'
r['limits']=assessment['limits']
(S/'east-unload-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh East held-cargo source 01 — October 2, 2026'
lesson='''

## Marsh East held-cargo source 01 — October 2, 2026

Following all12 same-revision staged turn coverage, East unload-01 generated with
exec-6127a987-1f8c-45b1-a92e-9e7aca541beb. Frozen exact prompt/four ordered refs
and source/guide hashes checked; all exact reference versions viewed before call.
Raw original retained and copied with SHA. Two complete lowering figures + neutral
East ruler; one alpha128 neutral147 BOX scale .2237442922374429 produces80x113,
86x91 and neutral34x147 vs selected32x147. Whole figures translated using body-boot
floor-band midpoint (exclude the case), bottom172; no opaque clipping or per-pose
fit/mirror/patch/recolour. Boot registration does not establish cargo floor contact.

Whole-motion and neutral boards inspected. Correct RIGHT profile, side inset panel
and single ivory RIGHT-edge latch retained through lowering; no frontal two-latch
box substitution. Neutralwidth+2 and crouched heads somewhat larger; rigid case
dimensions, limb lengths, camera/grade joins and contact remain provisional.
Unselected unload-east uses unchanged stagedcarry0, two whole generated poses,
unchanged selectedidle0; pickup exactly reverses complete PNGs. Preserve selected
state metadata as well as four130ms nonloop timing, top-level184/p92/172/H148.
Eight decoded APNG review frames pixel-exact. These checks establish source parity,
not normal action playback, physical contact, save/Continue or visual acceptance.

Next inspect actual normal workshop/expedition lowering/pickup using the selected
contract before admission, and correct whole source figures where joins/contact
fail. Three other facings and coherent carry-family save/Continue gates remain;
full set and cross-family consistency/polish still required. Goal active/incomplete.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f: present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARGO_EAST_UNLOAD01_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh East lowering 01

## Objective and acceptance
Full master-matched Marsh set, then cross-family consistency and polish. Active,
incomplete. East held source remains unselected and visually provisional.

## Accepted decisions and constraints
Own East selected body PRIMARY, staged cargo projection, old poses motion-only,
original East identity. One neutral scale; whole figures only; exact endpoints.
Selected pickup/unload four130ms frames, not legacy six-frame helper inference.

## Current state
carry-all-paths02 handoff covers all12 staged routes on one current parent revision.
East unload01 raw/request retained in marsh-cargo-held-material-v1/sources;
east-unload-01-unselected contains four-frame unload/pickup and review boards.
New retain/pack/record_marsh_cargo_east_unload01.py tools. Pipeline/bible/status and
canonical/installed skill synchronized. No normal catalog or runtime art selection.

## Verification
All refs/raw/whole-motion/neutral boards seen. Neutral34x147 vs selected32x147;
two whole poses80x113/86x91. Exact endpoint copies and whole pickup reversal;
8 APNG frames decode pixel-exact, no opaque clipping. Single-edge side-case retained.
Head, proportion, rigid-case and floor contact findings remain open. No native held
action test yet. No live job. Original generation retained with request hashes.

## Next action
Probe normal staged workshop/expedition pickup/unload with scratch APPDATA and
owner fingerprints, observing real action elapsed/player frames and lifecycle.
Review exact source/native pairs and physical contact; correct whole figures as
needed. Author other three facings, full saves/actual visible Continue, then coherent
normal-family admission. Full remaining set and consistency/polish must continue.
''',encoding='utf-8')
print(json.dumps({'generationId':r['generationId'],'decodedReviewFrames':8,'normalAdmission':False,'nativeActionPending':True,'skillMirrorsEqual':maintained.read_bytes()==installed.read_bytes()}))
