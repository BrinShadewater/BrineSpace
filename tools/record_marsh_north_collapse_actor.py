"""Record inspected North whole-source study without normal admission."""
from pathlib import Path
import json, runpy
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-collapse-material-v1'
MARKER='## Marsh North dry-collapse material and actor study — October 2, 2026'
LESSON='''
## Marsh North dry-collapse material and actor study — October 2, 2026

Unselected candidate02 combines exact selected North idle0, a complete newly
authored milder first dip, and four complete later source01 poses. Both raw
generations retain frozen prompts, ordered reference hashes and execution IDs.
One global neutral-derived scale per source; whole-cell BOX/alpha128 and whole
translations only. No limb painting, per-pose height fitting or palette repair.

Selected idle occupies55x146 although declared standingHeight is148. Source01
neutral occupies55x146; source02 neutral56x147 after sampling. Keep metadata148,
but calibrate occupied neutral against occupied master, not metadata. Do not
force sampled bounds with a separate pose scale. First dip59x132 reduces the
standing silhouette by14 rows, improved from21; old guide reduces it by11 rows.
This is a milder provisional dip, not a forced135-row target. Later widths
69/72/93/106 and heights99/83/56/60 reflect articulation and foreshortening.
Old prone119x78 is a motion guide, not permission to stretch new anatomy.
Rear-view dark heels/soles are legitimate selected/master material. Preserve
ivory boot uppers and shin guards without whitening exposed charcoal soles.

Actual normal Marsh.die and main/grid/player with explicit staged candidate02:
249checks,8exact source captures,6actor/player restores,66controlled20ms samples,
0failures/engine errors/exit0.63 bounded inputs stable;2931owner non-log files
unchanged under scratch APPDATA. All eight source/native views on both paired
boards inspected: whole figures unobscured, warm ivory/sage grade retained.
Fixed root and zero locomotion offsets; pause/restore and final20sec hold pass.
This is actor-only restoration, not full RunSave/TitleContinue. Native/source
APNGs are six exact180ms captured poses, one play, not realtime motion films.
Articulated hand/knee world contact, moving head/torso joins, final foreshortening
and whole-family acceptance remain open. Normal catalog and injury art unchanged.

Review:character/marsh-north-collapse-material-v1/actor-review-v1/index.html.
Next: coherent North white-fluid injury/rise with separately authored effects
behind exact complete bodies, then impact/recovery and normal restoration when
admitted. Full Marsh set and family polish remain active and incomplete.
'''

def has_marker(path):
    with path.open(encoding='utf-8') as stream:
        return any(MARKER in line for line in stream)

def main():
    review=BASE/'actor-review-v1'
    assessment={'normalAdmission':False,'allEightPairedViewsInspected':True,
      'pairedBoards':['paired-0.png','paired-1.png'],
      'material':'Warm ivory/sage retained; dark rear heel/sole faces match legitimate master material.',
      'firstDip':'59x132;14 occupied rows below selected146-row neutral versus old11-row reduction; provisional milder articulation.',
      'ruler':'Declared H148; selected/source01 neutral55x146, source02 neutral56x147 after sampling. No separate pose fitting.',
      'visibility':'All eight complete source/native figures unobscured at furnished clear center site.',
      'contact':'Fixed root and source floor registration observed; articulated limb world contact not established.',
      'proportions':'Head/torso joins, deep crouch transition and final106x60 prone foreshortening await moving/family acceptance.',
      'scope':'249checks/8exact sources/6actor-player restores; controlled visual clock. No full Save/TitleContinue or realtime moving review.',
      'next':'North white-fluid injury/rise from exact complete bodies and separately authored effects; retain unselected status.'}
    (review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_north_collapse_actor.py'),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        if not has_marker(path):
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh North dry collapse

## Objective and acceptance
Full master-matched Marsh set and family polish remain active/incomplete.
North candidate02 is a provisional staged study, unselected in normal catalog.

## Accepted decisions and constraints
Complete generated anatomy; one occupied-neutral scale per source, metadataH148.
No pose fitting, limb patches, mirroring or recoloring. Dark exposed soles valid.
Owner profiles/layouts and normal costs/failures preserved.

## Current state
character/marsh-north-collapse-material-v1 retains two raw sources, exact prompts,
reference hashes, candidates01/02 and actor-review-v1 with eight inspected views.
New prepare/build soften helpers, native review fixture and pairedUID, fingerprint,
publisher and recorder. Pipeline/bible/status and identical skill mirrors updated.

## Verification
249checks/8exact sources/6actor-player restores,66controlled20ms samples; exit0,
engine0.63input hashes stable;2931owner files unchanged. Both boards/all8views
inspected. Fixed root/offsets, pause and20sec settled hold pass. First dip reduces
occupied height14rows versus prior21 and oldguide11; source02 ruler samples147
rows versus selected146. No full Save/TitleContinue or realtime moving acceptance.

## Next action
Prepare North white-fluid injury/rise using exact whole bodies and authored
effect-only swatches; inspect rear-view glove anchors and stationary puddle.
Then actual injury/recovery, normal restoration/admission, other facings and
family moving review. Head/torso joins and prone foreshortening remain provisional.
'''
    (ROOT/'docs/MARSH_NORTH_COLLAPSE_MATERIAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded North staged milestone; normal admission false, full goal active.')

if __name__=='__main__':main()
