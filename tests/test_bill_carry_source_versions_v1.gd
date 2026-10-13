extends "res://tests/test_bill_carry_normal_snapshot_v1.gd"
const SELECTED_PLAYER=preload("res://scripts/bill_carry_player.gd")
const JOINT=preload("res://scripts/bill_carry_checkpoint.gd")
func make_player():
 # Version banks require the complete normal catalog, including inherited states.
 var grid=load("res://scripts/grid_canvas.gd").new()
 grid._load_major_bill_animations()
 var player=grid.human_water_player
 grid.free()
 return player
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var library=make_player()
 check(library.carry_binding()==SELECTED_PLAYER.MASTER_BINDING,"New sessions select the reviewed East master bank")
 for gear in ["","diving-helmet"]:
  var old_bank:Dictionary=library.carry_banks[SELECTED_PLAYER.BINDING]
  var new_bank:Dictionary=library.carry_banks[SELECTED_PLAYER.CURRENT_BINDING]
  var field:String="frames" if gear.is_empty() else "equipment_frames"
  var old_rows:Dictionary=old_bank[field] if gear.is_empty() else old_bank[field][gear]
  var new_rows:Dictionary=new_bank[field] if gear.is_empty() else new_bank[field][gear]
  check(not same_source(old_rows["carry-north"][0],new_rows["carry-north"][0]),"Distinct source versions are actually exercised")
  for binding in SELECTED_PLAYER.SOURCE_BINDINGS:
   for entry in [true,false]:
    for index in 6:
     var p=clone_player(library);check(p.select_binding(binding),"Select retained source bank")
     p.frame("pickup","north",9,Vector2.ONE,gear);p.frame("carry","north",10,Vector2.ONE,gear)
     var at:=10.0
     if entry:
      var elapsed:=0.001
      for previous in index:elapsed+=float(p.equipment_timing[gear]["carry-start-north"].durations[previous] if not gear.is_empty() else p.timing["carry-start-north"].durations[previous])/1000
      at+=elapsed
     else:
      p.start_motion.clear();p.current_key="carry-north";p.current_equipment=gear;p.phase=index*.14+.001;p.last_time=10;p.last_position=Vector2.ONE
     var shown:Texture2D=p.frame("carry","north",at,Vector2.ONE,gear)
     var expected_key:String="carry-start-north" if entry else "carry-north"
     check(same_source(shown,p.rows_for(gear)[expected_key][index]),"Requested exact slot reached")
     var data:Dictionary=p.snapshot();check(data.carry_binding==binding,"Snapshot binds exact source version")
     var q=clone_player(library);var original_binding:String=q.carry_binding();var original:Dictionary=q.snapshot()
     check(q.admits_loaded_snapshot(data) and q.carry_binding()==original_binding and q.snapshot()==original,"Cross-version admission has no live mutation")
     q.restore_snapshot(data);check(q.carry_binding()==binding and q.snapshot()==data,"Cross-version restore binds before reconstructing cache")
     check(same_source(q.frame("carry","north",at,Vector2.ONE,gear),shown),"Exact old/new cached artwork restored")
     for tick in range(1,9):
      var t:float=at+tick/60.0;var pos:=Vector2(1,1-tick*.001)
      check(same_source(p.frame("carry","north",t,pos,gear),q.frame("carry","north",t,pos,gear)),"Source-version future clock remains exact")
     check(p.begin_stow(at+8.0/60,gear,"north"),"Both banks can settle actual submitted source")
     var plan:Dictionary=p.snapshot();q=clone_player(library);q.restore_snapshot(plan)
     check(q.snapshot()==plan,"Arrival plan reconstructs against matching source version")
     for elapsed in [.02,.3,.7,1.3,2.0]:
      var t:float=float(plan.carry_stow.started)+elapsed
      check(same_source(p.frame("carry","north",t,Vector2.ONE,gear),q.frame("carry","north",t,Vector2.ONE,gear)),"Reverse entry and unload retain exact source after restore")
     var stable:Dictionary=q.snapshot();var stable_bank:String=q.carry_binding();var bad:Dictionary=plan.duplicate(true);bad.carry_stow.rows[0].index=99
     q.restore_snapshot(bad);check(q.snapshot()==stable and q.carry_binding()==stable_bank,"Rejected version switch leaves bank and playback intact")
 var actor=preload("res://scripts/bill_carry_npc.gd").new();actor.preview_player=library
 var joint:Dictionary={"crew":{"bill":actor.snapshot(),"playback":{"bill":{"water":library.snapshot()}}},"state":{"visual_time_seconds":0.0}}
 check(JOINT.valid(joint),"Current empty actor/player pair is valid")
 joint.crew.bill.carry_binding=SELECTED_PLAYER.BINDING
 check(not JOINT.valid(joint),"Mixed actor/player versions rejected")
 joint.crew.playback.bill.water.carry_binding=SELECTED_PLAYER.BINDING
 check(JOINT.valid(joint),"Retained empty actor/player pair remains valid")
 for gear in ["","diving-helmet"]:
  var old=clone_player(library);old.select_binding(SELECTED_PLAYER.BINDING)
  old.frame("pickup","north",9,Vector2.ONE,gear);old.frame("carry","north",10,Vector2.ONE,gear)
  var saved:Dictionary=old.snapshot();var broken=clone_player(library)
  if gear.is_empty():broken.carry_banks[SELECTED_PLAYER.BINDING].frames.erase("carry-start-north")
  else:broken.carry_banks[SELECTED_PLAYER.BINDING].equipment_frames[gear].erase("carry-start-north")
  var stable:Dictionary=broken.snapshot()
  check(not broken.admits_loaded_snapshot(saved),"Incomplete old bank cannot borrow current North entry")
  check(not broken.select_binding(SELECTED_PLAYER.BINDING) and broken.snapshot()==stable,"Malformed source bank cannot partly replace live bank")
 print("BILL SOURCE VERSIONS V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
