from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
note='''## Bill flood visibility isolated and readability staged — October 2, 2026

Eight frozen-source native diagnostics/both gears show crew attenuation hides Bill:
white crew restores the figure; hiding retained floor water or foreground does not.
Original selected full-water swim tint RGB(.37,.71,.74)/alpha.23 is the cause in
these captured East replacement poses. No source repaint, scale, foot or sort change.
70checks0fail/47.73s. Eight additional native comparisons use Bill-only staged
high-water RGB(.72,.86,.86), alpha.62/.78/.90 versus normal:66checks0fail/45.9s.
All16native presentations/two boards viewed;32original source-room files retained.
Both intervals engine0/clean log;2931owner non-log files unchanged/scratch APPDATA.
Source RGBA and physical foot unchanged between each gear's variants.

Alpha.90 is preferred for the next motion study: face/helmet/suit read better while
remaining submerged. Original shadows/bubbles/clock and water layers retained in
candidate. Stage only, normal renderer untouched. This is one actual flood takeover
pose per gear, not full cardinal swimming/treading, motion, original-master match,
water-depth continuity or outside-room fallback acceptance. The threshold .85
candidate branch is a study, not an approved transition. Case ownership may persist
while presentation is suppressed in water; this study does not resolve its lifetime.
Next continuous full-water source motion, depth transition and other directions,
then guarded normal admission, remaining cargo transitions and full-library polish.
Goal active/incomplete. No commit/export. Review:
character/bill-floor-case-north-v1/flood-readability-review.html.

Lesson: isolate same-source/same-clock/same-foot attenuation separately from floor
and foreground layers before changing character art or sort order. Original RGBA
can be valid yet lose identity under runtime tint/alpha. Retain water cues and
check actual native detail; static readability does not certify depth transitions.

'''
for file in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 target=R/file;old=target.read_text(encoding='utf-8')
 if note.splitlines()[0] not in old:target.write_text(note+old,encoding='utf-8')
for target in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=target.read_text(encoding='utf-8')
 if note.splitlines()[0] not in old:target.write_text(old+'\n'+note,encoding='utf-8')
files=['flood_readability_view.gd','prepare_flood_readability_audit.py','build_flood_readability_review.py']
decision={'preferredCandidate':{'rgb':[.72,.86,.86],'alpha':.90},'selectedInProduction':False,'visualReview':'Both native boards/all16 presentations viewed; .90 strongest retains face/helmet/suit detail. One East pose per gear; no continuous/cardinal/master acceptance.','sourceFilesSHA256PostRun':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in files}}
(P/'flood-readability-decision.json').write_text(json.dumps(decision,indent=2)+'\n')
(P/'FLOOD_VISIBILITY_HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill flood readability

## Objective and acceptance
Complete full Bill set matching masters/perspective/stature/proportions/matte grade,
then cross-family consistency and motion polish. Active/incomplete.

## Accepted decisions and constraints
Preserve original art, physical root, depth and owner profile. Runtime attenuation
causes observed full-water invisibility; no source regeneration needed for this defect.

## Current state
New staged flood_readability_view, fixture/runner and rebuildable review with32
original captures. RGB(.72,.86,.86)/alpha.90 preferred for moving-pose study only.
No production renderer/selection change. Pipeline/bible/both skill copies updated.

## Verification
70diagnostic+66candidate native checks0fail;47.73/45.9seconds. All16presentations
viewed/two boards. Each gear's exact source/foot unchanged. Engine0/clean logs;
2931owner files unchanged/scratch APPDATA. Source hashes post-run only.

## Next action
Continuous flood motion/cardinal/depth transition review; outside-room fallback,
early held-case priorities, shared-room floor lifetime, older-bank Continue and
normal guarded admission. Cargo idle join and full-library master polish open.
''')
print('Bill milestone, scoped decision, handoff and pipeline/bible/skill lessons recorded.')
