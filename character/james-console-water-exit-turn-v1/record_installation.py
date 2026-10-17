from pathlib import Path
import json,hashlib,uuid,subprocess
P=Path('character/james-console-water-exit-turn-v1');Q=Path('character/james-console-water-turn-v1')
checks=[(P,n) for n in ['native-installed','native-restore','native-interruptions','native-restore-aborted','native-layout-guard','native-staged','test_owner_report_regressions']]+[(Q,'native-staged'),(Path('character/james-workstation-arrival-polish-v1'),'native-dry-equipment'),(Path('character/james-water-family-v1'),'native-installed-routes')]
for path,name in checks:
 report=json.loads((path/(name+'-validation.json')).read_text());log=(path/(name+'.log')).read_text(encoding='utf8',errors='replace');assert report['exitCode']==0 and not report['timedOut'] and report['realProfileUnchanged'],name;assert 'ERROR' not in log and 'WARNING' not in log,name

def atomic(path,fn):
 path=Path(path);before=path.read_bytes();after=fn(before)
 if before==after:return
 temp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');temp.write_bytes(after)
 if path.read_bytes()!=before:temp.unlink();raise RuntimeError('Concurrent edit: '+str(path))
 temp.replace(path)

def registry(before):
 d=json.loads(before)
 for mode,group in [('bare','actionOverrides'),('helmet','equipmentActionOverrides')]:
  for label,folder in [('entry','james-console-water-turn-v1'),('exit','james-console-water-exit-turn-v1')]:d[group]['branforth-console-water-'+label]='character/'+folder+'/'+mode+'-manifest.json'
 return (json.dumps(d,indent=2)+'\n').encode()
