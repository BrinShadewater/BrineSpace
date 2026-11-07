extends "res://tests/test_veld_seated_south_selected.gd"
const CONTEXT_OUT="res://output/veld-read-north-context-v1/"
func _init():
	var path="res://tests/test_veld_read_north_context.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	DirAccess.make_dir_recursive_absolute(CONTEXT_OUT)
	var game=await fresh()
	game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant context fixture")
	game.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
	var records:Array=[]
	for quarter in range(4):
		game.occupied[CELL].rotation=quarter
		await game.veld_npc.rebuild(game)
		var data:Dictionary=game.veld_npc.geometry[CELL]
		var stations:Array=game.veld_npc.RoomActivity.stations(data)
		var props:Array=[]
		for prop in data.props:
			props.append({"id":prop.id,"role":preload("res://scripts/room_asset_library.gd").role_of(prop),"rect":prop.rect,"sortY":prop.get("sort_y",prop.rect.end.y)})
		var north:Array=stations.filter(func(s):return s.get("mode","")=="read" and s.facing=="north")
		var south:Array=stations.filter(func(s):return s.get("mode","")=="read" and s.facing=="south")
		check(north.is_empty(),"Current default observation has no North read station")
		check(not props.any(func(p):return p.id in ["wooden-desk","chair-rear"]),"Old North desk/chair absent from live geometry")
		check(props.any(func(p):return p.role=="observation_sofa"),"Current master sofa present")
		check(south.size()==1 and south[0].has("rest_point") and south[0].has("seat_depth"),"Current observation read resolves actual South sofa contact")
		game.selected_card_id="";game.selected_room_cell=CELL
		game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
		var ready:=false
		for attempt in 90:
			game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
			game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
			ready=game.grid_view.content_canvases.has(CELL) and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
			if ready:break
		check(ready,"Actual current room context retained and centered")
		check(root.get_texture().get_image().save_png(CONTEXT_OUT+"rotation-%d.png"%quarter)==OK,"Actual room context capture")
		records.append({"quarter":quarter,"props":props,"stations":stations,"northReads":north.size(),"southReads":south.size()})
		print("NORTH READ CONTEXT q",quarter," north=",north.size()," south=",south.size())
	var legacy:Dictionary={"activity_room":"observation_room","props":[],"blockers":[],"layout":[{"rotation":0}]}
	var fallback:Array=game.veld_npc.RoomActivity.stations(legacy)
	check(fallback[0].facing=="north" and fallback[0].mode=="read" and not fallback[0].has("rest_point"),"North remains a legacy/custom empty-furniture fallback, not current desk contact")
	var file=FileAccess.open(CONTEXT_OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"records":records,"scope":"actual current default observation geometry/stations/furniture in four rotations; prescribed room fixture, no artwork overrides or owner layout changes; no North character-contact proof"},"\t"));file.close()
	check(root.get_texture().get_image().save_png(CONTEXT_OUT+"final.png")==OK,"Final context capture")
	print("VELD READ NORTH CONTEXT: %d checks,%d failures; four current rotations"%[checks,failures]);quit(1 if failures else 0)
