extends SceneTree
const Assembly=preload("res://scripts/room_construction_art.gd")
const Materials=preload("res://scripts/construction_materials.gd")
const OUT="res://output/construction-art-v1/"
class Sheet extends Node2D:
	var grid
	var progress:=.5
	var rotations:=false
	func _draw():
		draw_rect(Rect2(0,0,1500,1100),Color("233b41"))
		var ids: Array=["life_support","med_bay","solar_array","corridor","corner","tee_corridor"]
		if rotations:
			for row in range(3):
				for q in range(4):Assembly.draw(grid,{"id":ids[row+3],"pos":Vector2i(q+1,row+1),"rotation":q},progress)
		else:
			for i in range(ids.size()):Assembly.draw(grid,{"id":ids[i],"pos":Vector2i(i%3+1,i/3+1),"rotation":0},progress)
func _init():call_deferred("run")
func capture(name: String):
	await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(OUT+name)
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	for key in Materials.PATHS:assert(Materials.texture(key)!=null)
	for id in ["corridor","corner","tee_corridor"]:
		for q in range(4):
			var room: Dictionary={"id":id,"rotation":q}
			var mask:=Materials.hull(room)
			assert(mask.size()>4)
			assert(Geometry2D.is_point_in_polygon(Vector2.ZERO,mask))
	root.content_scale_size=Vector2i(1200,900);root.size=Vector2i(1200,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://construction_art_preview.json";game.run_save_path="user://construction_art_preview.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	root.content_scale_size=Vector2i(1400,1100);root.size=Vector2i(1400,1100)
	game._set_paused(true,false);game.set_process(false);game.tick_timer.stop();game.hide()
	game._set_grid_zoom(.35,true,Vector2(.5,.5))
	var grid=game.grid_view
	var orders: Array=game.drone_fleet.orders.duplicate(true)
	var saved_target=grid.draw_target
	FileAccess.open(OUT+"capture-geometry.json",FileAccess.WRITE).store_string(JSON.stringify({"cell_size":grid._cell_size(),"design":root.content_scale_size,"physical":root.size}))
	var sheet:=Sheet.new();sheet.grid=grid;root.add_child(sheet);grid.draw_target=sheet
	for index in range(20):
		sheet.progress=float(index)/19.0;sheet.queue_redraw()
		await capture("motion-%02d.png"%index)
	sheet.progress=.5;sheet.rotations=true;sheet.queue_redraw();await capture("hallway-rotations-frame-v1.png")
	sheet.queue_redraw();await capture("hallway-rotations-repeat-v1.png")
	assert(FileAccess.get_file_as_bytes(OUT+"hallway-rotations-frame-v1.png")==FileAccess.get_file_as_bytes(OUT+"hallway-rotations-repeat-v1.png"))
	sheet.progress=.95;sheet.queue_redraw();await capture("hallway-rotations-fitted-v1.png")
	assert(orders==game.drone_fleet.orders)
	grid.draw_target=saved_target
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	print("CONSTRUCTION ART: painted materials; 12 hallway orientations; 20 work-driven frames; stable paused frame; unchanged orders; 0 failures")
	quit()
