extends "res://tests/test_veld_seated_north_continue.gd"
const BREATH="res://character/veld-seated-north-breathing-source-v1/"
const CONT_OUT="res://output/veld-breathing-continue-v1/"
func _init():
 var uid_path="res://tests/test_veld_breathing_continue.gd.uid"
 if not FileAccess.file_exists(uid_path):
  var uid=FileAccess.open(uid_path,FileAccess.WRITE);uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 call_deferred("run_breath_continue")
func fresh():
 var game=await super.fresh()
 game.grid_view.veld_player.load_manifest(BREATH+"bare-manifest.json",true)
 check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet",BREATH+"helmet-manifest.json"),"Fixture-only breath in each independent scene")
 return game
func photograph(game,name:String,texture:Texture2D,depth:float):
 game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(2,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
 var ready:=false
 for attempt in range(90):
  game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
  game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
  game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  var submitted:=false
  if game.grid_view.content_canvases.has(CELL):
   for slot in game.grid_view.content_canvases[CELL].slots:
    if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture and is_equal_approx(slot.item.sort_y,depth):submitted=true
  var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
  ready=submitted and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
  if ready:break
 check(ready,"Actual source/depth/camera ready for breath Continue capture")
 check(root.get_texture().get_image().save_png(CONT_OUT+name)==OK,"Native breath Continue capture")
func run_breath_continue():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
 if failures:quit(2);return
 DirAccess.make_dir_recursive_absolute(CONT_OUT)
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(game.veld_npc.active and game.Architects.present(game,"veld"),"Normal selected Veld release")
 game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.powered_room_cells[CELL]=true;await game.veld_npc.rebuild(game)
 var station:Dictionary={}
 for candidate in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
  if candidate.get("mode","")=="sit" and candidate.get("facing","")=="north" and candidate.has("seat_depth") and game.veld_npc.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(candidate.point)):
   station=candidate;break
 check(not station.is_empty(),"Registered clear actual lounge chair")
 if failures:quit(1);return
 var records=[]
 for equipped in [false,true]:
  for elapsed in [.8,1.4,2.2,4.6]:
   var actor=game.veld_npc;prepare(actor,station,equipped);actor.stage="life_seated";actor.timer=7.4
   game.visual_time_seconds=400;game.grid_view.veld_player.current_key="";game.grid_view.veld_player.last_time=-1
   game.grid_view._get_veld_live_frame_source(game)
   actor.timer=7.4-elapsed;game.visual_time_seconds=400+elapsed
   var shown:Texture2D=game.grid_view._get_veld_live_frame_source(game);var pixels:PackedByteArray=shown.get_image().get_data()
   var at:Vector2=position(actor);var foot:Vector2=actor.foot;var depth:float=LIFE.seated_draw_depth(actor,shown,at);var timer:float=actor.timer
   var gear:String="helmet" if equipped else "bare";var name:String="%s-%s"%[gear,str(elapsed).replace(".","-")]
   var neutral:Image=Image.load_from_file(BREATH+"frames/"+gear+"/sit-idle-north/000.png")
   check(pixels!=neutral.get_data(),"Interior checkpoint actually shows nonneutral breath")
   await photograph(game,name+"-before.png",shown,depth)
   check(SAVE.write(game,game.run_save_path)==OK,"Actual disk checkpoint write: "+SAVE.last_error)
   var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Actual disk checkpoint read: "+SAVE.last_error)
   if disk.is_empty():quit(1);return
   game.queue_free();await process_frame;game=await fresh()
   check(await SAVE.restore_staged(game,disk),"Fresh staged Continue: "+SAVE.last_error)
   game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-breathing-continue.loop"
   actor=game.veld_npc;restores+=1
   check(actor.stage=="life_seated" and actor.timer==timer and actor.helmet_equipped==equipped,"Saved held action/gear clock restored")
   var restored:Texture2D=game.grid_view._get_veld_live_frame_source(game)
   var identical:bool=restored.get_image().get_data()==pixels
   check(identical,"Fresh Continue retains interior breath pixels rather than restarting neutral")
   check(actor.foot==foot and position(actor)==at and is_equal_approx(LIFE.seated_draw_depth(actor,restored,position(actor)),depth),"Fresh Continue preserves physical/furniture/depth contact")
   game._process(.5)
   check(actor.timer==timer and game.grid_view._get_veld_live_frame_source(game).get_image().get_data()==restored.get_image().get_data(),"Paused restored breath frozen")
   await photograph(game,name+"-after.png",restored,depth)
   records.append({"gear":gear,"elapsed":elapsed,"exactPixelsRestored":identical,"timer":timer,"physicalFoot":foot,"contact":at,"depth":depth,"name":name})
   print("BREATH CONTINUE ",name," restores=",restores," failures=",failures)
 var file=FileAccess.open(CONT_OUT+"continuity.json",FileAccess.WRITE);file.store_string(JSON.stringify({"records":records,"scope":"Actual disk/fresh scene interior-held Continue, fixture-only paired sources; prescribed station entry"},"\t"))
 # Exercise actual NPC service guards at interior breaths, not the hook alone.
 for equipped in [false,true]:
  for loss in ["power","suspended"]:
   for elapsed in [.8,1.4,2.2,4.6]:
    var actor=game.veld_npc;game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
    prepare(actor,station,equipped);actor.stage="life_seated";actor.timer=7.4
    game.visual_time_seconds=400;game.grid_view.veld_player.current_key="";game.grid_view.veld_player.last_time=-1;game.grid_view._get_veld_live_frame_source(game)
    actor.timer=7.4-elapsed;game.visual_time_seconds=400+elapsed
    var before:Texture2D=game.grid_view._get_veld_live_frame_source(game);var at:Vector2=position(actor);var foot:Vector2=actor.foot
    if loss=="power":game.powered_room_cells.erase(CELL)
    else:game.occupied[CELL].suspended=true
    check(not actor.service_available(game,CELL),"Actual service lost during interior breath")
    actor.update(game,.00001)
    var after:Texture2D=game.grid_view._get_veld_live_frame_source(game)
    check(actor.stage=="life_rise" and actor.goal.is_empty(),"Actual interior service guard dispatches rise")
    check(actor.foot==foot and position(actor).distance_to(at)<.001,"Interior breath interruption preserves furniture/physical contact")
    check(is_equal_approx(LIFE.seated_draw_depth(actor,before,at),LIFE.seated_draw_depth(actor,after,position(actor))),"Interior interruption retains registered chair depth")
    var a:Image=before.get_image();var b:Image=after.get_image();var protected_same:=true;var changed:=0
    for y in range(256):
     for x in range(256):
      if a.get_pixel(x,y)!=b.get_pixel(x,y):
       changed+=1
       if not (y>146 and y<178 and abs(x-128)>10 and abs(x-128)<34):protected_same=false
    check(protected_same and changed>0,"Rise only relaxes local breath, fixed anatomy/equipment/source remains exact")
    check(actor.valid_veld_snapshot(actor.snapshot()),"Interior interrupted snapshot valid")
    interruptions+=1
 # Actual timed transitions, with neutral source joins at natural entry and exit.
 for equipped in [false,true]:
  game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
  var actor=game.veld_npc;prepare(actor,station,equipped);game.visual_time_seconds=400
  game.grid_view.veld_player.current_key="";game.grid_view.veld_player.last_time=-1
  actor.update(game,.8)
  check(actor.stage=="life_seated" and is_equal_approx(actor.timer,7.4),"Actual lowering timer enters held stage")
  var held:Texture2D=game.grid_view._get_veld_live_frame_source(game)
  var neutral:Image=Image.load_from_file(BREATH+"frames/"+("helmet" if equipped else "bare")+"/sit-idle-north/000.png")
  check(held.get_image().get_data()==neutral.get_data(),"Natural seated entry exact neutral")
  actor.timer=.00001;game.visual_time_seconds=407.4-.00001
  held=game.grid_view._get_veld_live_frame_source(game);check(held.get_image().get_data()==neutral.get_data(),"Natural full-duration held exit ends at neutral")
  actor.update(game,.00001)
  check(actor.stage=="life_rise" and is_equal_approx(actor.timer,.8),"Actual held timer starts full rise")
  check(game.grid_view._get_veld_live_frame_source(game).get_image().get_data()==neutral.get_data(),"Natural held to rise neutral join exact")
 check(restores==8 and interruptions==16,"Eight fresh interior/second-cycle restores and16actual breath interruptions")
 check(root.get_texture().get_image().save_png(CONT_OUT+"final.png")==OK,"Fresh native final")
 print("VELD BREATHING CONTINUE: %d checks,%d failures; %d fresh restores"%[checks,failures,restores]);quit(1 if failures else 0)
