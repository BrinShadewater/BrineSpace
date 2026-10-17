from pathlib import Path
import json,hashlib,subprocess,sys,time,uuid

P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
validation=json.loads((R/'output/veld-west-carry-poses-v4/validation.json').read_text())
assert validation['passed'] and not validation['realProfileChanges']
outputs=list((P/'frames').rglob('*.png'))+[P/n for n in ['bare-manifest.json','helmet-manifest.json','bare-carry.png','helmet-carry.png','bare-chronology.png','helmet-chronology.png','bare-scales.png','helmet-scales.png','FAMILY_REVIEW.json']]
before={p.relative_to(P).as_posix():sha(p) for p in outputs}
subprocess.run([sys.executable,str(P/'build_family.py')],cwd=R,check=True,stdout=subprocess.DEVNULL)
assert before=={p.relative_to(P).as_posix():sha(p) for p in outputs}
(P/'REBUILD_REVIEW.json').write_text(json.dumps({'failures':0,'byteExactOutputs':len(outputs),'bindings':before},indent=2)+'\n',encoding='utf8')
selected=json.loads((P.parent/'installed/selected-library.json').read_text());pngs=set();manifests=set()
for states in selected['resolved'].values():
 for key,state in states.items():
  if key.endswith('-west'):pngs.update(state['frameFiles']);manifests.add(state['manifest'])
for files,bindings in [(pngs,selected['sourceBindings']),(manifests,selected['bindings'])]:
 for ref in files:assert sha(R/ref)==bindings[ref]
