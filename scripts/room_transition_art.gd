extends RefCounted
## Cosmetic events only, bounded per grid and never serialized into room/run data.
const Settings=preload("res://scripts/title_settings.gd")
const Art=preload("res://scripts/environment_art.gd")
const Materials=preload("res://scripts/construction_materials.gd")
const Assembly=preload("res://scripts/room_construction_art.gd")
const Footprint=preload("res://scripts/room_footprint.gd")
var events: Array[Dictionary]=[]
func add(kind: String, room: Dictionary, clock: float) -> void:
	if kind not in ["complete","scrap"] or Settings.reduced_motion or Settings.effects_quality==0: return
	events=events.filter(func(event): return clock>=event.started and clock-event.started<event.duration and event.room.pos!=room.pos)
	if events.size()>=16: events.pop_front()
	events.append({"kind":kind,"room":room.duplicate(true),"started":clock,"duration":3.2 if kind=="complete" else 5.5})
func draw(grid,game,kind:="") -> void:
	var clock: float=game.get_visual_time_seconds()
	events=events.filter(func(event):
		if clock<event.started or clock-event.started>=event.duration: return false
		var room: Dictionary=event.room
		if event.kind=="scrap":
			return not Footprint.cells(room.pos,room.get("size",Vector2i.ONE)).any(func(cell): return game.occupied.has(cell) or game.drone_fleet.reserved(cell))
		return game.occupied.has(room.pos) and game.occupied[room.pos].id==room.id)
	if Settings.reduced_motion or Settings.effects_quality==0:
		events.clear();return
	for event in events:
		if not kind.is_empty() and event.kind!=kind: continue
		var room: Dictionary=event.room
		if event.kind=="scrap":
			Assembly.draw(grid,room,1.0-(clock-event.started)/event.duration,false)
		seal(grid.draw_target,room,grid._cell_size(),clock-event.started,event.kind=="scrap")
static func seal(canvas: CanvasItem,room: Dictionary,size: float,elapsed: float,dismantle:=false) -> void:
	var scale_value:=size/384.0
	var center: Vector2=(Vector2(room.pos)+Vector2(room.get("size",Vector2i.ONE))*.5)*size
	var mask:=Materials.hull(room)
	var fade:=1.0-smoothstep(.5,3.2,elapsed)
	if fade<=0: return
	# Small water displacements follow hull joints; sediment settles below the frame.
	for i in range(mask.size()):
		var edge: Vector2=mask[(i+1)%mask.size()]-mask[i]
		var joint: Vector2=(mask[i]+edge*.32)*scale_value+center
		var age:=clampf((elapsed-float(i)*.055)/3.2,0,1)
		if age<=0: continue
		Art.sprite(canvas,"intake-bubble",joint+Vector2(sin(i*2.3)*age*7,-age*18)*scale_value,Vector2(11,16)*scale_value,Color(.75,.84,.81,fade*.35))
		if i%2==0:
			Art.sprite(canvas,"sediment-puff",joint+Vector2(age*9,age*10)*scale_value,Vector2(32,16)*(1.0+age*.6)*scale_value,Color(.54,.58,.51,fade*(.32 if dismantle else .2)))
