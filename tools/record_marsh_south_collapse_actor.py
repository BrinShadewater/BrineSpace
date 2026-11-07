"""Record actual staged dry actor proof and keep injury/family acceptance open."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-collapse-material-v1'

def main():
    review=BASE/'actor-review-v1'
    assessment={'normalAdmission':False,'allEightPairedViewsInspected':True,'pairedBoards':['paired-0.png','paired-1.png'],'fullSettledStationCaptureInspected':True,'material':'Ivory boot uppers and warm ivory/sage body retained in actual normal renderer; standing initial source byte-exact selected idle.','proportions':'Head/body and compressed prone length remain provisional for family/moving review; do not stretch old bounds.','visibility':'All whole figures visible at corrected open center site. Initial failed site occluded prone head/arms behind tank despite root can_stand.','contact':'Root and normal draw offsets fixed. Source hands/knees/forearms remain registered near the common projected floor plane, but this is not articulated hand/knee world contact proof.','clock':'Actual normal visual player selection with fixture-assigned visual time in66x20ms samples. Pause holds freeze actor/source at fixed visual time. Native APNG is a pose illustration, not realtime film; browser moving review unverified.','next':'Retain as improved staged dry basis; inspect existing white fluid and prepare coherent injury/rise without recoloring/patching anatomy. Full normal acceptance and family polish open.'}
    (review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_south_collapse_actor.py'),run_name='__main__')
    lesson='''
## Marsh South dry-collapse actual actor study — October 2, 2026

Normal Marsh.die, exact main/grid/player render the explicit unselected source01
in furnished Cold Store.249checks/8exact source captures/6actor+player restores
pass,66x20ms controlled visual-clock samples; all six collapse holds visited in
order, dead root/locomotion offsets fixed, long-settled source held at20seconds.
46 bounded input hashes stable and2931 owner non-log files unchanged under scratch
APPDATA; exit0/engine0. All eight views on two paired boards and full settled
station image inspected: ivory boots/warm grade preserved and whole body visible.
Actor-only restore is not full RunSave/Title Continue. No normal catalog admission.

Retained first interval249checks/1failure/exit1: idle player was already breathing,
so fixture's frame0 baseline assertion wrong. Its first standable root also let
tank art occlude prone head/arms. Reset current_key ONLY for study baseline and
choose clear floor envelope nearest room center; do not change production idle,
navigation or props. Intermediate rerun had typed-var GDScript parse error/exit1;
fixed explicit bool. Both failed intervals preserve inputs/profile/logs; final
passed interval is authoritative. Failed occluded captures are not anatomy proof.

Lesson: standable root and clear travel segment do not prove visible room space
for a complete collapse silhouette. Review actual prop layering; don't remove
furniture to make acceptance easy. Also distinguish fixed actor root, source floor
registration and articulated limb world contact: only first two evidenced here.
Normal dead action uses visual player clock; compare exact subtraction at phase
boundaries rather than rounding100+elapsed. Screenshot design coordinates1920x1080
must map to actual framebuffer1333x750 before cropping; crops remain exact pixels.
Six-pose180ms native APNG is illustrative captured poses, not realtime recording
or browser moving review. Head/torso/limb joins and prone foreshortening remain
provisional family work. Old injury guide inspected: white left-hand drips then
floor puddle; injury body itself also differs from dry, so simple image subtraction
is not automatically a clean fluid layer. Preserve white-fluid narrative, dry
shutdown and complete new anatomy when preparing injury/rise.

Review:character/marsh-south-collapse-material-v1/actor-review-v1/index.html.
Next: coherent white-fluid injury/rise basis, actual injury-to-recovery playback,
normal full restoration/admission when art ready, remaining facings/family polish.
Full Marsh goal remains active and incomplete.
'''
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift; do not overwrite'
    marker='## Marsh South dry-collapse actual actor study — October 2, 2026'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',maintained]:
        text=path.read_text(encoding='utf-8')
        if marker not in text:
            with path.open('a',encoding='utf-8') as stream:stream.write(lesson)
    installed.write_bytes(maintained.read_bytes())
    status=ROOT/'docs/CURRENT_STATUS.md';text=status.read_text(encoding='utf-8')
    if marker not in text:
        # Append without truncation: desktop readers can memory-map shared docs.
        with status.open('a',encoding='utf-8') as stream:stream.write(lesson)
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh staged South dry actor

## Objective and acceptance
Full Marsh master-matched set and consistency/polish. Still active/incomplete.
This milestone proves actual staged dry actor placement/player behavior, not
whole-family art acceptance or production source selection.

## Accepted decisions and constraints
Keep complete source01 anatomy, one148 neutral ruler, warm ivory/sage material.
No pose-height fitting, limb painting or palette normalization. Shutdown dry;
injury remains white fluid. Normal costs/failures, owner profile/layouts unchanged.

## Current state
character/marsh-south-collapse-material-v1/actor-review-v1 has8paired source/native
views, two boards, finite pose APNG and scoped verification/visual assessment.
New review_marsh_south_collapse_actor.gd and original pairedUIDca0shclpm5v68,
fingerprint/publish/record helpers. No normal runtime/catalog changes. Pipeline,
bible/status and maintained/installed master-repair skill record this evidence.

## Verification
249checks/8exact source pairs/6actor+player restores,66controlled20ms samples.
Normal die clears work, fixed root/draw offsets, sixordered holds and final20sec
hold; pause at fixed visual time.46bounded inputs stable;2931ownerfiles unchanged.
Exit0/engine0. Two boards/all8views and full settled image inspected. Source01
earlier217source-player checks remain scoped to earlier input interval.
Retained249checks/1failure first interval: baseline breathing and tank occlusion;
retained intermediate parse failure; fixture clock/site/type repaired.
No full RunSave/TitleContinue, natural traffic, articulated limb contact or
browser/realtime motion acceptance. APNG is exact captured pose illustration.

## Next action
Prepare coherent white-fluid injury/rise from improved dry body, retaining effect
without anatomy patching. Old injury body differs from dry: do not assume image
subtraction isolates fluid. Then actual injury/recovery and normal restoration
checks when sources ready. Continue other facings and whole-family polish.
'''
    (ROOT/'docs/MARSH_SOUTH_COLLAPSE_ACTOR_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded actual staged dry actor milestone; full Marsh goal remains active.')

if __name__=='__main__':main()
