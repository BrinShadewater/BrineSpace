extends RefCounted
const Architects=preload("res://scripts/architects.gd")
const MATCHES={
	"bill":["brine_core","command_center","crew_hab","crew_lounge","galley"],
	"veld":["research_lab","bio_lab","xeno_lab","anomaly_lab","data_archive","med_bay","med_center"],
	"branforth":["reactor","maintenance_bay","salvage_workshop","life_support","pressure_control","airlock"],
	"marsh":["mining_drone_bay","salvage_drone_bay","construction_drone_bay","battery_array","listening_post"]}
static func identity(game,actor) -> String:
	for id in Architects.IDS:
		if Architects.actor_for(game,id)==actor:return id
	return ""
static func reward(id: String,room: Dictionary) -> String:
	if not MATCHES.get(id,[]).has(room.get("id","")):return ""
	return "metal" if id in ["branforth","marsh"] else "data"
static func assign(game,id: String,cell: Vector2i) -> bool:
	if id not in Architects.IDS or not Architects.present(game,id):return false
	if cell!=Vector2i(-1,-1) and not game.occupied.has(cell):return false
	var actor=Architects.actor_for(game,id)
	if actor.dead:return false
	if cell!=Vector2i(-1,-1):
		for other in Architects.IDS:
			var peer=Architects.actor_for(game,other)
			if peer!=actor and Architects.present(game,other) and not peer.dead and peer.primary_room==cell:return false
	actor.primary_room=cell
	if actor.goal=="primary-work":actor.goal="";actor.path.clear();actor.timer=0;actor.state="idle"
	return true
static func attending(actor,cell: Vector2i) -> bool:
	return actor.active and not actor.dead and actor.primary_room==cell and actor.goal=="primary-work" and actor.goal_cell==cell and actor.path.is_empty() and actor.state=="interact" and actor.timer>0 and actor.expedition.is_empty() and actor.movement_medium=="dry"
static func bonuses(game,working: Dictionary) -> Dictionary:
	var result := {}
	var counted := {}
	for id in Architects.IDS:
		var actor=Architects.actor_for(game,id)
		var cell: Vector2i=actor.primary_room
		if not Architects.present(game,id) or not working.has(cell) or counted.has(cell) or not game.occupied.has(cell) or not attending(actor,cell):continue
		var key:=reward(id,game.occupied[cell])
		if key.is_empty():continue
		result[key]=int(result.get(key,0))+1;counted[cell]=true
	return result
static func break_needed(game,actor) -> bool:
	if not actor.needs_air():return false
	var start: int=actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot))
	if start<0:return false
	for need in ["hunger","fatigue"]:
		if actor.needs[need]<65:continue
		if need=="hunger" and (int(game.resources.food)<=0 or actor.helmet_equipped):continue
		for cell in actor.room_nodes:
			if not actor.service_preferences[need].has(game.occupied[cell].id) or not actor.service_available(game,cell):continue
			for target in actor.room_nodes[cell]:
				if not actor.route_between(start,target).is_empty():return true
	return false

static func choose(game,actor) -> bool:
	var cell: Vector2i=actor.primary_room
	if not game.occupied.has(cell) or not actor.room_nodes.has(cell) or not actor.service_available(game,cell) or actor.movement_medium!="dry":return false
	if break_needed(game,actor):return false
	var start: int=actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot))
	if start<0:return false
	var nodes: Array=actor.room_nodes[cell].duplicate()
	var center: Vector2=(Vector2(cell)+Vector2.ONE*0.5)*384
	var equipment: Array=nodes.filter(func(node):return actor.equipment_spot(cell,actor.graph.get_point_position(node)-center))
	if not equipment.is_empty():nodes=equipment
	nodes.sort_custom(func(a,b):return actor.graph.get_point_position(a).distance_squared_to(center)<actor.graph.get_point_position(b).distance_squared_to(center))
	for node in nodes:
		var target: Vector2=actor.graph.get_point_position(node)
		if not actor.spawn_clear(target):continue
		var route: PackedVector2Array=actor.route_between(start,node)
		if route.is_empty():continue
		actor.goal="primary-work";actor.goal_cell=cell;actor.path=actor.smooth_route(route);actor.state="walk"
		actor.activity="going to primary workplace / "+str(game.occupied[cell].display_name)
		if actor.foot.distance_to(target)<12:actor.path.clear();actor.arrive()
		return true
	return false
