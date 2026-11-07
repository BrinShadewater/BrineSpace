"""Record first held-family inspection scope without promoting inventory into acceptance."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-selected-family-audit-2026-10-02'
MARKER='## Marsh current full selected-family inventory and initial review — October 2, 2026'
LESSON='''
## Marsh current full selected-family inventory and initial review — October 2, 2026

tools/audit_marsh_selected_families.py resolves current ordered normal catalog
from source, not older consistency runtime-contract.73body manifests select228
states/1190slots; all metadataH148, no occupied silhouettes touching source edges.
All selected paths/hashes, metadata/timing, ordered overrides and74complete family
boards retained incharacter/marsh-selected-family-audit-2026-10-02. Common pivot
registration uses per-family whole silhouette extents and asserts no clipping.
No generated interpolation, palette repair, pose height fitting or acceptance
from dimensions. Equipment is precomposed in selected body states; this source
inventory does not by itself prove runtime action reachability or equipment joins.

First SIX boards inspected in held source form: idle,walk,run,carry,weld,swim.
Idle/walk retain current narrower selected masters; run-to-idle/walk head/upper
body/material relationships deserve own-master and moving review next. Carry
front/side head/torso/box joins remain a separate target. South welding is a
deliberate lowered/toward-camera posture; do not force it to standing height or
upright side silhouette. Swimming foreshortening changes projected length and
occupied height; keep own camera/master density, not equal perspective rectangles.
These are review priorities, not automatic anatomy failures or completed moving
acceptance.68remaining boards unreviewed by this inventory milestone. Fullset
coverage counts and edge checks do not prove full master/style/size/proportion/
grade/animation quality; retained dated scoped native evidence remains separate.

Review:character/marsh-selected-family-audit-2026-10-02/index.html.
Next: run idle/action whole-body comparison and repair where evidenced, remaining
selected family boards, full-set runtime/motion and consistency/polish. Entire
Marsh objective stays active and incomplete.
'''
def main():
    path=BASE/'inventory.json';report=json.loads(path.read_text());observations={'idle':'Current selected directional identity/standing anchors; held review only.','walk':'Current slimmer South/North material selections retained; full moving/foot contact acceptance separate.','run':'Priority: own-master head/upper-body/material and idle/walk joins, then movement cadence. Dimensions alone not anatomy verdict.','carry':'Separate own-master head/torso/box/idle joins and cargo lifecycle review target.','weld':'South lowered toward-camera working posture deliberate; do not force standing height. Tool/contact/material joins need scoped runtime review.','swim':'Directional foreshortening/projected length intentional; own-master density and equipment/transition joins require motion review.'}
    for board in report['boards']:
        if board['family'] in observations:board.update(visualReviewed=True,reviewScope='All held source figures inspected; no new master/moving/runtime acceptance.',observations=observations[board['family']])
    report['initialHeldFamilyReview']={'inspectedFamilies':list(observations),'unreviewedBoards':sum(not b['visualReviewed'] for b in report['boards']),'fullGoalComplete':False}
    path.write_text(json.dumps(report,indent=2)+'\n')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes());print('Recorded6held family reviews/68unreviewed; no fullset acceptance claim.')
if __name__=='__main__':main()
