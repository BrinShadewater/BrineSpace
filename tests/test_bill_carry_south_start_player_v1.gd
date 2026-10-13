extends SceneTree
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 for gear in ["","diving-helmet"]:
  var player=load("res://character/bill-carry-start-south-v1/carry_start_preview_player.gd").new()
  player.load_manifest("res://character/bill-cargo-south-master-head-v1/manifest.json")
  player.load_manifest("res://character/bill-carry-south-gait-v2/bare-manifest.json",true)
  player.load_manifest("res://character/bill-carry-start-south-v1/bare-manifest.json",true)
  check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-south-gait-v2/helmet-manifest.json"),"Paired gait admission")
  check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-start-south-v1/helmet-manifest.json"),"Paired bridge admission")
  check(player.load_equipment_manifest("diving-helmet","res://character/bill-cargo-south-master-head-v1/helmet-manifest.json"),"Original pickup admission")
  # Restore new gait after the original cargo bank contributes its pickup rows.
  check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-south-gait-v2/helmet-manifest.json"),"New equipped gait remains selected")
  var rows:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
  check(player.frame("pickup","south",9,Vector2.ONE,gear)!=null,"Actual pickup source seeds ordinary nonempty motion state")
  var entrance:Texture2D=player.frame("carry","south",10,Vector2.ONE,gear)
  check(entrance==rows["carry-start-south"][0] and player.start_motion.started==10,"Direct carry entry starts exact held pose without turn")
  var seen:={}
  for tick in range(1,20):
   var time:float=10+tick/60.0;var actual:Texture2D=player.frame("carry","south",time,Vector2.ONE+Vector2(0,tick*.002),gear)
   seen[rows["carry-start-south"].find(actual)]=true
   check(actual==player.frame_at_elapsed("carry-start-south",time-10,gear),"Direct bridge clock follows finite source sequence")
  check(seen.size()==6,"All six bridge row textures observed; final two carry identical contact pixels")
  var exit:Texture2D=player.frame("carry","south",10.34,Vector2(1,1.04),gear)
  check(exit==rows["carry-south"][0] and player.start_motion.is_empty() and is_equal_approx(player.phase,.139),"Direct entry exits exact contact0 late phase")
  var next:Texture2D=player.frame("carry","south",10.34+1.0/60,Vector2(1,1.042),gear)
  check(next==rows["carry-south"][1],"Next moving tick progresses instead of repeating whole contact hold")
  player.current_key="";player.motion.clear();player.frame("carry","south",20,Vector2.ONE,gear)
  player.frame("carry","south",20.1,Vector2.ONE,"diving-helmet" if gear.is_empty() else "")
  check(player.start_motion.is_empty(),"Gear change cancels stale first-step plan")
  player.current_key="";player.motion.clear();player.frame("carry","south",30,Vector2.ONE,gear)
  player.frame("carry","south",29.9,Vector2.ONE,gear)
  check(player.start_motion.is_empty(),"Backwards clock cancels stale first-step plan")
  player.load_manifest("res://character/bill-cargo-east-master-head-v1/manifest.json",true)
  player.load_manifest("res://character/bill-carry-turn-identity-matrix-v5/bare-manifest.json",true)
  check(player.load_equipment_manifest("diving-helmet","res://character/bill-cargo-east-master-head-v1/helmet-manifest.json"),"Original East carry admission")
  check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-identity-matrix-v5/helmet-manifest.json"),"Original South-South turn admission")
  player.start_motion.clear();player.motion.clear();player.current_key=""
  check(player.frame("carry","east",40,Vector2.ONE,gear)!=null,"Actual held South source seeds pending direction change")
  var turning:Texture2D=player.frame("carry","south",40.1,Vector2.ONE,gear)
  check(player.start_motion.is_empty() and turning==rows["carry-turn-east-south"][0],"A new carry direction turns before arming the first step")
  var stepped:Texture2D=player.frame("carry","south",40.1+player.cycle_seconds("carry-turn-east-south",gear)+.001,Vector2.ONE,gear)
  check(not player.start_motion.is_empty() and stepped==rows["carry-start-south"][0],"Completed turn arms exact held first-step entrance")
 print("BILL SOUTH FIRST STEP PLAYER: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
