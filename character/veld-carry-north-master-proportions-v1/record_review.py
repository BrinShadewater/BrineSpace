from pathlib import Path
import json,os,shutil,time
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-carry-north-master-proportions-v3'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));e=json.loads((P/'motion-review-evidence.json').read_text(encoding='utf-8'));assert v['passed'] and e['sourceNativePairs']==104 and e['decodedNativeFramesExact']==104
e['visualReview']='Raw v1/v2 rejected support-leg repetition; raw v3 and registered paired/master board inspected. Final four chronological native/source boards reviewed,104pairs, plus full helmet0native at47/93/148sizes. Balanced3+3source with landings improves gait and slimmer master body. Continuous in-room cadence, exact held joins and head/material polish remain.'
(P/'motion-review-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
reg=json.loads((P/'registration.json').read_text(encoding='utf-8'));reg['visualReview']=e['visualReview'];(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
block="""## Veld whole North carrying gait follows the original master — October 2, 2026

New staged character/veld-carry-north-master-proportions-v1 pairs six whole
rear-facing carry poses with unchanged original33x35North helmet. Original North
identity reference and exact held body are authorities; cargo naturally hidden
in front, teal device screenleft/triplecanisters screenright, no mirroring.
Builtin rawv1 4f41aba5 rejected imbalanced support sequence despite633passing
playback checks; v2 4e1ef872 also repeated support late. Whole-source edit v3
 d527dcb3 corrects fifth/sixth poses: two3pose support/lift/passing/landing halves.
Raw3candidates/prompts/reference hashes retained; v1 packaged rejection preserved.

One firstcontact148ruler .23604465709728867 and global source bootfloor; whole
skull-axis128 translations, not warm collar/bolt pixels, remove2pxfitting drift.
All six original33x35shell positions11268; fixed scale/grade, bounded head fit,
body outside fitting bounds exact. Shared West material recipe, protected hip
hardware, no procedural body bands/per-pose scale. Registered nativeH149/head24-25
vs canonical heldH147/head23; this small residual and material/contact remain polish.
Original six140ms840cycle/stride .0827027027027027/dry/depth0 metadata retained.

Build56checks0. Final nativev3 633checks0/104presentations6.91s/30inputs unchanged;
all2931owner non-log files unchanged with scratchAPPDATA. Four chronological
source/native boards104pairs and fullhelmet0native seen at47/93/148display sizes;
104lossless native APNG frames decodeexact. Raw and master comparisons reviewed.
No normal adoption, authored firststep/stop, real North route or wholecontinuous
cadence acceptance. Next North master-held-to-gait start/stop, South equivalent,
then guarded normal cargo/Continue/traffic/fire/flood/case lifecycle; North idle,
furniture/swimming/full-library consistency/polish remain. Full goal active.
Lesson: a six-slot technically valid row may still repeat the wrong support leg.
Specify two explicit halfcycles, inspect support/landings and loop order, repair
whole source through imagegen; use skull silhouette for registration instead of
warm collar fasteners. Passing source selection tests does not establish gait.
Handoff: character/veld-carry-north-master-proportions-v1/HANDOFF.md.

"""
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 st=p.stat();tmp=p.with_name(p.name+'.veld-north-gait.tmp')
 with tmp.open('wb') as dst,p.open('rb') as src:dst.write(block.encode('utf-8'));shutil.copyfileobj(src,dst,1024*1024)
 assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns,'Concurrent reference update'
 for attempt in range(5):
  try:os.replace(tmp,p);break
  except PermissionError:
   if attempt==4:raise
   time.sleep(.2)
(P/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 2, 2026 · Project: BrineSpace · Task: North carrying master gait\n\n## Objective and acceptance\nFull master-matched Veld animation library followed by cross-library consistency/polish. Active/incomplete.\n\n## Accepted decisions and constraints\nOriginal North master authority; whole source, one ruler/global floor, asymmetric equipment, original shell, shared grade, scratch saves.\n\n## Current state\nThree raw source versions/provenance, rejected v1 package, final paired frames/manifests/APNGs and registered master comparison. New test+UID/runner and native boards. No normal selection changes.\n\n## Verification\n'+block+'## Next action\nMaster-held North firststep/stop, South sources, guarded production cargo/Continue/traffic/fire/flood/case ownership; remaining full-library consistency/polish.\n',encoding='utf-8')
(P/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Veld North carrying</title><style>body{background:#202a30;color:#eee;font:18px sans-serif;margin:30px}img{max-width:100%}p{max-width:65ch}</style><h1>Veld North carrying</h1><p>Refreshed walking draft following the original North master, with alternating steps and the same compact helmet.</p><h2>Bare</h2><img src="bare-carry-north.apng"><h2>Helmet</h2><img src="helmet-carry-north.apng"><h2>Master comparison</h2><img src="paired-master-contact.png"><h2>Engine comparison: bare</h2><p>Previously selected artwork above, new draft below.</p><img src="bare-native-motion.apng"><h2>Engine comparison: helmet</h2><img src="helmet-native-motion.apng">',encoding='utf-8')
print('Recorded scoped North gait milestone in five references and handoff')
