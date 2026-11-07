extends SceneTree
## Native cutout export and material/scale diagnostic. Does not install artwork.
## --registration=res://...json --export=res://...png --review=res://output/...png
## Optional: --reference-view=res://...gd --width=320
var registration_path := ""
var export_path := ""
var review_path := ""
var reference_view_path := ""
var world_width := 320.0

class Cutout extends Node2D:
	var texture: Texture2D
	var pieces: Array
	func _draw() -> void:
		for part in pieces:
			var points := PackedVector2Array()
			var uv := PackedVector2Array()
			for point in part:
				points.append(Vector2(point[0],point[1]))
				uv.append(Vector2(point[0],point[1])/texture.get_size())
			draw_polygon(points,PackedColorArray([Color.WHITE]),uv,texture)

class Review extends Node2D:
	var texture: Texture2D
	var region: Rect2
	var width_world: float
	var reference
	func label(at: Vector2,value: String) -> void:
		draw_string(ThemeDB.fallback_font,at,value,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("c5d0d8"))
	func sprite(at: Vector2,width: float) -> void:
		draw_texture_rect_region(texture,Rect2(at,Vector2(width,width*region.size.y/region.size.x)),region)
	func _draw() -> void:
		draw_rect(Rect2(0,0,1040,900),Color("16272c"))
		label(Vector2(24,30),"Material / scale diagnostic - standalone asset, NOT an installed layout")
		if reference!=null:
			reference.configure_embedded(0,[],false,0.0)
			reference.render_into(self,Vector2(240,260),1.0)
			draw_set_transform(Vector2.ZERO)
		label(Vector2(30,485),"Existing room: 1 pixel per world unit")
		label(Vector2(555,70),"Candidate: %.0f world units wide, same scale"%width_world)
		if width_world*region.size.y/region.size.x>140:
			# Full-length side banks keep native scale in two taller columns.
			draw_rect(Rect2(535,90,230,400),Color("465356"))
			draw_rect(Rect2(785,90,230,400),Color("b6bdb7"))
			sprite(Vector2(555,110),width_world)
			sprite(Vector2(805,110),width_world)
		else:
			draw_rect(Rect2(535,90,480,170),Color("465356"))
			sprite(Vector2(555,110),width_world)
			label(Vector2(555,295),"Light ground: alpha / edge review")
			draw_rect(Rect2(535,310,480,160),Color("b6bdb7"))
			sprite(Vector2(555,330),width_world)
		if region.size.y>region.size.x*3.0:
			label(Vector2(30,540),"Top / middle / bottom material detail (diagnostic only)")
			# Segment long side banks for inspection; keep native-scale panels above intact.
			var section_height: float=region.size.y/3.0
			var detail_width: float=minf(300.0,310.0*region.size.x/section_height)
			for section in range(3):
				var source_rect:=Rect2(region.position+Vector2(0,section*section_height),Vector2(region.size.x,section_height))
				draw_texture_rect_region(texture,Rect2(Vector2(30+section*330,565),Vector2(detail_width,detail_width*section_height/region.size.x)),source_rect)
		else:
			label(Vector2(30,540),"Fitted material overview (diagnostic only)")
			var detail_width: float=minf(980.0,310.0*region.size.x/region.size.y)
			sprite(Vector2(30,565),detail_width)

func fail(message: String) -> void:
	push_error(message)
	quit(1)

func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--registration="): registration_path=arg.trim_prefix("--registration=")
		if arg.begins_with("--export="): export_path=arg.trim_prefix("--export=")
		if arg.begins_with("--review="): review_path=arg.trim_prefix("--review=")
		if arg.begins_with("--reference-view="): reference_view_path=arg.trim_prefix("--reference-view=")
		if arg.begins_with("--width="): world_width=float(arg.trim_prefix("--width="))
	call_deferred("run")

func run() -> void:
	if not FileAccess.file_exists(registration_path) or export_path.is_empty() or not review_path.begins_with("res://output/") or world_width<=0 or world_width>440:
		fail("Provide registration, export, output/ review path and width in (0,440].")
		return
	var data=JSON.parse_string(FileAccess.get_file_as_string(registration_path))
	if not data is Dictionary or not data.has_all(["source","sha256","region","pieces"]):
		fail("Registration requires source, sha256, region and pieces.")
		return
	if data.region.size()!=4 or data.region[2]<=0 or data.region[3]<=0:
		fail("Registration requires a positive region width and height.")
		return
	var native_height: float=world_width*data.region[3]/data.region[2]
	if native_height>380 or (native_height>140 and world_width>210):
		fail("Native candidate exceeds review panels; use a larger review board, not a false display scale.")
		return
	if export_path==data.source or FileAccess.get_sha256(data.source)!=data.sha256:
		fail("Source hash mismatch or attempted source overwrite.")
		return
	var raw:=Image.new()
	if raw.load_png_from_buffer(FileAccess.get_file_as_bytes(data.source))!=OK:
		fail("Cannot decode registered source.")
		return
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	root.size=raw.get_size()
	root.content_scale_size=root.size
	root.transparent_bg=true
	root.canvas_item_default_texture_filter=Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	var cutout:=Cutout.new()
	cutout.texture=ImageTexture.create_from_image(raw)
	cutout.pieces=data.pieces
	root.add_child(cutout)
	await process_frame
	await RenderingServer.frame_post_draw
	var cleaned:=root.get_texture().get_image()
	if cleaned.get_size()!=raw.get_size() or cleaned.get_pixel(0,0).a!=0:
		fail("Native size/transparent exterior failed.")
		return
	if cleaned.save_png(export_path)!=OK:
		fail("Could not save cutout export.")
		return
	cutout.queue_free()
	await process_frame
	root.size=Vector2i(1040,900)
	root.content_scale_size=root.size
	var board:=Review.new()
	board.texture=ImageTexture.create_from_image(cleaned)
	board.region=Rect2(data.region[0],data.region[1],data.region[2],data.region[3])
	board.width_world=world_width
	if not reference_view_path.is_empty():
		preload("res://scripts/room_layout_store.gd").path="res://output/wall-asset-review-isolated-layouts.json"
		board.reference=load(reference_view_path).new()
		board.reference.embedded=true
		board.reference.hide()
		root.add_child(board.reference)
	root.add_child(board)
	await process_frame
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute(review_path.get_base_dir())
	var capture:=root.get_texture().get_image()
	if capture.get_size()!=Vector2i(1040,900) or capture.save_png(review_path)!=OK:
		fail("Native review dimensions/export failed.")
		return
	print("WALL ASSET PASS: source hash, native ",cleaned.get_size()," alpha export, 1040x900 scale board; NOT room integration")
	var script_path: String=get_script().resource_path
	if not FileAccess.file_exists(script_path+".uid"):
		var uid_file:=FileAccess.open(script_path+".uid",FileAccess.WRITE)
		uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	quit()
