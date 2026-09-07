extends RefCounted
const CYCLES := 3
const POWER_COST := 3

static func target(game, kind: String) -> Vector2i:
	var cells: Array=game.drone_fleet.sites.keys()
	cells.sort_custom(func(a,b):return a.x*40+a.y<b.x*40+b.y)
	for cell in cells:
		var site: Dictionary=game.drone_fleet.sites[cell]
		if site.kind==kind and not site.discovered and site.units>0:
			var reserved:=false
			for room in game.placed_rooms:
				if room.get("investigation",{}).get("target",Vector2i(-1,-1))==cell:reserved=true
			if not reserved:return cell
	return Vector2i(-1,-1)

static func begin(game, cell: Vector2i, kind: String) -> bool:
	if kind not in ["mining","salvage"] or not game.occupied.has(cell):return false
	var room: Dictionary=game.occupied[cell]
	if room.id!="listening_post" or not room.get("investigation",{}).is_empty():return false
	if not game.running or room.get("suspended",false) or not game.powered_room_cells.has(cell):return false
	var destination:=target(game,kind)
	if destination==Vector2i(-1,-1) or int(game.resources.power)<POWER_COST:return false
	game.resources.power-=POWER_COST
	room.investigation={"target":destination,"remaining":CYCLES,"kind":kind}
	game._log("Listening Post: resolving %s echoes. Three functioning cycles required." % kind,false)
	return true

static func tick(game) -> void:
	for room in game.placed_rooms:
		if room.id!="listening_post" or room.get("investigation",{}).is_empty():continue
		if not game.powered_room_cells.has(room.pos):continue
		var investigation: Dictionary=room.investigation
		investigation.remaining-=1
		if investigation.remaining>0:continue
		var cell: Vector2i=investigation.target
		if game.drone_fleet.sites.has(cell):
			game.drone_fleet.sites[cell].discovered=true
			room["last_signal"]=cell
			game._log("Listening Post: %s resolved at %s. Extraction still requires a drone route." % [investigation.kind,cell],false)
		room.erase("investigation")

static func inspector(game, room: Dictionary) -> String:
	var investigation: Dictionary=room.get("investigation",{})
	if not investigation.is_empty():return "\nINVESTIGATION: %s\n%d functioning cycles remaining. Pauses while offline.\n" % [investigation.kind,investigation.remaining]
	var result:="\nLISTENING POST\nInvestigate one signal: 3 stored Power, 3 functioning cycles.\n"
	for kind in ["mining","salvage"]:
		if target(game,kind)!=Vector2i(-1,-1):
			result+="[url=listen:%d:%d:%s]Investigate %s echoes[/url]\n" % [room.pos.x,room.pos.y,kind,kind]
	if room.has("last_signal"):result+="Last resolved coordinates: %s\n" % room.last_signal
	return result
