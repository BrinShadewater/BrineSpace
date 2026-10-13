extends SceneTree
const PLAYER=preload("res://scripts/crew_sprite_player.gd")
const SAFE=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func caption(view:SubViewport,text:String,pos:Vector2):
 var label:=Label.new();label.text=text;label.position=pos;label.add_theme_font_size_override("font_size",14);view.add_child(label)
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 if failures:quit(2);return
 var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var normal=grid.human_water_player;var staged=PLAYER.new()
 for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:staged.set(property,normal.get(property).duplicate(true))
 staged.load_manifest("res://character/bill-carry-turn-east-south-motion-v3/bare-manifest.json",true)
 check(staged.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-east-south-motion-v3/helmet-manifest.json"),"Paired staged admission")
 var board:=Image.create(2048,1280,false,Image.FORMAT_RGBA8);board.fill(Color("22343e"));var terminal_slot:=0;var joins:=[]
 var gameview:=SubViewport.new();gameview.size=Vector2i(1280,880);gameview.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(gameview)
 var background:=ColorRect.new();background.color=Color("22343e");background.size=Vector2(1280,880);gameview.add_child(background)
 for gear_index in range(2):
  var gear:String="" if gear_index==0 else "diving-helmet"
  var manifest_path:String="res://character/bill-carry-turn-east-south-motion-v3/bare-manifest.json" if gear.is_empty() else "res://character/bill-carry-turn-east-south-motion-v3/helmet-manifest.json"
  var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path));check(manifest.status=="staged_visual_review","Fixture does not claim selected runtime")
  for state in manifest.states:
   var key:String=state.id;var dirs:Array=key.split("-");var source:String=dirs[-2];var destination:String=dirs[-1]
   var row:Array=staged.frames[key] if gear.is_empty() else staged.equipment_frames[gear][key]
   check(row.size()==6,"All6staged phases admitted");check(abs(staged.cycle_seconds(key,gear)-.8)<.00001,"Original800ms clock")
   staged.motion={};staged.current_key="";staged.current_equipment="";staged.phase=0;staged.last_time=-1;staged.last_position=Vector2.ZERO
   staged.frame("carry",source,1.0,Vector2.ZERO,gear);staged.frame("carry",destination,1.01,Vector2.ZERO,gear)
   check(staged.motion.get("clip","")==key,"Actual sprite-player direction chooser selects authored quarter")
   var elapsed:=0.0
   for i in row.size():
    var raw:=Image.new();check(SAFE.load_png(raw,state.frameFiles[i])==OK,"Literal candidate PNG")
    check(raw.get_data()==row[i].get_image().get_data(),"Exact admitted candidate pixels")
    check(row[i].get_meta("crew_pivot")==Vector2(128,224) and row[i].get_meta("crew_standing_height")==148.0,"Canonical foot and density metadata")
    var mid:float=1.01+elapsed+float(state.frameDurationsMs[i])/2000.0;elapsed+=float(state.frameDurationsMs[i])/1000.0
    check(staged.frame("carry",destination,mid,Vector2.ZERO,gear)==row[i],"Advancing real sprite-player clock yields prescribed source slot")
   var terminal=staged.frame("carry",destination,1.01+elapsed+.001,Vector2.ZERO,gear)
   var carry:Array=staged.frames["carry-"+destination] if gear.is_empty() else staged.equipment_frames[gear]["carry-"+destination]
   check(terminal==carry[0] and staged.motion.get("clip","").is_empty(),"Turn completion enters actual destination carry0")
   var endimage:Image=row[-1].get_image();var nextimage:Image=terminal.get_image()
   joins.append({"gear":gear,"turn":key,"terminalCarry0ByteEqual":endimage.get_data()==nextimage.get_data()})
   for texture in [row[-1],terminal]:
    board.blend_rect(texture.get_image(),Rect2i(0,0,256,256),Vector2i(terminal_slot*256,1024));terminal_slot+=1
  for family in range(2):
   var player=staged if family==0 else normal;var row:Array=player.frames["carry-turn-east-south"] if gear.is_empty() else player.equipment_frames[gear]["carry-turn-east-south"]
   for i in row.size():board.blend_rect(row[i].get_image(),Rect2i(0,0,256,256),Vector2i(i*256,(gear_index*2+family)*256))
   for height_index in range(2):
    var height:float=82.0 if height_index==0 else 27.0;var lane:int=height_index*4+gear_index*2+family
    caption(gameview,("STAGED" if family==0 else "NORMAL")+" "+("bare" if gear.is_empty() else "helmet")+" "+str(int(height)),Vector2(8,lane*110+8))
    for i in row.size():
     var sprite:=Sprite2D.new();sprite.texture=row[i];sprite.centered=false;sprite.scale=Vector2.ONE*height/148.0;sprite.position=Vector2(220+i*160,lane*110+105)-Vector2(128,224)*sprite.scale;gameview.add_child(sprite)
 var view:=SubViewport.new();view.size=Vector2i(2048,1280);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
 var picture:=Sprite2D.new();picture.texture=ImageTexture.create_from_image(board);picture.centered=false;view.add_child(picture)
 for i in range(4):caption(view,["STAGED bare E/S","NORMAL bare E/S","STAGED helmet E/S","NORMAL helmet E/S"][i],Vector2(8,i*256+8))
 for i in range(8):caption(view,["bare S held","bare S carry0","bare E held","bare E carry0","helmet S held","helmet S carry0","helmet E held","helmet E carry0"][i],Vector2(i*256+8,1032))
 await RenderingServer.frame_post_draw
 check(view.get_texture().get_image().save_png("res://output/bill-east-south-motion-v3-staged-native/full-size.png")==OK,"Fresh native fullsize/current/terminal comparison")
 check(gameview.get_texture().get_image().save_png("res://output/bill-east-south-motion-v3-staged-native/gameplay-size.png")==OK,"Fresh native82/27comparison")
 var report:=FileAccess.open("res://output/bill-east-south-motion-v3-staged-native/player-joins.json",FileAccess.WRITE);report.store_string(JSON.stringify({"scope":"Fixture-only staged sprite-player turn admission/clock/direction/terminalcarry0;not actualNPCroute/contact/Continue or normal selection","joins":joins},"  "))
 grid.free();print("BILL EAST SOUTH MOTION V3 STAGED: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
