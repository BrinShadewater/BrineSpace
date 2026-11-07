from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent.parent;P=ROOT/'character/bill-meal-contact-audit-v1';P.mkdir(exist_ok=True);OUT=ROOT/'output/bill-meal-counter-contact-candidate-v1'
n=json.loads((OUT/'validation.json').read_text());d=json.loads((OUT/'contacts.json').read_text())
assert n['passed'] and not n['realProfileChanges'] and d['stations']==8 and len(d['captures'])==24
assert {r['station']['facing'] for r in d['captures']}=={'north'}
assert '103 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
h='''# Project handoff

Updated: October1,2026 · BrineSpace · Bill meal actual galley contact audit

## Objective and acceptance
Complete Bill's master-consistent full animation set and full-set polish.
Actual counter audit exposes low authored reaches; meal contact not accepted.

## Accepted decisions and constraints
Owner layout copied into scratch APPDATA, physical service/prop geometry unchanged.
Use actual stations/normal chooser and native grid draw; candidate art injection
is explicit static review, not proof of new pickup/core/return phase dispatch.
Selected master size/proportion/materials remain authoritative; do not enlarge
Bill or relocate counters merely to make hand contact pass.

## Current state
New tests/test_bill_meal_counter_contact_candidates.gd/paired UID and maintained
tools/run_bill_meal_counter_contact_candidate_validation.py. Both N/S candidate
families loaded, actual available stations chosen, reach/hold sources inserted
statically into existing bare eat/drink renderer at unchanged positions.
Owner current layout offers sp-galley-2 at(112,160) and sp-galley-4 at(-112,-80),
both north facing and unchanged across four rotations:8 station cases/24 captures.
No south production contact available, no forced facing or fake rear station.
output/bill-meal-counter-contact-candidate-v1 retains contacts.json, full native
captures and screenshot-detail HTML/PNG. No runtime or art source changes this turn.

## Verification
103native checks PASS42.02s: actual station/prop, can_stand/begin_room_activity,
original6s life_eat, exact staged grid-source selection, fixed contact position
and capture success. All2,914 owner non-log files intact under scratch APPDATA.
Native room captures visually reviewed. Authored waist-level north bowl/cup reach
reads below raised worktop instead of contacting it; navigation/chooser success
does not resolve that visual gap. No numerical hand/worktop acceptance claim.
Both directions' source families previously passed standalone/native loading,
but south contact and actual saved meal phase/interruption/restore unproved.

## Next action
Author north bowl/cup contact reaches for actual counter-height perspective using
these native captures as context and selected master as identity authority. Keep
planted feet/body size and actual service floor; adjust connected forearm/hand
reach rather than prop geometry. Re-review at actual stations before installing
saved meal phases/contact/interrupt/restore proof. South directional coverage is
staged; actual alternate-layout South contact requires separate honest fixture.
West meals/rest/drydeath/inspection broader audits and full-set polish remain.
Goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(h,encoding='utf-8')
note='''
Bill actual galley meal contact audit — October1,2026.
Copied current owner layouts into scratch; normal actual stations/chooser/native
grid draw, explicit static staged source injection (not new phase dispatch).
103native checks PASS42.02s;8stations/24captures across4rotations. Both current
service counters sp-galley-2(112,160)/sp-galley-4(-112,-80) face north; no actual
south contact offered. All2,914 owner non-log files unchanged. Original6s eat
consumer, walkable station, exact staged source and fixed foot position proven.
Visual review contradicts contact acceptance: waist-level north bowl/cup reach
appears below raised counter worktop. Native/player/navigation passes do not
prove hand contact. Do not enlarge Bill or move owner counters to hide mismatch.
Lesson: author reach height in actual room projection before treating standalone
grasp or exact endpoint joins as service-ready. Retain current-layout availability
limits; do not force south facing and claim a production service contact.
Next north contact-source correction at actual counter height, fresh native
station review, then normal saved meal phases/contact/interrupt/diskrestore proof.
South alternate-layout contact remains separate; west/rest/drydeath/inspection
broader audits/full consistency polish remain. Full goal active.
Handoff:character/bill-meal-contact-audit-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill actual galley meal contact audit — October1,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/'HANDOFF.md',OUT/'contacts.json',OUT/'validation.json',OUT/'contact-detail-review.png',OUT/'index.html',ROOT/'tests/test_bill_meal_counter_contact_candidates.gd',ROOT/'tools/run_bill_meal_counter_contact_candidate_validation.py']+[OUT/r['screenshot'] for r in d['captures']]
(P/'audit-evidence.json').write_text(json.dumps({'status':'contact_correction_required','native':n,'checks':103,'stations':8,'captures':24,'scope':d['scope'],'finding':'north authored reaches below worktop; no South station available in current owner layout','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
print('Recorded actual galley contact gap and available north-only layout stations')
