extends RefCounted
## Per-bay mission clock lives in the placed-room snapshot. No separate save file.
const Field = preload("res://scripts/wreck_field.gd")
const HEADINGS := ["east","southeast","south","southwest","west","northwest","north","northeast"]
const DIRECTIONS := [Vector2.UP,Vector2.RIGHT,Vector2.DOWN,Vector2.LEFT]
# Launcher anchors, set so each rotation's launcher art sits flush on its wall (owner, Sept 27).
# Owner, Sept 27 (second pass): the launcher passes through the hull and ends just outside it.
const DOCKS := [Vector2(0,-143),Vector2(129,0),Vector2(0,153),Vector2(-131,0)]
static func dock(q:int) -> Vector2:return DOCKS[posmod(q,4)]
static func smooth_fraction(t:float) -> float:return t*t*(3-2*t)
static func pose(time:float,q:int) -> Dictionary:
	var t:=clampf(time,0,32)
	var p:=Vector2.ZERO
	var yaw:=0.0
	var state:="recharge"
	if t>=2 and t<3.6:state="idle"
	elif t>=3.6 and t<6:
		state="launch";p.x=72*pow((t-3.6)/2.4,2)
	elif t>=6 and t<10:
		state="cruise";p.x=lerpf(72,312,(t-6)/4)
	elif t>=10 and t<12:
		state="brake";var f:=(t-10)/2;p.x=312+60*(2*f-f*f)
	elif t>=12 and t<16:state="scan";p.x=372
	elif t>=16 and t<20:
		state="turn";yaw=PI*smooth_fraction((t-16)/4);p=Vector2(372+60*sin(yaw),60-60*cos(yaw))
	elif t>=20 and t<24:
		state="return";var f:=smooth_fraction((t-20)/4);p=Vector2(lerpf(372,130,f),lerpf(120,90,smooth_fraction(f)));yaw=atan2(-180*f*(1-f),-242)
	elif t>=24 and t<27:
		state="align";var a:=PI*smooth_fraction((t-24)/3);p=Vector2(130-45*sin(a),45+45*cos(a));yaw=PI+a
	elif t>=27 and t<30:state="dock";p.x=130*(1-smooth_fraction((t-27)/3))
	var angle:float=DIRECTIONS[posmod(q,4)].angle()
	return {"position":dock(q)+p.rotated(angle),"heading":HEADINGS[posmod(roundi((angle+yaw)/(PI/4)),8)],"state":state,"beacon":t>=2 and t<3.6,"time":t,"scan":clampf((t-12)/4,0,1)}

static func clear_position(game,room:Dictionary,point:Vector2) -> bool:
	# Actual body clearance, not its transparent 512px frame.
	for offset in [Vector2.ZERO,Vector2(30,0),Vector2(-30,0),Vector2(0,30),Vector2(0,-30)]:
		var cell:=Vector2i((Vector2(room.pos)+Vector2.ONE*.5+(point+offset)/384).floor())
		if cell==room.pos:continue
		if cell.x<0 or cell.y<0 or cell.x>=40 or cell.y>=40:return false
		if game.occupied.has(cell) or Field.blocks(game.wrecks,cell) or game.drone_fleet.reserved(cell):return false
	return true

static func clear_route(game,room:Dictionary) -> bool:
	for i in range(107):
		if not clear_position(game,room,pose(i*.3,int(room.get("rotation",0))).position):return false
	return true

static func advance(game,delta:float) -> void:
	if not game.running or game.paused or not game.hardware.power:return
	for room in game.placed_rooms:
		if room.id!="survey_probe_bay":continue
		if room.get("suspended",false) or not game.powered_room_cells.has(room.pos):continue
		var t:float=room.get("survey_clock",0.0)
		var next:=minf(32,t+delta)
		# Preflight all of the loop before the warning beacon starts. Later building
		# changes hold the probe at its last safe point instead of teleporting it home.
		if t<2 and next>=2 and not clear_route(game,room):room.survey_blocked=true;continue
		var safe:=true
		for i in range(1,maxi(1,ceili((next-t)*10))+1):
			var sample:=lerpf(t,next,float(i)/maxi(1,ceili((next-t)*10)))
			if not clear_position(game,room,pose(sample,int(room.get("rotation",0))).position):safe=false;break
		if not safe:room.survey_blocked=true;continue
		room.survey_blocked=false
		room.survey_clock=0.0 if next>=32 else next

static func lights(game) -> Array:
	var lights:Array=[]
	for room in game.placed_rooms:
		if room.id!="survey_probe_bay" or room.get("suspended",false) or not game.hardware.power or not game.powered_room_cells.has(room.pos):continue
		var p:=pose(float(room.get("survey_clock",0)),int(room.get("rotation",0)))
		if p.state in ["idle","recharge"]:continue
		lights.append({"position":Vector2(room.pos)+Vector2.ONE*.5+p.position/384,"direction":DIRECTIONS[posmod(int(room.get("rotation",0)),4)],"radius":2.8 if p.state=="scan" else .65,"strength":1.0,"kind":"survey_probe"})
	return lights

static func valid_rooms(rooms:Array) -> bool:
	for room in rooms:
		if room.has("survey_clock") and (not (room.survey_clock is float or room.survey_clock is int) or not is_finite(float(room.survey_clock)) or room.survey_clock<0 or room.survey_clock>=32):return false
		if room.has("survey_blocked") and not room.survey_blocked is bool:return false
	return true

static func status(room:Dictionary) -> String:
	if room.get("survey_blocked",false):return "PROBE HELD // Exterior route obstructed."
	return "PROBE // "+str(pose(float(room.get("survey_clock",0)),int(room.get("rotation",0))).state).to_upper()


static func lamp(game,room:Dictionary) -> String:
	if not game.hardware.power or not game.powered_room_cells.has(room.pos):return "yellow"
	if game.paused or room.get("suspended",false) or room.get("survey_blocked",false):return "red"
	return "yellow" if pose(float(room.get("survey_clock",0)),int(room.get("rotation",0))).state=="recharge" else "blue"
