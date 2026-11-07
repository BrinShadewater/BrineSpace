extends SceneTree
const DB=preload("res://scripts/room_database.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	var grid=preload("res://scripts/grid_canvas.gd").new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var records: Array=[]
	for entry in DB.all_rooms().values():
		var row: Dictionary={"id":entry.id,"name":entry.display_name,"props":[]}
		if grid._is_narrow_corridor(entry):
			row["view"]="corridor"
		else:
			var room=grid._bill_room_view(entry)
			room.configure_embedded(0,[],false,0.0)
			row["view"]=room.get_script().resource_path
			row["floor_owner"]=""
			var script: Script=room.get_script()
			while script!=null:
				if script.source_code.contains("func draw_room_floor("):
					row.floor_owner=script.resource_path
					break
				script=script.get_base_script()
			for prop in room.props:
				var rect: Rect2=prop.rect
				var visual: Rect2=room.prop_visual_bounds(prop)
				row.props.append({"id":str(prop.id),"rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"visual":[visual.position.x,visual.position.y,visual.size.x,visual.size.y]})
		if row.view!="corridor":
			row["rotations"]=[]
			var room=grid._bill_room_view(entry)
			for q in range(4):
				room.configure_embedded(q,[],false,0.0)
				var props: Array=[]
				for prop in room.props:
					var rect: Rect2=prop.rect
					var visual: Rect2=room.prop_visual_bounds(prop)
					props.append({"id":str(prop.id),"rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"visual":[visual.position.x,visual.position.y,visual.size.x,visual.size.y]})
				row.rotations.append({"q":q,"props":props})
		records.append(row)
	DirAccess.make_dir_recursive_absolute("res://output/floor-coverage")
	var out:=FileAccess.open("res://output/floor-coverage/runtime.json",FileAccess.WRITE)
	out.store_string(JSON.stringify(records,"	"))
	print("FLOOR COVERAGE: ",records.size()," live identities and actual machinery footprints")
	quit()
