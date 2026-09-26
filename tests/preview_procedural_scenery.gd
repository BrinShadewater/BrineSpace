extends SceneTree
## Art-only native fixture. Paired existing/bought props use production exterior lamps/fog.
class Samples extends Node2D:
	var size_value := 200.0
	var images: Array=[]
	const BOUGHT := ["uw1-188","uw1-193","uw1-145","mat-130"]
	const OLD := ["sub-biomes-v1/brine-seep-stones-v1.png","sub-biomes-v1/coral-lace-coral-v1.png","sub-biomes-v1/kelp-ribbon-kelp-v1.png","driftwood-v1/waterlogged-timber-v1.png"]
	func _ready():
		for path in OLD:
			var img:=Image.new()
			img.load_png_from_buffer(FileAccess.get_file_as_bytes("res://legacy/default/assets/environment/"+path))
			images.append(ImageTexture.create_from_image(img))
	func _draw():
		for i in range(4):
			var width:=size_value*.34
			var at:=Vector2(19.5+i,19.62)*size_value
			var texture: Texture2D=images[i]
			var extent:=texture.get_size()/texture.get_width()*width
			draw_texture_rect(texture,Rect2(at-Vector2(.23*size_value,0)-extent*.5,extent),false,Color(.65,.76,.75,.9))
			preload("res://scripts/site_scenery.gd").draw_asset(self,BOUGHT[i],at+Vector2(.23*size_value,0),width)
func _init(): call_deferred("run")
func run():
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://site_art_preview_%d.json"%OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	game.set_meta("site_seed",32)
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game._set_paused(true,false)
	# Dedicated visual setup, never presented as paid-expedition evidence.
	game.wrecks.clear();game.drone_fleet.sites.clear();game.site_layout.scenery.clear()
	for cell in [Vector2i(19,20),Vector2i(21,20),Vector2i(22,20)]: game._place_room("solar_array",cell,true)
	game.paused=false
	game.Architects.advance_core(game,10.0)
	game._advance_cycle()
	game.crew_comms.minimize()
	game._set_paused(true,false)
	game.grid_view.profile_draw=true
	while game.grid_scroll.size.x<600 or game.grid_scroll.size.y<300: await process_frame
	game._set_grid_zoom(.35,true,Vector2(21.0,20.0)/40.0)
	var deadline:=Time.get_ticks_msec()+5000
	while game._grid_view_center_ratio().distance_to(Vector2(21.0,20.0)/40.0)>.002 and Time.get_ticks_msec()<deadline:
		await process_frame
	await process_frame
	var samples:=Samples.new()
	samples.size_value=game.get_cell_size()
	game.grid_view.env_passes[0].add_child(samples)
	game.grid_view.env_below_key.clear();game.grid_view.queue_redraw()
	await process_frame
	RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png("res://output/procedural-sites-2026-09-23/native-scenery-audition-final.png")
	var frames: Array=[]
	for i in range(60):
		game.grid_view.queue_redraw()
		await process_frame
		RenderingServer.force_draw(false)
		frames.append(game.grid_view.draw_profile_usec.duplicate())
	FileAccess.open("res://output/procedural-sites-2026-09-23/native-render-profile.json",FileAccess.WRITE).store_string(JSON.stringify({"scope":"paused art fixture, 60 warm redraw samples; CPU instrumentation, not FPS benchmark","seed":32,"generation_usec":game.site_layout.generation_usec,"draw_samples":frames,"cell_size":game.get_cell_size(),"viewport":str(root.size)},"  "))
	print("NATIVE SCENERY AUDITION: captured with production light and fog")
	quit()
