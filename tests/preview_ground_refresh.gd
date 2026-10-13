extends SceneTree
const Art=preload("res://scripts/environment_art.gd")
const Rock=preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
const Seabed=preload("res://assets/environment/seabed-v1/seabed_background.gd")
const OUT="res://output/ground-refresh-v1/"
class Sheet extends Node2D:
	var old={}
	var rock=Rock.new()
	var field={Vector2i(1,3):{"kind":"basalt","progress":12.0,"active":true,"cleared":false},Vector2i(2,3):{"kind":"basalt","progress":0.0,"active":false,"cleared":false}}
	func _ready():
		old.silt=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/assets/environment/seabed-v1/silt-plain-source-v1.png")
		old.basalt=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/assets/environment/rock-blockers-v1/basalt-surface-v1.png")
	func _draw():
		draw_rect(Rect2(0,0,1200,900),Color("233b41"))
		for row in range(2):
			var key: String=["silt-plain","basalt-surface"][row]
			draw_string(ThemeDB.fallback_font,Vector2(20,28+row*300),key+" / old | new source | new game tint | mirrored join",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var tex: Texture2D=old.silt if row==0 else old.basalt
				if col>0:tex=Art.texture(key)
				var rect:=Rect2(20+col*300,45+row*300,270,240)
				var tint:=Color.WHITE if col<2 else (Color(.49,.60,.64) if row==0 else Color(.73,.85,.86))
				if col<3:draw_texture_rect(tex,rect,false,tint)
				else:
					for tile in range(2):
						var at:=rect.position+Vector2(tile*135,0)
						draw_set_transform(at+Vector2(135 if tile==1 else 0,0),0,Vector2(-1 if tile==1 else 1,1))
						draw_texture_rect(tex,Rect2(0,0,135,240),false,tint)
						draw_set_transform(Vector2.ZERO)
		Art.sprite(self,"tube-worms",Vector2(900,700),Vector2.ONE*160)
		Art.sprite(self,"tube-worms",Vector2(1100,700),Vector2.ONE*65,Color(.33,.48,.52,.75))
		# Connected natural blockers with existing edge/crack and cutting textures.
		rock.draw_into(self,field,200,1.2,Vector2i(-1,-1))
func _init():call_deferred("run")
func capture(name: String):
	await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(OUT+name)
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	var seabed=Seabed.new();seabed.prepare()
	assert(seabed.textures["silt-plain"]==Art.texture("silt-plain"))
	assert(seabed.textures["tube-worms"]==Art.texture("tube-worms"))
	assert(Rock.new().texture()==Art.texture("basalt-surface"))
	var duplicate=Seabed.new();duplicate.prepare();assert(duplicate.scenery==seabed.scenery)
	assert(Art.texture("silt-plain").get_size()==Vector2(1024,1024))
	root.content_scale_size=Vector2i(1200,900);root.size=Vector2i(1200,900)
	var sheet:=Sheet.new();root.add_child(sheet)
	await capture("native-comparison-v1.png")
	var before:=sheet.field.duplicate(true)
	sheet.queue_redraw();await capture("native-repeat-v1.png")
	assert(before==sheet.field)
	assert(FileAccess.get_file_as_bytes(OUT+"native-comparison-v1.png")==FileAccess.get_file_as_bytes(OUT+"native-repeat-v1.png"))
	sheet.queue_free();await process_frame
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://ground_art_preview.json";game.run_save_path="user://ground_art_preview.loop"
	game.set_meta("site_seed",32);root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game._set_paused(true,false)
	# Dedicated art fixture, preserving production fog and lamp rules.
	for cell in [Vector2i(19,20),Vector2i(21,20),Vector2i(22,20)]:game._place_room("solar_array",cell,true)
	game.paused=false;game.Architects.advance_core(game,10.0);game._advance_cycle()
	game._set_paused(true,false);game.crew_comms.minimize()
	while game.grid_scroll.size.x<600 or game.grid_scroll.size.y<300:await process_frame
	game._set_grid_zoom(.35,true,Vector2(20,20)/40.0)
	var deadline:=Time.get_ticks_msec()+5000
	while game._grid_view_center_ratio().distance_to(Vector2(20,20)/40.0)>.002 and Time.get_ticks_msec()<deadline:await process_frame
	await capture("native-station-v1.png")
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	print("GROUND REFRESH: 3 selected bindings; unchanged placement; paused drawing; 0 failures")
	quit()
