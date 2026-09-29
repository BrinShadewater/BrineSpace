extends RefCounted
## Approved v10 components, driven by the existing fleet phase clock.
const Motion=preload("res://scripts/drone_animation.gd")
const DATA="res://assets/drone-runtime-2026-09-26/docks.json"
static var records:Dictionary={}
static func required_paths(kind:String,drone:Dictionary,operating:bool) -> Array:
	var paths:Array=record(kind).components.values()
	if not pose(drone).present: return paths
	var d:=drone.duplicate()
	d.kind=kind; d.animation_heading="south"
	var state:=Motion.sample(d,operating)
	var meta:Dictionary=Motion.catalog(kind).headings.south
	if kind=="salvage" and state.loaded and state.state not in ["retrieve","release"]:
		paths.append(meta.cargoPose); paths.append(meta.closedPose)
	else: paths.append(state.clip.atlas.path)
	for layer in ["effectAtlas","cargoAtlas"]:
		if state.clip.has(layer): paths.append(state.clip[layer].path)
	if kind=="mining":
		paths.append(meta.wheelAtlas.path)
		if state.loaded and not state.clip.has("cargoAtlas"): paths.append(meta.cargoPose)
	if kind=="salvage": paths.append(meta.rotorAtlas.path)
	return paths

static func prepare_paths(paths:Array,parallel_decode:bool=false) -> bool:
	# Decode independent layers together; upload small pieces within a short
	# frame budget. Touch the full set before any upload can evict a sibling.
	for path in paths:
		if Motion.textures.has(path): Motion.last_used[path]=Engine.get_process_frames()
		elif parallel_decode: Motion.request_texture(path)
	if not parallel_decode:
		for path in paths:
			if Motion.textures.has(path): continue
			Motion.request_texture(path)
			Motion.finish_texture(path)
			return false
		return true
	var started:=Time.get_ticks_usec()
	var ready:=true
	for path in paths:
		if Motion.textures.has(path): continue
		if Time.get_ticks_usec()-started>=4000:
			ready=false
			continue
		if not Motion.finish_texture(path): ready=false
	return ready

# A background decode still running when the engine shuts down crashes it (access violation
# on quit). Owners of these jobs call this as they leave the tree.
static func finish_pending_jobs() -> void:
	for path in Motion.image_jobs.keys():
		var job: Dictionary=Motion.image_jobs[path]
		WorkerThreadPool.wait_for_task_completion(job.task)
		# A completed task ID is invalid after wait; consume its decoded image directly.
		Motion.image_jobs.erase(path)
		if job.result.has("image"): Motion.cache_image(path,job.result.image)
		else: push_error("Drone animation missing: "+path)
static func prepare_preview(kind:String,operating:bool=true) -> bool:
	return prepare_paths(required_paths(kind,{},operating))
static func record(kind:String) -> Dictionary:
	if records.is_empty(): records=JSON.parse_string(FileAccess.get_file_as_string(DATA))
	return records[kind]
static func bounds(rect:Rect2,values:Array) -> Rect2:
	return Rect2(rect.position+Vector2(values[0],values[1])*rect.size,Vector2(values[2]-values[0],values[3]-values[1])*rect.size)
static func legacy_rect(prop:Dictionary,kind:String) -> Rect2:
	var r:=record(kind)
	var width:float=r.world_width
	var size:=Vector2(width,width*r.sizes["water-pad"][1]/r.sizes["water-pad"][0])
	var at:=Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
	return Rect2(Vector2(at.x-width*.5,at.y+45-size.y),size)
static func center(rect:Rect2,kind:String) -> Vector2:
	var r:=record(kind)
	var height:float=rect.size.x*r.sizes["water-pad"][1]/r.sizes["water-pad"][0]
	rect=Rect2(Vector2(rect.position.x,rect.end.y-height),Vector2(rect.size.x,height))
	var well:=bounds(rect,record(kind).well)
	return Vector2(well.get_center().x,well.position.y+well.size.y*.4)
# Owner, Sept 27: docked drones read too small in their pad wells. The fleet draws at this
# same scale, so docked, launching and flying drones stay one size.
# Owner, Sept 27 (second pass): mining and construction +50%, salvage +30% on top of the first.
const SIZE_BOOST:={"construction":1.875,"mining":2.025,"salvage":1.69}
# Boosted drones can reach just past the pad frame; retained draw slots use this envelope.
static func visual_bounds(rect:Rect2) -> Rect2: return rect.grow(rect.size.x*.3)
static func art_scale(rect:Rect2,kind:String) -> float:
	var r:=record(kind)
	return float(SIZE_BOOST.get(kind,1.0))*float(r.hull_width)/float(Motion.catalog(kind).get("nominalSouthHullWidthWorld",Motion.catalog(kind).get("nominalWidthWorld",120.36)))*rect.size.x/float(r.world_width)
static func piece(canvas:CanvasItem,r:Dictionary,key:String,at:Vector2,scale_value:float,alpha:float=1.0) -> void:
	var size:=Vector2(r.sizes[key][0],r.sizes[key][1])*scale_value
	canvas.draw_texture_rect(Motion.texture(r.components[key]),Rect2(at-size*.5,size),false,Color(1,1,1,alpha))
