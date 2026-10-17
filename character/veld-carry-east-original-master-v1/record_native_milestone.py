from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld original East traveling gait diagnosis — October 3, 2026'
note='## Veld original East traveling gait diagnosis — October 3, 2026\n\ncharacter/veld-carry-east-original-master-v1/continuous-video-v1 has a paired32-frame\nsource study exercised by actual distance-driven crew_sprite_player at47/93/148,\nthree diagnostic strides96.53/100.13/103.73 source pixels, two cycles each gear.\nCorrected midpoint fixture:2299checks0/396presentations/11.89s;75inputs and all2931\nowner non-log files unchanged under scratch APPDATA. Boundary-sampled first fixture\nmissed frame slots:2275checks64failures retained separately; no art/player changes.\nAll six native gear/stride boards inspected. Sparse native travel replay and browser\nmaster comparison delivered; no complete rigid contact or normal integration proof.\n\nEarly flat-support toe-outline proxy drift0.48-1.23px at93px across the tested distances\nis encouraging but covers only two five-frame windows, not heel/toe roll or every\nnear/far support. No final stride selected.32-frame similarity alone is insufficient.\nDirect five-figure same-scale comparison catches video-induced PURPLE cloth drift:\nstarting V2 key/original-held/true original empty are neutral/olive-grey, video is plum.\nStability within a clip does not establish colour fidelity to its reference.\nV1 retained as motion evidence, not final artwork. Scoped grade-preservation trial\n448379855364450 submitted to continuous-video-v2 using byte-identical original input,\nsame motion wording plus explicit neutral/olive-grey cloth/no-purple instructions.\nEstimatedUSD0.19; billing unverified; exclusive ledger and no automatic paid retry.\n\nLessons: sample authored duration midpoints to exercise every pose; equal clock bins\ncan land on unequal-duration boundaries. Verify physical contact independently of\nplayer phase. Compare the video directly with its unchanged source AND original\nmasters; a stable purple grade can pass all temporal/pixel checks and still be wrong.\nNext review entire grade trial, both-foot material landmarks/loop, final stride,\nauthored start/stop and held handoffs; North contact repair, full original action/\ndirection matrix, ordinary controller/save integration and library polish remain.\nFull objective active/incomplete. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.\n\n'
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
