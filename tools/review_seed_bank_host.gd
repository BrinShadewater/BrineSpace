extends SceneTree
## Read-only host study. Rectangular overlaps are not runtime collision proof.
const OUT := "res://output/seed-bank-host-study"
const ASSET := "res://assets/botanical-seed-west-wall-v1/"
class Board extends Node2D:
	var rooms: Array = []
	var texture: Texture2D
	var region: Rect2
	var candidate: Rect2
	func _draw() -> void:
		draw_rect(Rect2(0,0,1000,560),Color("26363a"))
		draw_string(ThemeDB.fallback_font,Vector2(24,28),"Seed bank host study: existing furniture retained; candidate outlined orange",HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		for i in range(2):
			var center := Vector2(250+i*500,295)
			rooms[i].render_into(self,center,1.0)
			draw_set_transform(Vector2.ZERO)
			var target := Rect2(center+candidate.position,candidate.size)
			draw_texture_rect_region(texture,target,region)
			draw_rect(target,Color("ebaa64"),false,1.0)
			if i==1:
				draw_rect(Rect2(center+Vector2(-184,-36),Vector2(candidate.size.x,72)),Color(1,0.2,0.2,0.45))
			draw_string(ThemeDB.fallback_font,Vector2(35+i*500,535),"Closed west wall" if i==0 else "Open west wall: candidate crosses door bay",HORIZONTAL_ALIGNMENT_LEFT,-1,17)
		draw_string(ThemeDB.fallback_font,Vector2(24,555),"Visual overlay only; no room data changed, no crew or collision acceptance",HORIZONTAL_ALIGNMENT_LEFT,-1,15)
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	if FileAccess.file_exists(OUT+".png") or FileAccess.file_exists(OUT+".json"):
		push_error("Refuse to overwrite prior study"); quit(1); return
	var reg = JSON.parse_string(FileAccess.get_file_as_string(ASSET+"registration.json"))
	var record = JSON.parse_string(FileAccess.get_file_as_string(ASSET+"material-scale-review.json"))
	if FileAccess.get_sha256(ASSET+"wall.png")!=record.export_sha256:
		push_error("Stale export"); quit(1); return
	var raw:=Image.new()
	if raw.load_png_from_buffer(FileAccess.get_file_as_bytes(ASSET+"wall.png"))!=OK:
		push_error("Cannot decode export"); quit(1); return
	root.size=Vector2i(1000,560)
	root.content_scale_size=root.size
	root.canvas_item_default_texture_filter=Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	preload("res://scripts/room_layout_store.gd").path="res://output/seed-host-isolated-layouts.json"
	var board:=Board.new()
	board.texture=ImageTexture.create_from_image(raw)
	board.region=Rect2(reg.region[0],reg.region[1],reg.region[2],reg.region[3])
	board.candidate=Rect2(-184,-160,record.proposed_display_width_world,320)
	var reports: Array=[]
	for i in range(2):
		var room=load("res://rooms/full-wall-v1/hydroponics_bay_view.gd").new()
		room.embedded=true
		room.hide()
		root.add_child(room)
		room.configure_embedded(0,[] if i==0 else [3],false,0.0)
		var overlaps: Array=[]
		for prop in room.props:
			if board.candidate.intersects(prop.rect): overlaps.append(str(prop.id))
		reports.append({"open_sides":[] if i==0 else [3],"rect_overlap_ids":overlaps,"door_bay_overlap":i==1})
		board.rooms.append(room)
	root.add_child(board)
	await process_frame
	await RenderingServer.frame_post_draw
	if root.get_texture().get_image().save_png(OUT+".png")!=OK:
		push_error("Capture failed"); quit(1); return
	var f:=FileAccess.open(OUT+".json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"asset":ASSET,"export_sha256":record.export_sha256,"candidate_rect":[-184,-160,board.candidate.size.x,320],"cases":reports,"scope":"Static rectangular overlaps and visual overlay; no runtime placement","owner_acceptance":null},"\t"))
	if not FileAccess.file_exists(get_script().resource_path+".uid"):
		var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE)
		uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("SEED HOST STUDY PASS: capture and overlap report; fit is not accepted")
	quit()
