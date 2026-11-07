extends SceneTree
const Floors=preload("res://rooms/whole-room/room_floor.gd")
const Details=preload("res://rooms/floor-profiles-v1/details.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	preload("res://scripts/room_layout_store.gd").loaded=true
	preload("res://scripts/room_layout_store.gd").data={}
	var grid=preload("res://scripts/grid_canvas.gd").new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var selected: PackedStringArray=[]
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--review-rooms="): selected=arg.trim_prefix("--review-rooms=").split(",")
	var records: Array=[]
	var missing:=0
	var count:=0
	for entry in preload("res://scripts/room_database.gd").all_rooms().values():
		if grid._is_narrow_corridor(entry): continue
		if not selected.is_empty() and entry.id not in selected: continue
		var view=grid._bill_room_view(entry)
		var profile:=Floors.profile_for(view)
		assert(not profile.is_empty(),"Every live room must have a profile")
		for q in range(4):
			view.configure_embedded(q,[],false,0.0)
			var result:=Details.resolve(view,profile)
			var bad:=profile.duplicate(true)
			bad.details=[{"asset":"detail-inspection_plug","hosts":["__missing_host_negative_control__"],"purpose":"negative control","scale":1.0}]
			assert(not Details.resolve(view,bad).missing.is_empty(),"Missing host must not reuse cached placements")
			result=Details.resolve(view,profile)
			assert(Details.resolve(view,profile)==result,"Stable geometry reuses the same placement result")
			for piece in result.pieces:
				if piece.asset=="detail-standing_mat":
					assert(not Details.floor_pads(view).any(func(pad): return str(pad.host)==str(piece.host)),"Do not duplicate authored workstation pads")
			for item in result.missing:
				print("MISSING ",entry.id," q",q," ",item)
			missing+=result.missing.size()
			count+=result.pieces.size()
			records.append({"id":entry.id,"q":q,"pieces":result.pieces,"missing":result.missing})
	var file:=FileAccess.open("res://output/floor-coverage/anchors-resolved.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"	"))
	print("FLOOR ANCHORS: ",count," placed; ",missing," missing; current hosts, floor containment, routes and piece spacing checked")
	quit(1 if missing else 0)
