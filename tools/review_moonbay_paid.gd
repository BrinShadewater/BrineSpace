extends SceneTree
## Native paid placement and mission walkthrough. Always run with scratch APPDATA.

const MainScene = preload("res://scenes/main.tscn")
const Mission = preload("res://scripts/moonbay_missions.gd")
const Save = preload("res://scripts/run_save.gd")
var game
var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for _i in range(8): await process_frame
	await RenderingServer.frame_post_draw

func capture(label: String) -> void:
	game._refresh_inspector()
	game.find_child("MoonbayPanel",true,false).refresh()
	game.grid_view.queue_redraw()
	await settle()
	var path := "res://output/moonbay-review/paid-%s.png" % label
	check(root.get_texture().get_image().save_png(path)==OK,"Native capture "+label)
	print("CAPTURE ",path)

func run() -> void:
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i(1920,1080)
	root.size = Vector2i(1600,900)
	game = MainScene.instantiate()
	game.meta.save_path = "user://moonbay_paid.meta"
	game.run_save_path = "user://moonbay_paid.loop"
	root.add_child(game)
	current_scene = game
	game._confirm_doctrines()
	game.resources.metal = 100
	game.resources.rare_minerals = 20
	var home := Vector2i(-1,-1)
	for rotation in range(4):
		if home.x>=0: break
		game.selected_rotation = rotation
		for y in range(17,22):
			if home.x>=0: break
			for x in range(17,22):
				var cell := Vector2i(x,y)
				if game.get_placement_problem("moonbay",cell).is_empty():
					home = cell
					break
	check(home.x>=0,"Paid run finds an ocean-facing Moonbay site connected to the station")
	if home.x<0: quit(1); return
	var metal_before: int = game.resources.metal
	game.hand.assign(["moonbay"])
	game.selected_card_id = "moonbay"
	game._on_grid_clicked(home)
	check(game.resources.metal==metal_before-20 and game.drone_fleet.reserved(home+Vector2i.ONE),"Moonbay card pays 20 Metal and reserves all four cells")
	for _frame in range(1400):
		game._process(0.1)
		if game.occupied.has(home): break
	check(game.occupied.has(home),"Crew completes paid Moonbay construction")
	if not game.occupied.has(home): quit(1); return
	game.set_process(false)
	game.tick_timer.stop()
	game.running = true
	game.paused = false
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game.selected_room_cell = home
	game._refresh_all()
	game._set_grid_zoom(0.36)
	await settle()
	var at: Vector2 = Vector2(home+Vector2i.ONE)*game.get_cell_size()-game.grid_scroll.size*0.5
	game.grid_scroll.scroll_horizontal = roundi(at.x)
	game.grid_scroll.scroll_vertical = roundi(at.y)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://output/moonbay-review"))
	await capture("built")
	var deep := Vector2i(-1,-1)
	for cell in game.drone_fleet.sites:
		if game.drone_fleet.sites[cell].get("moonbay_deep",false): deep=cell; break
	check(deep.x>=0,"Paid run contains a distant deep site")
	if deep.x<0: quit(1); return
	var site: Dictionary = game.drone_fleet.sites[deep]
	site.hazardous = false
	var panel = game.find_child("MoonbayPanel",true,false)
	for order_index in range(3):
		panel.crew_choice.select(0)
		panel.order_choice.select(order_index)
		panel.refresh()
		for i in range(panel.target_choice.item_count):
			if panel.target_choice.get_item_metadata(i)==deep: panel.target_choice.select(i); break
		check(panel.target_choice.selected>=0 and panel.target_choice.get_item_metadata(panel.target_choice.selected)==deep,"Order %d offers the deep site" % order_index)
		if failures>0: quit(1); return
		panel.launch_button.pressed.emit()
		var state: Dictionary = Mission.mission_state(game.occupied[home])
		check(state.phase=="approach","Order %d dispatches from inspector" % order_index)
		var saved_at_sea := false
		for _step in range(700):
			for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:
				if not actor.moonbay_assignment.is_empty(): Mission.advance_crew(game,actor,1.0)
			Mission.tick(game,1.0)
			if state.phase=="work" and not saved_at_sea and order_index==0:
				saved_at_sea = true
				check(Save.write(game,game.run_save_path)==OK,"At-sea paid run writes checkpoint")
				var data: Dictionary = Save.read(game.run_save_path)
				check(not data.is_empty() and Save.restore(game,data),"At-sea paid run resumes from disk")
				game._set_paused(false,false)
				state = Mission.mission_state(game.occupied[home])
				check(state.phase=="work" and not game.bill_npc.moonbay_assignment.is_empty(),"Continue preserves mission and pilot")
			if state.phase=="idle": break
		check(state.phase=="idle","Order %d returns and unloads" % order_index)
		check(game.bill_npc.moonbay_assignment.is_empty(),"Order %d releases pilot" % order_index)
		await capture(["survey","recover","deep-access"][order_index])
	site = game.drone_fleet.sites[deep]
	check(site.get("discovered",false) and site.get("deep_accessed",false),"Survey and deep access resolve at the destination")
	site.hazardous = true
	panel.crew_choice.select(0)
	panel.order_choice.select(2)
	panel.refresh()
	for i in range(panel.target_choice.item_count):
		if panel.target_choice.get_item_metadata(i)==deep: panel.target_choice.select(i); break
	panel.launch_button.pressed.emit()
	var hazard_state: Dictionary = Mission.mission_state(game.occupied[home])
	hazard_state.hazard_roll = 0.0
	for _step in range(700):
		if not game.bill_npc.moonbay_assignment.is_empty(): Mission.advance_crew(game,game.bill_npc,1.0)
		Mission.tick(game,1.0)
		if hazard_state.phase=="idle": break
	check(hazard_state.phase=="idle" and hazard_state.damage==1,"Hazard returns the pilot with a damaged sub")
	await capture("hazard-return")
	panel.refresh()
	panel.repair_button.pressed.emit()
	check(hazard_state.damage==0,"Four Metal repairs the sub")
	await capture("repaired")
	print("MOONBAY PAID ","PASS" if failures==0 else "FAIL"," / ",failures," failures")
	quit(0 if failures==0 else 1)
