"""Record reviewed South/North complete carry sources and scoped native evidence."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1]
MARKER='## Marsh South and North carry01 staged master matching — October 2, 2026'

def main():
    proofs={}
    for direction in ['south','north']:
        base=ROOT/f'character/marsh-{direction}-carry-material-v1'
        assessment={'normalAdmission':False,'fullGoalComplete':False,'allSixViewsInspected':True,'viewCount':6,'wholeNeutralAndCycleBoardsInspected':True,'scope':'Selected idle,four moving carry phases and final paused carry, six exact source/native framebuffer crops in two boards. No fullscene or continuous film acceptance.','appearance':'Fitted adult body/head/quiet warm grade closer to selected own facing; complete two-hand crate support in South, front-held crate fully occluded in North rear view. Cargo/head/hip/sole/camera joins and full-family consistency provisional.','remaining':'East/West carry and all relevant carry turns,pickup/unload/held joins,independent normal full saves/visible Continues,full-set consistency and polish.'}
        (base/'actor-review-v1/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
        runpy.run_path(str(ROOT/f'tools/publish_marsh_{direction}_carry01_actor.py'),run_name='__main__')
        ev=json.loads((base/'actor-review-v1/verification.json').read_text());assert ev['visualReviewed'] and ev['failures']==0 and ev['exitCode']==0 and ev['engineErrors']==0 and ev['captures']==6 and ev['exactSources']==6 and ev['actorPlayerRestores']==4
        proofs[direction]=ev
    s,n=proofs['south'],proofs['north']
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    lesson=f'''
{MARKER}

Full Marsh master/style/camera/size/height/proportion/grade goal remains active and
incomplete. New South and North carry01 cycles are STAGED/UNSELECTED. Normal
catalog remains77 body manifests/228 states/1190 slots, coverage only. No normal
carry admission, full RunSave/Title Continue or complete cargo journey acceptance
belongs to this milestone. Existing selected cardinal run/damage/idle/walk work
preserved. No gameplay/economy/failure/navigation/controller changes.

South source exec-93058684-6a69-4380-ad91-8a7f50de23b5: four whole alternating
cargo-walk poses plus unobstructed neutral ruler. Selected58x147 fitted idle first
PRIMARY; older carry guide only supplies crate/support/motion; own South original
identity third. Preserve swept blond hair, screen LEFT implant, collar/chest plate/
harness and authentic ankle hardware. Slate waist-held crate has two ivory latches,
supported hands overlapping sides, lower belt/hip occlusion. One neutral147 BOX
scale .26972477064220185 gives all four64x147 and ruler62x147. Selected versus
ruler widths58/62 diagnostic, not exact geometry proof. Whole source, neutral and
old/new cycle comparisons inspected; head/body/quiet warm grade closer to fitted
master, hand/crate/leg joints provisional.

North source exec-f36e8bbe-a893-4895-99e9-4145a5f7c4ef: four whole alternating
rear cargo poses plus neutral. Selected55x146 rear idle first PRIMARY, own older
rear cargo guide second motion/occlusion ONLY, own original North master third.
Blond hair whorl, rear plate/harness/pouches/small RIGHT-temple edge retained.
Crate is held IN FRONT away from viewer and fully occluded by body, as selected
rear cargo guide shows. Both elbows bent beside waist/forearms forward; no crate
invented on back or behind pelvis. One neutral146 BOX scale .24787775891341257:
57x146/57x142/57x146/57x142,ruler56x146. Native/body/ruler dimensions are scoped
diagnostics; rear support/raised charcoal soles and cargo occlusion judged visually.
Whole source/neutral/old-new cycle inspected. North guide wrapper uses actual
opposite walk0/walk3 and preserves both North/South guide dependency hashes.

Both exact frozen prompts, ordered reference/source SHAs, raw files/original paths/
generation IDs retained. Five complete alpha128 cells per sheet, one unobstructed
neutral BOX scale, whole translation to bbox bottom172 with zero clipped opaque
pixels. No mirror, limb/crate patches, recolour or per-pose/cargo-width fitting.
184canvas,p92/172,H148,four180ms loop and explicit carry stride
.0827027027027027 unchanged. Four APNG frames decode pixel-exact to their sources.
Initial South APNG assertion was a checker bug: collecting mutable iterator frame
objects reused decoder state. Fixed by copying each decoded frame before comparison;
source PNGs unchanged. Illustrative held APNGs are not continuous native film.

Actual normal Marsh.move/main/grid/player in dedicated normal workshop_carry stage
on a clear168world furnished interval: normal46world/sec, correct heading/root axis,
carry selected and running excluded, distance phase order, two wraps, four valid
actor/player snapshots/restores and pause holds, final stationary cargo pause.
South fixture UIDcz7shcarry1v93,North UIDda8nhcarry1v94 paired. North reverses
only physical interval with actual negativeY segment_clear; artwork never mirrored.
Dedicated free fixture room, normal testing_free_build/testing_disable_failures
false, not paid-site proof. Scratch APPDATA; owner's real profile unused.
South{s['checks']} checks/6 exact source-native views/95 controlled20ms samples/
4 restores/2 wraps,{s['stableBoundedInputs']} bounded inputs stable during native
interval. North{n['checks']} checks/6 exact views/95 samples/4 restores/2 wraps,
{n['stableBoundedInputs']} stable interval inputs. Both2931 owner non-log files
unchanged,zero failures/engine errors,exit0. All12 views across four paired boards
inspected. Source and runtime mechanics scoped separately from hand/contact quality.
After both terminal native intervals, publisher assessment key corrected from the
inherited eight-view name to allSixViewsInspected, including future South preparer;
publication metadata only, runtime/source fixtures unchanged. Freeze proves each
native interval, not that every publication helper stayed unchanged afterward.

Limits: authored normal cargo-stage fixture with actual actor movement, not a full
workshop/expedition pickup/carry/unload journey; no full RunSave/Title Continue,
turn endpoint compatibility,natural traffic,equipment/full-family or continuous
moving contact/occlusion acceptance. South passing has less compression than North;
cross-facing cargo/hip/head/sole/grade consistency remains for full-set polish.

Next East own carry guides prepared and reviewed: eight unchanged complete frames
(idle0/1,walk0/3 PRIMARY;carry0..3 cargo/motion ONLY),32x147 selected side idle.
Old carry combined widths75/60/64/55 at148 high are cargo silhouettes, not body
calibration. Head/upper-body grade and crate perspective vary; preserve own visible
implant/side identity and original two-hand cargo support, use one consistent crate
projection across steps. No new East carry source/native acceptance. East guide
wrapper depends on South guide helper; freeze both. Then West own-master carry,
turns/held joins,independent normal full saves/visible Continues,full consistency
and polish. Do not transfer South/North proofs to another facing. Goal incomplete.
'''
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream:stream.write(lesson)
    installed.write_bytes(maintained.read_bytes())
    handoff=f'''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: South/North carry01

## Objective and acceptance
Full master-matched set/consistency/polish active and incomplete. Two complete
own-master carry loops staged and native-reviewed; no normal catalog admission.
Existing77/228/1190 catalog coverage is not full art acceptance.

## Accepted decisions and constraints
Selected own body/camera/grade PRIMARY; old carry only cargo/support/motion.
South crate at waist with two supporting hands/two latches; North front-held crate
fully occluded in rear view. Whole figures/neutral calibration, no mirror/patch/
recolour/pose fitting. Authentic hardware/charcoal soles and asymmetry preserved.
184,p92/172,H148,four180ms,current carry distance cadence. Scratch APPDATA,
owner profile unchanged;normal costs/failures unchanged. Free fixture site only.

## Current state and changed files
South/North carry material-v1 sources with exact raw/ID/original path/prompt/order/
SHAs/guides; candidate01 complete four PNGs/ruler/recipe/manifest/comparisons/APNG.
New prepare/build/native fixture+UID/fingerprint/publisher tools. South helper
reused for North with explicit rear146 calibration/opposite walk0/walk3. Both
actor-review-v1 have6 exact source/native views/two boards/assessment/verification.
Pipeline,bible,status,maintained and installed master-repair skill appended.
East carry guides ready:8 unchanged whole frames/metadata/SHAs/two boards inspected;
32x147 own selected idle PRIMARY. No new East source/native acceptance.

## Verification and scope
South{s['checks']} and North{n['checks']} checks,each6 views/95 controlled20ms
samples/4 actual actor-player restores/pause holds/2 wraps/final stationary hold.
58/62 bounded native-interval inputs stable,each2931 owner non-log files unchanged,
0 failures/engine errors,exit0. SouthpositiveY,NorthnegativeY physical routes;
normal46world/sec/carry rendering/run exclusion/distance phase observed.
All12 native/source views and both neutral/cycle boards inspected. APNG4 decoded
frames pixel-exact. Checker mutable-iterator bug repaired before native validation.
After terminal intervals, publication-only key corrected to actual six-view count;
interval freeze is dated evidence, not current publication-helper immutability.
No full save/Continue,pickup/unload/turn joins,natural traffic,continuous contact,
full-scene/equipment/full-family acceptance. No live native process.

## Remaining work and next action
Author East four whole cargo phases+neutral matching32x147 own side body/master,
consistent crate projection/support,opposite complete leg halves. Then West,
carry turning/held joins,independent normal full-save/visible Continue validation.
Full-set camera/body/head/grade/equipment/contact consistency and polish remain.
Keep goal active. Do not overwrite owner's layouts/saves or infer full acceptance
from coverage counts/native restore checks.
'''
    (ROOT/'docs/MARSH_CARRY_SN_01_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded South/North whole carry sources and six-view native proofs; skill mirrors equal; goal incomplete.')
if __name__=='__main__':main()
