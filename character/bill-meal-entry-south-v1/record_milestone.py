from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-meal-entry-south-candidate-native-v1'
n=json.loads((OUT/'validation.json').read_text());assert n['passed'] and not n['realProfileChanges'] and json.loads((P/'verification.json').read_text())['passed']
assert '87 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill south bowl pickup/return candidates

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
South bowl transitions connect exact selected idle to corrected eating hold.

## Accepted decisions and constraints
Selected front idle owns identity/perspective/proportions/matte materials.
Connected hands reach, grasp low bowl, left hand supports underneath, draw inward.
Two hands total, planted upright body, subdued steel badge, burgundy shoulders.
Current actual galley contacts N/S; no geometry/reward/service-clock changes.

## Current state
Primary exec-018f1c11-9ba0-457d-bcf0-e672fe42d2be/raw/exact prompt retained.
It had red badge/full empty reach with no visible bowl contact. Corrected source
exec-0721ab24-21ce-40b0-823b-c655b5aa960a/raw/exact prompt retained and selected.
Six493/492/492/493/493/492px figures, interiors0..4 (redundant hold5 retained
unused), fixed[.278,.3001] ruler,density1.13, selected south neutral/skin/hair
grade. Local grade_shoulders.py samples plate interiors instead of dark outlines
for bounded shoulder gain[.81724,.91379,.96429], alpha unchanged. Exact idle/eat000
donors. Two bare staged states/14refs/seven580ms slots/exact reverse return,
256plane/pivot128,224/H148/dry0/sole223. Build/verify/preview/hash evidence retained.
No normal loader/actor changes; actual bowl service phase integration pending.

## Verification
28package/87native PASS12.95s after shoulder correction. Prior brighter native
run archived by runner. Exact pixels, source/donor bindings, finite pacing/hold,
dry metadata, exact idle/held joins and all reversed poses. Fresh148/82/idle boards
reviewed; badge consistent grey, shoulder grade closer, bowl contacts hands before
inward draw, no obvious extra hands/steps. Fine suit/harness details, interior
proportion/arm progression and reversed-return contact readability remain for
full polish. All2,914 owner non-log files unchanged under scratch APPDATA.
Source grasp readability is not proof of physical world-counter reach/contact;
actual contact, interruption, saved phases and disk restore remain unproved.

## Next action
Author south cup pickup-return, assemble full south family, prove actual N/S meal
phase/contact/interruption/restore behavior. Apply shoulder-interior sampling
lesson during wider meal/full-set material audit. West meals/rest/drydeath,
inspection broader audits and full cross-animation polish remain. Goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill south bowl pickup/return candidate — September30,2026.
Primary exec-018f1c11-9ba0-457d-bcf0-e672fe42d2be/raw/prompt retained;
red badge and missing visible contact corrected with built-in
exec-0721ab24-21ce-40b0-823b-c655b5aa960a/raw/exact prompt retained. Six
493/492/492/493/493/492px figures, five interiors0..4, fixed[.278,.3001]
ruler,density1.13, exact idle/current eating-held donors, sole223. Two bare staged
states/14refs/seven580ms slots/exact reverse.28package/87native PASS12.95s after
shoulder grade fix; fresh148/82/idle boards reviewed. All2,914 owner non-log files
intact in scratch APPDATA; no actor/loader/geometry/reward changes.
Lesson: broad red-region medians can be dominated by dark outlines and overboost
burgundy plates (initial gains1.48/1.35/1.59 produced bright shoulder pop).
Use bounded shoulder plate interior samples for authority/source, retain alpha
and one atlas gain; local corrected gain.817/.914/.964. Apply during wider grade
audit rather than trusting neutral cloth match. Ensure visible front hand/bowl
contact before inward draw; exact endpoints do not prove physical counter reach.
Fine detail/interior alignment/contact/reverse readability remain for full polish.
Next south cup transitions/full family, actual N/S service/contact/interrupt/
restore proof, west/rest/drydeath and full-set polish. Full goal active.
Handoff:character/bill-meal-entry-south-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south bowl pickup/return candidate — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/name for name in ['build.py','verify.py','build_preview.py','grade_shoulders.py','manifest.json','verification.json','HANDOFF.md','index.html','source-rulers.json','registration.json','frame-hashes.json','contact-sheet.png']]+list((P/'sources').glob('*'))+[OUT/'validation.json',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_meal_entry_south_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':28,'native':87},'native':n,'scope':'staged authored pickup/reverse/native joins; actual meal phase/contact/interrupt/restore and full polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded south bowl transitions, corrected badge/contact/shoulder grade and native proof')
