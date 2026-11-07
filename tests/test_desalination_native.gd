extends SceneTree
## Actual construction, staged checkpoint loading, room geometry and native captures.
const Rooms = preload("res://scripts/room_database.gd")
const Save = preload("res://scripts/run_save.gd")
const Grid = preload("res://scripts/grid_canvas.gd")
const OUT := "res://output/desalination-intake-decal-20261019/"
var checks := 0
var failures := 0

class Board extends Node2D:
	var views: Array = []
	func _draw() -> void:
		draw_rect(Rect2(0,0,1600,900),Color("101b20"))
		for q in range(4):
			var anchor := Vector2(225+q*385,490)
			var view = views[q]
			view.configure_embedded(q,[(1+q)%4,(2+q)%4,(3+q)%4],true,0.0,[])
			view.set_meta("raised_north_visible",true)
			view.render_into(self,anchor,0.88,true)
			view.shell_pass=1
			view.render_into(self,anchor,0.88,false,false)
			view.shell_pass=0
			draw_set_transform(anchor,0,Vector2.ONE*0.88)
			preload("res://rooms/whole-room/north_wall.gd").draw_into(self,"desalination_unit",Vector2i.ZERO,false,false,view)
			view.shell_pass=2
			view.render_into(self,anchor,0.88,false,false)
			view.shell_pass=0
			draw_set_transform(Vector2.ZERO)
			draw_string(ThemeDB.fallback_font,Vector2(anchor.x-145,210),"INTAKE "+["NORTH","EAST","SOUTH","WEST"][q],HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color("bbd4ce"))
			draw_string(ThemeDB.fallback_font,Vector2(anchor.x-145,720),"Doors "+["W / S / E","N / W / S","E / N / W","S / E / N"][q],HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color("809c97"))
		draw_string(ThemeDB.fallback_font,Vector2(70,110),"DESALINATION UNIT / authored layouts / four orientations",HORIZONTAL_ALIGNMENT_LEFT,-1,30,Color("e1e7dc"))

func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:
		failures+=1
		push_error(message)

func _initialize() -> void: run.call_deferred()

func start_game(checkpoint: Dictionary = {}):
	Save.pending=checkpoint
	var game=load("res://scenes/main.tscn").instantiate()
	game.Preferences.save_path="user://desalination.cfg"
	game.meta.save_path="user://desalination.meta"
	game.run_save_path="user://desalination.loop"
	root.add_child(game)
	current_scene=game
	var deadline:=Time.get_ticks_msec()+90000
	while not game.startup_complete and Time.get_ticks_msec()<deadline: await process_frame
	check(game.startup_complete,"Station finishes staged startup")
	game.set_process(false)
	game.tick_timer.stop()
	game._set_paused(true,false)
	game.crew_comms.minimize()
	return game

