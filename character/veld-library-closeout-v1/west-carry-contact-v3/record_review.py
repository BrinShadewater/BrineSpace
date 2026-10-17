from pathlib import Path
import hashlib,json,subprocess,sys,time,uuid

P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
outputs=[P/n for n in ['bare.png','helmet.png','comparison.png','paired-comparison.png','BUILD_REVIEW.json']]
before={p.name:sha(p) for p in outputs};subprocess.run([sys.executable,str(P/'build_key.py')],cwd=R,check=True)
assert before=={p.name:sha(p) for p in outputs}
review=json.loads((P/'BUILD_REVIEW.json').read_text())
checks=0
for field in ['height','floor','headTop','headWidth','headAxis']:
 assert review['metrics']['candidate'][field]==review['metrics']['control'][field];checks+=1
assert review['bodyOutsideHelmetExact'];checks+=1
for ref,value in review['bindings'].items():assert sha(R/ref)==value;checks+=1
selected=json.loads((P.parent/'installed/selected-library.json').read_text());pngs=set();manifests=set()
for states in selected['resolved'].values():
 for key,state in states.items():
  if key.endswith('-west'):pngs.update(state['frameFiles']);manifests.add(state['manifest'])
for files,bindings in [(pngs,selected['sourceBindings']),(manifests,selected['bindings'])]:
 for ref in files:assert sha(R/ref)==bindings[ref]
