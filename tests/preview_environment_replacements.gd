extends SceneTree
const Art=preload("res://scripts/environment_art.gd")
const Rock=preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
const Wreck=preload("res://assets/environment/wrecked-rooms-v1/wreck_view.gd")
const Hardware=preload("res://scripts/station_hardware.gd")
const OUT="res://output/procedural-replacements-v1/"
class EffectsGame extends RefCounted:
	func get_visual_time_seconds() -> float: return 1.2
class Sheet extends Node2D:
	var rocks=Rock.new()
	var wrecks=Wreck.new()
	var field: Dictionary={}
	var clock:=1.2
	func _ready():
		for i in range(16):
			var at:=Vector2i(i%8,i/8)*3+Vector2i(1,9)
			field[at]={"kind":"basalt","progress":float(i)*2,"active":true,"cleared":false}
			for side in range(4):
				if i & (1<<side): field[at+Rock.DIRECTIONS[side]]={"kind":"basalt","progress":0.0,"active":false,"cleared":false}
			assert(Rock.connections(field,at)==i)
	func _draw():
		draw_rect(Rect2(0,0,1400,1000),Color("233b41"))
		var index:=0
		for key in Art.PATHS:
			var at:=Vector2(120+(index%6)*230,95+(index/6)*180)
			draw_string(ThemeDB.fallback_font,at-Vector2(100,65),key,HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
			var tex=Art.texture(key)
			var extent:=Vector2(190,minf(110,190*tex.get_height()/float(tex.get_width())))
			Art.sprite(self,key,at,extent)
			index+=1
		rocks.draw_into(self,field,55,clock,Vector2i(-1,-1))
		for i in range(4): Hardware.draw_exterior_light(self,Vector2(950+i*100,480),Vector2.DOWN.rotated(i*PI*.5),384,true,float(i)/3.0)
		const Preferences=preload("res://scripts/title_settings.gd")
		var old_quality:=Preferences.effects_quality
		var old_reduced:=Preferences.reduced_motion
		for quality in range(3):
			for reduced in [false,true]:
				Preferences.effects_quality=quality;Preferences.reduced_motion=reduced
				preload("res://scripts/station_effects.gd").draw_hazards(self,EffectsGame.new(),[{"pos":Vector2i(9+quality,8 if reduced else 7),"hull_crack":.5}],80)
		Preferences.effects_quality=old_quality;Preferences.reduced_motion=old_reduced
func _init(): call_deferred("run")
func capture(name: String):
	await process_frame
	RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(OUT+name)
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	for key in Art.PATHS:
		assert(Art.texture(key)!=null,key)
		assert(Art.texture(key)==Art.texture(key))
	root.content_scale_size=Vector2i(1400,1000);root.size=Vector2i(1400,1000)
	var sheet:=Sheet.new();root.add_child(sheet)
	await capture("native-sheet-v1.png")
	var before:=sheet.field.duplicate(true)
	sheet.queue_redraw();await capture("native-sheet-repeat-v1.png")
	assert(before==sheet.field)
	assert(FileAccess.get_file_as_bytes(OUT+"native-sheet-v1.png")==FileAccess.get_file_as_bytes(OUT+"native-sheet-repeat-v1.png"))
	sheet.clock=1.7;sheet.queue_redraw();await capture("native-sheet-time-v1.png")
	assert(FileAccess.get_file_as_bytes(OUT+"native-sheet-v1.png")!=FileAccess.get_file_as_bytes(OUT+"native-sheet-time-v1.png"))
	sheet.queue_free();await process_frame
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://environment_art_preview.json"
	game.run_save_path="user://environment_art_preview.loop"
	game.set_meta("site_seed",32)
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game._set_paused(true,false)
	# Dedicated art fixture: paid-run behavior is not asserted by this capture.
	for cell in [Vector2i(19,20),Vector2i(21,20),Vector2i(22,20)]:game._place_room("solar_array",cell,true)
	game.paused=false;game.Architects.advance_core(game,10.0);game._advance_cycle()
	game._set_paused(true,false)
	game.crew_comms.minimize()
	while game.grid_scroll.size.x<600 or game.grid_scroll.size.y<300: await process_frame
	game._set_grid_zoom(.35,true,Vector2(20,20)/40.0)
	var deadline:=Time.get_ticks_msec()+5000
	while game._grid_view_center_ratio().distance_to(Vector2(20,20)/40.0)>.002 and Time.get_ticks_msec()<deadline: await process_frame
	await capture("native-station-v1.png")
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	print("ENVIRONMENT REPLACEMENTS: 12 textures; cached raw loads; deterministic draws; station capture; 0 failures")
	quit()
