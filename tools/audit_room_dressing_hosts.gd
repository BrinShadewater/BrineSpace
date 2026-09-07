extends SceneTree
## Native resolved-host audit. No gameplay scene, saves, or image modification.
const Grid = preload("res://scripts/grid_canvas.gd")
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
const Database = preload("res://scripts/room_database.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	var failures: Array=[]
	var seen: Dictionary={}
	var profiles:=0
	var references:=0
	var mat_bounds: Array=[]
	var baked_profiles: Array=[]
	var check_mats: bool="--check-mat-bounds" in OS.get_cmdline_user_args()
	var helper_names: Dictionary={}
	var negative_helper := ""
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--negative-helper="): negative_helper=argument.trim_prefix("--negative-helper=")
	var negative: bool="--negative-missing-host" in OS.get_cmdline_user_args()
	var grid = Grid.new()
	grid.hide()
	grid.process_mode = Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var catalog: Dictionary = Database.all_rooms()
	if "--negative-unmapped-room" in OS.get_cmdline_user_args():
		catalog["__unmapped_room_negative_control__"] = {"id":"__unmapped_room_negative_control__"}
	var procedural: Array = []
	var entries: Array = []
	for id in catalog:
		if grid._is_narrow_corridor(catalog[id]):
			procedural.append(id)
			continue
		entries.append(catalog[id])
	# Resolve the same room instance the station uses, not a batch-manifest subset.
	for entry in entries:
			var room = grid._bill_room_view(entry)
			if room == null:
				failures.append("%s: no runtime view" % entry.id)
				continue
			var view_path: String=room.get_script().resource_path
			if seen.has(view_path):
				failures.append("%s: shared/fallback view %s (already used by %s)" % [entry.id,view_path,seen[view_path]])
				continue
			seen[view_path]=entry.id
			for property in room.get_property_list():
				if not (property.usage & PROPERTY_USAGE_SCRIPT_VARIABLE): continue
				var helper=room.get(property.name)
				if not (helper is Object) or not is_instance_valid(helper): continue
				if helper.get_script()!=Dressing: continue
				helper_names[entry.id+":"+str(property.name)]=true
				profiles+=1
				for q in range(4):
					room.configure_embedded(q,[],false,0.0)
					# These three q0 renderers explicitly suppress dressing.floor()
					# and substitute baked perimeter slices for registered furniture.
					# Their other rotations still exercise every authored host below.
					if q==0 and entry.id in ["pressure_control","listening_post","isolation_vault"] and property.name=="dressing" and not room.props.is_empty() and room.props.all(func(prop): return prop.has("flush_region")):
						baked_profiles.append(entry.id+" q0: baked perimeter, dressing suppressed")
						continue
					var hosts: Dictionary={}
					for prop in room.props: hosts[str(prop.id)]=true
					var refs: Array=[]
					var profile: Dictionary=helper.profile
					if "--negative-surface-host" in OS.get_cmdline_user_args() and profiles==1 and q==0:
						profile=profile.duplicate(true)
						profile["surface_routes"]=[{"from":{"host":"__missing_surface_host__"},"to":{"host":"__missing_surface_host__"}}]
					if check_mats:
						for mat in profile.get("mats",[]):
							var host: Dictionary=helper.find_prop(mat.host)
							if host.is_empty(): continue # Existing host gate reports this below.
							var pad:=Rect2(host.rect.position+Vector2(mat.offset[0],mat.offset[1]),Vector2(mat.size[0],mat.size[1]))
							var inside:=Rect2(-180,-180,360,360).encloses(pad)
							mat_bounds.append({"room":entry.id,"helper":str(property.name),"quarter":q,"host":mat.host,"rect":[pad.position.x,pad.position.y,pad.size.x,pad.size.y],"inside":inside})
							if not inside: failures.append("%s/%s q%d: mat for %s outside interior %s"%[entry.id,property.name,q,mat.host,pad])
					for item in profile.get("furniture",[]): refs.append(str(item.id))
					for category in ["mats","supported"]:
						for item in profile.get(category,[]): refs.append(str(item.host))
					for route in profile.get("routes",[])+profile.get("surface_routes",[]):
						refs.append(str(route.from.host))
						refs.append(str(route.to.host))
					if q==0 and ((negative and profiles==1) or property.name==negative_helper): refs.append("__missing_host_negative_control__")
					for host in refs:
						references+=1
						if not hosts.has(host): failures.append("%s q%d: missing host %s"%[entry.id,q,host])
	grid.free()
	if check_mats: print("MAT BOUNDS RECORDS: "+JSON.stringify(mat_bounds))
	print("BAKED PROFILE EXCEPTIONS: "+JSON.stringify(baked_profiles))
	print(JSON.stringify({"scope":"Live catalog runtime views; resolved furniture, mat, supported-object and route host identities for every live Dressing instance in four native rotations; procedural corridors have no dressing profiles; not pixel or export acceptance","catalog_rooms":catalog.size(),"procedural_rooms":procedural,"views":seen.size(),"view_owners":seen,"profiles":profiles,"helpers":helper_names.keys(),"references":references,"errors":failures},"\t"))
	quit(1 if not failures.is_empty() else 0)