func run() -> void:
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").trim_suffix("/")
	var actual:=ProjectSettings.globalize_path("user://").replace("\\","/").trim_suffix("/")
	if expected.is_empty() or expected.to_lower()!=actual.to_lower():
		push_error("Refusing fixture outside isolated APPDATA")
		quit(1)
		return
	print("ISOLATED PROFILE: ",actual)
	root.size=Vector2i(1600,900)
	var risers=preload("res://rooms/whole-room/riser_catalog.gd")
	check(risers.material("desalination_unit")=="desalination_unit" and risers.family("desalination_unit")=="clinical","Custom riser selected while clinical department fallback is retained")
	var riser:Dictionary=risers.catalog().get("desalination_unit",{})
	check(not riser.is_empty(),"Room-specific riser is registered")
	if riser.is_empty():
		quit(1)
		return
	var face:Rect2=risers.source_rect("desalination_unit","face")
	check(is_equal_approx(face.size.x/face.size.y,6.4) and Rect2(Vector2.ZERO,risers.texture("desalination_unit").get_size()).encloses(face),"Riser face has the existing 6.4:1 aspect and valid source bounds")
	var reserve:Array=riser.door_reserve_world
	check(riser.no_baked_windows and reserve.size()==4 and Rect2(reserve[0],reserve[1],reserve[2],reserve[3]).is_equal_approx(Rect2(-46,-252,92,76)),"Window-free wall reserves the independent central doorway")
	check(preload("res://rooms/whole-room/riser_geometry.gd").HEIGHT==60.0,"Existing riser height is retained")
	var game=await start_game()
	check(game.resources.water==4,"Fresh loop has four Water")
	check(not game.testing_free_build,"Normal placement costs remain enabled")
	check(game.meta.unlocked_room_ids.has("desalination_unit"),"Unit is a foundation blueprint")
	# Dedicated foundation fixture; the unit itself uses the real paid build journey.
	for cell in [Vector2i(21,20),Vector2i(19,20),Vector2i(19,19),Vector2i(20,19),Vector2i(20,18)]:
		game.wrecks.erase(cell)
		game.drone_fleet.sites.erase(cell)
	game._place_room("solar_array",Vector2i(21,20),true)
	game._place_room("current_turbine",Vector2i(19,20),true)
	game.resources.metal=12
	game.resources.data=0
	game.resources.power=20
	game.hand.assign(["desalination_unit"])
	game.selected_card_id="desalination_unit"
	game.selected_rotation=0
	check(game.get_placement_problem("desalination_unit",Vector2i(20,19)).is_empty(),"Legal connected paid placement")
	game._on_grid_clicked(Vector2i(20,19))
	check(game.resources.metal==7 and game.drone_fleet.reserved(Vector2i(20,19)),"Actual placement reserves five Metal")
	game._set_paused(false,false)
	for frame in range(1600):
		game._process(0.1)
		if game.occupied.has(Vector2i(20,19)): break
		if frame%30==0: await process_frame
	game._set_paused(true,false)
	var built:bool=game.occupied.has(Vector2i(20,19))
	check(built,"Architect completes the paid Desalination Unit")
	if not built:
		print("CONSTRUCTION DIAGNOSTIC: ",game.drone_fleet.orders)
		quit(1)
		return
	game.resources.power=20
	var water:int=game.resources.water
	game._apply_room_economy()
	check(game.resources.water==water+2,"Completed unit produces two Water in the real economy")
	game.selected_card_id=""
	game.hovered_card_id=""
	game.selected_room_cell=Vector2i(20,19)
	game._refresh_all()
	check(game.inspector_label.get_parsed_text().contains("SEAWATER INTAKE NORTH"),"Inspector reports actual intake orientation")
	# Resource names become inline icons in the native RichTextLabel.
	var intake_text:String=preload("res://scripts/station_ui_insights.gd").desalination_intake(game,game.occupied[Vector2i(20,19)])
	var inspector_file:=FileAccess.open(OUT+"inspector.txt",FileAccess.WRITE)
	inspector_file.store_string(intake_text+"\n\n"+game.inspector_label.get_parsed_text())
	inspector_file.close()
	check(game.inspector_label.get_parsed_text().contains("CLEAR") and intake_text.contains("2 Water for 2 Power"),"Inspector explains the operating requirement: "+intake_text)
	check(game.preview_texture.texture!=null,"Built room has a rendered inspector card")
	check(game._room_flavor_line(game.occupied[Vector2i(20,19)]).contains("Salt remains outside"),"Unit has its own BRINE line rather than implying Oxygen output")
	game.room_operation_button.pressed.emit()
	check(game.occupied[Vector2i(20,19)].get("suspended",false),"Inspector button suspends the room")
	water=game.resources.water
	game._apply_room_economy()
	check(game.resources.water==water,"Suspended unit produces no Water")
	game.room_operation_button.pressed.emit()
	game._apply_room_economy()
	check(game.resources.water==water+2,"Inspector resume restores production next cycle")
	game._refresh_all()
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(OUT+"station.png")==OK,"Capture actual native station and inspector")
	water=game.resources.water
	var save_result:=Save.write(game,game.run_save_path)
	check(save_result==OK,"Checkpoint writes with the new room: "+Save.last_error)
	var checkpoint:Dictionary=Save.read(game.run_save_path)
	check(not checkpoint.is_empty(),"Written checkpoint can be read")
	if checkpoint.is_empty():
		quit(1)
		return
	current_scene=null
	game.free()
	game=await start_game(checkpoint)
	check(game.resources.water==water and water>4,"Continue preserves saved Water rather than replacing it with starter Water")
	check(game.occupied.get(Vector2i(20,19),{}).get("id","")=="desalination_unit","Continue restores the new room")
	check(game.occupied[Vector2i(20,19)].rotation==0,"Continue preserves intake orientation")
	check(game.get_room_doors(game.occupied[Vector2i(20,19)]).size()==3,"Continue uses the three-door room definition")
	game.resources.power=20
	game._apply_room_economy()
	check(game.resources.water==water+2,"Restored unit remains functional")
	# Three occupied neighbors force actual transit through the unit in every rotation.
	var npc=preload("res://scripts/bill_npc.gd").new()
	for q in range(4):
		game.occupied.clear()
		game.placed_rooms.clear()
		var cell:=Vector2i(20,20)
		var sides:Array=[(1+q)%4,(2+q)%4,(3+q)%4]
		var infos:Array=[["desalination_unit",cell,q]]
		for side in sides:
			infos.append(["brine_core",cell+Vector2i([Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][side]),0])
		for info in infos:
			var room:Dictionary=Rooms.get_room(info[0])
			room.pos=info[1]
			room.rotation=info[2]
			game.occupied[info[1]]=room
			game.placed_rooms.append(room)
		npc.rebuild(game)
		var center:Vector2=(Vector2(cell)+Vector2.ONE*0.5)*384.0
		var starts:Array=[npc.nearest_in_room(center,cell,false)]
		for side in sides:
			var door:Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][side]
			starts.append(npc.nearest_in_room(center+Vector2(door)*384.0,cell+door,false))
		check(not starts.has(-1),"Standable interior points in all three connected neighbors q%d"%q)
		for a in range(starts.size()):
			for b in range(a+1,starts.size()):
				if starts[a]<0 or starts[b]<0: continue
				var route:PackedVector2Array=npc.graph.get_point_path(starts[a],starts[b])
				check(not route.is_empty(),"Actual crew graph connects rooms q%d pair%d-%d"%[q,a,b])
				for step in range(1,route.size()):
					check(npc.segment_clear(route[step-1],route[step]),"Transit route clears machinery q%d pair%d-%d"%[q,a,b])
		var geometry:Dictionary=game.grid_view.bill_room_geometry(game.occupied[cell],sides)
		check(geometry.props.size()==5,"Five equipment props, including service cartridges, present q%d"%q)
		if q==2:
			game.selected_card_id=""
			game.hovered_card_id=""
			game.selected_room_cell=cell
			game._refresh_all()
			game.grid_view.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			check(root.get_texture().get_image().save_png(OUT+"connected-north.png")==OK,"Capture actual north-connected room without a floating riser over its neighbor")
	npc=null
	game.hide()
	var studio=preload("res://scripts/room_layout_editor.gd").new()
	studio.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.add_child(studio)
	var entry_index:=-1
	for i in range(studio.entries.size()):
		if studio.entries[i].room=="desalination_unit": entry_index=i
	check(entry_index>=0,"Desalination Unit is in the actual Studio picker")
	if entry_index>=0:
		studio.switch_room(entry_index)
		check(studio.riser_default("desalination_unit",true)=="desalination_unit" and studio.riser_record("desalination_unit").source==riser.source,"Actual Studio Room default resolves to the custom wall")
		for q in range(4):
			studio.switch_rotation(q)
			check(studio.room.room_id=="desalination_unit" and studio.room.props.size()==5,"Studio uses the five-prop live room layout q%d"%q)
			for side in range(4):
				check(studio.Geometry.has_port(studio.room.layout[0],side)==(side!=q),"Studio three-door geometry matches rotated intake q%d side%d"%[q,side])
		studio.switch_rotation(0)
		await process_frame
		await RenderingServer.frame_post_draw
		check(root.get_texture().get_image().save_png(OUT+"studio.png")==OK,"Capture actual Studio consumer")
	studio.queue_free()
	await process_frame
	# A fixed native surface avoids the desktop window's expand/stretch scale.
	var surface:=SubViewport.new()
	surface.size=Vector2i(1600,900)
	surface.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(surface)
	var board:=Board.new()
	board.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	for q in range(4):
		var view=load("res://rooms/desalination-unit-v1/view.gd").new()
		view.embedded=true
		view.hide()
		root.add_child(view)
		board.views.append(view)
	surface.add_child(board)
	await process_frame
	await RenderingServer.frame_post_draw
	var orientation_image:Image=surface.get_texture().get_image()
	check(orientation_image.save_png(OUT+"orientations.png")==OK,"Capture four actual room orientations")
	# The legacy shell only drew jamb/corner caps. Continuous top caps must reach
	# the same crown height as adjacent production rooms, outside the old face band.
	for q in range(4):
		for x in [-120,0]:
			var at:=Vector2(225+q*385,490)+Vector2(x,-266)*0.88
			var cap_pixel:Color=orientation_image.get_pixel(roundi(at.x),roundi(at.y))
			check(cap_pixel.r+cap_pixel.g+cap_pixel.b>0.7,"Continuous raised top cap, including the doorway lintel, q%d x%d: %s"%[q,x,cap_pixel])
		var probe_room:Dictionary=Rooms.get_room("desalination_unit")
		probe_room.pos=Vector2i(20,20)
		probe_room.rotation=q
		var exterior:Array[Vector2i]=game._ocean_exterior_cells(probe_room)
		var intake:Vector2=Vector2(exterior[0]-probe_room.pos)
		var arrow_at:=Vector2(225+q*385,490)+intake*28.0*0.88
		var arrow_pixel:Color=orientation_image.get_pixel(roundi(arrow_at.x),roundi(arrow_at.y))
		check(arrow_pixel.g>0.5 and arrow_pixel.b>0.4,"Visible intake arrow points toward actual ocean face q%d: %s"%[q,arrow_pixel])
	print("DESALINATION NATIVE: %d checks / %d failures"%[checks,failures])
	quit(1 if failures else 0)
