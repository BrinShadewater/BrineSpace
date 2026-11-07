extends "res://rooms/whole-room/nursery_furnished_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("mycelium-cultivation-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	full_wall.apply(self)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	if prop.id in ["bench","filter"] and prop.has("layout_original_size"):
		var result:=Rect2(scaled_source_point(prop,prop.registration.outline[0]),Vector2.ZERO)
		for point in prop.registration.outline: result=result.expand(scaled_source_point(prop,point))
		return result
	return super.prop_visual_bounds(prop)

func scaled_source_point(prop: Dictionary, point: Vector2) -> Vector2:
	var original: Vector2=prop.get("layout_original_size",prop.rect.size)
	var old_foot: Vector2=prop.rect.position+Vector2(original.x*0.5,original.y)
	var foot: Vector2=Vector2(prop.rect.get_center().x,prop.rect.end.y)
	return foot+(pixel_to_world(point)+prop.art_offset-old_foot)*prop.rect.size.x/original.x

func draw_registered_prop(prop: Dictionary) -> void:
	draw_prop_base(prop)
	draw_prop_animation(prop)

func draw_prop_base(prop: Dictionary) -> void:
	if prop.id in ["bench","filter"] and prop.has("layout_original_size"):
		var vertices:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for point in prop.registration.outline:
			vertices.append(scaled_source_point(prop,point))
			uv.append(point/Vector2(texture.get_size()))
		draw_cached_polygon(vertices,uv,texture)
		return
	if full_wall.owns(prop):
		full_wall.draw(self,prop)
		return
	var was_operating:=operating
	operating=false
	super.draw_registered_prop(prop)
	operating=was_operating

func is_animated_prop(prop: Dictionary) -> bool:
	return prop.id in ["bench","filter","rack","reservoir"] or (full_wall.owns(prop) and posmod(quarter,4)==0)

func draw_prop_animation(prop: Dictionary) -> void:
	if not operating: return
	if prop.id=="rack":
		draw_rack_irrigation(prop.art_offset)
		return
	if prop.id=="reservoir":
		draw_reservoir_effect(prop.art_offset)
		return
	var bounds:=prop_visual_bounds(prop)
	if prop.id=="bench":
		# Scan stays inside the surviving bench's small monitor in every layout.
		var scan:=0.27+fposmod(machine_clock*0.055,0.13)
		var at:=bounds.position+bounds.size*Vector2(0.51,scan)
		painter.draw_line(at,at+Vector2(bounds.size.x*0.12,0),Color(0.46,0.78,0.66,0.65),1.0)
	elif prop.id=="filter":
		for i in range(3):
			var at:=bounds.position+bounds.size*Vector2(0.30+i*0.225,0.31)
			painter.draw_circle(at,0.65,Color(0.43,0.76,0.70,0.35+0.25*(1.0+sin(machine_clock*3.0+i))))
	elif full_wall.owns(prop) and posmod(quarter,4)==0:
		# Source-space nozzle gaps belong to the selected north idle artwork.
		var outlets=[Vector2(485,604),Vector2(1018,728)]
		for i in range(outlets.size()):
			var phase:=fposmod(machine_clock*0.65+i*0.37,1.0)
			if phase>0.70: continue
			var source: Vector2=outlets[i]+Vector2(0,phase*30.0)
			var uv: Vector2=(source-Vector2(36,204))/Vector2(1466,592)
			var at: Vector2=bounds.position+bounds.size*uv
			painter.draw_line(at,at+Vector2(0,1.1),Color(0.45,0.72,0.76,0.65),0.7)

