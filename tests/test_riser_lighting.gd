extends SceneTree
const Lighting=preload("res://rooms/whole-room/room_lighting.gd")
const Hardware=preload("res://scripts/station_hardware.gd")
const Settings=preload("res://scripts/title_settings.gd")
const Store=preload("res://scripts/room_layout_store.gd")
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(4): await process_frame
func capture(name: String) -> Image:
	await settle(); await RenderingServer.frame_post_draw
	var image:=root.get_texture().get_image(); image.save_png("res://output/layout-editor/"+name+".png"); return image
func run() -> void:
	root.size=Vector2i(1600,900)
	Store.path="res://output/layout-editor/riser-light-test.json"; Store.loaded=true; Store.data={}; Store.defaults_path="res://output/layout-editor/riser-light-defaults.json"
	if FileAccess.file_exists(Store.path+".recovery.json"): DirAccess.remove_absolute(Store.path+".recovery.json")
	assert(Lighting.anchors_for({},false)==Lighting.anchors_for({},true))
	var legacy: Dictionary={"light/low/0":[-140,-185],"lighting/light/low/0":{"brightness":0.5}}
	var migrated: Array=Lighting.anchors_for(legacy,false)
	assert(migrated[0].at.y==Lighting.Riser.CAP_TOP+9 and migrated[0].brightness==0.5)
	for direction in [Vector2.UP,Vector2.RIGHT,Vector2.DOWN,Vector2.LEFT]:
		var mount:=Hardware.exterior_mount(Vector2.ZERO,direction,384)
		assert(is_equal_approx(Hardware.exterior_light_radius(384),145.92),"Exterior illumination uses a direction-independent radius")
		if direction==Vector2.DOWN:
			assert(is_equal_approx(mount.y,198.0),"South fixture attaches to the solid deck rim")
		else:
			assert(absf(mount.y)>250 if direction.y!=0 else absf(mount.x)>196,"Fixture attaches outside the wall footprint")
	Store.data[Store.key("research-analysis-wall",0)]=legacy.duplicate(true)
	var editor=preload("res://scripts/room_layout_editor.gd").open(root)
	await settle(); assert(editor.draft["light/raised/0"]==[-140,Lighting.Riser.CAP_TOP+6],"Studio migrates legacy position before defaults hide it"); editor.layer=4; editor.rebuild_list()
	var fixtures: Array=editor.entities().duplicate(true)
	editor.riser_toggle.button_pressed=true
	await capture("riser-fixtures-on")
	editor.riser_toggle.button_pressed=false
	assert(editor.entities()==fixtures,"Hiding riser preserves light positions and IDs")
	await capture("riser-fixtures-hidden")
	var at: Vector2=editor.canvas.origin()+fixtures[0].rect.get_center()*editor.canvas.factor()
	assert(Rect2(Vector2.ZERO,editor.canvas.size).has_point(at),"Stored light anchor remains inside the studio canvas")
	editor.close_editor(); await settle()
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://riser-light-fixture.loop"; game.meta.save_path="user://riser-light-fixture.meta"
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false); game.crew_comms.minimize()
	game.placed_rooms.clear(); game.occupied.clear(); game.wrecks.clear(); game.powered_room_cells.clear()
	for cell in [Vector2i(20,20),Vector2i(21,20),Vector2i(20,21)]:
		game._place_room("research_lab" if cell==Vector2i(20,20) else "crew_hab",cell,true)
		game.powered_room_cells[cell]=true; game.grid_view.room_light_levels[cell]=1.0
	game.selected_card_id=""; game.hovered_card_id=""; game.hover_cell=Vector2i(-1,-1)
	Settings.raised_walls=true; game._refresh_all(); await settle(); game._fit_station_view(); await settle(); game._set_grid_zoom(game.grid_zoom*0.7); await settle()
	var room: Dictionary=game.occupied[Vector2i(20,21)]
	var raised: Array=game.grid_view._layout_light_anchors(room)
	Settings.raised_walls=false
	assert(game.grid_view._layout_light_anchors(room)==raised,"Station cutaway does not move fixtures, including shared north boundaries")
	game.grid_view.surface_key=[]; game.grid_view.light_surface_key=[]; game.grid_view.queue_redraw()
	await capture("station-riser-hidden-lights")
	Settings.raised_walls=true; game.hardware.exterior=false; game.grid_view.surface_key=[]; game.grid_view.queue_redraw()
	var unlit:=await capture("exterior-off")
	game.hardware.exterior=true; game.grid_view.queue_redraw()
	var lit:=await capture("exterior-outward")
	assert(lit.get_data()!=unlit.get_data(),"Exterior radial lights change station rendering")
	game.hardware.power=false; game.grid_view.queue_redraw()
	var dark:=await capture("exterior-power-off")
	assert(dark.get_data()!=lit.get_data())
	print("RISER LIGHTS PASS: fixed illumination anchors, legacy light compatibility, exterior radial illumination, exposed station edges, power/exterior gates, studio and station renders")
	quit()
