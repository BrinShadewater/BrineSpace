extends RefCounted
## Physical branch selection shared by pressure control and emergency isolation.
## A boundary must be a real bridge: alternate routes make it unsafe to seal.
const DIRS := [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]

static func plan(rooms: Array, inside: Vector2i, outside: Vector2i, connected: Callable) -> Dictionary:
	var occupied := {}
	for room in rooms: occupied[room.pos]=room
	if not occupied.has(inside) or not occupied.has(outside):
		return {"ok":false,"reason":"Both sides must contain built rooms."}
	if not DIRS.has(outside-inside) or not connected.call(occupied[inside],occupied[outside],outside-inside):
		return {"ok":false,"reason":"Select a connected doorway."}
	var cells: Array[Vector2i]=[inside]
	var seen := {inside:true}
	var index := 0
	while index<cells.size():
		var cell:=cells[index]
		index+=1
		for direction in DIRS:
			var next: Vector2i=cell+direction
			if (cell==inside and next==outside) or (cell==outside and next==inside):continue
			if seen.has(next) or not occupied.has(next):continue
			if not connected.call(occupied[cell],occupied[next],direction):continue
			seen[next]=true
			cells.append(next)
	if seen.has(outside):
		return {"ok":false,"reason":"Another doorway reconnects this branch. Choose a single entrance."}
	for cell in cells:
		if occupied[cell].id=="brine_core":
			return {"ok":false,"reason":"The selected branch contains BRINE Core."}
	return {"ok":true,"cells":cells,"inside":inside,"outside":outside}

