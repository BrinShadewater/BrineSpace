extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const PATHS=["res://character/crew-runtime-walk-v2/bill/manifest.json","res://character/crew-runtime-walk-v2/veld/manifest.json","res://character/crew-runtime-walk-v2/branforth/manifest.json"]
const OUT="res://character/crew-finish-study-v1/"
class Study extends Node2D:
	var actors: Array=[]
	var who:=0
	var direction:=0
	var clock:=0.0
	var paused:=false
	var sprites: Array=[]
	var mats: Array=[]
	func _ready() -> void:
		for row in range(3):
			for col in range(4):
				var sprite:=Sprite2D.new();sprite.centered=false
				sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST if col<2 else CanvasItem.TEXTURE_FILTER_LINEAR
				if col%2==1:
					var mat:=ShaderMaterial.new();mat.shader=load("res://character/crew-finish-study-v1/matte.gdshader");sprite.material=mat;mats.append(mat)
				add_child(sprite);sprites.append(sprite)
	func _process(delta: float) -> void:
		if not paused:clock+=delta
		refresh()
	func refresh() -> void:
		var heading: String=["south","east","north","west"][direction]
		var p=actors[who];var key: String="walk-"+heading
		var tex=p.frame_at_elapsed(key,fposmod(clock,p.cycle_seconds(key)))
		for row in range(3):
			var height: float=[82.,54.,27.][row];var factor:=height/148.0
			for col in range(4):
				var sp: Sprite2D=sprites[row*4+col];sp.texture=tex;sp.scale=Vector2.ONE*factor
				sp.position=Vector2(160+col*270,215+row*185)-Vector2(92,172)*factor
		var rect: Vector4=[Vector4(80,30,105,49),Vector4(101,29,123,47),Vector4.ZERO,Vector4(61,29,83,47)][direction]
		for mat in mats:mat.set_shader_parameter("warm_face",who==1 and direction!=2);mat.set_shader_parameter("face_rect",rect/184.0)
		queue_redraw()
	func _unhandled_key_input(event: InputEvent) -> void:
		if event is InputEventKey and event.pressed and not event.echo:
			if event.keycode==KEY_TAB:who=(who+1)%3
			if event.keycode==KEY_RIGHT:direction=(direction+1)%4
			if event.keycode==KEY_LEFT:direction=(direction+3)%4
			if event.keycode==KEY_SPACE:paused=not paused
	func _draw() -> void:
		draw_rect(Rect2(0,0,1120,730),Color("17252c"))
		draw_string(ThemeDB.fallback_font,Vector2(25,32),["Bill","Maria Veld","James Branforth"][who]+" / "+["South","East","North","West"][direction]+" — finishing study",HORIZONTAL_ALIGNMENT_LEFT,-1,22)
		for col in range(4):draw_string(ThemeDB.fallback_font,Vector2(30+270*col,76),["Current / nearest","Matte / nearest","Current / linear","Matte / linear"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		for row in range(3):
			var y:=105+row*185
			for col in range(4):
				draw_rect(Rect2(25+col*270,y,255,150),Color("414c50"))
				for line in range(5):draw_line(Vector2(25+col*270,y+line*32),Vector2(280+col*270,y+line*32),Color("485256"))
				draw_string(ThemeDB.fallback_font,Vector2(30+col*270,y+20),["Close ~82px","Mid ~54px","Wide ~27px"][row],HORIZONTAL_ALIGNMENT_LEFT,-1,14)
		draw_string(ThemeDB.fallback_font,Vector2(25,687),"Tab: character   Left/Right: direction   Space: pause. Same poses, scale and timing in every column.",HORIZONTAL_ALIGNMENT_LEFT,-1,17)
		draw_string(ThemeDB.fallback_font,Vector2(25,714),"Preview only. Matte compresses highlights; Veld also has a masked warm-skin adjustment. No live artwork changed.",HORIZONTAL_ALIGNMENT_LEFT,-1,15)
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1120,730);root.content_scale_size=Vector2i.ZERO;root.title="BrineSpace — three-scale character finishing study"
	var study:=Study.new()
	for path in PATHS:
		var p=Player.new();p.load_manifest(path);study.actors.append(p)
	root.add_child(study)
	if "capture" in OS.get_cmdline_user_args():
		study.set_process(false)
		for who in range(3):
			for direction in range(4):
				study.who=who;study.direction=direction;study.clock=0.45;study.refresh()
				await process_frame;await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png(OUT+"%s-%s.png"%[["bill","veld","branforth"][who],["south","east","north","west"][direction]])
		study.who=2;study.direction=1
		DirAccess.make_dir_recursive_absolute(OUT+"motion")
		for tick in range(60):
			study.clock=tick*0.05;study.refresh();await process_frame;await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT+"motion/%03d.png"%tick)
		print("FINISH STUDY: 12 comparisons, three scales/four treatments; 60 motion frames");quit()
