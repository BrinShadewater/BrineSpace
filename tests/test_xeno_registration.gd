extends SceneTree
const View=preload("res://rooms/underwater/batch-two/xeno_lab_view.gd")
class FlatView extends "res://rooms/underwater/batch-two/xeno_lab_view.gd":
	func draw_registered_prop(prop: Dictionary) -> void:
		super.draw_registered_prop(prop)
		for region in display_regions(prop):
			var start:=life_point(prop,region.position)
			painter.draw_rect(Rect2(start,life_point(prop,region.end)-start),Color("24242f"))
class XenoMaterialPanel extends Node2D:
	var view
	func _draw() -> void: view.render_into(self,Vector2(384,384),1.6)
func _init() -> void: call_deferred("run")
func run() -> void:
	var view: View=FlatView.new() if "--negative-flat-material" in OS.get_cmdline_user_args() else View.new()
	view.embedded=true
	view.hide()
	root.add_child(view)
	var source:=view.life_texture.get_image()
	var missed:=0
	for prop in view.props:
		var regions:=view.display_regions(prop)
		var bounds:=Rect2(prop.registration.outline[0],Vector2.ZERO)
		for p in prop.registration.outline: bounds=bounds.expand(p)
		var examples: Array=[]
		var count:=0
		for y in range(int(bounds.position.y),int(bounds.end.y)):
			for x in range(int(bounds.position.x),int(bounds.end.x)):
				var c:=source.get_pixel(x,y)
				# Bright violet only; blue paint and green preserved samples are not LEDs.
				if c.r-c.g<0.06 or c.b-c.g<0.10 or c.b<0.28: continue
				var point:=Vector2(x,y)
				if not Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)): continue
				var covered:=false
				for i in range(regions.size()):
					if Geometry2D.is_point_in_polygon(point,view.display_polygon(regions[i],i)): covered=true
				if not covered:
					count+=1
					if examples.size()<24: examples.append(point)
		missed+=count
		if count>0: print("UNCOVERED ",prop.id,": ",count," bright violet pixels; examples ",examples)
	if missed>0: push_error("Xeno bright violet pixels outside replacement apertures: "+str(missed))
	else: print("XENO SOURCE APERTURES PASS: bright violet indicator coverage")
	root.size=Vector2i(768,768)
	root.content_scale_size=root.size
	var panel:=XenoMaterialPanel.new()
	panel.view=view
	root.add_child(panel)
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		panel.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var image:=root.get_texture().get_image()
		for host in view.props:
			if host.id!="xeno_workbench": continue
			# Nearly white source light evades the violet-only source detector.
			for source_point in [Vector2(970,931),Vector2(985,931)]:
				var screen:=Vector2i(Vector2(384,384)+view.life_point(host,source_point)*1.6)
				var lens_color:=image.get_pixelv(screen)
				if maxf(lens_color.r,maxf(lens_color.g,lens_color.b))>0.35:
					push_error("Xeno workbench status strip remains bright offline: q%d"%q)
					missed+=1
		var prop: Dictionary=view.props[0]
		# Hand-selected lamp interiors, independent of renderer aperture helpers.
		for point in [Vector2(231,212),Vector2(394,212),Vector2(312,437),Vector2(218,454),Vector2(407,455)]:
			var pixel:=Vector2i(Vector2(384,384)+view.life_point(prop,point)*1.6)
			var color:=image.get_pixelv(pixel)
			if color.b+0.005<color.g or color.r>color.g+0.005 or maxf(color.r,maxf(color.g,color.b))>0.3:
				push_error("Xeno unlit lamp is tinted or bright: q%d point%s color%s"%[q,point,color])
				missed+=1
		for index in [0,1,2,3,4,5]:
			var region: Rect2=view.display_regions(prop)[index].grow(-2)
			var start: Vector2=Vector2(384,384)+view.life_point(prop,region.position)*1.6
			var end: Vector2=Vector2(384,384)+view.life_point(prop,region.end)*1.6
			var detail:=image.get_region(Rect2i(start,end-start))
			var colors: Dictionary={}
			for y in range(detail.get_height()):
				for x in range(detail.get_width()): colors[detail.get_pixel(x,y).to_rgba32()]=true
			if colors.size()<3:
				push_error("Xeno offline surface flattened: q%d region%d"%[q,index])
				missed+=1
		view.configure_embedded(q,[],true,0.5)
		panel.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var active_image:=root.get_texture().get_image()
		for host in view.props:
			if host.id!="xeno_workbench": continue
			for source_point in [Vector2(970,931),Vector2(985,931)]:
				var screen:=Vector2i(Vector2(384,384)+view.life_point(host,source_point)*1.6)
				var lens_color:=active_image.get_pixelv(screen)
				if maxf(lens_color.r,maxf(lens_color.g,lens_color.b))<0.6:
					push_error("Xeno workbench status strip does not light while operating: q%d"%q)
					missed+=1
	if missed==0: print("XENO MATERIAL PASS: six offline surface interiors plus workbench lens off/on in four rotations; not exhaustive emissive acceptance")
	quit(1 if missed>0 else 0)
