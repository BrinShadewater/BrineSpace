extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	var owner := Node.new()
	owner.set_meta("tablet_controls",true)
	root.add_child(owner)
	preload("res://scripts/audio_shutdown.gd").request(owner)
	await create_timer(0.4).timeout
	if owner.process_mode == Node.PROCESS_MODE_DISABLED or root.get_meta("audio_quitting",false):
		push_error("iPad Quit must not disable the application")
		quit(1); return
	var tablet := preload("res://scripts/tablet_controls.gd").new()
	tablet.fingers = {0:Vector2(10,10),1:Vector2(20,20)}
	tablet.notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	if not tablet.fingers.is_empty():
		push_error("Backgrounding must clear all gesture pointers")
		tablet.free(); quit(1); return
	tablet.free()
	print("IPAD QUIT PASS")
	quit(0)
