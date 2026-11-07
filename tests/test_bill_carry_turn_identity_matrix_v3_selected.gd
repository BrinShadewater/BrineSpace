extends SceneTree
const SAFE=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
 if failures:quit(2);return
 var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
 var board:=Image.create(3072,4096,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"));var slot:=0
 for gear in ["","diving-helmet"]:
  var path:String="res://character/bill-carry-turn-identity-matrix-v3/bare-manifest.json" if gear.is_empty() else "res://character/bill-carry-turn-identity-matrix-v3/helmet-manifest.json"
  var m:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path));check(m.status=="selected_runtime","Current selected status")
  for state in m.states:
   var key:String=state.id;var row:Array=player.frames[key] if gear.is_empty() else player.equipment_frames[gear][key]
   check(row.size()==state.frameFiles.size(),"All selected turn phases loaded")
   var elapsed:=0.0
   for i in row.size():
    var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Literal selected frame available")
    check(raw.get_data()==row[i].get_image().get_data(),"Exact normal-loader pixels")
    check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Master density and fixed foot pivot")
    var mid:float=elapsed+float(state.frameDurationsMs[i])/2000.0;elapsed+=float(state.frameDurationsMs[i])/1000.0
    check(player.frame_at_elapsed(key,mid,gear)==row[i],"Original turn source clock")
    board.blend_rect(raw,Rect2i(0,0,256,256),Vector2i(slot%12*256,slot/12*256));slot+=1
   check(player.frame_at_elapsed(key,elapsed+.001,gear)==row[-1],"Simulation elapsed accessor clamps terminal phase")
   var dirs:Array=key.split("-")
   for endpoint in [0,-1]:
    var direction:String=dirs[-2] if endpoint==0 else dirs[-1]
    var heldkey:String="pickup-"+direction;var held:Array=player.frames[heldkey] if gear.is_empty() else player.equipment_frames[gear][heldkey]
    check(row[endpoint].get_image().get_data()==held[-1].get_image().get_data(),"Exact normal-loaded static held cardinal join")
   if row.size()==11:
    var cycle:float=player.cycle_seconds(key,gear);check(abs(cycle-1.6)<.001,"Original half turn1600ms source clock")
    var matched:=false
    for d in ["east","west","north","south"]:
     var held:Array=player.frames["pickup-"+d] if gear.is_empty() else player.equipment_frames[gear]["pickup-"+d]
     if row[5].get_image().get_data()==held[-1].get_image().get_data():matched=true
    check(matched,"Half path exact current loaded cardinal midpoint")
 if DisplayServer.get_name()!="headless":
  var view:=SubViewport.new();view.size=Vector2i(3072,4096);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
  var sprite:=Sprite2D.new();sprite.texture=ImageTexture.create_from_image(board);sprite.centered=false;view.add_child(sprite);await RenderingServer.frame_post_draw
  check(view.get_texture().get_image().save_png("res://output/bill-carry-turn-identity-matrix-selected-native-v3/loaded-water-carry.png")==OK,"Fresh all184phase native capture");view.queue_free()
 grid.free();print("BILL CARRY TURN IDENTITY MATRIX V3 SELECTED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
