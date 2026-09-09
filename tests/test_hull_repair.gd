extends SceneTree
const Repairs=preload("res://scripts/hull_repair.gd")
const Flood=preload("res://scripts/room_flooding.gd")
const Save=preload("res://scripts/run_save.gd")
var failures := 0
var game
func check(ok: bool,message: String):
	if not ok: failures+=1; push_error(message)
func _init(): call_deferred("run")
func capture(label: String):
	if DisplayServer.get_name()=="headless": return
	game._set_grid_zoom(0.8,true,(Vector2(20,20)+Vector2.ONE*0.5)/40.0)
	game.selected_card_id=""
	game.selected_room_cell=Vector2i(20,20)
	preload("res://scripts/flood_alerts.gd").refresh(game)
	game._refresh_all()
	for i in range(5): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/hull-"+label+".png")
func run():
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://hull-repair-%d.meta" % OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.set_process(false)
	game.paused=false
	preload("res://scripts/architects.gd").advance_core(game,10)
	game.hardware.pumps=false
	game.hardware.doors=false
	game.resources.metal=20
	var cell := Vector2i(20,20)
	var room: Dictionary=game.occupied[cell]
	room.hull_crack=0.2
	room.water_level=0.1
	check(Repairs.request(game,cell),"Repair order accepted")
	check(game.resources.metal==18 and room.hull_crack==0.2,"Reserve metal without remote sealing")
	check(not Repairs.request(game,cell) and game.resources.metal==18,"Duplicate order cannot double charge")
	var actor=game.bill_npc
	var start: Vector2=actor.foot
	for i in range(1200):
		game._update_test_walker(0.1)
		if float(room.leak_repair.progress)>0.5: break
	check(float(room.leak_repair.progress)>0.5,"Crew reaches and works on physical leak")
	check(actor.foot.distance_to(start)>10 and actor.foot.distance_to(room.leak_repair.point)<1,"Repair requires walking to work point")
	check(actor.state=="weld","Dry crew uses authored blowtorch animation")
	check(actor.valid_snapshot(actor.snapshot()),"Hull welding snapshot validates")
	await capture("repair-torch")
	var progress: float=room.leak_repair.progress
	game.paused=true
	Repairs.advance(game,actor,1)
	check(room.leak_repair.progress==progress,"Pause holds repair")
	game.paused=false
	check(Save.write(game,game.run_save_path)==OK,"Repair writes disk checkpoint")
	var saved:=Save.read(game.run_save_path)
	check(not saved.is_empty(),"Paid repair checkpoint validates")
	actor.die()
	game._update_test_walker(1)
	check(room.hull_crack>0 and room.leak_repair.progress==progress,"Death cannot seal damage")
	if saved.is_empty(): quit(1); return
	check(Save.restore(game,saved),"Repair checkpoint restores")
	game.set_process(false)
	game.tick_timer.stop()
	game.paused=false
	room=game.occupied[cell]
	check(room.leak_repair.progress==progress and game.resources.metal==18,"Partial work and paid metal persist")
	for i in range(600):
		game._update_test_walker(0.1)
		if not room.has("leak_repair"): break
	check(room.hull_crack==0 and not room.has("leak_repair"),"Completed torch work seals damage")
	check(room.water_level>0.1 and game.resources.metal==18,"Existing water remains; no second charge")
	var water: float=room.water_level
	Flood.step_water(game,1)
	check(is_equal_approx(room.water_level,water),"Repaired hull stops inflow")
	var repair_foot: Vector2=game.bill_npc.foot
	for i in range(3):
		room.hull_crack=Repairs.SEVERITIES[i]
		room.water_level=0
		Flood.step_water(game,0.1)
		check(is_equal_approx(room.water_level,Repairs.SEVERITIES[i]*0.004),"Variant leak rate")
		check(Repairs.variant(room)==i,"Variant severity classification")
		room.water_level=0.35
		game.bill_npc.foot=(Vector2(cell)+Vector2.ONE*0.5)*384+Vector2(-85,105)
		await capture("variant-%d" % i)
	game.bill_npc.foot=repair_foot
	game.resources.metal=20
	actor=game.bill_npc
	actor.helmet_equipped=true
	actor.tank_oxygen=60
	room.water_level=0.9
	check(Repairs.request(game,cell),"Helmeted crew can take critical-water rupture repair")
	for i in range(500):
		game._update_test_walker(0.1)
		if room.has("leak_repair") and float(room.leak_repair.progress)>=1:
			await capture("repair-underwater")
			break
	print("UNDERWATER REPAIR ",actor.activity," / ",actor.state," / ",actor.foot," / ",room.get("leak_repair",{}))
	check(not actor.dead and actor.state=="repair" and actor.movement_medium=="flooded","Submerged repair uses swimming hold with active torch")
	for i in range(500):
		game._update_test_walker(0.1)
		if not room.has("leak_repair"): break
	check(room.hull_crack==0 and not actor.dead and actor.tank_oxygen<60,"Helmeted rupture repair completes while using oxygen")
	room.hull_crack=1
	game.resources.metal=0
	check(not Repairs.request(game,cell),"Insufficient metal refuses repair")
	check(not Repairs.valid({"cost":2,"duration":6.0,"progress":NAN,"worker":""}),"Corrupt saved progress rejected")
	game.resources.metal=20
	room.water_level=0.95
	actor.helmet_equipped=false
	actor.breath_oxygen=15
	check(Repairs.request(game,cell),"Unsafe repair can be queued for later prepared crew")
	Repairs.advance(game,actor,0.1)
	check(room.leak_repair.progress==0 and str(room.leak_repair.status).begins_with("Unsafe"),"Insufficient air blocks starting rupture work")
	await capture("safety-controls")
	check(Repairs.reassign(game,cell,"bill") and room.leak_repair.preferred=="bill","Owner can assign a crew member without new charge")
	check(Repairs.cancel(game,cell) and game.resources.metal==20 and room.hull_crack>0,"Unstarted cancellation refunds all metal and leaves leak")
	Repairs.request(game,cell)
	room.leak_repair.progress=8.0
	check(Repairs.cancel(game,cell) and game.resources.metal==17,"Partial cancellation refunds only unused whole Metal")
	preload("res://scripts/flood_alerts.gd").refresh(game)
	check(game.flood_alert_button.text.contains("1 CRITICAL"),"Station flood alert exposes critical room")
	check(game.flood_alert_button.get_meta("target")==cell,"Flood alert locates critical room")
	var warned: Dictionary=game.flood_alert_button.get_meta("stages")
	room.water_level=0.849
	preload("res://scripts/flood_alerts.gd").refresh(game)
	check(game.flood_alert_button.get_meta("stages")[cell]==3,"Alert hysteresis avoids boundary spam")
	actor.breath_oxygen=6
	actor.helmet_equipped=false
	actor.set_meta("flood_safety_wait",0.0)
	room.water_level=0.95
	check(preload("res://scripts/flood_safety.gd").advance(game,actor,0.1) and actor.activity.contains("escape path blocked"),"No refuge produces explicit low-air blockage instead of imaginary escape")
	room.hull_crack=0
	room.water_level=0
	preload("res://scripts/flood_alerts.gd").refresh(game)
	check(game.flood_alert_button.text=="FLOOD / CLEAR","Alert clears when station is dry")
	print("HULL REPAIR ","PASS" if failures==0 else "FAIL")
	DirAccess.remove_absolute(game.run_save_path)
	DirAccess.remove_absolute(game.meta.save_path)
	quit(0 if failures==0 else 1)
