extends SceneTree
const Visuals=preload("res://scripts/flood_visuals.gd")
const Store=preload("res://scripts/room_layout_store.gd")
var failures := 0
func check(ok: bool,message: String):
	if not ok:
		failures+=1
		push_error(message)
func _init(): call_deferred("run")
func run():
	var slot := Node2D.new()
	root.add_child(slot)
	var water_prop := {"rect":Rect2(0,0,30,50)}
	Visuals.prop_material(slot,water_prop,0.6,1,Vector2.ZERO,1)
	check(is_equal_approx(slot.material.get_shader_parameter("waterline_y"),4.4),"Prop depth uses its floor baseline")
	Visuals.prop_material(slot,water_prop,0,2,Vector2.ZERO,1)
	check(slot.material==null,"Dry props release submersion material")
	Visuals.prop_material(slot,water_prop,0.6,3,Vector2.ZERO,1)
	check(is_equal_approx(slot.material.get_shader_parameter("depth"),0.6),"Reflooding restores cached depth uniforms")
	slot.material=null # Retained draw slot reused by a crew entry, then a prop.
	Visuals.prop_material(slot,water_prop,0.6,4,Vector2.ZERO,1)
	check(is_equal_approx(slot.material.get_shader_parameter("depth"),0.6),"Reused slot initializes new material uniforms")
	slot.queue_free()
	# Waterlines must rise in world height, not merely change a room's tint.
	check(Visuals.crew_waterline(100,0.12,false)>Visuals.crew_waterline(100,0.35,false),"Waist water rises above ankle water")
	check(Visuals.crew_waterline(100,0.65,true)>Visuals.crew_waterline(100,0.93,true),"Critical depth covers swimmers' heads")
	for q in range(4):
		for id in ["corridor","corner","tee_corridor"]:
			var room := {"id":id,"rotation":q}
			var polygon := Visuals.shape(room)
			check(Geometry2D.is_point_in_polygon(Vector2.ZERO,polygon),"Rotated water footprint contains corridor center")
	Store.loaded=true
	Store.data={}
	var view=load("res://rooms/full-wall-v1/storage_bay_view.gd").new()
	root.add_child(view)
	view.configure_embedded(0,[1,3],true,0)
	var before: Array=view.props.duplicate(true)
	var passes: int=view.full_wall.placement_passes
	for i in range(30): view.configure_embedded(0,[1,3],true,float(i))
	check(view.props==before and view.full_wall.placement_passes==passes,"Stable frames retain exactly the same furniture without relocating it")
	var prop: Dictionary=view.props.back()
	var old_sort: float=prop.sort_y
	Store.data[Store.key("storage-wall",0)]={"order/"+str(prop.id):1}
	Store.revision+=1
	view.configure_embedded(0,[1,3],true,31)
	check(view.props.back().sort_y==old_sort+512,"Live layout ordering is still applied on the retained path")
	check(view.full_wall.placement_passes==passes,"Layout application does not rerun vacant-position search")
	view.configure_embedded(1,[0,2],true,32)
	check(view.full_wall.placement_passes>passes,"Rotation rebuilds placement")
	view.queue_free()
	await process_frame
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://flood-render-test-%d.meta" % OS.get_process_id()
	game.run_save_path="user://flood-render-test-%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.set_process(false)
	var grid=game.grid_view
	grid.visible_draw_rooms=game.placed_rooms
	var key: Array=grid._surface_state().duplicate(true)
	game.placed_rooms[0].water_level=0.61
	game.placed_rooms[0].hull_crack=0.8
	check(grid._surface_state()==key,"Changing water and cracks leaves static floor and wall caches valid")
	game.placed_rooms[0].leak_repair={"progress":2.5,"worker":"bill"}
	check(grid._surface_state()==key,"Repair progress does not rebuild static room surfaces")
	game.placed_rooms[0].rotation=1
	check(grid._surface_state()!=key,"Structural edits still invalidate cached surfaces")
	var a := Vector2i(20,20)
	var b := Vector2i(21,20)
	grid.render_door_cache_active=true
	grid.render_door_cache.clear()
	var actual: int=grid._door_frame_for_pair(game,a,b)
	check(grid._door_frame_for_pair(game,b,a)==actual and grid.render_door_cache.size()==1,"Door render cache shares both sides of a seam")
	grid.render_door_cache[[a,b]]=9
	grid.render_door_cache_active=false
	check(grid._door_frame_for_pair(game,a,b)==actual,"Physics ignores cached render aperture")
	await process_frame
	grid.render_door_cache_active=true
	check(grid._door_frame_for_pair(game,a,b)==actual,"New frame discards stale door aperture")
	grid.render_door_cache_active=false
	print("FLOOD RENDERING ","PASS" if failures==0 else "FAIL")
	quit(0 if failures==0 else 1)
