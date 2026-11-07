extends SceneTree
## Static group diagnostic; shared world scale, not installed collision evidence.
## --group=res://...json --review=res://output/...png
class Board extends Node2D:
	var entries: Array = []
	func _draw() -> void:
		draw_rect(Rect2(0,0,1040,600),Color("26363a"))
		draw_string(ThemeDB.fallback_font,Vector2(24,30),"Prop group: native 1 px/world unit (top); 2x diagnostic (bottom)",HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		draw_string(ThemeDB.fallback_font,Vector2(24,580),"Static arrangement only. Door access, crew routes and collision remain unverified.",HORIZONTAL_ALIGNMENT_LEFT,-1,18)
		for panel in range(2):
			var factor := float(panel+1)
			var origin := Vector2(30,60+panel*190)
			for entry in entries:
				draw_texture_rect_region(entry.texture,Rect2(origin+entry.at*factor,entry.size*factor),entry.region)

func _initialize() -> void:
	call_deferred("run")

func finite_numbers(value: Variant, count: int) -> bool:
	if not value is Array or value.size()!=count:
		return false
	for number in value:
		if not (number is float or number is int) or not is_finite(float(number)):
			return false
	return true

func run() -> void:
	var group_path := ""
	var output_path := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--group="): group_path=arg.trim_prefix("--group=")
		if arg.begins_with("--review="): output_path=arg.trim_prefix("--review=")
	if group_path.is_empty() or output_path.is_empty():
		push_error("Require --group and --review"); quit(1); return
	var group=JSON.parse_string(FileAccess.get_file_as_string(group_path))
	if not group is Dictionary or not group.get("entries") is Array or group.entries.is_empty():
		push_error("Group requires a nonempty entries array"); quit(1); return
	var board := Board.new()
	for entry in group.entries:
		if not entry is Dictionary or not entry.get("export") is String or not entry.get("sha256") is String:
			push_error("Group entry requires export and sha256 strings"); quit(1); return
		if not finite_numbers(entry.get("region"),4) or not finite_numbers(entry.get("at"),2) or not finite_numbers([entry.get("width")],1):
			push_error("Group region, position and width require finite numbers"); quit(1); return
		if ProjectSettings.globalize_path(output_path).simplify_path()==ProjectSettings.globalize_path(entry.export).simplify_path():
			push_error("Review must not overwrite a group export"); quit(1); return
		if FileAccess.get_sha256(entry.export)!=entry.sha256:
			push_error("Group export hash mismatch"); quit(1); return
		var raw := Image.new()
		if raw.load_png_from_buffer(FileAccess.get_file_as_bytes(entry.export))!=OK:
			push_error("Cannot decode group export"); quit(1); return
		var r: Array=entry.region
		if r.size()!=4 or r[2]<=0 or r[3]<=0 or entry.width<=0:
			push_error("Invalid group region or scale"); quit(1); return
		if r[0]<0 or r[1]<0 or r[0]+r[2]>raw.get_width() or r[1]+r[3]>raw.get_height():
			push_error("Group source region exceeds export canvas"); quit(1); return
		# Both panels must retain every pixel, including tall props and positions.
		# The 2x panel determines usable width490 and height150 world units.
		if entry.at[0]<0 or entry.at[1]<0 or entry.at[0]+entry.width>490 or entry.at[1]+entry.width*r[3]/r[2]>150:
			push_error("Group exceeds review panels; adjust board, not asset scale"); quit(1); return
		board.entries.append({"texture":ImageTexture.create_from_image(raw),"region":Rect2(r[0],r[1],r[2],r[3]),"at":Vector2(entry.at[0],entry.at[1]),"size":Vector2(entry.width,entry.width*r[3]/r[2])})
	root.size=Vector2i(1040,600)
	root.content_scale_size=root.size
	root.canvas_item_default_texture_filter=Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	root.add_child(board)
	await process_frame
	await RenderingServer.frame_post_draw
	if root.get_texture().get_image().save_png(output_path)!=OK:
		push_error("Cannot save group review"); quit(1); return
	var script_path: String=get_script().resource_path
	if not FileAccess.file_exists(script_path+".uid"):
		var f:=FileAccess.open(script_path+".uid",FileAccess.WRITE)
		f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("PROP GROUP PASS: export hashes and static native-scale capture; not runtime placement")
	quit()
