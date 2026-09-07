extends SceneTree
const Geometry = preload("res://tools/modular_room_geometry.gd")
const Database = preload("res://scripts/room_database.gd")
const NAMES = ["north","east","south","west"]
var failures := 0
func check(value: bool, message: String) -> void:
	if not value:
		failures+=1
		if failures<20: push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	var manifest: Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/production-ten/manifest.json"))
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--additional-manifest="):
			var extra: Variant=JSON.parse_string(FileAccess.get_file_as_string(arg.trim_prefix("--additional-manifest=")))
			assert(extra is Array and not extra.is_empty(),"Additional manifest must contain rooms")
			manifest.append_array(extra)
	var identities: Dictionary={}
	for entry in manifest:
		assert(not identities.has(entry.id),"Duplicate connection identity")
		identities[entry.id]=true
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
	var open_pairs := 0
	var samples := 0
	for a in registrations:
		for b in registrations:
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
				if expected:
					open_pairs+=1
					for step in range(101):
						check(Geometry.can_stand(Vector2(offset)*384*step/100.0,layout,props,edges),"Connected route obstructed: %s/%s side%d"%[a.id,b.id,side])
						samples+=1
				else:
					check(not Geometry.can_stand(Vector2(offset)*192,layout,props,edges),"Incompatible boundary traversable")
				pairs+=1
	print("REGISTERED ROOM CONNECTIONS: %d pairs, %d compatible, %d route samples, %d failures; geometry only, not pixel/actor/economy acceptance"%[pairs,open_pairs,samples,failures])
	quit(1 if failures else 0)
