"""Native source review using Bill's production construction handoff clocks."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_east_run_master_native_v2.gd').read_text().split(' var selected=grid.human_animations')[0]
s=s.replace('bill-east-run-master-native-v2/','bill-east-torch-handoffs-native-v1/')
s+=''' var review:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-east-torch-handoffs-master-v1/review.json"))
 var rows={};var timings={}
 for key in review.sources:
  var source:Dictionary=review.sources[key]
  player.load_manifest("res://"+str(source.manifest),true)
  rows[key]=player.frames[key].duplicate();timings[key]=player.timing[key].duplicate(true)
  check(rows[key].size()==source.files.size(),"complete bank: "+key)
  check(timings[key].durations==source.durations and timings[key].loop==source.loop,"original timing/loop: "+key)
 for key in rows:
  player.frames[key]=rows[key];player.timing[key]=timings[key]
  var state:String=key.trim_suffix("-east")
  if not grid.human_animations.has(state):grid.human_animations[state]={}
  grid.human_animations[state]["east"]=rows[key];grid.human_animation_timing[key]=timings[key]
  for texture in rows[key]:texture.set_meta("major_bill_v2",true)
 check(same(rows["torch-draw-east"][0],rows["torch-stow-east"][5]),"exact idle endpoints")
 check(same(rows["torch-draw-east"][5],rows["weld-east"][0]) and same(rows["torch-stow-east"][0],rows["weld-east"][0]),"exact active torch endpoints")
 actor.foot=start+Vector2(8,0);game.paused=false;grid.human_walk_join=null;game.visual_time_seconds=100
 actor.goal="";actor.state="idle";actor.timer=10;grid.human_animation_key=""
 await capture("idle before",grid._get_human_frame_source(actor.animation_state(),"east"),"idle-east",0,"controller")
 var slots=[]
 for key in rows:
  actor.goal="construction";actor.state="weld";var cursor=0.0
  for slot in range(rows[key].size()):
   var phase:float=cursor+float(timings[key].durations[slot])/2000.0
   if key=="torch-draw-east":actor.timer=phase
   elif key=="torch-stow-east":actor.timer=9.48+phase
   else:actor.timer=1.0
   var state:String=actor.animation_state()
   check(state==key.trim_suffix("-east"),"production controller state: %s/%d"%[key,slot])
   if key!="weld-east":check(absf(actor.action_elapsed()-phase)<.00001,"production action clock phase")
   else:check(actor.action_elapsed()<0,"weld keeps loop clock")
   game.visual_time_seconds+=.1;grid.human_animation_key=key;grid.human_animation_last_time=game.visual_time_seconds
   grid.human_animation_last_position=game.get_test_walker_position()/grid._cell_size();grid.human_animation_phase=phase;grid.human_animation_started=game.visual_time_seconds-phase
   player.current_equipment="";player.current_key=key;player.last_time=game.visual_time_seconds;player.last_position=game.get_test_walker_position()/grid._cell_size();player.phase=phase;player.started=game.visual_time_seconds-phase;player.motion={"state":state,"direction":"east","started":game.visual_time_seconds,"clip":""}
   var shown:Texture2D=grid._get_human_frame_source(state,"east")
   check(same(shown,rows[key][slot]),"production source identity: %s/%d"%[key,slot])
   slots.append({"key":key,"slot":slot,"timer":actor.timer,"elapsed":actor.action_elapsed(),"foot":[actor.foot.x,actor.foot.y]})
   await capture(key+" / pose "+str(slot),shown,key,slot,"controller")
   cursor+=float(timings[key].durations[slot])/1000.0
 var boundaries=[]
 for timer_value in [.519999,.520001,9.479999,9.48,9.9999]:
  actor.timer=timer_value
  var state:String=actor.animation_state();var key:String=state+"-east"
  var expected_state:String="torch-draw" if timer_value<.52 else ("torch-stow" if timer_value>=9.48 else "weld")
  var expected_slot:int=5 if state=="torch-draw" or (state=="torch-stow" and timer_value>9.99) else 0
  check(state==expected_state,"production520ms draw/stow boundary state")
  game.visual_time_seconds+=.1;grid.human_animation_key=key;grid.human_animation_last_time=game.visual_time_seconds;grid.human_animation_last_position=game.get_test_walker_position()/grid._cell_size();grid.human_animation_phase=0;grid.human_animation_started=game.visual_time_seconds
  var shown:Texture2D=grid._get_human_frame_source(state,"east")
  check(same(shown,rows[key][expected_slot]),"boundary submitted exact endpoint source")
  boundaries.append({"timer":timer_value,"state":state,"expectedSlot":expected_slot})
  await capture("boundary / "+str(timer_value),shown,key,expected_slot,"boundary")
 actor.goal="";actor.state="idle";actor.timer=0;grid.human_animation_key="";game.visual_time_seconds+=.1
 await capture("idle after",grid._get_human_frame_source(actor.animation_state(),"east"),"idle-east",0,"controller")
 game.paused=true
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"slots":slots,"boundaries":boundaries,"scope":"18 source slots and five construction-timer boundaries through production Bill animation_state/action_elapsed and retained furnished ColdStore renderer. Exact current idle/weld endpoints. Prescribed stationary timers; main processing disabled. Not autonomous construction completion, tool ownership, moving routes, gear/save or normal admission."},"\\t"));file.close()
 print("BILL TORCH HANDOFFS: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
'''
(R/'tools/review_bill_east_torch_handoffs_native_v1.gd').write_text(s)
(R/'tools/review_bill_east_torch_handoffs_native_v1.gd.uid').write_text('uid://c4billeasthtf1\n')
s=(R/'tools/run_bill_east_family_native_v2.py').read_text().replace('bill-east-family-native-v2','bill-east-torch-handoffs-native-v1').replace('bill-east-family-review-v1','bill-east-torch-handoffs-master-v1').replace('prepare_bill_east_family_native_v2','prepare_bill_east_torch_handoffs_native_v1').replace('review_bill_east_family_native_v2','review_bill_east_torch_handoffs_native_v1').replace('run_bill_east_family_native_v2','run_bill_east_torch_handoffs_native_v1').replace('==50 and len(report.get(\'slots\',[]))==175','==25 and len(report.get(\'slots\',[]))==18 and len(report.get(\'boundaries\',[]))==5')
s=s.replace("for name in ['prepare_bill", "for name in ['prepare_bill_east_torch_handoffs_master_v1.py','build_bill_east_torch_handoffs_master_v1.py','prepare_bill")
(R/'tools/run_bill_east_torch_handoffs_native_v1.py').write_text(s)
print('Prepared18 production clock/source slots and five timer boundaries;25retained captures.')
