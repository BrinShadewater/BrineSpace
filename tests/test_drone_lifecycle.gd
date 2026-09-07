extends SceneTree
const Fleet = preload("res://scripts/drone_fleet.gd")
const Field = preload("res://scripts/wreck_field.gd")
var failures := 0
func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		push_error(label)
func _init() -> void:
	for kind in ["mining","salvage"]:
		var fleet = Fleet.new()
		var home := Vector2i(20,20)
		var target := Vector2i(20,21)
		var rooms: Array = [{"id":kind+"_drone_bay","pos":home}]
		var field := {target:{"kind":"basalt" if kind=="mining" else "engineering","progress":0.0,"active":true,"cleared":false}}
		var phases := {}
		var completed := 0
		for frame in range(420):
			fleet.advance(0.1,rooms,{home:true},field)
			completed += Field.advance(field,{home:true},0.1,fleet.clearance_seconds).size()
			var drone: Dictionary = fleet.drones[home]
			phases[drone.phase] = true
			if frame%13==0:
				var saved: Dictionary = fleet.snapshot()
				var progress: float = field[target].progress
				fleet.advance(0.0,rooms,{},field)
				Field.advance(field,{home:true},0.0,fleet.clearance_seconds)
				check(fleet.snapshot()==saved and field[target].progress==progress,kind+" zero simulation time freezes state and work")
				check(Fleet.valid(saved,rooms),kind+" every saved phase validates")
				var restored = Fleet.new()
				restored.restore(saved)
				check(restored.snapshot()==saved,kind+" every phase restores exactly")
		check(completed==1 and field[target].cleared,kind+" completes clearance exactly once with small steps")
		for phase in ["docked","launching","outbound","working","returning","docking"]: check(phases.has(phase),kind+" visits "+phase)
		# User pauses a job after arrival; the drone returns without resetting cuts.
		fleet.restore(null)
		field[target] = {"kind":"basalt" if kind=="mining" else "engineering","progress":0.0,"active":true,"cleared":false}
		fleet.advance(6.0,rooms,{home:true},field)
		Field.advance(field,{home:true},6.0,fleet.clearance_seconds)
		var retained: float = field[target].progress
		field[target].active = false
		fleet.advance(0.1,rooms,{home:true},field)
		check(fleet.drones[home].phase=="returning",kind+" interrupted work returns home")
		Field.advance(field,{home:true},0.1,fleet.clearance_seconds)
		check(field[target].progress==retained,kind+" job pause retains cuts")
		# Build orders can reclaim a harvest ground; workers move away.
		fleet.restore(null)
		fleet.advance(6.0,rooms,{home:true},{})
		var site: Vector2i = Vector2i(fleet.drones[home].target)
		fleet.enqueue("corridor",site,0)
		fleet.advance(0.1,rooms,{home:true},{})
		check(fleet.drones[home].phase=="returning",kind+" vacates a reserved construction site")
		fleet.advance(20.0,rooms,{home:true},{})
		check(Vector2i(fleet.drones[home].target)!=site,kind+" next harvest avoids reserved site")
	var builders = Fleet.new()
	var rooms: Array = [{"id":"brine_core","pos":Vector2i(20,20)},{"id":"construction_drone_bay","pos":Vector2i(20,21)}]
	builders.enqueue("corridor",Vector2i(20,22),1)
	builders.advance(0.1,rooms,{Vector2i(20,21):true},{})
	check(builders.drones[Vector2i(20,20)].order.is_empty(),"Dedicated powered builder receives first order")
	check(not builders.drones[Vector2i(20,21)].order.is_empty(),"Dedicated bay owns paid order")
	var saved: Dictionary = builders.snapshot()
	builders.advance(4.0,rooms,{}, {})
	check(builders.drones[Vector2i(20,21)]==saved.drones[Vector2i(20,21)],"Offline builder retains order without teleporting it to Core")
	check(builders.advance(30.0,rooms,{Vector2i(20,21):true},{}).size()==1,"Restored power completes construction once")
	print("DRONE LIFECYCLE %s: both clearance kinds, all phases, suspension, return, small steps, saves, site reclamation and dedicated builder" % ("PASS" if failures==0 else "FAIL"))
	quit(0 if failures==0 else 1)
