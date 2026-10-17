from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld North scanner occlusion and corrected native validation — October 3, 2026'
note='## Veld North scanner occlusion and corrected native validation — October 3, 2026\n\nTwo original-master input source trials retained. First142 source rejected because\nhands/scanner cross rear panels. Focused retake142/5917ms keeps hands in front and\nback panels unobstructed, but performs two actions. Full source retained; contiguous\nfirst0..77/78poses/3250ms includes complete raise/operate/lower/rest, no interior\nomission or local anatomy/RGB repair. Original North has magenta edge contamination;\nprepared cleanup input remains separately identified, not pixel-identical original.\nFrozen scale1/3/offset0, darkalpha tolerance8/components>=20/noerosion. Each source\n710checks0; fixed whole rear34x36 shell000 at112,68/clear115,77,143,103, body outside\nfit exact. SourceH148..149/top76..77/floor224; controlH149/top76/floor224; head23..24\nversuscontrol22 remains a proportion difference. Two trials estimatedUSD0.56,\nbillingunverified; no new paid generation in corrected validation turn.\n\nPreserved failed native v1:739checks/158failures, distinct ImageTexture objects\nloaded independently for identical files compared by object identity. New v2 checks\nclock against own state bank and source pixel data across states:895checks0,\n284presentations/11.41s,engine0/no logged errors/scratchAPPDATA/313inputs unchanged,\n2931owner non-log files unchanged. No production player or art change. Complete\nnative142 paired replay568pixel/durationchecks0. All six native chronology boards\nand whole bare0/bare35/helmet77 at47/93/148 beside untouched original/prepared/current\nidle visually reviewed. Back panels clear, helmet fixed; raised elbows spread wide.\nFabric/detail/finish, modest head width difference, continuous motion and complete\nidle joins remain open. Source/native midpoint evidence is not ordinary integration.\n\nLesson: separately loaded texture instances are not source identity. Validate clock\nselection within the loaded state and compare actual image data across states.\nA repeated source cannot satisfy a single-action timeline merely because endpoints\nmatch; retain full evidence and explicitly author a complete contiguous cycle.\nStaged only, no normal selection/controller/save changes. Next full continuous\nmotion/material and selected idle join review, cardinal actions and full-library\ncontroller/contact/save/polish. Full objective active/incomplete.\nHandoff: character/veld-interact-north-original-master-v1/HANDOFF.md.\n\n'
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
