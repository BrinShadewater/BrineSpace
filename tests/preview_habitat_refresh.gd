extends SceneTree
const View=preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const OUT="res://output/habitat-refresh-v1/"
class Sheet extends Node2D:
	var view=View.new()
	var old: Dictionary={}
	func _ready():
		view.prepare()
		old["coral-cup-corals"]=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/assets/environment/sub-biomes-v1/coral-cup-corals-v1.png")
		old["sponge-sea-fans"]=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/assets/environment/sub-biomes-v1/sponge-sea-fans-v2.png")
	func sprite(tex: Texture2D, at: Vector2, width: float, tint: Color):
		var extent:=Vector2(width,width*tex.get_height()/tex.get_width())
		draw_texture_rect(tex,Rect2(at-extent*.5,extent),false,tint)
	func _draw():
		draw_rect(Rect2(0,0,1200,820),Color("17292d"))
		for row in range(2):
			var id: String=["coral-cup-corals","sponge-sea-fans"][row]
			draw_string(ThemeDB.fallback_font,Vector2(20,30+row*200),id+" / old | new source | new tint | dark seabed",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(150+col*300,115+row*200)
				draw_rect(Rect2(at-Vector2(135,75),Vector2(270,150)),Color("233b41") if col==3 else Color("8b9a91"))
				var tex: Texture2D=old[id] if col==0 else view.textures[id]
				sprite(tex,at,120,Color.WHITE if col<2 else Color(.59,.68,.66,.85))
		draw_string(ThemeDB.fallback_font,Vector2(20,445),"Coral sediment / source | mirrored source | runtime tint | mirrored tint",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
		for col in range(4):
			var rect:=Rect2(20+col*300,470,260,300)
			draw_set_transform(rect.position+Vector2(rect.size.x if col%2==1 else 0,0),0,Vector2(-1 if col%2==1 else 1,1))
			draw_texture_rect(view.textures["coral-ground"],Rect2(Vector2.ZERO,rect.size),false,Color.WHITE if col<2 else Color(.49,.58,.57,1))
			draw_set_transform(Vector2.ZERO)
class Samples extends Node2D:
	var size_value:=200.0
	var view=View.new()
	var mesh: ArrayMesh
	func _ready():
		view.prepare()
		mesh=View.ground_mesh(Vector2(20.5,19.4),Vector2(2.7,1.8))
	func _draw():
		draw_mesh(mesh,view.textures["coral-ground"],Transform2D().scaled(Vector2.ONE*size_value))
		for i in range(4):
			var id: String=["coral-lace-coral","coral-cup-corals","sponge-vase-sponges","sponge-sea-fans"][i]
			var tex: Texture2D=view.textures[id]
			var width:=size_value*.38
			var extent:=Vector2(width,width*tex.get_height()/tex.get_width())
			draw_texture_rect(tex,Rect2(Vector2(19.5+i,19.62)*size_value-extent*.5,extent),false,Color(.59,.68,.66,.85))
func _init():call_deferred("run")
func capture(filename: String):
	await process_frame
	RenderingServer.force_draw(false)
	var image=root.get_texture().get_image()
	image.save_png(OUT+filename)
func run():
	root.content_scale_size=Vector2i(1200,820);root.size=Vector2i(1200,820)
	var sheet:=Sheet.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(sheet)
	await capture("native-comparison-v3.png")
	for id in ["coral-lace-coral","sponge-vase-sponges","coral-cup-corals","sponge-sea-fans"]:
		assert(sheet.view.textures[id].get_width()==512)
	assert(sheet.view.textures["coral-ground"].get_size()==Vector2(1024,1024))
	assert(sheet.view.textures.size()==21)
	var comparison=View.new();comparison.prepare()
	assert(comparison.props==sheet.view.props)
	sheet.queue_free();await process_frame
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://habitat_art_preview.json"
	game.run_save_path="user://habitat_art_preview.loop"
	game.set_meta("site_seed",32)
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game._set_paused(true,false)
	game.site_layout.scenery.clear()
	for cell in [Vector2i(19,20),Vector2i(21,20),Vector2i(22,20)]:game._place_room("solar_array",cell,true)
	game.paused=false;game.Architects.advance_core(game,10.0);game._advance_cycle()
	game.crew_comms.minimize();game._set_paused(true,false)
	while game.grid_scroll.size.x<600 or game.grid_scroll.size.y<300:await process_frame
	game._set_grid_zoom(.35,true,Vector2(21.0,20.0)/40.0)
	var deadline:=Time.get_ticks_msec()+5000
	while game._grid_view_center_ratio().distance_to(Vector2(21.0,20.0)/40.0)>.002 and Time.get_ticks_msec()<deadline:await process_frame
	var samples:=Samples.new();samples.size_value=game.get_cell_size()
	game.grid_view.env_passes[0].add_child(samples)
	game.grid_view.env_below_key.clear();game.grid_view.queue_redraw()
	await capture("native-station-v3.png")
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	print("HABITAT REFRESH: 21 habitat textures; deterministic placement; 5 selected bindings; 0 failures")
	quit()
