extends SceneTree
const OUT := "res://assets/marsh-charging-v1/review"
var game
func _init(): call_deferred("run")
func settle():
	game.grid_view.queue_redraw()
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
func capture(label: String) -> Image:
	await settle()
	var frame := root.get_texture().get_image()
	frame.save_png(OUT.path_join(label+".png"))
	return frame
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://charging_native_%d.meta"%OS.get_process_id()
	game.run_save_path="user://charging_native_%d.loop"%OS.get_process_id()
	game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=false
	game.crew_comms.set_process(false) # Do not let tutorial dialogue pause the fixture.
	game.grid_view.set_process(false) # Freeze unrelated lighting fades during pixel comparisons.
	root.size=Vector2i(1600,900)
	var cell:=Vector2i(19,21)
	game.Architects.advance_core(game,10)
	game._place_room("corridor",Vector2i(19,22),true)
	game.resources.metal=30
	game.selected_card_id="";game.hovered_card_id=""
	game.selected_room_cell=cell;game.hover_cell=cell
	game._set_grid_zoom(0.6)
	await settle()
	game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room()
	game._refresh_all()
	await capture("derelict")
	game._toggle_wreck_work(cell);game._update_wreck_clearance(18)
	assert(game.wrecks[cell].cleared)
	game.powered_room_cells.erase(cell)
	game._refresh_all()
	await capture("unpowered")
	game.powered_room_cells[cell]=true
	game.grid_view.room_light_levels[cell]=1.0
	game.CryoRecovery.advance(game,3)
	game._refresh_inspector()
	var a:=await capture("pumping-a")
	game.CryoRecovery.advance(game,0.3)
	var b:=await capture("pumping-b")
	var pod_region:=Rect2i(260,185,80,135)
	assert(a.get_region(pod_region).get_data()!=b.get_region(pod_region).get_data(),"Native white fluid must move while powered")
	game.powered_room_cells.erase(cell)
	game._refresh_inspector()
	a=await capture("outage-a")
	game.CryoRecovery.advance(game,4)
	b=await capture("outage-b")
	assert(a.get_region(pod_region).get_data()==b.get_region(pod_region).get_data(),"Native white fluid must freeze on power loss")
	game.powered_room_cells[cell]=true
	for width in [960,1280,1600,2560]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		await settle();game._focus_inspected_room()
		game._refresh_inspector()
		await capture("charging-%d"%width)
	root.size=Vector2i(1600,900)
	await settle();game._focus_inspected_room()
	for q in range(4):
		game.occupied[cell].rotation=q;game.wrecks[cell].rotation=q
		await capture("rotation-%d"%q)
	game.occupied[cell].rotation=0;game.wrecks[cell].rotation=0
	game.CryoRecovery.advance(game,12)
	assert(game.marsh_npc.active and game.meta.unlocked_architect_ids.has("marsh"))
	await capture("awake-empty")
	var paths=[game.meta.save_path,game.run_save_path]
	game.free()
	for path in paths:
		if FileAccess.file_exists(path):DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("MARSH CHARGING NATIVE PASS: pumping, outage freeze, four sizes, four rotations, awake empty pod")
	quit()
