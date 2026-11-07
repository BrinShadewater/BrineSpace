extends SceneTree
const Repairs=preload("res://scripts/hull_repair.gd")
var reports := []
func _init(): call_deferred("run")
func run():
	for variant in range(3):
		var game=load("res://scenes/main.tscn").instantiate()
		game.meta.save_path="user://flood-balance-%d-%d.meta" % [OS.get_process_id(),variant]
		game.run_save_path=game.meta.save_path+".loop"
		root.add_child(game)
		current_scene=game
		game.set_process(false)
		game.tick_timer.stop()
		game.crew_comms.set_process(false)
		game.paused=false
		var room: Dictionary=game.occupied[Vector2i(20,20)]
		var actor=game.bill_npc
		var cycle_clock := 0.0
		# Real startup, supplies, economy, failure conditions, pumps and paid repair.
		for i in range(110): game._process(0.1)
		cycle_clock=11.0
		room.hull_crack=Repairs.SEVERITIES[variant]
		var start_metal: int=game.resources.metal
		var requested := false
		var sealed_at := -1.0
		var water_at_seal := 0.0
		var peak := 0.0
		for i in range(900):
			var time := i*0.1
			if i==50: requested=Repairs.request(game,room.pos)
			game._process(0.1)
			cycle_clock+=0.1
			if cycle_clock>=game.tick_timer.wait_time:
				cycle_clock=0
				game._on_tick_timer_timeout()
				game.tick_timer.stop()
			peak=maxf(peak,float(room.get("water_level",0)))
			if float(room.hull_crack)==0 and sealed_at<0:
				sealed_at=time
				water_at_seal=room.water_level
			if actor.dead or not game.running or (sealed_at>=0 and time-sealed_at>=10): break
		reports.append({"profile":Repairs.NAMES[variant],"requested":requested,"sealed_seconds":sealed_at,"peak_water":peak,"crew_alive":not actor.dead,"run_active":game.running,"metal_start":start_metal,"metal_end":game.resources.metal,"water_at_seal":water_at_seal,"water_end":room.get("water_level",0),"repair_status":room.get("leak_repair",{}).get("status",""),"status":actor.activity,"free_build":game.testing_free_build})
		game.queue_free()
		await process_frame
	FileAccess.open("res://output/flood-balance.json",FileAccess.WRITE).store_string(JSON.stringify(reports,"	"))
	print("FLOOD BALANCE ",JSON.stringify(reports))
	quit()
