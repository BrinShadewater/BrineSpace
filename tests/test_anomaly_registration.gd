extends SceneTree
const View=preload("res://rooms/underwater/batch-two/anomaly_lab_view.gd")
class FlatLensView extends "res://rooms/underwater/batch-two/anomaly_lab_view.gd":
	func draw_registered_prop(prop: Dictionary) -> void:
		super.draw_registered_prop(prop)
		if prop.id!="anomaly_receiver": return
		for i in range(3):
			var points:=PackedVector2Array()
			for p in display_polygon(display_regions(prop)[i],0): points.append(life_point(prop,p))
			painter.draw_colored_polygon(points,Color("23252d"))
class MaterialPanel extends Node2D:
	var view
	var focus_platform:=false
	func _draw() -> void:
		if not focus_platform:
			view.render_into(self,Vector2(384,384),1.6)
			return
		var prop: Dictionary=view.props[0]
		draw_set_transform(Vector2(384,384)-view.prop_visual_bounds(prop).get_center()*4.0,0,Vector2(4,4))
		view.painter=self
		view.draw_registered_prop(prop)
		draw_set_transform(Vector2.ZERO)
class FlatPlatformView extends "res://rooms/underwater/batch-two/anomaly_lab_view.gd":
	func draw_registered_prop(prop: Dictionary) -> void:
		super.draw_registered_prop(prop)
		if prop.id!="anomaly_platform": return
		for index in platform_strip_indices():
			var points:=PackedVector2Array()
			for p in aperture_polygons(prop)[index]: points.append(life_point(prop,p))
			painter.draw_colored_polygon(points,Color("23252d"))
class FlatCapacitorView extends "res://rooms/underwater/batch-two/anomaly_lab_view.gd":
	func draw_registered_prop(prop: Dictionary) -> void:
		super.draw_registered_prop(prop)
		if prop.id!="anomaly_capacitors": return
		for i in range(3):
			var points:=PackedVector2Array()
			for p in aperture_polygons(prop)[i]: points.append(life_point(prop,p))
			painter.draw_colored_polygon(points,Color("23252d"))
