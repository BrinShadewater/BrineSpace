from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld North complete two-key idle and scanner texture-step review — October 3, 2026'
note='## Veld North complete two-key idle and scanner texture-step review — October 3, 2026\n\nsingle-breath-key-v1/scanner-joins-v1 retains unchanged2realidlekeys/78completefirst\nscanneraction/2idlekeys, paired82/6250ms. No skippedinterior/interpolation orartchanges.\n328source exactreplaychecks0. Nativeactualplayer authoredmidpoint comparison337checks0,\n164presentations/8.15s,engine0/no errors/scratchAPPDATA/335inputs unchanged,\n2931owner nonlogfiles unchanged.328native exactpixel/durationreplaychecks0.\nPaired8slot source detailboards andfourboundary whole nativeboards47/93/148 inspected.\nSamewhole originalrearhelmet staysfixed; boots/ruler retained. Hair/backpanel shading\nandscannerreturnarmcontour stillswitch. Two timedbrowserrest/inhalesnapshots andjoined\nfinalsample reviewed; not fullcontinuousnative scene/controller/contact acceptance.\n\nFixedspatial commonopaque pixels betweenidlekeys:head495/meanRGBMAE5.55/174pixels\nmaxRGBdelta>8;torso2667/MAE9.18/1224above8;legs2367/MAE6.03/695above8. Thesecombine\ngeometry/detail/grade, notpurecolour orphysicalbreathingmeasurements. Changes extend\noutsideuppercloth; observedtexturestep isnotacceptable quietbreath. REJECT final\n2keyquietidle, retain usefulsource/registration study. No normal selection/player/\ncontroller/save edits andno newgeneration thisturn. Initialpreviewencodingerror\ncorrectedUTF8; source/native evidence unaffected.\n\nLesson: a registered original-like key andvalidloop clocks can stillflicker when\nwholegenerated appearance changes betweenkeys. Inspectunchangingregions andcomplete\nidle/actionjoins separately fromheight/pivot/bodybounds. Do notdeclarefinalidlefrom\nstaticnativepass orduplicate/interpolateframes tohide sourceidentityvariation.\nNorth head/material/quietloop defects remain open; proceed acrossremainingoriginal-\nsource directionalactionrepairs(South next) andreturntofull-librarypolish, thenactual\ncontacts/controller/Continue acceptance. Fullgoalactive/incomplete, notblocked.\nHandoff: character/veld-idle-north-original-master-v1/HANDOFF.md.\n\n'
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
