from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'close_lower_window_v181.py').read_text(encoding='utf-8').replace("out=p/'lower-window-v181'", "out=p/'lower-window-v191'")
a=s.index('findings=');b=s.index('\nledger=',a)
s=s[:a]+"findings="+repr(['Three selected lower repairs retain readable boot/ankle construction with less stark highlights in six source repair boards, five-frame source board and all five paired native captures/four sizes. Source review preceded native launch.', 'Phase18 upper-tail177.29to158.79/median64.36to62.91; phase19 upper-tail173.98to166.92/median63.99to63.71; phase20 upper-tail176.26to164.18/median65.36to66.50. Phase18 is more restrained than19; moving grade continuity remains open. Phase21 original boots brighter.', 'Original alpha/one-pixel rim/rows above181/paired body below110 exact. Internal hardware visually assessed; protected outlines do not prove master anatomy or proportions.', 'Five20ms sources100ms finite fixture verified. No continuous full49motion/no-flash/contact acceptance, normal carry lifecycle or all-family completion.'])+s[b:]
s=s.replace("[(13,179,'87ca67f3-1206-4cde-909a-d64aa2bb9493'),(14,180,'635e3907-2f65-47de-8095-8991e864b719')]", "[(18,188,'a5e65cf2-c350-4aa3-a2c5-a2c20ea2e461'),(19,189,'b9f0056e-14ac-4913-89c1-13e2c4b11139'),(20,190,'6e369a8e-22d8-4cfd-bd15-4bf9f89e7be2')]")
s=s.replace('+[13,14]','+[18,19,20]').replace('starting15','starting21').replace('sourceIndices=[12,13,14,15,16]','sourceIndices=[17,18,19,20,21]')
a=s.index('section=');b=s.index('\nguides=',a)
section='''### James carrying lower finish phases18 to20 neighbour review - October3,2026

V188phase18/V189phase19/V190phase20 retained provisionally after six source
repair boards were visually reviewed BEFORE native window launch. V191phase17..21
source board and all five paired native captures/four sizes then visually reviewed.
Boot/ankle construction remains readable with less stark highlights. Original alpha,
one-pixel rim, rows above181 and paired body below110 exact;1029/1023/1033admitted,
64507/64513/64503outside-exact pixels. Interior geometry remains a visual assessment,
not protected original-master landmarks or final anatomy/proportion acceptance.

Local95thpercentiles18:177.29to158.79;19:173.98to166.92;20:176.26to164.18.
Medians64.36to62.91,63.99to63.71,65.36to66.50.18has stronger restraint than19;
full moving review must assess finish continuity. Original phase21boots brighter.
Lesson: preserve source-first review after V184rejection; compare raw boot/ankle
landmarks and protected hardware before engine work. Outline protection cannot
rescue internal pose drift. Upper-tail reductions are diagnostics, not uniform
grading/flash acceptance. Original master authority; phase5finish provisional.

V19173checks/0failures/fivecaptures, original20ms each100ms finite source window,
engine terminal; scratch APPDATA owner profile unchanged, frozen hashes stable.
Ledger18/19/20 nowV188/V189/V190, priorV120/V122/V123 preserved.49/49candidate
coverage unchanged. Normal selection unchanged. V173full-cycle evidence remains
specific to its earlier frozen sources. Continue lower finish21and remaining gait,
continuous full49master anatomy/contact/flash/seam review, normal carrying lifecycle
and all-family consistency/polish. No final source/full-goal acceptance.
Evidence: character/james-west-carry-walk-keys-v1/lower-window-v191/review.json.
'''
s=s[:a]+"section="+repr(section)+s[b:]
s=s.replace("'### James carrying lower finish phases10 and11 neighbour review'", "'### James carrying lower finish phases15 to17 with boot drift rejection'")
a=s.index('handoff=');b=s.index('\nfor folder',a)
handoff='''# Project handoff

Updated: October3,2026. Objective: full James master-matched animation set,
then all-family consistency/polish. Goal active; coverage is not acceptance.

Accepted constraints: original master authority; matte warm charcoal/yellow/worn
metal; original pose/registration; preserve owner profile and normal selection.

Changed: V188phase18/V189phase19/V190phase20 raw/protected paired sources,
frozen prompts/references/reviews; V191five-frame manifests/APNG/native probe
and paired UID/captures/evidence; lower helper18..20mappings; ledger; status,
pipeline, bible and repository/installed crew consistency reference.

Checks:73native/0failures/fivecaptures,100ms, engine0/no timeout, scratch profile
owner unchanged, frozen hashes stable. Six source repair boards reviewed BEFORE
native launch; five-frame source board and all five native captures/four sizes
reviewed. Original alpha/rim/upper rows preserved; hardware visually assessed.

Remaining: finish21and beyond; moving grade continuity (18darker than19), full49
master anatomy/contact/flash/seam review, versioned normal carry lifecycle and
all-family consistency. No normal selection change or continuous acceptance.
V173full-cycle evidence remains frozen to its earlier source versions.
'''
s=s[:a]+"handoff="+repr(handoff)+s[b:]
s=s.replace('retainedPhases=[13,14]','retainedPhases=[18,19,20]')
(p/'close_lower_window_v191.py').write_text(s,encoding='utf-8')
