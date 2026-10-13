extends SceneTree
## Native reserve risk/readability/navigation fixture. Scratch APPDATA required.
var checks := 0
var failures := 0
func _initialize() -> void:
	root.size = Vector2i(1600,900)
	root.content_scale_size = Vector2i(1920,1080)
	run.call_deferred()
func check(ok: bool, message: String) -> void:
	checks+=1
	if not ok:
		failures+=1
		push_error(message)
func settle() -> void:
	for _frame in range(5): await process_frame
func capture(name: String) -> void:
	await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png("res://output/ui-resource-outlook-2026-10-04/"+name+".png")==OK,"Capture: "+name)
func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.Preferences.save_path = "user://resource-outlook.cfg"
	game.meta.save_path = "user://resource-outlook.meta"
	game.run_save_path = "user://resource-outlook.loop"
	root.add_child(game)
	current_scene = game
	var frames := 0
	while not game.startup_complete and frames<600:
		frames+=1
		await process_frame
	check(game.startup_complete,"Gameplay initializes")
	game._set_paused(true,false)
	game.crew_comms.minimize()
	game._refresh_resources()
	var net: Dictionary = game._displayed_cycle_delta(game._simulate_room_economy(true,game.cycle+1))
	for key in game.BASE_STORAGE_CAPACITY:
		var id: String = "rare" if key=="rare_minerals" else str(key)
		check(game.resource_chips[id].get_meta("reserve_outlook").change==int(net.get(key,0)),"HUD uses real displayed forecast: "+id)
	# Controlled presentation reserves/rates; action semantics are checked separately below.
	game.resources.oxygen = 12
	game._set_resource_chip("oxygen","OXYGEN\n12/30  -1",Color.WHITE)
	game._apply_resource_outlook("oxygen","oxygen",-1)
	check(game.resource_labels.oxygen.text.contains("FALLING") and game.resource_chips.oxygen.get_meta("reserve_outlook").tone=="normal","Comfortable declining reserve is labelled without urgent warning")
	game.resources.oxygen = 2
	game._set_resource_chip("oxygen","OXYGEN\n2/30  -1",Color.WHITE)
	game._apply_resource_outlook("oxygen","oxygen",-1)
	check(game.resource_labels.oxygen.text.contains("LOW") and game.resource_chips.oxygen.get_meta("reserve_outlook").tone=="warning","Two-cycle supply uses low label and muted warning")
	check(game._reserve_forecast("oxygen",-1).contains("~2 cycles"),"Low reserve hint quantifies depletion")
	game.resources.food = 1
	game._set_resource_chip("food","FOOD\n1/30  -1",Color.WHITE)
	game._apply_resource_outlook("food","food",-1)
	check(game.resource_chips.food.get_meta("reserve_outlook").tone=="danger","Last-cycle supply has stronger warning")
	game.resources.water = 0
	game._set_resource_chip("water","WATER\n0/30  +0",Color.WHITE)
	game._apply_resource_outlook("water","water",0)
	check(game.resource_labels.water.text.contains("EMPTY") and game.resource_chips.water.get_meta("reserve_outlook").tone=="normal","Unused empty Water reserve has factual label without urgent warning")
	game.resources.data = 0
	game._set_resource_chip("data","DATA\n0/30  -1",Color.WHITE)
	game._apply_resource_outlook("data","data",-1)
	check(not game._reserve_forecast("data",-1).contains("0 cycles") and game.resource_labels.data.text.contains("EMPTY"),"Empty reserve does not claim zero-cycle countdown")
	game.resources.power = game._get_resource_capacity("power")
	game._set_resource_chip("power","POWER\n%d/%d  +0" % [game.resources.power,game.resources.power],Color.WHITE)
	game._apply_resource_outlook("power","power",0)
	check(game.resource_labels.power.text.contains("FULL") and game._reserve_forecast("power",0).contains("cannot be retained"),"Full reserve explains storage limit")
	await settle()
	await capture("reserve-risk")
	game.resources.oxygen = 0
	game._set_resource_chip("oxygen","OXYGEN\n0/30  +4",Color.WHITE)
	game._apply_resource_outlook("oxygen","oxygen",4)
	await settle()
	check(game.resource_labels.oxygen.text.contains("REFILLING"),"Empty improving reserve describes recovery")
	for id in game.resource_labels:
		var label: Label = game.resource_labels[id]
		check(label.get_combined_minimum_size().x<=label.size.x+1,"Resource caption fits HUD: "+str(id))
	await capture("reserve-refilling")
	check(not game._reserve_forecast("integrity",0).contains("Storage") and game._reserve_forecast("integrity",0).contains("100%"),"Integrity retains structural percentage rather than storage fullness")
	game.resources.food = 7
	check(game._reserve_forecast("food",-3).contains("~3 cycles"),"Fractional depletion rounds up")
	game._refresh_resources()
	var before: Dictionary = game.resources.duplicate(true)
	var chip: PanelContainer = game.resource_chips.oxygen
	chip.grab_focus()
	var accept := InputEventAction.new()
	accept.action = "ui_accept"
	accept.pressed = true
	chip.gui_input.emit(accept)
	await settle()
	check(game.inspected_resource=="oxygen" and game.journal_layer.visible,"Keyboard activation opens selected supply details")
	check(game.archive_label.text.to_lower().contains("oxygen"),"Supply detail page retains resource context")
	check(game.resources==before,"Reading forecast/details does not spend or allocate resources")
	print("RESOURCE OUTLOOK: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
