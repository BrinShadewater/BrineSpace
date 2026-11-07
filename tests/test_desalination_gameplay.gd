extends SceneTree
const Rooms = preload("res://scripts/room_database.gd")
const Meta = preload("res://scripts/meta_state.gd")
class Station extends "res://scripts/main.gd":
	func _refresh_all() -> void: pass
var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func add(game, id: String, cell: Vector2i) -> Dictionary:
	var room := Rooms.get_room(id)
	room.pos = cell
	room.rotation = 0
	game.placed_rooms.append(room)
	game.occupied[cell] = room
	return room
func _init() -> void:
	var definition := Rooms.get_room("desalination_unit")
	check(not definition.is_empty(),"Desalination Unit is a registered room")
	if definition.is_empty():
		quit(1)
		return
	check(definition.cost=={"metal":5} and definition.production=={"water":2} and definition.consumption=={"power":2},"Agreed paid cost, output and Power requirement")
	check(definition.rarity=="common" and definition.ocean_side=="north", "Early common blueprint has an ocean intake")
	check(Rooms.get_layout(definition.layout).doors==["west","east","south"],"Three door blueprint leaves the north wall reserved for its intake")
	var game := Station.new()
	game.meta.save_path = "user://desalination-gameplay.meta"
	check(game.meta.unlocked_room_ids.has("desalination_unit"),"Fresh profile owns the unit")
	game.running = true
	add(game,"brine_core",Vector2i(20,20))
	game.resources.metal = 5
	game.resources.data = 0
	game.resources.water = 4
	game.resources.power = 3
	game.hand.assign(["desalination_unit"])
	game.selected_card_id = "desalination_unit"
	# Each rotated door can be the sole station connection; the fourth side stays intake-only.
	var directions: Array[String] = ["north","east","south","west"]
	for q in range(4):
		definition.rotation=q
		game.selected_rotation=q
		var doors:Array=game.get_room_doors(definition)
		check(doors.size()==3 and not doors.has(directions[q]),"Three rotated doors exclude intake q%d"%q)
		for side in range(4):
			game.occupied.clear()
			game.placed_rooms.clear()
			var connection:Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][side]
			add(game,"brine_core",Vector2i(20,20)+connection)
			var problem:String=game.get_placement_problem("desalination_unit",Vector2i(20,20))
			check(not problem.is_empty() if side==q else problem.is_empty(),"Placement uses door rather than intake q%d side%d: %s"%[q,side,problem])
	game.occupied.clear()
	game.placed_rooms.clear()
	add(game,"brine_core",Vector2i(20,20))
	game.selected_rotation = 0
	check(game.get_placement_problem("desalination_unit",Vector2i(20,19)).is_empty(),"South door connects to the Core with a clear north intake")
	game._on_grid_clicked(Vector2i(20,19))
	check(game.drone_fleet.reserved(Vector2i(20,19)) and game.resources.metal==0,"Normal click spends five Metal and queues construction")
	check(game.resources.data==0 and game.resources.water==4,"No Data or Water is required to build")
	check(not game.get_footprint_placement_problem("corridor",Vector2i(20,18),0).is_empty(),"Queued intake keeps its ocean cell available")
	game.drone_fleet.orders.clear()
	var unit := add(game,"desalination_unit",Vector2i(20,19)) # Completed-room economy fixture.
	var forecast: Dictionary = game._simulate_room_economy(true,1)
	check(forecast.delta.water==2 and forecast.power_used==3,"Forecast includes two Water and Core plus unit demand")
	game._apply_room_economy()
	check(game.resources.water==6 and game.resources.power==0,"Actual cycle produces water and spends the three required Power")
	game._apply_room_economy()
	check(game.resources.water==6 and not game.powered_room_cells.has(unit.pos),"No Power means no fresh water")
	game.resources.power = 3
	unit.suspended = true
	forecast = game._simulate_room_economy()
	check(forecast.offline[unit.pos]=="SUSPENDED" and int(forecast.delta.get("water",0))==0,"Suspension stops production")
	unit.suspended = false
	game.hardware.pumps = false
	forecast = game._simulate_room_economy()
	check(forecast.offline[unit.pos]=="PUMPS OFF" and int(forecast.delta.get("water",0))==0,"Pump switch stops production")
	game.hardware.pumps = true
	var intake := Vector2i(20,18)
	for blocker in ["room","rock","deposit","construction"]:
		if blocker=="room": game.occupied[intake] = {"id":"corridor","display_name":"Corridor"}
		elif blocker=="rock": game.wrecks[intake] = {"kind":"basalt","cleared":false}
		elif blocker=="deposit": game.drone_fleet.sites[intake] = {"kind":"mining","units":5,"discovered":true}
		else: game.drone_fleet.enqueue("corridor",intake,0)
		game.resources.power = 1
		forecast = game._simulate_room_economy()
		check(forecast.offline[unit.pos]=="INTAKE BLOCKED" and int(forecast.delta.get("water",0))==0,"Intake obstruction stops production: "+blocker)
		check(not forecast.blackout and forecast.power_used==1,"A blocked intake draws no Power and does not cause a false blackout: "+blocker)
		game.occupied.erase(intake)
		game.wrecks.clear()
		game.drone_fleet.sites.clear()
		game.drone_fleet.orders.clear()
	for q in range(4):
		unit.rotation = q
		var cells: Array[Vector2i] = game._ocean_exterior_cells(unit)
		var expected: Vector2i = unit.pos+[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][q]
		check(cells==[expected],"Quarter turn moves intake correctly")
		var previous: Dictionary = game.occupied.get(expected,{})
		game.occupied[expected] = {"id":"corridor","display_name":"Blocker"}
		check(not game._ocean_face_problem(unit).is_empty(),"Rotated intake detects its actual obstruction")
		if previous.is_empty(): game.occupied.erase(expected)
		else: game.occupied[expected] = previous
	unit.rotation = 0
	game.resources.power = 3
	game.resources.water = 29
	game._apply_room_economy()
	check(game.resources.water==30,"Production respects Water storage capacity")
	game.free()
	print("DESALINATION GAMEPLAY: %d checks / %d failures" % [checks,failures])
	quit(1 if failures else 0)
