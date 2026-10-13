"""Append a bounded Bill milestone without reading large status/history files."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
note='''

## Bill East detailed-donor reach and stature limitation — October 3, 2026

New bill-east-reach-adjacent-motion-v1 retains all six 760ms slots and exact
idle endpoints. Detailed idle edit target produced a closer warm face, collar
and matte suit. Independent expanded poses from the same donor changed occupied
height to205/191/223 and overflowed; rejected before admission, preserved without
anatomy fitting. Small adjacent whole-pose edits yielded four usable source poses;
supporting superseded recovery remains traceable. All whole figures and three
actual native comparison pages reviewed.

Actual main paused furnished-room V4:904checks0,150prescribed samples,36capture
pairs,engine0/53.84s.4567tested inputs and2931owner non-log files unchanged under
scratch APPDATA. Strict Ysole depth passes. Current crowns24,24,23,22,21,24 and
heights148,148,149,150,151,148 reveal late-pose head/stature rise. Lossless whole
Y-1 registration preserves pixels/contact but can increase crown drift: fixed
profile height and floor checks do not establish anatomical stature consistency.
Candidate provisional/unselected; natural dispatch/full cadence/gear/whole-run
Continue and normal admission remain unverified. New-bank browser review pending.

Lesson: a successful detailed-donor pilot does not establish family consistency.
Compare both contact and stature before expansion/admission. Try small direct edits
from the successful donor to reduce accumulated redraw drift; retain rejected
results and complete provenance chains. Source head-window differences include
movement and are not a style score. Verify PNG RGBA/hash before treating a black
transparent preview as corruption. Use explicit UTF-8 for generated tool reads;
display-only board-label correction retained original pages and exact body pixels.

Full Bill goal active/incomplete. Next late-reach stature/arm arc, full playback,
other East/West/cardinal/gear/water/life families and complete master polish.
Handoff:character/bill-east-reach-adjacent-motion-v1/HANDOFF.md.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:
    paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for p in paths:
    assert p.is_file(),p
    with p.open('a',encoding='utf-8') as f:f.write(note)
print('Appended milestone and bounded lessons to eight maintained records.')
