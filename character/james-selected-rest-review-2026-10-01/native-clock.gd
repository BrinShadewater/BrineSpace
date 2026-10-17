extends "res://character/james-rest-material-continuity-v1/validate.gd"
const DEST="res://character/james-selected-rest-review-2026-10-01/"
var records:Array=[]
var clock_cases:Array=[]
var previous_pose:String=""
var current_case:String=""
func save_progress(complete:bool) -> void:
 var f:=FileAccess.open(DEST+"native-clock-evidence.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"complete":complete,"checks":checks,"failures":failures,"cases":clock_cases,"records":records,"scope":"Eight prescribed initial ordinary life_lie states, four facings/both initial gears on a clear corridor node. Normal actor.update20ms transitions and normal selected renderer, repeated sleep cycles and zero-delta freeze. No chooser/arrival/service completion/fatigue benefit, actual furniture, Continue, acquired gear, natural task or continuous native-video acceptance."},"  "))
func capture_clock(actor,force:=false) -> void:
 var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
 var player=game.grid_view.branforth_player
 var key:String=actor.animation_state()+"-"+actor.direction
 var pool:Dictionary=player.equipment_frames["diving-helmet"] if actor.helmet_equipped else player.frames
 var index:int=pool[key].find(source)
 check(index>=0,"Actual selected source identity "+key)
 var signature:String=key+":"+str(index)
 if not force and signature==previous_pose:return
 previous_pose=signature
 game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 var file:String=DEST+"native/"+current_case+"-"+str(records.size()).pad_zeros(4)+".png"
 check(root.get_texture().get_image().save_png(file)==OK,"Chronological renderer capture")
 var pt:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot/384.0*game.get_cell_size())
 records.append({"case":current_case,"key":key,"index":index,"gear":actor.helmet_equipped,"stage":actor.stage,"timer":actor.timer,"clock":game.visual_time_seconds,"footViewport":[pt.x,pt.y],"capture":file})
func run() -> void:
 var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
 if DisplayServer.get_name()=="headless" or not "brine-james-native-" in OS.get_environment("APPDATA") or OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
 root.size=Vector2i(1600,900);DirAccess.make_dir_recursive_absolute(DEST+"native")
 await fresh_scene();game.running=true;game.paused=false;game.Architects.advance_core(game,10)
 game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("corridor",CELL,true)
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 var actor=game.branforth_npc;actor.rebuild(game)
 var node:int=actor.nearest_in_room((Vector2(CELL)+Vector2.ONE*.5)*384,CELL,false)
 check(node>=0,"Clear fixture floor node")
 if node<0:save_progress(false);quit(2);return
 var initial_foot:Vector2=actor.graph.get_point_position(node)
 game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1);game._set_grid_zoom(1.8,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
 await process_frame
 game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
 game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
 var clips:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(DEST+"selected-clips.json"))
 for mode in ["bare","helmet"]:
  for direction in ["north","east","south","west"]:
   current_case=mode+"-"+direction;previous_pose=""
   actor.active=true;actor.dead=false;actor.helmet_equipped=mode=="helmet";actor.movement_medium="dry";actor.foot=initial_foot;actor.direction=direction;actor.path.clear();actor.goal="";actor.goal_cell=CELL;actor.bunk_motion.clear();actor.air_recovery=0;actor.state="idle";actor.stage="life_lie";actor.timer=.8;actor.activity="prescribed rest clock"
   for need in actor.needs:actor.needs[need]=0.0
   game.visual_time_seconds=100;game.grid_view.branforth_player.current_key="";game.grid_view.branforth_player.motion.clear()
   var pool:Dictionary=game.grid_view.branforth_player.equipment_frames["diving-helmet"] if actor.helmet_equipped else game.grid_view.branforth_player.frames
   for action in ["lie-down","sleep","get-up"]:
    var key:String=action+"-"+direction;var contract:Dictionary=clips[mode+"-"+key]
    for i in range(6):
     var file:String=("res://"+str(contract.manifest)).get_base_dir().path_join(contract.frames[i])
     var disk:=Image.load_from_file(ProjectSettings.globalize_path(file));var source:Texture2D=pool[key][i]
     check(source.get_image().get_data()==disk.get_data(),"Current selected loaded RGBA "+key+str(i))
   var seen:Dictionary={};var samples:=0;var froze:=false
   await capture_clock(actor,true)
   for step in range(800):
    actor.update(game,.02);game.visual_time_seconds+=.02;samples+=1
    check(actor.foot==initial_foot,"Clock fixture foot remains planted")
    check(actor.direction==direction and actor.helmet_equipped==(mode=="helmet"),"Clock fixture facing/gear remain stable")
    var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
    var key:String=actor.animation_state()+"-"+direction
    if actor.stage in ["life_lie","life_sleep","life_get_up"]:seen[key+":"+str(pool[key].find(source))]=true
    if actor.stage=="life_sleep" and actor.timer<8 and not froze:
     froze=true;var timer:float=actor.timer;var pixels:=source.get_image().get_data()
     for zero in range(5):
      actor.update(game,0);check(actor.timer==timer and game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Zero-delta source freeze")
    await capture_clock(actor)
    if actor.stage.is_empty():break
   check(actor.stage.is_empty() and froze,"Normal clock reaches idle and freeze sampled")
   for action in ["lie-down","sleep","get-up"]:
    for index in range(6):check(seen.has(action+"-"+direction+":"+str(index)),"Actual advancing source slot "+action+str(index))
   clock_cases.append({"id":current_case,"samples":samples,"sourceSlots":seen.size(),"seconds":game.visual_time_seconds-100,"completed":actor.stage.is_empty()});save_progress(false)
   print("JAMES SELECTED REST CLOCK CASE ",current_case," complete=",actor.stage.is_empty())
   if failures:quit(2);return
 save_progress(true)
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES SELECTED REST CLOCK: ",checks," checks; ",failures," failures; ",records.size()," captures")
 quit(1 if failures else 0)
