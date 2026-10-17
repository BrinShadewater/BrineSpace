extends SceneTree
## Native presentation/action regression. Run with scratch APPDATA.
const Settings = preload("res://scripts/title_settings.gd")
const Cycle = preload("res://scripts/airlock_cycle.gd")
const Mission = preload("res://scripts/moonbay_missions.gd")
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
	for _frame in range(5): await process_frame
func capture(name: String) -> void:
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/ui-mission-integration-2026-10-03/"+name+".png")==OK,"Capture: "+name)
func run() -> void:
	Settings.save_path = "user://mission-ui.cfg"
	Settings.initialized = false
	Settings.initialize(root)
	Settings.reduced_motion = false
	var overlay = preload("res://scripts/restore_overlay.gd").new()
	root.add_child(overlay)
	await settle()
	var loading = overlay.find_child("RestoreProgress",true,false)
	var spinner: ProgressBar = loading.get_node("Body/LoadingProgress")
	check(spinner.indeterminate and spinner.visible,"Restore shows activity without invented percentage")
	check(overlay.detail.text == overlay.message,"Restore retains caller message")
	check(loading.size.x < root.get_visible_rect().size.x,"Restore card fits viewport")
	await capture("restore")
	overlay.queue_free()
	await settle()
	Settings.reduced_motion = true
	overlay = preload("res://scripts/restore_overlay.gd").new()
	root.add_child(overlay)
	await settle()
	check(not overlay.find_child("LoadingProgress",true,false).visible,"Reduced Motion removes restore animation")
	overlay.queue_free()
	await settle()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://mission-ui.meta"
	game.run_save_path = "user://mission-ui.loop"
	root.add_child(game)
	current_scene = game
	var frames := 0
	while not game.startup_complete and frames < 600:
		frames += 1
		await process_frame
	check(game.startup_complete,"Gameplay initializes")
	game._set_paused(true,false)
	game.crew_comms.minimize()
	game.wrecks.clear()
	game.drone_fleet.sites.clear()
	if not game.Architects.present(game,"bill"):
		game.recovered_crew.append({"architect_id":"bill","alive":true})
	game.bill_npc.active = true
	game.bill_npc.dead = false
	var cell := Vector2i(20,19)
	game._place_room("airlock",cell,true)
	game.powered_room_cells[cell] = true
	game.selected_room_cell = cell
	game.selected_card_id = ""
	var airlock
	for node in game.find_children("*","VBoxContainer",true,false):
		if node.get_script()==preload("res://scripts/airlock_panel.gd"): airlock = node; break
	check(airlock != null,"Airlock controls exist")
	var room: Dictionary = game.occupied[cell]
	room.airlock_cycle = {"phase":"flooding","elapsed":2.0}
	game._refresh_inspector()
	airlock.refresh()
	check(airlock.cycle_badges.get_child(0).get_node("Content/Value").text == "50%","Airlock water reads actual cycle pose")
	check(airlock.cycle_badges.get_child(1).get_node("Content/Value").text == "0%","Airlock pressure reads actual cycle pose")
	var stable = airlock.cycle_badges.get_child(0)
	airlock.refresh()
	check(stable == airlock.cycle_badges.get_child(0),"Unchanged airlock readings retain nodes")
	check(airlock.cycle_button.disabled,"Mid-cycle hatch action stays disabled")
	await settle()
	check(airlock.action.get_parent()==airlock.refill.get_parent(),"Locker actions share compact row")
	await capture("airlock")
	room.airlock_cycle = {"phase":"dry","elapsed":0.0}
	airlock.refresh()
	check(not airlock.cycle_button.disabled,"Dry powered airlock enables outward cycle")
	airlock.cycle_button.pressed.emit()
	check(Cycle.state(room).phase=="sealing_inner","Hatch button still invokes actual cycle request")
	var bay_cell := Vector2i(26,17)
	game._place_room("moonbay",bay_cell,true)
	game.selected_room_cell = bay_cell
	var bay = game.find_child("MoonbayPanel",true,false)
	bay.order_choice.select(1)
	var target := Vector2i(26,13)
	game.drone_fleet.sites[target] = preload("res://scripts/harvest_sites.gd").make_site("salvage",3)
	game.drone_fleet.sites[target].discovered = true
	var state := Mission.mission_state(game.occupied[bay_cell])
	state.target = target
	bay.order_choice.select(0)
	state.phase = "work"
	state.crew = "bill"
	state.order = "recover"
	state.progress = 7.0
	state.chamber_water = 1.0
	game._refresh_inspector()
	bay.refresh()
	check(bay.mission_meter.visible and bay.mission_meter.value==50,"Mission meter uses actual recover phase duration")
	check(bay.order_choice.selected==1,"Active mission displays its actual order rather than stale picker selection")
	state.crew = "veld"
	bay.refresh()
	check(bay.crew_choice.get_item_metadata(bay.crew_choice.selected)=="veld","Active mission retains its actual pilot in the disabled picker")
	state.crew = "bill"
	bay.refresh()
	game.drone_fleet.sites[target].units = 0
	bay.refresh()
	check(bay.target_choice.item_count==1 and bay.target_choice.get_item_metadata(0)==target,"Active destination remains visible after cargo site depletion")
	check(bay.mission_badges.get_child(1).get_node("Content/Value").text=="100%","Mini-sub chamber readout uses actual water")
	check(bay.recall_button.visible and bay.launch_button.disabled,"Active mission retains recall and prevents launch")
	check(bay.target_choice.item_count==1 and bay.target_choice.get_item_metadata(0)==target,"Destination retains real contact metadata")
	game._fit_station_view()
	await settle()
	await capture("moonbay")
	bay.recall_button.pressed.emit()
	check(state.recall and bay.recall_button.disabled,"Recall invokes existing mission action")
	check(bay.mission_badges.get_child_count()==3,"Recall acknowledgement is visible")
	state.phase = "idle"
	state.damage = 1
	state.recall = false
	bay.refresh()
	check(not bay.mission_meter.visible and bay.repair_button.visible,"Idle damaged sub exposes repair without progress")
	var before: int = game.resources.metal
	bay.repair_button.pressed.emit()
	check(state.damage==0 and game.resources.metal==before-Mission.REPAIR_METAL,"Repair retains real cost and state change")
	game.drone_fleet.sites.clear()
	bay.refresh()
	check(bay.target_choice.item_count==0 and bay.target_choice.disabled and bay.target_choice.text=="NO CONTACTS FOR THIS ORDER","No-contact placeholder creates no selectable destination")
	root.size = Vector2i(1280,720)
	game._refresh_inspector()
	await settle()
	for button in [bay.helmet_button,bay.refill_button,bay.launch_button]:
		check(button.get_global_rect().end.x <= root.get_visible_rect().end.x,"Compact control fits horizontally: "+button.text)
	await capture("moonbay-compact")
	print("MISSION UI: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
