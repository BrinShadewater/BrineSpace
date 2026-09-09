extends RefCounted
## Audio uses the same scrolled/zoomed grid coordinates as the visible station.
static func listener_position(game) -> Vector2:
	return game.grid_scroll.get_global_rect().get_center()

static func screen_position(game, cell: Vector2) -> Vector2:
	return game.grid_view.get_global_transform() * ((cell+Vector2.ONE*0.5)*game.get_cell_size())

static func configure(player: AudioStreamPlayer2D, game, cell: Vector2) -> void:
	player.position = screen_position(game,cell)
	player.max_distance = maxf(game.get_cell_size()*6.0,game.grid_scroll.size.length()*0.65)
	player.attenuation = 1.6
	player.panning_strength = 0.55

static func sources(game) -> Dictionary:
	var result := {}
	var distances := {}
	var center := listener_position(game)
	for room in game.placed_rooms:
		if not game.powered_room_cells.has(room.pos) or room.get("suspended",false): continue
		var kinds := []
		if room.get("category","") in ["Engineering","Drone"] and not str(room.id).begins_with("corridor"): kinds.append("machinery")
		if room.id in ["life_support","hydroponics_bay","biodome"]: kinds.append("life_support")
		if room.id == "brine_core": kinds.append("core")
		if room.id == "cold_store": kinds.append("refrigeration")
		if room.id == "salvage_workshop": kinds.append("workshop")
		if room.id == "galley": kinds.append("galley_work")
		if room.id in ["med_bay","med_center","med_office"]: kinds.append("medical_work")
		if room.id in ["research_lab","bio_lab","xeno_lab","anomaly_lab"]: kinds.append("lab_work")
		if room.id in ["hydroponics_bay","mycelium_nursery","biodome"]: kinds.append("cultivation_work")
		if room.id == "listening_post": kinds.append("receiver")
		if room.id == "airlock" and preload("res://scripts/airlock_cycle.gd").state(room).phase in ["flooding","draining"]: kinds.append("airlock")
		for kind in kinds:
			consider(result,distances,kind,Vector2(room.pos),screen_position(game,Vector2(room.pos)).distance_squared_to(center))
	for drone in game.drone_fleet.drones.values():
		if drone.phase == "working" and drone.get("kind","") in ["mining","salvage"] and float(drone.get("battery",1.0)) > 0.0:
			var cell := Vector2(drone.get("position",drone.get("target",Vector2.ZERO)))
			consider(result,distances,str(drone.kind)+"_work",cell,screen_position(game,cell).distance_squared_to(center))
		if drone.phase in ["launching","outbound","returning","docking"]:
			var cell := Vector2(drone.get("position",drone.get("home",Vector2.ZERO)))
			consider(result,distances,"drone",cell,screen_position(game,cell).distance_squared_to(center))
	return result

static func consider(result: Dictionary, distances: Dictionary, kind: String, cell: Vector2, distance: float) -> void:
	if distance < float(distances.get(kind,INF)):
		result[kind] = cell
		distances[kind] = distance
