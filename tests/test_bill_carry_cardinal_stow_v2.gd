extends SceneTree
var checks:=0
var failures:=0
const MASTERS=[
 ["res://character/bill-cargo-east-master-head-v1/manifest.json","res://character/bill-cargo-east-master-head-v1/helmet-manifest.json"],
 ["res://character/bill-cargo-south-master-head-v1/manifest.json","res://character/bill-cargo-south-master-head-v1/helmet-manifest.json"],
 ["res://character/bill-cargo-west-master-head-v1/manifest.json","res://character/bill-cargo-west-master-head-v1/helmet-manifest.json"],
 ["res://character/bill-cargo-north-master-head-v1/manifest.json","res://character/bill-cargo-north-master-head-v1/helmet-manifest.json"]]
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func reset(player):player.start_motion.clear();player.motion.clear();player.current_key="";player.last_time=-1
func make_player():
 var p=load("res://character/bill-carry-cardinal-runtime-v2/stow_player.gd").new()
 for pair in MASTERS:
  p.load_manifest(pair[0],true);check(p.load_equipment_manifest("diving-helmet",pair[1]),"Directional master admission")
 p.load_manifest("res://character/bill-carry-turn-identity-matrix-v5/bare-manifest.json",true)
 check(p.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-identity-matrix-v5/helmet-manifest.json"),"Full turn matrix")
 check(p.load_candidates(),"Latest cardinal sources and gradual North rise")
 return p
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 for gear in ["","diving-helmet"]:
  for direction in ["east","south","west","north"]:
   for partial in [true,false]:
    var p=make_player();p.frame("pickup",direction,9,Vector2.ONE,gear);p.frame("carry",direction,10,Vector2.ONE,gear)
    var at:float=10.1 if partial else 11.02
    if not partial:p.frame("carry",direction,10.34,Vector2.ONE,gear)
    var prior:Texture2D=p.frame("carry",direction,at,Vector2(1.03,1),gear)
    check(p.begin_stow(at,gear,direction),"Actual partial entry or gait admitted from each direction")
    var plan:Dictionary=p.stow_plan.duplicate(true);var rows:Dictionary=p.rows_for(gear)
    check(p.frame("carry","north",at,Vector2.ONE,gear)==prior,"Arrival holds exact prior source")
    check(is_equal_approx(plan.until-plan.unload_started,2.0),"Original unloading budget2seconds")
    check(rows["unload-north"].size()==14,"Improved fourteen-row North rise admitted")
    var bridge:String="carry-start-"+direction;var turn:String="carry-turn-"+direction+"-north"
    check(rows[bridge][0].get_image().get_data()==(rows[turn][0] if direction!="north" else rows["unload-north"][0]).get_image().get_data(),"Exact held source into turn/unload")
    if direction!="north":check(rows[turn].back().get_image().get_data()==rows["unload-north"][0].get_image().get_data(),"Exact North yaw-to-unload join")
    var cursor:float=at
    for row in plan.rows:
     check(p.frame("carry","north",cursor+float(row.seconds)*.5,Vector2.ONE,gear)==rows[row.key][row.index],"Every planned source advances on its authored clock")
     cursor+=float(row.seconds)
    var ending:Texture2D=p.frame("unload","north",float(plan.until)+.001,Vector2.ONE,gear)
    check(p.stow_plan.is_empty() and ending==rows["unload-north"].back(),"Completion preserves final North source")
    check(p.frame("unload","north",float(plan.until)+.05,Vector2.ONE,gear)==ending,"Completion does not restart unload")
   for cancellation in ["gear","clock","state","stale"]:
    var p=make_player();p.frame("carry",direction,20,Vector2.ONE,gear);p.frame("carry",direction,20.1,Vector2.ONE,gear)
    if cancellation=="stale":check(not p.begin_stow(20.3,gear,direction),"Reject old source cache without mutating plan");continue
    check(p.begin_stow(20.1,gear,direction),"Cancellation begins valid stow")
    p.frame("pickup" if cancellation=="state" else "carry","north",20.0 if cancellation=="clock" else 20.2,Vector2.ONE,("diving-helmet" if gear.is_empty() else "") if cancellation=="gear" else gear)
    check(p.stow_plan.is_empty(),"Discard stale stow on "+cancellation)
 print("BILL CARDINAL STOW GUARDS: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
