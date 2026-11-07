extends SceneTree
## Native real-action feedback checks. Scratch APPDATA required.
const Settings = preload("res://scripts/title_settings.gd")
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
	check(root.get_texture().get_image().save_png("res://output/ui-action-feedback-2026-10-04/"+name+".png")==OK,"Capture: "+name)
func run() -> void:
	Settings.save_path = "user://action-feedback.cfg"
	Settings.initialize(root)
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://action-feedback.meta"
	game.run_save_path = "user://action-feedback.loop"
	root.add_child(game)
	current_scene = game
	var frames := 0
	while not game.startup_complete and frames<600:
		frames+=1
		await process_frame
	check(game.startup_complete,"Gameplay initializes")
	game._set_paused(true,false)
	game.crew_comms.minimize()
	var cell := Vector2i(26,17)
	game._place_room("solar_array",cell,true)
	game.selected_room_cell = cell
	game._refresh_all()
	await settle()
	check(not game.room_action_feedback_row.visible,"Feedback starts compact and hidden")
	game._toggle_inspected_room()
	check(game.occupied[cell].suspended and game.room_action_feedback.text.contains("suspended"),"Suspend action acknowledges real state")
	game._toggle_inspected_room()
	check(not game.occupied[cell].suspended and game.room_action_feedback.text.contains("next cycle"),"Resume explains next-cycle timing")
	check(game.inspector_effects.text.contains("Resume scheduled") and not game.inspector_effects.text.contains("Resume this room"),"Inspector explains pending resume without requesting it again")
	game._toggle_inspected_room_lock()
	check(game.occupied[cell].doors_locked and game.room_action_feedback.text.contains("cannot pass"),"Lock feedback explains sealed doors")
	game.hardware.doors = true
	game._toggle_inspected_room_lock()
	check(not game.occupied[cell].doors_locked and game.room_action_feedback.text.contains("Station-wide"),"Release explains overriding global door lock")
	game.hardware.doors = false
	game.resources.metal = 20
	game.occupied[cell].local_incident = true
	game._refresh_all()
	game._repair_inspected_room()
	check(not game.occupied[cell].get("local_incident",false) and game.resources.metal==18 and game.room_action_feedback.text.contains("2 Metal spent"),"Containment repair confirms actual cost and completion")
	game.occupied[cell].hull_crack = 0.2
	game._refresh_all()
	game._repair_inspected_room()
	check(game.occupied[cell].has("leak_repair") and game.resources.metal==16 and game.room_action_feedback.text.contains("queued"),"Hull repair confirms queued work rather than completion")
	await settle()
	await capture("repair-feedback")
	preload("res://scripts/hull_repair.gd").cancel(game,cell)
	game.occupied[cell].hull_crack = 0.0
	game._refresh_all()
	var before: int = game.resources.metal
	game._scrap_inspected_room()
	check(game.occupied.has(cell) and game.resources.metal==before,"First scrap press preserves room and resources")
	check(game.room_scrap_cancel.visible and game.room_action_feedback.text.contains("Solar Array") and game.room_action_feedback.text.contains("Cancel"),"Confirmation names room and provides cancellation")
	await settle()
	check(game.room_action_feedback_row.get_rect().end.x <= game.room_action_feedback_row.get_parent().size.x+1,"Confirmation fits inspector width")
	await capture("scrap-confirmation")
	game.room_scrap_cancel.pressed.emit()
	check(game.room_scrap_button.get_meta("armed")==Vector2i(-1,-1) and not game.room_action_feedback_row.visible,"Cancel disarms and hides confirmation")
	check(game.occupied.has(cell) and game.resources.metal==before,"Cancel preserves room and resources")
	game._scrap_inspected_room()
	game.selected_room_cell = Vector2i(0,0)
	await settle()
	check(game.room_scrap_button.get_meta("armed")==Vector2i(-1,-1),"Selecting another room disarms pending scrap")
	game.selected_room_cell = cell
	game._refresh_all()
	game._scrap_inspected_room()
	game._toggle_inspected_room_lock()
	check(game.room_scrap_button.get_meta("armed")==Vector2i(-1,-1) and not game.room_scrap_cancel.visible,"Another successful action disarms pending scrap")
	game._scrap_inspected_room()
	game._scrap_inspected_room()
	check(not game.occupied.has(cell) and game.resources.metal==before+2,"Second confirmed press uses existing refund")
	check(game.room_action_feedback.text.contains("2 Metal recovered") and not game.room_scrap_cancel.visible,"Scrap completion acknowledges actual refund")
	game.room_action_feedback_until = Time.get_ticks_msec()-1
	await settle()
	check(not game.room_action_feedback_row.visible,"Ordinary acknowledgement expires")
	game._show_room_action_feedback("Old room feedback",cell)
	game.selected_room_cell = Vector2i(0,0)
	await settle()
	check(not game.room_action_feedback_row.visible,"Changing selection clears old acknowledgement")
	print("ACTION FEEDBACK: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
