import json,subprocess
from pathlib import Path
from milestone_notes import record_guides
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';review=bank/'release-expedition-playtest-v355';output=root/'output/james-expedition-playtest-v355'
validation=json.loads((output/'validation.json').read_text());data=json.loads((review/'lifecycle-review.json').read_text())
assert validation['exitCode']==0 and validation['ownerUnchanged'] and validation['qaOverrideRemoved']
assert data['failures']==0 and len(data['cases'])==4
assert all(c['delivered'] and c['siteUnits']==2 and c['metal']==6 and c['data']==1 and len(c['phases'])==12 for c in data['cases'])
assert (review/'expedition_playtest.gd.uid').exists()
paths=[p.relative_to(root).as_posix() for p in review.glob('*.png')];assert len(paths)==8
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=('\0'.join(paths)+'\0').encode(),capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
section=f'''### James packaged exterior expeditions — October 4, 2026

V355 unchanged V351 Windows package: {data['checks']} checks, zero failures, four
complete salvage deliveries across all airlock rotations. Normal main crew update,
survival, airlock warning/flood/drain cycle, dispatch, exterior routing, salvage,
pickup, loaded return and unloading exercised. All twelve phases reached; one site
unit removed and exactly one Metal/one Data credited only after safe return.
Helmet required by real dispatch rules. {len(data['captures'])} native follow-camera
captures (10Hz active/2Hz waiting), four lossless animated PNGs and four chronology
boards. Boards viewed: no obvious body cut-off or missing equipment in sampled
poses. Exact package hashes verified; scratch APPDATA, owner unchanged, temporary
QA override removed. Review: James bank/release-expedition-playtest-v355/review.json.

Capture last_source is recorded after drawing: during core-visible approach frames,
Architects.pod_for_display also samples this player with bare idle-south and can
overwrite that diagnostic field. Do not interpret those incidental entries as a
helmet removal. Actual actor textures/native images are the visual evidence; this
trace alone does not establish per-frame gear provenance during approach.

Scope: fixture-created nearby salvage site and airlock connected to actual core,
scripted initial floor contact/full tank, normal controller selects and executes
mission route at fixed60Hz. Not random-world dispatch ecology, real-time pacing,
long-session traffic or loaded checkpoint interruption. Animated playbacks supplied,
not continuously observed by agent; no production edits or rebuild. Gameplay
closeout now covers cargo, rest, survival, refuge routing and exterior deliveries
in the existing Windows candidate. Remaining visual acceptance is continuous
selected-motion review; cargo quilt and wide North unload stance remain polish.
'''
(review/'review.json').write_text(json.dumps({'version':355,'validation':validation,'checks':data['checks'],'cases':data['cases'],'nativeCaptures':len(data['captures']),'visualReview':'Four chronology boards viewed; no obvious body cut-off or missing equipment in sampled poses. Native animated playbacks supplied, not continuously observed by agent.','scope':data['scope'],'productionChanged':False,'packageRebuilt':False,'remaining':'Continuous selected-motion visual acceptance; cargo quilt and wide North unload stance polish. Long-session random-world/traffic and loaded checkpoint interruption not certified.'},indent=2)+'\n')
handoff='''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James exterior expeditions

## Objective and acceptance
Finish James and prepare the next game version. All four packaged exterior salvage
journeys now verified; continuous selected-motion visual acceptance remains open.

## Accepted decisions and constraints
Accepted art, forward torch, inward tablet and belt wrench retained. Owner saves
protected. No production artwork/runtime edit, rebuilt package or publication here.

## Current state
New V355 expedition fixture/UID, preparation/run/media/closeout helpers; four native
animated PNGs and four chronology boards. Existing V351 Windows candidate unchanged.

## Verification
'''+section+'''
## Next action
Finish continuous motion review without expanding the animation set. Keep known
cargo fabric and North unload stance polish explicit. The tested local candidate
is output/james-release-closeout-v351/deliverable/BrineSpace.exe with PCK alongside.
'''
(review/'HANDOFF.md').write_text(handoff);(output/'HANDOFF.md').write_text(handoff)
record_guides(root,section,'### James packaged refuge routing — October 4, 2026')
with (bank/'HANDOFF.md').open('a',encoding='utf8') as f:f.write('\n'+section)
f=bank/'material-repair-progress.json';old=f.read_bytes();ledger=json.loads(old);ledger['releaseExteriorPlaytest']={'version':355,'checks':data['checks'],'cases':4,'failures':0,'ownerUnchanged':True,'productionChanged':False,'fullVisualGoalComplete':False};assert f.read_bytes()==old;f.write_text(json.dumps(ledger,indent=2)+'\n')
f=root/'docs/JAMES_RELEASE_CLOSEOUT.md';old=f.read_bytes();text=f.read_text();text=text.replace('Continuous motion and exterior hazard playtest remain.','V355 normal packaged exterior dispatch/delivery passes all four airlock rotations. Continuous visual motion review remains.');text=text.replace('Final exterior and continuous motion review remain;','V355 complete exterior salvage deliveries pass all four airlock rotations. Final continuous motion review remains;');text=text.replace('Next action: complete exterior and continuous game-scale review','Next action: complete continuous selected-motion visual review');assert f.read_bytes()==old;f.write_text(text)
print(json.dumps({'version':355,'checks':data['checks'],'cases':4,'failures':0,'ownerUnchanged':True,'rasterLfs':8}))