(P/'FINAL_VERDICT.json').write_text(json.dumps({'status':'Useful near-leading contact key retained, requested opposite-contact not achieved','sourceReview':'Whole authored body and paired helmet neck/face/body reviewed; comparison viewed at 47/93/148px and enlarged','checks':checks,'failures':0,'byteExactRebuildOutputs':len(outputs),'selectedWestPngsUnchanged':len(pngs),'selectedWestManifestsUnchanged':len(manifests),'scope':'Static authoring key and packaging checks only; no gait, native/controller/contact/Continue or normal admission proof','remaining':['Distinct opposite-leading and passing poses','Whole alternating cycle and loop seam','Carry/unload/pickup and planted-turn joins','Native/controller/lifecycle gates'],'normalAdmission':False},indent=2)+'\n',encoding='utf8')
hand='''# Project handoff

Updated: October 4, 2026 — Veld West whole-body carry sources

## Objective and acceptance
Match carry to the original-master unload/cargo reference. Useful paired near-leg-leading contact key staged here; no finished alternating loop or normal admission. Full Veld library unfinished.

## Decisions and method changes
One Hailuo02 first/last carry job, 448738642895348, succeeded (6s768P24fps; USD0.28 estimate, billing unverified). Full142 source poses/5917ms retained under west-carry-source-v1. All142 bare poses reviewed. Material/head/case continuity is substantially close, but supporting outlines repeatedly rise while headtop remains76. Opaque floor217..224, alpha128 lower-boot floor218..225 vs control223. Rejected before loop/helmet expansion, not per-pose refloored/rescaled or cropped to hide failure. 284 APNG grouped-pixel/hold checks passed; these do not establish gait quality or world contact.

Changed method to built-in imagegen whole-body authored poses. One six-pose sheet in west-carry-poses-v2 retained with original high-resolution cargo reference and exact prompt. All six bodies reviewed; repeated leading-leg arrangements and crowded nominal cell boundaries fail gait/extraction. No sheet frames or manifests produced.

One individual built-in contact edit retained here in source.png, exact prompt.txt and INPUTS.json. It did not deliver the requested opposite-leading leg. Retain honestly as a near-leading contact key, not a new full cycle. No isolated limb stencil, RGB grade or anatomy assembly. Built-in billing not verified.

## Changed files and current state
Three new source folders with raw sources, prompts, hashes and rejection records. This folder has build_key.py, bare.png, helmet.png, two comparison boards, index.html, BUILD_REVIEW/FINAL_VERDICT, recorder and bound review. Original helmet shell reused without design change; outside-head body exact. No runtime manifest, loader, controller, selected frame or timing change. No live generation job.

## Verification and limits
Same1086x1448 source canvas, same fixed uniform scale0.10832719233603537 and offset73,73 as cargo control; no pose-specific registration. Candidate/control both H148, floor223, headtop76, width27, axis130. Original neutral head axis133 remains3px behind cargo control. Boot extent94..175 is wider than neutral109..147; short relaxed stride and physical loading remain to review. Whole source, bare/helmet comparison and 47/93/148px software review boards viewed; browser preview visible. Five generated outputs rebuild byte-exact. Normal ending-West722 PNGs/38 manifests unchanged. Checks prove static packing/source integrity, not native playback, an alternating walk, actual contact or Continue. No new Godot test or owner-profile access this interval.

## Next action
Author a distinct opposite-leading complete contact and both passing/down poses, with unambiguous pose controls. Do not call repeated near-leading poses a complete cycle or mirror asymmetric gear. Review identity, grounded support, natural hip/torso coordination and exact loop seam before pairing full gait. Preserve existing840ms carry cadence/stride contract until source proves it. Then matched carry/unload/pickup and planted-turn joins, controller timing/dispatch, interruption and fresh-process Continue. Pickup520ms remains rejected timing audition and workshop pickup currently displays idle; West arrival actually faces north. No approval gate.
'''
(P/'HANDOFF.md').write_text(hand,encoding='utf8')
source=P.parent/'west-carry-source-v1'
(source/'HANDOFF.md').write_text('# West carry video source rejection\n\nOctober 4, 2026. One Hailuo02 job448738642895348, USD0.28 estimate/billing unverified. All142 source poses retained and reviewed, grouped APNG284 checks pass. Rejected before loop/helmet/native expansion: repeated supporting boot outline elevation with fixed head/torso; no per-pose refloor or partial-cycle rescue. Same cargo conditioning controls preserved. SOURCE_VERDICT.json and contact-failure.png contain scoped evidence. Continuation method changed to whole-body authored pose trials; current useful but incomplete contact key is ../west-carry-contact-v3/. No normal changes.\n',encoding='utf8')
html=(source/'index.html').read_text(encoding='utf8').replace('Whole-body carry source from the same cargo master as the new unload. Staged source review only; no installed animation or gameplay change.','REJECTED gait source: supporting boot outlines rise while head height stays fixed. Whole-body identity is close, but no carry loop was selected. Full source retained; no installed animation or gameplay change.')
(source/'index.html').write_text(html,encoding='utf8')
title='## Veld West carry source gate and contact key — October 4, 2026'
note=title+'\n\nCarry/unload material continuity progressed, but no finished carry loop admitted. One Hailuo02 job448738642895348 (USD0.28 estimate/billing unverified), all142 poses retained/reviewed, rejected for support-floor drift; no loop or helmet expansion. Built-in six-pose sheet also rejected for repeated leg arrangements/crowded cells. One built-in whole-body contact edit retained in character/veld-library-closeout-v1/west-carry-contact-v3/: fixed original scale/offset, cargo-control head H148/top76/width27/axis130 and floor223 exact, paired original shell/outside-body exact, five byte-exact rebuilt outputs. Requested opposite-leading leg not achieved; key honestly labelled near-leading only. Sources/prompts/rejections retained. Both gear boards and software47/93/148px comparisons plus browser preview reviewed; no new native/controller proof. Selected ending-West722 PNGs/38 manifests unchanged. Next unambiguous opposite-contact/passing/down whole-body poses and full gait/join/lifecycle gates. Full Veld unfinished, no live job or approval gate.\n\n'
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
for folder in [source,P.parent/'west-carry-poses-v2',P]:
 files=[p for p in folder.rglob('*') if p.is_file() and p.name!='FINAL_REVIEW.json']
 (folder/'FINAL_REVIEW.json').write_text(json.dumps({'scope':'Unselected carry authoring/source gate; not full gait or normal admission','bindings':{p.relative_to(R).as_posix():sha(p) for p in files}},indent=2)+'\n',encoding='utf8')
print('Recorded contact key:',checks,'static checks; 5 byte-exact outputs;',len(pngs),'West PNGs/',len(manifests),'manifests unchanged')
