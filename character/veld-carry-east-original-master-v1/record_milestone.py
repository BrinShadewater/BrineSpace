from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld original East gait source study — October 3, 2026'
note='## Veld original East gait source study — October 3, 2026\n\ncharacter/veld-carry-east-original-master-v1 retains rejected oversized V1 atlas,\nselected original-only six-key V2 foundation, and completed MiniMax task448373312799191.\n141 raw video frames extracted with ONE original-guided scale0.2073976222 and fixed\nplate offset53,46; no per-frame resizing, floor correction or body RGB grading.\nAll raw and extracted chronological boards inspected: head26 throughout, body147-150,\nfloor222-224. Upper body/equipment visibly stable; final master-grade fidelity pending.\n\nProvisional consecutive raw32..63 paired study uses original whole profile shell,\n32 frames/1333ms per gear.160 source protection/clipping/exact APNG replay checks0.\nThis is SOURCE evidence, not native playback or a completed traveling gait.\nLower-body recurrence favors32 over16 frames, but cannot establish near/far identity.\nTwo inspected support-band centroid fits imply different travel96.53/103.73 pixels\nper32 frames, with residual spans6.03/5.74px. Rolling boot silhouette centroid is\nnot a rigid sole landmark; no stride calibrated or world-contact acceptance claimed.\n\nLessons: old motion references can contaminate identity despite guide-only wording;\nuse original-only full-character references for new gait sources. Similarity and\nbottom-alpha centroids cannot prove a complete two-step cycle or stationary soles.\nKeep full raw chronology, fixed registration and explicit contact windows; track\nphysical landmarks and verify actual distance-driven playback before gait admission.\n\nNext: identify near/far boots and stable sole landmarks across both supports, inspect\nloop temporally, calibrate measured stride, then native/world walking at47/93/148,\nauthored start/stop and exact held/idle handoffs. North contact failure, other directions,\nfull action coverage, normal controller/save integration and cross-library polish remain.\nFull objective active/incomplete. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.\n\n'
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