(P/'SELECTION_REVIEW.json').write_text(json.dumps({'westPngsUnchanged':len(pngs),'westManifestsUnchanged':len(manifests),'failures':0,'normalAdmission':False},indent=2)+'\n',encoding='utf8')
family=json.loads((P/'FAMILY_REVIEW.json').read_text());rows=family['rows']
(P/'SOURCE_VERDICT.json').write_text(json.dumps({'status':'Staged full alternating cycle; visual consistency/contact gate incomplete','method':'Five individual built-in imagegen complete-body pose edits, one previous near-contact source reused; no new MiniMax job','allSixWholeSourcesAndBothGearChronologyReviewed':True,'representativeNativeCapturesReviewed':4,'softwareReviewSizes':[47,93,148],'headWidthRange':[min(x['headWidth'] for x in rows),max(x['headWidth'] for x in rows)],'headAxisRange':[min(x['headAxis'] for x in rows),max(x['headAxis'] for x in rows)],'bootFloorAlpha128Range':[min(x['floorAlpha128'] for x in rows),max(x['floorAlpha128'] for x in rows)],'materialFinding':'Blue median128..154 in B channel, visible second-half badge brightening; median is a diagnostic, not a certified material mask or exposure measure. Small case/hardware/head variations also remain.','poseFinding':'Correct opposite leading legs and planted support/raised swing boots in both passing poses. More natural alternating gait than failed video. Short stride/loop smoothness/actual physical contact still not accepted.','normalAdmission':False,'next':'Use immutable original high-resolution cargo master as primary identity authority and these whole-body poses only as geometry controls; avoid chaining generated costume/grade drift or isolated limb/colour stencils.'},indent=2)+'\n',encoding='utf8')
hand='''# Project handoff

Updated: October 4, 2026 — Veld West authored carry cycle

## Objective and acceptance
Complete original-master-consistent cargo animation. Six-pose alternating carry candidate now staged for both gears, not owner accepted or installed. Visual consistency/contact gate remains incomplete; full Veld library unfinished.

## Accepted decisions and constraints
Five built-in imagegen complete-pose edits: opposite contact, near/far down and near/far passing. Previous near-contact v3 source reused as slot0. Explicit foreground/background knee/ankle instructions succeeded where earlier generic opposite-contact requests did not. All five new high-resolution sources, exact prompts and input hashes retained in their named folders. No new MiniMax job, billing for built-in edits unverified. Whole connected bodies, no isolated limb compositing, synthetic inbetween frames or per-pose grade/registration corrections.

## Changed files and current state
build_family.py produces12 PNGs, two manifests, paired APNGs, full chronology/head boards and three-scale software boards. Poses order: near contact/down/support-and-far-pass, far contact/down/support-and-near-pass. One fixed source scale0.10832719233603537 and offset73,73 for all1086x1448 sources. 256canvas, pivot128224, density148, dry, original840ms cycle and stride0.07351351351351351 unchanged. Original West helmet shell reused; body outside shell exact in all6 frames. Browser preview visible. No normal loader, controller, selected artwork or game timing changed. No live job.

## Verification
30 helmet-outside-body/APNG pixel-hold checks passed;21 outputs rebuild byte-exact. Native scoped player fixture504checks/0failures,12 three-scale presentations at47/93/148px. Exact source poses/pixels, metadata, moving-stride wrap, stationary hold, idle return, fresh-player restore, and103 ticks per gear over two moving cycles visit all6 slots.649 targeted inputs and2936 owner-profile nonlogfiles unchanged. Selected ending-West722 PNGs/38 manifests unchanged. All6 whole sources, bare/helmet chronology and software scales reviewed;4 representative native captures viewed. Test+UID in tests/test_veld_west_carry_poses_v4.gd; scratch-profile runner tools/run_veld_west_carry_poses_v4.py; output/veld-west-carry-poses-v4.

First native interval504checks/4failures preserved in output/pre-boundary-assertion: independent distance accumulation versus duration subtraction chose adjacent poses at exact0.7/1.4s boundaries. Diagnostic cadence showed source5 vs expected4 and source4 vs expected3, both gears. Final assertion permits adjacent slots ONLY within1e-6 of an exact hold boundary, retains exact comparison elsewhere and records all four boundary ties. Production player unchanged; no fixed wait or source-clock workaround.

## Limits and remaining work
Art gate remains incomplete despite technical pass. Head width27..29, axis128..132.5, top76..78; body H146..150 naturally changes with pose but does not prove proportion consistency. Boot opaque edge floor223..225 vs reference223, so no exact planted world-contact claim. Blue diagnostic medians progress56,84,128 to62,96,154; visible brighter badges on second half, not solved by clock checks. Small face/case/hardware changes remain. No continuously watched native animation, actual NPC route/furniture/root/contact, interruption or disk Continue acceptance. Wider contact/raised swing poses and loop/handoff smoothness need review. Original cargo head remains3px ahead of neutral master. West workshop arrival faces north; pickup currently idle during520ms wait and reversed pickup remains rushed audition.

## Next action
Reauthor material/detail consistency using the immutable high-resolution cargo master as PRIMARY identity authority and these correct full-body poses as separate geometry controls. Do not propagate brighter clothing from generated opposite pose into its children or apply per-frame exposure/anatomy masks. Establish supporting-foot geometry through the authored poses with one fixed ruler, then full loop and carry/unload/pickup/planted-turn handoffs. Preserve old840ms cadence/stride until visual/contact gates pass; then controller/lifecycle and fresh-process Continue checks before normal admission. No approval gate.
'''
(P/'HANDOFF.md').write_text(hand,encoding='utf8')
title='## Veld West full authored carry cycle staged — October 4, 2026'
note=title+'\n\nFive built-in complete-pose edits plus previous near contact now form a true alternating six-pose carry candidate in character/veld-library-closeout-v1/west-carry-poses-v4/, both gears, original shell/840ms stride contract and one fixed master scale/offset.30 packaging checks/21 byte-exact rebuilt outputs;504 native player checks0failures,12 three-scale presentations, two movement-driven cycles visit all6 poses.649 inputs/2936 owner files and selected ending-West722 PNGs/38 manifests unchanged. All whole sources/chronology/software scales and4 native captures reviewed; preview visible. Initial4 exact floating-boundary assertion failures preserved, corrected only fixture tie semantics with explicit cadence evidence; production player unchanged. Visual gate INCOMPLETE: second-half blue badge brightening, head outlines27..29/axis128..132.5 and boot edge223..225 plus minor case/details. Not installed or physical/NPC/interruption/Continue acceptance. Next immutable-master identity plus correct pose geometry controls, material/contact/loop/whole-family joins; full Veld unfinished, no live job or approval gate.\n\n'
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
else:raise RuntimeError('Concurrent status changes prevented guarded prepend')
parent=P.parent/'HANDOFF.md'
if title not in parent.read_text(encoding='utf8'):
 with parent.open('a',encoding='utf8') as f:f.write('\n\n'+note)
files=[p for p in P.rglob('*') if p.is_file() and p.name!='FINAL_REVIEW.json']+[R/'tests/test_veld_west_carry_poses_v4.gd',R/'tests/test_veld_west_carry_poses_v4.gd.uid',R/'tools/run_veld_west_carry_poses_v4.py',R/'output/veld-west-carry-poses-v4/validation.json',R/'output/veld-west-carry-poses-v4/cadence.json']
(P/'FINAL_REVIEW.json').write_text(json.dumps({'scope':'Staged full authored carry candidate; visual consistency/contact gate incomplete; no normal admission','bindings':{p.relative_to(R).as_posix():sha(p) for p in files}},indent=2)+'\n',encoding='utf8')
print('Recorded six-pose candidate:',len(files),'bound deliverables;',len(outputs),'outputs rebuild exact;',len(pngs),'West PNGs/',len(manifests),'manifests unchanged')
