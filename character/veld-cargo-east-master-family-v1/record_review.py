from pathlib import Path
import hashlib,json,os,shutil,time,urllib.request
P=Path(__file__).resolve().parent;R=P.parents[1];N=R/'output/veld-cargo-east-master-family-v1'
refs=[('character/veld-unload-east-consistent-v1/source-v1.png','action geometry only; obsolete patch/proportions'),('character/veld-cargo-turns-master-family-v1/original-east-density-reference.png','original identity/style/proportions'),('character/veld-cargo-turns-master-family-v1/corrected-east-held-density-reference.png','canonical held identity/case/grip')]
(P/'references-unload-v1.json').write_text(json.dumps([{'path':p,'role':role,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()} for p,role in refs],indent=2)+'\n',encoding='utf-8')
(P/'execution-unload-v1.json').write_text(json.dumps({'tool':'builtin image_gen','execution':'de663e63-43fd-4cca-9635-6d5fc0daa0b3','source':'raw-unload-v1.png','sha256':hashlib.sha256((P/'raw-unload-v1.png').read_bytes()).hexdigest(),'prompt':'prompt-unload-v1.txt','references':'references-unload-v1.json','status':'reviewed_staged_whole_action_source','scope':'Six complete authored poses, single standing ruler; canonical first/idle last aliases in package, no normal adoption.'},indent=2)+'\n',encoding='utf-8')
for file,review in [('join-review-evidence.json','All16pivot-registered whole sources and16head/case diagnostic presentations inspected. Current bare pickup/unload heads32 and crouch36 vs stagedheld26/carry26-27; obsolete atom marking and suit/case proportions drift. Same helmet34proxy does not certify underlying body or equipment placement. Actual grid loader references checked, no runtime mutation.'),('unload-extraction.json','All12old/new whole source poses and6head-case details inspected. New first-standing148 ruler/head proxies28,28,30,30,29,28 improve old source; rotated/crouched proxies not exact head widths. Source all cell-right-edge alpha>200 counts0. Generated complete body/connected crouch/grip/release; isolated floor prop phase4 extracted without boot pixels. Source/body/case material and full joins remain provisional.'),('family-registration.json','All12paired whole poses and6helmet details inspected. Canonical held/selected idle exact endpoints, coherent crouch/release in sampled source. Helmet fixed scale with rigid6/12/16degree bends anchored by rotated gasket. Bare phase/material/case detail variation and terminal selected idle broader than canonical held remain polish concerns; no final full-motion/world acceptance.'),('native-review-evidence.json','All4chronological boards /72source-native pairs inspected at93px; helmet unload010 full engine scene inspected at47/93/148. Helmet collar visually connected, smooth case reaches floor before clear hands/rise, source identity closer. Sampled rendering does not prove continuous native cadence or actual actor/room/world ownership/interruption/Continue.')]:
 path=P/file;data=json.loads(path.read_text());data['visualReview']=review;path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
samples=json.loads((P/'browser-review/samples.json').read_text());assert len([s for s in samples if s['kind']=='finite-completion' and s['state']['elapsed']=='520.0' and s['state']['phase']=='5'])==4
http=[]
for name in ['index.html','paired-unload-contact.png','bare-unload-east.apng','helmet-unload-east.apng','bare-pickup-east.apng','helmet-pickup-east.apng']:
 with urllib.request.urlopen('http://127.0.0.1:8791/character/veld-cargo-east-master-family-v1/'+name) as response:
  exact=response.read()==(P/name).read_bytes();assert response.status==200 and exact;http.append({'file':name,'status':200,'exactBytes':exact})
