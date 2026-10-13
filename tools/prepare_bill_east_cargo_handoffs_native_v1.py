"""Native all-slot cargo review and production workshop unload action clock."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_east_run_master_native_v2.gd').read_text().split(' var selected=grid.human_animations')[0].replace('bill-east-run-master-native-v2/','bill-east-cargo-handoffs-native-v1/')
s+=''' var review:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-east-cargo-handoffs-master-v1/review.json"))
 var rows={};var timings={}
 for key in review.sources:
  var source:Dictionary=review.sources[key]
  player.load_manifest("res://"+str(source.manifest),true)
  rows[key]=player.frames[key].duplicate();timings[key]=player.timing[key].duplicate(true)
  check(rows[key].size()==source.files.size(),"complete cargo source bank: "+key)
  check(timings[key].durations==source.durations and timings[key].loop==source.loop,"selected clocks retained: "+key)
 for key in rows:
  player.frames[key]=rows[key];player.timing[key]=timings[key]
  var state:String=key.trim_suffix("-east")
  if not grid.human_animations.has(state):grid.human_animations[state]={}
  grid.human_animations[state]["east"]=rows[key];grid.human_animation_timing[key]=timings[key]
  for texture in rows[key]:texture.set_meta("major_bill_v2",true)
 check(same(rows["pickup-east"][0],rows["unload-east"][5]),"exact shared ground-crate endpoints")
 check(same(rows["pickup-east"][10],rows["unload-east"][0]),"exact shared held-crate endpoints")
 actor.foot=start+Vector2(8,0);game.paused=false;grid.human_walk_join=null;game.visual_time_seconds=100
 actor.state="idle";actor.stage="";actor.goal="";grid.human_animation_key=""
 await capture("idle before",grid._get_human_frame_source(actor.animation_state(),"east"),"idle-east",0,"cargo")
 var slots=[]
 for key in rows:
  var state:String=key.trim_suffix("-east");actor.state=state;actor.stage="workshop_unload" if state=="unload" else ("workshop_carry" if state=="carry" else "");actor.goal="";var cursor=0.0
  for slot in range(rows[key].size()):
   var phase:float=cursor+float(timings[key].durations[slot])/2000.0
   actor.timer=2.0-phase if state=="unload" else 10.0
   check(actor.animation_state()==state,"production animation pose agrees: "+key)
   if state=="unload":check(absf(actor.action_elapsed()-phase)<.00001,"production workshop unload clock phase")
   game.visual_time_seconds+=.1;grid.human_animation_key=key;grid.human_animation_last_time=game.visual_time_seconds;grid.human_animation_last_position=game.get_test_walker_position()/grid._cell_size();grid.human_animation_phase=phase;grid.human_animation_started=game.visual_time_seconds-phase
   player.current_equipment="";player.current_key=key;player.last_time=game.visual_time_seconds;player.last_position=game.get_test_walker_position()/grid._cell_size();player.phase=phase;player.started=game.visual_time_seconds-phase;player.motion={"state":state,"direction":"east","started":game.visual_time_seconds,"clip":""}
   var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),"east")
   check(same(shown,rows[key][slot]),"cargo source slot identity: %s/%d"%[key,slot])
   slots.append({"key":key,"slot":slot,"phase":phase,"productionElapsed":actor.action_elapsed(),"foot":[actor.foot.x,actor.foot.y]})
   await capture(key+" / pose "+str(slot),shown,key,slot,"cargo")
   cursor+=float(timings[key].durations[slot])/1000.0
  grid.human_animation_phase=cursor+.001;player.phase=cursor+.001
  if state=="unload":actor.timer=2.0-cursor-.001
  var expected:int=0 if timings[key].loop else rows[key].size()-1
  check(same(grid._get_human_frame_source(actor.animation_state(),"east"),rows[key][expected]),"loop/nonloop terminal retained: "+key)
 actor.state="idle";actor.stage="";actor.goal="";actor.timer=0;grid.human_animation_key="";game.visual_time_seconds+=.1
 await capture("idle after",grid._get_human_frame_source(actor.animation_state(),"east"),"idle-east",0,"cargo")
 game.paused=true
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"slots":slots,"scope":"25 source slots: repaired pickup11/unload6 and current carry8, exact shared cargo endpoints, loop/nonloop terminals and current idle before/after through retained furnished ColdStore renderer. Production workshop unload animation_state/action_elapsed used; pickup/carry explicit stationary source phases. Not actual cargo ownership/dispatch/completion, physical carrying route, coherent normal admission, gear/save or continuous native cadence."},"\\t"));file.close()
 print("BILL CARGO HANDOFFS: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_east_cargo_handoffs_native_v1.gd').write_text(s);(R/'tools/review_bill_east_cargo_handoffs_native_v1.gd.uid').write_text('uid://c4billeastchf1\n')
s=(R/'tools/run_bill_east_family_native_v2.py').read_text().replace('bill-east-family-native-v2','bill-east-cargo-handoffs-native-v1').replace('bill-east-family-review-v1','bill-east-cargo-handoffs-master-v1').replace('prepare_bill_east_family_native_v2','prepare_bill_east_cargo_handoffs_native_v1').replace('review_bill_east_family_native_v2','review_bill_east_cargo_handoffs_native_v1').replace('run_bill_east_family_native_v2','run_bill_east_cargo_handoffs_native_v1').replace("==50 and len(report.get('slots',[]))==175","==27 and len(report.get('slots',[]))==25")
s=s.replace("for name in ['prepare_bill", "for name in ['prepare_bill_east_cargo_handoffs_master_v1.py','build_bill_east_cargo_handoffs_master_v1.py','prepare_bill")
(R/'tools/run_bill_east_cargo_handoffs_native_v1.py').write_text(s)
print('Prepared25source slots and27retained source/world captures; production unload clock.')
