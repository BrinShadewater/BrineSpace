extends SceneTree
## Regression coverage for owner report loading errors and viewport kelp culling.
var failures := 0
var checks := 0
class GridHarness extends GridCanvas:
	func _ready(): pass
	func _process(_delta): pass
	func _draw(): pass
class ReentrantView extends Node2D:
	var embedded := false
	var same_instance := false
	func _ready():
		same_instance = get_parent()._lazy_view(&"probe",get_script()) == self
class KelpCanvas extends Node2D:
	var view = preload("res://assets/environment/upright-kelp-v1/upright_kelp_view.gd").new()
	var regions: Array = [{"biome":"kelp","center":Vector2(5,5),"radius":1.0},{"biome":"kelp","center":Vector2(80,80),"radius":2.0}]
	var camera := Vector2.ZERO
	var cell_size := 384.0
	var clock := 0.0
	var culled := false
	func _draw():
		draw_set_transform(-camera)
		view.render_into(self,cell_size,regions,clock,Rect2(camera,Vector2(512,512)) if culled else Rect2())
func _init(): call_deferred("run")
func check(ok: bool,message: String):
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func run():
	var grid := GridHarness.new()
	root.add_child(grid)
	var view = grid._lazy_view(&"probe",ReentrantView)
	check(view.same_instance,"Loading-time reentry must return the in-progress room instance")
	check(grid.lazy_views.size()==1 and grid.get_child_count()==1,"Reentry must not duplicate rooms")
	grid.free()
	var archive = preload("res://scripts/title_archive.gd").new()
	archive.meta_state = preload("res://scripts/meta_state.gd").new()
	archive.meta_state.save_path = "user://report-regression.meta"
	root.add_child(archive)
	archive.show_section("about")
	var labels := ""
	for node in archive.find_children("*","Label",true,false): labels += node.text + "\n"
	check(labels.contains("BUILD ID") and labels.contains("ENGINE"),"Credits must include complete build information")
	check(labels.contains("STUDIO") and labels.contains("RIGHTS"),"Credits must finish building after version text")
	archive.free()
	root.content_scale_size = Vector2i(512,512)
	root.size = Vector2i(512,512)
	var canvas := KelpCanvas.new()
	root.add_child(canvas)
	var prefs = preload("res://scripts/title_settings.gd")
	for setting in range(3):
		prefs.reduced_motion = setting==1
		prefs.effects_quality = 0 if setting==2 else 2
		for size in [192.0,384.0,768.0]:
			canvas.cell_size = size
			var anchor: Vector2 = Vector2(4.8,5.65)*size
			for offset in [Vector2(256,256),Vector2(-15,100),Vector2(530,100),Vector2(256,-15)]:
				canvas.camera = anchor-offset
				for clock in [0.0,2.0,6.0]:
					canvas.clock = clock
					canvas.culled = false
					canvas.queue_redraw()
					await RenderingServer.frame_post_draw
					var expected := root.get_texture().get_image().get_data()
					canvas.culled = true
					canvas.queue_redraw()
					await RenderingServer.frame_post_draw
					check(expected==root.get_texture().get_image().get_data(),"Kelp pixels must match at viewport edges, zooms and motion settings")
	canvas.free()
	print("REPORT REGRESSIONS: %d checks / %d failures" % [checks,failures])
	quit(failures)
