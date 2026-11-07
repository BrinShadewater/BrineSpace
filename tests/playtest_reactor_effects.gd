extends "res://tests/playtest_underwater_life_support.gd"
## Reactor-only renderer-state and production pause-clock evidence.
## The inherited harness isolates saves/input. This is not an economy or crew test.
class FrozenChamber extends "res://rooms/whole-room/reactor_view.gd":
	func draw_registered_prop(prop: Dictionary) -> void:
		var saved: float=machine_clock
		if prop.id=="reactor_chamber": machine_clock=0.2
		super.draw_registered_prop(prop)
		machine_clock=saved

func evidence_subject() -> String: return "reactor-effects"
func subject_view(): return game.grid_view.reactor_view

func verify_motion_and_routes() -> void:
	subject_id="reactor"
	var cell:=Vector2i(20,20)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.unpowered_room_cells.clear()
	game._place_room(subject_id,cell,true)
	game.test_walker_cell=Vector2i(-1,-1)
	game.test_walker_next_cell=Vector2i(-1,-1)
	# Keep these measurement frames explicitly crew-free, not depth evidence.
	var crew: Array=[game.bill_npc,game.veld_npc,game.branforth_npc]
	var prior_active: Array=[]
	for npc in crew:
		prior_active.append(npc.active)
		npc.active=false
	if "--negative-frozen-reactor-chamber" in OS.get_cmdline_user_args():
		var frozen:=FrozenChamber.new()
		frozen.embedded=true
		frozen.hide()
		game.grid_view.add_child(frozen)
		game.grid_view.reactor_view=frozen
	game._refresh_all()
	await settle()
	game._fit_station_view()
	var records: Array=[]
	for q in range(4):
		game.occupied[cell].rotation=q
		for working in [true,false]:
			game.powered_room_cells.clear()
			if working: game.powered_room_cells[cell]=true
			game.grid_view.room_light_levels.clear()
			game.visual_time_seconds=0.2
			await capture("reactor-q%d-%s-a"%[q,"on" if working else "off"])
			var before: Dictionary={}
			for prop in subject_view().props: before[prop.id]=machine_pixels(cell,prop)
			game.visual_time_seconds=1.1
			await capture("reactor-q%d-%s-b"%[q,"on" if working else "off"])
			for prop in subject_view().props:
				var changed: bool=before[prop.id]!=machine_pixels(cell,prop)
				var expected: bool=working and prop.id in ["reactor_chamber","reactor_console"]
				expect(changed==expected,"Reactor q%d working=%s host=%s motion=%s expected=%s"%[q,working,prop.id,changed,expected])
				records.append({"quarter":q,"working":working,"host":prop.id,"changed":changed,"expected":expected})
		game.powered_room_cells[cell]=true
		game.grid_view.room_light_levels.clear()
		game.visual_time_seconds=0.2
		game._set_paused(true)
		await capture("reactor-q%d-paused-a"%q)
		var paused_bytes: Dictionary={}
		for prop in subject_view().props: paused_bytes[prop.id]=machine_pixels(cell,prop)
		game._process(0.9)
		expect(is_equal_approx(game.visual_time_seconds,0.2),"Reactor pause preserves production visual clock")
		await capture("reactor-q%d-paused-b"%q)
		for prop in subject_view().props:
			expect(paused_bytes[prop.id]==machine_pixels(cell,prop),"Reactor paused host remains still: "+str(prop.id))
		# Exercise the actual main clock, rather than advancing a detached room clock.
		game._set_paused(false)
		game._process(0.9)
		expect(game.visual_time_seconds>0.2,"Reactor resume advances production visual clock")
		game._set_paused(true)
		await capture("reactor-q%d-resumed"%q)
		for prop in subject_view().props:
			if prop.id in ["reactor_chamber","reactor_console"]:
				expect(paused_bytes[prop.id]!=machine_pixels(cell,prop),"Reactor host resumes: "+str(prop.id))
	for i in range(crew.size()): crew[i].active=prior_active[i]
	var record:=FileAccess.open(capture_dir.path_join("reactor-effects.json"),FileAccess.WRITE)
	record.store_string(JSON.stringify({"scope":"Four-rotation crew-free host crops; direct operation binding, actual main pause/resume clock; not economy, crew overlap or exported evidence","view_sha256":FileAccess.get_sha256("res://rooms/whole-room/reactor_view.gd"),"main_sha256":FileAccess.get_sha256("res://scripts/main.gd"),"crew_active_restored":prior_active,"comparisons":records,"failures":failures},"\t"))
	print("REACTOR EFFECTS: ",records.size()," host operation comparisons; four production-clock pause/resume pairs; crew-free measurements")
