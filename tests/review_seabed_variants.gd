extends "res://tests/review_station_motion.gd"
## Art fixture: consumer-owned dimensions/tint, no changed geography or resources.
const DEST="res://output/seabed-variants-v1/"
const Scenery=preload("res://scripts/site_scenery.gd")
class Density extends Node2D:
	func _draw():
		draw_rect(Rect2(0,0,1100,620),Color("17292d"))
		for row in range(4):
			var id: String=Scenery.CHOICES[row]
			draw_string(ThemeDB.fallback_font,Vector2(16,25+row*150),Scenery.REPLACEMENTS[id],HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(145+col*265,83+row*150)
				draw_rect(Rect2(at-Vector2(120,45),Vector2(240,90)),Color("8b9a91") if col%2==0 else Color("233b41"))
				Scenery.draw_asset(self,id,at,95.0,Color.WHITE if col<2 else Color(.65,.76,.75,.9))
				draw_string(ThemeDB.fallback_font,at+Vector2(-110,65),"source / 95px" if col<2 else "runtime tint / 95px",HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
func capture(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(DEST+name+".png")
func run():
	DirAccess.make_dir_recursive_absolute(DEST)
	Settings.save_path="user://scenery-review.cfg";Settings.pause_unfocused=false
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://scenery-review.meta";game.run_save_path="user://scenery-review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear();game.test_walker_cell=Vector2i(-1,-1)
	game.testing_free_build=true;game.testing_disable_failures=true
	for cell in [Vector2i(18,20),Vector2i(21,20)]:game._place_room("battery_array",cell,true)
	game.site_layout={"scenery":[],"seed":32}
	for family in range(4):game.site_layout.scenery.append({"family":family,"at":Vector2(18.5+family,19.3),"size":.32 if family<2 else .45})
	game.site_layout.scenery.append({"family":1,"at":Vector2(18.5,20.5),"size":.36})
	game.site_layout.scenery.append({"family":3,"at":Vector2(21.5,20.5),"size":.45})
	game.powered_room_cells.clear();game.unpowered_room_cells.clear()
	for room in game.placed_rooms:
		game.powered_room_cells[room.pos]=true
		game.grid_view.room_light_levels[room.pos]=1.0
	game.visual_time_seconds=1.3;game._set_paused(true,false);game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	game.grid_view.env_below_key.clear();game.grid_view.prewarm_station_views(game);game._refresh_all()
	for zoom in [.25,.45,.65]:
		await focus(Vector2(20,19.9),zoom)
		await capture("station-%02d"%roundi(zoom*100))
	for family in [1,3]:
		await focus(Vector2(18.5+family,19.6),.65)
		await capture("rounded-close" if family==1 else "driftwood-close")
	check(game.site_layout.scenery.size()==6,"Art render retains authored placements")
	check(game.occupied.size()==2,"Decorative scenery creates no occupancy")
	var view=Scenery.replacement_view
	view.prepare()
	for id in ["rounded-boulders","pale-driftwood"]:
		check(view.textures[id]!=null and view.textures[id].get_width()==512,"Selected variant loads at 512px")
	check(Scenery.REPLACEMENTS["mb-210"]=="rounded-boulders","Rounded rock binding")
	check(Scenery.REPLACEMENTS["mat-131"]=="pale-driftwood","Pale timber binding")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No source artwork placeholders")
	game.hide()
	root.content_scale_size=Vector2i(1100,620);root.size=Vector2i(1100,620)
	var sheet:=Density.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(DEST+"native-density.png")
	print("SEABED VARIANTS REVIEW: %d failures"%failures)
	quit(failures)
