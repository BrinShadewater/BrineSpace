extends SceneTree
## Read-only native views for rectangular mat-bound failures across the live catalog.
const Grid=preload("res://scripts/grid_canvas.gd")
const Database=preload("res://scripts/room_database.gd")
const Dressing=preload("res://rooms/whole-room/room_dressing.gd")
var output:=""
var selected_room:=""
class MatReviewPanel extends Node2D:
	var room
	var quarter:=0
	func _draw() -> void:
		draw_rect(Rect2(0,0,1100,1040),Color("17232c"))
		room.configure_embedded(quarter,[],false,0.2)
		room.render_into(self,Vector2(550,540),2.0)
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output=arg.trim_prefix("--output=")
		if arg.begins_with("--room="): selected_room=arg.trim_prefix("--room=")
	call_deferred("run")
func run() -> void:
	if not selected_room.is_empty() and not Database.all_rooms().has(selected_room):
		push_error("Unknown room selection")
		quit(1)
		return
	if not output.begins_with("res://output/") or output.contains("..") or DirAccess.dir_exists_absolute(output):
		push_error("Use a new output directory")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(output)
	root.size=Vector2i(1100,1040)
	root.content_scale_size=root.size
	var grid:=Grid.new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var panel:=MatReviewPanel.new()
	root.add_child(panel)
	var records: Array=[]
	for entry in Database.all_rooms().values():
		if not selected_room.is_empty() and entry.id!=selected_room: continue
		if grid._is_narrow_corridor(entry): continue
		var room=grid._bill_room_view(entry)
		for q in range(4):
			room.configure_embedded(q,[],false,0.2)
			var bad: Array=[]
			for property in room.get_property_list():
				if not (property.usage & PROPERTY_USAGE_SCRIPT_VARIABLE): continue
				var helper=room.get(property.name)
				if not (helper is Object) or not is_instance_valid(helper) or helper.get_script()!=Dressing: continue
				for mat in helper.profile.get("mats",[]):
					var host: Dictionary=helper.find_prop(mat.host)
					if host.is_empty(): continue
					var pad:=Rect2(host.rect.position+Vector2(mat.offset[0],mat.offset[1]),Vector2(mat.size[0],mat.size[1]))
					if not Rect2(-180,-180,360,360).encloses(pad): bad.append({"helper":property.name,"host":mat.host,"rect":[pad.position.x,pad.position.y,pad.size.x,pad.size.y]})
			if bad.is_empty() and selected_room.is_empty(): continue
			panel.room=room
			panel.quarter=q
			panel.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var name:="%s-q%d.png"%[entry.id,q]
			assert(root.get_texture().get_image().save_png(output.path_join(name))==OK)
			records.append({"room":entry.id,"quarter":q,"file":name,"flagged_mats":bad,"sha256":FileAccess.get_sha256(output.path_join(name))})
	var record:=FileAccess.open(output.path_join("mat-review.json"),FileAccess.WRITE)
	record.store_string(JSON.stringify({"scope":"Native sealed-room offline 2x mat-bound diagnostic; not runtime lighting, crew, route or aesthetic acceptance","captures":records},"\t"))
	print("MAT REVIEW CAPTURES: ",records.size())
	quit()
