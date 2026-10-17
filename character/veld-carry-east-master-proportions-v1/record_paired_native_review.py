from pathlib import Path
import hashlib,json,os,time,shutil,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1];O=P/'paired-package-v1';N=R/'output/veld-carry-east-master-proportions-native-v2'
validation=json.loads((N/'validation.json').read_text());assert validation['passed']
motion=json.loads((O/'motion-review-evidence.json').read_text());motion['visualReview']='All four chronological boards /104 source-native pairs inspected at93px, plus bare000/helmet017 full engine captures at47/93/148px. Shell remains identical and collar visually connected in inspected poses. Source helmet/head detail board inspected across all six poses. Case/clasp/grip and bare material variation remain provisional; sampled captures do not establish continuous native cadence or actual controller/world adoption.'
motion['browserReview']={'files':[{'path':f'browser-review/{name}','sha256':hashlib.sha256((O/'browser-review'/name).read_bytes()).hexdigest()} for name in ['paired-source.jpg','engine-comparison.jpg']],'scope':'Rendered paired source sheet and native APNG presentation snapshots only; no browser-source exact-phase binding or full watched cadence claim.'}
motion['previewVerification']=[]
for name in ['index.html','paired-master-contact.png','bare-native-motion.apng','helmet-native-motion.apng']:
 with urllib.request.urlopen('http://127.0.0.1:8791/character/veld-carry-east-master-proportions-v1/paired-package-v1/'+name) as response:
  exact=response.read()==(O/name).read_bytes();assert response.status==200 and exact;motion['previewVerification'].append({'file':name,'status':200,'exactBytes':exact})
(O/'motion-review-evidence.json').write_text(json.dumps(motion,indent=2)+'\n',encoding='utf-8')
reg=json.loads((O/'package-registration.json').read_text());reg['visualReview']='All12paired whole poses and6helmet close-ups inspected; original East shell fixed34x38, translated only. No visible collar gap in inspected source/engine snapshots. Full motion/material/world joins pending.'
(O/'package-registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
block='''## Veld East paired master carry and native player review — October 2, 2026

paired-package-v1 stages12exact body/shared-helmet frames. Original East component
crop82,17,116,55 stays34x38, unchanged pixels/grade, translated by warm-head axis
and gasket anchor. Body outside bounded head fit exact, below110exact, all6bare
frames exact to reviewedcase-v2. Original256canvas/pivot128,224/H148/6x140msloop/
840ms/stride.0872972973 retained; explicit whole res paths.62build+54independent
package checks0fail. All12whole/6helmet details inspected; connected collar in
inspected presentations, shell architecture fixed. No production binding change.

First native interval633checks/4failures retained in native-v1: ideal wall-clock
oracle expects next slot at.7/1.4s, actual distance phase.6999999699/1.3999999398
precedes boundary from Vector2rounding. Corrected test identifies exactly one frozen
displayed source, checks phase within1microsecond of prescribed movement, permits
only preceding slot at exact ideal boundary with that tolerance. No runtime fix.
Fresh native-v2:841checks0fail/104samples/7.91s, actualCrewSpritePlayer both gears,
30Hz prescribed distance/time over2cycles,47/93/148rulers.30targeted inputs stable;
all2931owner non-log files unchanged, scratchAPPDATA. Four chronological boards/
104source-native pairs and2full engine captures inspected;104APNGdecoded frames
exact. Browser paired source sheet/native presentation snapshots inspected;
4HTTPfiles200/exact. This is sampled player/source proof, not full continuous
cadence, actual cargo controller/world/ownership/interruption/Continue acceptance.

Lesson: derive review records from the actual frozen displayed texture. At true
hold boundaries, physical Vector2distance rounding can land just before ideal
wall time; preserve phase evidence and bound any adjacent-slot allowance tightly.
Never alter runtime pacing to hide a fixture oracle error. Shared fixed-scale
equipment and protected bodies still need actual transition/contact review.
Next East held/carry/pickup/unload joins and full-cycle weight/contact/material
review, then matched action sources/real world lifecycle. South/North matching,
remaining sit/read/context, guarded adoption and full-set polish remain open.
Review: character/veld-carry-east-master-proportions-v1/paired-package-v1/.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(5):
  with path.open('rb') as f:head=f.read(65536)
  if block.splitlines()[0].encode() in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-pair.tmp')
  with tmp.open('wb') as dest,path.open('rb') as src:dest.write(block.encode());shutil.copyfileobj(src,dest,1024*1024)
  after=path.stat()
  if (before.st_mtime_ns,before.st_size)!=(after.st_mtime_ns,after.st_size):tmp.unlink();continue
  try:os.replace(tmp,path);break
  except PermissionError:tmp.unlink(missing_ok=True);time.sleep(.5)
 else:raise RuntimeError(f'Concurrent update prevented {path}')
with (P/'SOURCE_REVIEW.md').open('a',encoding='utf-8') as f:f.write('\n'+block)
for path in [P/'HANDOFF.md',R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md']:
 source=path.read_text(encoding='utf-8');start=source.index('## Next action');source=source[:start]+block+'''## Next action
Audit East held/carry/pickup/unload joins and full-cycle weight/contact/material;
author matching action family from the original masters and canonical held pose.
Then actual controller/room cargo ownership, interruptions and fresh Continue
before guarded adoption. Preserve paired-package-v1 exact sources/original clock,
fixed East shell and failed native-v1 evidence. South/North master matching, other
seated/read contexts and full cross-library polish remain. Full goal active.
''';path.write_text(source,encoding='utf-8')
print(json.dumps({'buildChecks':62,'packageChecks':54,'nativeChecks':841,'nativeFailures':0,'nativeSamples':104,'decodedFramesExact':104,'ownerFilesUnchanged':2931,'httpExactFiles':4,'maintainedReferences':5,'handoffs':2,'scope':'staged paired player proof; world/full objective incomplete'}))
