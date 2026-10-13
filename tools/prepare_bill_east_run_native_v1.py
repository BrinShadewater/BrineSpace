"""Narrow prescribed-phase room review, including fixture/art hashes before engine load."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
prefix=(R/'tools/review_bill_east_walk_join_native_v2.gd').read_text(encoding='utf-8').split(' var left=Vector2.ZERO;',1)[0].replace('bill-east-walk-join-native-v2/','bill-east-run-master-native-v1/')
body=''' var selected=grid.human_animations["run"]["east"].duplicate()
 var selected_timing=grid.human_animation_timing["run-east"].duplicate(true)
 var selected_stride=grid.human_stride_distance.get("run-east")
 player.load_manifest("res://character/bill-east-run-master-v1/manifest.json",true)
 check(same(grid.human_animations["run"]["east"][0],selected[0]),"candidate loading leaves normal retained run unchanged")
 check(player.frames["run-east"].size()==6,"complete six-pose candidate loaded")
 check(player.timing["run-east"]==selected_timing,"original run timing and loop preserved")
 check(grid.human_stride_distance.get("run-east")==selected_stride,"candidate load leaves retained stride untouched")
 actor.foot=start+Vector2(8,0);game.paused=false;grid.human_walk_join=null
 for variant in ["selected","candidate"]:
  grid.human_animations["run"]["east"]=selected if variant=="selected" else player.frames["run-east"]
  for texture in grid.human_animations["run"]["east"]:texture.set_meta("major_bill_v2",true)
  actor.state="idle";grid.human_animation_key="";game.visual_time_seconds=100
  await capture("idle before",grid._get_human_frame_source("idle","east"),"idle-east",0,variant)
  var cursor=0.0
  actor.state="run"
  for slot in range(6):
   game.visual_time_seconds+=.1;grid.human_animation_key="run-east";grid.human_animation_last_time=game.visual_time_seconds;grid.human_animation_last_position=actor.foot/grid._cell_size()
   grid.human_animation_phase=cursor+float(selected_timing.durations[slot])/2000.0
   var shown=grid._get_human_frame_source("run","east")
   check(same(shown,grid.human_animations["run"]["east"][slot]),"actual retained run source selected at prescribed phase")
   await capture("run pose "+str(slot),shown,"run-east",slot,variant)
   cursor+=float(selected_timing.durations[slot])/1000.0
  grid.human_animation_phase=cursor+.001
  check(same(grid._get_human_frame_source("run","east"),grid.human_animations["run"]["east"][0]),"last-to-first source-clock seam wraps to phase zero")
  actor.state="idle";game.visual_time_seconds+=.1
  await capture("idle after",grid._get_human_frame_source("idle","east"),"idle-east",0,variant)
 game.paused=true
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"All six selected and candidate run poses through actual retained Bill renderer in furnished ColdStore at fixed foot, with staged current master idle before/after. Explicit prescribed source phases; not advancing physical running, autonomous goals, normal admission or full gear/save acceptance."},"\\t"));file.close()
 print("BILL RUN SOURCE REVIEW: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_east_run_master_native_v1.gd').write_text(prefix+body,encoding='utf-8')
runner='''from pathlib import Path
import os,json,subprocess,time,hashlib
from run_bill_east_walk_join_native_v2 import owner,inputs
R=Path(__file__).resolve().parents[1];D=R/'output/bill-east-run-master-native-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def current_inputs():
 result=inputs()
 for p in (R/'character/bill-east-run-master-v1').rglob('*'):
  if p.is_file():result[str(p)]=sha(p)
 for name in ['prepare_bill_east_run_native_v1.py','review_bill_east_run_master_native_v1.gd','review_bill_east_run_master_native_v1.gd.uid','run_bill_east_run_master_native_v1.py']:result[str(R/'tools'/name)]=sha(R/'tools'/name)
 return result
before=owner();frozen=current_inputs();env=os.environ.copy();env['APPDATA']=str(D/'scratch-appdata');Path(env['APPDATA']).mkdir();start=time.monotonic()
with (D/'engine.log').open('w',encoding='utf-8') as log:r=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(R),'--script','res://tools/review_bill_east_run_master_native_v1.gd','--resolution','1600x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
after=owner();current=current_inputs();changes=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)];source_changes=[p for p in frozen.keys()|current.keys() if frozen.get(p)!=current.get(p)]
report=json.loads((D/'report.json').read_text(encoding='utf-8')) if (D/'report.json').exists() else {};log=(D/'engine.log').read_text(encoding='utf-8');clean=not any(s in log for s in ['ERROR:','SCRIPT ERROR','WARNING:'])
ok=r.returncode==0 and report.get('failures')==0 and len(report.get('captures',[]))==16 and not changes and not source_changes and clean
v=dict(passed=ok,engineExit=r.returncode,engineLogClean=clean,seconds=round(time.monotonic()-start,2),checks=report.get('checks'),failures=report.get('failures'),captures=len(report.get('captures',[])),inputCount=len(frozen),inputChanges=source_changes,ownerNonLogCount=len(before),ownerChanges=changes,scratchAPPDATA=env['APPDATA'],normalAdmission=False)
for name,data in [('validation',v),('inputs-before',frozen),('inputs-after',current),('owner-before',before),('owner-after',after)]:(D/(name+'.json')).write_text(json.dumps(data,indent=2)+'\\n',encoding='utf-8')
print(json.dumps(v));print(log[-2400:] if not ok else '');raise SystemExit(0 if ok else 1)
'''
(R/'tools/run_bill_east_run_master_native_v1.py').write_text(runner,encoding='utf-8')
print('Prepared six-phase native room review and complete candidate/fixture fingerprint map.')
