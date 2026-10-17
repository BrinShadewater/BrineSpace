extends SceneTree
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(value:bool,label:String):
	checks+=1
	if not value:failures+=1;push_error(label)
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var old=FreshProjection
	var cache=preload("res://scripts/retained_wall_context.gd").new()
	var occupied:Dictionary={};var powered:Dictionary={};var rooms:Array=[]
	for i in range(40):
		var cell:=Vector2i(i%8,i/8)
		var room:={"pos":cell,"id":"reactor","rotation":i%4,"cost":{"metal":12},"water_level":0.5,"fire":{"elapsed":0.0}}
		occupied[cell]=room;powered[cell]=true;rooms.append(room)
	# Outside the structural snapshot, but inside a painted wall's dependencies.
	occupied[Vector2i(-1,0)]={"pos":Vector2i(-1,0),"id":"corridor","rotation":0}
	var common:Array=[{"walls":true,"power":true},128.0,[],40,powered,[],1,true,Vector2i(-1,-1),true,0.0]
	for room in rooms:
		common[2].append(cache.structural(room))
		common[5].append([room.pos,[false,false,false,false],0.0,false,"",true,0,false,0.0])
	for iteration in range(200):
		if iteration%20==0:
			occupied[Vector2i(-1,0)].rotation=iteration%4
			common[6]=iteration
		elif iteration%20==1:powered.erase(Vector2i(0,0))
		elif iteration%20==2:powered[Vector2i(0,0)]=true
		elif iteration%20==3:occupied[Vector2i(-1,0)].rotation+=1
		elif iteration%20==4:occupied[Vector2i(-1,0)].water_level=float(iteration)
		cache.prepare(common,occupied,powered,rooms)
		var fresh:Dictionary=old.context(common,occupied,powered)
		for room in rooms:
			var shade:=float(iteration%7)/7.0
			check(cache.key(room,shade)==old.key(fresh,room,shade),"Exact fresh projection "+str(iteration)+" "+str(room.pos))
	check(cache.reuses>100,"Unchanged and live-only inputs reuse metadata")
	check(cache.keys.size()==40 and cache.shade_keys.size()<=40,"Only current room/shade keys retained")
	var saved:Array=cache.key(rooms[0],0.0).duplicate(true)
	occupied[Vector2i(-1,0)].rotation+=1
	check(cache.key(rooms[0],0.0)==saved,"Cached key stays immutable after external input mutation")
	cache.prepare(common,occupied,powered,rooms)
	check(cache.key(rooms[0],0.0)!=saved,"External-neighbor mutation invalidates cache")
	rooms.pop_back()
	cache.prepare(common,occupied,powered,rooms)
	check(cache.keys.size()==39 and cache.shade_keys.is_empty(),"Removed rooms and stale shades are released")
	var weak:WeakRef=weakref(cache)
	cache=null
	check(weak.get_ref()==null,"Scene-owned context does not retain itself")
	var result:={"checks":checks,"failures":failures}
	FileAccess.open("user://result.json",FileAccess.WRITE).store_string(JSON.stringify(result))
	print("RETAINED WALL CONTEXT ",JSON.stringify(result));quit(1 if failures else 0)

class FreshProjection extends RefCounted:
	const LIVE_FIELDS=["water_level","hull_crack","leak_repair","moonbay_mission","tidal_chamber","airlock_cycle","fire","fire_heat","fire_water_seconds","electrical_repair_progress","survey_clock","survey_blocked"]
	static func context(common:Array,occupied:Dictionary,powered:Dictionary)->Dictionary:
		common=common.duplicate()
		common[0]=common[0].duplicate()
		common[0].erase("interior")
		var entries:Dictionary={}
		for entry in common[5]:entries[entry[0]]=[entry.duplicate(true)]
		return {"common":common,"occupied":occupied,"powered":powered,"snapshots":{},"entries":entries,"globals":common.slice(6)}
	static func key(ctx:Dictionary,room:Dictionary,shade:float)->Array:
		var structures:Array=[];var power:Array=[]
		for y in range(-1,2):
			for x in range(-1,2):
				var cell:Vector2i=room.pos+Vector2i(x,y)
				if not ctx.snapshots.has(cell):
					var snapshot:Dictionary=ctx.occupied.get(cell,{}).duplicate(true)
					for field in LIVE_FIELDS:snapshot.erase(field)
					ctx.snapshots[cell]=snapshot
				structures.append([cell,ctx.snapshots[cell]]);power.append([cell,ctx.powered.has(cell)])
		return [ctx.common[0],ctx.common[1],structures,power,ctx.entries.get(room.pos,[]),ctx.globals,shade]
