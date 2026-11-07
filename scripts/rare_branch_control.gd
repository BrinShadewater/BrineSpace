extends RefCounted
const Branch=preload("res://scripts/station_branch.gd")
const Architects=preload("res://scripts/architects.gd")

static func physical(a: Dictionary,b: Dictionary,d: Vector2i) -> bool:
	var db=preload("res://scripts/room_database.gd")
	var names: Array=["north","east","south","west"]
	var index: int=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT].find(d)
	if index<0:return false
	var a_doors: Array=db.get_layout(a.layout).doors
	var b_doors: Array=db.get_layout(b.layout).doors
	return a_doors.has(names[posmod(index-int(a.get("rotation",0)),4)]) and b_doors.has(names[posmod(index+2-int(b.get("rotation",0)),4)])

static func occupied_by_crew(game,cells: Array) -> bool:
	for id in Architects.IDS:
		var actor=Architects.actor_for(game,id)
		if actor.active and not actor.dead and cells.has(actor.cell_at(actor.foot)):return true
	return false

static func plan(game,controller: Dictionary,inside: Vector2i,outside: Vector2i) -> Dictionary:
	var result:=Branch.plan(game.placed_rooms,inside,outside,physical)
	if result.ok and result.cells.has(controller.pos):return {"ok":false,"reason":"Controller must remain outside the branch."}
	return result

static func select(game,controller: Dictionary,inside: Vector2i,outside: Vector2i) -> bool:
	if controller.has("branch_active"):return false
	var result:=plan(game,controller,inside,outside)
	if not result.ok:return false
	controller["branch_preview"]={"inside":inside,"outside":outside}
	return true

static func commit(game,controller: Dictionary) -> bool:
	if not game.running or not game.powered_room_cells.has(controller.pos) or controller.get("suspended",false):return false
	if not controller.has("branch_preview") or controller.has("branch_active"):return false
	var preview: Dictionary=controller.branch_preview
	var result:=plan(game,controller,preview.inside,preview.outside)
	if not result.ok or occupied_by_crew(game,result.cells):return false
	if int(game.resources.power)<4:return false
	for cell in result.cells:
		if game.occupied[cell].has("branch_owner"):return false
	game.resources.power-=4
	controller.branch_active={"cells":result.cells,"inside":result.inside,"outside":result.outside,"remaining":2,"mode":"flood" if controller.id=="pressure_control" else "isolate"}
	if controller.id=="pressure_control":
		for cell in result.cells:game.occupied[cell]["branch_owner"]=controller.pos
	else:
		controller.branch_active.remaining=0
		controller.branch_active["armed"]=true
	game._log("%s: branch secured. Two functioning cycles to complete." % controller.display_name,false)
	return true

static func release(game,controller: Dictionary) -> void:
	if not controller.has("branch_active"):return
	for room in game.placed_rooms:
		if room.get("branch_owner",Vector2i(-1,-1))!=controller.pos:continue
		room.erase("branch_owner")
		room.erase("flooded")
		room.erase("isolated")
	controller.erase("branch_active")
	game._log("Branch released through emergency equalization.",false)

static func tick(game) -> void:
	for room in game.placed_rooms:
		if room.has("branch_owner") and not game.occupied.has(room.branch_owner):
			room.erase("branch_owner")
			room.erase("flooded")
			room.erase("isolated")
	for controller in game.placed_rooms:
		if not controller.has("branch_active"):continue
		if controller.branch_active.get("armed",false):
			for cell in controller.branch_active.cells:
				if not game.occupied.has(cell) or not game.occupied[cell].get("local_incident",false):continue
				for affected in controller.branch_active.cells:
					if game.occupied.has(affected):
						game.occupied[affected]["branch_owner"]=controller.pos
						game.occupied[affected]["isolated"]=true
				controller.branch_active.armed=false
				game._log("Isolation Vault: local incident contained. Branch disconnected; occupants remain inside.",false)
				break
			continue
		if not game.powered_room_cells.has(controller.pos):continue
		var operation: Dictionary=controller.branch_active
		if operation.remaining<=0:continue
		operation.remaining-=1
		if operation.remaining>0:continue
		for cell in operation.cells:
			if not game.occupied.has(cell):continue
			game.occupied[cell]["flooded" if operation.mode=="flood" else "isolated"]=true
		game._log("%s: branch %s complete." % [controller.display_name,operation.mode],false)

static func offline(room: Dictionary) -> bool:
	return room.get("isolated",false) or (room.get("flooded",false) and not room.get("flood_compatible",false))

static func inspector(game,controller: Dictionary) -> String:
	var prefix:="branch:%d:%d:" % [controller.pos.x,controller.pos.y]
	var text:="\nBRANCH CONTROL\nEmpty branches only. 4 Power, 2 functioning cycles.\n"
	if controller.has("branch_active"):
		text+=("ARMED — reserve latch ready.\n" if controller.branch_active.get("armed",false) else "")
		text+="%s: %d cycles remaining.\n[url=%srelease]Emergency equalize and release[/url]\n" % [controller.branch_active.mode,controller.branch_active.remaining,prefix]
		return text
	if controller.has("branch_preview"):
		var p: Dictionary=controller.branch_preview
		var result:=plan(game,controller,p.inside,p.outside)
		if result.ok:
			text+="Affected rooms: %d\n" % result.cells.size()
			for cell in result.cells:text+="%s %s\n" % [game.occupied[cell].display_name,cell]
			text+="Crew present: %s\n[url=%scommit]Confirm branch operation[/url]\n" % ["YES — evacuate before starting" if occupied_by_crew(game,result.cells) else "no",prefix]
	var listed:=0
	for room in game.placed_rooms:
		for direction in Branch.DIRS:
			var result:=plan(game,controller,room.pos,room.pos+direction)
			if not result.ok:continue
			text+="[url=%sselect:%d:%d:%d:%d]Preview %s branch (%d rooms)[/url]\n" % [prefix,room.pos.x,room.pos.y,room.pos.x+direction.x,room.pos.y+direction.y,room.display_name,result.cells.size()]
			listed+=1
			if listed>=12:return text
	return text
