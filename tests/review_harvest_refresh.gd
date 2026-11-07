extends "res://tests/review_station_motion.gd"
## Supplied art states; stock conservation is verified separately by finite-harvest tests.
const DEST="res://output/harvest-refresh-v1/"
const Art=preload("res://scripts/harvest_site_art.gd")
const Sites=preload("res://scripts/harvest_sites.gd")
class Sheet extends Node2D:
	var art=Art.new()
	func _draw():
		draw_rect(Rect2(0,0,1150,740),Color("17292d"))
		for row in range(2):
			for col in range(5):
				var base:=Vector2(col*230,row*280)
				draw_rect(Rect2(base+Vector2(5,35),Vector2(220,210)),Color("8b9a91") if col%2==1 else Color("233b41"))
				var site:=Sites.make_site("mining" if row==0 else "salvage",24)
				site.units=24-col*6;site.discovered=true
				art.draw_site(self,site,base+Vector2(115,140),190,true)
				draw_string(ThemeDB.fallback_font,base+Vector2(12,24),"Mining" if row==0 else "Salvage",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
				draw_string(ThemeDB.fallback_font,base+Vector2(12,266),"%d / 24 remaining"%site.units,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
		for i in range(3):
			var identity: String=["mining","frame","cable"][i]
			var at:=Vector2(190+i*380,635)
			var tex: Texture2D=art.texture(identity)
			var extent:=Vector2(95,95.0*tex.get_height()/tex.get_width())
			draw_texture_rect(tex,Rect2(at-extent*.5,extent),false)
			draw_string(ThemeDB.fallback_font,at+Vector2(-110,76),identity+" / source colour, 95px",HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
func capture(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(DEST+name+".png")
func run():
	DirAccess.make_dir_recursive_absolute(DEST)
	Settings.save_path="user://harvest-art.cfg";Settings.pause_unfocused=false
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://harvest-art.meta";game.run_save_path="user://harvest-art.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear();game.site_layout={"scenery":[],"seed":32}
	game.testing_free_build=true;game.testing_disable_failures=true
	for cell in [Vector2i(18,21),Vector2i(22,21)]:game._place_room("battery_array",cell,true)
	game.test_walker_cell=Vector2i(-1,-1)
	game.drone_fleet.sites_initialized=true;game.drone_fleet.sites.clear()
	for row in range(2):
		for col in range(3):
			var site:=Sites.make_site("mining" if row==0 else "salvage",24)
			site.units=[24,12,0][col];site.discovered=true
			game.drone_fleet.sites[Vector2i(19+col,19+row)]=site
	game.powered_room_cells.clear();game.unpowered_room_cells.clear()
	for room in game.placed_rooms:
		game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game.visual_time_seconds=1.3;game._set_paused(true,false)
	game.selected_card_id="";game.selected_room_cell=Vector2i(20,20)
	game.grid_view.env_below_key.clear();game.grid_view.prewarm_station_views(game);game._refresh_all()
	for zoom in [.25,.45]:
		await focus(Vector2(20.5,20),zoom)
		await capture("station-%02d"%roundi(zoom*100))
	for row in range(2):
		await focus(Vector2(19.5,19.5+row),.65)
		await capture("mining-close" if row==0 else "salvage-close")
	var art=game.grid_view.harvest_site_art
	for identity in Art.SOURCES:
		var tex: Texture2D=art.texture(identity)
		check(tex.get_width()==512 and tex.get_image().detect_alpha()!=Image.ALPHA_NONE,"Selected extraction texture has alpha at 512px")
	check(Art.SOURCES.mining=="res://assets/environment/harvest-refresh-v1/runtime/mining.png","Mineral binding")
	check(Art.SOURCES.frame=="res://assets/environment/harvest-refresh-v1/runtime/frame.png","Frame binding")
	check(Art.SOURCES.cable=="res://assets/environment/harvest-refresh-v1/runtime/cable.png","Cable binding")
	check(game.occupied.size()==2 and game.drone_fleet.sites.size()==6,"Art retains supplied room/site counts")
	check(not Sites.blocks(game.drone_fleet.sites,Vector2i(21,19)),"Exhausted mineral site remains buildable")
	check(not Sites.blocks(game.drone_fleet.sites,Vector2i(21,20)),"Exhausted salvage site remains buildable")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No placeholder artwork")
	game.hide();root.content_scale_size=Vector2i(1150,740);root.size=Vector2i(1150,740)
	var sheet:=Sheet.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(DEST+"native-depletion.png")
	print("HARVEST REFRESH REVIEW: %d failures"%failures)
	quit(failures)
