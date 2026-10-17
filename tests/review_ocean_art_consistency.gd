extends "res://tests/review_station_motion.gd"
var destination="res://output/ocean-art-consistency-v1/"
const View=preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")

const GROUND_IDS=["sulfur-ground","sponge-ground","brine-ground","kelp-ground","coral-ground","nodules-ground","iron-ground"]
const Variants=preload("res://assets/environment/biome-floor-variants-v1/biome_floor_view.gd")
const Detail=preload("res://assets/environment/floor-details-v1/floor_details_view.gd")
const Rock=preload("res://assets/environment/rock-features-v1/rock_feature_view.gd")
const Scenery=preload("res://scripts/site_scenery.gd")
const Generator=preload("res://scripts/site_generator.gd")
const FEATURE_ROWS=[
	["shell-hash",.24,"detail"],["urchin-tests",.20,"detail"],["worm-tubes",.22,"detail"],
	["split-slab",.36,"rock"],["layered-ridge",.36,"rock"],["porous-rock",.36,"rock"],
	["kelp-holdfast",.48,"habitat"],["nodules-brittle-stars",.48,"habitat"],["iron-hydroids",.48,"habitat"]
]
class Sheet extends Node2D:
	var clock:=2.0
	var habitat=View.new()
	var detail=Detail.new()
	var rocks=Rock.new()
	func _ready():habitat.prepare();detail.prepare();rocks.prepare()
	func _draw():
		draw_rect(Rect2(0,0,1200,820),Color("17292d"))
		draw_string(ThemeDB.fallback_font,Vector2(16,25),"Combined size/density: 270 physical px per cell / source and runtime tint",HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color.WHITE)
		for i in range(FEATURE_ROWS.size()):
			var item=FEATURE_ROWS[i];var origin=Vector2(i%3*400,i/3*260+40)
			var tex: Texture2D=(detail.textures if item[2]=="detail" else rocks.textures if item[2]=="rock" else habitat.textures)[item[0]]
			var width: float=item[1]*270.0
			var extent=Vector2(width,width*tex.get_height()/tex.get_width())
			draw_string(ThemeDB.fallback_font,origin+Vector2(14,20),str(item[0])+" / "+str(item[1])+" cell / "+str(snappedf(width,.1))+"px",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
			for col in range(2):
				var at=origin+Vector2(100+col*200,130)
				draw_rect(Rect2(at-Vector2(95,85),Vector2(190,170)),Color("8b9a91") if col==0 else Color("233b41"))
				draw_texture_rect(tex,Rect2(at-extent*.5,extent),false,Color.WHITE if col==0 else Color(.59,.68,.66,.85))
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
	Settings.save_path="user://ocean-art-consistency.cfg";Settings.pause_unfocused=false;Settings.effects_quality=1;Settings.reduced_motion=false
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://ocean-art-consistency.meta";game.run_save_path="user://ocean-art-consistency.loop"
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
	FileAccess.open(destination+"density.json",FileAccess.WRITE).store_string(JSON.stringify({"world_cell":game.get_cell_size(),"physical_cell":game.get_cell_size()*float(root.size.x)/root.content_scale_size.x,"feature_width_cells":[.24,.20,.22,.36,.36,.36,.48,.48,.48],"material_full_uv_cells":9.2},"  "))
	var normal=View.new();normal.prepare()
	var repeated=View.new();repeated.prepare()
	check(normal.textures.size()==21,"All habitat textures load")
	check(normal.props==repeated.props,"Replacement preserves deterministic decoration")
	var variants=Variants.new();variants.prepare()
	check(variants.textures.size()==3,"All three additional materials load")
	for identity in ["brine-ground","coral-ground","iron-ground"]:
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
	var outcomes: Dictionary={}
	for seed_value in range(32):
		var layout=Generator.generate(seed_value+9000)
		var saved=layout.duplicate(true)
		for region in layout.habitats:
			var choice:=Variants.variant_for(region)
			if not outcomes.has(region.biome):outcomes[region.biome]={}
			outcomes[region.biome][choice]=true
		for item in layout.scenery:Scenery.rock_feature_for(item)
		check(saved==layout,"Art selection does not mutate generated site")
	for biome in Variants.HABITATS:check(outcomes[biome].size()==2,"Seeded maps retain original and alternate "+biome+" floors")
	FileAccess.open(destination+"seed-coverage.json",FileAccess.WRITE).store_string(JSON.stringify(outcomes,"  "))
	game.hide();root.content_scale_size=Vector2i(1200,820);root.size=Vector2i(1200,820)
	var sheet:=Sheet.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	var start=await sheet_capture(sheet,"combined-native-size")
	sheet.clock=7.0
	var later=await sheet_capture(sheet,"native-later")
	check(start==later,"Native density board remains stable")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing source artwork")
	print("OCEAN ART CONSISTENCY REVIEW: %d failures"%failures)
	quit(failures)
