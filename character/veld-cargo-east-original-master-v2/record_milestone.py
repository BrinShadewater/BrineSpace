from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld original East cargo shared-case draft — October 3, 2026'
note='''## Veld original East cargo shared-case draft — October 3, 2026

character/veld-cargo-east-original-master-v2 packages paired six-pose520ms unload/
reverse pickup with exact original held entry and whole original empty East body
exit. Whole atlasV4 and independent no-case deep body retained with exact prompts;
intermediate deep/contact edit rejected for changing case size. Same complete
deposited equipment25x21 (opaque23x19) at150,204/ground223 reused behind whole
character in contact/release/standing. No RGB/limb/body-region corrections or
per-pose atlas scaling. One atlas ruler0.2361878453/Y66; independent complete deep
source density follows actual matching crouch81, not standing148. Head26/27/27/28/
27/27; small silhouette/material differences remain. Whole original helmet fits
follow head; body outside fitting protected. Staged idle includes floorcase only
for chronology; normal selectors unchanged, ordinary prop ownership not solved.

18 build/13 source checks0. Native605checks0/108presentations/6.78s at47/93/148,
counts/timing/finite tail/exact joins/root/ruler,42inputs unchanged and2931 real
owner non-log files unchanged under scratch APPDATA.108 exact APNG native replay
pixel checks0; raw/source/native action boards inspected, browser bare cycle3,
contact500ms and helmet cycle33/released600ms observed. Initial native board crop
showed master row; corrected to actual action row before review. No ordinary
controller/world case lifetime/save/final smoothness or owner acceptance claimed.

Lessons: isolate each anatomical boot from props before registering complete
source. Atlas near residual0.458px/Ydrift0/far toeXspan0 does not survive unchanged
after new deep source and exact original endpoints: final nearXspan2.333px and
allfloors223. Source coordinates/resampling and occlusion affect contact proxies;
fixed root or standing ruler cannot prove anatomical/world planting. Reuse complete
equipment with a complete empty-hand character to remove object identity drift,
without painting over anatomy; inspect grip/occlusion and physical held-to-floor
size separately. Metric/pixel checks cannot certify identity, matte grade or motion.

Next full unload/pickup grip/contour/material/helmet-pitch polish and case ownership;
then remaining original-faithful East actions, turn polish, failed North walking
contacts, other directions/full action matrix, ordinary integration and cross-library
polish. Full objective active/incomplete. Handoff: character/veld-cargo-east-original-master-v2/HANDOFF.md.

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
  tmp.replace(path);print(path.name,'updated');break
 else:raise RuntimeError('Concurrent updates prevented guarded prepend: '+str(path))
