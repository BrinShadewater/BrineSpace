extends "res://tests/test_veld_seated_south_selected.gd"
const CONTEXT_OUT="res://output/veld-seated-side-context-v1/"
func _init():
	var path="res://tests/test_veld_seated_side_context.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(CONTEXT_OUT)
	var records:Array=[]
	for room_id in ["crew_lounge","observation_room"]:
		var game=await fresh()
		game.paused=false;game.Architects.advance_core(game,10);game.paused=true
		check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant real context fixture")
		game.selected_rotation=0;game._place_room(room_id,CELL,true);game.powered_room_cells[CELL]=true
		for quarter in 4:
			game.occupied[CELL].rotation=quarter
			await game.veld_npc.rebuild(game)
			var data:Dictionary=game.veld_npc.geometry[CELL]
			var stations:Array=game.veld_npc.RoomActivity.stations(data)
			var seated:Array=stations.filter(func(s):return s.get("mode","") in ["sit","read"])
			check(not seated.is_empty(),"Actual default retains supported seated service")
			check(not seated.any(func(s):return s.facing in ["east","west"]),"No current East/West seated service eligibility")
			check(seated.all(func(s):return s.facing==("north" if room_id=="crew_lounge" else "south")),"Actual default facing follows furnishing/resolver")
			var props:Array=[]
			for prop in data.props:
				props.append({"id":prop.id,"role":preload("res://scripts/room_asset_library.gd").role_of(prop),"rect":prop.rect,"sortY":prop.get("sort_y",prop.rect.end.y)})
			game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
			var ready:=false
			for attempt in 90:
				game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
				game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
				ready=game.grid_view.content_canvases.has(CELL) and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
				if ready:break
			check(ready,"Actual room geometry retained/centered")
			check(root.get_texture().get_image().save_png(CONTEXT_OUT+"%s-%d.png"%[room_id,quarter])==OK,"Native furnishing context capture")
			records.append({"room":room_id,"quarter":quarter,"props":props,"stations":stations,"seatedStations":seated})
		game.queue_free();await process_frame
	var file=FileAccess.open(CONTEXT_OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"records":records,"scope":"actual current lounge/observation default geometry and RoomActivity eligibility in all four rotations; prescribed real room fixtures, no artwork injection or furniture edits; no East/West character-contact acceptance"},"\t"));file.close()
	print("VELD SIDE SEATED CONTEXT: %d checks,%d failures; eight current room/rotation contexts"%[checks,failures]);quit(1 if failures else 0)