func _init() -> void: call_deferred("run")
func run() -> void:
	var view: View
	if "--negative-flat-platform" in OS.get_cmdline_user_args(): view=FlatPlatformView.new()
	elif "--negative-flat-capacitor" in OS.get_cmdline_user_args(): view=FlatCapacitorView.new()
	elif "--negative-flat-lens" in OS.get_cmdline_user_args(): view=FlatLensView.new()
	else: view=View.new()
	view.embedded=true
	view.hide()
	root.add_child(view)
	var source:=view.life_texture.get_image()
	var missed:=0
	var source_hosts:=0
	var separate_texture_hosts:=0
	var platform_shapes:=view.aperture_polygons(view.props[0])
	for check in [[18,Vector2(174,453),false],[18,Vector2(184,447),true],[19,Vector2(482,439),false],[19,Vector2(491,449),true]]:
		if Geometry2D.is_point_in_polygon(check[1],platform_shapes[check[0]])!=check[2]:
			push_error("Anomaly slanted lamp mask must preserve face and cover aperture")
			missed+=1
	for prop in view.props:
		# Furnishings use their own texture and source coordinate system.
		# This audit's suppression apertures belong only to the main room donor.
		if prop.registration.get("dressing",false):
			separate_texture_hosts+=1
			continue
		source_hosts+=1
		var shapes:=view.aperture_polygons(prop)
		var bounds:=Rect2(prop.registration.outline[0],Vector2.ZERO)
		for p in prop.registration.outline: bounds=bounds.expand(p)
		var examples: Array=[]
		var count:=0
		for y in range(int(bounds.position.y),int(bounds.end.y)):
			for x in range(int(bounds.position.x),int(bounds.end.x)):
				var c:=source.get_pixel(x,y)
				if c.r-c.g<0.06 or c.b-c.g<0.10 or c.b<0.28: continue
				var point:=Vector2(x,y)
				if not Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)): continue
				var covered:=false
				for shape in shapes:
					if Geometry2D.is_point_in_polygon(point,shape): covered=true
				if not covered:
					count+=1
					if examples.size()<24: examples.append(point)
		missed+=count
		if count>0: print("UNCOVERED ",prop.id,": ",count," bright violet pixels; examples ",examples)
	if missed>0: push_error("Anomaly bright violet pixels outside replacement apertures: "+str(missed))
	else: print("ANOMALY SOURCE APERTURES PASS: ",source_hosts," main-donor hosts; ",separate_texture_hosts," separate-texture furnishings excluded, not emissively certified")
	root.size=Vector2i(768,768)
	root.content_scale_size=root.size
	var panel:=MaterialPanel.new()
	panel.view=view
	root.add_child(panel)
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		panel.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var capture:=root.get_texture().get_image()
		var platform: Dictionary=view.props[0]
		# Resolve narrow source-space bezels in a prop-only native diagnostic.
		# Whole-room 1.6x sampling can legitimately collapse them below one pixel.
		panel.focus_platform=true
		panel.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var platform_capture:=root.get_texture().get_image()
		var origin: Vector2=Vector2(384,384)-view.prop_visual_bounds(platform).get_center()*4.0
		for index in view.platform_strip_indices():
			var shape: PackedVector2Array=view.aperture_polygons(platform)[index]
			var pixels:=PackedVector2Array()
			var bounds:=Rect2(origin+view.life_point(platform,shape[0])*4.0,Vector2.ZERO)
			for p in shape:
				var point: Vector2=origin+view.life_point(platform,p)*4.0
				pixels.append(point)
				bounds=bounds.expand(point)
			var colors: Dictionary={}
			for y in range(int(ceil(bounds.position.y)),int(floor(bounds.end.y))):
				for x in range(int(ceil(bounds.position.x)),int(floor(bounds.end.x))):
					if Geometry2D.is_point_in_polygon(Vector2(x+0.5,y+0.5),pixels):
						colors[platform_capture.get_pixel(x,y).to_rgba32()]=true
			if colors.size()<2:
				push_error("Anomaly offline platform strip flattened: q%d strip%d"%[q,index])
				missed+=1
		panel.focus_platform=false
		var prop: Dictionary=view.props[3]
		for index in range(3):
			# Sample inside the optical circle, not its metal bezel or corners.
			var center: Vector2=view.display_regions(prop)[index].get_center()
			var colors: Dictionary={}
			for offset in [Vector2.ZERO,Vector2(0,-15),Vector2(0,-18)]:
				var pixel:=Vector2i(Vector2(384,384)+view.life_point(prop,center+offset)*1.6)
				colors[capture.get_pixelv(pixel).to_rgba32()]=true
			if colors.size()<2:
				push_error("Anomaly offline lens flattened: q%d lens%d"%[q,index])
				missed+=1
		var capacitor: Dictionary=view.props[2]
		for index in range(3):
			var region: Rect2=view.display_regions(capacitor)[index]
			var colors: Dictionary={}
			for offset in [1.0,3.0,6.0]:
				var point:=Vector2(region.position.x+offset,region.get_center().y)
				var pixel:=Vector2i(Vector2(384,384)+view.life_point(capacitor,point)*1.6)
				colors[capture.get_pixelv(pixel).to_rgba32()]=true
			if colors.size()<2:
				push_error("Anomaly offline capacitor glass flattened: q%d tube%d"%[q,index])
				missed+=1
	if missed==0: print("ANOMALY LENS MATERIAL PASS: three receiver faces and three capacitor apertures across four rotations; static material only")
	if missed==0: print("ANOMALY PLATFORM MATERIAL PASS: ten recessed strips across four rotations; static material only")
	quit(1 if missed>0 else 0)
