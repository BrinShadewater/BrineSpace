extends RefCounted
const Mission = preload("res://scripts/survey_probe.gd")
static var textures := {}
static func texture(path:String) -> Texture2D:
	if not textures.has(path):
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))!=OK:return null
		textures[path]=ImageTexture.create_from_image(image)
	return textures[path]
static func launcher(q:int) -> Dictionary:
	if posmod(q,4)==2:
		var south:=texture("res://assets/probe-outlet-stub-v3/south-launcher-round-collar.png")
		return {"id":"survey_hatch","rect":Rect2(-21.2,96,64,95.25292),"sort_y":183,"registration":{},"collision_boxes":[[.1,.25,.8,.7]],"texture":south}
	var direction:String=["north","east","south","west"][posmod(q,4)]
	var data:Dictionary=LAUNCHERS[direction]
	var tex:=texture(data.image)
	var scale_value:=.34*float(data.libraryScale)
	return {"id":"survey_hatch","rect":Rect2(Mission.dock(q)-Vector2(data.anchor[0],data.anchor[1])*scale_value,Vector2(tex.get_size())*scale_value),"sort_y":Mission.dock(q).y+30,"registration":{},"collision_boxes":[[.1,.25,.8,.7]],"texture":tex}
static func draw_clipped(canvas,tex:Texture2D,dest:Rect2,source:Rect2,clip:Rect2,tint:=Color.WHITE) -> void:
	var r:=dest.intersection(clip)
	if not r.has_area():return
	var uv:=Rect2(source.position+(r.position-dest.position)/dest.size*source.size,r.size/dest.size*source.size)
	canvas.draw_texture_rect_region(tex,r,uv,tint)
static func body(canvas,p:Dictionary,origin:Vector2,scale_value:float,clip:Rect2,wake_enabled:=true,opacity:=1.0) -> void:
	var center:Vector2=origin+p.position*scale_value
	var rect:=Rect2(center-Vector2.ONE*87.04*scale_value,Vector2.ONE*174.08*scale_value)
	if wake_enabled and p.state in ["launch","cruise","return","brake","turn","align"]:
		var frame:=posmod(int(p.time*30),60)
		var wake:=texture(PATHS["wake-"+p.heading])
		draw_clipped(canvas,wake,rect,Rect2((frame%6)*512,(frame/6)*512,512,512),clip)
	var tex:=texture(PATHS[p.heading])
	draw_clipped(canvas,tex,rect,Rect2(Vector2.ZERO,tex.get_size()),clip,Color(1,1,1,opacity))
	var angle:=float(Mission.HEADINGS.find(p.heading))*PI/4
	var lamp:=center+Vector2.from_angle(angle)*3.06*scale_value
	if clip.has_point(lamp):
		var color:Color={"yellow":Color("e6bd60"),"red":Color("c36155"),"blue":Color("6ab8df")}[p.get("lamp","yellow" if p.state=="recharge" else "blue")]
		color.a=(.4+.6*(.5+.5*cos(float(p.time)*TAU)))*opacity
		canvas.draw_circle(lamp,.782*scale_value,color)
static func collar_inset(q:int) -> float:
	# Side collars sit within the cap, rather than fully in front of it.
	return 18.0 if posmod(q,4) in [1,3] else 36.0
