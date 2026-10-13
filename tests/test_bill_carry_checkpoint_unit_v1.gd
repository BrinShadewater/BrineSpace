extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://character/bill-carry-continuation-v1/checkpoint.gd")
const PLAYER=preload("res://character/bill-carry-continuation-v1/carry_player.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
 var data:Dictionary=SAVE.read("res://output/bill-carry-continue-candidate-v1/scratch-appdata/Godot/app_userdata/BrineSpace/bill-carry-continue.loop")
 check(not data.is_empty() and CHECKPOINT.valid_candidate(data),"Actual final disk candidate still valid with follow-up guards")
 if failures:quit(1);return
 for missing in ["playback","bill","water"]:
  var bad=data.duplicate(true)
  if missing=="playback":bad.crew.erase("playback")
  elif missing=="bill":bad.crew.playback.erase("bill")
  else:bad.crew.playback.bill.erase("water")
  check(not CHECKPOINT.valid_candidate(bad),"Absent required candidate playback rejected without runtime error")
 var saved:Dictionary=data.crew.playback.bill.water
 var player=PLAYER.new();player.frames["carry-east"]=[];player.equipment_frames["diving-helmet"]={"carry-east":[]};player.restore_snapshot(saved)
 check(player.snapshot()==saved,"Valid snapshot restores exact playback dictionary")
 var bad=saved.duplicate(true);bad.carry_binding="other";player.restore_snapshot(bad);check(player.snapshot()==saved,"Rejected binding cannot mutate playback")
 bad=saved.duplicate(true);bad.erase("motion");bad.carry_start={"started":data.state.visual_time_seconds,"gear":"diving-helmet"};check(not PLAYER.valid_carry_snapshot(bad),"Missing motion with active entry rejected without runtime error")
 bad=saved.duplicate(true);bad.carry_start={"started":NAN,"gear":"diving-helmet"};check(not PLAYER.valid_carry_snapshot(bad),"Nonfinite first-step time rejected")
 bad=saved.duplicate(true);bad.carry_start={"started":100.0,"gear":"other"};check(not PLAYER.valid_carry_snapshot(bad),"Unsupported gear rejected")
 print("BILL CARRY CHECKPOINT GUARDS: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
