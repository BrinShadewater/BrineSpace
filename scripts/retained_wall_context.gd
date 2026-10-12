extends RefCounted
## Scene-owned immutable wall dependency keys; retains no images or live room objects.
const LIVE_FIELDS=["water_level","hull_crack","leak_repair","moonbay_mission","tidal_chamber","airlock_cycle","fire","fire_heat","fire_water_seconds","electrical_repair_progress","survey_clock","survey_blocked"]
var previous_common:Array=[]
var previous_power:Dictionary={}
var previous_external:Array=[]
var previous_cells:Array=[]
var keys:Dictionary={}
var shade_keys:Dictionary={}
var builds:=0
var reuses:=0
func structural(room:Dictionary)->Dictionary:
	var result:Dictionary=room.duplicate(true)
	for field in LIVE_FIELDS:result.erase(field)
	return result
func prepare(common:Array,occupied:Dictionary,powered:Dictionary,rooms:Array)->void:
	# Interior lighting is on floor/light passes; corridor shade stays keyed separately.
	common=common.duplicate()
	common[0]=common[0].duplicate()
	common[0].erase("interior")
	var included:Dictionary={}
	for room in common[2]:included[room.pos]=true
	var external:Array=[]
	var external_seen:Dictionary={}
	var cells:Array=[]
	for room in rooms:
		cells.append(room.pos)
		for y in range(-1,2):
			for x in range(-1,2):
				var cell:Vector2i=room.pos+Vector2i(x,y)
				if included.has(cell) or external_seen.has(cell) or not occupied.has(cell):continue
				external_seen[cell]=true
				external.append([cell,structural(occupied[cell])])
	if not keys.is_empty() and common==previous_common and powered==previous_power and external==previous_external and cells==previous_cells:
		reuses+=1;return
	previous_common=common.duplicate(true)
	previous_power=powered.duplicate(true)
	previous_external=external
	previous_cells=cells
	keys.clear();shade_keys.clear()
	var snapshots:Dictionary={}
	var entries:Dictionary={}
	for entry in previous_common[5]:entries[entry[0]]=[entry]
	for room in rooms:
		var structures:Array=[];var power:Array=[]
		for y in range(-1,2):
			for x in range(-1,2):
				var cell:Vector2i=room.pos+Vector2i(x,y)
				if not snapshots.has(cell):snapshots[cell]=structural(occupied.get(cell,{}))
				structures.append([cell,snapshots[cell]]);power.append([cell,powered.has(cell)])
		keys[room.pos]=[previous_common[0],previous_common[1],structures,power,entries.get(room.pos,[]),previous_common.slice(6),0.0]
	builds+=1
func key(room:Dictionary,shade:float)->Array:
	var base:Array=keys[room.pos]
	if shade==0.0:return base
	if not shade_keys.has(room.pos) or shade_keys[room.pos][-1]!=shade:
		var result:Array=base.duplicate()
		result[-1]=shade
		shade_keys[room.pos]=result
	return shade_keys[room.pos]
