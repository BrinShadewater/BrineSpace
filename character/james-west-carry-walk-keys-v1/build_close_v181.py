from pathlib import Path
p=Path('character/james-west-carry-walk-keys-v1')
s=(p/'close_lower_window_v178.py').read_text(encoding='utf-8').replace("out=p/'lower-window-v178'", "out=p/'lower-window-v181'").replace("==(86,0,6)","==(73,0,5)")
a=s.index('findings=');b=s.index('\nledger=',a)
s=s[:a]+"findings="+repr(['Both new lower finishes retain readable articulated hardware with less stark toe highlights in four source repair boards, five-frame source board and all five paired native captures/four sizes.', 'Phase13 upper-tail luma176.58to155.96 and median65.50to63.71; phase14 upper-tail175.02to167.90 and median65.28to65.21. Phase13 is more restrained than14; full motion must assess whether this causes a finish jump. Phases15/16 original boots remain brighter.', 'Full original alpha, one-pixel rim, rows above181 and paired body below110 exact. Internal hardware visually assessed; outline preservation does not certify master anatomy.', 'Five-frame20ms each (100ms) finite fixture verified. No continuous full49motion/flash/contact acceptance, normal integration or all-family completion.'])+s[b:]
s=s.replace("[(10,176,'35a29212-a6ea-4673-9710-70d121ff9273'),(11,177,'21a4819b-192f-4422-a1d7-493d0f6023c3')]", "[(13,179,'87ca67f3-1206-4cde-909a-d64aa2bb9493'),(14,180,'635e3907-2f65-47de-8095-8991e864b719')]")
s=s.replace('+[10,11]','+[13,14]').replace('starting13','starting15')
s=s.replace('nativeChecks=86','nativeChecks=73').replace('reviewedNativeCaptures=6','reviewedNativeCaptures=5').replace('sourceIndices=[8,9,10,11,12,13]','sourceIndices=[12,13,14,15,16]').replace('durationsMs=[30,20,20,20,20,20]','durationsMs=[20,20,20,20,20]')
a=s.index("section='''");b=s.index('\nguides=',a)
section='''### James carrying lower finish phases13 and14 neighbour review - October3,2026

V179phase13/V180phase14 retained provisionally after four source repair boards,
V181phase12..16 source board and all five paired native captures/four sizes were
visually reviewed. Toe highlights less stark, hardware readable. Original alpha,
one-pixel rim, rows above181 and paired body below110 exact.1017/1031admitted,
64519/64505outside-exact pixels. Interior hardware receives visual assessment;
alpha preservation is not original-master anatomy acceptance.

Local95thpercentile13:176.58to155.96;14:175.02to167.90. Medians65.50to63.71
and65.28to65.21.13has stronger restraint than14; moving review must determine
whether this creates a finish jump. Original boots15/16 remain brighter.
Lesson: each repair must pass neighbour construction/finish review; preserve
measured differences as open motion risks instead of declaring uniform grading
from reduced highlights. Original master remains authority, phase5 provisional.

V18173checks/0failures/fivecaptures, exact20ms each100ms source window, engine
terminal; scratch APPDATA owner profile unchanged, frozen hashes stable. Ledger
13/14 nowV179/V180, priorV113/V114 preserved;49/49coverage unchanged. Normal
selection unchanged. V173full-cycle evidence is specific to its earlier frozen
sources. Continue coordinated lower finish15and beyond, continuous full gait/
master anatomy/foot contact/flash/seam review, normal carry lifecycle and all-family
consistency/polish. No final source or full-goal acceptance.
Evidence: character/james-west-carry-walk-keys-v1/lower-window-v181/review.json.
'''
s=s[:a]+"section="+repr(section)+s[b:]
s=s.replace("'### James carrying lower finish phase9 neighbour review'", "'### James carrying lower finish phases10 and11 neighbour review'")
a=s.index("handoff='''");b=s.index('\nfor folder',a)
handoff='''# Project handoff

Updated: October3,2026. Goal: full James animation library matching masters,
style/perspective/proportions/grade, followed by all-family consistency/polish.
Goal active; source coverage is not final acceptance.

Accepted constraints: original master authority, matte warm charcoal/yellow/worn
metal, original pose/registration. Preserve owner profile and normal selection.

Changed: V179phase13/V180phase14 raw sources, paired protected candidates,
frozen prompts/references/reviews; V181five-frame manifests/APNG/native probe
and paired UID/captures/evidence; lower helper13/14mappings; ledger; status,
pipeline, bible and repository/installed crew consistency reference.

Checks:73native/0failures/five captures, exact100mswindow, engine0/no timeout,
owner profile unchanged under scratch APPDATA, frozen hashes stable. Four repair
boards, source window and all five native captures/four sizes visually reviewed.
Phase13 highlight reduction stronger than14; moving finish continuity still open.

Remaining: coordinate lower finish15and beyond; continuous full49master anatomy,
contact/flash/seam review; versioned normal pickup/carry/turn/unload lifecycle;
all-family consistency. No normal selection change or continuous-motion acceptance.
V173full-cycle evidence remains frozen to its earlier source versions.
'''
s=s[:a]+"handoff="+repr(handoff)+s[b:]
s=s.replace('retainedPhases=[10,11],checks=86','retainedPhases=[13,14],checks=73').replace('reviewedCaptures=6','reviewedCaptures=5')
(p/'close_lower_window_v181.py').write_text(s,encoding='utf-8')
