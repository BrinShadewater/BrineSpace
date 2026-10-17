from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'close_lower_window_v232.py').read_text(encoding='utf-8').replace('lower-window-v232','lower-window-v238')
spec=[(0,234,'521585a7-ddfd-406e-8b81-c11de94dc948'),(1,235,'a61539a5-e964-4616-98e8-a516ea191568'),(2,236,'8011e2e3-9112-47e9-bb5f-09bf498767f2'),(3,237,'1f330db9-c9a1-439c-a319-42212552283e')]
a=s.index('for phase,version,execution in ');b=s.index(':\n folder=',a);s=s[:a]+'for phase,version,execution in '+repr(spec)+s[b:]
s=s.replace('[43,44,45,46,47,48]','[0,1,2,3]').replace('[42,43,44,45,46,47,48]','[47,48,0,1,2,3,4]')
s=s.replace('Review full49 current candidates continuously against original master, lower finish start0..3/seam, grade/contact/anatomy; normal lifecycle and all-family consistency','Preserve original phase30 knee anatomy while refining material continuity; current49 continuous master/grade/contact/seam review, normal lifecycle and all-family consistency')
findings=['Eight raw/protected and paired repair boards reviewed before native launch; seven-pose source board and all three native boards now visually reviewed at four sizes for both gears. Opening boot placement and overlapping toes remain readable.', 'Opening lower highlights softened: 95ths0:166.05to155.93;1:172.77to166.18;2:172.27to161.76;3:171.90to166.88. Frames1/3 have small median rises and retain brighter details than neighbouring poses; moving grade remains open.', 'Original alpha/rim/upper body exact and shared lower body preserved. Static seam review does not establish continuous flash-free looping, master proportions or world foot contact.']
a=s.index('findings=');b=s.index('\nledger=',a);s=s[:a]+'findings='+repr(findings)+s[b:]
section='''### James carrying opening lower finish phases0 to3 - October3,2026

V234..V237 phases0..3 retained provisionally after eight raw/protected and paired
source boards reviewed before native launch. Seven-pose source board47/48/0..4
and three native boards visually reviewed for both gears at four sizes.
Original target and original-master material reference used; boot layout remains
readable, with exact alpha/rim/above181 and shared paired body protection.
Admitted pixels698/621/945/1063. Local95ths0:166.05to155.93;
1:172.77to166.18;2:172.27to161.76;3:171.90to166.88. Medians0:63.00to63.64;
1:66.43to68.19;2:63.64to60.85;3:65.28to66.19. Frames1/3 remain brighter in
some details. Lesson: softer peak highlights can coexist with brighter midtones;
judge the actual neighbouring poses in motion rather than peak statistics alone.

V238 seven40ms poses280ms:99 native checks/0 failures/7 paired captures.
Scratch owner profile unchanged; frozen input hashes stable. Ledger0..3 upgraded
fromV167..170 toV234..237 with history preserved. Lower finish refinement now
covers all49 phases, but this is candidate coverage rather than visual acceptance.
Next preserve restored phase30 knee anatomy while refining material continuity,
then current whole-cycle master/grade/contact/seam review, versioned normal cargo
lifecycle and all-family consistency/polish. Normal selection unchanged; full
objective active/incomplete. Evidence: character/james-west-carry-walk-keys-v1/lower-window-v238/review.json.
'''
a=s.index('section=');b=s.index('\nguides=',a);s=s[:a]+'section='+repr(section)+s[b:]
s=s.replace("record_guides(r,section,'### James carrying lower finish phases40 to42 wide stride')", "record_guides(r,section,'### James current49 full-cycle audit identifies seam finish and knee continuity')")
handoff='''# Project handoff

Objective: full master-matched James animation set, then cross-family consistency
and polish. Active/incomplete; normal selection unchanged.
Changed: V234..237 opening lower finish candidates; V238 seven-pose review;
ledger0..3, current status, pipeline, bible and repository/installed skill notes.
Checks:99 native/0 failures/7 captures,280ms original clocks; eight source repair
boards and source/seven native poses visually reviewed; owner profile unchanged,
frozen hashes stable. Original alpha, rim, upper body and paired lower body exact.
Decisions: retain opening finish provisionally; preserve original joint/foot layout.
Remaining: phase30 knee material continuity without anatomical drift; frames1/3
and other highlight variation in full moving grade; master proportions/contact;
normal carrying integration and all-family consistency. No final acceptance.
'''
a=s.index('handoff=');b=s.index('\nfor folder in folders',a);s=s[:a]+'handoff='+repr(handoff)+s[b:]
(p/'close_lower_window_v238.py').write_text(s,encoding='utf-8')
