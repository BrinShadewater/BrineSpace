extends SceneTree
const Reference = preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
const Candidate = preload("res://assets/environment/rock-blockers-v1/rock_view.gd")
const Field = preload("res://scripts/wreck_field.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":
		push_error("Terrain pixel checks require a native display");quit(2);return
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").simplify_path()
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--profile="): expected=arg.trim_prefix("--profile=")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected:
		push_error("Wrong profile"); quit(2); return
	var results := []
	for size in [16.0,24.3]:
		for offset in [0.0,0.5]:
			for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
				for stage in range(5):
					var field := Field.initial()
					var working:bool=stage in [1,2]
					var selected:=Vector2i(19,20) if stage==2 else Vector2i(16,20)
					if stage==2:
						field[selected]={"kind":"basalt","progress":0.0,"active":false,"cleared":false}
					if working:
						field[selected].progress=9.0
						field[selected].active=true
					if stage==3:
						field[selected].progress=Field.DURATION
						field[selected].cleared=true
					if stage==4:field[Vector2i(12,21)].cleared=true
					var unchanged:Dictionary=field.duplicate(true)
					var views := []
					var renderers := [Reference.new(),Candidate.new()]
					renderers[0].skip_empty_minerals=false
					renderers[1].skip_empty_minerals=true
					for mode in 2:
						var viewport := SubViewport.new()
						viewport.size=Vector2i(512,300)
						viewport.transparent_bg=true
						viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS
						root.add_child(viewport)
						var canvas := Node2D.new()
						canvas.position=-Vector2(10,16)*size+Vector2.ONE*offset
						canvas.texture_filter=filter
						viewport.add_child(canvas)
						canvas.draw.connect(func(): renderers[mode].draw_into(canvas,field,size,1.23,selected,working))
						views.append(viewport)
					await RenderingServer.frame_post_draw
					var a: Image=views[0].get_texture().get_image()
					var b: Image=views[1].get_texture().get_image()
					results.append({"size":size,"offset":offset,"filter":filter,"stage":stage,"state_unchanged":field==unchanged,"exact":a.get_data()==b.get_data(),
						"before":views[0].get_render_info(Viewport.RENDER_INFO_TYPE_CANVAS,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME),
						"after":views[1].get_render_info(Viewport.RENDER_INFO_TYPE_CANVAS,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME)})
					if results.size()==1:
						a.save_png("user://terrain-skip-reference.png")
						b.save_png("user://terrain-skip-candidate.png")
					for view in views: view.queue_free()
					await process_frame
	FileAccess.open("user://terrain-skip-results.json",FileAccess.WRITE).store_string(JSON.stringify(results))
	print("TERRAIN DRAW SKIP ",results.size()," comparisons; exact ",results.filter(func(row):return row.exact).size())
	quit(0 if results.all(func(row):return row.exact and row.state_unchanged and row.after<row.before) else 2)
