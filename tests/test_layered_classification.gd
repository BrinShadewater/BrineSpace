extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const Database=preload("res://scripts/room_database.gd")
class Reference extends GridCanvas:
	func _uses_layered_art(room: Dictionary) -> bool:
		if ExpansionViews.PATHS.has(room.get("id","")): return true
		if room.get("id","") in ["observation_room","salvage_workshop","galley","cold_store"]: return true
		if room.get("id","")=="airlock": return true
		return room.get("id", "") in ["current_turbine", "biomass_digester", "heat_recovery", "construction_drone_bay", "mycelium_nursery", "life_support", "hydroponics_bay", "reactor", "med_bay", "crew_hab", "cryo_chamber", "clone_lab", "data_archive", "biodome", "xeno_lab", "med_office","med_center","holographic_core","bio_lab","anomaly_lab", "battery_array", "research_lab", "maintenance_bay", "storage_bay", "ore_refinery", "mining_drone_bay", "salvage_drone_bay", "crew_lounge", "command_center", "quarantine_cell", "solar_array", "radio_lab", "shield_generator", "tidal_condenser", "gravity_loom", "brine_core", "corridor", "corner", "tee_corridor", "pressure_control", "listening_post", "isolation_vault"]

var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	var candidate=Grid.new();var reference=Reference.new();var cases:Array=[{}, {"id":""}, {"id":"unknown"}, {"id":null}]
	for id in Database.all_rooms():
		for rotation in range(4):cases.append({"id":id,"rotation":rotation})
	for id in Grid.ExpansionViews.PATHS:cases.append({"id":id})
	for id in ["airlock","corridor","corner","tee_corridor","brine_core"]:cases.append({"id":StringName(id)})
	for room in cases:
		var original:Dictionary=room.duplicate(true)
		check(candidate._uses_layered_art(room)==reference._uses_layered_art(room),"Layer classification parity "+str(room))
		check(room==original,"Input immutable")
	var timings:Array=[]
	for pair in range(3):
		var stamp:=Time.get_ticks_usec();var old_count:=0
		for iteration in range(100):
			for room in cases:old_count+=int(reference._uses_layered_art(room))
		var old_usec:=Time.get_ticks_usec()-stamp;stamp=Time.get_ticks_usec();var new_count:=0
		for iteration in range(100):
			for room in cases:new_count+=int(candidate._uses_layered_art(room))
		var new_usec:=Time.get_ticks_usec()-stamp
		check(old_count==new_count,"Timed classification counts equal")
		timings.append({"old_usec":old_usec,"new_usec":new_usec,"calls":cases.size()*100})
	candidate.free();reference.free()
	FileAccess.open("user://layered.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"timings":timings}))
	print("LAYERED_CLASSIFICATION ",checks," checks; ",failures," failures ",timings);quit(1 if failures else 0)
