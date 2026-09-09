extends SceneTree
## Read-only host study. Rectangular overlaps are not runtime collision proof.
const OUT := "res://output/seed-sections-relocation-study"
const ASSETS := ["res://assets/seed-sorting-west-section-v1/", "res://assets/seed-storage-west-section-v1/"]
class Board extends Node2D:
	var rooms: Array = []
	var entries: Array = []
	func _draw() -> void:
		draw_rect(Rect2(0,0,1000,560),Color("26363a"))
		draw_string(ThemeDB.fallback_font,Vector2(24,28),"Seed bank host study: all furniture retained; right panel tests relocation",HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		for i in range(2):
			var center := Vector2(250+i*500,295)
			rooms[i].render_into(self,center,1.0)
			draw_set_transform(Vector2.ZERO)
			for entry in entries:
				var target := Rect2(center+entry.rect.position,entry.rect.size)
				draw_texture_rect_region(entry.texture,target,entry.region)
				draw_rect(target,Color("ebaa64"),false,1.0)
			if i==1:
				draw_rect(Rect2(center+Vector2(-184,-36),Vector2(68,72)),Color(0.2,0.8,0.4,0.25))
			draw_string(ThemeDB.fallback_font,Vector2(35+i*500,535),"Current layout with seed overlay" if i==0 else "Relocation proposal / west door open",HORIZONTAL_ALIGNMENT_LEFT,-1,17)
		draw_string(ThemeDB.fallback_font,Vector2(24,555),"Visual overlay only; no room data changed, no crew or collision acceptance",HORIZONTAL_ALIGNMENT_LEFT,-1,15)
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	if FileAccess.file_exists(OUT+".png") or FileAccess.file_exists(OUT+".json"):
		push_error("Refuse to overwrite prior study"); quit(1); return
	root.size=Vector2i(1000,560)
	root.content_scale_size=root.size
	root.canvas_item_default_texture_filter=Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	preload("res://scripts/room_layout_store.gd").path="res://output/seed-sections-isolated-layouts.json"
	var board:=Board.new()
	var provenance: Array=[]
	for n in range(2):
		var asset: String=ASSETS[n]
		var reg=JSON.parse_string(FileAccess.get_file_as_string(asset+"registration.json"))
		var record=JSON.parse_string(FileAccess.get_file_as_string(asset+"material-scale-review.json"))
		if FileAccess.get_sha256(asset+"wall.png")!=record.export_sha256 or FileAccess.get_sha256(asset+"registration.json")!=record.registration_sha256:
			push_error("Stale export or registration"); quit(1); return
		var raw:=Image.new()
		if raw.load_png_from_buffer(FileAccess.get_file_as_bytes(asset+"wall.png"))!=OK:
			push_error("Cannot decode export"); quit(1); return
		var rect:=Rect2(-184,-184 if n==0 else 48,record.proposed_display_width_world,136)
		board.entries.append({"texture":ImageTexture.create_from_image(raw),"region":Rect2(reg.region[0],reg.region[1],reg.region[2],reg.region[3]),"rect":rect,"asset":asset})
		provenance.append({"asset":asset,"export_sha256":record.export_sha256,"registration_sha256":record.registration_sha256,"rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y]})
	var reports: Array=[]
	for i in range(2):
		var room=load("res://rooms/full-wall-v1/hydroponics_bay_view.gd").new()
		room.embedded=true
		room.hide()
		root.add_child(room)
		room.configure_embedded(0,[3],false,0.0)
		var shifts := {"full_wall_hydroponics-wall_crops":Vector2(68,0),"hydro_nutrients":Vector2(96,0),"hydro_harvest_stand":Vector2(96,0)}
		var inventory: Array=[]
		if i==1:
			for prop in room.props:
				if shifts.has(str(prop.id)):
					prop.rect.position+=shifts[str(prop.id)]
					prop.sort_y=prop.rect.end.y
		for prop in room.props:
			inventory.append({"id":str(prop.id),"rect":[prop.rect.position.x,prop.rect.position.y,prop.rect.size.x,prop.rect.size.y]})
		var moved_conflicts: Array=[]
		if i==1:
			for prop in room.props:
				if not shifts.has(str(prop.id)): continue
				for other in room.props:
					if prop.id!=other.id and room.prop_visual_bounds(prop).intersects(room.prop_visual_bounds(other)):
						moved_conflicts.append([str(prop.id),str(other.id)])
		var overlaps: Array=[]
		for entry in board.entries:
			var ids: Array=[]
			for prop in room.props:
				if entry.rect.intersects(prop.rect): ids.append(str(prop.id))
			overlaps.append({"asset":entry.asset,"rect_overlap_ids":ids,"door_bay_overlap":i==1 and entry.rect.intersects(Rect2(-184,-36,68,72))})
		reports.append({"open_sides":[3],"sections":overlaps,"inventory":inventory,"moved_visual_conflicts":moved_conflicts})
		board.rooms.append(room)
	root.add_child(board)
	await process_frame
	await RenderingServer.frame_post_draw
	if root.get_texture().get_image().save_png(OUT+".png")!=OK:
		push_error("Capture failed"); quit(1); return
	var f:=FileAccess.open(OUT+".json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"assets":provenance,"section_gap":96,"door_opening":72,"axial_margin_each":12,"cases":reports,"scope":"Static rectangular overlaps and visual overlay; no runtime placement","owner_acceptance":null},"\t"))
	if not FileAccess.file_exists(get_script().resource_path+".uid"):
		var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE)
		uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("SEED HOST STUDY PASS: capture and overlap report; fit is not accepted")
	quit()
