from pathlib import Path
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent
old=(R/'character/krusher-continuous-playback-v1/native/bunk.gd').read_text()
prefix=old[:old.index(' game.wrecks.erase(HAB)')].replace('character/krusher-continuous-playback-v1/native/bunk.gd.uid','character/krusher-activity-motion-v1/turns.gd.uid').replace('character/krusher-continuous-playback-v1/review/bunk','character/krusher-activity-motion-v1/turns-v2')
prefix=prefix.replace('func run()->void:', 'func digest(data:PackedByteArray)->String:\n var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(data);return hash.finish().hex_encode()\nfunc run()->void:')
tail=''' game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"branforth","alive":true}]
 var player=preload("res://scripts/james_cargo_player.gd").new();player.game=game
 var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS))
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired candidate admission")
 game.grid_view.branforth_player=player
 var actor=game.branforth_npc
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 game.drone_fleet.orders.clear()
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.powered_room_cells.clear();game.unpowered_room_cells.clear()
 for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
  game._place_room("storage_bay",HAB+offset,true);game.powered_room_cells[HAB+offset]=true
 actor.signature="";await actor.rebuild(game);actor.active=true
 var center:Vector2=(Vector2(HAB)+Vector2.ONE*.5)*384.0;var camera:Vector2=(Vector2(HAB)+Vector2.ONE*.5)/float(game.GRID_SIZE)
 game.selected_room_cell=HAB;game._refresh_all();game._set_grid_zoom(.8,true,camera);await settle()
 for attempt in range(120):
  game.camera_zoom_target=-1;game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:break
 var vectors={"east":Vector2.RIGHT,"south":Vector2.DOWN,"west":Vector2.LEFT,"north":Vector2.UP};var episodes:Array=[]
 for family in ["carry","swim","swim-carry"]:
  for room in game.occupied.values():room.water_level=0.0 if family=="carry" else .93;room.flooded=family!="carry"
  actor.movement_medium="dry" if family=="carry" else "flooded"
  for gear in ["bare","helmet"]:
   actor.helmet_equipped=gear=="helmet"
   var equipment:String="" if gear=="bare" else "diving-helmet"
   for origin in vectors:
    for destination in vectors:
     if origin==destination:continue
     var key:String=family+"-turn-"+origin+"-"+destination;var extent:Array=player.clip_extent(key,equipment)
     var anchor:=Vector2.INF
     for id in actor.graph.get_point_ids():
      var point:Vector2=actor.graph.get_point_position(id)
      if point.distance_to(center)>130:continue
      var start:Vector2=point-Vector2(vectors[origin])*20.0;var end:Vector2=point+Vector2(vectors[destination])*65.0
      actor.foot=point;actor.direction=destination
      if family=="carry":
       if actor.travel_segment_clear(start,point,origin) and actor.travel_segment_clear(point,end,destination):anchor=point;break
      elif actor.swim_segment_clear(start,point,origin,origin) and actor.swim_segment_clear(point,end,destination,origin,false,extent):
       var cargo_clear:=true
       if family=="swim-carry":
        actor.direction=destination
        for at in [point,end]:
         actor.foot=at
         if not actor.Life.clear(actor,"cargo-turn"):cargo_clear=false
       if cargo_clear:anchor=point;break
     check(anchor.is_finite(),key+" has a real furnished-room turn clearance")
     if not anchor.is_finite():continue
     actor.foot=anchor-Vector2(vectors[origin])*20;actor.direction=origin;actor.state="walk";actor.stage="workshop_carry" if family=="carry" else "";actor.goal="";actor.goal_cell=HAB;actor.dead=false;actor.timer=0;actor.bunk_motion.clear();actor.console_motion.clear();actor.construction_motion.clear();actor.meal_return.clear();actor.air_recovery=0;actor.tank_oxygen=100;actor.breath_oxygen=100
     actor.expedition={"phase":"return","cargo":{"metal":1}} if family=="swim-carry" else {}
     actor.path=PackedVector2Array([anchor+Vector2(vectors[origin])*100]);actor.preview_player=player
     player.current_key="";player.last_time=-1;player.last_position=Vector2.ZERO;player.motion.clear();player.return_plan.clear()
     var label:String=gear+"-"+key;var elapsed:=0.0;var previous:String="";var previous_foot:=Vector2.INF;var seen:Dictionary={};var selected:Dictionary={};var count:=0;var missed:=[];var changed:=false
     var turn_time:float=.5;var duration:float=turn_time+player.cycle_seconds(key,equipment)+.3
     var stop_time:float=duration;duration+=.8 if family=="swim" else 0
     for tick in range(ceili(duration*30)+1):
      if elapsed>=turn_time and not changed:
       actor.path=PackedVector2Array([actor.foot+Vector2(vectors[destination])*160]);changed=true
      if family=="swim" and elapsed>=stop_time:actor.path.clear();actor.state="idle"
      elif tick>0:actor.move(1.0/30.0)
      game.visual_time_seconds=elapsed
      var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture!=null,"Native locomotion source exists")
      if texture==null:break
      var source:Dictionary=player.last_source.duplicate(true);var hash:String=digest(pixels(texture));var foot:Vector2=actor.foot
      if not source.is_empty():
       var bank:Dictionary=player.frames if gear=="bare" else player.equipment_frames[equipment]
       check(bank.has(source.key) and pixels(texture)==pixels(bank[source.key][source.index]),"Native turn selects current candidate pixels")
       selected[str(source.key)]=true
       if source.key==key:seen[int(source.index)]=true
      if hash!=previous or foot.distance_to(previous_foot)>2.5:
       game.camera_zoom_target=-1;game._restore_grid_view_center(actor.foot/384.0/float(game.GRID_SIZE));game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
       var world_foot:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038)+actor.observation_visual_offset()*game.get_cell_size()/384.0;var scale:float=game.get_cell_size()/384.0*65.28/148.0
       var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(world_foot-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale)
       check((root.get_stretch_transform()*game.grid_scroll.get_global_rect()).encloses(screen),"Complete turn source canvas visible")
       var image:Image=root.get_texture().get_image();var rect:Rect2i=Rect2i(screen.grow(7).intersection(Rect2(Vector2.ZERO,image.get_size())));var name:String="%s-%04d.png"%[label,count]
       image.get_region(rect).save_png(capture_dir.path_join(name))
       if count==0:image.save_png(capture_dir.path_join(label+"-full.png"))
       records.append({"file":name,"episode":label,"time":elapsed,"tick":tick,"action":actor.animation_state(),"direction":actor.direction,"source":source,"sourceHash":hash,"screen":[screen.position.x,screen.position.y,screen.size.x,screen.size.y],"crop":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"foot":[foot.x,foot.y]});count+=1;previous=hash;previous_foot=foot
      elapsed+=1.0/30.0
     var bank:Dictionary=player.frames if gear=="bare" else player.equipment_frames[equipment]
     for i in range(bank[key].size()):
      if not seen.has(i):missed.append(i)
     check(missed.is_empty(),label+" every authored turn hold reached")
     episodes.append({"label":label,"family":family,"gear":gear,"from":origin,"to":destination,"requested":key,"sources":selected.keys(),"turnSlots":seen.keys(),"missingTurnSlots":missed,"captures":count,"duration":elapsed})
     print("TURN "+label+" captures="+str(count)+" missing="+str(missed))
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"episodes":episodes,"records":records,"scope":"72 furnished-room turn trials across carry/swim/swim-carry and both gears. Staged movement legs use production move/renderer and real transition clearance at30Hz; crop captures at source/position changes. Not natural cargo dispatch, economy or autonomous route selection."},"\\t"))
 print("KRUSHER_TURNS checks=%d failures=%d episodes=%d captures=%d"%[checks,failures,episodes.size(),records.size()]);game.free();quit(1 if failures else 0)
'''
(H/'turns.gd').write_text(prefix+tail,encoding='utf-8')
runner=(H/'run_native.py').read_text().replace("review=P/'review-v2'","review=P/'turns-v2'").replace("P/'scratch-appdata'","P/'scratch-appdata-turns'").replace('krusher-activity-motion-v1/motion.gd','krusher-activity-motion-v1/turns.gd').replace('KRUSHER_ACTIVITIES','KRUSHER_TURNS')
(H/'run_turns.py').write_text(runner)
print('Prepared 72 native carry/swim turn trials')
