extends SceneTree
const GUARD=preload("res://character/bill-floor-case-north-v1/finish_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var data:Dictionary=SAVE.read("user://finite-exit-admission-input.loop")
 check(not data.is_empty() and GUARD.problem(data).is_empty(),"Read real released finite-exit disk checkpoint copied to scratch")
 if failures:quit(1);return
 var plan:Dictionary=data.crew.playback.bill.water.finish_exit
 check(not plan.is_empty() and data.state.visual_time_seconds>=float(plan.release_at),"Input genuinely holds released exit")
 for fault in ["missing_case","shifted_case","prestart_clock","actor_schema","player_schema","actor_binding_type","player_binding_type","player_binding_null"]:
  var bad:Dictionary=data.duplicate(true)
  if fault in ["missing_case","shifted_case"]:
   for room in bad.state.placed_rooms:
    if room.pos==bad.crew.bill.finish_exit.cell:
     if fault=="missing_case":room.erase(FLOOR.FIELD)
     else:room[FLOOR.FIELD].anchor+=Vector2(1,0)
  elif fault=="prestart_clock":bad.state.visual_time_seconds=float(plan.started)-.001
  elif fault=="actor_schema":bad.crew.bill.finish_exit=false
  elif fault=="player_schema":bad.crew.playback.bill.water.finish_exit=false
  elif fault=="actor_binding_type":bad.crew.bill.finish_binding=7
  elif fault=="player_binding_type":bad.crew.playback.bill.water.finish_binding=7
  else:bad.crew.playback.bill.water.finish_binding=null
  check(not GUARD.problem(bad).is_empty(),"Released contact and typed pairing fault rejected")
  # Empty fake scene intentionally lacks all mutation APIs. Successful rejection
  # proves the wrapper stops before touching any scene or loaded player.
  check(not await GUARD.restore_staged({},bad),"Reject before requiring mutable scene/player")
 var legacy:Dictionary=data.duplicate(true)
 for value in [legacy.crew.bill,legacy.crew.playback.bill.water]:value.erase("finish_exit");value.erase("finish_binding")
 for room in legacy.state.placed_rooms:room.erase(FLOOR.FIELD)
 check(GUARD.problem(legacy).is_empty(),"Legacy checkpoint without candidate fields remains admitted")
 print("BILL FLOOR CASE FINISH ADMISSION V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
