extends SceneTree
const Flood = preload("res://scripts/room_flooding.gd")
const Save = preload("res://scripts/run_save.gd")
var failures := 0
func check(ok: bool,message: String):
	if not ok:
		failures+=1
		push_error(message)
func _init(): call_deferred("run")
func run():
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://flood-review-%d.meta" % OS.get_process_id()
	game.run_save_path="user://flood-review-%d.loop" % OS.get_process_id()
	game.meta.selected_architect="bill"
	root.add_child(game)
	current_scene=game
	game.crew_comms.opening_enabled=false
	game.crew_comms.set_process(false)
	game.set_process(false)
	game.tick_timer.stop()
	game.paused=false
	preload("res://scripts/architects.gd").advance_core(game,10.0)
	check(preload("res://scripts/architects.gd").present(game,"bill"),"Visible architect released before staging flood")
	var cell := Vector2i(20,20)
	var room: Dictionary = game.occupied[cell]
	game.selected_card_id=""
	game.selected_room_cell=cell
	game.hardware.pumps=false
	var actor = game.bill_npc
	actor.helmet_equipped=true
	actor.tank_oxygen=37.25
	actor.breath_oxygen=8.5
	actor.starvation=12.0
	room.water_level=0.62
	room.hull_crack=0.7
	check(Save.write(game,game.run_save_path)==OK,"Flood checkpoint writes to disk")
	var loaded := Save.read(game.run_save_path)
	check(not loaded.is_empty(),"Flood checkpoint validates from disk")
	check(Save.restore(game,loaded),"Flood checkpoint restores")
	game.set_process(false)
	game.tick_timer.stop()
	game.paused=false
	room=game.occupied[cell]
	actor=game.bill_npc
	check(is_equal_approx(room.water_level,0.62) and is_equal_approx(room.hull_crack,0.7),"Room water and leak persist")
	check(actor.tank_oxygen==37.25 and actor.breath_oxygen==8.5 and actor.starvation==12.0,"Individual survival clocks persist")
	actor.helmet_equipped=false
	actor.path.clear()
	actor.stage=""
	actor.state="idle"
	game._set_grid_zoom(0.8,true,(Vector2(cell)+Vector2.ONE*0.5)/40.0)
	for water in [0.12,0.35,0.65,0.93]:
		room.water_level=water
		actor.foot=(Vector2(cell)+Vector2.ONE*0.5)*384+Vector2(-85,105)
		actor.path=PackedVector2Array([actor.foot+Vector2(40,0)])
		actor.state="walk"
		game._update_test_walker(0.01)
		game._refresh_all()
		for frame in range(5): await process_frame
		if DisplayServer.get_name()!="headless":
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/flood-stage-%d.png" % roundi(water*100))
	print("FLOOD SAVE / NATIVE ","PASS" if failures==0 else "FAIL")
	DirAccess.remove_absolute(game.run_save_path)
	DirAccess.remove_absolute(game.meta.save_path)
	quit(0 if failures==0 else 1)