static func pose(d:Dictionary) -> Dictionary:
	var phase:String=d.get("phase","docked")
	var t:=clampf(float(d.get("elapsed",0))/1.2,0,1)
	var opened:=0.0;var depth:=0.0;var cable:=1.0 if phase=="docked" else 0.0
	var present:=phase in ["docked","launching","docking"]
	if phase=="launching":
		opened=smoothstep(0,.2,t)*(1.0-smoothstep(.8,1,t))
		depth=smoothstep(.2,.7,t)
		cable=1.0-smoothstep(.7,1,t)
	elif phase=="docking":
		opened=smoothstep(0,.2,t)*(1.0-smoothstep(.8,1,t))
		depth=1.0-smoothstep(.25,.8,t)
		cable=smoothstep(0,.25,t)
	return {"cable":cable,"opened":opened,"depth":depth,"present":present,"warning":phase in ["launching","docking"] or (phase=="docked" and not d.get("job","").is_empty())}
static func draw(canvas:CanvasItem,rect:Rect2,kind:String,drone:Dictionary,operating:bool,clock:float) -> void:
	Motion.begin(canvas)
	var r:=record(kind)
	var scale_value:=rect.size.x/float(r.sizes["water-pad"][0])
	# Preserve native aspect ratio, anchored at the registered floor contact.
	rect=Rect2(Vector2(rect.position.x,rect.end.y-r.sizes["water-pad"][1]*scale_value),Vector2(rect.size.x,r.sizes["water-pad"][1]*scale_value))
	var p:=pose(drone)
	var well:=bounds(rect,r.well);var surface:=bounds(rect,r.surface)
	canvas.draw_texture_rect(Motion.texture(r.components["water-pad"]),rect,false)
	# Ripples remain inside the water well, behind machinery.
	for i in range(5):
		var y:float=well.position.y+well.size.y*(.15+i*.16)+sin(clock*.7+i)*scale_value*.6
		canvas.draw_line(Vector2(well.position.x+well.size.x*.12,y),Vector2(well.end.x-well.size.x*.12,y),Color(.26,.49,.49,.18),maxf(.25,scale_value*.7))
	var doors:=Motion.texture(r.components.doors)
	var visible_width:float=surface.size.x*.5*(1.0-float(p.opened))
	if visible_width>.001:
		var source_width:float=doors.get_width()*.5*(1.0-float(p.opened))
		canvas.draw_texture_rect_region(doors,Rect2(surface.position,Vector2(visible_width,surface.size.y)),Rect2(Vector2.ZERO,Vector2(source_width,doors.get_height())))
		canvas.draw_texture_rect_region(doors,Rect2(Vector2(surface.end.x-visible_width,surface.position.y),Vector2(visible_width,surface.size.y)),Rect2(Vector2(doors.get_width()-source_width,0),Vector2(source_width,doors.get_height())))
	var at:=center(rect,kind)+Vector2(0,float(p.depth)*well.size.y*.12)
	var dw:float=r.sizes.drone[0]*scale_value
	var dh:float=r.sizes.drone[1]*scale_value
	var alpha:float=(1.0-float(p.depth)) if p.present else 0.0
	var anchor_y:float=surface.position.y+26.0*rect.size.x/800.0
	var attach_y:float=at.y+dh*.38
	for sign_value in [-1,1]:
		var x:float=at.x+sign_value*dw*(.50 if kind=="construction" else .57)
		var end_y:float=lerpf(anchor_y,attach_y,float(p.cable))
		var segment:=Motion.texture(r.components["cable-segment"])
		var pitch:float=segment.get_height()*scale_value
		var y:=anchor_y
		while y<end_y:
			var height:=minf(pitch,end_y-y)
			canvas.draw_texture_rect_region(segment,Rect2(x-segment.get_width()*scale_value*.5,y,segment.get_width()*scale_value,height),Rect2(0,0,segment.get_width(),height/scale_value))
			y+=pitch
		if alpha>0:piece(canvas,r,"clevis",Vector2(x,attach_y),scale_value,alpha)
	if alpha>0:
		piece(canvas,r,"cradle",at,scale_value,alpha)
		var d:=drone.duplicate(true)
		d.kind=kind
		# Dock registration is authored south-facing; heading changes only outside.
		d.animation_heading="south"
		if not d.has("phase"):d.phase="docked"
		if d.phase=="docked" and operating:
			d.clock=clock;d.animation_rotor=clock*30.0
		Motion.draw(canvas,d,at,1.0,art_scale(rect,kind),operating,clock,alpha)
	if p.present and p.depth>0 and p.depth<1:
		piece(canvas,r,"contact-foam",Vector2(well.get_center().x,well.position.y+well.size.y*.55),scale_value,sin(float(p.depth)*PI)*.55)
	for sign_value in [-1,1]:
		piece(canvas,r,"winch",Vector2(at.x+sign_value*dw*(.50 if kind=="construction" else .57),anchor_y),scale_value)
	for beacon in r.beacons:
		var point:=rect.position+Vector2(beacon[0],beacon[1])*rect.size
		piece(canvas,r,"warning-beacon",point,scale_value)
		if p.warning and operating:
			var radius:=2.8*scale_value
			canvas.draw_arc(point-Vector2(0,3)*scale_value,radius,clock*TAU/.8,clock*TAU/.8+PI*.7,8,Color("e3b542"),maxf(.4,1.6*scale_value))
	var status_at:=rect.position+rect.size*Vector2(.50,.88)
	piece(canvas,r,"status-light",status_at,scale_value)
	var status:Color=Color("ffcd2d") if not operating or float(drone.get("battery",12))<11.999 else Color("309bff") if not drone.get("job","").is_empty() else Color("ff302e")
	status.a=.3+.7*pow(.5+.5*cos(clock*TAU/.85),3)
	canvas.draw_circle(status_at,1.5*scale_value,status)
