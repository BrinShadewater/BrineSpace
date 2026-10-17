from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld South original-master scanner source and native review — October 3, 2026'
note='## Veld South original-master scanner source and native review — October 3, 2026\n\nRebuilt South scanner from byte-identical original native South master, uniformly\n3x nearest on dark12/18/24; identical first/last endpoints. MiniMax task\n448629913780717 Success, complete142poses/5917ms retained. EstimatedUSD0.28,\nbilling unverified. Raw source, exact prompt, provenance and immutable inputs saved.\nFixed1/3registration offset0; alpha tolerance8/components20/no erosion or RGB edits.\nOriginal master H148/floor224/head24; input alpha control H149/head23.\nSource H146..149/floor224/head22..24/axis128..130, consistent with downward glance.\nWhole original front35x39helmet at11069/clear11177143102, outside fit body exact.\n710 source/replay checks0. Actual player midpoint native577checks0/284presentations\nat47/93/148,11.03s/engine0;311inputs and2931owner non-logfiles unchanged under\nscratchAPPDATA. Native replay568pixel/durationchecks0. All six raw chronology boards,\nmaster/control comparison, six native paired chronology boards and two whole native\nthree-scale comparisons visually inspected. No complete continuous scene acceptance.\n\nOne complete draw/inspect/stow action retained without omitted interior poses.\nSTAGED NOT FINAL: scanner screen flashes cyan/green/yellow; draw originates viewer-left\nbelt while original tool pouch is viewer-right; subtle face/fabric/detail variation\nremains. Fixed original helmet face does not follow bare downward head motion, so\npaired helmet is appearance evidence only. Current selected bare idle looks darker/\ncooler beside original/candidate; actual full idle/action joins still required.\nNo normal runtime selection/controller/save edits. Preview index.html preserves full\nsource video and paired APNGs. Native checks certify loading/clocks/protection,\nnot prop identity, anatomical gear motion, finished grade or owner acceptance.\n\nLesson: unchanged endpoint/ruler and stable helmet construction cannot certify prop\nside, display brightness or helmet head motion. Compare asymmetric belt equipment\nand paired action semantics across the whole source before expansion/adoption.\nNext whole-source South refinement for correct pouch and subdued constant display,\nhelmet-motion validation and complete joins; North quiet idle remains rejected for\ntexture step. Full directional actions, contacts/controller/Continue and library\nconsistency/polish remain. Full goal active/incomplete.\nHandoff: character/veld-interact-south-original-master-v1/HANDOFF.md.\n\n'
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
