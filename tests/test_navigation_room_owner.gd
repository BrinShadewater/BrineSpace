extends SceneTree
## Reusing local room geometry must preserve each placed room's ownership.
const Main=preload("res://scripts/main.gd")
const Grid=preload("res://scripts/grid_canvas.gd")
const Rooms=preload("res://scripts/room_database.gd")
const NPC=preload("res://scripts/bill_npc.gd")
const Marsh=preload("res://scripts/marsh_npc.gd")
var failures:=0
var checks:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func boarding_route(actor,room:Dictionary)->PackedVector2Array:
	var view=preload("res://rooms/large-rooms/moonbay.gd")
	actor.foot=(Vector2(room.pos)+Vector2.ONE)*actor.CELL+view.airlock_point(room)
	var target:Vector2=(Vector2(room.pos)+Vector2.ONE)*actor.CELL+view.boarding_point(room)
	var start:int=actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot))
	var finish:int=actor.nearest_in_room(target,actor.cell_at(target))
	return PackedVector2Array() if start<0 or finish<0 else actor.graph.get_point_path(start,finish)
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	var game:=Main.new();var grid:=Grid.new();game.grid_view=grid
	game.occupied.clear();game.placed_rooms.clear()
	for anchor in [Vector2i(10,10),Vector2i(15,15),Vector2i(20,20)]:
		var room:Dictionary=Rooms.get_room("moonbay");room.pos=anchor;room.rotation=0
		var state:Dictionary=preload("res://scripts/moonbay_missions.gd").mission_state(room)
		state.phase="boarding";state.progress=3.0;state.chamber_water=1.0
		game.placed_rooms.append(room)
		for y in range(2):
			for x in range(2):game.occupied[anchor+Vector2i(x,y)]=room
	# A different exterior connection makes some tile keys new, others shared.
	var corridor:Dictionary=Rooms.get_room("corridor");corridor.pos=Vector2i(20,19);corridor.rotation=0;game.placed_rooms.append(corridor);game.occupied[corridor.pos]=corridor
	var room:Dictionary=game.occupied[Vector2i(20,20)]
	for Script in [NPC,Marsh]:
		var actor=Script.new();actor.active=true
		await actor.rebuild(game)
		var cold:=boarding_route(actor,room)
		check(not cold.is_empty(),"Cold geometry has a valid boarding route")
		var cache_count:int=actor.room_cache.size()
		var owners:Dictionary={}
		for key in actor.room_cache:
			if actor.room_cache[key].data.has("room"):owners[key]=actor.room_cache[key].data.room.pos
		for repeat in range(2):
			await actor.rebuild(game)
			check(actor.room_cache.size()==cache_count,"Warm rebuild retains local geometry cache")
			for cell in actor.geometry:
				check(actor.geometry[cell].room.pos==game.occupied[cell].pos,"Navigation geometry belongs to its placed room: %s"%cell)
			var warm:=boarding_route(actor,room)
			check(warm==cold,"Warm boarding route matches cold geometry")
			for key in owners:check(actor.room_cache[key].data.room.pos==owners[key],"Shared template owner remains immutable")
		# The first rebuild after locking/unlocking must use the current locks.
		room.doors_locked=true
		await actor.rebuild(game)
		check(boarding_route(actor,room).is_empty(),"First locked rebuild removes internal cell crossings")
		room.doors_locked=false
		await actor.rebuild(game)
		check(boarding_route(actor,room)==cold,"First unlocked rebuild restores exact boarding route")
	grid.free();game.free()
	FileAccess.open("user://result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("NAVIGATION ROOM OWNER ",checks," checks ",failures," failures");quit(1 if failures else 0)
