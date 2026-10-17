from pathlib import Path
import hashlib,json,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-stop-bridge-v340'
for stem in ['probe','interrupt_probe']:
    v=json.loads((o/f'{stem}-validation.json').read_bytes())
    assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
traces=json.loads((o/'traces.json').read_bytes())
interrupt=json.loads((o/'interrupt-review.json').read_bytes())
assert traces['checks']==290 and traces['failures']==0 and len(traces['traces'])==48
assert all(x['pixelsEqual'] for x in traces['traces'])
assert interrupt['checks']==2289 and interrupt['failures']==0 and interrupt['samples']==272
for stem in ['probe','interrupt_probe','phase_player']:assert (o/f'{stem}.gd.uid').is_file()
media=list(o.glob('*.png'))
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0')
assert len(media)==98 and all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
report={'version':340,'entryChecks':290,'interruptChecks':2289,'failures':0,'entryScenarios':48,'interruptSamples':272,'normalChanged':False,'sourceAcceptance':False,'fullGoalComplete':False,'ownerProfileUnchanged':True,'visualReview':'Two bare/helmet four-direction entry boards actually viewed; static entry continuity only, not full motion.','priorFailedTrial':{'checks':2017,'failures':56,'finding':'Swim slot boundary subtraction could select previous pose on restart.'},'scope':'Staged exact-source player; pause, fresh player restore, restart/re-interruption and entry travel checks. Actor collision route, direction/equipment changes and whole-run Continue remain unverified.','prelaunchFreeze':False}
report['postRunCodeBindings']={str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [o/'phase_player.gd',o/'probe.gd',o/'interrupt_probe.gd',r/'scripts/crew_sprite_player.gd',r/'scripts/james_cargo_player.gd',r/'scripts/grid_canvas.gd']}
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
section='''### James staged all-phase swimming stop and restart — October 3, 2026

V340 staged James-only player reuses exact selected swim/stop textures and metadata.
Finite phase-specific stop prefixes, reverse restart rows and re-stop rows preserve
current poses. No generated art, grading, scale changes or normal loader edits.
Initial interruption trial2017checks/56failures identified floating point slot
boundary selection. Restart phase now enters just inside the intended slot;
transition movement is consumed once rather than replayed as gait distance.
Final isolated runs:290entry checks0 across48all-phase/cardinal/both-gear cases;
2289interruption checks0 across272bridge samples including pause, independent fresh
player restore, restart, re-stop, completion and moving restart entry. Owner profile
unchanged. Two bare/helmet entry boards actually viewed; all48entry pairs exact.
98LFS images, three paired scriptUIDs. Post-run hashes retained, no prelaunch freeze.

Technical/still evidence does not establish temporal smoothness or game acceptance.
Full derived motion at gameplay scales, direction/equipment changes, actual whole
bridge actor clearance, ordinary NPC interruptions and whole-run Continue remain.
Do not install until those checks pass; existing master material/proportion/cargo
and remaining hazard/death/rest/core consistency work remains. Full goal incomplete.
Handoff: character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/HANDOFF.md.
'''
record_guides(r,section,'### James actual swim-stop phase discontinuity — October 3, 2026')
(o/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 3, 2026 · Task: James staged water continuity\n\n## Objective and acceptance\nFull James animation set matching original masters, followed by consistency/polish. Incomplete.\n\n## Accepted decisions and constraints\nPreserve original selected pixels, registration, grade, tools and independent actor physics. Staged only until motion and collision evidence passes.\n\n## Current state\n'+section+'\n## Verification\n290entry/2289interruption checks0;48entry/272interruption scenarios; two entry boards viewed;98LFS PNGs; scratch profiles unchanged. Prior56failures corrected.\n\n## Next action\nReview complete derived playback at148/82/54/27, test facing/gear changes, then integrate full-bridge clearance through actual renderer/NPC route and verify whole-run Continue. Continue remaining families and master polish.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old)
data['waterPhaseBridge']={'version':340,'file':str((o/'review.json').relative_to(r)),'entryChecks':290,'interruptChecks':2289,'failures':0,'normalChanged':False,'sourceAcceptance':False}
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('V340 staged:290entry +2289interruption checks0;98LFS images;five guides/handoff/ledger updated;normal unchanged.')
