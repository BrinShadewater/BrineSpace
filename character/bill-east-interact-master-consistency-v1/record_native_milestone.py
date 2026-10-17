from pathlib import Path
import ast,json,hashlib,subprocess
R=Path.cwd();P=R/'character/bill-east-interact-master-consistency-v1';N=P/'native'
lesson='''\n\n## Bill East interaction native density and inherited loader closure — October 3, 2026

Actual Grid Bill loader plus independent fixture-only staged interaction player:
53 checks, zero failures, six exact source-pose captures at H148/82/54/27.
Timing, six source textures, stateful cursors/restores, finite endpoint and return
to selected idle verified. 3303 bounded inputs and all 2931 owner non-log files
unchanged under scratch APPDATA. New Godot tools retain paired UID files.
All three native pages and corrected current-context board visually inspected:
master definition remains clearer at small sizes, but bright face/ivory hardware
still creates an idle/action material seam. Candidate stays provisional/unselected.
Pivot guides are not world floor/contact, continuous cadence or normal-job proof.

A literal manifest audit missed inherited load_candidates: 26 traced manifest
loads add four carry-start states per gear AND overwrite existing carry sources.
Actual native inventory is 216 bare/198 helmet, versus literal 212/194. Preserve
older audit evidence; bind corrected selected sources to the full inherited load
order. Counts/keys do not prove all selected texture pixels or natural reachability.
The old lifeRows summary is still literal-only, not updated closure authority.
First fixture count failure retained; no runtime change to satisfy wrong assumptions.
Review and provenance: character/bill-east-interact-master-consistency-v1/native/.
Next restrained master/idle material pilot, complete-family joins, actual contact,
natural behavior and checkpoint/titleContinue, then whole-library polish.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:
 for name in ['crew-consistency.md','source-density.md']:paths.append(root/'references'/name)
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(lesson)
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 with path.open('a',encoding='utf-8') as f:f.write(lesson+'\nFull Bill objective remains active/incomplete. Restrained grade pilot prepared from exact extended-arm candidate, original master and selected idle; no selected source/runtime change.\n')
for path in [P/'prepare_grade_pilot.py',R/'tools/run_bill_east_interact_master_native_v1.py']:ast.parse(path.read_text())
for name in ['review_bill_east_interact_master_v1','ensure_bill_east_interact_master_uids']:assert (R/'tools'/f'{name}.gd.uid').exists()
files=[str(x.relative_to(R)).replace('\\','/') for x in P.rglob('*.png')]
r=subprocess.run(['git','check-attr','filter','--',*files],text=True,capture_output=True,check=True);assert all(x.endswith(': filter: lfs') for x in r.stdout.splitlines())
print(f'Six guidance and two project records appended; 2 Python AST, 2 UID pairs, {len(files)} PNG LFS attributes verified.')
