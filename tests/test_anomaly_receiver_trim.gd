extends SceneTree
const View=preload("res://rooms/underwater/batch-two/anomaly_lab_view.gd")
class ReceiverPanel extends Node2D:
	var view
	var origin: Vector2
	func _draw() -> void:
		var host: Dictionary=view.props[3]
		origin=Vector2(384,384)-view.prop_visual_bounds(host).get_center()*4.0
		draw_set_transform(origin,0,Vector2(4,4))
		view.painter=self
		view.draw_registered_prop(host)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(768,768)
	root.content_scale_size=root.size
	var view:=View.new()
	view.embedded=true
	view.hide()
	root.add_child(view)
	var panel:=ReceiverPanel.new()
	panel.view=view
	root.add_child(panel)
	var failures:=0
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		panel.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var capture:=root.get_texture().get_image()
		for sample in [[Vector2(1022,939),true],[Vector2(1038,948),true],[Vector2(1028,944),false],[Vector2(1032,944),false]]:
			var screen:=Vector2i(panel.origin+view.life_point(view.props[3],sample[0])*4.0)
			var color:=capture.get_pixelv(screen)
			var peak:=maxf(color.r,maxf(color.g,color.b))
			if (sample[1] and peak<0.45) or (not sample[1] and peak>0.3):
				push_error("Receiver must retain pale trim around a dark lens: q%d source%s"%[q,sample[0]])
				failures+=1
	print("ANOMALY RECEIVER TRIM: ",failures," failures; four rotations, two trim and two unlit lens samples each; visual review separate")
	quit(1 if failures>0 else 0)
