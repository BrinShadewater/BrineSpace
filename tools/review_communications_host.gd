extends SceneTree
## Read-only Radio Lab overlay; rectangular checks are not collision acceptance.
const OUT = "res://output/communications-host-study"
const HOST = "res://rooms/full-wall-v1/radio_lab_view.gd"
const SECTION = "res://assets/communications-south-section-v1/"
class Board extends Node2D:
	var cases: Array = []
	var compact = false
	func _draw() -> void:
		draw_rect(Rect2(0,0,500 if compact else 1000,540 if compact else 1020),Color("26363a"))
		draw_string(ThemeDB.fallback_font,Vector2(20,25),"Radio Lab: short section, furniture retained" if compact else "Radio Lab: existing furniture retained; communications candidate outlined orange",HORIZONTAL_ALIGNMENT_LEFT,-1,17)
		for i in range(cases.size()):
			var c = cases[i]
			var center = Vector2(250+(i%2)*500,270+(i/2)*480)
			c.room.render_into(self,center,1.0)
			draw_set_transform(Vector2.ZERO)
			draw_texture_rect_region(c.texture,Rect2(center+c.rect.position,c.rect.size),c.region)
			draw_rect(Rect2(center+c.rect.position,c.rect.size),Color("ebaa64"),false,1.0)
			for door in c.doors:
				if c.rect.intersects(door): draw_rect(Rect2(center+door.position,door.size),Color(1,0.2,0.2,0.4))
			draw_string(ThemeDB.fallback_font,Vector2(35+(i%2)*500,490+(i/2)*480),c.side+": visual overlaps "+str(c.overlaps.size())+", door overlap "+str(c.door_overlap),HORIZONTAL_ALIGNMENT_LEFT,-1,16)
		draw_string(ThemeDB.fallback_font,Vector2(20,530 if compact else 1010),"Static overlay; occupied access unverified" if compact else "Static overlay; no room edits or occupied-access, mounting, collision or visual acceptance",HORIZONTAL_ALIGNMENT_LEFT,-1,15)
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var compact = "--section" in OS.get_cmdline_user_args()
	var out_path = "res://output/communications-section-host-study" if compact else OUT
	if FileAccess.file_exists(out_path+".png") or FileAccess.file_exists(out_path+".json"):
		push_error("Study exists; preserve prior evidence"); quit(1); return
	root.size=Vector2i(500,540) if compact else Vector2i(1000,1020)
	root.content_scale_size=root.size
	root.canvas_item_default_texture_filter=Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	preload("res://scripts/room_layout_store.gd").path="res://output/communications-host-isolated-layouts.json"
	var family_path = "res://assets/communications-service-wall-v1/family.json"
	var family = JSON.parse_string(FileAccess.get_file_as_string(family_path))
	if compact:
		var reviewed=JSON.parse_string(FileAccess.get_file_as_string(SECTION+"material-scale-review.json"))
		family={"directions":{"south":{"export":reviewed.export_path,"registration":reviewed.registration_path,"review":SECTION.trim_prefix("res://")+"material-scale-review.json","sha256":reviewed.export_sha256}}}
	var board=Board.new()
	board.compact=compact
	var reports: Array=[]
	for side in (["south"] if compact else ["north","south","west","east"]):
		var entry=family.directions[side]
		var export_path="res://"+entry.export
		var reg_path="res://"+entry.registration
		var review_path="res://"+entry.review
		var reg=JSON.parse_string(FileAccess.get_file_as_string(reg_path))
		var review=JSON.parse_string(FileAccess.get_file_as_string(review_path))
		if FileAccess.get_sha256(export_path)!=entry.sha256 or entry.sha256!=review.export_sha256 or FileAccess.get_sha256(reg_path)!=review.registration_sha256:
			push_error("Stale candidate dependency"); quit(1); return
		var raw=Image.new()
		if raw.load_png_from_buffer(FileAccess.get_file_as_bytes(export_path))!=OK:
			push_error("Cannot decode candidate"); quit(1); return
		var size=Vector2(review.proposed_display_width_world,review.proposed_display_height_world)
		var at=Vector2(-160,-184)
		if side=="south": at=Vector2(-160,184-size.y)
		if side=="west": at=Vector2(-184,-160)
		if side=="east": at=Vector2(184-size.x,-160)
		var candidate=Rect2(at,size)
		var room=load(HOST).new()
		room.embedded=true
		room.hide()
		root.add_child(room)
		room.configure_embedded(0,[1,3],false,0.0)
		var overlaps: Array=[]
		for prop in room.props:
			var visual: Rect2=room.prop_visual_bounds(prop)
			if candidate.intersects(visual):
				overlaps.append({"id":str(prop.id),"visual_rect":[visual.position.x,visual.position.y,visual.size.x,visual.size.y]})
		var doors=[Rect2(-184,-36,24,72),Rect2(160,-36,24,72)]
		var door_overlap=false
		for door in doors:
			if candidate.intersects(door): door_overlap=true
		board.cases.append({"room":room,"texture":ImageTexture.create_from_image(raw),"region":Rect2(reg.region[0],reg.region[1],reg.region[2],reg.region[3]),"rect":candidate,"side":side,"doors":doors,"overlaps":overlaps,"door_overlap":door_overlap})
		reports.append({"side":side,"export_sha256":entry.sha256,"registration_sha256":review.registration_sha256,"candidate_rect":[at.x,at.y,size.x,size.y],"visual_rect_overlaps":overlaps,"door_bay_overlap":door_overlap})
	root.add_child(board)
	await process_frame
	await RenderingServer.frame_post_draw
	if root.get_texture().get_image().save_png(out_path+".png")!=OK:
		push_error("Capture failed"); quit(1); return
	var dependencies={}
	for path in [HOST,"res://rooms/underwater/acoustic-comms/radio_lab_view.gd","res://rooms/full-wall-v1/full_wall_prop.gd","res://rooms/full-wall-v1/default-layouts.json","res://scripts/room_database.gd",family_path]:
		dependencies[path]=FileAccess.get_sha256(path)
	if compact:
		dependencies[SECTION+"material-scale-review.json"]=FileAccess.get_sha256(SECTION+"material-scale-review.json")
	var file=FileAccess.open(out_path+".json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"host":"radio_lab","quarter":0,"open_sides":[1,3],"dependencies":dependencies,"cases":reports,"scope":"Static visual-rectangle and72-unit door-bay study; no runtime placement acceptance"},"\t"))
	if not FileAccess.file_exists(get_script().resource_path+".uid"):
		var uid=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE)
		uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("COMMUNICATIONS HOST STUDY PASS: capture/report only; inspect fit separately")
	quit()
