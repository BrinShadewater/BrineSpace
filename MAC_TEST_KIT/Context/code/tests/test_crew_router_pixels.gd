extends SceneTree
## Native route/lease/pixel regression across canvas removal and reparenting.
const Router = preload("res://scripts/crew_storage/router.gd")
var failures := 0
var checks := 0
class DrawOwner extends Node2D:
	var texture: Texture2D
	func _draw(): texture.draw(get_canvas_item(), Vector2.ZERO)
func check(ok: bool, why: String):
	checks += 1
	if not ok: failures += 1; push_error(why)
func _initialize(): call_deferred("run")
func capture(trigger: CanvasItem, viewport: SubViewport) -> Image:
	trigger.queue_redraw()
	await trigger.draw
	await RenderingServer.frame_post_draw
	return viewport.get_texture().get_image()
func run():
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\", "/")
	check(not expected.is_empty() and OS.get_user_data_dir().replace("\\", "/") == expected, "Explicit scratch profile required")
	check(DisplayServer.get_name() != "headless", "Native renderer required")
	if failures: quit(1); return
	var session := Node.new(); root.add_child(session)
	var viewport := SubViewport.new(); viewport.size = Vector2i(96, 64)
	viewport.transparent_bg = true; viewport.world_2d = World2D.new()
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS; session.add_child(viewport)
	var first := Node2D.new(); first.position = Vector2(8, 8); viewport.add_child(first)
	var second := Node2D.new(); second.position = Vector2(40, 16); second.scale = Vector2(2, 2); viewport.add_child(second)
	var image := Image.create(8, 8, false, Image.FORMAT_RGBA8); image.fill(Color.RED)
	for x in range(4):
		for y in range(8): image.set_pixel(x, y, Color.GREEN)
	var source = load("res://scripts/crew_storage/frame.gd").new(); source.source = image
	var frame := CanvasTexture.new(); frame.diffuse_texture = source
	frame.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	frame.set_script(load("res://scripts/crew_storage/display.gd"))
	var bank = load("res://scripts/crew_storage/bank.gd").new(); bank.sources[frame.get_instance_id()] = source
	Router.start(self, session, bank)
	var router = Router.active
	var owner := DrawOwner.new(); owner.texture = frame; first.add_child(owner)
	var peer := DrawOwner.new(); peer.texture = frame; peer.position = Vector2(8, 40); viewport.add_child(peer)
	var before := await capture(owner, viewport)
	check(before.get_pixel(9, 9) == Color.GREEN and before.get_pixel(14, 9) == Color.RED, "Real routed source pixels appear at the first parent")
	check(router.presenter.owners.size() == 2, "Both live draws hold pose leases")
	owner.reparent(second, true)
	var reparented := await capture(owner, viewport)
	check(before.get_data() == reparented.get_data(), "Keep-global reparent across scaled parents preserves every viewport pixel")
	var canvas: int = owner.get_canvas_item().get_id()
	var peer_id: int = peer.get_instance_id()
	var peer_slots: Array = router.presenter.owner_slots[peer_id].duplicate()
	second.remove_child(owner)
	check(router.presenter.owner_slots.get(peer_id, []) == peer_slots, "Removing another owner preserves the peer's existing lease")
	for index in peer_slots:
		check(router.presenter.slots[index].holders.has(peer_id), "Peer remains a holder without redrawing")
	await RenderingServer.frame_post_draw
	var absent := viewport.get_texture().get_image()
	check(absent.get_pixel(9, 9).a == 0.0 and absent.get_pixel(9, 41) == Color.GREEN, "Leaving removes its pixels and preserves the other owner")
	check(not router.canvas.has(canvas) and router.presenter.owners.size() == 1, "Off-tree canvas routing and its lease are released")
	second.add_child(owner)
	var returned := await capture(owner, viewport)
	check(before.get_data() == returned.get_data(), "Re-entering redraw restores identical source and peer pixels")
	check(router.missing == 0 and router.presenter.owners.size() == 2, "No missing route or lost peer lease after re-entry")
	session.free()
	check(Router.active == null, "Normal session exit closes routing")
	print("CREW ROUTER PIXELS: %d checks, %d failures" % [checks, failures])
	call_deferred("quit", 1 if failures else 0)
