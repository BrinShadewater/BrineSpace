from pathlib import Path
import hashlib,json,subprocess,sys,time,uuid
P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
outputs=[P/x for x in ['CONTACT_REVIEW.json','world-contact-comparison.png','TRIAL_REVIEW.json','bare.png','helmet.png','trial-comparison.png','world-motion.png','MOTION_REVIEW.json']]
before={p.relative_to(P).as_posix():sha(p) for p in outputs}
for name in ['audit_contact.py','build_trials.py','build_motion_review.py']:
 subprocess.run([sys.executable,str(P/name)],cwd=R,check=True,stdout=subprocess.DEVNULL)
assert before=={p.relative_to(P).as_posix():sha(p) for p in outputs}
(P/'REBUILD_REVIEW.json').write_text(json.dumps({'byteExactOutputs':len(outputs),'failures':0,'bindings':before},indent=2)+'\n',encoding='utf8')
v5=P.parent/'west-carry-master-match-v5';v5bindings=json.loads((v5/'FAMILY_REVIEW.json').read_text())['bindings']
for ref,expected in v5bindings.items():assert sha(R/ref)==expected
selected=json.loads((P.parent/'installed/selected-library.json').read_text());pngs=set();manifests=set()
for states in selected['resolved'].values():
 for key,state in states.items():
  if key.endswith('-west'):pngs.update(state['frameFiles']);manifests.add(state['manifest'])
for files,bindings in [(pngs,selected['sourceBindings']),(manifests,selected['bindings'])]:
 for ref in files:assert sha(R/ref)==bindings[ref]
