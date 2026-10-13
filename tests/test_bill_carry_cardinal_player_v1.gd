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
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var player=load("res://character/bill-carry-cardinal-runtime-v1/carry_player.gd").new()
 for pair in MASTERS:
  player.load_manifest(pair[0],true);check(player.load_equipment_manifest("diving-helmet",pair[1]),"Original directional master admission")
 player.load_manifest("res://character/bill-carry-turn-identity-matrix-v5/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-identity-matrix-v5/helmet-manifest.json"),"Original full turn matrix")
 check(player.load_candidates(),"Latest eight paired gait/bridge banks admitted")
 for gear in ["","diving-helmet"]:
  var rows:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
  for direction in ["east","south","west","north"]:
   reset(player);check(player.frame("pickup",direction,9,Vector2.ONE,gear)!=null,"Original pickup present")
   check(player.frame("carry",direction,10,Vector2.ONE,gear)==rows["carry-start-"+direction][0],"Direct entry exact held row")
   var seen:={}
   for tick in range(1,20):
    var time:float=10+tick/60.0;var texture=player.frame("carry",direction,time,Vector2.ONE+Vector2(tick*.002,0),gear);seen[rows["carry-start-"+direction].find(texture)]=true
    check(texture==player.frame_at_elapsed("carry-start-"+direction,time-10,gear),"Finite authored entry clock")
   check(seen.size()==6,"Every direct bridge row observed")
   check(player.frame("carry",direction,10.34,Vector2(1.04,1),gear)==rows["carry-"+direction][0] and player.start_motion.is_empty(),"Exact contact exit")
   check(player.frame("carry",direction,10.34+1.0/60,Vector2(1.042,1),gear)==rows["carry-"+direction][1],"Next tick progresses to next leg pose")
   for cancellation in ["gear","clock","state"]:
    reset(player);player.frame("carry",direction,20,Vector2.ONE,gear)
    player.frame("pickup" if cancellation=="state" else "carry",direction,19.9 if cancellation=="clock" else 20.1,Vector2.ONE,("diving-helmet" if gear.is_empty() else "") if cancellation=="gear" else gear)
    check(player.start_motion.is_empty(),"Cancel stale bridge on "+cancellation)
   for destination in ["east","south","west","north"]:
    if destination==direction:continue
    reset(player);player.frame("carry",direction,30,Vector2.ONE,gear)
    var key:String="carry-turn-"+direction+"-"+destination
    check(player.frame("carry",destination,30.1,Vector2.ONE,gear)==rows[key][0] and player.start_motion.is_empty(),"Facing change turns before first step")
    var end:float=30.1+player.cycle_seconds(key,gear)+.001
    check(player.frame("carry",destination,end,Vector2.ONE,gear)==rows["carry-start-"+destination][0] and player.start_motion.direction==destination,"Each completed quarter/half turn opens correct directional entry")
 print("BILL CARDINAL CARRY PLAYER: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
