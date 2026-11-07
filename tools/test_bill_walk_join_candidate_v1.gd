extends SceneTree
var checks=0
var failures=0
func check(ok:bool):
 checks+=1
 if not ok:failures+=1;push_error("Join interruption/branch check failed")
func _init():
 var own="res://tools/test_bill_walk_join_candidate_v1.gd.uid"
 if not FileAccess.file_exists(own):
  var f=FileAccess.open(own,FileAccess.WRITE);f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");f.close()
 call_deferred("run")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"))
 var actor=preload("res://scripts/bill_npc.gd").new();actor.helmet_equipped=false;actor.movement_medium="dry"
 var p=preload("res://scripts/crew_sprite_player.gd").new();p.load_manifest("res://character/bill-east-walk-master-full-v1/manifest.json")
 var join=preload("res://tools/bill_east_walk_join_candidate_v1.gd").new();var idle=join.idle
 for slot in range(48):
  var source=p.frames["walk-east"][slot];join.reset()
  check(join.frame("idle","east",10.0,idle,0,actor)==idle)
  check(join.frame("walk","east",10.1,source,slot,actor)==idle)
  check(join.frame("walk","east",10.3,source,slot,actor)==source)
  check(join.frame("idle","east",10.32,idle,0,actor)==source)
  var anchor=int((slot+6)/12)%4*12
  check(join.frame("idle","east",10.39,idle,0,actor)==join.middle[anchor])
  check(join.frame("idle","east",10.39,idle,0,actor)==join.middle[anchor])
  check(join.frame("walk","east",10.4,source,slot,actor)==join.middle[anchor])
  check(join.frame("walk","east",10.48,source,slot,actor)==join.middle[anchor])
  check(join.frame("walk","east",10.55,source,slot,actor)==source)
  check(join.frame("idle","east",10.57,idle,0,actor)==source)
  check(join.frame("idle","east",10.8,idle,0,actor)==idle)
 join.reset();join.frame("idle","east",20,idle,0,actor);join.frame("walk","east",20.1,p.frames["walk-east"][0],0,actor)
 check(join.frame("idle","east",20.12,idle,0,actor)==idle)
 check(join.frame("idle","east",20.2,idle,0,actor)==idle)
 actor.helmet_equipped=true;check(join.frame("walk","east",21,idle,0,actor)==idle);check(join.previous_state=="")
 actor.helmet_equipped=false;actor.movement_medium="water";check(join.frame("walk","east",22,idle,0,actor)==idle)
 actor.movement_medium="dry";check(join.frame("walk","west",23,idle,0,actor)==idle)
 check(join.frame("interact","east",24,idle,0,actor)==idle)
 var file=FileAccess.open("res://output/bill-walk-join-branches-v1/report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"stopSlots":48,"pauseRepeat":true,"restartDuringSettle":true,"shortMoveCancellation":true,"gearWaterOtherStateBypass":true}));file.close()
 print("BILL JOIN BRANCHES: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
