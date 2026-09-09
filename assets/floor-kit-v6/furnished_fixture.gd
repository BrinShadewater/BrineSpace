extends RefCounted
## Opt-in visual fixture only; these dense placements never appear in normal play.
static var textures: Array[Texture2D]=[]
static func draw_details(c: CanvasItem, center: Vector2) -> void:
	if textures.is_empty():
		var names:=DirAccess.get_files_at("res://assets/floor-kit-v6/exports")
		for name in names:
			if not name.ends_with(".png") or name.begins_with("corridor-"): continue
			var im:=Image.new()
			if im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/floor-kit-v6/exports/"+name)) != OK: push_error("Failed to load image (assets/floor-kit-v6/furnished_fixture.gd)")
			textures.append(ImageTexture.create_from_image(im))
	for i in range(textures.size()):
		var at:=center+Vector2(-140+(i%5)*70,-140+(i/5)*56)
		c.draw_texture_rect(textures[i],Rect2(at-Vector2.ONE*192,Vector2.ONE*384),false)
