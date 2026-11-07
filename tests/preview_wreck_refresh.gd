extends SceneTree
const View=preload("res://assets/environment/wrecked-rooms-v1/wreck_view.gd")
const Field=preload("res://scripts/wreck_field.gd")
const OUT="res://output/wreck-refresh-v1/"
class Sheet extends Node2D:
	var view=View.new()
	var field={}
	func _ready():
		for row in range(4):
			for col in range(4):
				field[Vector2i(col,row)]={"kind":Field.TYPES[row],"progress":[0,.44,.6,.94][col]*Field.DURATION,"cleared":false,"active":col==1}
	func _draw():
		draw_rect(Rect2(0,0,1200,1000),Color("233b41"))
		view.draw_into(self,field,220,1.2,Vector2i(-1,-1))
		for row in range(4):
			draw_string(ThemeDB.fallback_font,Vector2(900,45+row*220),Field.TYPES[row],HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for scale_value in [110,55]:
				var tex=view.texture(Field.TYPES[row],"wreck")
				draw_texture_rect(tex,Rect2(920 if scale_value==110 else 1050,65+row*220,scale_value,scale_value),false,Color(.72,.82,.83))
func _init():call_deferred("run")
func capture(name: String):
	await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(OUT+name)
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	var view=View.new()
	for kind in Field.TYPES:
		for stage in ["wreck","stripped"]:
			var tex=view.texture(kind,stage)
			assert(tex!=null and tex.get_size()==Vector2(1024,1024))
			assert(view.texture(kind,stage)==tex)
	root.content_scale_size=Vector2i(1200,1000);root.size=Vector2i(1200,1000)
	var sheet:=Sheet.new();root.add_child(sheet)
	await capture("native-stages-v3.png")
	var before:=sheet.field.duplicate(true)
	sheet.queue_redraw();await capture("native-repeat-v3.png")
	assert(before==sheet.field)
	assert(FileAccess.get_file_as_bytes(OUT+"native-stages-v3.png")==FileAccess.get_file_as_bytes(OUT+"native-repeat-v3.png"))
	# Near-finished interiors must be independent of the removed equipment layer.
	var expected:=Image.new();assert(expected.load(OUT+"native-stages-v3.png")==OK)
	var saved: Dictionary=sheet.view.textures.duplicate()
	var blank:=Image.create(1024,1024,false,Image.FORMAT_RGBA8);blank.fill(Color.TRANSPARENT)
	for kind in Field.TYPES:sheet.view.textures[kind+"-wreck"]=ImageTexture.create_from_image(blank)
	sheet.queue_redraw();await capture("native-no-equipment-reference-v3.png")
	var actual:=Image.new();assert(actual.load(OUT+"native-no-equipment-reference-v3.png")==OK)
	for row in range(4):
		var interior:=Rect2i(693,row*220+33,154,154)
		assert(expected.get_region(interior).get_data()==actual.get_region(interior).get_data(),"Removed machinery leaked into late-clearance interior")
	sheet.view.textures=saved
	sheet.queue_free();await process_frame
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://wreck_art_preview.json";game.run_save_path="user://wreck_art_preview.loop"
	game.set_meta("authored_site_fixture",true);root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game._set_paused(true,false);game.crew_comms.minimize()
	while game.grid_scroll.size.x<600 or game.grid_scroll.size.y<300:await process_frame
	game._set_grid_zoom(.2,true,Vector2(20,20)/40.0)
	var deadline:=Time.get_ticks_msec()+5000
	while game._grid_view_center_ratio().distance_to(Vector2(20,20)/40.0)>.002 and Time.get_ticks_msec()<deadline:await process_frame
	await capture("native-station-v3.png")
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	print("WRECK REFRESH: 8 selected textures; 4 clearance stages; native scale; deterministic drawing; 0 failures")
	quit()

