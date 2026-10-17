from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
n=json.loads((H/'native-selected-v1-checks.json').read_text());assert n['exit_code']==0 and not n['engine_errors'] and not n['real_profile_changed_files'] and not n['candidateLoadedExplicitly']
assert '2257 checks, 0 failures' in (H/'native-selected-v1.log').read_text()
paths=[R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json',R/'character/dr-veld-v2/clearance.json',R/'tools/review_veld_cargo_selected_v1.gd',H/'native-selected-v1.log',H/'native-selected-v1-checks.json',H/'candidate-clearance-checks-v1.json',H/'selected-rebuild-checks.json',H/'browser-installed-frame7-v1.png']
results={}
for name,count,cases,folder in [('full_expedition',18448,6,'expedition'),('expedition_interruptions',12201,4,'interruption')]:
 output=R/('output/veld-full-expedition-selected-v1' if name=='full_expedition' else 'output/veld-expedition-interruptions-selected-v1')
 v=json.loads((output/'validation.json').read_text());report=H/(folder+'-selected-review-v1/report.json');r=json.loads(report.read_text());assert v['passed'] and not v['realProfileChanges'] and r['checks']==count and r['failures']==0 and len(r['journeys'])==cases
 results[name]=dict(checks=count,journeys=cases,validation=v)
 paths.extend([output/'validation.json',output/'native.log',report,R/f'tools/review_veld_{name}_selected_v1.gd',R/f'tools/run_veld_{name}_selected_validation_v1.py'])
 paths.extend(H/(folder+'-selected-review-v1')/c['file'] for row in r['journeys'] for c in row['captures'])
frames={}
for family in ['veld-salvage-pickup-family-coherent-v1','veld-swim-carry-matrix-coherent-v1',H.name]:
 for gear in ['bare','helmet']:
  p=R/'character'/family/(gear+'-manifest.json');m=json.loads(p.read_text());assert m['status'].startswith('installed');paths.append(p)
  for s in m['states']:
   for f in s['frameFiles']:
    q=(p.parent/f).resolve();frames[q.relative_to(R).as_posix()]=sha(q)
 paths.append(R/'character'/family/'build.py')
assert len(frames)==336
paths.extend(H/f'native-selected-page-{i:02}.png' for i in range(14))
(H/'selected-evidence-v1.json').write_text(json.dumps(dict(installed=True,states=48,references=336,nativeChecks=2257,journeys=results,frameHashes=frames,hashes={p.relative_to(R).as_posix():sha(p) for p in paths},scope='Actual normal runtime loader, all336pixels/metadata/clocks and cargo turn endpoints; six complete journeys/four return restores; four safety journeys/12phase-entry restores/eight power holds/48gear guards. Broader traffic/arbitrary-phase/all safety/full-set and owner acceptance open.'),indent=2)+'\n',encoding='utf-8')
title='Veld scientific actions and swimming cargo families installed — September 30, 2026'
body='''Normal runtime now selects48gearstates/336refs across scientific work/pickup,cardinal water cargo and12direction cargo turns,with conservative clearance.2257normal-loader pixel/metadata/clock/join checks,18448six full journey and12201four interruption journey checks PASS; no candidate loads/profile injection.779baseline no-shrink checks,1108package checks and exact6manifest/336reference rebuild proof PASS. Native selected148/82/54 boards and light north/south frame7 master review captured. Engine errors0; owner profile unchanged. Literal loader overrides,registry,clearance,manifest status and builders updated; rollback inputs retained. [Handoff](../character/veld-swim-carry-turn-matrix-coherent-v1/INSTALL_HANDOFF.md),[review](http://127.0.0.1:8791/character/veld-swim-carry-turn-matrix-coherent-v1/?v=full-cargo-v1). Broader traffic/other safety/arbitrary-phase restores,remaining life/distress/recovery/death and whole-set consistency/polish remain. Full goal active; no owner/full-set/release acceptance.
'''
for rel in ['docs/CURRENT_STATUS.md','docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;old=p.read_bytes()
 if title.encode() not in old:p.write_bytes(('## '+title+'\n\n'+body+'\n').encode()+old)
lesson='''
## Cargo family normal-loader promotion — September 30, 2026

Final selection proof must remove candidate manifest loads and profile injection,
then compare all loaded frames/metadata/clocks against exact sources and repeat real
journeys/checkpoints/safety guards. Preserve the old clearance as an explicit baseline
for no-shrink checks after installing its conservative union. Registry selection is
the authority for installed metadata; builders must retain that status on regeneration
and audit the newly selected source instead of asserting the retired baseline remains
live. Prove actual regeneration byte-exact for all manifests/frame references. Keep
historical candidate evidence separate from current selected evidence and do not
claim full traffic/safety/owner/full-set acceptance from these fixtures. Veld cargo:
character/veld-swim-carry-turn-matrix-coherent-v1/INSTALL_HANDOFF.md.
'''
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 if b'Cargo family normal-loader promotion' not in p.read_bytes():
  with p.open('ab') as out:out.write(lesson.encode())
print('48selected gearstates/336refs bound to2257normal-loader/18448journey/12201guard checks; milestone and lessons recorded.')
