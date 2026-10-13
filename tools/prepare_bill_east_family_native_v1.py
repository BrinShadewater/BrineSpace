"""Exercise all family source slots and action boundaries through retained drawing."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_east_run_master_native_v2.gd').read_text(encoding='utf-8').split(' var selected=grid.human_animations')[0]
s=s.replace('bill-east-run-master-native-v2/','bill-east-family-native-v1/')
s+=''' var review:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-east-family-review-v1/review.json"))
 var rows={};var timings={}
 for key in review.sources:
  var source:Dictionary=review.sources[key]
  player.load_manifest("res://"+str(source.manifest),true)
  rows[key]=player.frames[key].duplicate();timings[key]=player.timing[key].duplicate(true)
  check(rows[key].size()==source.files.size(),"complete declared family source bank: "+key)
  check(timings[key].durations==source.durations,"original durations retained: "+key)
  check(timings[key].loop==source.loop,"original loop flag retained: "+key)
 for key in rows:
  player.frames[key]=rows[key];player.timing[key]=timings[key]
  var state:String=key.get_slice("-",0)
  if not grid.human_animations.has(state):grid.human_animations[state]={}
  grid.human_animations[state]["east"]=rows[key];grid.human_animation_timing[key]=timings[key]
  for texture in rows[key]:texture.set_meta("major_bill_v2",true)
 actor.foot=start+Vector2(8,0);game.paused=false;grid.human_walk_join=null;game.visual_time_seconds=100
 var slots=[]
 for key in rows:
  var state:String=key.get_slice("-",0);var count:int=rows[key].size()
  actor.state="idle";grid.human_animation_key="";game.visual_time_seconds+=.1
  await capture(key+" / idle before",grid._get_human_frame_source("idle","east"),"idle-east",0,"family")
  actor.state=state;var cursor=0.0
  for slot in range(count):
   game.visual_time_seconds+=.1
   var phase:float=cursor+float(timings[key].durations[slot])/2000.0
   grid.human_animation_key=key;grid.human_animation_last_time=game.visual_time_seconds
   grid.human_animation_last_position=game.get_test_walker_position()/grid._cell_size()
   grid.human_animation_phase=phase;grid.human_animation_started=game.visual_time_seconds-phase
   player.current_equipment="";player.current_key=key;player.last_time=game.visual_time_seconds
   player.last_position=game.get_test_walker_position()/grid._cell_size();player.phase=phase
   player.started=game.visual_time_seconds-phase;player.motion={"state":state,"direction":"east","started":game.visual_time_seconds,"clip":""}
   var shown:Texture2D=grid._get_human_frame_source(state,"east")
   check(same(shown,rows[key][slot]),"family source slot selected: %s / %d"%[key,slot])
   slots.append({"key":key,"slot":slot,"phase":phase,"foot":[actor.foot.x,actor.foot.y]})
   if slot in [0,count/2 as int,count-1]:await capture(key+" / pose "+str(slot),shown,key,slot,"family")
   cursor+=float(timings[key].durations[slot])/1000.0
  grid.human_animation_phase=cursor+.001;player.phase=cursor+.001
  var expected:int=0 if timings[key].loop else count-1
  check(same(grid._get_human_frame_source(state,"east"),rows[key][expected]),"loop wrap or nonloop terminal source: "+key)
  actor.state="idle";grid.human_animation_key="";game.visual_time_seconds+=.1
  await capture(key+" / idle after",grid._get_human_frame_source("idle","east"),"idle-east",0,"family")
 game.paused=true
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"slots":slots,"scope":"Ten East banks loaded together: six repaired loops/actions and four unmodified selected handoffs. Every declared source slot, loop/nonloop terminal, idle entry/exit and retained furnished ColdStore submission verified. Prescribed fixed-foot source phases with normal main/timer disabled. Direct boundary comparisons, NOT autonomous controller transitions, pickup/cargo/tool lifecycles, physical running/carrying route, gear/save acceptance or normal admission."},"\\t"));file.close()
 print("BILL EAST FAMILY: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_east_family_native_v1.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_bill_east_torch_master_native_v2.py').read_text(encoding='utf-8')
s=s.replace('bill-east-torch-master-native-v2','bill-east-family-native-v1').replace('bill-east-torch-master-v1','bill-east-family-review-v1').replace('prepare_bill_east_torch_native_v2','prepare_bill_east_family_native_v1').replace('review_bill_east_torch_master_native_v2','review_bill_east_family_native_v1').replace('run_bill_east_torch_master_native_v2','run_bill_east_family_native_v1')
s=s.replace("for name in ['prepare_bill", "review=json.loads((R/'character/bill-east-family-review-v1/review.json').read_text())\n for path in review['protectedInputs']:result[str(R/path)]=sha(R/path)\n for name in ['prepare_bill")
s=s.replace("==16 and not changes","==50 and len(report.get('slots',[]))==175 and not changes")
(R/'tools/run_bill_east_family_native_v1.py').write_text(s,encoding='utf-8')
print('175 source slots across10banks and50retained world/source boundary captures prepared.')
