extends SceneTree
const View=preload("res://rooms/underwater/batch-two/data_archive_view.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	var view:=View.new()
	view.embedded=true
	root.add_child(view)
	var source:=view.life_texture.get_image()
	var missed:=0
	var separate_texture_hosts:=0
	for prop in view.props:
		# Furnishings use their own texture and source coordinate system; this
		# audit's apertures belong only to the main room donor (same rule as
		# test_anomaly_registration.gd).
		if prop.registration.get("dressing",false):
			separate_texture_hosts+=1
			continue
		var regions:=view.display_regions(prop)
		var bounds:=Rect2(prop.registration.outline[0],Vector2.ZERO)
		for p in prop.registration.outline: bounds=bounds.expand(p)
		var examples: Array=[]
		var count:=0
		for y in range(int(bounds.position.y),int(bounds.end.y)):
			for x in range(int(bounds.position.x),int(bounds.end.x)):
				var c:=source.get_pixel(x,y)
				if minf(c.g,c.b)-c.r<0.10 or c.g<0.27: continue
				var point:=Vector2(x,y)
				if not Geometry2D.is_point_in_polygon(point,PackedVector2Array(prop.registration.outline)): continue
				var covered:=false
				for region in regions:
					if region.has_point(point): covered=true
				if not covered:
					count+=1
					if examples.size()<24: examples.append(point)
		missed+=count
		if count>0: print("UNCOVERED ",prop.id,": ",count," source cyan pixels; examples ",examples)
	if missed>0: push_error("Archive source indicator pixels outside replacement apertures: "+str(missed))
	else: print("ARCHIVE SOURCE APERTURES PASS: source cyan indicator coverage")
	quit(1 if missed>0 else 0)
