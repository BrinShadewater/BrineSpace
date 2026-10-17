from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_lower_window_v221.py').read_text(encoding='utf-8').replace('lower-window-v221','lower-window-v225')
s=s.replace("[(37,218,'5a73eed0-2275-4dd5-8544-e1270b5766c7'),(38,219,'b837a1bb-2ce8-4594-a0e4-a525c3414e79'),(39,220,'20b3adff-0b4a-4729-a470-248c898be573')]", "[(40,222,'df389a50-ab11-41f4-ac61-e82e496e75cc'),(41,223,'23dd1940-d3c0-4a3d-8e4b-0e9f9d126740'),(42,224,'2c687cef-fb28-4263-b8e5-6cdd09c52255')]")
s=s.replace('[37,38,39]','[40,41,42]').replace('[36,37,38,39,40]','[39,40,41,42,43]')
s=s.replace('Coordinate lower finish40 onward','Coordinate lower finish43 onward')
findings=['Six raw/protected and paired source boards reviewed before native launch. Wide stride boot angles and toe/heel/ankle arrangement retained provisionally.', '40median68.10to69.28/95th174.15to163.34;41median65.61to62.53/95th168.75to155.07;42median67.56to64.12/95th173.79to163.28. Phase40 midtones slightly brighter,41 more subdued; continuous moving grade acceptance open. Original43 toe highlights brighter.', 'Source window and all five paired native captures/four sizes reviewed. Alpha protection and native clocks do not prove anatomy, physical planting or continuous flash-free motion.']
a=s.index('findings=');b=s.index('\nledger=',a);s=s[:a]+'findings='+repr(findings)+s[b:]
section='''### James carrying lower finish phases40 to42 wide stride - October3,2026

V222phase40/V223phase41/V224phase42 retained provisionally after six raw/protected
and paired source boards reviewed BEFORE native launch. Original target plus
original-master material sample, no competing pose image. Independent sole pitch,
toe/heel and ankle arrangement preserved provisionally.1034/1016/1044 admitted,
64502/64520/64492 outside-exact pixels; alpha/rim/above181/paired body exact.
40median68.10to69.28/95th174.15to163.34;41median65.61to62.53/95th168.75to155.07;
42median67.56to64.12/95th173.79to163.28.40midtones slightly brighter;41more subdued.
Final moving grade and original-master anatomy/contact acceptance remain open.

V225phase39..43 five40ms sources200ms:73 native checks/0 failures/5 paired
four-size captures. Source board and both packed native boards reviewed; scratch
owner profile unchanged, frozen hashes stable. Original43 toe highlights brighter.
Lesson: reducing the brightest reflections may still raise midtones; inspect
both local tone distribution and adjacent source/native views, then full motion.
Do not equate preserved alpha, fixed pivot or green clocks with planted anatomy.

Ledger40/41/42 nowV222/V223/V224, priorV154/V155/V156 preserved;49/49 candidates
unchanged. Next finish43 onward, continuous full49 master/proportions/contact/
grade/seam, normal carrying lifecycle and all-family consistency. Normal selection
unchanged; no full source/goal acceptance. Evidence: character/
james-west-carry-walk-keys-v1/lower-window-v225/review.json.
'''
a=s.index('section=');b=s.index('\nguides=',a);s=s[:a]+'section='+repr(section)+s[b:]
s=s.replace("record_guides(r,section,'### James carrying lower finish phases35 and36 foot separation')", "record_guides(r,section,'### James carrying lower finish phases37 to39 independent boot pitch')")
handoff='''# Project handoff

Full master-matched James animation set and all-family polish active/incomplete.
Changed: V222phase40/V223phase41/V224phase42 raw/protected pairs, frozen prompts/
material references; V225five-frame manifests/APNG/native probe+UID/captures;
ledger40..42; current status/pipeline/bible/repository and installed skill notes.
Checks:73 native/0/5,200ms original clocks; six repair boards and all source/native
captures reviewed; owner profile unchanged, frozen hashes stable.40midtones
slightly brighter,41more subdued, moving grade still open.
Remaining: finish43 onward; continuous full49 master/contact/grade/seam; versioned
normal carrying lifecycle and all-family consistency/polish. Normal unchanged.
'''
a=s.index('handoff=');b=s.index('\nfor folder in folders',a);s=s[:a]+'handoff='+repr(handoff)+s[b:]
(p/'close_lower_window_v225.py').write_text(s,encoding='utf-8')
