from pathlib import Path
import hashlib, json, subprocess, sys, time, uuid

P = Path(__file__).resolve().parent
R = P.parents[2]
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
validation = json.loads((R/'output/veld-west-cargo-timing-v1/validation.json').read_text())
assert validation['passed'] and not validation['realProfileChanges']
outputs = [p for p in P.iterdir() if p.name in ['FAMILY_REVIEW.json'] or p.name.endswith('-manifest.json') or p.name.endswith('-60hz.json') or p.name in ['bare-unload.png','helmet-unload.png','bare-pickup.png','helmet-pickup.png']]
before = {p.name: sha(p) for p in outputs}
subprocess.run([sys.executable, str(P/'build.py')], cwd=R, check=True)
assert before == {p.name: sha(p) for p in outputs}
(P/'REBUILD_REVIEW.json').write_text(json.dumps({'byteExactOutputs':len(outputs),'failures':0,'bindings':before},indent=2)+'\n',encoding='utf8')
selected = json.loads((P.parent/'installed/selected-library.json').read_text())
pngs=set(); manifests=set()
for states in selected['resolved'].values():
 for key, state in states.items():
  if key.endswith('-west'):
   manifests.add(state['manifest']); pngs.update(state['frameFiles'])
for files, bindings in [(pngs,selected['sourceBindings']),(manifests,selected['bindings'])]:
 for ref in files: assert sha(R/ref)==bindings[ref], ref
(P/'SELECTION_REVIEW.json').write_text(json.dumps({'westPngsUnchanged':len(pngs),'westManifestsUnchanged':len(manifests),'failures':0,'normalAdmission':False},indent=2)+'\n',encoding='utf8')
cadence=json.loads((R/'output/veld-west-cargo-timing-v1/cadence.json').read_text())
counts=[{'gear':x['gear'],'kind':x['kind'],'uniquePoses':len({t['slot'] for t in x['ticks']}),'ticks':len(x['ticks'])} for x in cadence]
(P/'CADENCE_VERDICT.json').write_text(json.dumps({'presentations':counts,'unload':'Compatible 2-second clock candidate; staged only','pickup':'Rejected for admission: rushed 520ms audition; 32 of 97 poses presented at 60Hz','failures':0},indent=2)+'\n',encoding='utf8')
hand='''# Project handoff

Updated: October 4, 2026 — Veld West cargo timing

## Objective and acceptance
Continue original-master animation closeout. Two-second unload is staged for review. Half-second pickup is an audition rejected for admission. Full library remains unfinished.

## Accepted decisions and constraints
Reuse complete source poses 0 through 96, with no drawing, grading, anatomy changes or per-frame placement. Later standing hold is omitted; full 142-frame source remains preserved. Unload spans the existing 2-second controller slot; pickup reverses those poses over the existing 520ms wait for comparison only. No game timers, production loaders or normal selection changed.

## Changed files and current state
This folder contains paired manifests, four APNG previews, predicted cadence schedules, two join boards, index.html, build and review scripts/reports. Native fixture: tests/test_veld_west_cargo_timing_v1.gd plus UID; tools/run_veld_west_cargo_timing_v1.py. The browser preview shows both gears and both timings. No new generation job or charge.

## Verification
776 packaging checks passed; 11 generated outputs rebuild byte-exact. Native player test: 2982 checks, zero failures, 388 presentations at 47/93/148px. Actual 60Hz unload presents all 97 poses in 121 ticks; pickup presents only 32 in 33 ticks, both gears. Entry, terminal, idle return, fresh-player snapshot continuation, source pixels and dry state passed. Representative bare/helmet native captures and both join boards viewed; browser visibility verified. 824 targeted inputs and 2936 owner-profile files unchanged during native interval. Selected ending-West 722 PNGs/38 manifests unchanged.

## Limits and remaining work
This is player/source-clock evidence, not an actual NPC route, physical contact, service loss or disk Continue acceptance. Workshop arrival explicitly faces north, so this West candidate is not naturally dispatched there. Workshop pickup currently displays idle for its 520ms wait; adding this manifest alone would not change that. Do not alter gameplay duration casually or weaken snapshot validation. Installed carry still has older case hardware, brighter skin/patch details and a different helmet fit. Walking leg stance differs naturally from the held neutral pose; it is not itself a defect. Original source foot-outline variance and upright translating helmet limits remain.

## Next action
Build a matching whole-body carry source from the same high-resolution cargo master, preserving the accepted gait cadence and planted turn stance. Review all carry/unload/pickup joins before normal admission. Pickup needs a suitable short action or an explicit lifecycle decision; this rushed reversal is not the final answer. Then controlled NPC handoffs, interruption and fresh-process Continue checks, plus remaining directions and broader library gates.
'''
(P/'HANDOFF.md').write_text(hand,encoding='utf8')
title='## Veld West cargo timing reviewed — October 4, 2026'
note=title+'\n\nOriginal-master West unload staged at existing 2-second action clock using 97 consecutive whole-source poses. Paired 520ms reverse pickup remains a rushed audition, not admitted: native 60Hz visits 97 unload poses versus 32 pickup poses. 776 packaging checks and 2982 native player checks passed, 388 presentations; 11 outputs rebuild byte-exact. 824 targeted inputs/2936 owner-profile files unchanged; selected ending-West 722 PNGs/38 manifests unchanged. Preview and join boards reviewed in character/veld-library-closeout-v1/west-cargo-timing-v1/. No loader/controller/timer change. Actual workshop arrival faces north and pickup displays idle; this is not route/physical contact/disk Continue proof. Next matching whole-body carry source and complete-family joins, then lifecycle/controller gates. Full Veld unfinished; no live job or approval gate.\n\n'
status=R/'docs/CURRENT_STATUS.md'
for attempt in range(20):
 stat=status.stat(); tmp=status.with_name(status.name+'.'+uuid.uuid4().hex+'.tmp')
 with status.open(encoding='utf8') as f:
  if title in ''.join(f.readline() for _ in range(120)): break
 with tmp.open('wb') as out, status.open('rb') as src:
  out.write(note.encode())
  while chunk:=src.read(1024*1024): out.write(chunk)
 after=status.stat()
 if (stat.st_size,stat.st_mtime_ns)==(after.st_size,after.st_mtime_ns):
  try: tmp.replace(status); break
  except PermissionError: pass
 tmp.unlink(); time.sleep(.5)
else: raise RuntimeError('Concurrent status changes prevented guarded prepend')
parent=P.parent/'HANDOFF.md'
if title not in parent.read_text(encoding='utf8'):
 with parent.open('a',encoding='utf8') as f: f.write('\n\n'+note)
files=[p for p in P.iterdir() if p.is_file() and p.name!='FINAL_REVIEW.json']+[R/'tests/test_veld_west_cargo_timing_v1.gd',R/'tests/test_veld_west_cargo_timing_v1.gd.uid',R/'tools/run_veld_west_cargo_timing_v1.py',R/'output/veld-west-cargo-timing-v1/validation.json',R/'output/veld-west-cargo-timing-v1/cadence.json']
(P/'FINAL_REVIEW.json').write_text(json.dumps({'scope':'Staged 2-second unload; rejected 520ms pickup audition; not normal admission','failures':0,'bindings':{p.relative_to(R).as_posix():sha(p) for p in files}},indent=2)+'\n',encoding='utf8')
print('Recorded cargo timing milestone:',len(files),'deliverables;',len(pngs),'selected West PNGs and',len(manifests),'manifests unchanged')
