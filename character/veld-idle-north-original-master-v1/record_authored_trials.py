from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld North authored breathing strips retain head/grid drift — October 3, 2026'
note='## Veld North authored breathing strips retain head/grid drift — October 3, 2026\n\nChanged authoring route after two head-turn video rejections: built-in imagegen\nwhole four-pose transparent breathing stripsauthored-strip-v4/v5, both referenced\nsame exact768 nearest-enlarged preparedNorth native master. Raw output, exactprompt,\ninputhashes/metadata, fixedgrid diagnostic builders/frames/replays/boards and rejection\nverdicts saved immediately inworkspace. No API fallback or additional MiniMax job.\nAllfour rawposes and same-ruler original comparison viewed for each; generated alpha\npreserved, no local RGB/anatomy edit. Input/raw/prompt hashes reverified.\n\nV4heads rear-facing butnativewidth24vsoriginal22. One sourcegridorigin20/pitch533,\nscale148/602/offset63,58; allH147/floor223, headaxis128.5then127.5. Global sampling\ncalibration could change height/floor, not fix head/bodyratio. V5whole-strip focused\n22/148headwidth instruction stillhead23..24, andnonuniform placement:sourcecentres\n308.5/760.5/1263/1724.5; uniform472pitch residues0/-20/+10.5/0(~-4.70/+2.47native).\nOne fixed sourcegridorigin73,scale148/630,offset73,57 yields148H/floor223butaxis\n128/123.5/130.5/128.5. Both REJECTED; no per-cell recenter/rescale/refloor rescue.\nNo native tests or normal selection/controller/save changes for failedsource art.\n\nLesson: a strip can fix directional head turns yetfail source registration or\nhead/body proportion. Numeric proportion wording is not a guarantee. Evaluate\nuniform grid and original detail atone ruler before packaging/native validation.\nNext reference the actual high-density raw master ratherthannearest-upscaled native\nfor a controlled whole-pose fidelity trial; testthishypothesis, do not claimitfixes\nresults. Then fullquietidle/scanner motion/joins, cardinal actions andordinary\ncontroller/contact/Continue/full-library polish remain. Fullgoalactive/incomplete.\nHandoff: character/veld-idle-north-original-master-v1/HANDOFF.md.\n\n'
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
