extends SceneTree
## Native hint/focus and actual disabled-reason checks. Scratch APPDATA required.
const Style = preload("res://scripts/title_button_style.gd")
const Settings = preload("res://scripts/title_settings.gd")
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
func hover(pos: Vector2) -> void:
	var motion := InputEventMouseMotion.new()
	motion.position = pos
	root.push_input(motion,true)
func wait_hint(button: Button, visible: bool) -> void:
	for _frame in range(120):
		if button.has_meta("tooltip_layer")==visible: return
		await process_frame
	check(false,"Hint state did not settle")
func capture(name: String) -> void:
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/ui-feedback-2026-10-04/"+name+".png")==OK,"Capture: "+name)
func run() -> void:
	Settings.save_path = "user://feedback-ui.cfg"
	Settings.initialize(root)
	Settings.tooltip_delay = 0.15
	var host := Control.new()
	host.theme = Style.menu_theme()
	root.add_child(host)
	var button := Button.new()
	button.text = "DISPATCH"
	button.position = Vector2(1600,980)
	button.size = Vector2(300,50)
	Style.apply(button,300,50)
	Style.set_hint(button,"Need 4 Metal to repair the mini-sub before launching.")
	button.disabled = true
	host.add_child(button)
	await settle()
	hover(button.get_global_rect().get_center())
	await wait_hint(button,true)
	if not button.has_meta("tooltip_layer"):
		quit(1); return
	await settle()
	var layer = button.get_meta("tooltip_layer")
	var panel: PanelContainer = layer.get_node("HintCard")
	check(panel.get_node("Body/Unavailable").visible,"Disabled hover explains unavailable state")
	check(panel.get_node("Body/HintText").text.contains("4 Metal"),"Disabled hint contains actionable reason")
	check(root.get_visible_rect().encloses(panel.get_global_rect()),"Bottom-right hint fits viewport after layout")
	check(panel.get_global_rect().end.y < button.get_global_rect().position.y,"Bottom-edge hint sits above its control")
	Style.set_hint(button,"Need 1 more Metal to repair the mini-sub.")
	await settle()
	check(layer==button.get_meta("tooltip_layer"),"Live hint refresh retains popup")
	check(panel.get_node("Body/HintText").text.contains("1 more Metal"),"Live hint shows current amount")
	await capture("disabled-hint")
	hover(Vector2(5,5))
	await wait_hint(button,false)
	check(button.tooltip_text.contains("1 more Metal"),"Leaving retains latest hint rather than stale text")
	button.disabled = false
	Style.set_hint(button,"Launch the selected mission.")
	button.grab_focus()
	await wait_hint(button,true)
	await settle()
	check(not button.get_meta("tooltip_layer").get_node("HintCard/Body/Unavailable").visible,"Keyboard-focused enabled hint has no unavailable heading")
	button.release_focus()
	await wait_hint(button,false)
	var plain := Button.new()
	plain.text = "2x"
	plain.position = Vector2(60,100)
	plain.size = Vector2(100,42)
	Style.apply_plain(plain)
	host.add_child(plain)
	plain.grab_focus()
	await settle()
	check(plain.get_theme_stylebox("focus").border_width_bottom==2,"Plain keyboard focus has a restrained underline")
	check(Style._focus().border_width_left==0,"Hull mouse selection still has no persistent outline")
	await capture("keyboard-focus")
	host.queue_free()
	await settle()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://feedback-ui.meta"
	game.run_save_path = "user://feedback-ui.loop"
	root.add_child(game)
	current_scene = game
	var frames := 0
	while not game.startup_complete and frames<600:
		frames+=1
		await process_frame
	check(game.startup_complete,"Gameplay initializes")
	game._set_paused(true,false)
	game.crew_comms.minimize()
	game.wrecks.clear()
	game.drone_fleet.sites.clear()
	if not game.Architects.present(game,"bill"): game.recovered_crew.append({"architect_id":"bill","alive":true})
	game.bill_npc.active = true
	game.bill_npc.dead = false
	var cell := Vector2i(20,19)
	game._place_room("airlock",cell,true)
	game.selected_room_cell = cell
	var airlock
	for node in game.find_children("*","VBoxContainer",true,false):
		if node.get_script()==preload("res://scripts/airlock_panel.gd"): airlock=node; break
	game.powered_room_cells[cell] = true
	var room: Dictionary = game.occupied[cell]
	room.airlock_cycle = {"phase":"flooding","elapsed":2.0}
	airlock.refresh()
	check(airlock.cycle_button.disabled and airlock.cycle_button.tooltip_text.contains("current chamber cycle"),"Airlock held cycle explains waiting")
	room.airlock_cycle = {"phase":"dry","elapsed":0.0}
	room.suspended = true
	airlock.refresh()
	check(airlock.action.disabled and airlock.action.tooltip_text.contains("Resume the airlock"),"Suspended locker reason identifies room state")
	room.suspended = false
	game.drone_fleet.sites[cell+Vector2i.UP] = preload("res://scripts/harvest_sites.gd").make_site("salvage",3)
	airlock.refresh()
	check(airlock.cycle_button.tooltip_text.contains("resource deposit") and airlock.cycle_button.tooltip_text.contains("Clear"),"Blocked hatch hint identifies obstruction and remedy")
	game.drone_fleet.sites.clear()
	var bay_cell := Vector2i(26,17)
	game._place_room("moonbay",bay_cell,true)
	game.selected_room_cell = bay_cell
	var bay = game.find_child("MoonbayPanel",true,false)
	var state := preload("res://scripts/moonbay_missions.gd").mission_state(game.occupied[bay_cell])
	state.damage = 1
	game.resources.metal = 3
	bay.refresh()
	check(bay.launch_button.disabled and bay.launch_button.tooltip_text.contains("Repair"),"Damaged sub launch reason explains repair")
	check(bay.repair_button.disabled and bay.repair_button.tooltip_text.contains("1 more Metal"),"Mini-sub repair reason uses current shortfall")
	state.damage = 0
	bay.refresh()
	check(bay.launch_button.tooltip_text.contains("No eligible contacts"),"Empty contact reason explains another order or survey")
	game._refresh_inspector()
	await settle()
	await capture("moonbay-reasons")
	game.selected_room_cell = cell
	game._refresh_inspector()
	check(game.room_repair_button.disabled and game.room_repair_button.tooltip_text.contains("No repair is needed"),"Intact hull explains why repair is unavailable")
	room.local_incident = true
	game.resources.metal = 1
	game._refresh_inspector()
	check(game.room_repair_button.disabled and game.room_repair_button.tooltip_text.contains("1 more Metal"),"Room repair reason uses actual shortfall")
	room.leak_repair = {}
	game._refresh_inspector()
	check(game.room_repair_button.tooltip_text.contains("already queued"),"Queued repair explains waiting for crew")
	room.erase("leak_repair")
	game.running = false
	game._refresh_inspector()
	check(game.room_operation_button.tooltip_text.contains("concluded") and game.room_lock_button.tooltip_text.contains("concluded"),"Concluded expedition explains unavailable room controls")
	print("UI FEEDBACK: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
