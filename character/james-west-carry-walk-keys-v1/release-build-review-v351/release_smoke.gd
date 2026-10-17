extends Node
class ReleaseErrors extends Logger:
	var messages: Array[String] = []
	func _log_error(function: String, file: String, line: int, code: String, rationale: String, _editor_notify: bool, error_type: int, _script_backtraces: Array[ScriptBacktrace]) -> void:
		# Warnings are reviewed in the log; engine/script errors fail the fixture.
		if error_type != Logger.ERROR_TYPE_WARNING:
			messages.append("%s %s:%s %s %s" % [function, file, line, code, rationale])
	func _log_message(_message: String, _error: bool) -> void:
		pass
var release_errors := ReleaseErrors.new()
var failures := 0
func check(ok: bool, message: String):
	if not ok:
		failures += 1
		push_error(message)
func _ready():
	if not "brine-james-release-" in OS.get_environment("APPDATA"):
		push_error("Scratch APPDATA required");get_tree().quit(2);return
	var uid_path:String=get_script().resource_path+".uid"
	if not FileAccess.file_exists(uid_path):FileAccess.open(uid_path,FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	OS.add_logger(release_errors)
	process_mode = Node.PROCESS_MODE_ALWAYS
	call_deferred("run")
func run():
	check(not OS.is_debug_build(), "Must execute in the actual release template")
	var title
	var title_deadline:=Time.get_ticks_msec()+60000
	while Time.get_ticks_msec()<title_deadline:
		await get_tree().process_frame
		title=get_tree().current_scene
		if title!=null and title.has_method("_start_game"):break
		if title!=null and title.has_method("_film_ended"):
			var skip:=InputEventKey.new();skip.keycode=KEY_SPACE;skip.pressed=true;title._unhandled_input(skip)
	check(title != null and title.has_method("_start_game"), "Configured title scene loaded")
	if title == null or not title.has_method("_start_game"):
		get_tree().quit(1); return
	title.meta_state.unlocked_architect_ids["branforth"]=true
	title.meta_state.selected_architect="branforth"
	title.start_button.pressed.emit()
	var picker = title.archive
	check(is_instance_valid(picker) and picker.has_method("_confirm"), "New Game opens architect selection")
	if not is_instance_valid(picker) or not picker.has_method("_confirm"):
		get_tree().quit(1); return
	picker.confirm.pressed.emit()
	var game
	var startup_deadline := Time.get_ticks_msec() + 90000
	while Time.get_ticks_msec() < startup_deadline:
		await get_tree().process_frame
		for child in get_tree().root.get_children():
			if child.has_method("type_transmission") and child.typing:
				var accept := InputEventAction.new()
				accept.action = "ui_accept"; accept.pressed = true
				child._input(accept)
		game = get_tree().current_scene
		if game != null and game != title and game.get("startup_complete") == true: break
	check(game != null and game != title and game.get("startup_complete") == true, "New Game completes in release")
	if game == null or game == title or game.get("startup_complete") != true:
		get_tree().quit(1); return
	check(game.meta.selected_architect=="branforth", "Normal New Game selects James in scratch-owned fixture")
	check(game.grid_view.branforth_player.get_script().resource_path=="res://scripts/james_water_player.gd", "Packaged selected James water player loaded")
	for child in get_tree().root.get_children():
		if child.has_method("finish_after_scene_change"):
			var continue_deadline := Time.get_ticks_msec() + 30000
			while is_instance_valid(child) and child.continue_button.disabled and Time.get_ticks_msec() < continue_deadline:
				await get_tree().process_frame
			if is_instance_valid(child):
				check(not child.continue_button.disabled, "Transmission Continue becomes available")
				child.continue_button.pressed.emit()
	# Continue resumes after a covered rendered frame, not a fixed frame count.
	var handoff_deadline := Time.get_ticks_msec() + 30000
	while Time.get_ticks_msec() < handoff_deadline:
		var transition_present := false
		for child in get_tree().root.get_children():
			if child.has_method("finish_after_scene_change"): transition_present = true
		if not transition_present and game.process_mode != Node.PROCESS_MODE_DISABLED: break
		await get_tree().process_frame
	check(game.process_mode != Node.PROCESS_MODE_DISABLED, "Continue handoff restores processing before simulation check")
	game.crew_comms.minimize()
	if game.paused: game._toggle_pause()
	var before: float = game.visual_time_seconds
	for i in range(240): await get_tree().process_frame
	check(game.visual_time_seconds > before, "Station simulation advances")
	check(not get_tree().paused and game.process_mode != Node.PROCESS_MODE_DISABLED, "Station process restored after Continue")
	check(game.grid_view.visible_draw_rooms.size() > 0, "Station renders after New Game")
	var report = get_tree().root.get_node("BugReport")
	var key := InputEventKey.new(); key.keycode=KEY_F8; key.pressed=true
	report._input(key)
	check(get_tree().paused and report.overlay.visible, "Release F8 opens and pauses")
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("user://release-report.png")
	var existed: bool = FileAccess.file_exists(game.run_save_path)
	var checkpoint := FileAccess.get_file_as_bytes(game.run_save_path) if existed else PackedByteArray()
	var path: String = report.save_report("Release New Game smoke")
	check(not path.is_empty(), "Release report is written")
	var zip := ZIPReader.new()
	check(zip.open(path)==OK, "Release ZIP opens")
	check(zip.file_exists("diagnostics/live_station.save"), "Release live snapshot is included")
	check(zip.read_file("report.txt").get_string_from_utf8().contains("brinespace-"), "Release content fingerprint is included")
	zip.close()
	check(FileAccess.file_exists(game.run_save_path)==existed, "Report does not create a player checkpoint")
	if existed: check(FileAccess.get_file_as_bytes(game.run_save_path)==checkpoint,"Report preserves checkpoint bytes")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(), "Release has no missing-art placeholders")
	report._hide_overlay()
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("user://release-game.png")
	game._set_paused(true,false)
	var checkpoint_path:String=game.run_save_path
	check(preload("res://scripts/run_save.gd").write(game,checkpoint_path)==OK,"Write actual release scratch checkpoint")
	var saved_foot:Vector2=game.branforth_npc.foot
	var saved_stage:String=game.branforth_npc.stage
	check(get_tree().change_scene_to_file("res://scenes/title_screen.tscn")==OK,"Return to packaged title for Continue")
	var deadline:=Time.get_ticks_msec()+30000
	while Time.get_ticks_msec()<deadline:
		await get_tree().process_frame
		title=get_tree().current_scene
		if title!=null and title.has_method("_continue_loop") and title.continue_button.visible:break
	check(title!=null and title.has_method("_continue_loop") and title.continue_button.visible,"Normal title offers saved-loop Continue")
	if title==null or not title.has_method("_continue_loop") or not title.continue_button.visible:get_tree().quit(1);return
	title.continue_button.pressed.emit()
	deadline=Time.get_ticks_msec()+180000
	while Time.get_ticks_msec()<deadline:
		await get_tree().process_frame
		var loading_present:=false
		for child in get_tree().root.get_children():
			if child.has_method("type_transmission"):
				loading_present=true
				if child.typing:
					var accept:=InputEventAction.new();accept.action="ui_accept";accept.pressed=true;child._input(accept)
				elif child.has_method("finish_after_scene_change") and not child.continue_button.disabled:child.continue_button.pressed.emit()
		game=get_tree().current_scene
		if game!=null and game.get("startup_complete")==true and not loading_present and game.process_mode!=Node.PROCESS_MODE_DISABLED:break
	check(game!=null and game.get("startup_complete")==true,"Normal saved-loop Continue completes")
	if game==null or game.get("startup_complete")!=true:get_tree().quit(1);return
	check(game.paused and game.branforth_npc.foot==saved_foot and game.branforth_npc.stage==saved_stage,"Continue preserves paused James contact/stage")
	check(game.meta.selected_architect=="branforth" and game.grid_view.branforth_player.get_script().resource_path=="res://scripts/james_water_player.gd","Continue keeps packaged James selection")
	game.crew_comms.minimize();game._toggle_pause()
	before=game.visual_time_seconds
	for i in range(120):await get_tree().process_frame
	check(game.visual_time_seconds>before and game.grid_view.visible_draw_rooms.size()>0,"Continued release simulation advances and renders")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"Continued release has no missing-art placeholders")
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("user://release-continue.png")
	OS.remove_logger(release_errors)
	for message in release_errors.messages: print("CAPTURED RELEASE ERROR: ", message)
	check(release_errors.messages.is_empty(), "Release has no engine or script errors")
	print("JAMES ACTUAL RELEASE NEW GAME + SAVED CONTINUE + F8: %d failures; debug=%s" % [failures, OS.is_debug_build()])
	get_tree().quit(1 if failures else 0)
