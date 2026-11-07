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
	var peer_image:=Image.create(8,8,false,Image.FORMAT_RGBA8);peer_image.fill(Color.BLUE)
	var peer_source=load("res://scripts/crew_storage/frame.gd").new();peer_source.source=peer_image
	var peer_frame:=CanvasTexture.new();peer_frame.diffuse_texture=peer_source;peer_frame.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	peer_frame.set_script(load("res://scripts/crew_storage/display.gd"));bank.sources[peer_frame.get_instance_id()]=peer_source
	var peer := DrawOwner.new(); peer.texture = peer_frame; peer.position = Vector2(8, 40); viewport.add_child(peer)
	var before := await capture(owner, viewport)
	check(before.get_pixel(9, 9) == Color.GREEN and before.get_pixel(14, 9) == Color.RED, "Real routed source pixels appear at the first parent")
	check(router.presenter.owners.size() == 2, "Both live draws hold pose leases")
	var id:int=owner.get_instance_id()
	var peer_id:int=peer.get_instance_id()
	var peer_slots:Array=router.presenter.owner_slots[peer_id].duplicate()
	var old_slots:Array=router.presenter.owner_slots[id].duplicate()
	first.hide()
	check(router.presenter.owner_slots.get(id,[]).is_empty(),"Hidden ancestor retires pose leases")
	for index in peer_slots:check(router.presenter.slots[index].holders.has(peer_id),"Hidden owner preserves visible peer lease")
	for index in old_slots:
		if router.presenter.slots[index].holders.is_empty():router.presenter.drop_slot(index)
		check(router.presenter.slots[index].frame==null,"Hidden last owner allows immutable image eviction")
	await RenderingServer.frame_post_draw
	var absent:=viewport.get_texture().get_image()
	check(absent.get_pixel(9,9).a==0.0 and absent.get_pixel(9,41)==Color.BLUE,"Hidden owner disappears; peer unchanged")
	first.show()
	# No explicit queue_redraw: hide retirement must request valid commands on reveal.
	await process_frame;await RenderingServer.frame_post_draw
	var restored:=viewport.get_texture().get_image()
	check(before.get_data()==restored.get_data(),"Reveal restores exact retained source pixels")
	owner.hide()
	check(router.presenter.owner_slots.get(id,[]).is_empty(),"Direct hide retires pose leases")
	owner.show();await process_frame;await RenderingServer.frame_post_draw
	check(before.get_data()==viewport.get_texture().get_image().get_data(),"Repeated reveal remains pixel exact")
	check(router.missing==0,"No route lost through hide/reveal")

	session.free()
	check(Router.active == null, "Normal session exit closes routing")
	print("CREW HIDDEN LEASES: %d checks, %d failures" % [checks, failures])
	call_deferred("quit", 1 if failures else 0)
