extends RefCounted
## Local containment failures give armed branch bulkheads a physical boundary to protect.
static func seed(game) -> void:
	if game.cycle%8!=0:return
	for room in game.placed_rooms:
		if game.powered_room_cells.has(room.pos) and room.get("tags",[]).has("containment_risk"):
			room["local_incident"]=true
			room["hull_crack"]=minf(1.0,float(room.get("hull_crack",0))+preload("res://scripts/hull_repair.gd").SEVERITIES[(game.cycle/8-1)%3])
			game._log("Containment fault at %s. Repair the room or isolate its branch." % room.pos,false)
			return

static func resolve(game) -> void:
	var spread: Array[Vector2i]=[]
	var damage:=0
	for room in game.placed_rooms:
		if not room.get("local_incident",false) or room.get("isolated",false):continue
		damage+=1
		for direction in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
			var cell: Vector2i=room.pos+direction
			if not game.occupied.has(cell) or game.occupied[cell].get("local_incident",false):continue
			if game._placed_rooms_connected(room,game.occupied[cell],direction):
				spread.append(cell)
				break
	for cell in spread:game.occupied[cell]["local_incident"]=true
	if damage>0:
		game.resources.integrity=maxi(0,int(game.resources.integrity)-damage)
		game._log("Local containment faults: %d Integrity lost. Repair affected rooms." % damage,false)

static func repair(game,cell: Vector2i) -> bool:
	if game.occupied.has(cell) and float(game.occupied[cell].get("hull_crack",0))>0:
		return preload("res://scripts/hull_repair.gd").request(game,cell)
	if not game.running or not game.occupied.has(cell) or not game.occupied[cell].get("local_incident",false) or int(game.resources.metal)<2:return false
	game.resources.metal-=2
	game.occupied[cell].erase("local_incident")
	game.occupied[cell].hull_crack=0.0
	game._log("Containment repair completed at %s." % cell,false)
	return true
