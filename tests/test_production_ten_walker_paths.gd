extends SceneTree
const Geometry = preload("res://tools/modular_room_geometry.gd")
const Database = preload("res://scripts/room_database.gd")
const NAMES = ["north","east","south","west"]
var failures := 0
class RegisteredGeometry extends Control:
	var registrations: Dictionary = {}
	func bill_room_geometry(room: Dictionary, sides: Array) -> Dictionary:
		var entry: Dictionary = registrations["%s:%d" % [room.id,int(room.rotation)]]
		var layout: Array = [entry.room.duplicate(true)]
		var edges: Array = Geometry.edges(layout)
		# Edge order for a single room is N/E/S/W, matching embedded views.
		for side in range(4): edges[side].open = sides.has(side)
		return {"layout":layout,"props":entry.props.duplicate(true),"edges":edges}
func check(value: bool, message: String) -> void:
	if not value:
		failures+=1
		if failures<20: push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	var manifest: Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/production-ten/manifest.json"))
	var focus := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--additional-manifest="):
			var path := arg.trim_prefix("--additional-manifest=")
			if not FileAccess.file_exists(path):
				push_error("Missing additional manifest: "+path)
				quit(1)
				return
			var extra: Variant=JSON.parse_string(FileAccess.get_file_as_string(path))
			if not (extra is Array) or extra.is_empty():
				push_error("Additional manifest must contain rooms: "+path)
				quit(1)
				return
			manifest.append_array(extra)
		if arg.begins_with("--focus="): focus=arg.trim_prefix("--focus=")
	assert(focus.is_empty() or manifest.any(func(entry): return entry.id==focus),"Focus identity missing")
	var game=load("res://scripts/main.gd").new()
	var registrations: Array=[]
	for entry in manifest:
		var view=load("res://"+entry.integration.view).new()
		view.embedded=true
		root.add_child(view)
		for q in range(4):
			view.configure_embedded(q,[],false,0.0)
			var room: Dictionary=view.layout[0].duplicate(true)
			var ports: Array=Database.get_layout(Database.get_room(entry.id).layout).doors
			for side in range(4):
				check(Geometry.has_port(room,side)==ports.has(NAMES[posmod(side-q,4)]),"Database topology mismatch: "+entry.id)
				check(not view.edges[side].open,"Disconnected opening: "+entry.id)
			registrations.append({"id":entry.id,"rotation":q,"room":room,"props":view.props.duplicate(true),"ports":ports})
		view.free()
	var pairs := 0
	var provider := RegisteredGeometry.new()
	game.grid_view = provider
	for registration in registrations:
		provider.registrations["%s:%d" % [registration.id,registration.rotation]] = registration
	var npc = preload("res://scripts/bill_npc.gd").new()
	var open_pairs := 0
	var samples := 0
	for a in registrations:
		for b in registrations:
			if not focus.is_empty() and a.id!=focus and b.id!=focus: continue
			for side in range(4):
				var offset: Vector2i=Geometry.DIRS[side]
				var first: Dictionary=a.room.duplicate(true)
				var second: Dictionary=b.room.duplicate(true)
				second.cell=offset
				var layout: Array=[first,second]
				var edges: Array=Geometry.edges(layout)
				var expected: bool=a.ports.has(NAMES[posmod(side-a.rotation,4)]) and b.ports.has(NAMES[posmod(side+2-b.rotation,4)])
				var shared: Array=edges.filter(func(edge): return edge.shared)
				check(shared.size()==1 and shared[0].open==expected,"Shared boundary disagrees with database")
				var props: Array=a.props.duplicate(true)
				for prop in b.props:
					var moved: Dictionary=prop.duplicate(true)
					moved.rect.position+=Vector2(offset)*384
					props.append(moved)
				var origin := Vector2i(20,20)
				game.occupied.clear()
				for info in [[a,origin],[b,origin+offset]]:
					var placed: Dictionary=Database.get_room(info[0].id).duplicate(true)
					placed.pos=info[1]
					placed.rotation=info[0].rotation
					game.occupied[info[1]]=placed
				game.test_walker_cell=origin
				game.test_walker_next_cell=origin+offset
				game.test_walker_previous_cell=Vector2i(-1,-1)
				check(game._connected_neighbor_cells(origin).has(origin+offset)==expected,"Walker neighbor selection disagrees")
				if expected:
					open_pairs+=1
					npc.rebuild(game)
					var center := (Vector2(origin)+Vector2.ONE*0.5)*384.0
					var start: int = npc.nearest_in_room(center,origin,false)
					var finish: int = npc.nearest_in_room(center+Vector2(offset)*384.0,origin+offset,false)
					check(start >= 0 and finish >= 0,"Room must contain a standable navigation point")
					if start >= 0 and finish >= 0:
						var route: PackedVector2Array = npc.graph.get_point_path(start,finish)
						check(not route.is_empty(),"Live NPC graph disconnected: %s q%d/%s q%d side%d" % [a.id,a.rotation,b.id,b.rotation,side])
						for step in range(1,route.size()):
							check(npc.segment_clear(route[step-1],route[step]),"Live NPC route crosses a blocker")
							samples+=1
				else:
					check(not Geometry.can_stand(Vector2(offset)*192,layout,props,edges),"Incompatible boundary traversable")
				pairs+=1
	print("REGISTERED ROOM WALKER PATHS: %d pairs, %d compatible, %d graph segments, %d failures; live NPC graph; no sprite/pixel acceptance"%[pairs,open_pairs,samples,failures])
	provider.free()
	game.free()
	quit(1 if failures else 0)
