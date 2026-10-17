from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld East video grade trial rejected — October 3, 2026'
note='## Veld East video grade trial rejected — October 3, 2026\n\nGrade-preservation task448379855364450 completed,141 raw frames/all six raw\nchronology boards inspected, same fixed-reference extraction and five-figure\noriginal-master comparison. Added explicit neutral/olive-grey/no-purple wording\nstill yields plum cloth absent from unchanged starting key/held/true empty masters.\nV2 rejected for final art:147-152body/26-27head/223-225floor; no selected loop or\nnative admission. Both source videos/prompts/ledgers retained, no live job remains.\nEarlier native V1 motion sweep2299checks0 remains valid diagnostic playback evidence,\nnot final colour or complete rigid-foot acceptance. No normal selector changes.\n\nLesson: explicit colour-preservation prose alone did not solve two demonstrated\nvideo grade failures. Keep the matched whole source and reject the video drift;\ndo not spend on uncontrolled prompt-only retries or conceal it with body-region\npatches. Next investigate a different whole-source authoring/colour-preservation\napproach, retaining both complete footsteps/physical contact rather than accepting\na smaller easy loop. Source/temporal/native/master fidelity are separate evidence.\nFull scope remains active/incomplete: original-faithful gait/start/stop, North foot\ncontact repair, full original action/direction set, controller/save integration and\ncross-library polish. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.\n\n'
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
