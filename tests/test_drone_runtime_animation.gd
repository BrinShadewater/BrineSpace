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
	var empty_path:="res://assets/mining-rover-v1-2026-09-26/completion/atlases/empty-120.png"
	# Scene/Studio teardown consumes completed worker results directly. Preserve
	# the decoder's transparency classification just like finish_texture does.
	Motion.request_texture(empty_path)
	var queued_visible_path:String=Dock.record("construction").components["water-pad"]
	Motion.request_texture(queued_visible_path)
	Dock.finish_pending_jobs()
	check(Motion.image_jobs.is_empty(),"Teardown drains all image tasks")
	check(Motion.texture_bytes[empty_path]==4 and Motion.textures[empty_path].get_meta("drone_invisible",false),"Teardown keeps fully transparent atlas collapsed")
	var source_image:=Image.new()
	check(source_image.load_png_from_buffer(FileAccess.get_file_as_bytes(queued_visible_path))==OK,"Visible teardown reference loads")
	check(Motion.textures[queued_visible_path].get_image().get_data()==source_image.get_data(),"Teardown preserves every visible source pixel")
	var empty_texture:=Motion.texture(empty_path)
	check(empty_texture.get_size()==Vector2(1,1) and Motion.texture_bytes[empty_path]==4,"Transparent 92 MiB atlas uses one RGBA pixel")
	check(empty_texture.get_meta("drone_invisible",false),"Transparent atlas stays invisible")
	var visible_texture:=Motion.texture(Dock.record("construction").components["water-pad"])
	check(not visible_texture.get_meta("drone_invisible",false) and visible_texture.get_width()>1,"Visible dock artwork keeps its original pixels")
	var order_before := Motion.texture_order.duplicate()
	var bytes_before := Motion.cached_bytes
	var old_use: int = Motion.last_used[empty_path]
	Motion.last_used[empty_path] = Engine.get_process_frames() - 5
	var cache_report := Motion.cache_diagnostics()
	check(cache_report.classification_complete and cache_report.stale_decoded_bytes == 4, "Cache report classifies an aged transparent allocation")
	check(cache_report.recent_decoded_bytes + cache_report.stale_decoded_bytes == bytes_before, "Cache report accounts for every tracked byte")
	check(Motion.cached_bytes == bytes_before and Motion.texture_order == order_before and Motion.textures.has(empty_path), "Cache report never evicts or changes recency")
	var monitor := preload("res://scripts/performance_monitor.gd").new()
	check(monitor.snapshot().drone_texture_cache == cache_report, "Performance report includes the same cache accounting")
	monitor.free()
	Motion.last_used[empty_path] = old_use
	check(Dock.pose({"phase":"launching","elapsed":1.2}).depth==1.0,"launch ends submerged")
	check(Dock.pose({"phase":"docking","elapsed":0.0}).depth==1.0,"return starts submerged")
	check(Dock.pose({"phase":"docking","elapsed":1.2}).depth==0.0,"return ends raised")
	# Resource UIDs belong to the source checkout; exported packs are read-only.
	print("DRONE RUNTIME: ",count," clips, 144 directional phase samples, dock boundaries; ",failures," failures")
	quit(failures)
