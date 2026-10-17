from pathlib import Path
import json, hashlib, subprocess, sys, time, uuid

P=Path(__file__).resolve().parent; R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
validation=json.loads((R/'output/veld-west-carry-master-match-v5/validation.json').read_text())
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
verdict={'status':'Staged immutable-master matched carry; visual/contact/join acceptance incomplete','normalAdmission':False,'wholeSourcesAndPairedChronologyReviewed':True,'softwareReviewSizes':[47,93,148],'representativeNativeCapturesReviewed':2,'joinComparisonReviewed':True,'blueDiagnosticSpreadBeforeAfter':[26,15],'bootFloorAlpha128Range':[223,225],'remaining':['Small badge/case/head detail differences','Walking-to-feet-together unload needs settle/contact review','Physical root/stride audit','Whole cargo/turn joins and NPC/interruption/disk Continue gates'],'billing':'No new MiniMax job; built-in imagegen billing unverified'}
(P/'SOURCE_VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n',encoding='utf8')
join=json.loads((P/'JOIN_REVIEW.json').read_text());join.update({'visuallyReviewed':True,'finding':'Carry has wide contact/swing poses; unload entry has feet together. Direct transition is not a reviewed settle bridge. Carry/anchor retain sharper details than video unload endpoint. Original helmet shell stays consistent; head/face outline details still differ.','joinAcceptance':False});(P/'JOIN_REVIEW.json').write_text(json.dumps(join,indent=2)+'\n',encoding='utf8')
hand='''# Project handoff

Updated: October 4, 2026 - Veld West immutable-master carry consistency

## Objective and acceptance
Finish Veld against original masters. Revised six-pose West carry is staged for both gears. Playback passes; visual/contact/join acceptance remains incomplete. Full Veld library unfinished. No normal admission, commit or export.

## Accepted decisions and constraints
Five built-in imagegen whole-body edits use immutable high-resolution cargo master as identity authority and corresponding V4 whole poses only as geometry controls. Prior near-contact source reused for slot0. New sources, exact prompts and reference hashes saved in opposite/down-a/passing-a/down-b/passing-b. No new MiniMax job; built-in billing unverified. Preserve connected anatomy, original matte palette and original helmet. No isolated limb composites, per-pose registration/RGB correction or synthetic inbetween frames.

## Changed files and current state
build_family.py, twelve frames, paired manifests/APNGs/chronology/scales, material and join comparisons, preview and review reports. Test plus paired UID: tests/test_veld_west_carry_master_match_v5.gd; scratch-profile runner tools/run_veld_west_carry_master_match_v5.py. Fixed scale0.10832719233603537, whole offset73,73 for all1086x1448 sources;256canvas/pivot128224/density148. Six140ms poses,840ms loop and stride0.07351351351351351 retained. Original West helmet shell reused; outside-shell body exact in all6 poses. Loader/controller/timers/normal selections unchanged by this work. No live job.

## Verification
30 packaging checks passed;21 outputs rebuild byte-exact. Native504checks/0failures,12 three-scale presentations,18.01seconds. Exact source pixels, metadata, stationary hold, movement-driven wrap, idle return and fresh-player restore; two cycles visit all6 slots per gear.649 targeted inputs and2936 owner-profile files unchanged during native interval. Selected ending-West722 PNGs/38 manifests unchanged. All five new high-resolution sources plus retained contact source, paired chronology and software47/93/148px boards reviewed;2 native captures viewed. Existing fixture's explicit1e-6 floating-boundary tie allowance retained; production player unchanged. Native evidence in output/veld-west-carry-master-match-v5.

## Findings and limits
Blue badge diagnostic spread26 to15; maximum deviation from immutable cargo master23 to12, RMS16.20 to6.20. Threshold-selected colour medians are diagnostics, not certified material masks or exposure acceptance. Overall grade closer; badge/case/head detail differences remain. Head top-band widths27..29 include possible collar edges, not certified anatomical widths. Original cargo head remains3px forward of neutral master. Boot opaque edges223..225 remain, not exact planted world contact.

Paired fixed-pivot join-comparison.png reviewed: wide carry contact/swing poses versus feet-together unload entry require a reviewed settle bridge. Carry/anchor preserve sharper details than video-derived unload endpoint. Pickup end uses same unload-entry source in reverse. This board proves no smooth transition. Native player checks do not establish actual NPC route/root/physical contact, continuously watched playback, interruption or disk Continue. Actual workshop arrival faces north, pickup currently displays idle during520ms wait; reversed pickup remains rushed audition.

## Next action
Establish supporting-foot/root/stride relation and complete-body carry-stop transition, preserving original identity. Review complete carry/unload/pickup/planted-turn joins, then actual controller lifecycle and fresh-process Continue before normal admission. Do not change gameplay timers or stride without scoped evidence. Continue current task; no approval gate.
'''
(P/'HANDOFF.md').write_text(hand,encoding='utf8')
title='## Veld West immutable-master carry consistency staged - October 4, 2026'
note=title+'\n\nFive whole-body edits use immutable cargo identity plus V4 geometry; retained contact key completes six poses per gear in character/veld-library-closeout-v1/west-carry-master-match-v5/. Blue badge diagnostic spread26 to15/max master deviation23 to12, closer grade but small details remain.30 packaging checks/21 byte-exact outputs;504 native checks0failures,12 presentations18.01s.649 inputs/2936 owner files and selected West722 PNGs/38 manifests unchanged. Sources, paired chronology/scales,2 native captures and cargo join board reviewed. Boot contours223..225 and walking-to-feet-together unload settle remain unaccepted; native fixture is not physical/NPC/interruption/Continue proof. Original helmet/body mapping and840ms stride contract preserved. Staged, not installed; full Veld unfinished. Next physical stride/contact and whole-body settle/whole-family joins. No live job or approval gate.\n\n'
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
files=[p for p in P.rglob('*') if p.is_file() and p.name!='FINAL_REVIEW.json']+[R/'tests/test_veld_west_carry_master_match_v5.gd',R/'tests/test_veld_west_carry_master_match_v5.gd.uid',R/'tools/run_veld_west_carry_master_match_v5.py',R/'output/veld-west-carry-master-match-v5/validation.json',R/'output/veld-west-carry-master-match-v5/cadence.json']
(P/'FINAL_REVIEW.json').write_text(json.dumps({'scope':'Staged immutable-master matched carry; visual/contact/join gate incomplete','bindings':{p.relative_to(R).as_posix():sha(p) for p in files}},indent=2)+'\n',encoding='utf8')
print('Recorded',len(files),'deliverables;',len(outputs),'byte-exact outputs;',len(pngs),'West PNGs/',len(manifests),'manifests unchanged')
