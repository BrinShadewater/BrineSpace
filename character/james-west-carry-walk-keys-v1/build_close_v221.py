from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_lower_window_v217.py').read_text(encoding='utf-8').replace('lower-window-v217','lower-window-v221')
s=s.replace("[(35,215,'3f8dc846-d256-48d7-ba6e-6701ab6663e9'),(36,216,'987c4f87-ef76-405b-8963-be00f91a92cd')]", "[(37,218,'5a73eed0-2275-4dd5-8544-e1270b5766c7'),(38,219,'b837a1bb-2ce8-4594-a0e4-a525c3414e79'),(39,220,'20b3adff-0b4a-4729-a470-248c898be573')]")
s=s.replace('[35,36]','[37,38,39]').replace('[33,34,35,36,37]','[36,37,38,39,40]')
s=s.replace('Coordinate lower finish37 onward','Coordinate lower finish40 onward')
findings=['Six raw/protected and paired source boards reviewed before native launch; each separated boot retains its own pitch, toe/heel and ankle layout provisionally.', 'Local median/95th:37 68.50to65.41/174.31to165.08;38 66.56to61.64/177.44to158.05;39 67.31to63.64/177.99to163.36. Phase38 somewhat more subdued than37/39; continuous moving grade acceptance remains open. Original40 toe highlights brighter.', 'Source window and all five paired native captures/four sizes reviewed. Alpha/rim protection is not anatomy/contact/master or continuous motion acceptance.']
a=s.index('findings=');b=s.index('\nledger=',a);s=s[:a]+'findings='+repr(findings)+s[b:]
section='''### James carrying lower finish phases37 to39 independent boot pitch - October3,2026

V218phase37/V219phase38/V220phase39 retained provisionally after six raw/protected
and paired source boards reviewed BEFORE native launch. Original pose plus original
master material sample used; other-pose finish reference omitted from generation.
Each boot preserves its independent sole angle, toe/heel and ankle arrangement.
1012/994/1034 admitted,64524/64542/64502 outside-exact pixels; alpha/rim/above181/
paired lower body exact.37median68.50to65.41/95th174.31to165.08;38median66.56to
61.64/95th177.44to158.05;39median67.31to63.64/95th177.99to163.36.38somewhat more
subdued than37/39; moving grade still open. Original40 toe highlights brighter.

V221phase36..40 five40ms sources200ms:73 native checks/0 failures/5 paired
four-size captures; source board and both packed native boards visually reviewed.
Scratch owner profile unchanged; frozen hashes stable. Lesson: as the leading
toe lifts, evaluate boot pitch independently from torso scale; compare adjacent
pose hardware and native-size finish, not equal luma statistics across masks.
Alpha preservation cannot certify internal landmarks, original-master anatomy or
physical contact. Whole-cycle visual review is still required for colour flashes.

Ledger37/38/39 nowV218/V219/V220; priorV150/V151/V152 preserved;49/49 candidate
coverage unchanged. Next lower finish40 onward, full49 master/proportions/contact/
moving grade/seam, normal carrying lifecycle and all-family consistency. Normal
selection unchanged; no full source/goal acceptance. Evidence: character/
james-west-carry-walk-keys-v1/lower-window-v221/review.json.
'''
a=s.index('section=');b=s.index('\nguides=',a);s=s[:a]+'section='+repr(section)+s[b:]
s=s.replace("record_guides(r,section,'### James carrying phase34 geometry-preserving finish remake')", "record_guides(r,section,'### James carrying lower finish phases35 and36 foot separation')")
handoff='''# Project handoff

Full James master-matched animation set and all-family polish active/incomplete.
Changed: V218phase37/V219phase38/V220phase39 raw/protected pairs, frozen prompts/
material references; V221paired five-frame manifest/APNG/native probe+UID/captures;
ledger37..39; status/pipeline/bible/repository and installed skill reference.
Checks:73 native/0/5,200ms original window, six repair boards and all source/native
captures reviewed; owner profile unchanged; frozen hashes stable. Each boot pitch
retained provisionally,38finish more subdued than neighbours.
Remaining: finish40 onward; continuous full49 master/contact/grade/seam, versioned
normal carrying lifecycle, cross-family consistency/polish. Normal unchanged.
'''
a=s.index('handoff=');b=s.index('\nfor folder in folders',a);s=s[:a]+'handoff='+repr(handoff)+s[b:]
(p/'close_lower_window_v221.py').write_text(s,encoding='utf-8')
