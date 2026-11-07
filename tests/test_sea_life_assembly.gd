extends SceneTree
const Life = preload("res://scripts/ocean_life.gd")
class Assembly:
	extends Node2D
	var clock := 55.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,1600,900),Color(0.04,0.08,0.12))
		Life._draw_authored_whale(self,Vector2(800,450),0,70,clock,1.0)
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var path := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): path=arg.trim_prefix("--capture-dir=")
	if path.is_empty(): quit(2); return
	DirAccess.make_dir_recursive_absolute(path)
	root.size=Vector2i(1600,900)
	root.content_scale_size=Vector2i(1600,900)
	if not Life.ready(): print("SEA LIFE ASSEMBLY: failures=1"); quit(1); return
	var canvas:=Assembly.new()
	root.add_child(canvas)
	var failures:=0
	for i in range(8):
		canvas.clock=55.0+float(i)/6
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		if root.get_texture().get_image().save_png(path.path_join("tidewalker-assembly-%02d.png"%i))!=OK: failures+=1
	canvas.clock=55.0
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var frozen:=root.get_texture().get_image()
	frozen.save_png(path.path_join("tidewalker-art-overview.png"))
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	if frozen.get_data()!=root.get_texture().get_image().get_data(): failures+=1
	print("SEA LIFE ASSEMBLY: failures=",failures)
	canvas.queue_free();await process_frame
	quit(1 if failures else 0)
