extends SceneTree
## Scene churn must not retain dead routing records during a long expedition.
const Router = preload("res://scripts/crew_storage/router.gd")
var checks := 0
var failures := 0
class DrawOwner extends Node2D:
	func _draw(): pass
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
func _initialize(): call_deferred("run")
func run() -> void:
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\", "/")
	check(not expected.is_empty() and OS.get_user_data_dir().replace("\\", "/") == expected, "Explicit scratch profile required")
	if failures: quit(1); return
	var session := Node2D.new()
	root.add_child(session)
	Router.start(self, session, null)
	var router = Router.active
	var baseline: int = router.canvas.size()
	for index in range(128):
		# Spatial station sounds use CanvasItems even though they draw no crew.
		var voice := AudioStreamPlayer2D.new()
		session.add_child(voice)
		voice.free()
	check(router.canvas.size() == baseline, "Retired spatial voices leave no routing WeakRefs")
	var owner := DrawOwner.new()
	session.add_child(owner)
	var id: int = owner.get_instance_id()
	var canvas: int = owner.get_canvas_item().get_id()
	router.track_script_draw(owner)
	router.epochs[id] = Engine.get_process_frames()
	check(router.canvas.has(canvas) and router.tracked_owners.has(id), "Live custom draw owner is routed")
	var callback: Callable = router.tracked_owners[id].callback
	session.remove_child(owner)
	check(not router.canvas.has(canvas), "Off-tree canvas is removed while its Node remains alive")
	check(not router.epochs.has(id) and not router.tracked_owners.has(id), "Off-tree draw bookkeeping is released")
	check(not owner.draw.is_connected(callback), "Off-tree draw callback is disconnected")
	session.add_child(owner)
	router.track_script_draw(owner)
	check(router.canvas.has(canvas) and router.tracked_owners.has(id), "Re-entering owner can route again")
	check(owner.draw.get_connections().size() == 1, "Re-entering owner has one routing callback")
	owner.free()
	check(router.canvas.size() == baseline and router.tracked_owners.is_empty() and router.epochs.is_empty(), "Freed draw owner leaves no session records")
	check(router.canvas.has(session.get_canvas_item().get_id()), "Unrelated live canvas remains routed")
	session.free()
	check(Router.active == null, "Session closes on grid exit")
	check(not node_added.is_connected(router.register), "Closed session unsubscribes from additions")
	if router.has_method("unregister"):
		check(not node_removed.is_connected(router.unregister), "Closed session unsubscribes from removals")
	print("CREW ROUTER LIFETIME: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
