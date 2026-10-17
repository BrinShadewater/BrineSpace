from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld original East cargo separate visual prop — October 3, 2026'
note='''## Veld original East cargo separate visual prop — October 3, 2026

character/veld-cargo-east-original-master-v3 separates complete floor equipment
from authored contact/release/original-empty body. All12 paired recompositions
exactly equal earlier v2;24build checks0. Same520ms unload/reverse pickup, exact
held entry, now case-free true original East standing idle. Original suit/head/
boot/source density untouched. floor-case.png25x21, offset22,-20 relative128,224;
cargo-contract.json uses full literal texture path and260ms contact/take events.
Staged cargo_prop.gd/.uid owns fixed visual deposit anchor, one event per action,
pickup/delivery retirement and JSON visual snapshot/restore/rejected-state guard.
No ordinary selector, resource credit, world collectible or production integration.

Native1000checks0/142presentations/7.82s in bothgear47/93/148: all14 body slots,
source count/timing/finite tails/root/ruler, stationary case during prescribed70px
body displacement, visual state restore/reject and delivery retirement.65inputs
unchanged and all2931 real owner non-log files unchanged under scratch APPDATA.
142exact native APNG timeline/pixel checks0 (2367ms/gear); earlier42 v2 frozen
inputs still match original hashes. Whole body-only and paired native lifecycle
boards inspected; browser fixed-case/contact/gear/play controls reviewed.

Lessons: a deposited object embedded into idle follows actor root and cannot
represent world placement. Preserve complete authored body and complete equipment
as separate sources, verify recomposition byte-exact before changing lifetime, and
store placement once independently of actor position. Keep visual ownership apart
from gameplay resource credit; caller can retire on existing delivery. A prescribed
standing root-position probe proves anchor independence, never walking/nav/foot
planting. Visual-helper JSON checkpoint is not RunSave/menu Continue acceptance.

Remaining original-master grip/held-to-floor case size, head/boot/contour/material/
helmet pitch and full motion polish; original-faithful East gait/start/stop next,
then turn polish, failed North world walking contact, other directions/full action
matrix, ordinary visual retirement/controller/save integration and library polish.
Full objective active/incomplete. Handoff: character/veld-cargo-east-original-master-v3/HANDOFF.md.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(20):
  with path.open('r',encoding='utf-8') as f:head=''.join(next(f,'') for _ in range(120))
  if title in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-'+uuid.uuid4().hex+'.tmp')
  with tmp.open('wb') as dest,path.open('rb') as source:dest.write(note.encode('utf-8'));shutil.copyfileobj(source,dest,1024*1024)
  after=path.stat()
  if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):tmp.unlink();time.sleep(.5);continue
  try:tmp.replace(path)
  except PermissionError:
   tmp.unlink();time.sleep(.5);continue
  print(path.name,'updated');break
 else:raise RuntimeError('Concurrent updates prevented guarded prepend: '+str(path))