(P/'browser-review/evidence.json').write_text(json.dumps({'samples':samples,'http':http,'scope':'Paused helmet contact and four finite source completions (bare normal /helmet quarter speed), not uninterrupted visual cadence or browser-native exact phase binding.'},indent=2)+'\n',encoding='utf-8')
validation=json.loads((N/'validation.json').read_text());assert validation['passed'];block='''## Veld East matched pickup/unload master family — October 2, 2026

Actual selected source join audit16whole/16detail views: bare action heads32 and
crouch36 vs stagedheld26/carry26-27, obsolete atom marking/suit/case drift. Current
loader paths checked. Six authored East unloading source poses2144x733 now use
original identity and corrected held master, square-ring patch/graphite suit/plain
case. Raw/prompt/reference hashes/execution retained. One first-standing148 ruler
(.2474916388), physical boot registration; no body strips/per-pose height fitting.
All12old/new source whole views+6details inspected; head proxies28/28/30/30/29/28.
Isolated release-cell case extracted33x25 without boots, fixed149,200 in4/5.

New unselected cargo-east-master-family-v1 aliases canonical whole held0, selected
idle whole body under floor prop5. Four whole authored interiors get unchanged
West master grade recipe; case/grip contexts/alpha protected. Original East shell
34x38 at fixed scale, rigid6/12/16degree tilt with transformed gasket anchoring.
Carry paired sources exact reused; pickup exact unload reverse. Original520ms
finite holds/metadata, H148/p128224 and explicit whole res paths.80build+91package
checks0fail; all12paired whole/6helmet details inspected. Bare grade/head/case
variation and broader selected terminal idle remain final polish concerns.

Actual standaloneCrewSpritePlayer453checks0fail/72native samples/6.06s, two actions/
two gears at30Hz prescribed time,47/93/148rulers.56frozen targeted inputs stable,
scratchAPPDATA/all2931owner non-log files unchanged.4chronological boards/72source-
native pairs and helmet unload010 full scene inspected;72decoded native snapshots
exact. Recorded600ms repeating viewer is separate from finite520msgame action.
Actual browser paused helmet contact and4finite source completions at520ms reviewed
(bare normal,helmetquarter speed); six HTTPfiles200/exact. Normal runtime selections
unchanged. No actual cargo ownership/room/controller/interruption/Continue or full
continuous native cadence acceptance. All5maintained refs carry this milestone.

Lesson: matching helmet silhouette can hide body/marking/head drift. Audit whole
idle/held/action/gait sources together at their physical pivot. A clean authored
prop can be separated after release, but hand contact cannot be erased with a
wide case crop. Rigid helmet rotation must transform its gasket anchor; constant
head size and source-clock tests do not prove floor contact or natural handoffs.
Next full moving/contact/material review and actual East cargo/start/stop/turn/
ownership/interruption/Continue joins. South/North actions and other contexts plus
full cross-library polish remain; full Veld goal active/incomplete.

'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(5):
  with path.open('rb') as f:head=f.read(65536)
  if block.splitlines()[0].encode() in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-east-actions.tmp')
  with tmp.open('wb') as dst,path.open('rb') as src:dst.write(block.encode());shutil.copyfileobj(src,dst,1024*1024)
  after=path.stat()
  if (before.st_mtime_ns,before.st_size)!=(after.st_mtime_ns,after.st_size):tmp.unlink();continue
  try:os.replace(tmp,path);break
  except PermissionError:tmp.unlink(missing_ok=True);time.sleep(.5)
 else:raise RuntimeError(f'Concurrent update prevented {path}')
(P/'HANDOFF.md').write_text('''# Project handoff
Updated: October 2, 2026 · Project: BrineSpace · Task: Veld master cargo family

## Objective and acceptance
Continue full Veld set/master consistency and cross-library polish. Staged East
actions are a milestone; full objective includes actual motion/world/lifecycle.

## Accepted decisions and constraints
Original masters define identity/proportions/matte grade. Preserve selected runtime,
whole authored anatomy, physical boot/root, fixed equipment scale and original
finite holds. Generated source retained; owner saves never used by tests.

## Current state
raw-unload-v1/prompt/refs/execution, extraction/grade/paired builders, full source
audit/contact boards, manifests and independent verifier; canonical held/selected
idle aliases. New paired test/UID/isolated runner,72native sample review. All staged.

## Verification
80build+91package checks;453native/0fail/72samples/6.06s.56inputs stable;2931owner
files unchanged. All4native chronological boards/72pairs,1full scene,12paired/
6helmet details and12old/new source+6details viewed. Browser4finite completions/
paused contact; no uninterrupted/native/world acceptance. Details in evidenceJSON.

## Next action
Inspect remaining material/head/case variation and moving/contact joins, then
actual East cargo/start/stop/turn/ownership/interruption/Continue. South/North
master actions, remaining furniture/read contexts, guarded adoption and full-set
cross-library polish remain. Keep original case contact in3 separate from exact
locked independent floor case4/5; do not claim matching52Omsclocks proves contact.
''',encoding='utf-8')
for path in [R/'character/veld-carry-east-master-proportions-v1/HANDOFF.md',R/'character/veld-cargo-turns-master-family-v1/HANDOFF.md']:
 source=path.read_text();start=source.index('## Next action');path.write_text(source[:start]+block+'''## Next action
East paired pickup/unload now staged in character/veld-cargo-east-master-family-v1.
Next moving/contact/material and actual start/stop/turn/ownership/interruption/
Continue joins before guarded adoption. South/North master actions, furniture/
read contexts and full cross-library polish remain. Full Veld goal active.
''',encoding='utf-8')
print(json.dumps({'buildChecks':80,'packageChecks':91,'nativeChecks':453,'nativeFailures':0,'nativeSamples':72,'ownerFilesUnchanged':2931,'targetedInputsUnchanged':56,'browserFiniteCompletions':4,'maintainedReferences':5,'scope':'staged matched East actions; full goal incomplete'}))
