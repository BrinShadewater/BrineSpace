"""Record inspected provisional North white-fluid actor milestone."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-injury-material-v1'
MARKER='## Marsh North white-fluid injury and recovery study — October 2, 2026'
LESSON='''
## Marsh North white-fluid injury and recovery study — October 2, 2026

Unselected North injury candidate01 uses exact complete dry candidate02 bodies
and the four previously authored effect-only white-fluid swatches, at unchanged
148-standing density. No new bitmap generation or anatomy edits. Frozen reuse
request hashes18complete body/old guide frames and7effect/provenance inputs.
Old rear guide inspected: coolant on SCREEN RIGHT glove; do not mirror the body
or apply front-view screen-side anchors. Separate droplets at(114,141)/(120,142),
fixed floor puddle center(135,172), growing24-to36px width, retained through rise,
half-alpha in penultimate recovery pose then none. Effects behind exact body;
12opaque body pixel comparisons pass, fall5/rise0 and final idle byte-exact.
Recovery reverses complete body poses, consistent with existing motion policy.

Actual normal physical impact, fall/rise, main/grid/player with staged manifest:
404checks,14exact source/native captures,12actor/player restores,0failures/engine
errors/exit0.107bounded inputs stable;2931owner non-log files unchanged under
scratch APPDATA. Existing renderer reset of cosmetic key supplies exact fresh
idle0 after injury; no runtime/schema changes in this North interval. Pause and
fixed root verified. Both source APNGs and native12pose APNG decode exactly;
180ms one-play holds illustrate poses, not realtime motion/browser acceptance.

Four paired boards/all14views inspected. Complete figures unobscured; warm
ivory/sage body grade, matte dark gloves and exposed rear charcoal soles retained.
White separated drips visible beside right glove; floor puddle stationary through
rise and visible in normal room renderer. These establish held registration,
not physically articulated limb contact or moving fluid continuity. Milder
first-dip timing, head/torso joins and prone foreshortening remain provisional.
No normal catalog admission or full RunSave/TitleContinue in this study.

Review:character/marsh-north-injury-material-v1/actor-review-v1/index.html.
Next: normal North damage-family admission with full checkpoint/TitleContinue
proof once provisional selection is recorded, then remaining facings and moving
family polish. Full Marsh master/style/proportion/grade goal remains incomplete.
'''
def main():
    review=BASE/'actor-review-v1'
    assessment={'normalAdmission':False,'allFourteenPairedViewsInspected':True,'pairedBoards':[f'paired-{i}.png' for i in range(4)],'sourceComparisonInspected':True,
      'material':'Warm ivory/sage exact complete bodies; dark rear soles legitimate. White coolant remains visible in normal renderer.',
      'effectRegistration':'Separated screen-right glove drips, stationary floor puddle beside hand, growth and recovery fade inspected in source/native holds.',
      'wholeBody':'All12opaque body pixel comparisons pass; no body patch/recolor/scale/mirror.',
      'handoffs':'Fall5/rise0 byte-exact; rise5/selected idle0 byte-exact and first actual normal idle equality verified.',
      'limits':'Held views and controlled simulation phase. Moving fluid continuity, limb world contact, head/body joins and prone foreshortening provisional. No full Save/TitleContinue or realtime motion film.',
      'next':'Record provisional normal source selection and verify complete checkpoint/TitleContinue family, then other facings/family moving polish.'}
    (review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_north_injury_material.py'),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh North white-fluid injury

## Objective and acceptance
Full master-matched Marsh set and family polish remain active/incomplete.
North dry/injury/rise remain provisional and unselected in normal catalog.

## Accepted decisions and constraints
Exact complete North candidate02 bodies; reuse separately authored coolant
swatches at148density behind bodies. Screen-right rear glove, fixed floor puddle.
No body patch/fit/recolor/mirror. Owner profiles and normal economy unchanged.

## Current state
character/marsh-north-injury-material-v1: frozen reuse provenance,12whole-body
injury/rise frames, two finite source APNGs, four inspected paired native boards.
New prepare/build, independent actual-impact fixture and pairedUIDce4nhinjm9v72,
fingerprint/publish/record helpers. Pipeline/bible/status and skill mirrors updated.
No new generation or runtime/schema change; previous renderer idle join reused.

## Verification
404checks/14exact source-native pairs/12actor-player restores, pause/fixed root,
exact fall/rise and first normal idle joins;0fail/engine0/exit0.107bounded hashes
stable;2931owner files unchanged.12opaque body comparisons and12source/12native
APNG frames exact. Four boards/all14views visually inspected. Held fluid placement
and complete visibility pass; source-family proportions remain provisional.

## Next action
Provisional normal North damage selection then full20checkpoint/TitleContinue
family proof using established normal South damage harness adapted independently.
Keep normal flags/save rules, scratchAPPDATA and profile fingerprints. Continue
other facings and moving family polish; no realtime/browser/limb-contact acceptance.
'''
    (ROOT/'docs/MARSH_NORTH_INJURY_MATERIAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded provisional North injury milestone; full goal active.')
if __name__=='__main__':main()
