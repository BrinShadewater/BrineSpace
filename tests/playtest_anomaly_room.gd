extends "res://tests/playtest_underwater_life_support.gd"
var measured_machines: Dictionary={}
class FrozenDiagnosticsView extends "res://rooms/underwater/batch-two/anomaly_lab_view.gd":
	func effect_marks(prop: Dictionary,time: float) -> Array:
		return [] if prop.id=="anomaly_diagnostics" else super.effect_marks(prop,time)

func capture(name: String) -> void:
	# Preserve the normal crew-bearing review frame first.
	await super.capture(name)
	if subject_id!="anomaly_lab": return
	var crew: Array=[game.bill_npc,game.veld_npc,game.branforth_npc]
	var active: Array=[]
	for npc in crew:
		active.append(npc.active)
		npc.active=false
	game.grid_view.queue_redraw()
	await settle()
	measured_machines.clear()
	for prop in subject_view().props:
		measured_machines[prop.id]=super.machine_pixels(Vector2i(20,20),prop)
	var directory:=capture_dir.path_join("machine-measurements")
	DirAccess.make_dir_recursive_absolute(directory)
	room_pixels(Vector2i(20,20)).save_png(directory.path_join(name+".png"))
	for i in range(crew.size()): crew[i].active=active[i]
	game.grid_view.queue_redraw()
	await settle()
	for i in range(crew.size()): expect(crew[i].active==active[i],"Measurement restores crew visibility")
	var record:=FileAccess.open(directory.path_join(name+".json"),FileAccess.WRITE)
	record.store_string(JSON.stringify({"scope":"Crew-free machinery measurement only; normal review PNG preserves input crew visibility, which may be inactive","review_capture":name+".png","crew_active_restored":active,"hosts":measured_machines.keys(),"visual_time":game.visual_time_seconds},"\t"))

func machine_pixels(cell: Vector2i, prop: Dictionary) -> PackedByteArray:
	expect(cell==Vector2i(20,20) and measured_machines.has(prop.id),"Current unoccluded machine sample exists")
	return measured_machines.get(prop.id,PackedByteArray())

func verify_motion_and_routes() -> void:
	subject_id="anomaly_lab"
	if "--negative-missing-diagnostics-motion" in OS.get_cmdline_user_args():
		var frozen:=FrozenDiagnosticsView.new()
		frozen.embedded=true
		frozen.hide()
		game.grid_view.add_child(frozen)
		game.grid_view.anomaly_view=frozen
	await super.verify_motion_and_routes()
	var cell:=Vector2i(20,20)
	var names:=["north","east","south","west"]
	for q in range(4):
		game.occupied[cell].rotation=q
		var view=subject_view()
		view.configure_embedded(q,[0,1,2,3],false,0.0)
		var actual: Array=game.get_room_doors(game.occupied[cell])
		for side in range(4):
			expect(Geometry.has_port(view.layout[0],side)==actual.has(names[side]),"Anomaly single-door topology matches database")
			if actual.has(names[side]):
				for step in range(101): expect(Geometry.can_stand(Vector2(Geometry.DIRS[side])*181*step/100.0,view.layout,view.props,view.edges),"Anomaly route to supported socket")
		for i in range(view.props.size()):
			var prop: Dictionary=view.props[i]
			var front:=Vector2(prop.rect.get_center().x,prop.rect.end.y+8)
			expect(Rect2(-180,-180,360,360).encloses(Rect2(front-Vector2(22,1),Vector2(44,2))),"Anomaly service line contained")
			for j in range(i): expect(not view.prop_visual_bounds(prop).intersects(view.prop_visual_bounds(view.props[j])),"Anomaly assemblies do not overlap")
			for step in range(90):
				for mark in view.effect_marks(prop,step/30.0):
					for p in mark: expect(view.effect_region(prop).has_point(p),"Anomaly effect stays on active surface")
			for shape in view.aperture_polygons(prop):
				for p in shape: expect(Geometry2D.is_point_in_polygon(p,PackedVector2Array(prop.registration.outline)),"Anomaly cover stays on host")
		for state in [{"name":"powered","power":10,"suspended":false,"active":true},{"name":"power-starved","power":0,"suspended":false,"active":false},{"name":"suspended","power":10,"suspended":true,"active":false}]:
			game.resources.power=state.power
			game.occupied[cell].suspended=state.suspended
			game._apply_room_economy()
			game.grid_view.room_light_levels.clear()
			expect(game.powered_room_cells.has(cell)==state.active,"Anomaly operation: "+state.name)
			expect(game.grid_view._room_light_target(game.occupied[cell])==(1.0 if state.active else 0.0),"Anomaly power/suspension lighting")
			game._refresh_all()
			game.visual_time_seconds=0.2
			await capture("anomaly-economy-q%d-%s-a"%[q,state.name])
			var before: Array=[]
			for prop in view.props: before.append(machine_pixels(cell,prop))
			game.visual_time_seconds=1.1
			await capture("anomaly-economy-q%d-%s-b"%[q,state.name])
			for i in range(view.props.size()): expect((before[i]!=machine_pixels(cell,view.props[i]))==(state.active and view.is_animated_prop(view.props[i])),"Anomaly host motion: "+str(view.props[i].id))
		game.occupied[cell].suspended=false
	print("ANOMALY ECONOMY/TOPOLOGY: four rotations, three actual states, four hosts, apertures, surface envelopes and 404 socket samples")
	print("ANOMALY MEASUREMENT: host motion uses separate crew-free captures; normal review frames and final viewport retain original crew visibility")
