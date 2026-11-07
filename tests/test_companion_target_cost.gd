extends SceneTree
# October 20 pre-optimization target oracle plus local CPU measurements.
# Timing is diagnostic, not an FPS, rendering or frame-pacing acceptance gate.
const Assist=preload("res://scripts/companion_repair.gd")
const Fixture=preload("res://tests/test_companion_repair.gd")
const Rooms=preload("res://scripts/room_database.gd")
var failures:=0
var checks:=0
func _init():run.call_deferred()
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	var game=Fixture.Game.new()
	var josh=Fixture.JoshFixture.new()
	var rng=RandomNumberGenerator.new();rng.seed=20261020
	for i in range(500):
		game.occupied.clear()
		game.paused=i%17==0;game.hardware.doors=i%19==0
		for worker in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:
			worker.active=rng.randf()>.2;worker.dead=rng.randf()<.1
			worker.goal="hull-repair" if rng.randf()>.5 else "ward-repair"
			worker.state="weld" if rng.randf()>.3 else "idle"
			worker.expedition={} if rng.randf()>.2 else {"test":true}
		for k in range(40):
			var room={"water_level":.5 if rng.randf()<.1 else 0.0,"suspended":rng.randf()<.1}
			if rng.randf()<.3:room.leak_repair={"worker":["bill","veld","branforth","marsh"][rng.randi_range(0,3)],"point":Vector2(200,200) if rng.randf()>.2 else Vector2(900,900)}
			game.occupied[Vector2i(k,0)]=room
		josh.foot=Vector2(260,200);josh.interest_cell=Vector2i(rng.randi_range(-1,39),0)
		check(Assist.target(game,josh)==reference_target(game,josh),"Target parity across changing worker, job and room states")
	game.paused=false;game.hardware.doors=false
	for worker in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:
		worker.active=true;worker.dead=false;worker.goal="";worker.state="idle";worker.expedition={}
	for count in [40,200]:
		game.occupied.clear()
		for i in range(count):game.occupied[Vector2i(i%40,i/40)]={}
		for mode in ["idle","active-hull"]:
			game.bill_npc.goal="hull-repair" if mode=="active-hull" else ""
			game.bill_npc.state="weld" if mode=="active-hull" else "idle"
			# Worst active search with no valid room job; keeps scanning fallback exercised.
			for order in [false,true]:
				var times:Dictionary={}
				for candidate in ([false,true] if not order else [true,false]):
					var started:=Time.get_ticks_usec()
					for i in range(4000):
						if candidate:Assist.target(game,josh)
						else:reference_target(game,josh)
					times["candidate" if candidate else "baseline"]=float(Time.get_ticks_usec()-started)/4000.0
				print("TARGET_USEC rooms=",count," mode=",mode," reverse=",order," ",times)
	# Display-name fast path must retain fallback semantics for sparse test rooms.
	for neighbor in [{"id":"hydroponics_bay","display_name":"Custom name"},{"id":"hydroponics_bay"},{"id":"missing"},{"id":"hydroponics_bay","display_name":""}]:
		check(old_name(neighbor)==new_name(neighbor),"Display name parity")
	var neighbor={"id":"hydroponics_bay","display_name":"Hydroponics Bay"}
	for reverse in [false,true]:
		var times:Dictionary={}
		for candidate in ([false,true] if not reverse else [true,false]):
			var started:=Time.get_ticks_usec()
			for i in range(20000):
				if candidate:new_name(neighbor)
				else:old_name(neighbor)
			times["candidate" if candidate else "baseline"]=float(Time.get_ticks_usec()-started)/20000.0
		print("NAME_USEC reverse=",reverse," ",times)
	print("COMPANION TARGET COST checks=",checks," failures=",failures)
	quit(1 if failures else 0)
static func old_name(neighbor:Dictionary)->String:
	return str(neighbor.get("display_name",Rooms.get_room(str(neighbor.id)).get("display_name",neighbor.id)))
static func new_name(neighbor:Dictionary)->String:
	return str(neighbor.display_name) if neighbor.has("display_name") else str(Rooms.get_room(str(neighbor.id)).get("display_name",neighbor.id))
static func reference_target(game, josh) -> Dictionary:
	if not game.running or game.paused or game.hardware.doors:return {}
	var cells: Array=game.occupied.keys()
	if cells.has(josh.interest_cell):
		cells.erase(josh.interest_cell);cells.push_front(josh.interest_cell)
	for cell in cells:
		var room: Dictionary=game.occupied[cell]
		if float(room.get("water_level",0))>=0.5 or room.get("suspended",false):continue
		var job: Dictionary=room.get("leak_repair",{})
		if job.is_empty() or str(job.get("worker","")).is_empty() or not job.has("point"):continue
		var worker=game.Architects.actor_for(game,job.worker)
		if worker==null or not worker.active or worker.dead or worker.goal!="hull-repair" or worker.state!="weld":continue
		if not worker.expedition.is_empty() or worker.foot.distance_to(job.point)>2:continue
		if josh.foot.distance_to(job.point)>384:continue
		return {"cell":cell,"point":job.point}
	return Assist.ward_target(game,josh)
