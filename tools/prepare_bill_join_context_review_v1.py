"""Build a narrow actual-renderer context fixture from the established room setup."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'tools/review_bill_east_walk_join_native_v2.gd').read_text(encoding='utf-8')
prefix=source.split(' var left=Vector2.ZERO;',1)[0].replace('bill-east-walk-join-native-v2/','bill-walk-join-context-native-v1/')
body=''' var provider=preload("res://tools/bill_east_walk_join_candidate_v1.gd").new()
 var cases=[
  {"name":"helmet","state":"idle","helmet":true},
  {"name":"water","state":"tread","medium":"water"},
  {"name":"west","state":"idle","direction":"west"},
  {"name":"run","state":"run"},
  {"name":"carry","state":"carry"},
  {"name":"weld","state":"weld"},
  {"name":"construction enter","state":"weld","goal":"construction","timer":.2},
  {"name":"inspection","state":"idle","stage":"workshop_inspect","timer":1.0},
  {"name":"meal","state":"idle","stage":"life_eat","timer":1.0}]
 var results=[]
 check(grid.human_walk_join==null,"normal renderer join provider defaults to null")
 for context in cases:
  provider.reset();grid.human_walk_join=provider
  actor.dead=false;actor.helmet_equipped=false;actor.movement_medium="dry";actor.direction="east";actor.stage="";actor.goal="";actor.state="walk";actor.timer=10;actor.foot=start
  grid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=100.0;game.paused=false
  grid._get_human_frame_source("walk","east")
  actor.foot+=Vector2(8,0);game.visual_time_seconds+=.2
  var walked=grid._get_human_frame_source("walk","east")
  check(walked!=null and provider.previous_state=="walk","walking provider active before "+context.name)
  actor.state=context.state;actor.direction=context.get("direction","east");actor.helmet_equipped=context.get("helmet",false);actor.movement_medium=context.get("medium","dry");actor.stage=context.get("stage","");actor.goal=context.get("goal","");actor.timer=context.get("timer",10.0)
  game.visual_time_seconds+=.02
  var shown=grid._get_human_frame_source(actor.state,actor.direction)
  check(provider.previous_state=="" and provider.stopped<0 and provider.last_display==null,"actual dispatch cancels previous walk for "+context.name)
  grid.human_walk_join=null
  var baseline=grid._get_human_frame_source(actor.state,actor.direction)
  check(same(shown,baseline),"special activity source identical to provider-free renderer for "+context.name)
  grid.human_walk_join=provider
  if context.name in ["run","carry","weld"]:await capture(context.name,shown,actor.state+"-east",0,"selected activity")
  actor.helmet_equipped=false;actor.movement_medium="dry";actor.direction="east";actor.stage="";actor.goal="";actor.state="idle";actor.timer=10
  game.visual_time_seconds+=.02
  var returned=grid._get_human_frame_source("idle","east")
  grid.human_walk_join=null;var idle_baseline=grid._get_human_frame_source("idle","east");grid.human_walk_join=provider
  check(same(returned,idle_baseline),"return to dry idle has no stale walking or settle pose for "+context.name)
  await capture("idle after "+context.name,returned,"idle-east",0,"candidate")
  results.append({"context":context.name,"sourceMatchesBaseline":same(shown,baseline),"returnMatchesIdle":same(returned,idle_baseline)})
 game.paused=true;grid.human_walk_join=null
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"contexts":results,"captures":captures,"scope":"Actual grid getter dispatch, nine prescribed activity/equipment contexts and dry East idle return; default furnished room capture. No autonomous activity choice, physical water contact, full gear/action loops or normal candidate admission."},"\\t"));file.close()
 print("BILL JOIN CONTEXT: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_walk_join_context_native_v1.gd').write_text(prefix+body,encoding='utf-8')
runner='''from pathlib import Path
import os,json,subprocess,time
from run_bill_east_walk_join_native_v2 import owner,inputs
R=Path(__file__).resolve().parents[1];D=R/'output/bill-walk-join-context-native-v1';D.mkdir(exist_ok=False)
before=owner();frozen=inputs();env=os.environ.copy();env['APPDATA']=str(D/'scratch-appdata');Path(env['APPDATA']).mkdir()
start=time.monotonic()
with (D/'engine.log').open('w',encoding='utf-8') as log:r=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(R),'--script','res://tools/review_bill_walk_join_context_native_v1.gd','--resolution','1600x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
after=owner();current=inputs();changes=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)];source_changes=[p for p in frozen.keys()|current.keys() if frozen.get(p)!=current.get(p)]
report=json.loads((D/'report.json').read_text(encoding='utf-8')) if (D/'report.json').exists() else {};log=(D/'engine.log').read_text(encoding='utf-8')
ok=r.returncode==0 and report.get('failures')==0 and len(report.get('contexts',[]))==9 and not changes and not source_changes and not any(s in log for s in ['ERROR:','SCRIPT ERROR','WARNING:'])
v=dict(passed=ok,engineExit=r.returncode,seconds=round(time.monotonic()-start,2),checks=report.get('checks'),failures=report.get('failures'),contexts=report.get('contexts'),inputCount=len(frozen),inputChanges=source_changes,ownerNonLogCount=len(before),ownerChanges=changes,scratchAPPDATA=env['APPDATA'],normalAdmission=False)
for name,data in [('validation',v),('inputs-before',frozen),('inputs-after',current),('owner-before',before),('owner-after',after)]: (D/(name+'.json')).write_text(json.dumps(data,indent=2)+'\\n',encoding='utf-8')
print(json.dumps(v));print(log[-2400:] if not ok else '')
raise SystemExit(0 if ok else 1)
'''
(R/'tools/run_bill_walk_join_context_native_v1.py').write_text(runner,encoding='utf-8')
print('Prepared actual renderer context fixture and isolated runner.')
