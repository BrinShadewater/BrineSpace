extends SceneTree
var game
var viewport_width := 1600
var capture_dir := "res://output"
var write_cards := false
class CardCanvas extends Node2D:
	var view
	func _draw() -> void:
		if view != null: view.render_into(self,Vector2(256,256),1.16,false,true)

class SpriteCanvas extends Node2D:
	var clock := 0.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,768,320),Color("183239"))
		var i := 0
		for kind in ["mining","salvage","construction"]:
			preload("res://scripts/drone_art.gd").draw_drone(self,kind,Vector2(128+i*256,145),145,clock,true,true)
			i += 1

func _init() -> void: call_deferred("run")
func frame() -> void:
	game.grid_view.queue_redraw()
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
func capture(label: String) -> void:
	await frame()
	assert(root.get_texture().get_image().save_png(capture_dir.path_join("drone-fleet-w%d-" % viewport_width+label+".png"))==OK)
func run() -> void:
	root.size = Vector2i(1600,900)
	game = load("res://scenes/main.tscn").instantiate()
	game.run_save_path = "user://drone_visual_%d.loop" % OS.get_process_id()
	game.meta.save_path = game.run_save_path+".meta"
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--width="): viewport_width = int(argument.trim_prefix("--width="))
		if argument.begins_with("--capture-dir="): capture_dir = argument.trim_prefix("--capture-dir=")
		if argument == "--write-cards": write_cards = true
	assert(DirAccess.make_dir_recursive_absolute(capture_dir)==OK)
	root.size = Vector2i(viewport_width,roundi(viewport_width*9.0/16.0))
	game.set_process(false)
	game.tick_timer.stop()
	game.testing_disable_failures = true
	game.occupied.clear()
	game.placed_rooms.clear()
	game.wrecks.clear()
	game.drone_fleet.restore(null)
	game._place_room("brine_core",Vector2i(20,20),true)
	game._place_room("mining_drone_bay",Vector2i(19,20),true)
	game.occupied[Vector2i(19,20)].rotation = 1
	game._place_room("salvage_drone_bay",Vector2i(21,20),true)
	game.occupied[Vector2i(21,20)].rotation = 1
	game._place_room("construction_drone_bay",Vector2i(20,21),true)
	game.resources.power = 40
	game.drone_fleet.synchronize(game.placed_rooms)
	game.drone_fleet.enqueue("corridor",Vector2i(20,22),0)
	game.test_walker_cell = Vector2i(-1,-1)
	game.hand.assign(["construction_drone_bay","mining_drone_bay","salvage_drone_bay"])
	game._refresh_all()
	await frame()
	await frame()
	root.mode = Window.MODE_WINDOWED
	root.size = Vector2i(viewport_width,roundi(viewport_width*9.0/16.0))
	await frame()
	assert(root.size==Vector2i(viewport_width,roundi(viewport_width*9.0/16.0)),"Native capture uses requested viewport size")
	game._fit_station_view()
	game._set_grid_zoom(0.22)
	await frame()
	game._center_grid_on_station_now()
	await capture("docked")
	for step in [[2.5,"launch"],[3.0,"work"],[2.0,"work-b"],[3.0,"return"],[2.5,"dock"]]:
		game.paused = false
		game._update_wreck_clearance(step[0])
		await capture(step[1])
	# Native card captures use exactly the station room components.
	var vp := SubViewport.new()
	vp.size = Vector2i(512,512)
	vp.transparent_bg = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	var canvas := CardCanvas.new()
	vp.add_child(canvas)
	for identity in ["construction","mining","salvage"]:
		# Separate preview instances prevent live station deployment state leaking into cards.
		var view = load("res://rooms/production-ten/"+identity+"_drone_bay_view.gd").new()
		view.embedded = true
		view.hide()
		root.add_child(view)
		var entry := [identity,view]
		canvas.view = view
		canvas.view.drone_deployed = false
		canvas.view.hatch_open = 0.0
		canvas.view.configure_embedded(0,[],false,0.0)
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var card_path: String = "res://assets/drones/fleet-v1/"+entry[0]+"-bay-card-v3.png" if write_cards else capture_dir.path_join(entry[0]+"-bay-card-v3.png")
		assert(vp.get_texture().get_image().save_png(card_path)==OK)
		for q in range(4):
			var room := {"id":entry[0]+"_drone_bay","rotation":q}
			var anchors: Dictionary = game.grid_view.drone_anchors(room)
			canvas.view.configure_embedded(q,[],false,0.0)
			if identity == "construction":
				canvas.view.configure_embedded(q,[0,1,2,3],false,0.0)
				for distance in range(-180,181,4):
					var point := Vector2(0,distance).rotated(q*PI/2.0)
					assert(canvas.view.can_stand(point),"Construction bay circulation remains clear through rotated ports")
				canvas.view.configure_embedded(q,[],false,0.0)
			for prop in canvas.view.props:
				if str(prop.id).ends_with("_rov"):
					assert(anchors.dock.is_equal_approx(Vector2(prop.rect.get_center().x,prop.rect.end.y-50)),"Dock matches rendered cradle after rotation")
				if str(prop.id).ends_with("_hatch"):
					assert(anchors.hatch.is_equal_approx(Vector2(prop.rect.get_center().x,prop.rect.end.y-35)),"Launch anchor matches actual hatch after rotation")
			canvas.view.drone_deployed = false
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var docked := vp.get_texture().get_image()
			canvas.view.drone_deployed = true
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var away := vp.get_texture().get_image()
			assert(docked.get_data()!=away.get_data(),"Deployment removes drone pixels in each rotation")
			assert(docked.save_png(capture_dir.path_join("drone-%s-q%d-docked.png" % [entry[0],q]))==OK)
			assert(away.save_png(capture_dir.path_join("drone-%s-q%d-empty.png" % [entry[0],q]))==OK)
		canvas.view.drone_deployed = false
	canvas.queue_free()
	await process_frame
	vp.size = Vector2i(768,320)
	var sprites := SpriteCanvas.new()
	vp.add_child(sprites)
	await process_frame
	await RenderingServer.frame_post_draw
	var first := vp.get_texture().get_image()
	assert(first.save_png(capture_dir.path_join("drone-work-tools-a.png"))==OK)
	sprites.clock = 0.35
	sprites.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var second := vp.get_texture().get_image()
	assert(second.save_png(capture_dir.path_join("drone-work-tools-b.png"))==OK)
	for i in range(3):
		var region := Rect2i(i*256,0,256,320)
		assert(first.get_region(region).get_data()!=second.get_region(region).get_data(),"Every drone has moving working pixels")
	sprites.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	assert(second.get_data()==vp.get_texture().get_image().get_data(),"Frozen animation time renders identical pixels")
	print("DRONE NATIVE CAPTURES COMPLETE")
	quit()