static func interior(room,prop:Dictionary) -> void:
	var special:bool=room.quarter==0 and room.get_meta("raised_north_visible",false) and preload("res://scripts/room_layout_store.gd").surface_positions(room).get("wall/riser","")==""
	if special:
		load("res://scripts/probe_launcher_mechanics.gd").draw(room.painter,float(room.survey_clock),0)
	else:
		if room.quarter!=0:
			# Inner sleeve reaches under the cap; draw before the inset collar.
			var sleeve:=PackedVector2Array()
			for point in [Vector2(-18,-184),Vector2(18,-184),Vector2(18,-144),Vector2(-18,-144)]:
				sleeve.append(point.rotated(room.quarter*PI*.5))
			room.painter.draw_colored_polygon(sleeve,Color("30383b"))
		# Sink the older directional collar into the room; the pressure wall
		# occludes its outer end rather than letting it paint over the wall.
		var inset:Vector2=-Mission.DIRECTIONS[posmod(int(room.quarter),4)]*collar_inset(room.quarter) if room.quarter in [1,3] else Vector2.ZERO
		if room.quarter==2:
			# From above the vertical south collar exposes its top edge only.
			# Keep the rails and right-side fittings, not the front-facing opening.
			var source:=Rect2(Vector2.ZERO,prop.texture.get_size())
			room.painter.draw_texture_rect_region(prop.texture,Rect2(prop.rect.position.x,96,prop.rect.size.x,81),Rect2(0,0,1028,980))
			draw_clipped(room.painter,prop.texture,prop.rect,source,Rect2(18,159,166,25))
			# Reuse the rounded outer sleeve crown as a shallow inner collar.
			# Its bowed top and side shoulders remain visible above the wall cap.
			room.painter.draw_texture_rect_region(texture("res://assets/probe-outlet-stub-v3/outlet-matte-v2.png"),Rect2(-23,172,46,12),Rect2(315,282,615,270))
		else:
			draw_clipped(room.painter,prop.texture,Rect2(prop.rect.position+inset,prop.rect.size),Rect2(Vector2.ZERO,prop.texture.get_size()),Rect2(-184,-184,368,368))
	var p:=Mission.pose(float(room.survey_clock),int(room.quarter))
	if special:
		var mechanics=load("res://scripts/probe_launcher_mechanics.gd")
		p=mechanics.probe_pose(float(room.survey_clock))
		# The props pass repaints the platform after the raised wall. Repaint its
		# tunnel portion too, so the rear cross-edge cannot stripe the vehicle.
		mechanics.tunnel(room.painter,float(room.survey_clock),str(room.survey_status))
	if not special and room.quarter!=0:
		var distance:float=p.position.distance_to(Mission.dock(room.quarter))
		p.position-=Mission.DIRECTIONS[posmod(int(room.quarter),4)]*collar_inset(room.quarter)*(1-smoothstep(90,130,distance))
	p.lamp=room.survey_status
	var floor_top:float=-176 if room.quarter==0 and room.get_meta("raised_north_visible",false) else -174
	body(room.painter,p,Vector2.ZERO,1.0,Rect2(-174,floor_top,348,174-floor_top))
	if p.beacon and room.operating and room.survey_status=="blue":
		var offsets:=[Vector2(35,-54),Vector2(79,15),Vector2(36,32),Vector2(-69,13)]
		var at:Vector2=Mission.dock(room.quarter)+offsets[posmod(room.quarter,4)]
		var angle:=float(p.time)/.8*TAU
		room.painter.draw_circle(at,4,Color("594c2d"))
		room.painter.draw_arc(at,3,angle,angle+1.5,12,Color("d7af58"),1.5)
static func exterior(canvas,game,cell_size:float) -> void:
	for room in game.placed_rooms:
		if room.id!="survey_probe_bay":continue
		var p:=Mission.pose(float(room.get("survey_clock",0)),int(room.get("rotation",0)))
		p.lamp=Mission.lamp(game,room)
		var origin:Vector2=(Vector2(room.pos)+Vector2.ONE*.5)*cell_size
		var s:=cell_size/384
		var q:int=posmod(int(room.get("rotation",0)),4)
		# Leave the pressure wall opaque. The room renderer owns the interior half.
		var hull:=Rect2(origin-Vector2.ONE*cell_size*.5,Vector2.ONE*cell_size)
		for clip in [Rect2(-1e5,-1e5,2e5,hull.position.y+1e5),Rect2(-1e5,hull.end.y,2e5,1e5),Rect2(-1e5,hull.position.y,hull.position.x+1e5,cell_size),Rect2(hull.end.x,hull.position.y,1e5,cell_size)]:
			body(canvas,p,origin,s,clip)
		if p.state=="scan":
			var tex:=texture(PATHS["scan-"+p.heading])
			var frame:=mini(59,int(float(p.scan)*59))
			var center:Vector2=origin+p.position*s
			canvas.draw_texture_rect_region(tex,Rect2(center-Vector2.ONE*148.48*s,Vector2.ONE*296.96*s),Rect2((frame%6)*512,(frame/6)*512,512,512))
		# The overhead sleeve covers the vehicle while it travels through the tube.
		if not game.occupied.has(room.pos+Vector2i(Mission.DIRECTIONS[q])):
			var raised:bool=q==0 and game.hardware.walls and preload("res://scripts/title_settings.gd").raised_walls
			outlet(canvas,origin,s,q,raised)
