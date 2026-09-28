extends RefCounted
## Registered moving art; simulation timing and navigation remain in survey_probe.gd.
const Art=preload("res://scripts/survey_probe_art.gd")
const BASE="res://assets/probe-launcher-v2/base.png"
const CRADLE="res://assets/probe-launcher-v2/cradle.png"
const BASE_SOURCE=Rect2(140,129,529,1674)
const CRADLE_SOURCE=Rect2(152,192,1231,610)
const BASE_RECT=Rect2(-24,-178,40,68)
const TRAVEL=32.0

static func motion(time:float) -> Vector2:
	var t:=clampf(time,0,32)
	var travel:=0.0
	if t>=3.6 and t<6:travel=minf(TRAVEL,72*pow((t-3.6)/2.4,2))
	elif t>=6 and t<27:travel=TRAVEL
	elif t>=27 and t<30:travel=minf(TRAVEL,130*(1-smoothstep(27,30,t)))
	var release:=smoothstep(2,3.4,t)*(1-smoothstep(30,31.5,t))
	return Vector2(travel,release)

static func draw(canvas:CanvasItem,time:float,q:int,base:bool=true) -> void:
	if q!=0:return
	if base:
		# Shorten the straight rail run, retaining the connector and front crossmember
		# at their original pixel scale. Rear edge overlaps the riser foot by two units.
		var density:=BASE_SOURCE.size.x/BASE_RECT.size.x
		for band in [[0.0,24.0,BASE_SOURCE.position.y],[24.0,20.0,850.0],[44.0,24.0,BASE_SOURCE.end.y-24*density]]:
			canvas.draw_texture_rect_region(Art.texture(BASE),Rect2(BASE_RECT.position+Vector2(0,band[0]),Vector2(40,band[1])),Rect2(BASE_SOURCE.position.x,band[2],529,band[1]*density))
	var state:=motion(time)
	var size:=Vector2(36,17.84)
	var center:=Vector2(-4,-137-state.x)
	# Two hydraulic halves release laterally; the cradle follows the launch rails.
	for side in [0,1]:
		var source:=Rect2(CRADLE_SOURCE.position+Vector2(side*615.5,0),Vector2(615.5,610))
		var at:=center-size*.5+Vector2(side*18+(1 if side else -1)*state.y*3,0)
		canvas.draw_texture_rect_region(Art.texture(CRADLE),Rect2(at,Vector2(18,size.y)),source)

static func tunnel(canvas:CanvasItem,time:float,status:String) -> void:
	var pose:=probe_pose(time)
	pose.lamp=status
	# Registered inside the painted portal: sprite disappears behind its steel lip,
	# then becomes visible in the dark throat. Reverse clipping reveals its return.
	# Follow the round throat instead of two rectangular clip bands. Fade the
	# vehicle into its unlit depth before it reaches the upper clipping boundary.
	for row in range(42):
		var depth:=float(row)+0.5
		# Full fin span clears the mouth; narrowing happens only in the faded depth.
		var half_width:=20*sqrt(maxf(0,1-pow((12-depth)/12,2))) if depth<12 else 20.0
		var opacity:=smoothstep(0,12,depth)
		Art.body(canvas,pose,Vector2.ZERO,1.0,Rect2(-4-half_width,-218+row,half_width*2,1),false,opacity)

static func probe_pose(time:float) -> Dictionary:
	var pose:=Art.Mission.pose(time,0)
	# Align to the rail centre while docking; blend back to the ocean route behind
	# the opaque upper wall, preserving the simulation and exterior trajectory.
	var distance:float=pose.position.distance_to(Art.Mission.dock(0))
	pose.position.x-=4.0*(1-smoothstep(90,130,distance))
	return pose
