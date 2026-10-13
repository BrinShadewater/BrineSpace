extends SceneTree
const C=preload("res://scripts/companions.gd")
const Art=preload("res://scripts/margot_cryo_art.gd")
const OUT="res://output/margot-cryo-landing-v13"
var game
func _init():call_deferred("run")
func settle():
	game.grid_view.queue_redraw()
	for i in range(3):await process_frame
	await RenderingServer.frame_post_draw
func run():
	assert(Art.lid_travel(Art.OPEN_START,true,false)==0 and Art.lid_travel(Art.OPEN_END,true,false)==Art.DOOR_TRAVEL,"Full painted door retracts")
	assert(Art.lid_travel(0.0,false,true)==Art.DOOR_TRAVEL,"Recovered pod retains full open door")
	assert(Art.layer("door").get_pixel(256,355).a==0.0,"Painted door aperture is true alpha")
	assert(Art.cover_rect(Art.OPEN_START,true)==Art.GLASS,"Cover begins closed")
	assert(Art.cover_rect(4.3,true).position.y<Art.GLASS.position.y,"Cover slides upward")
	var overlap:=Art.cover_rect(Art.OPEN_END,true).intersection(Art.GLASS)
	assert(overlap.position==Art.GLASS.position and overlap.size==Vector2i(61,9),"Higher open glass retains a small top overlap")
	assert(Art.cover_rect(6.0,false)==Art.GLASS,"Unstarted cover stays closed")
	var aperture_test:=Image.create(512,512,false,Image.FORMAT_RGBA8)
	var test_cloud:=Image.create(48,34,false,Image.FORMAT_RGBA8)
	test_cloud.fill(Color.WHITE)
	Art.blend_inside(aperture_test,test_cloud,Art.GLASS.end-Vector2i(20,20))
	assert(aperture_test.get_used_rect()==Rect2i(Art.GLASS.end-Vector2i(20,20),Vector2i(20,20)),"Internal vapour stays behind right and lower rim")
	assert(Art.unfreezing(0.0)==0.0 and Art.unfreezing(Art.OPEN_START)==1.0,"Startup unfreezing completes before opening")
	assert(Art.unfreezing(2.0)>0.0 and Art.unfreezing(2.0)<1.0,"Frost clears gradually")
	assert(is_zero_approx(Art.hop_height(Art.OPEN_END)) and is_zero_approx(Art.hop_height(Art.LANDING)),"Hop starts and lands at registered feet")
	assert(is_equal_approx(Art.hop_height((Art.OPEN_END+Art.LANDING)*0.5),7.0),"Small seven-unit hop apex")
	assert(Art.cold_color(0.0)==Art.cold_color(Art.LANDING),"Colour returns only after floor contact")
	assert(Art.cold_color(8.0)==Color.WHITE,"Natural selected cat colour restored")
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://margot-cryo.meta"
	game.run_save_path="user://margot-cryo.loop"
	game.meta.selected_companion_ids=[]
	root.size=Vector2i(1600,900);root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop()
	var cell: Vector2i=C.CELLS.margot
	# Inspect the unpowered found ward through an actual diver lamp. Unsurveyed
	# open water is intentionally obscured by the exterior fog renderer.
	var lamp=game.bill_npc
	var saved_lamp:=[lamp.active,lamp.movement_medium,lamp.foot,lamp.direction]
	lamp.active=true;lamp.movement_medium="exterior";lamp.direction="north"
	lamp.foot=(Vector2(cell)+Vector2(0.5,0.7))*384.0
	game.selected_card_id="";game.hovered_card_id="";game.selected_room_cell=cell
	game._refresh_all();await settle()
	game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room();await settle()
	game.inspector_focus_button.set_meta("cell",cell);game._focus_inspected_room();await settle()
	# Inspect the actual unpowered/worn room pass without the exterior fog overlay;
	# this capture checks artwork, not exploration visibility or fog balance.
	var exterior_fog=game.grid_view.env_passes[game.grid_view.Env.FOG]
	exterior_fog.modulate=Color(1,1,1,0)
	await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT.path_join("found.png"))
	exterior_fog.modulate=Color.WHITE
	lamp.active=saved_lamp[0];lamp.movement_medium=saved_lamp[1]
	lamp.foot=saved_lamp[2];lamp.direction=saved_lamp[3]
	if "--found-only" in OS.get_cmdline_user_args():
		print("MARGOT FOUND VISUAL PASS: unpowered/worn room pass; exterior fog omitted for artwork inspection")
		quit();return
	game._place_room("corridor",Vector2i(20,21),true)
	game.resources.metal=40
	preload("res://scripts/ward_repair.gd").use_clock()
	game.paused=false;C.toggle(game,cell);game._update_wreck_clearance(18)
	assert(game.occupied.has(cell),"Pet ward repaired")
	game.powered_room_cells[cell]=true
	game.grid_view.room_light_levels[cell]=1.0
	game.selected_card_id="";game.selected_room_cell=cell
	game.inspector_focus_button.set_meta("cell",cell);game._refresh_all()
	await settle();game._focus_inspected_room();await settle()
	root.get_texture().get_image().save_png(OUT.path_join("repaired-closed.png"))
	C.toggle(game,cell);game.paused=true
	var site: Dictionary=game.wrecks[cell]
	var actor=game.companion_actors.margot
	for key in ["nap-south","nap-exit-south"]:
		for body in actor.poses.frames[key]:
			var bounds: Rect2i=body.get_image().get_used_rect()
			var fitted:=Art.fit_inside(Vector2(251.5,250),bounds)
			assert(fitted.x-92+bounds.position.x>=Art.GLASS.position.x+2,"Wake clears left rim")
			assert(fitted.x-92+bounds.end.x<=Art.GLASS.end.x-2,"Wake clears right rim")
	for index in range(101):
		site.boot=index*0.08
		var texture:=C.margot_pod_texture(game,cell)
		assert(texture.get_meta("crew_standing_height")==148.0,"Selected cat density")
		assert(C.margot_pod_texture(game,cell)==texture,"Pause reuses identical frame")
		assert(not actor.active,"Cat remains in emergence until powered completion")
		await settle()
		texture.get_image().save_png(OUT.path_join("layer-%03d.png"%index))
		if index%10==0:root.get_texture().get_image().save_png(OUT.path_join("native-%03d.png"%index))
	var expected: Vector2=C.spawn_point(actor,cell)
	var origin: Vector2=(Vector2(cell)+Vector2.ONE*0.5)*384.0+Art.FOOT
	var landing_pixel:=Art.PIVOT+(expected-origin)*Art.DENSITY
	var final_pose: Image=actor.player.frame_at_elapsed("idle-south",0.0).get_image()
	var at:=Vector2i((landing_pixel-Vector2(92,172)).round())
	var final_image: Image=C.margot_pod_texture(game,cell).get_image()
	var visible_bounds:=Rect2i(at+final_pose.get_used_rect().position,final_pose.get_used_rect().size)
	assert(Rect2i(Vector2i.ZERO,final_image.get_size()).encloses(visible_bounds),"Full landing silhouette, including paws, fits animation canvas")
	for y in range(final_pose.get_height()):
		for x in range(final_pose.get_width()):
			var pixel:=final_pose.get_pixel(x,y)
			if pixel.a>0.99:
				assert(final_image.get_pixelv(at+Vector2i(x,y)).is_equal_approx(pixel),"Final animated pose retains every opaque selected cat pixel")
	game.paused=false;C.advance(game,0.001);game.paused=true
	assert(site.recovered and actor.active,"Single cat released")
	assert(actor.foot.distance_to(expected)<0.01,"Animated and live landing share navigation point")
	C.margot_pod_texture(game,cell).get_image().save_png(OUT.path_join("empty-open.png"))
	await settle();root.get_texture().get_image().save_png(OUT.path_join("released.png"))
	print("MARGOT CRYO PASS: density, selected poses, pause and landing")
	quit()
