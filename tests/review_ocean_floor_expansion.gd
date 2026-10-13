extends "res://tests/review_station_motion.gd"
## Native source/tint/scale, blocker masks and actual station art review.
const DEST := "res://output/ocean-floor-expansion-v1/"
const Ocean := preload("res://assets/environment/ocean-floor-expansion-v1/ocean_floor_view.gd")
const Field := preload("res://scripts/wreck_field.gd")
const Rocks := preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
class Sheet extends Node2D:
	var ocean = Ocean.new()
	var rocks = Rocks.new()
	var references = preload("res://assets/environment/seabed-refresh-v1/seabed_refresh_view.gd").new()
	var cell_pixels := 270.0
	func _draw():
		draw_rect(Rect2(0,0,1500,1200),Color("17292d"))
		var row := 0
		for id in Ocean.WIDTHS:
			draw_string(ThemeDB.fallback_font,Vector2(12,30+row*125),id,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at := Vector2(280+col*245,55+row*125)
				draw_rect(Rect2(at-Vector2(110,48),Vector2(220,96)),Color("929e94") if col%2==0 else Color("233b41"))
				ocean.draw_asset(self,id,at,float(Ocean.WIDTHS[id])*cell_pixels,Color.WHITE if col<2 else Color(.59,.68,.66,.85))
			row += 1
		for id in ["ribbon-kelp","basalt-outcrop"]:
			draw_string(ThemeDB.fallback_font,Vector2(12,30+row*125),"Installed: "+id,HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
			for col in range(4):
				var at := Vector2(280+col*245,55+row*125)
				draw_rect(Rect2(at-Vector2(110,48),Vector2(220,96)),Color("929e94") if col%2==0 else Color("233b41"))
				references.draw_asset(self,id,at,.55*cell_pixels,Color.WHITE if col<2 else Color(.59,.68,.66,.85))
			row += 1
		draw_string(ThemeDB.fallback_font,Vector2(12,1110),"Measured %.1f screen px/cell · .45 zoom · source / underwater tint"%cell_pixels,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
		for col in range(2):
			draw_texture_rect(ocean.texture("fractured-stone" if col==0 else "mineral-vein"),Rect2(1040+col*180,1090,155,105),false)
class Masks extends Node2D:
	var rocks = Rocks.new()
	func _draw():
		draw_rect(Rect2(0,0,1500,1050),Color("354b50"))
		for family in range(2):
			for mask in range(16):
				var origin := Vector2(150+(mask%4)*330,145+(mask/4)*230)
				var cell := Vector2i(9 if family==0 else 27,8)
				var field := {cell:{"kind":"basalt","progress":0.0,"active":false,"cleared":false}}
				for side in range(4):
					if mask & (1<<side): field[cell+Rocks.DIRECTIONS[side]]={"kind":"basalt","progress":0.0,"active":false,"cleared":false}
				draw_set_transform(origin-Vector2(cell)*45+Vector2(family*100,0))
				rocks.draw_into(self,field,45,0,Vector2i(-1,-1),false)
				draw_set_transform(Vector2.ZERO)
				draw_string(ThemeDB.fallback_font,origin+Vector2(0,95),"mask %d"%mask,HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func shot(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(DEST+name+".png")
func run():
	DirAccess.make_dir_recursive_absolute(DEST)
	Settings.initialized=true;Settings.pause_unfocused=false
	game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://ocean_review.meta";game.run_save_path="user://ocean_review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks=Field.initial()
	game.testing_free_build=true;game.testing_disable_failures=true
	game._place_room("brine_core",Vector2i(20,20),true)
	game._place_room("airlock",Vector2i(21,20),true)
	game._place_room("mining_drone_bay",Vector2i(22,20),true)
	game._place_room("construction_drone_bay",Vector2i(22,21),true)
	for turn in range(4):
		game.occupied[Vector2i(22,20)].rotation=turn
		if game._doors_connect("corridor",0,Vector2i.LEFT,game.occupied[Vector2i(22,20)]): break
	game.running=true;game._set_paused(true,false)
	for room in game.placed_rooms:
		game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game.grid_view.env_below_key.clear();game._refresh_all()
	for zoom in [.25,.45,.65]:
		await focus(Vector2(20,20),zoom);await shot("station-%d"%roundi(zoom*100))
	# Diagnostic habitat captures retain production fog/lighting; hidden views
	# cannot be counted as aesthetic acceptance.
	for at in [Vector2(17,20),Vector2(24,19),Vector2(20,9),Vector2(10,26)]:
		await focus(at,.45);await shot("habitat-%d-%d"%[at.x,at.y])
	await focus(Vector2(22.5,20.5),.45)
	var measured_cell: float = game.get_cell_size()*root.get_final_transform().get_scale().x
	var view = Ocean.new();view.prepare()
	check(view.textures.size()==8,"All eight selected sprites load")
	for id in Ocean.SOURCES: check(view.texture(id)!=null,"Texture: "+id)
	check(game.occupied.size()==4,"Decorations add no occupancy")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No source placeholders")
	# Actual paid mining/building path; progress-based waits include travel/recharge.
	game.testing_free_build=false;game.testing_disable_failures=false
	game.resources.metal=20;game.resources.power=10;game.running=true
	game.drone_fleet.sites.clear()
	game.drone_fleet.sites_initialized=true
	game.drone_fleet.synchronize(game.placed_rooms)
	var target := Vector2i(23,20)
	game._toggle_wreck_work(target);game._set_paused(false,false)
	check(game.wrecks[target].active,"Mineral-rich blocker starts mining")
	var steps := 0
	while float(game.wrecks[target].progress)<6.0 and steps<800:
		game._update_wreck_clearance(.25);steps+=1
	check(float(game.wrecks[target].progress)>=6.0,"Actual mining drone reaches partial cut")
	game._set_paused(true,false)
	var partial: float = game.wrecks[target].progress
	game._update_wreck_clearance(5.0)
	check(game.wrecks[target].progress==partial,"Pause freezes actual mineral excavation")
	await shot("mineral-partial-paused")
	game._set_paused(false,false)
	var metal_before: int = game.resources.metal
	steps=0
	while Field.blocks(game.wrecks,target) and steps<800:
		game._update_wreck_clearance(.25);steps+=1
	check(not Field.blocks(game.wrecks,target),"Mining releases mineral blocker footprint")
	steps=0
	while game.resources.metal<metal_before+Field.YIELDS.basalt and steps<800:
		game._update_wreck_clearance(.25);steps+=1
	check(game.resources.metal==metal_before+Field.YIELDS.basalt,"Existing basalt yield retained")
	await shot("mineral-cleared")
	game.selected_card_id="corridor";game.selected_rotation=0;game.hand.assign(["corridor"])
	for turn in range(4):
		game.selected_rotation=turn
		if game.get_placement_problem("corridor",target).is_empty(): break
	metal_before=game.resources.metal
	var cost: int = game.RoomDatabaseScript.get_room("corridor").cost.metal
	game._on_grid_clicked(target)
	check(game.resources.metal==metal_before-cost,"Rebuilding spends normal room cost")
	steps=0
	while not game.occupied.has(target) and steps<800:
		game._update_wreck_clearance(.25);steps+=1
	check(game.occupied.has(target),"Actual construction drone builds in mined footprint")
	game._set_paused(true,false);await shot("mineral-paid-rebuild")
	game.hide();root.content_scale_size=Vector2i(1500,1200);root.size=Vector2i(1500,1200)
	var sheet := Sheet.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	sheet.cell_pixels=measured_cell
	await process_frame;RenderingServer.force_draw(false);await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(DEST+"native-density.png")
	sheet.free()
	var masks := Masks.new();masks.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(masks)
	await process_frame;RenderingServer.force_draw(false);await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(DEST+"blocker-masks.png")
	print("OCEAN FLOOR EXPANSION REVIEW: %d failures"%failures)
	quit(failures)
