extends RefCounted
## Resolves each authored service brief against the current rotated machinery.
const Art=preload("res://rooms/floor-profiles-v1/modern_details.gd")
static var bounds_cache: Dictionary={}
static var enabled:=true # Native visibility fixture toggles this in its isolated process.
static var placement_cache: Dictionary={}
static func ink_bounds(asset: String, q: int, scale_value: float) -> Rect2:
	if not bounds_cache.has(asset):
		var r: Rect2=Art.bounds(asset)
		bounds_cache[asset]=r
	var r: Rect2=bounds_cache[asset]
	var result:=Rect2(r.position.rotated(q*PI/2)*scale_value,Vector2.ZERO)
	for v in [r.position,Vector2(r.end.x,r.position.y),r.end,Vector2(r.position.x,r.end.y)]: result=result.expand(v.rotated(q*PI/2)*scale_value)
	return result
static func protected_routes(view: Node) -> Array:
	var routes: Array=[]
	for edge in view.edges:
		if not edge.get("port",false): continue
		var at: Vector2=edge.center
		if at.length()>205: continue
		var half:=Vector2(20,20)
		var a:=Vector2.ZERO
		var b:=at-at.normalized()*12
		routes.append(Rect2(a.min(b)-half,(a-b).abs()+half*2))
	return routes
static func floor_pads(_view: Node) -> Array:
	# Automatic mats are disabled; do not reserve invisible pad footprints.
	return []
static func resolve(view: Node, profile: Dictionary) -> Dictionary:
	if profile.is_empty(): return {"pieces":[],"missing":[]}
	var geometry: Array=[]
	for prop in view.props: geometry.append([str(prop.id),prop.rect,view.prop_visual_bounds(prop)])
	geometry.append(floor_pads(view))
	for edge in view.edges: geometry.append([edge.center,edge.get("port",false)])
	var signature:=hash([geometry,profile.get("details",[]),preload("res://scripts/room_layout_store.gd").surface_positions(view)])
	var key: String=str(profile.id)+":"+str(view.quarter)
	if placement_cache.has(key) and placement_cache[key].signature==signature: return placement_cache[key].result
	var result:=_resolve_uncached(view,profile)
	placement_cache[key]={"signature":signature,"result":result}
	return result
static func _resolve_uncached(view: Node, profile: Dictionary) -> Dictionary:
	var result: Array=[]
	var missing: Array=[]
	var routes:=protected_routes(view)
	var pads:=floor_pads(view)
	var floor_rect:=Rect2(-174,-174,348,348)
	for source_spec in profile.get("details",[]):
		var spec: Dictionary=source_spec.duplicate(false)
		var override: Dictionary=spec.get("rotations",{}).get(str(view.quarter),{})
		for key in override: spec[key]=override[key]
		var host: Dictionary={}
		for candidate_id in spec.hosts:
			for prop in view.props:
				if str(prop.id)==candidate_id:
					host=prop
					break
			if not host.is_empty(): break
		if host.is_empty():
			missing.append({"asset":spec.asset,"reason":"missing host","hosts":spec.hosts})
			continue
		# Keep manually placed mats, but omit automatic workstation mats.
		if spec.asset=="detail-standing_mat" and not preload("res://scripts/room_layout_store.gd").surface_positions(view).has("decor/"+str(spec.asset)+"/"+str(host.id)):
			continue
		var placed:=false
		var host_rect: Rect2=host.rect.merge(view.prop_visual_bounds(host))
		for direction in [Vector2.DOWN,Vector2.RIGHT,Vector2.LEFT,Vector2.UP]:
			var utility: bool=spec.asset.begins_with("cable-") or spec.asset.begins_with("drain-")
			var q:=posmod(roundi((direction.angle()-PI)/(PI/2)),4) if spec.asset.ends_with("equipment_entry") else (1 if utility and direction.x!=0 else 0)
			var local_bounds:=ink_bounds(spec.asset,q,float(spec.scale))
			var half:=local_bounds.size/2
			var tangent:=Vector2(-direction.y,direction.x)
			var host_half:=host_rect.size/2
			var reach: float=absf(direction.x)*host_half.x+absf(direction.y)*host_half.y
			var span: float=absf(tangent.x)*host_half.x+absf(tangent.y)*host_half.y
			var outward: float=absf(direction.x)*half.x+absf(direction.y)*half.y
			for slide in [0.0,-0.15,0.15,-0.25,0.25,-0.4,0.4,-0.55,0.55,-0.7,0.7,-0.85,0.85,-0.95,0.95]:
				var contact: Vector2=host_rect.get_center()+direction*reach+tangent*span*slide
				var middle: Vector2=contact+direction*(outward+float(spec.get("stand_off",4)))
				var rect:=Rect2(middle-half,local_bounds.size)
				if not floor_rect.encloses(rect): continue
				var blocked:=false
				for route in routes:
					if rect.intersects(route): blocked=true
				for prop in view.props:
					if rect.grow(2).intersects(prop.rect) or rect.intersects(view.prop_visual_bounds(prop)): blocked=true
				for pad in pads:
					if rect.intersects(pad.rect): blocked=true
				for other in result:
					if rect.grow(3).intersects(other.rect): blocked=true
				if blocked: continue
				result.append({"asset":spec.asset,"host":str(host.id),"purpose":spec.purpose,"at":middle-local_bounds.get_center(),"rect":rect,"q":q,"scale":float(spec.scale),"contact":contact,"utility":utility})
				placed=true
				break
			if placed: break
		if not placed: missing.append({"asset":spec.asset,"reason":"no clear host-adjacent floor","hosts":spec.hosts})
	var edits: Dictionary=preload("res://scripts/room_layout_store.gd").surface_positions(view)
	for piece in result:
		piece.id="decor/"+str(piece.asset)+"/"+str(piece.host)
		var value=edits.get(piece.id)
		if value is Array and value.size()==2:
			var at:=Vector2(value[0],value[1])
			piece.rect.position+=at-piece.at
			piece.at=at
	result=preload("res://scripts/room_layout_store.gd").surface_copies(result,edits)
	result=result.filter(func(piece): return not (edits.has(piece.id) and edits[piece.id]==null))
	result.sort_custom(func(a,b): return float(edits.get("order/"+str(a.id),0))<float(edits.get("order/"+str(b.id),0)))
	return {"pieces":result,"missing":missing}
static func draw(view: Node, c: CanvasItem, profile: Dictionary) -> void:
	if not enabled or not view.has_meta("layout_editor_preview"): return
	var resolved:=resolve(view,profile)
	for piece in resolved.pieces:
		if preload("res://scripts/room_layout_store.gd").surface_positions(view).get("hidden/"+piece.id,false): continue
		if piece.utility:
			c.draw_line(piece.contact,piece.at,Color(.12,.18,.17,.6),4)
			c.draw_line(piece.contact,piece.at,Color(.42,.49,.45,.35),1)
		Art.stamp(c,piece.asset,piece.at,piece.q,.65,piece.scale,preload("res://scripts/room_layout_store.gd").flip_axes(view,piece.id),piece.rect.get_center())
