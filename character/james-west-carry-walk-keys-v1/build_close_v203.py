from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'close_lower_window_v181.py').read_text(encoding='utf-8').replace("out=p/'lower-window-v181'", "out=p/'lower-window-v203'").replace('==(73,0,5)','==(86,0,6)')
a=s.index('findings=');b=s.index('\nledger=',a)
s=s[:a]+"findings="+repr(['Four selected repairs retain readable toe/ankle hardware and distinct overlapping boots in eight source repair boards, six-frame source board and all six paired native captures/four sizes. Source review preceded native launch.', 'Phase25upper-tail174.30to161.72/median63.35to63.50;26upper-tail175.65to163.77/median65.50to64.78;27upper-tail175.11to168.21/median66.00to68.44;28upper-tail174.19to156.96/median65.35to63.99. Phase28more restrained than27; moving grade continuity remains open. Phase29original toe highlights brighter.', 'Original alpha/one-pixel rim/rows above181/paired body below110 exact. Interior landmarks visually assessed; preserved outlines do not prove original-master anatomy/contact acceptance.', 'Six40ms sources240ms finite fixture verified. Not continuous full49motion/no-flash/seam, normal carry lifecycle or all-family completion.'])+s[b:]
s=s.replace("[(13,179,'87ca67f3-1206-4cde-909a-d64aa2bb9493'),(14,180,'635e3907-2f65-47de-8095-8991e864b719')]", "[(25,199,'b46373c3-ba83-4872-b68b-49e8d60e4019'),(26,200,'91e035f9-90e6-4fc7-ad93-2c8287b9d67f'),(27,201,'946e8d50-4506-4577-8b25-61f24ac005bc'),(28,202,'9991e4fe-9746-44c3-9b9d-91731eb57678')]")
s=s.replace('+[13,14]','+[25,26,27,28]').replace('starting15','starting29').replace('nativeChecks=73','nativeChecks=86').replace('reviewedNativeCaptures=5','reviewedNativeCaptures=6').replace('sourceIndices=[12,13,14,15,16]','sourceIndices=[24,25,26,27,28,29]').replace('durationsMs=[20,20,20,20,20]','durationsMs=[40,40,40,40,40,40]')
a=s.index('section=');b=s.index('\nguides=',a)
section='''### James carrying lower finish phases25 to28 overlap review - October3,2026

V199phase25/V200phase26/V201phase27/V202phase28 retained provisionally after
eight source repair boards reviewed BEFORE native launch. V203phase24..29 source
board and all six paired native captures/four sizes visually reviewed. Overlapping
boots remain distinct with readable ankle straps and less stark toe highlights.
Full original alpha, one-pixel rim, rows above181 and paired body below110 exact;
1030/1026/1000/927admitted,64506/64510/64536/64609outside-exact pixels.
Internal hardware landmarks receive visual assessment, not master anatomy proof.

Local95thpercentiles25:174.30to161.72;26:175.65to163.77;27:175.11to168.21;
28:174.19to156.96. Medians63.35to63.50,65.50to64.78,66.00to68.44,65.35to63.99.
28more restrained than27; moving grade continuity remains open. Original29toe
highlights brighter. Lesson: close limb overlap shrinks the admitted mask; compare
actual toe/heel/ankle construction and finish at native sizes rather than treating
statistics from different masks as equivalent material samples. Source-first
review remains required; alpha cannot preserve shifted interior joints. Original
master authority and provisional phase5finish reference roles remain distinct.

V20386checks/0failures/sixcaptures, exact40ms each240msfinite window, engine
terminal; scratch APPDATA owner profile unchanged, frozen hashes stable. Ledger
25..28 nowV199/V200/V201/V202, priorV131/V132/V133/V135 preserved;49/49candidate
coverage unchanged. Normal selection unchanged. V173full-cycle evidence remains
specific to its earlier frozen sources. Continue lower finish29and beyond, moving
grade21/27to28, full49master anatomy/contact/flash/seam review, normal carrying
lifecycle and all-family consistency/polish. No final source/full-goal acceptance.
Evidence: character/james-west-carry-walk-keys-v1/lower-window-v203/review.json.
'''
s=s[:a]+"section="+repr(section)+s[b:]
s=s.replace("'### James carrying lower finish phases10 and11 neighbour review'", "'### James carrying lower finish phases21 to24 with neighbour remake'")
a=s.index('handoff=');b=s.index('\nfor folder',a)
handoff='''# Project handoff

Updated: October3,2026. Objective: full master-matched James animation library,
then all-family consistency/polish. Goal active; coverage is not final acceptance.

Accepted constraints: original master authority, matte charcoal/yellow/worn metal,
original pose/registration; preserve owner profile and normal runtime selection.

Changed: V199phase25/V200phase26/V201phase27/V202phase28 raw/protected paired
sources, frozen prompts/references/reviews; V203six-frame manifests/APNG/native
probe/paired UID/captures/evidence; helper mappings; ledger; current status,
pipeline, bible and repository/installed crew consistency reference.

Checks:86native/0failures/six captures,240msoriginal clocks, engine0/no timeout,
scratch owner profile unchanged, frozen hashes stable. Eight source repair boards
reviewed before native launch, source window and all six paired captures/four sizes
reviewed. Overlapping boots remain distinct;28finish more restrained than27.

Remaining: finish29onward, moving grade21and27/28; continuous full49master
anatomy/contact/flash/seam review; versioned normal pickup/carry/turn/unload
lifecycle and all-family consistency. No normal selection change or continuous
acceptance. V173full-cycle evidence remains frozen to its earlier source versions.
'''
s=s[:a]+"handoff="+repr(handoff)+s[b:]
s=s.replace('retainedPhases=[13,14],checks=73','retainedPhases=[25,26,27,28],checks=86').replace('reviewedCaptures=5','reviewedCaptures=6')
(p/'close_lower_window_v203.py').write_text(s,encoding='utf-8')
