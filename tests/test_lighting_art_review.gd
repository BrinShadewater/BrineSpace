extends SceneTree
const Art = preload("res://scripts/lighting_art.gd")
const Lighting = preload("res://rooms/whole-room/room_lighting.gd")
const Effects = preload("res://scripts/station_effects.gd")
const Visibility = preload("res://scripts/underwater_visibility.gd")
const Preferences = preload("res://scripts/title_settings.gd")
class Fixture:
	extends Node2D
	var reference := false
	var angle := 0.0
	var game := preload("res://tests/test_lighting_art.gd").FakeGame.new()
	func _draw() -> void:
		draw_rect(Rect2(0,0,1600,900),Color(.035,.075,.095))
		for i in range(3):
			var centre := Vector2(260+i*500,200)
			draw_rect(Rect2(centre-Vector2(192,120),Vector2(384,260)),Color(.10,.13,.14))
			Lighting.draw_halos(self,1.0,i==1,i==0,[centre])
			if reference: Lighting._blob(self,centre+Vector2(0,80),Vector2(54,54),Color(.30,.04,.03))
			else: Lighting._beacon(self,centre+Vector2(0,80),Vector2(54,54),angle,Color(.30,.04,.03))
		# Runtime bubble stream at 1:1 world/art scale. Room cells only provide anchors.
		var rooms: Array=[]
		for x in range(4): rooms.append({"pos":Vector2i(x,1)})
		Effects.draw_hull_bubbles(self,game,rooms,384)
func _initialize() -> void: call_deferred("run")
func capture(canvas, path: String) -> Image:
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var result := root.get_texture().get_image()
	result.save_png(path)
	return result
func run() -> void:
	var directory := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): directory=arg.trim_prefix("--capture-dir=")
	if directory.is_empty(): quit(2); return
	DirAccess.make_dir_recursive_absolute(directory)
	root.size=Vector2i(1600,900); root.content_scale_size=Vector2i(1600,900)
	Preferences.effects_quality=2; Preferences.reduced_motion=false
	var canvas := Fixture.new(); root.add_child(canvas)
	var fog := ColorRect.new(); fog.position=Vector2(0,500); fog.size=Vector2(1600,400)
	var visibility := Visibility.new();fog.material=visibility.material
	visibility.material.set_shader_parameter("cell_size",128.0)
	visibility.material.set_shader_parameter("clock",12.0)
	visibility.material.set_shader_parameter("motion",0.0)
	visibility.material.set_shader_parameter("caustic_light",1.0)
	canvas.add_child(fog)
	var saved := Art.textures.duplicate()
	for key in ["warm","cool","bubbles"]: Art.textures[key]=null
	canvas.reference=true;visibility.material.set_shader_parameter("use_caustics_tex",false)
	await capture(canvas,directory.path_join("lighting-procedural.png"))
	Art.textures=saved;canvas.reference=false
	visibility.material.set_shader_parameter("use_caustics_tex",true)
	for i in range(4):
		canvas.angle=float(i)*PI*.5
		await capture(canvas,directory.path_join("lighting-authored-%d.png"%i))
	var first := await capture(canvas,directory.path_join("lighting-frozen.png"))
	var second := await capture(canvas,directory.path_join("lighting-frozen-repeat.png"))
	var failures := 0 if first.get_data()==second.get_data() else 1
	Preferences.effects_quality=0
	await capture(canvas,directory.path_join("lighting-low.png"))
	Preferences.effects_quality=2;Preferences.reduced_motion=true
	await capture(canvas,directory.path_join("lighting-reduced-motion.png"))
	print("LIGHTING NATIVE REVIEW: failures=",failures)
	canvas.queue_free(); await process_frame
	quit(1 if failures else 0)
