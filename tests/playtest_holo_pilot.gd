extends SceneTree
const View=preload("res://rooms/underwater/batch-two/holographic_core_view.gd")
var destination:=""
class FlatHardwareView extends "res://rooms/underwater/batch-two/holographic_core_view.gd":
	# Negative control recreates the old blank bays in this fixture only.
	func draw_registered_prop(prop: Dictionary) -> void:
		super.draw_registered_prop(prop)
		if prop.id=="holo_compute":
			for region in display_regions(prop):
				var start:=life_point(prop,region.position)
				painter.draw_rect(Rect2(start,life_point(prop,region.end)-start),Color("111b23"))
class HoloPanel extends Node2D:
	var view
	func _draw() -> void:
		if view!=null: view.render_into(self,Vector2(384,384),1.6)
class FlatGlassView extends "res://rooms/underwater/batch-two/holographic_core_view.gd":
	func draw_registered_prop(prop: Dictionary) -> void:
		super.draw_registered_prop(prop)
		if operating or prop.id!="holo_terminal": return
		for region in display_regions(prop):
			var start:=life_point(prop,region.position)
			painter.draw_rect(Rect2(start,life_point(prop,region.end)-start),Color("111b23"))
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
	var view=FlatGlassView.new() if "--negative-flat-glass" in OS.get_cmdline_user_args() else (FlatHardwareView.new() if "--negative-flat-hardware" in OS.get_cmdline_user_args() else View.new())
	view.embedded=true
	view.hide()
	root.add_child(view)
	var panel:=HoloPanel.new()
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
					if not working and view.props[i].id=="holo_terminal":
						# Interior samples exclude the bezel; colour variation must belong
						# to dark glass, not bright painted screen content.
						for region in view.display_regions(view.props[i]):
							var inner: Rect2=region.grow(-3)
							var start: Vector2=Vector2(384,384)+view.life_point(view.props[i],inner.position)*1.6
							var end: Vector2=Vector2(384,384)+view.life_point(view.props[i],inner.end)*1.6
							var detail:=capture.get_region(Rect2i(start,end-start))
							var colors: Dictionary={}
							var bright:=false
							for y in range(detail.get_height()):
								for x in range(detail.get_width()):
									var color:=detail.get_pixel(x,y)
									colors[color.to_rgba32()]=true
									bright=bright or maxf(color.r,maxf(color.g,color.b))>0.25
							if colors.size()<2 or bright:
								push_error("Holo offline terminal glass flattened or luminous")
								failures+=1
					if not working and view.props[i].id=="holo_compute":
						for region in view.display_regions(view.props[i]):
							var inner: Rect2=region.grow(-4)
							var start: Vector2=Vector2(384,384)+view.life_point(view.props[i],inner.position)*1.6
							var end: Vector2=Vector2(384,384)+view.life_point(view.props[i],inner.end)*1.6
							var detail:=capture.get_region(Rect2i(start,end-start))
							var colors: Dictionary={}
							for y in range(detail.get_height()):
								for x in range(detail.get_width()): colors[detail.get_pixel(x,y).to_rgba32()]=true
							if colors.size()<8:
								push_error("Holo offline hardware detail flattened")
								failures+=1
					var bounds: Rect2=view.prop_visual_bounds(view.props[i])
					var crop:=Rect2i(Vector2(384,384)+bounds.position*1.6,bounds.size*1.6)
					var pixels:=capture.get_region(crop).get_data()
					if frame==0: before.append(pixels)
					elif (pixels!=before[i])!=working:
						push_error("Holo host motion mismatch: "+str(view.props[i].id))
						failures+=1
	if failures==0: print("HOLO PILOT PASS: four rotations, four host motion/offline comparisons, retained offline bay detail and dark terminal glass; direct renderer state, not economy integration")
	quit(1 if failures else 0)
