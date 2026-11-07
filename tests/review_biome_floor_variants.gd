extends "res://tests/review_station_motion.gd"
var destination="res://output/biome-floor-variants-v1/"
const View=preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")

const GROUND_IDS=["brine-ground","coral-ground","iron-ground"]
const Variants=preload("res://assets/environment/biome-floor-variants-v1/biome_floor_view.gd")
const OLD_PATHS={
	"brine-ground":"res://assets/environment/habitat-sediments-v1/runtime/brine-ground.png",
	"coral-ground":"res://assets/environment/habitat-refresh-v1/runtime/coral-sediment.png",
	"iron-ground":"res://assets/environment/habitat-sediments-v1/runtime/iron-ground.png"
}
class Sheet extends Node2D:
	var view=Variants.new()
	var old: Dictionary={}
	var clock:=2.0
	func _ready():
		view.prepare()
		for id in GROUND_IDS:old[id]=preload("res://scripts/safe_image.gd").raw_texture(OLD_PATHS[id])
	func _draw():
		draw_rect(Rect2(0,0,1200,750),Color("17292d"))
		for row in range(3):
			var id: String=GROUND_IDS[row]
			draw_string(ThemeDB.fallback_font,Vector2(16,25+row*245),id+" / old field | new field | old native crop | new native crop",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(40+col*295,45+row*245)
				var tex: Texture2D=old[id] if col%2==0 else view.textures[Variants.HABITATS[id.trim_suffix("-ground")]]
				if col<2:draw_texture_rect(tex,Rect2(at,Vector2(190,190)),false)
				else:
					# Actual material ruler: radius 4 x 2.3 field span at 270 physical px/cell.
					var span:=190.0*tex.get_width()/(9.2*270.0)
					draw_texture_rect_region(tex,Rect2(at,Vector2(190,190)),Rect2((tex.get_size()-Vector2.ONE*span)*.5,Vector2.ONE*span),Color(.49,.58,.57))
class Samples extends Node2D:
	var view=View.new()
	var size_value:=200.0
	func select_biome(biome: String):
		view.regions=[{"biome":biome,"center":Vector2(20.5,19.3),"radius":Vector2(4,4)}]
		view.initialized=false;view.meshes.clear();view.props.clear();view.prepare()
		view.props.clear()
		for i in range(2):view.props.append({"id":biome+"-"+View.DEFINITIONS[biome].props[i],"at":Vector2(19.4+1.8*i,19.3),"size":.48})
		queue_redraw()
	func _draw():view.render_into(self,size_value,1.3)
func capture(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(destination+name+".png")
func sheet_capture(sheet,name: String):
	sheet.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(destination+name+".png")
	return root.get_texture().get_image().get_data()
func run():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--out="):destination=arg.trim_prefix("--out=").trim_suffix("/")+"/"
	DirAccess.make_dir_recursive_absolute(destination)
	Settings.save_path="user://biome-floor-variant-review.cfg";Settings.pause_unfocused=false;Settings.effects_quality=1;Settings.reduced_motion=false
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://biome-floor-variant-review.meta";game.run_save_path="user://biome-floor-variant-review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear();game.site_layout={"scenery":[],"seed":32}
	for identity in Architects.IDS:
		var actor=Architects.actor_for(game,identity)
		actor.active=false;actor.foot=Vector2.ZERO
	game.testing_free_build=true;game.testing_disable_failures=true
	for cell in [Vector2i(19,20),Vector2i(20,20),Vector2i(21,20)]:game._place_room("battery_array",cell,true)
	game.test_walker_cell=Vector2i(-1,-1)
	game.powered_room_cells.clear();game.unpowered_room_cells.clear()
	for room in game.placed_rooms:game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game.visual_time_seconds=1.3;game._set_paused(true,false);game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	game.grid_view.env_below_key.clear();game.grid_view.prewarm_station_views(game);game._refresh_all()
	var samples:=Samples.new();game.grid_view.env_passes[0].add_child(samples)
	await focus(Vector2(20.5,19.8),.45)
	samples.size_value=game.get_cell_size()
	for identity in GROUND_IDS:
		samples.select_biome(identity.trim_suffix("-ground"))
		await capture(identity)
	var normal=View.new();normal.prepare()
	var repeated=View.new();repeated.prepare()
	check(normal.textures.size()==21,"All habitat textures load")
	check(normal.props==repeated.props,"Replacement preserves deterministic decoration")
	var variants=Variants.new();variants.prepare()
	check(variants.textures.size()==3,"All three additional materials load")
	for identity in GROUND_IDS:
		var biome: String=identity.trim_suffix("-ground")
		var id: String=Variants.HABITATS[biome]
		var tex: Texture2D=variants.textures[id]
		check(tex.get_width()==1024 and tex.get_height()==1024,"1024-square material")
		check(tex.get_image().detect_alpha()==Image.ALPHA_NONE,"Opaque material field")
		var region={"biome":biome,"center":Vector2(20.5,19.3),"radius":Vector2(4,4)}
		var before=region.duplicate(true)
		check(Variants.variant_for(region)==id,"Production coordinates select alternate material")
		check(variants.texture_for(region,normal.textures[identity])==tex,"Actual alternate texture selected")
		check(region==before,"Material selection preserves saved geometry")
		region.center=Vector2(20,20)
		check(variants.texture_for(region,normal.textures[identity])==normal.textures[identity],"Original material retained")
	check(Variants.variant_for({"biome":"kelp","center":Vector2(20.5,19.3)})=="","Other biomes retain their materials")
	var mesh=View.ground_mesh(Vector2(20,20),Vector2(4,4))
	var arrays=mesh.surface_get_arrays(0)
	var uv: PackedVector2Array=arrays[Mesh.ARRAY_TEX_UV]
	var colours: PackedColorArray=arrays[Mesh.ARRAY_COLOR]
	check(uv[0]!=uv[1],"Continuous ground UVs")
	var has_boundary:=false;var has_interior:=false
	for colour in colours:
		if colour.a==0:has_boundary=true
		if colour.a==1:has_interior=true
	check(has_boundary and has_interior,"Feathered ground boundary retained")
	check(game.occupied.size()==3,"Life artwork creates no room occupancy")
	game.hide();root.content_scale_size=Vector2i(1200,750);root.size=Vector2i(1200,750)
	var sheet:=Sheet.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	var start=await sheet_capture(sheet,"native-comparison")
	sheet.clock=7.0
	var later=await sheet_capture(sheet,"native-later")
	check(start==later,"Mineral props remain static")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing source artwork")
	print("BIOME FLOOR VARIANTS REVIEW: %d failures"%failures)
	quit(failures)
