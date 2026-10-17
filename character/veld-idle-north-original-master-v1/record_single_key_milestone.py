from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld North high-density reference and whole single-breath key — October 3, 2026'
note='## Veld North high-density reference and whole single-breath key — October 3, 2026\n\nBuilt-in authored-strip-v6-high-density changes only V4 reference toactual raw-clean\nmaster, exactsameprompt. Allfourraw andfixedgrid mastercomparison inspected. Uniform\nsourcepitch516.67residues0/.33/.67/0; frozenintegergridorigin6/pitch517, calibrated\nonefirst-pose148ruler scale164/756offset72,69. ALLnativeH148/top77/floor224/head24/\naxis127.5. Detailedquilting/grid improved; headratio stillfailsoriginal22/128.5.\nREJECTED finalidle; original/generatedraw/prompt/provenance preserved.\n\nChanged layoutstrategy toONE whole source inhale edit ofactual raw-cleanmaster:\nsingle-breath-key-v1. Exactoldscale148/1109offset44,66, unchangedwhole generatedRGBA\napartfromresampling. NativeH148/top77/floor224/left97/right159matchrest; head23/129\nvsoriginal22/128.5.641head/6453wholeRGBApixels differ; commonRGBMAE7.51includes\npose/detail/grade, notpurecolour.2actualrealkeys(preparedmasterrest+inhale),750mseach;\nno interpolation, inventedduplicatesorlocalanatomy/grade corrections. Fixedwhole\nrear34x36helmetat112,68/clear115,77,143,103; outsidefitbodyexact.\n\nFailednative17checks2 preserved: fixture mistakenlyexpectsframe_at_elapsedto loop;\nthatmethod intentionallyclampssimulation-driven elapsed. Newv2tests clampedmethod\nandactualcosmeticframepath across5times/bothgears:27checks0/4presentations/5.62s,\nengine0/no errors/scratchAPPDATA/28inputs unchanged/2931owner nonlogfiles unchanged.\n8native replaychecks0. Allfour native47/93/148 original/prepared/currentidlecomparison\nviews inspected. No productionplayer/art/normal selection/controller/save edits.\nPrepared two-key candidate isSTUDYONLY; head/detailchanges andsteppedflicker/complete\ncontinuousmotion/scannerjoins remain unresolved. Native replay != sceneacceptance.\n\nLesson: highdensitysource helpsdetail/grid butdidnotfixheadratio. Singlewholepose\nedit retainscommonruler betterthanrepeatedstriplayout butstillchangesprotected\nappearance. Separateclampedelapsed sampler from cosmeticloop API in native tests.\nNext continuous two-key flicker and completeNorthscannerjoins atactualscale, refine\nsource ifneeded; othercardinalactions/ordinarycontacts/controller/Continue/full-library\nfidelity/polish remain. Fullgoalactive/incomplete.\nHandoff: character/veld-idle-north-original-master-v1/HANDOFF.md.\n\n'
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