(P/'SELECTION_REVIEW.json').write_text(json.dumps({'retainedV5BindingsUnchanged':len(v5bindings),'selectedWestPngsUnchanged':len(pngs),'selectedWestManifestsUnchanged':len(manifests),'normalAdmission':False,'failures':0},indent=2)+'\n',encoding='utf8')
inputs=json.loads((P/'INPUTS.json').read_text());(P/'retry/INPUTS.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf8')
verdict={'status':'Both whole-body repair trials rejected; V5 retained unchanged','normalAdmission':False,'newNativeRun':False,'wholeSourcesVisuallyReviewed':2,'softwareScaleReview':[47,93,148],'firstTrial':{'heelContourBeforeAfter':[155,153],'headAxisBeforeAfter':[129.5,132.5],'reason':'Requested substantial stance-leg movement not achieved; head shifted'},'retry':{'size':[1087,1447],'reason':'Whole source still misses stance-foot placement; canvas also changed. Rejected before packaging, no compensating registration/rescale'},'next':'Reauthor smoother complete-body gait with valid support-contact progression and master identity; then complete stop/settle and cargo/turn joins','billing':'Two built-in imagegen edits; billing unverified. No new MiniMax job.'}
(P/'SOURCE_VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n',encoding='utf8')
hand='''# Project handoff

Updated: October 4, 2026 - Veld West support-foot diagnosis

## Objective and acceptance
Continue original-master Veld closeout. Supporting-foot diagnosis completed; two local whole-body edits rejected. Previous V5 remains staged and unchanged, not installed. No completed gait/contact/unload-join acceptance; full Veld unfinished.

## Accepted decisions and constraints
Consumer uses cell_size*0.17/148 scale, not a fixed47px character at arbitrary cell size. Existing stride0.07351351351351351 equals64 source-pixel root travel per840ms cycle,10.6667 per equal pose interval. Preserve that existing contract rather than altering speed to mask a single bad stance pose. Fixed original source scale/offset, matte materials and rigid original helmet retained. No isolated leg composites or per-pose alignment/grade repair.

## Findings
Visually reviewed support-only sole windows avoid mixing the lifted foreground boot. Right sole contours: near124/132/148, far119/127/155. Subtract intended root movement: near heel-contour spread5.3333px, far17.3333px. Far pose5 is the specific outlier; near/far first down step advances8px versus10.6667px root. Heel contours change with articulation and are proxies, not exact anatomical landmarks or actual station route proof. Six held frames additionally slide within each nonzero movement interval; continuous gait/contact acceptance cannot come from source-clock coverage alone.

Two built-in full-body source edits used immutable cargo master plus V5 passing-b geometry. Trial1 heel155 to153 only, head axis129.5 to132.5: wrong correction and shifted upper body. Retry visibly still places stance boot too far right and changes canvas1086x1448 to1087x1447; rejected before packaging. Both complete sources, exact prompts and reference hashes retained. No new MiniMax job; built-in billing unverified. No further blind retry scheduled.

## Changed files and checks
audit_contact.py and CONTACT_REVIEW.json/world-contact-comparison.png; build_trials.py and first-trial paired bare/helmet, trial comparison/TRIAL_REVIEW.json; build_motion_review.py and101-frame software floor replay/MOTION_REVIEW.json; preview, prompts/sources, verdict and evidence records. Both raw sources, enlarged V5 boot-detail board, fixed-world support board and first trial full/47/93px board visually reviewed.101 exact decoded replay pixels and all6 source slots checked;8 artifacts rebuild byte-exact. Retained V5 bound source/frames/manifests and selected West722 PNGs/38 manifests unchanged. No new Godot run or owner profile access; previous V5 native504check pass retains its prior scope and is not this turn's contact acceptance. No gameplay/loader/controller/timer/normal selection/commit/export changes.

## Remaining work and next action
Smoother whole-body gait with coherent supporting feet and original identity before expanding complete carry-stop/settle. Unload remains feet-together while carry has wide/swing poses; no stop bridge authored in this interval. Review root/contact/loop and cargo/planted-turn joins, then actual NPC/interruption/fresh-process Continue before normal admission. North workshop arrival and idle pickup mapping remain separate controller limitations. Continue this task; no live generation job or approval gate.
'''
(P/'HANDOFF.md').write_text(hand,encoding='utf8')
title='## Veld West supporting-foot diagnosis - October 4, 2026'
note=title+'\n\nConsumer scale confirms existing840ms stride is64 native pixels per cycle. Supporting-sole contour replay isolates last far passing pose: near spread5.33px versus far17.33px; these are contour proxies, not actual station contact proof. Two built-in whole-body fixes missed requested foot movement, first also shifted head; both rejected, sources/prompts retained in character/veld-library-closeout-v1/west-carry-contact-audit-v6/.101-frame three-scale fixed-floor replay checked;8 review artifacts rebuild byte-exact, V5 bindings and selected West722 PNGs/38 manifests unchanged. No new native run or owner-profile access. V5 remains staged, full Veld unfinished. Next smoother whole-body gait/support progression then complete settle/cargo/turn/lifecycle gates; no live job or approval gate.\n\n'
status=R/'docs/CURRENT_STATUS.md'
for attempt in range(20):
 stat=status.stat();tmp=status.with_name(status.name+'.'+uuid.uuid4().hex+'.tmp')
 with status.open(encoding='utf8') as f:
  if title in ''.join(f.readline() for _ in range(120)):break
 with tmp.open('wb') as out,status.open('rb') as src:
  out.write(note.encode())
  while chunk:=src.read(1024*1024):out.write(chunk)
 after=status.stat()
 if (stat.st_size,stat.st_mtime_ns)==(after.st_size,after.st_mtime_ns):
  try:tmp.replace(status);break
  except PermissionError:pass
 tmp.unlink();time.sleep(.5)
else:raise RuntimeError('Concurrent status update prevented guarded prepend')
parent=P.parent/'HANDOFF.md'
if title not in parent.read_text(encoding='utf8'):
 with parent.open('a',encoding='utf8') as f:f.write('\n\n'+note)
files=[p for p in P.rglob('*') if p.is_file() and p.name!='FINAL_REVIEW.json']
(P/'FINAL_REVIEW.json').write_text(json.dumps({'scope':'Support-foot diagnostic; both generated trials rejected; unchanged staged V5','bindings':{p.relative_to(R).as_posix():sha(p) for p in files}},indent=2)+'\n',encoding='utf8')
print(len(outputs),'byte-exact outputs;',len(v5bindings),'V5 bindings;',len(pngs),'selected West PNGs/',len(manifests),'manifests unchanged')
