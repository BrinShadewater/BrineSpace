from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_lower_window_v225.py').read_text(encoding='utf-8').replace('lower-window-v225','lower-window-v232')
spec=[(43,226,'0aeb3593-6f54-446f-b0cf-dfb3b7ab0dc0'),(44,227,'b26904b8-ada0-4cb5-8ae4-37ee2a8dc90b'),(45,228,'3f39fd81-e9d4-40cb-ab24-aa7ada0c66d2'),(46,229,'1d52b5ec-a5db-418d-bf65-4859ef4dd5ac'),(47,230,'c8b5cd87-bc56-459a-b62e-ee07a6101dee'),(48,231,'2c3f3300-15df-496a-9a95-8c08cbc024e9')]
a=s.index('for phase,version,execution in ');b=s.index(':\n folder=',a);s=s[:a]+'for phase,version,execution in '+repr(spec)+s[b:]
s=s.replace('[40,41,42]','[43,44,45,46,47,48]').replace('[39,40,41,42,43]','[42,43,44,45,46,47,48]')
s=s.replace('(73,0,5)','(99,0,7)').replace('nativeChecks=73','nativeChecks=99').replace('reviewedNativeCaptures=5','reviewedNativeCaptures=7').replace('checks=73','checks=99').replace('reviewedCaptures=5','reviewedCaptures=7')
s=s.replace("['native-review-0.png','native-review-1.png']", "['native-review-0.png','native-review-1.png','native-review-2.png']").replace('durationsMs=[40]*5','durationsMs=[40]*7')
s=s.replace('Coordinate lower finish43 onward; full49 moving grade/master anatomy/contact/seam, normal lifecycle and all-family consistency','Review full49 current candidates continuously against original master, lower finish start0..3/seam, grade/contact/anatomy; normal lifecycle and all-family consistency')
findings=['Twelve raw/protected and paired source repair boards reviewed before native launch. Ending stride boot angles and ankle positions retained provisionally; close overlapping feet remain distinct.', '95ths43:172.49to156.78;44:178.01to165.99;45:177.12to169.54;46:172.91to162.43;47:166.24to155.95;48:162.57to154.31. Midtones44/45/46 slightly raised;45 strongest remaining highlights. Full moving grade still open.', 'Source window and all seven paired native captures/four sizes reviewed. Alpha/rim/upper body preserved; no continuous full49 flash/seam/contact/master or normal lifecycle acceptance.']
a=s.index('findings=');b=s.index('\nledger=',a);s=s[:a]+'findings='+repr(findings)+s[b:]
section='''### James carrying lower finish ending phases43 to48 - October3,2026

V226phase43/V227phase44/V228phase45/V229phase46/V230phase47/V231phase48
retained provisionally after twelve raw/protected and paired source boards reviewed
BEFORE native launch. Original targets plus original-master material sample used,
no competing pose image. Toe/heel/sole/ankle layout preserved provisionally; closer
ending boots stay distinct.1046/1046/1026/1027/876/723 admitted pixels, remaining
original pixels exact; alpha/rim/above181/paired lower body exact.
Local95ths43:172.49to156.78;44:178.01to165.99;45:177.12to169.54;
46:172.91to162.43;47:166.24to155.95;48:162.57to154.31. Medians43:67.07to64.92;
44:65.85to67.06;45:66.25to69.85;46:65.56to66.71;47:60.36to60.77;
48:63.49to59.21.45 strongest remaining highlights,44/45/46 midtones slightly
raised. Whole-cycle grade acceptance remains open.

V232phase42..48 seven40ms sources280ms:99 native checks/0 failures/7 paired
four-size captures. Source board and all three packed native boards reviewed;
scratch owner profile unchanged, frozen hashes stable. Lesson: occlusion reduces
the lower admission area at47/48; compare actual overlapping toes and ankle
details, not equal brightness statistics or silhouettes as anatomy proof.

Ledger43..48 upgraded fromV157/V158/V160/V161/V163/V164 toV226..V231 with history
preserved;49/49 candidate coverage unchanged. Lower finish refinement now covers
4..48;0..3 lower finish and whole-cycle/seam need review. Next freeze current49
and compare continuous motion with original master for grade, proportions and
physical contact; normal carry lifecycle and all-family consistency/polish remain.
Normal selection unchanged; no final source/full-goal acceptance. Evidence:
character/james-west-carry-walk-keys-v1/lower-window-v232/review.json.
'''
a=s.index('section=');b=s.index('\nguides=',a);s=s[:a]+'section='+repr(section)+s[b:]
s=s.replace("record_guides(r,section,'### James carrying lower finish phases37 to39 independent boot pitch')", "record_guides(r,section,'### James carrying lower finish phases40 to42 wide stride')")
handoff='''# Project handoff

Full master-matched James animation library and all-family polish active/incomplete.
Changed: V226..V231phase43..48 raw/protected paired sources, frozen prompts/material
references; V232seven-frame manifests/APNG/native probe+UID/captures; ledger43..48;
status/pipeline/bible/repository and installed skill references.
Checks:99 native/0/7,280ms original clocks; twelve repair boards and all source/native
captures reviewed; owner profile unchanged, frozen hashes stable. Ending overlapping
boots stay readable;45highlights and44..46midtones remain moving-grade concerns.
Remaining: freeze current49 and continuous full-cycle/master/contact/grade/seam
review; lower finish0..3; versioned normal carrying lifecycle; all-family consistency.
Normal selection unchanged; broad goal remains incomplete.
'''
a=s.index('handoff=');b=s.index('\nfor folder in folders',a);s=s[:a]+'handoff='+repr(handoff)+s[b:]
(p/'close_lower_window_v232.py').write_text(s,encoding='utf-8')
