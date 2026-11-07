extends SceneTree
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func make_player():
 var p=load("res://character/bill-carry-stow-west-north-v1/stow_player.gd").new()
 p.load_manifest("res://character/bill-cargo-west-master-head-v1/manifest.json")
 p.load_manifest("res://character/bill-cargo-north-master-head-v1/manifest.json",true)
 p.load_manifest("res://character/bill-carry-turn-identity-matrix-v5/bare-manifest.json",true)
 p.load_manifest("res://character/bill-carry-west-gait-v1/bare-manifest.json",true)
 p.load_manifest("res://character/bill-carry-start-west-v1/bare-manifest.json",true)
 for path in ["res://character/bill-cargo-west-master-head-v1/helmet-manifest.json","res://character/bill-cargo-north-master-head-v1/helmet-manifest.json","res://character/bill-carry-turn-identity-matrix-v5/helmet-manifest.json","res://character/bill-carry-west-gait-v1/helmet-manifest.json","res://character/bill-carry-start-west-v1/helmet-manifest.json"]:
  check(p.load_equipment_manifest("diving-helmet",path),"Complete paired source admission")
 return p
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 for gear in ["","diving-helmet"]:
  for interrupted_start in [false,true]:
   var p=make_player();p.frame("pickup","west",9,Vector2.ONE,gear);p.frame("carry","west",10,Vector2.ONE,gear)
   var at:=10.1 if interrupted_start else 11.0
   var prior:Texture2D=p.frame("carry","west",at,Vector2.ONE,gear)
   check(p.begin_stow(at,gear),"Actual displayed first-step/contact admitted into stow")
   var plan:Dictionary=p.stow_plan.duplicate(true)
   check(p.frame("carry","north",at,Vector2.ONE,gear)==prior,"Stow begins exact prior texture despite controller changing facing")
   check(is_equal_approx(plan.until-plan.unload_started,2.0),"Original unloading stage remains exactly2seconds")
   var ending:Texture2D=p.frame("unload","north",float(plan.until)+.001,Vector2.ONE,gear)
   check(p.stow_plan.is_empty() and ending==p.rows_for(gear)["unload-north"].back(),"Completion returns original North final frame without restarting")
   check(p.frame("unload","north",float(plan.until)+.05,Vector2.ONE,gear)==ending,"Next unload tick preserves completed last source")
  for interruption in ["gear","clock","state"]:
   var p=make_player();p.frame("pickup","west",9,Vector2.ONE,gear);p.frame("carry","west",10,Vector2.ONE,gear);p.frame("carry","west",11,Vector2.ONE,gear);check(p.begin_stow(11,gear),"Priority test starts valid stow")
   if interruption=="gear":p.frame("carry","north",11.1,Vector2.ONE,"diving-helmet" if gear.is_empty() else "")
   elif interruption=="clock":p.frame("carry","north",10.9,Vector2.ONE,gear)
   else:p.frame("pickup","north",11.1,Vector2.ONE,gear)
   check(p.stow_plan.is_empty(),"Gear/backwards clock/state change discards stow plan: "+interruption)
 print("BILL STOW PLAYER GUARDS: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
