extends SceneTree
## Native fixed controls, inspector disclosures and readable geometry. Scratch APPDATA required.
var checks := 0
var failures := 0
func _initialize() -> void:
	root.size = Vector2i(1600,900)
	root.content_scale_size = Vector2i(1920,1080)
	run.call_deferred()
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func settle() -> void:
	for _frame in range(6): await process_frame
func capture(name: String) -> void:
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/ui-ux-pass-2026-10-03/"+name+".png")==OK,"Capture: "+name)
func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.Preferences.save_path = "user://ux-layout.cfg"
	game.meta.save_path = "user://ux-layout.meta"
	game.run_save_path = "user://ux-layout.loop"
	root.add_child(game)
	current_scene = game
	var frames := 0
	while not game.startup_complete and frames < 600:
		frames += 1
		await process_frame
	check(game.startup_complete,"Gameplay startup")
	game.Preferences.reduced_motion = true
	game._set_paused(true,false)
	game.crew_comms.minimize()
	var core := Vector2i(-1,-1)
	for cell in game.occupied:
		if game.occupied[cell].id=="brine_core": core=cell; break
	game.selected_room_cell = core
	game.selected_card_id = ""
	game._refresh_inspector()
	await settle()
	var details: Button = game.inspector_details.get_node("DisclosureHeader")
	check(not game.inspector_label.visible and details.visible,"Secondary room details start collapsed")
	check(not game.inspector_status_label.visible,"Duplicate status label removed")
	check(not game.inspector_effects.text.contains("CURRENT STATUS"),"Summary does not repeat the badge status heading")
	details.button_pressed = true
	await settle()
	check(game.inspector_label.visible and game.inspector_label.text.contains("NEXT CYCLE"),"Disclosure retains real forecast text")
	var line_height: float = game.inspector_label.get_theme_font("normal_font").get_height(game.inspector_label.get_theme_font_size("normal_font_size"))
	check(game.inspector_label.size.y>=line_height*6,"Expanded details show at least six lines without scrolling")
	game._refresh_inspector()
	check(game.inspector_label.visible,"Live refresh retains disclosure choice")
	check(game.inspector_details.get_index()>game.find_child("CrewWorkPanel",true,false).get_index(),"Room actions precede secondary details")
	var work = game.find_child("CrewWorkPanel",true,false)
	check(not work.info.visible,"Workplace notes start collapsed")
	work.get_node("WorkplaceNotes/DisclosureHeader").button_pressed = true
	check(work.info.visible and work.info.text.contains("PRIMARY JOB"),"Workplace notes retain assignment context")
	work.get_node("WorkplaceNotes/DisclosureHeader").button_pressed = false
	await capture("inspector-expanded")
	details.button_pressed = false
	await settle()
	await capture("gameplay")
	game.wrecks.clear()
	game.drone_fleet.sites.clear()
	game._place_room("moonbay",Vector2i(26,17),true)
	game.selected_room_cell = Vector2i(26,17)
	game._refresh_inspector()
	var scroll = game.find_child("SideScroll",true,false)
	var time_panel = game.find_child("ControlsPanel",true,false)
	check(not scroll.is_ancestor_of(time_panel),"Cycle controls are outside scrolling content")
	for size in [Vector2i(1600,900),Vector2i(1280,720)]:
		root.size = size
		await settle()
		var anchored: Rect2 = time_panel.get_global_rect()
		check(root.get_visible_rect().encloses(anchored),"Full time panel fits viewport: "+str(size))
		scroll.scroll_vertical = int(scroll.get_v_scroll_bar().max_value)
		await settle()
		check(time_panel.get_global_rect()==anchored,"Sidebar scroll leaves cycle controls pinned")
		check(root.get_visible_rect().encloses(game.pause_button.get_global_rect()),"Pause stays reachable")
		scroll.scroll_vertical = 0
		await settle()
		check(time_panel.get_global_rect()==anchored,"Returning to summary leaves cycle controls pinned")
		await capture("moonbay-"+str(size.x))
	game.speed_buttons[1].pressed.emit()
	check(game.time_speed_index==1,"Pinned speed action remains wired")
	game.pause_button.pressed.emit()
	check(not game.paused,"Pinned resume action remains wired")
	game._set_paused(true,false)
	game.selected_card_id = "life_support"
	game._refresh_inspector()
	await settle()
	check(not game.inspector_label.visible,"New selection resets secondary disclosure")
	check(game.inspector_effects.text.contains("BUILD READINESS"),"Build decision remains in summary")
	for id in game.resource_labels:
		var label: Label = game.resource_labels[id]
		check(label.get_combined_minimum_size().x<=label.size.x+1,"Resource text fits allocated width: "+str(id))
		check(label.get_combined_minimum_size().y<=label.size.y+1,"Resource text fits allocated height: "+str(id))
	await capture("blueprint-compact")
	print("UX LAYOUT: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
