extends "res://tests/test_veld_seated_north_continue.gd"
const BREATH="res://character/veld-seated-north-breathing-source-v1/"
const BREATH_OUT="res://output/veld-seated-breathing-v1/"
func _init():
 var uid_path="res://tests/test_veld_seated_breathing.gd.uid"
 if not FileAccess.file_exists(uid_path):
  var uid=FileAccess.open(uid_path,FileAccess.WRITE);uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run_breath")
func run_breath():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
 if failures:quit(2);return
 DirAccess.make_dir_recursive_absolute(BREATH_OUT)
 var game=await fresh()
 game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(game.veld_npc.active and game.Architects.present(game,"veld"),"Normal selected architect release")
 game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.powered_room_cells[CELL]=true
 var player=game.grid_view.veld_player
 player.load_manifest(BREATH+"bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet",BREATH+"helmet-manifest.json"),"Fixture-only breathing overrides")
 var records=[]
 for rotation in range(4):
  game.occupied[CELL].rotation=rotation;await game.veld_npc.rebuild(game)
  var station:Dictionary={}
  for candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
   if candidate.get("mode","")=="sit" and candidate.get("facing","")=="north" and candidate.has("seat_depth") and game.veld_npc.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(candidate.point)):
    station=candidate;break
  check(not station.is_empty(),"Actual rotated lounge north seat registered")
  if station.is_empty():continue
  for equipped in [false,true]:
   var actor=game.veld_npc;prepare(actor,station,equipped);actor.stage="life_seated";actor.timer=7.4
   var gear:String="helmet" if equipped else "bare"
   var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BREATH+gear+"-manifest.json"))
   player.current_key="";player.last_time=-1
   var foot:Vector2=actor.foot;var at:Vector2=position(actor)
   for slot in range(7):
    # Interior samples avoid binary floating-point ambiguity at exact .6s edges.
    game.visual_time_seconds=400+slot*.6+(.001 if slot==0 else .031)
    var texture:Texture2D=game.grid_view._get_veld_live_frame_source(game)
    var expected:Image=Image.load_from_file(BREATH+manifest.states[0].frameFiles[slot%6])
    var selected_slot:=-1
    for possible in range(6):
     if texture.get_image().get_data()==Image.load_from_file(BREATH+manifest.states[0].frameFiles[possible]).get_data():selected_slot=possible;break
    check(texture.get_image().get_data()==expected.get_data(),"Actual source clock selects expected breathing pose: requested%d actual%d phase%f"%[slot,selected_slot,player.phase])
    check(actor.foot==foot and position(actor)==at,"Breathing leaves physical contact fixed")
    check(texture.get_meta("crew_seat_contact_depth",false),"Held pose retains chair depth marker")
    var depth:float=LIFE.seated_draw_depth(actor,texture,at)
    check(is_equal_approx(depth,maxf(at.y,station.seat_depth)),"Breathing retains actual chair ordering")
    game.selected_room_cell=CELL;game.selected_card_id="";game._set_grid_zoom(2,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
    var submitted:=false;var camera_ready:=false
    for attempt in range(90):
     game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
     game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
     game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
     submitted=false
     if game.grid_view.content_canvases.has(CELL):
      for item in game.grid_view.content_canvases[CELL].slots:
       if item.visible and item.item.get("kind","")=="crew" and item.item.member.texture==texture and is_equal_approx(item.item.sort_y,depth):submitted=true
     var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
     camera_ready=center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
     if submitted and camera_ready:break
    check(submitted and camera_ready,"Expected retained breathing source/depth and camera ready")
    var filename:String="rotation-%d-%s-%d.png"%[rotation,gear,slot]
    check(root.get_texture().get_image().save_png(BREATH_OUT+filename)==OK,"Native held breathing capture")
    records.append({"rotation":rotation,"gear":gear,"slot":slot,"screenshot":filename,"clock":game.visual_time_seconds,"station":station})
    var pixels:PackedByteArray=texture.get_image().get_data();var clock:float=game.visual_time_seconds
    game._process(.5)
    check(game.grid_view._get_veld_live_frame_source(game).get_image().get_data()==pixels and game.visual_time_seconds==clock,"Pause freezes breathing source and visual clock")
   actor.active=false
 check(records.size()==56,"Four actual rotations, paired gear, six breathing slots and seam")
 var evidence=FileAccess.open(BREATH_OUT+"captures.json",FileAccess.WRITE);evidence.store_string(JSON.stringify(records,"\t"))
 check(root.get_texture().get_image().save_png(BREATH_OUT+"final.png")==OK,"Fresh native final")
 print("VELD SEATED BREATHING: %d checks,%d failures; %d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
