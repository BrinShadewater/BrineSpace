extends "res://tests/test_bill_carry_normal_snapshot_v1.gd"
const SELECTED=preload("res://scripts/bill_carry_player.gd")
const JOINT=preload("res://scripts/bill_carry_checkpoint.gd")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var library=make_player()
 check(library.carry_binding()==SELECTED.CURRENT_BINDING,"New sessions select South3/North2")
 for gear in ["","diving-helmet"]:
  var versions:=[]
  for binding in SELECTED.SOURCE_BINDINGS:
   var bank:Dictionary=library.carry_banks[binding]
   versions.append(bank.frames if gear.is_empty() else bank.equipment_frames[gear])
  check(not same_source(versions[0]["carry-north"][0],versions[1]["carry-north"][0]),"North1 and North2 differ")
  check(same_source(versions[1]["carry-north"][0],versions[2]["carry-north"][0]),"South admission retains selected North2 bytes")
  check(same_source(versions[0]["carry-south"][0],versions[1]["carry-south"][0]),"Both prior versions preserve South2 bytes")
  check(not same_source(versions[1]["carry-south"][0],versions[2]["carry-south"][0]),"South3 actually differs from South2")
  for binding in SELECTED.SOURCE_BINDINGS:
   for direction in ["north","south"]:
    for entry in [true,false]:
     for index in 6:
      var p=clone_player(library);check(p.select_binding(binding),"Select complete retained source version")
      p.frame("pickup",direction,9,Vector2.ONE,gear);p.frame("carry",direction,10,Vector2.ONE,gear)
      var at:=10.0;var key:String="carry-start-"+direction if entry else "carry-"+direction
      if entry:
       var elapsed:=.001;var clock:Dictionary=p.timing if gear.is_empty() else p.equipment_timing[gear]
       for previous in index:elapsed+=float(clock[key].durations[previous])/1000
       at+=elapsed
      else:
       p.start_motion.clear();p.current_key=key;p.current_equipment=gear;p.phase=index*.14+.001;p.last_time=10;p.last_position=Vector2.ONE
      var shown:Texture2D=p.frame("carry",direction,at,Vector2.ONE,gear)
      check(same_source(shown,p.rows_for(gear)[key][index]),"Requested source slot reached")
      var saved:Dictionary=p.snapshot();var q=clone_player(library);var stable:Dictionary=q.snapshot()
      check(saved.carry_binding==binding,"Snapshot binds exact paired North/South source version")
      check(q.admits_loaded_snapshot(saved) and q.snapshot()==stable,"Detached admission leaves live state intact")
      q.restore_snapshot(saved);check(q.carry_binding()==binding and q.snapshot()==saved,"Cross-version restore reconstructs source/cache against bound bank")
      check(same_source(q.frame("carry",direction,at,Vector2.ONE,gear),shown),"Immediate exact source pixels restored")
      for tick in range(1,9):
       var t:float=at+tick/60.0;var pos:=Vector2(1,1+tick*.001*(-1 if direction=="north" else 1))
       check(same_source(p.frame("carry",direction,t,pos,gear),q.frame("carry",direction,t,pos,gear)),"Restored entry/gait future matches uninterrupted source clock")
      check(p.begin_stow(at+8.0/60,gear,direction),"Actual submitted source can settle and turn to North")
      saved=p.snapshot();q=clone_player(library);q.restore_snapshot(saved)
      check(q.snapshot()==saved,"Arrival reconstruction uses matching South/North program")
      for elapsed in [.02,.3,.7,1.3,2.0]:
       var t:float=float(saved.carry_stow.started)+elapsed
       check(same_source(p.frame("carry","north",t,Vector2.ONE,gear),q.frame("carry","north",t,Vector2.ONE,gear)),"Settle/turn/unload source clock survives restore")
      stable=q.snapshot();var bad:Dictionary=saved.duplicate(true);bad.carry_stow.rows[0].index=99
      q.restore_snapshot(bad);check(q.snapshot()==stable,"Malformed plan cannot mutate current version or playback")
  for direction in ["north","south"]:
   var p=clone_player(library);p.select_binding(SELECTED.NORTH2_BINDING)
   p.frame("pickup",direction,9,Vector2.ONE,gear);p.frame("carry",direction,10,Vector2.ONE,gear)
   var saved:Dictionary=p.snapshot();var broken=clone_player(library);var key:String="carry-start-"+direction
   if gear.is_empty():broken.carry_banks[SELECTED.NORTH2_BINDING].frames.erase(key)
   else:broken.carry_banks[SELECTED.NORTH2_BINDING].equipment_frames[gear].erase(key)
   var stable:Dictionary=broken.snapshot()
   check(not broken.admits_loaded_snapshot(saved),"Incomplete retained bank cannot borrow from current North/South source")
   check(not broken.select_binding(SELECTED.NORTH2_BINDING) and broken.snapshot()==stable,"Incomplete bank selection remains atomic")
 var actor=preload("res://scripts/bill_carry_npc.gd").new();actor.preview_player=library
 for binding in SELECTED.SOURCE_BINDINGS:
  library.select_binding(binding)
  var data:Dictionary={"crew":{"bill":actor.snapshot(),"playback":{"bill":{"water":library.snapshot()}}},"state":{"visual_time_seconds":0.0}}
  check(JOINT.valid(data),"Each matching actor/player version remains admitted")
  for other in SELECTED.SOURCE_BINDINGS:
   if other==binding:continue
   data.crew.bill.carry_binding=other
   check(not JOINT.valid(data),"Every mismatched actor/player version rejected")
 print("BILL SOURCE VERSIONS V2: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
