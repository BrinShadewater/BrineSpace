extends SceneTree
const View=preload("res://rooms/underwater/batch-two/med_office_view.gd")
var destination:=""
class MedOfficePanel extends Node2D:
	var view
	func _draw() -> void:
		if view!=null: view.render_into(self,Vector2(384,384),1.6)
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): destination=arg.trim_prefix("--output=")
	call_deferred("run")
func run() -> void:
	if destination.is_empty() or DirAccess.dir_exists_absolute(destination):
		push_error("Choose a new --output directory")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(destination)
	root.size=Vector2i(768,768)
	root.content_scale_size=Vector2i(768,768)
	var view:=View.new()
	view.embedded=true
	view.hide()
	root.add_child(view)
	var panel:=MedOfficePanel.new()
	panel.view=view
	root.add_child(panel)
	var failures:=0
	for q in range(4):
		for working in [false,true]:
			var before: Array=[]
			for frame in range(2):
				view.configure_embedded(q,[],working,0.2 if frame==0 else 1.1)
				panel.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				var capture:=root.get_texture().get_image()
				capture.save_png(destination.path_join("q%d-%s-%d.png"%[q,"working" if working else "offline",frame]))
				for i in range(view.props.size()):
					var bounds: Rect2=view.prop_visual_bounds(view.props[i])
					var crop:=Rect2i(Vector2(384,384)+bounds.position*1.6,bounds.size*1.6)
					var pixels:=capture.get_region(crop).get_data()
					if frame==0: before.append(pixels)
					elif (pixels!=before[i])!=(working and view.is_animated_prop(view.props[i])):
						push_error("MedOffice host motion mismatch: "+str(view.props[i].id))
						failures+=1
	if failures==0: print("MED OFFICE PILOT PASS: four rotations, four host motion/offline comparisons; direct renderer state, not economy integration")
	quit(1 if failures else 0)
