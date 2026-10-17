from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld North complete selected idle and master-based scanner joins — October 3, 2026'
note='## Veld North complete selected idle and master-based scanner joins — October 3, 2026\n\nFresh actual loader ordering/all118manifest bindings and selectedNorth72idle sources\npergear verified. All144idle sources on paired full boards and both endpoint/detail\nboards inspected. Current72idle/78singleaction/72idle chain222/9250ms: suit darkens,\nmagenta edges reappear at idle; helmet changes slightly. Bareidlefloor223/action224,\nhelmetidletop69/action68. SpatialRGB difference30.2..31.3 combines pose/detail/grade,\nnot isolated colour.302sourcebindingschecked,313prior native inputs unchanged.\n\nComparison reuses unchanged existing original-guided four-pose idle and same complete\n78action, bothgears86/6250ms.344source replaychecks0; native353checks0/172presentations,\n8.51s/engine0/no errors/scratchAPPDATA/182inputs unchanged/2931owner nonlogfiles unchanged;\n344native replaychecks0. Both source eight-slot detail boards and paired native\nfour-boundary boards at47/93/148 visually reviewed. Colour/helmet jump much reduced,\nbut hair texture/headwidth/backplate shading/return arm contour still differ.\nHistorical idle per-cell offsets and phase2 clear-box difference explicitly retained:\nthis diagnostic does not newly certify those packaging choices or final artwork.\nNo source painting/normal selection/controller/save change or paid generation.\n\nLesson: test complete CURRENT selected idle around new action and compare a separate\nmaster-based family. Common nominal148height is insufficient when floor/helmet/material\nswitch at state boundaries. Preserve originals and grade evidence rather than forcing\nimproved action to inherit stale idle appearance. Next full fixed-ruler original quiet\nNorth idle/scanner finish, continuous paired joins, cardinal actions and ordinary\ncontroller/contact/Continue plus full-library polish. Fullgoalactive/incomplete.\nHandoff: character/veld-interact-north-original-master-v1/HANDOFF.md.\n\n'
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
