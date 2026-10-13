"""Run source/player density review with scratch APPDATA and byte fingerprints."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/bill-east-walk-navigation-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def owner():
 folder=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {p.relative_to(folder).as_posix():sha(p) for p in folder.rglob('*') if p.is_file() and 'logs' not in p.relative_to(folder).parts}
def inputs():
 paths={ROOT/'scenes/main.tscn',ROOT/'project.godot',ROOT/'scripts/grid_canvas.gd',ROOT/'scripts/crew_sprite_player.gd',ROOT/'scripts/bill_carry_player.gd'}
 report=json.loads((ROOT/'character/bill-east-interact-master-consistency-v1/family-review.json').read_text(encoding="utf-8"))
 paths.update(Path(f) for f in report['frozenInputs'])
 paths.update(ROOT/f for f in json.loads((ROOT/'character/bill-east-idle-master-consistency-v1/validation.json').read_text(encoding="utf-8"))['protectedInputs'])
 paths.add(ROOT/'tools/build_bill_east_master_breathing_v1.py');paths.add(ROOT/'tools/build_bill_east_idle_interact_join_v1.py');paths.add(ROOT/'tools/build_bill_east_reach_adjacent_motion_v3.py');paths.add(ROOT/'tools/review_bill_east_reach_pilot_v3.py');paths.add(ROOT/'tools/build_bill_east_reach_adjacent_motion_v4.py');paths.add(ROOT/'tools/verify_bill_reach_stature_v2.py')
 audit=json.loads((ROOT/'character/bill-full-family-consistency-2026-10-03-v1/review.json').read_text(encoding="utf-8"))
 paths.update(ROOT/f for f in audit['frozenInputs'])
 for folder in [ROOT/'character/bill-east-interact-master-consistency-v1',ROOT/'character/bill-carry-cardinal-runtime-v3',ROOT/'character/bill-east-idle-master-motion-v1',ROOT/'character/bill-east-idle-interact-joined-v1',ROOT/'character/bill-east-reach-adjacent-motion-v2',ROOT/'character/bill-east-walk-master-full-v1']:
  paths.update(p for p in folder.rglob('*') if p.is_file() and p.suffix in ['.png','.json','.gd','.uid','.txt','.py','.html'])
 for name in ['review_bill_east_walk_navigation_v1.gd','review_bill_east_walk_navigation_v1.gd.uid','ensure_bill_east_walk_navigation_v1_uids.gd','ensure_bill_east_walk_navigation_v1_uids.gd.uid','run_bill_east_walk_navigation_v1.py']:paths.add(ROOT/'tools'/name)
 for folder in ['scripts','rooms']:paths.update((ROOT/folder).rglob('*.gd'));paths.update((ROOT/folder).rglob('*.gd.uid'))
 return {str(p):sha(p) for p in sorted(paths)}
def write(name,data):(OUT/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def main():
 global OUT
 godot=Path(sys.argv[1]);assert godot.is_file()
 version=sys.argv[2] if len(sys.argv)>2 else 'v5';assert version in ['v5']
 OUT=ROOT/'output/bill-east-walk-navigation-v1';OUT.mkdir(exist_ok=False)
 before=owner();write('owner-before.json',before)
 env=os.environ.copy();scratch=OUT/'scratch-appdata';scratch.mkdir();env['APPDATA']=str(scratch)
 with (OUT/'uids.log').open('w',encoding='utf-8') as log:uid=subprocess.run([str(godot),'--headless','--path',str(ROOT),'--script','res://tools/ensure_bill_east_walk_navigation_v1_uids.gd'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=60)
 assert uid.returncode==0,'UID setup failed; exact log retained'
 frozen=inputs();write('inputs-before.json',frozen);start=time.monotonic()
 with (OUT/'engine.log').open('w',encoding='utf-8') as log:
  try:result=subprocess.run([str(godot),'--path',str(ROOT),'--script','res://tools/review_bill_east_walk_navigation_v1.gd','--resolution','1600x900','--','--output=res://'+OUT.relative_to(ROOT).as_posix()+'/'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180);code=result.returncode
  except subprocess.TimeoutExpired:code=-1
 after=owner();write('owner-after.json',after);after_inputs=inputs();write('inputs-after.json',after_inputs)
 changes=[f for f in frozen.keys()|after_inputs.keys() if frozen.get(f)!=after_inputs.get(f)];owner_changes=[f for f in before.keys()|after.keys() if before.get(f)!=after.get(f)]
 log=(OUT/'engine.log').read_text(encoding="utf-8");report=json.loads((OUT/'report.json').read_text(encoding="utf-8")) if (OUT/'report.json').exists() else {}
 passed=code==0 and report.get('failures')==0 and len(report.get('traversals',[]))==2 and all(t['arrived'] for t in report.get('traversals',[])) and not changes and not owner_changes and not any(s in log for s in ['ERROR:','SCRIPT ERROR','WARNING:'])
 validation={'passed':passed,'engineExit':code,'seconds':round(time.monotonic()-start,2),'checks':report.get('checks'),'failures':report.get('failures'),'inputCount':len(frozen),'inputChanges':changes,'ownerNonLogCount':len(before),'ownerChanges':owner_changes,'scratchAPPDATA':str(scratch),'normalAdmission':False,'worldContactTested':True,'sourceSoleDepthAccepted':False,'naturalActorMovementTested':True,'autonomousGoalChoiceTested':False}
 write('validation.json',validation);print(json.dumps(validation))
 if not passed:print('\n'.join(line for line in log.splitlines() if any(s in line for s in ['ERROR','WARNING',' at:']))[-2400:])
 return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
