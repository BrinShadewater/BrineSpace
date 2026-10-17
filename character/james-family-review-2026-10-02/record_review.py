from pathlib import Path
import json,hashlib,os,uuid,re
P=Path(__file__).resolve().parent;R=P.parents[1]
inputs=json.loads((P/'inputs-before.json').read_bytes());changed=[p for p,h in inputs.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert set(changed)<= {'scripts/grid_canvas.gd'},changed
selection=json.loads((P/'current-selection.json').read_bytes())
text=(R/'scripts/grid_canvas.gd').read_text();start=text.index('elif actor == "branforth":');block=text[start:text.index('\nfunc ',start)]
C=R/'character/chief-engineer-branforth-v2';catalog=json.loads((C/'catalog.json').read_bytes());now={'bare':{},'helmet':{}}
loads=[(C/p,m) for f,m in [('body','bare'),('equipment','helmet')] for p in catalog[f]]
loads += [(R/p,'bare' if kind=='load_manifest' else 'helmet') for kind,p in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet",\s*)?"res://([^"]+)"',block)]
for p,m in loads:
    d=json.loads(p.read_bytes())
    for s in d['states']:now[m][s['id']]={'manifest':p.relative_to(R).as_posix(),'slots':len(s['frameFiles']),'standingHeight':d['standingHeight'],'pivot':d['pivot']}
assert now==selection,'Current James selection changed; re-review required'
guard={'inputCount':len(inputs),'changed':changed,'currentJamesResolvedSelectionIdentical':True,'unchangedInputCount':len(inputs)-len(changed)}
(P/'input-guard.json').write_text(json.dumps(guard,indent=2))
samples=json.loads((P/'sample-records.json').read_bytes());play=json.loads((P/'playback-evidence.json').read_bytes())
report={'completeScopedReview':True,'fullGoalComplete':False,'inputCount':len(inputs),'inputsUnchanged':True,'sampleReferencesReviewed':len(samples['records']),'boardsReviewed':16,'sourcePlayback':play,'findings':['No uniform height rescale justified by sampled standing sources; crouch/stride/cargo extents vary with pose.','East interact/inspect active tablet body and tablet look cooler/purpler than registered idle/torch/cargo sources, both gears. Current selected tablet-east-belt-fixed-source-v2 loads after inspect-material-continuity-v1. Further local material revision needs full cycle and belt-wrench/helmet/alpha/geometry preservation.','Side cargo faces/bodies and West tablet posture warrant full motion/proportion follow-up; not declared broken or accepted by three samples.','Legacy kneel/repair sources differ from standing torch work; actual branforth repair hooks select draw/weld/stow. Source membership alone does not establish natural action admission.'],'limits':'Source only: first/middle/last samples from13dry cardinal families/both gears, repeated registered idle0 masters. Browser time-separated playback poses inspected, not all12seconds/150 presentation frames or all source slots. No native scene/profile/Continue, furniture, sleep/water/death/seated/equipment/turn-family completion or owner acceptance.'}
report['inputsUnchanged']=not changed;report['inputGuard']=guard
(P/'review-evidence.json').write_text(json.dumps(report,indent=2))
note=f'''

## James primary dry family comparison — October 2, 2026

`character/james-family-review-2026-10-02` traces actual catalog plus ordered
grid_canvas overrides:337bare/247helmet selected states (coverage, not acceptance).
Six movement families and seven work families across four facings/two gears:
416sample references including repeated idle0 masters reviewed in16boards.
First/middle/last images registered by source pivot/documented standing ruler
to148, without changing any artwork. {len(inputs)-len(changed)}of{len(inputs)}frozen inputs
unchanged. Loader bytes changed during review; re-resolved current James selection
is identical for all584states; all frozen manifests/sources unchanged. Twelve-second constructed source-clock GIF
compares master/walk/carry/inspect/weld; browser time-separated initial/active
phases inspected.80ms presentation skips shorter source slots; independent cycles
repeat for comparison, not natural task chains or continuous native video proof.

Next concrete material target: East active tablet body/tablet looks cooler/purpler
than idle/torch/cargo in both gears. Selected tablet-east-belt-fixed-source-v2
overrides earlier inspect-material-continuity-v1. Do not edit an overridden pack
or globally resize/grade James from a local finding. Preserve belt wrench, paired
shared helmet, exact entrance/return, alpha, body geometry, clocks and source
provenance in any revision; inspect the entire cycle before installing it.
No uniform height correction justified by these samples. Pose/cargo extent is
not standing height. Side cargo face/body and West tablet posture need fuller
motion/proportion review. Legacy kneel/repair membership is distinct from actual
custom standing torch draw/weld/stow admission. No new source/runtime selection.

Review scope excludes full-slot/full-motion/native furniture and natural tasks,
other seated/rest/water/death/equipment/turn families and final owner acceptance.
Full James/master/cross-family objective remains active and incomplete.
'''
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    data=path.read_bytes()
    if b'## James primary dry family comparison' in data:continue
    updated=note.lstrip().encode()+b'\n'+data if path.name=='CURRENT_STATUS.md' else data+note.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(updated)
    assert path.read_bytes()==data;os.replace(tmp,path)
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: 2026-10-02 · Project: Brine Space · Task: James primary family comparison

## Objective and acceptance
Full James/master/style/perspective/height/proportion/grade set and consistency
goal active and incomplete. This is primary dry source comparison evidence only.

## Accepted decisions and constraints
Actual ordered loader selection; preserve matte masters, belt wrench, shared
helmet, natural pose perspective, geometry and clocks. No blanket rescale.

## Current state
New selection snapshot,416registered sampled references/16reviewed boards,
12-second constructed comparison GIF, provenance and frozen input hashes.
Five guides updated with findings and bounded scope. No production/art edits.

## Verification
{len(inputs)-len(changed)}of{len(inputs)}inputs unchanged; loader bytes changed during review,
current resolved James selection identical for all584states. Source samples
and browser time-separated initial/active playback phases reviewed; not every
slot or continuous video. No native tests required for review-only artifacts.

## Next action
East tablet full-cycle material review/correction against current idle/torch/
cargo, both gears. Selected belt-fixed-source-v2 overrides previous grade pack.
Preserve wrench/helmet/alpha/geometry/endpoints and assess full cycle before
installing. Side cargo and West tablet proportion follow-up, remaining full
family/context review and owner acceptance. Browser review service cleanup pending.
''')
print('Recorded16-board source review; input guard:',guard)
