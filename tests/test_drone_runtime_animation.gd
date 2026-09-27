extends SceneTree
const Motion=preload("res://scripts/drone_animation.gd")
const Dock=preload("res://scripts/drone_dock.gd")
var failures:=0
func check(ok:bool,label:String) -> void:
	if not ok:failures+=1;push_error(label)
func _init() -> void:
	var count:=0
	for kind in ["construction","mining","salvage"]:
		var m:=Motion.catalog(kind)
		for id in m.states:
			var clip:Dictionary=m.states[id]
			check(FileAccess.file_exists(clip.atlas.path),id+" atlas exists")
			check(int(clip.frameCount)>0 and int(clip.atlas.columns)>0,id+" frame geometry")
			for layer in ["effectAtlas","cargoAtlas"]:
				if clip.has(layer):check(FileAccess.file_exists(clip[layer].path),id+" "+layer)
			count+=1
		for direction in Motion.HEADINGS:
			for phase in ["docked","launching","outbound","working","returning","docking"]:
				var d:Dictionary={"kind":kind,"phase":phase,"clock":2.0,"animation_started":0.0,"animation_phase":phase,"animation_heading":direction,"elapsed":.6,"cargo":{"metal":1},"job":"construct"}
				var sample:=Motion.sample(d)
				check(sample.frame>=0 and sample.frame<sample.clip.frameCount,kind+direction+phase)
				var saved:=d.duplicate(true)
				Motion.sample(d,false)
				check(saved==d,"render sampling does not mutate fleet")
		for component in Dock.record(kind).components.values():check(FileAccess.file_exists(component),"dock component")
		var blocked:Dictionary={"kind":kind,"phase":"docked","route_wait":true,"animation_heading":"east","cargo":{}}
		var saved_blocked:=blocked.duplicate(true)
		var paths:=Dock.required_paths(kind,blocked,true)
		check(paths.has(m.states.get("blocked-south",m.states["idle-south"]).atlas.path),kind+" dock prepares blocked south artwork instead of idle/east")
		check(blocked==saved_blocked,"dock preparation does not mutate fleet")
		var charging:=Dock.required_paths(kind,{"phase":"docked","battery":1.0},true)
		check(charging.has(m.states.get("charging-south",m.states["idle-south"]).atlas.path),kind+" dock prepares charging artwork")
		var away:=Dock.required_paths(kind,{"phase":"outbound"},true)
		check(not away.has(m.states["idle-south"].atlas.path),kind+" absent drone does not warm an idle animation")
		if kind=="salvage":
			var loaded:=Dock.required_paths(kind,{"phase":"docked","cargo":{"metal":1}},true)
			check(loaded.has(m.headings.south.cargoPose) and loaded.has(m.headings.south.closedPose),"loaded salvage dock prepares both cargo poses")
	check(Dock.pose({"phase":"launching","elapsed":1.2}).depth==1.0,"launch ends submerged")
	check(Dock.pose({"phase":"docking","elapsed":0.0}).depth==1.0,"return starts submerged")
	check(Dock.pose({"phase":"docking","elapsed":1.2}).depth==0.0,"return ends raised")
	for path in ["res://scripts/drone_animation.gd","res://scripts/drone_dock.gd","res://tests/test_drone_runtime_animation.gd","res://tools/review_drone_runtime.gd","res://tools/review_drone_gameplay.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var f:=FileAccess.open(path+".uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("DRONE RUNTIME: ",count," clips, 144 directional phase samples, dock boundaries; ",failures," failures")
	quit(failures)
