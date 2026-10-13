extends "res://tests/review_station_motion.gd"
## Native source/tint/scale, blocker masks and actual station art review.
var destination := "res://output/ocean-family-review/"
const Fungi := preload("res://assets/environment/alien-fungi-biomes-v1/fungi_biome_view.gd")
const Ground := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const Ocean := preload("res://assets/environment/ocean-floor-expansion-v1/ocean_floor_view.gd")
const Field := preload("res://scripts/wreck_field.gd")
const Rocks := preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
const Tall := preload("res://assets/environment/tall-sea-plants-v1/tall_plants_view.gd")
const Giant := preload("res://assets/environment/giant-mushrooms-v1/giant_mushroom_view.gd")
const Upright := preload("res://assets/environment/upright-kelp-v1/upright_kelp_view.gd")
class Sheet extends Node2D:
	var ocean=Ocean.new()
	var fungi=Fungi.new()
	var ground=Ground.new()
	var reference=preload("res://assets/environment/seabed-refresh-v1/seabed_refresh_view.gd").new()
	var cell_pixels:=270.0
	var entries: Array=[]
	func _ready():
		ocean.prepare();fungi.prepare();ground.prepare();reference.prepare()
		for id in Ocean.WIDTHS:entries.append({"id":id,"texture":ocean.texture(id),"width":float(Ocean.WIDTHS[id])})
		for id in Fungi.WIDTHS:entries.append({"id":id,"texture":fungi.textures[id],"width":float(Fungi.WIDTHS[id])})
		for id in ["brine-seep-stones","nodules-nodule-cluster","iron-mineral-ledges"]:entries.append({"id":id,"texture":ground.textures[id],"width":.48})
		for id in ["ribbon-kelp","basalt-outcrop"]:entries.append({"id":"Installed: "+id,"texture":reference.textures[id],"width":.55})
	func _draw():
		draw_rect(Rect2(0,0,1600,1830),Color("17292d"))
		for i in range(entries.size()):
			var entry: Dictionary=entries[i]
			var origin:=Vector2((i%2)*800,(i/2)*250)
			draw_string(ThemeDB.fallback_font,origin+Vector2(12,25),entry.id+" / %.2f cell"%entry.width,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=origin+Vector2(100+col*200,135)
				draw_rect(Rect2(at-Vector2(96,100),Vector2(192,200)),Color("929e94") if col%2==0 else Color("233b41"))
				var art: Texture2D=entry.texture
				var extent:=art.get_size()/float(art.get_width())*float(entry.width)*cell_pixels
				draw_texture_rect(art,Rect2(at-extent*.5,extent),false,Color.WHITE if col<2 else Color(.59,.68,.66,.85))
		draw_string(ThemeDB.fallback_font,Vector2(12,1800),"Measured %.1f px/cell: source pale/dark, native tint pale/dark. Installed references share the ruler."%cell_pixels,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
class Materials extends Node2D:
	var ocean=Ocean.new()
	var fungi=Fungi.new()
	var ground=Ground.new()
	var cell_pixels:=270.0
	var entries: Array=[]
	func _ready():
		ocean.prepare();fungi.prepare();ground.prepare()
		for id in ["fractured-stone","mineral-vein"]:entries.append({"id":id,"texture":ocean.texture(id),"span":4.0,"tint":Color(.73,.85,.86)})
		entries.append({"id":"fungal-sediment","texture":fungi.textures["fungal-sediment"],"span":2.99,"tint":Color(.49,.58,.57)})
		for id in ["kelp-ground","sulfur-ground","sponge-ground","brine-ground","nodules-ground","iron-ground"]:entries.append({"id":id,"texture":ground.textures[id],"span":9.2,"tint":Color(.49,.58,.57)})
	func _draw():
		draw_rect(Rect2(0,0,1500,950),Color("17292d"))
		for i in range(entries.size()):
			var e: Dictionary=entries[i]
			var origin:=Vector2((i%3)*500,(i/3)*300)
			draw_string(ThemeDB.fallback_font,origin+Vector2(12,25),e.id+" / overview | native crop",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
			var art: Texture2D=e.texture
			draw_texture_rect(art,Rect2(origin+Vector2(15,55),Vector2(200,200)),false)
			var span:=200.0*art.get_width()/(float(e.span)*cell_pixels)
			draw_texture_rect_region(art,Rect2(origin+Vector2(270,55),Vector2(200,200)),Rect2((art.get_size()-Vector2.ONE*span)*.5,Vector2.ONE*span),e.tint)
		draw_string(ThemeDB.fallback_font,Vector2(12,935),"Native crops use each material's production UV span and tint at %.1f physical px/cell."%cell_pixels,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
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
	root.get_texture().get_image().save_png(destination+name+".png")
func run():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--out="):destination=arg.trim_prefix("--out=").trim_suffix("/")+"/"
	DirAccess.make_dir_recursive_absolute(destination)
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
	# Actual seabed integration through saved/authored habitat geometry after paid work.
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.testing_free_build=true;game.testing_disable_failures=true
	for cell in [Vector2i(9,28),Vector2i(11,28),Vector2i(9,26),Vector2i(11,26)]:game._place_room("battery_array",cell,true)
	game.powered_room_cells.clear();game.unpowered_room_cells.clear()
	for room in game.placed_rooms:game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game.wrecks[Vector2i(12,27)]={"kind":"basalt","progress":0.0,"active":false,"cleared":false}
	for biome in Ground.DEFINITIONS:
		game.site_layout={"seed":biome.hash(),"scenery":[],"habitats":[{"biome":biome,"center":Vector2(10.5,26.5),"radius":Vector2(4,4)}]}
		game.grid_view.env_below_key.clear();game.grid_view.prewarm_station_views(game);game._refresh_all()
		game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1);game.hover_cell=Vector2i(-1,-1)
		game.grid_view.queue_redraw()
		await focus(Vector2(10.5,26.8),.25);await shot("live-"+biome+"-overview")
		await focus(Vector2(10.5,27.6),.45);await shot("live-"+biome)
		await focus(Vector2(12.6,24.8),.45);await shot("live-"+biome+"-canopy")
	check(game.occupied.size()==4,"Combined live art creates no room occupancy")
	var fungi=Fungi.new();fungi.prepare();check(fungi.textures.size()==5,"All five fungi sources load")
	var ground=Ground.new();ground.prepare();check(ground.textures.size()==21,"All final habitat sources load")
	for id in ["sulfur-ground","sponge-ground","brine-ground","nodules-ground","iron-ground","kelp-ground","brine-seep-stones","nodules-nodule-cluster","iron-mineral-ledges"]:
		check(Ground.SELECTED_PATHS.has(id),"Selected whole habitat path: "+id)
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No combined source placeholders")
	check(abs(measured_cell-270.0)<.01,"Normal density remains measured 270 physical px/cell")
	# Verify the production instances, including exact selected pixels, not just a test loader.
	var background=game.grid_view.seabed_background
	for pair in [[background.tall_plants,Tall.SOURCES],[background.giant_mushrooms,Giant.SOURCES],[background.upright_kelp,Upright.SOURCES]]:
		var live_view=pair[0];live_view.prepare()
		check(live_view.textures.size()==3,"Three selected assets in production growth family")
		for id in pair[1]:
			var expected:=Image.load_from_file(pair[1][id])
			check(live_view.textures[id].get_image().get_data()==expected.get_data(),"Production selected pixels: "+id)
	for seed_value in [32,9062026,20260930]:
		var layout=preload("res://scripts/site_generator.gd").generate(seed_value)
		var present: Dictionary={}
		for view_class in [Tall,Giant,Upright]:
			for item in view_class.new().placements(layout.habitats):present[item.id]=true
		check(present.size()==9,"All nine new growth assets occur in generated habitats: %d"%seed_value)
	game.hide();root.content_scale_size=Vector2i(1600,1830);root.size=Vector2i(1600,1830)
	var sheet:=Sheet.new();sheet.cell_pixels=measured_cell;sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	await process_frame;RenderingServer.force_draw(false);await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(destination+"combined-props.png")
	check(sheet.entries.size()==14,"Twelve new props and two installed references on one ruler")
	sheet.free();root.content_scale_size=Vector2i(1500,950);root.size=Vector2i(1500,950)
	var materials:=Materials.new();materials.cell_pixels=measured_cell;materials.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(materials)
	await process_frame;RenderingServer.force_draw(false);await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(destination+"combined-materials.png")
	check(materials.entries.size()==9,"Nine new materials at their production density")
	materials.free();root.content_scale_size=Vector2i(1500,1050);root.size=Vector2i(1500,1050)
	var masks:=Masks.new();masks.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(masks)
	await process_frame;RenderingServer.force_draw(false);await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(destination+"blocker-masks.png")
	masks.free()
	# Reuse the maintained native comparison boards; every family shares the measured ruler.
	for spec in [
		[preload("res://tests/review_tall_sea_plants.gd").Sheet,Vector2i(1500,1000),"combined-tall-plants"],
		[preload("res://tests/review_giant_mushrooms.gd").Sheet,Vector2i(1920,1700),"combined-giant-fungi"],
		[preload("res://tests/review_upright_kelp.gd").Sheet,Vector2i(1500,1500),"combined-upright-kelp"]
	]:
		root.content_scale_size=spec[1];root.size=spec[1]
		var growth=spec[0].new();growth.cell_pixels=measured_cell;growth.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(growth)
		await process_frame;RenderingServer.force_draw(false);await process_frame;RenderingServer.force_draw(false)
		root.get_texture().get_image().save_png(destination+spec[2]+".png")
		growth.free()
	print("COMBINED OCEAN FAMILY REVIEW: %d failures"%failures)
	quit(failures)