static func outlet(canvas:CanvasItem,origin:Vector2,scale_value:float,q:int,raised:bool) -> void:
	var tex:=texture("res://assets/probe-outlet-stub-v3/outlet-matte-v2.png")
	# The final twelve units of the sleeve are buried inside the hull.
	var region:=Rect2(315,282,615,543.25)
	var edge:float=-271 if q==0 and raised else -184
	var center_x:float=-4.0 if q==0 and raised else 0.0
	var rect:=Rect2(center_x-24,edge-42.4,48,42.4)
	# Exterior is drawn after the hull, so crop the buried joint explicitly.
	# The cap owns the inner sixteen units and remains in front of the sleeve.
	if not (q==0 and raised):
		var cap_edge:float=-196.0 if q==2 else -200.0
		var visible_height:float=cap_edge-rect.position.y
		region.size.y*=visible_height/rect.size.y
		rect.size.y=visible_height
	# Solid steel backing stops the generated material's fractional alpha
	# from revealing water/probes through the centre of the metal sleeve.
	var backing:=PackedVector2Array()
	for point in [rect.position+Vector2(3,1),rect.position+Vector2(rect.size.x-3,1),rect.position+Vector2(rect.size.x-1,3),rect.end-Vector2(1,0),Vector2(rect.position.x+1,rect.end.y),rect.position+Vector2(1,3)]:
		backing.append(origin+point.rotated(q*PI*.5)*scale_value)
	canvas.draw_colored_polygon(backing,Color("30383b"))
	var points:=PackedVector2Array()
	for point in [rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)]:
		points.append(origin+point.rotated(q*PI*.5)*scale_value)
	var uv:=PackedVector2Array()
	for point in [region.position,Vector2(region.end.x,region.position.y),region.end,Vector2(region.position.x,region.end.y)]:uv.append(point/Vector2(tex.get_size()))
	canvas.draw_polygon(points,PackedColorArray([Color.WHITE]),uv,tex)

const PATHS := {
  "east": "res://assets/survey-probe-v1-2026-09-26/poses/east.png",
  "southeast": "res://assets/survey-probe-v1-2026-09-26/poses/southeast.png",
  "south": "res://assets/survey-probe-v1-2026-09-26/poses/south.png",
  "southwest": "res://assets/survey-probe-v1-2026-09-26/poses/southwest.png",
  "west": "res://assets/survey-probe-v1-2026-09-26/poses/west.png",
  "northwest": "res://assets/survey-probe-v1-2026-09-26/poses/northwest.png",
  "north": "res://assets/survey-probe-v1-2026-09-26/poses/north.png",
  "northeast": "res://assets/survey-probe-v1-2026-09-26/poses/northeast.png",
  "wake-east": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-east.png",
  "scan-east": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-east.png",
  "wake-southeast": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-southeast.png",
  "scan-southeast": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-southeast.png",
  "wake-south": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-south.png",
  "scan-south": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-south.png",
  "wake-southwest": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-southwest.png",
  "scan-southwest": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-southwest.png",
  "wake-west": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-west.png",
  "scan-west": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-west.png",
  "wake-northwest": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-northwest.png",
  "scan-northwest": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-northwest.png",
  "wake-north": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-north.png",
  "scan-north": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-north.png",
  "wake-northeast": "res://assets/survey-probe-v1-2026-09-26/atlases/wake-northeast.png",
  "scan-northeast": "res://assets/survey-probe-v1-2026-09-26/atlases/scan-northeast.png"
}
const LAUNCHERS := {
  "north": {
    "image": "res://assets/survey-probe-v1-2026-09-26/sources/north-launcher.png",
    "anchor": [
      64,
      212
    ],
    "libraryScale": 0.945
  },
  "east": {
    "image": "res://assets/survey-probe-v1-2026-09-26/sources/east-launcher.png",
    "anchor": [
      183,
      90
    ],
    "libraryScale": 0.945
  },
  "south": {
    "image": "res://assets/survey-probe-v1-2026-09-26/sources/south-launcher.png",
    "anchor": [
      70,
      117
    ],
    "libraryScale": 0.945
  },
  "west": {
    "image": "res://assets/survey-probe-v1-2026-09-26/sources/west-launcher.png",
    "anchor": [
      277,
      88
    ],
    "libraryScale": 0.945
  }
}
