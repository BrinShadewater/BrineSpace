extends SceneTree
## Read-only registration audit. This does not establish visual acceptance.
func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var path := "res://rooms/production-ten/crew_lounge_view.gd"
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--view="): path=argument.trim_prefix("--view=")
	var view=load(path).new()
	root.add_child(view)
	var report := {"view":path,"rotations":[]}
	var mat_failures:=0
	for q in range(4):
		view.configure_embedded(q,[],false,0.0)
		var record := {"quarter":q,"props":[],"overlaps":[],"visual_overlaps":[],"mats":[]}
		if view.get("dressing")!=null:
			for mat in view.dressing.profile.get("mats",[]):
				var host: Dictionary=view.dressing.find_prop(mat.host)
				if host.is_empty():
					mat_failures+=1
					record.mats.append({"host":mat.host,"missing_host":true})
					continue
				# Match room_dressing.floor's host-relative, screen-facing rectangle.
				var pad:=Rect2(host.rect.position+Vector2(mat.offset[0],mat.offset[1]),Vector2(mat.size[0],mat.size[1]))
				var inside:=Rect2(-180,-180,360,360).encloses(pad)
				if not inside: mat_failures+=1
				record.mats.append({"host":mat.host,"floor":str(pad),"inside_interior":inside})
		for prop in view.props:
			var rect: Rect2=prop.rect
			var center:=rect.get_center()
			var samples:={"front":Vector2(center.x,rect.end.y+14),"rear":Vector2(center.x,rect.position.y-14),"left":Vector2(rect.position.x-14,center.y),"right":Vector2(rect.end.x+14,center.y)}
			var access:={}
			for side in samples: access[side]=view.can_stand(samples[side])
			record.props.append({"id":prop.id,"floor":str(rect),"visual":str(view.prop_visual_bounds(prop)),"visual_inside_interior":Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"standable_side_midpoints":access})
		for i in range(view.props.size()):
			for j in range(i+1,view.props.size()):
				if view.prop_visual_bounds(view.props[i]).intersects(view.prop_visual_bounds(view.props[j])):
					record.visual_overlaps.append([view.props[i].id,view.props[j].id])
					if "--polygon-overlaps" in OS.get_cmdline_user_args():
						if not record.has("polygon_overlaps"): record.polygon_overlaps=[]
						record.polygon_overlaps.append({"pair":[view.props[i].id,view.props[j].id],"intersection_area":intersection_area(view,view.props[i],view.props[j])})
				if view.props[i].rect.intersects(view.props[j].rect):
					record.overlaps.append([view.props[i].id,view.props[j].id])
		report.rotations.append(record)
	print(JSON.stringify(report,"\t"))
	if "--require-mats-contained" in OS.get_cmdline_user_args() and mat_failures>0:
		push_error("Room mat containment failures: "+str(mat_failures))
		quit(1)
	else: quit()

# Diagnostic only: registered cutout polygons, not decoded texture alpha,
# dynamic overlays, shadows, collision footprints or crew-access acceptance.
func polygons(view, prop: Dictionary) -> Array:
	var result: Array=[]
	for piece in prop.registration.get("pieces",[prop.registration.outline]):
		var points:=PackedVector2Array()
		for point in piece: points.append(view.life_point(prop,point))
		result.append(points)
	return result

func intersection_area(view, first: Dictionary, second: Dictionary) -> float:
	var total:=0.0
	for a in polygons(view,first):
		for b in polygons(view,second):
			for overlap in Geometry2D.intersect_polygons(a,b):
				var twice_area:=0.0
				for i in range(overlap.size()): twice_area+=overlap[i].cross(overlap[(i+1)%overlap.size()])
				total+=absf(twice_area)*0.5
	return total
