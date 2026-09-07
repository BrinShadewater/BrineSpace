extends SceneTree
const Architects=preload("res://scripts/architects.gd")
const OUT="res://output/architect-recovery-v1"
var game
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(5): await process_frame
	await RenderingServer.frame_post_draw
func capture(label: String) -> Image:
	if is_instance_valid(game): game.grid_view.queue_redraw()
	await settle()
	var image:=root.get_texture().get_image()
	image.save_png(OUT.path_join(label+".png"))
	if is_instance_valid(game) and (label.begins_with("core-") or label.begins_with("released-") or label.begins_with("walking-")):
		core_pixels(image).save_png(OUT.path_join(label+"-room.png"))
	return image
func core_pixels(image: Image) -> Image:
	var local:=Rect2(Vector2(Architects.CORE_CELL)*game.get_cell_size(),Vector2.ONE*game.get_cell_size())
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local
	return image.get_region(Rect2i(screen))
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	game.Preferences.save_path="user://architect_native_%d.cfg" % OS.get_process_id()
	game.meta.save_path="user://architect_native_%d.meta" % OS.get_process_id()
	game.run_save_path="user://architect_native_%d.loop" % OS.get_process_id()
	game.meta.unlocked_architect_ids={"bill":true,"veld":true,"branforth":true}
	game.meta.selected_architect="bill"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	root.size=Vector2i(1600,900)
	await settle()
	for selected in Architects.IDS:
		game.meta.selected_architect=selected
		game._start_reboot_cycle()
		game.tick_timer.stop()
		game._set_paused(true,false)
		game.selected_card_id=""
		game.hovered_card_id=""
		game.selected_room_cell=Architects.CORE_CELL
		game.hover_cell=Architects.CORE_CELL
		game._set_grid_zoom(0.6)
		game._center_grid_on_station()
		game.grid_view.room_light_levels[Architects.CORE_CELL]=1.0
		await settle()
		var view=game.grid_view._bill_room_view(game.occupied[Architects.CORE_CELL])
		view.configure_embedded(0,[],false,0)
		print("CORE POD DIAGNOSTIC ",selected," / ",view.architect_pod," / props ",view.props.map(func(p): return p.id))
		assert(view.props.any(func(p): return p.id=="architect_pod"),"Core pod participates in registered rendering geometry")
		for i in range(6):
			game.architect_run.core.wake=i*7.0/6.0+0.03
			await capture("core-%s-%d" % [selected,i])
		var paused:=await capture("pause-%s-a" % selected)
		Architects.advance_core(game,2)
		var held:=await capture("pause-%s-b" % selected)
		assert(core_pixels(paused).get_data()==core_pixels(held).get_data(),"Pause freezes core emergence")
		game.paused=false
		Architects.advance_core(game,2)
		game.paused=true
		await capture("released-%s" % selected)
		for tick in range(60): game._update_test_walker(0.1)
		await capture("walking-%s" % selected)
		assert(Architects.actor_for(game,selected).active,"Selected actor releases to NPC")
	# The last loop starts Branforth; demonstrate Bill and Veld in recovered wards.
	for cell in game.wrecks:
		var ward: Dictionary=game.wrecks[cell]
		if ward.kind!="cryo": continue
		ward.paid=true
		ward.progress=18.0
		ward.cleared=true
		game._place_room("cryo_chamber",cell,true)
		game.occupied[cell].rotation=ward.rotation
		game.occupied[cell]["recovered_derelict"]=true
		game.powered_room_cells[cell]=true
		game.grid_view.room_light_levels[cell]=1.0
		game.selected_room_cell=cell
		game.hover_cell=cell
		game._refresh_all()
		await settle()
		game.inspector_focus_button.set_meta("cell",cell)
		game._focus_inspected_room()
		for i in range(6):
			ward.pods[0].wake=i*7.0/6.0+0.03
			await capture("ward-%s-%d" % [ward.pods[0].architect_id,i])
	for width in [1280,2560]:
		root.size=Vector2i(width,roundi(width*9.0/16))
		game.selected_room_cell=Architects.CORE_CELL
		game.hover_cell=Architects.CORE_CELL
		await settle()
		game.inspector_focus_button.set_meta("cell",Architects.CORE_CELL)
		game._focus_inspected_room()
		await capture("core-resolution-%d" % width)
	var paths: Array=[game.meta.save_path,game.run_save_path]
	game.free()
	var title=load("res://scripts/title_screen.gd").new()
	title.meta_state.save_path="user://architect_title_%d.meta" % OS.get_process_id()
	title.meta_state.unlocked_architect_ids={"bill":true}
	title.meta_state.selected_architect="bill"
	title.run_save_path="user://architect_title_%d.loop" % OS.get_process_id()
	root.add_child(title)
	current_scene=title
	title.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for width in [1280,1600,2560]:
		root.size=Vector2i(width,roundi(width*9.0/16))
		await capture("selection-%d" % width)
	assert(title.architect_choice.is_item_disabled(1) and title.architect_choice.is_item_disabled(2),"Unrecovered characters locked in title picker")
	title.free()
	for path in paths:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("ARCHITECT NATIVE PASS: three character clips, core and wards, spawn-to-NPC handoff, pause and title picker at three sizes")
	quit()
