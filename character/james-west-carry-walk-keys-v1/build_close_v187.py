from pathlib import Path
import json
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'close_lower_window_v181.py').read_text(encoding='utf-8').replace("out=p/'lower-window-v181'", "out=p/'lower-window-v187'")
a=s.index('findings=');b=s.index('\nledger=',a)
s=s[:a]+"findings="+repr(['Three new lower finishes retain readable articulated hardware with less stark toe/ankle highlights in six selected source boards, five-frame source board and all five paired native captures/four sizes.', 'Phase15 upper-tail175.57to164.29 but median63.71to67.46; phase16 upper-tail176.01to163.05 but median64.28to66.43; selected phase17 upper-tail176.46to162.61 and median65.99to62.83. Midtone consistency/full-motion flashes remain open; phase18 original boots brighter.', 'Phase17 V184 rejected for enlarged/shifted internal boot construction despite preserved original alpha and passing native73checks. V186 remake visually closer to original landmarks; provisional only.', 'Original alpha/one-pixel rim/rows above181/paired body below110 exact for selected sources. Five20ms sources100ms window verified. This is not continuous full49motion/contact, master anatomy, normal lifecycle or all-family acceptance.'])+s[b:]
s=s.replace("[(13,179,'87ca67f3-1206-4cde-909a-d64aa2bb9493'),(14,180,'635e3907-2f65-47de-8095-8991e864b719')]", "[(15,182,'a2833df7-de4b-47c3-b351-5e54e8563652'),(16,183,'e6c55b54-7060-413b-bbd3-501ad570e60e'),(17,186,'283f2f1c-ac6d-4f3b-8fa9-6c5579198202')]")
s=s.replace('+[13,14]','+[15,16,17]').replace('starting15','starting18').replace('sourceIndices=[12,13,14,15,16]','sourceIndices=[14,15,16,17,18]')
a=s.index('section=');b=s.index('\nguides=',a)
section='''### James carrying lower finish phases15 to17 with boot drift rejection - October3,2026

V182phase15/V183phase16/V186phase17 retained provisionally after six selected
source repair boards and V187phase14..18 source board plus all five paired native
captures/four sizes were visually reviewed. Toe/ankle highlights less stark,
hardware readable. Original alpha, one-pixel rim, rows above181 and paired body
below110 exact;1012/1017/1019admitted,64524/64519/64517outside-exact pixels.
Local95thpercentiles15:175.57to164.29;16:176.01to163.05;17:176.46to162.61.
Medians63.71to67.46,64.28to66.43,65.99to62.83. Not uniform grade/flash acceptance.
Original phase18boots still brighter; wider finish coordination remains open.

V184phase17 is REJECTED: raw edit enlarged/shifted internal boot construction.
Protecting original alpha then admitted fragmented/altered interior hardware.
Two rejected source boards reviewed; V18573nativechecks/0failures/fivecaptures
produced but no native visual acceptance. Native boards not visually reviewed.
V186remake explicitly prioritises original toe/heel/ankle landmarks and is visually
closer; internal master anatomy remains unproven. V184never selected in ledger.
Lesson: review raw/crop and protected source boards BEFORE launching a candidate
native window. Alpha/rim protection and green technical checks cannot rescue an
internally moved boot. Preserve rejected provenance; remake from original pose,
never fit/warp displaced limbs into its outline. Original master stays authority.

V18773checks/0failures/fivecaptures, original20ms each100ms finite source window,
engine terminal; scratch APPDATA owner profile unchanged, frozen hashes stable.
Ledger15/16/17 nowV182/V183/V186, priorV116/V117/V119 preserved;49/49candidate
coverage unchanged. Normal selection unchanged. HistoricalV173full-cycle checks
remain specific to their frozen earlier sources. Continue finish18and remaining
gait, continuous full49master anatomy/contact/flash/seam review, normal carry
lifecycle and all-family consistency/polish. No final source/full-goal acceptance.
Evidence: character/james-west-carry-walk-keys-v1/lower-window-v187/review.json.
'''
s=s[:a]+"section="+repr(section)+s[b:]
s=s.replace("'### James carrying lower finish phases10 and11 neighbour review'", "'### James carrying lower finish phases13 and14 neighbour review'")
a=s.index('handoff=');b=s.index('\nfor folder',a)
handoff='''# Project handoff

Updated: October3,2026. Objective: full James master-matched animation library,
then all-family consistency/polish. Goal remains active.

Accepted constraints: master authority; matte warm charcoal/yellow/worn metal;
original pose/registration; preserve owner profile and normal runtime selection.

Changed: V182phase15/V183phase16/V186phase17 raw/protected paired sources,
frozen prompts/references/reviews; rejectedV184/V185evidence; V187five-frame
manifest/APNG/native probe/paired UID/captures/evidence; lower helper mappings;
ledger; current status/pipeline/bible/repository and installed crew skill reference.

Checks: finalV18773native/0failures/five captures,100ms, engine0/no timeout,
scratch owner profile unchanged, frozen hashes stable. Six selected source boards,
five-frame source board and all five paired four-size native captures reviewed.
V184two source boards rejected for boot interior drift; V185technical73/0does
not override source failure, its five native captures were not visually reviewed.

Lesson: source review must precede native-window launch; alpha protection cannot
preserve moved internal joints/boot construction. V186remake closer, provisional.

Remaining: finish18and remaining gait; full continuous49master anatomy/contact/
flash/seam review; versioned normal pickup/carry/turn/unload lifecycle; all-family
consistency. Midtone variation persists. No normal change or final acceptance.
'''
s=s[:a]+"handoff="+repr(handoff)+s[b:]
s=s.replace('retainedPhases=[13,14]','retainedPhases=[15,16,17]')
a=s.index('section=')
rejection='''
rejected=p/'lower-material-phase17-v184';reject_review=json.loads((rejected/'package-review.json').read_bytes())
reject_review.update(disposition='rejected_internal_boot_pose_drift',reviewedSourceBoards=['lower-detail-review.png','paired-lower-review.png'],reason='Generated boot/ankle scale and locations moved; alpha-protected interior no longer preserves original construction.',nativeIncluded=True,sourceAcceptance=False,normalChanged=False)
(rejected/'package-review.json').write_text(json.dumps(reject_review,indent=2)+'\\n',encoding='utf-8')
(rejected/'generation.json').write_text(json.dumps(dict(state='terminal_copied_rejected',execution='a37bf40c-a290-454e-a917-90e12b3f2d9c',rawSha256=sha(rejected/'raw.png'),prompt='prompt.txt',inputs='inputs.json'),indent=2)+'\\n',encoding='utf-8')
failed=p/'lower-window-v185';fn=json.loads((failed/'native-evidence.json').read_bytes());fv=json.loads((failed/'native_probe-validation.json').read_bytes())
assert (fn['checks'],fn['failures'],fn['captures'])==(73,0,5) and fv['realProfileUnchanged'] and fv['exitCode']==0 and not fv['timedOut']
(failed/'review.json').write_text(json.dumps(dict(disposition='source_rejected_before_native_visual_review',checks=73,failures=0,capturesProduced=5,reviewedNativeCaptures=0,reason='V184internal boot drift; technical pass does not establish art quality.',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\\n',encoding='utf-8')
folders += [rejected,failed]
'''
s=s[:a]+rejection+s[a:]
(p/'close_lower_window_v187.py').write_text(s,encoding='utf-8')
