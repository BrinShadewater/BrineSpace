extends SceneTree
const OUT="res://character/james-side-motion-review-2026-10-02/"
const PACK="res://character/james-east-cargo-heads-v3/"
var checks:=0
var failures:=0
func check(ok:bool,why:String):
 checks+=1
 if not ok:failures+=1;push_error(why)
func _initialize():call_deferred("run")
func run():
 if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
 var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.branforth_player
 var grid2=load("res://scripts/grid_canvas.gd").new();grid2._load_replacement_crew_animations();var resumed=grid2.branforth_player
 for mode in ["bare","helmet"]:
  var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PACK+mode+"-manifest.json"));var gear:String="" if mode=="bare" else "diving-helmet"
  for state in pack.states:
   var elapsed:=0.0
   for i in range(state.frameFiles.size()):
    var expected:=Image.load_from_file(PACK.path_join(state.frameFiles[i]));var actual:Texture2D=player.frame_at_elapsed(state.id,elapsed+.0001,gear)
    check(actual!=null,"Selected source exists")
    check(actual.get_image().get_data()==expected.get_data(),"Exact selected pixels "+mode+state.id+str(i))
    check(actual.get_meta("crew_pivot")==Vector2(128,224),"Selected pivot")
    check(actual.get_meta("crew_standing_height")==148.0,"Selected ruler")
    elapsed+=state.frameDurationsMs[i]/1000.0
   if not state.id.begins_with("carry-turn-"):continue
   var parts:Array=state.id.split("-");var a:String=parts[2];var b:String=parts[3]
   player.current_key="";player.motion.clear();player.last_time=-1.0
   player.frame("carry",a,0.0,Vector2.ZERO,gear,true);player.frame("carry",a,.2,Vector2(.05,0),gear,true)
   var entrance:Texture2D=player.frame("carry",b,.3,Vector2(.06,0),gear,true)
   check(entrance.get_image().get_data()==player.frame_at_elapsed(state.id,.0001,gear).get_image().get_data(),"Turn entrance exact")
   var duration:float=player.cycle_seconds(state.id,gear);var middle:float=.3+duration*.5
   player.frame("carry",b,middle,Vector2(.08,0),gear,true)
   var file:=FileAccess.open("user://james-turn-playback.bin",FileAccess.WRITE);file.store_var(player.snapshot());file.close()
   file=FileAccess.open("user://james-turn-playback.bin",FileAccess.READ);var saved:Dictionary=file.get_var();file.close()
   check(player.valid_snapshot(saved),"Valid scratch binary player snapshot")
   resumed.restore_snapshot(saved)
   for i in range(8):
    var time:float=middle+duration*.5*float(i)/7.0
    var one:Texture2D=player.frame("carry",b,time,Vector2(.08+.02*float(i)/7.0,0),gear,true)
    var two:Texture2D=resumed.frame("carry",b,time,Vector2(.08+.02*float(i)/7.0,0),gear,true)
    check(one.get_image().get_data()==two.get_image().get_data(),"Snapshot future selected pixels")
    check(player.snapshot()==resumed.snapshot(),"Snapshot future full playback clock")
   var finish:float=.3+duration+.001
   var exit:Texture2D=player.frame("carry",b,finish,Vector2(.11,0),gear,true)
   check(exit.get_image().get_data()==player.frame_at_elapsed("carry-"+b,.0001,gear).get_image().get_data(),"Destination carry0 exact")
 var f:=FileAccess.open(OUT+"selected-cargo-v3-native-evidence.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"selectedSources":128,"turnCases":12,"scope":"Actual normal grid loader:9states per gear/128refs and12paired moving-player turn entry/exit + scratch binary playback snapshot future. Not ordinary actor hauling, RunSave/Continue, room visibility or natural chooser acceptance."},"  "))
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  f=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES SELECTED CARGO V3: ",checks,"checks; ",failures,"failures;128sources/12turn cases")
 grid.free();grid2.free();quit(1 if failures else 0)
