extends SceneTree
const Art=preload("res://scripts/environment_art.gd")
const Hardware=preload("res://scripts/station_hardware.gd")
const Effects=preload("res://scripts/station_effects.gd")
const Preferences=preload("res://scripts/title_settings.gd")
const KEYS=["sprinkler-nozzle","door-threshold","water-drop","water-splash","current-streak","intake-bubble","water-wave","silt-fleck"]
const OUT="res://output/water-detail-v1/"
class Fixture extends RefCounted:
	var time:=1.2
	var hardware={"power":false,"exterior":false}
	var occupied={}
	var powered_room_cells={Vector2i(1,2):true}
	func get_visual_time_seconds() -> float:return time
	func _turbine_intake_clear(_room) -> bool:return true
	func _turbine_intake_cell(_room) -> Vector2i:return Vector2i(0,2)
class Sheet extends Node2D:
	var fixture=Fixture.new()
	func _draw():
		draw_rect(Rect2(0,0,1200,820),Color("233b41"))
		for i in range(KEYS.size()):
			var at:=Vector2(150+(i%4)*300,110+(i/4)*200)
			var tex=Art.texture(KEYS[i])
			draw_string(ThemeDB.fallback_font,at-Vector2(130,80),KEYS[i],HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			var fit:=minf(180.0/tex.get_width(),120.0/tex.get_height())
			Art.sprite(self,KEYS[i],at,tex.get_size()*fit)
		# Native scale: two sprinklers, drops/splashes and turbine flow.
		Hardware.draw_effects(self,fixture,[{"id":"solar_array","pos":Vector2i(3,2),"water_level":.5,"spray_visual_until":100.0}],170)
		var old:=Preferences.reduced_motion
		for reduced in [false,true]:
			Preferences.reduced_motion=reduced
			var cell:=Vector2i(1,3 if reduced else 2)
			fixture.powered_room_cells={cell:true}
			Effects.draw_turbine_flow(self,fixture,[{"id":"current_turbine","pos":cell}],170)
		Preferences.reduced_motion=old
		draw_set_transform(Vector2.ZERO)
		for i in range(4):
			draw_set_transform(Vector2(870+i*70,620),i*PI*.5)
			Art.band(self,"door-threshold",Rect2(-20,-12,40,24))
		draw_set_transform(Vector2.ZERO)
func _init():call_deferred("run")
func capture(name: String):
	await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(OUT+name)
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	for key in KEYS:assert(Art.texture(key)!=null)
	root.content_scale_size=Vector2i(1200,820);root.size=Vector2i(1200,820)
	var sheet:=Sheet.new();root.add_child(sheet)
	await capture("native-sheet-v1.png")
	sheet.queue_redraw();await capture("native-repeat-v1.png")
	assert(FileAccess.get_file_as_bytes(OUT+"native-sheet-v1.png")==FileAccess.get_file_as_bytes(OUT+"native-repeat-v1.png"))
	sheet.fixture.time=1.7;sheet.queue_redraw();await capture("native-time-v1.png")
	assert(FileAccess.get_file_as_bytes(OUT+"native-sheet-v1.png")!=FileAccess.get_file_as_bytes(OUT+"native-time-v1.png"))
	sheet.queue_free();await process_frame
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://water_art_preview.json";game.run_save_path="user://water_art_preview.loop"
	game.set_meta("site_seed",32);root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game._set_paused(true,false)
	for cell in [Vector2i(19,20),Vector2i(21,20),Vector2i(22,20)]:game._place_room("solar_array",cell,true)
	game.paused=false;game.Architects.advance_core(game,10.0);game._advance_cycle()
	game._set_paused(true,false);game.crew_comms.minimize()
	while game.grid_scroll.size.x<600 or game.grid_scroll.size.y<300:await process_frame
	game._set_grid_zoom(.35,true,Vector2(20,20)/40.0)
	var deadline:=Time.get_ticks_msec()+5000
	while game._grid_view_center_ratio().distance_to(Vector2(20,20)/40.0)>.002 and Time.get_ticks_msec()<deadline:await process_frame
	await capture("native-station-v1.png")
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	print("WATER DETAIL: 8 bindings; native effects, pause and reduced motion; station capture; 0 failures")
	quit()