atomic('character/ACTIVE_ASSETS.json',registry)
for path in [P,Q]:
 def selected(before):
  d=json.loads(before);d.update(status='installed_console_motion_verified',runtimeInstalled=True,fullSetComplete=False,normalJourneys=8,normalJourneyChecks=57618,diskRestores=10,diskRestoreChecks=57746+10108,interruptionCases=48,interruptionChecks=450,geometryGuardChecks=46,geometryGuardCases=4,dryRegressionChecks=29629,ordinaryWaterRegressionChecks=2036,ownerRegression='PASS',handoff='docs/JAMES_CONSOLE_WATER_INSTALL_HANDOFF_2026-09-30.md')
  d['scope']='Selected compact quarter pixels and James-only normal flooded-console approach, simulation holds,6s service, safe egress; four room rotations and two gear. Bare breathable flooded.65, helmet submerged.95. Ten actual Continue disk restores,48 safety/gear/power interruptions, geometry guard. Not arbitrary traffic/next-goal journeys, complete exterior work or owner/full-set acceptance.'
  d['pending']=['Next-goal/traffic and full furniture/meal/equipment/exterior journeys','Cross-family material/proportion/motion polish and owner/full-set acceptance']
  return (json.dumps(d,indent=2)+'\n').encode()
 atomic(path/'selection.json',selected)
 before={str(f.relative_to(path)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (path/'frames').rglob('*.png')}
 subprocess.run(['C:/Python314/python.exe',str(path/'build.py')],check=True,stdout=subprocess.DEVNULL)
 after={str(f.relative_to(path)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (path/'frames').rglob('*.png')};assert before==after
 subprocess.run(['C:/Python314/python.exe',str(path/'verify.py')],check=True)
atomic(P/'record_staging.py',lambda b:b'"""Historical staging recorder: refuses to overwrite an installed selection."""\nimport json\nfrom pathlib import Path\nif json.loads((Path(__file__).resolve().parent/"selection.json").read_text()).get("runtimeInstalled",False):\n    raise RuntimeError("Already installed; use record_installation.py, not the historical staging recorder")\n'+b if not b.startswith(b'"""Historical staging') else b)
atomic(Q/'record_staging.py',lambda b:b'"""Historical staging recorder: refuses to overwrite an installed selection."""\nimport json\nfrom pathlib import Path\nif json.loads((Path(__file__).resolve().parent/"selection.json").read_text()).get("runtimeInstalled",False):\n    raise RuntimeError("Already installed; see current installation handoff")\n'+b if not b.startswith(b'"""Historical staging') else b)
subprocess.run(['C:/Python314/python.exe','character/james-animation-coverage-2026-09-30/audit.py'],check=True)
coverage=json.loads(Path('character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text())
for group in ['body','equipment']:
 for key in ['swim-turn-east-north','swim-turn-north-east']:assert 'james-console-water-turn-v1' in coverage[group][key]['path']
 for key in ['swim-turn-west-north','swim-turn-north-west']:assert 'james-console-water-exit-turn-v1' in coverage[group][key]['path']
lesson='''### James flooded-console controller and selected quarters installed - September 30, 2026

Static contact art is now integrated into normal James chooser/update/grid paths.
Four compact selected quarter keys replace only their own legacy quarters; old
composed half-turn pixels remain selected. Fine contact is authored console+(0,6),
inside existing36 service radius. Facing-aware East approach via left lane; explicit
simulation-owned520ms entry hold,6s North swim reading,520ms West exit hold, then
clear egress to graph(32,144). Dry stations and other actors retain base behavior.
Finish a power-interrupted partial entry before starting the different exit quarter;
no service reward. Air/fire/death supersede the work hold. Draining cancels wet
contact and starts fresh dry choice. Gear changes preserve phase only with clear
geometry. Recheck full selected clip after geometry changes, not just standing feet.

Explicit frame_at_elapsed must synchronize cosmetic state and reset its key so
ordinary playback neither repeats the quarter nor resumes a stale swim fraction.
Selected quarter clearance includes both the clip and incoming/destination full
swim profiles. Snapshot carries typed local contact/phase/elapsed/gear/aborted entry;
restore validates contact against current furniture and preserves exact Continue
pixels/paused clock/path. Save fixtures use real released architect roster/wrecks:
invented recovered entries are rejected. Malformed fields reject without exceptions.

57618 normal journey checks PASS:8 cases/4rotations/two gear, natural vitals and safety,
no clip/hold injection. Bare uses breathable flooded.65, helmet submerged.95; do not
claim bare submerged survival.57746 normal+10108 aborted restore checks PASS:10 actual
scratch checkpoint writes/reads/staged Continue restores, exact pixels/clock/actor/
path, then normal completion.450 checks cover48 phase/power/low-air/fire/drain/gear/
natural oxygen-death interruptions;46 prove4 geometry invalidations. Live flooded
poses remain clear; corpse check records first selected frame, not whole collapse.
29629 dry equipment and2036 ordinary-water route checks, owner-report regressions
PASS. Both package verifiers53/52 and refreshed522-contact checks each PASS. Builders
preserve installed selection metadata; frame hashes unchanged. Four native installed
views reviewed; profiles unchanged. No whole-set, arbitrary traffic/next-goal,
exterior dispatch or owner acceptance claim.

Contact counterfactual now explicitly loads immutable legacy manifests, since the
normal player already contains promoted quarters. Historical staging recorders
refuse to overwrite installed status. Coverage regex accepts whitespace after
helmet argument; both gear bind all4 new keys. Evidence:
docs/JAMES_CONSOLE_WATER_INSTALL_HANDOFF_2026-09-30.md. Full James goal active.
'''
for path in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 atomic(path,lambda b:b+b'\n\n'+lesson.encode() if lesson.splitlines()[0].encode() not in b else b)
status='''## James flooded-console turns and controller installed - September 30, 2026

Compact East/North and West/North quarters now selected bare/helmet. James reaches
fine contact, completes stationary entry, reads6s, completes stationary exit, then
swims to safe graph join.57618 normal journey,57746 normal restore+10108 aborted
restore,450 interruption and46 geometry-guard checks PASS. Ten actual disk Continue
restores keep exact pose/clock/path;48 safety/gear/power events honor priorities.
Dry29629, ordinary-water2036 and owner-report regressions PASS; both source packages
53/52 and selected contact522each PASS. Native views reviewed, profiles unchanged.
Builders/registry/coverage and both skills/pipeline/bible updated. Full James goal
active:next-goal/traffic, full furniture/meal/equipment/exterior journeys and broad
cross-family polish remain. No owner/full-set/release acceptance.
[Handoff](JAMES_CONSOLE_WATER_INSTALL_HANDOFF_2026-09-30.md).

'''
atomic('docs/CURRENT_STATUS.md',lambda b:status.encode()+b if status.splitlines()[0].encode() not in b else b)
files=['scripts/branforth_npc.gd','scripts/bill_npc.gd','scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json']
(P/'installed-code-hashes.json').write_text(json.dumps({f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf8')
print('Installed status, registry, coverage, source profiles and milestone lessons recorded. Full objective remains active.')
