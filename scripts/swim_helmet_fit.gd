extends RefCounted
## Compose swimming equipment once at load time from preserved body/helmet sources.
const ROOT = "res://character/crew-underwater-v1/"
static var head_fits: Dictionary = {}

static func composite_tilted(body: Image, overlay: Image, offset: Vector2, angle: float, head_rect: Rect2i, direction: String) -> void:
	# Rotate around the neck seal so the crown leans into the swimming direction.
	var pivot := Vector2(overlay.get_width()*0.5,overlay.get_height()*0.85)
	var reach := overlay.get_width()+overlay.get_height()
	var center := Vector2(offset)+pivot
	for y in range(maxi(0,floori(center.y)-reach),mini(body.get_height(),ceili(center.y)+reach)):
		for x in range(maxi(0,floori(center.x)-reach),mini(body.get_width(),ceili(center.x)+reach)):
			var source := (Vector2(x,y)+Vector2.ONE*0.5-center).rotated(-angle)+pivot
			var pixel := Vector2i(source.floor())
			var inside := pixel.x>=0 and pixel.y>=0 and pixel.x<overlay.get_width() and pixel.y<overlay.get_height()
			# Bare hair/skull is an occluded layer. Only the visor reveals the face.
			var visor := inside and source.y>=overlay.get_height()*8.0/28.0 and source.y<overlay.get_height()*19.0/28.0 and (source.x>overlay.get_width()*0.58 if direction=="east" else source.x<overlay.get_width()*0.42)
			var scalp := source.y<overlay.get_height()*0.32 or (not inside and source.y<overlay.get_height()*0.65)
			if head_rect.has_point(Vector2i(x,y)) and scalp and not visor:
				body.set_pixel(x,y,Color.TRANSPARENT)
			if not inside: continue
			var color := overlay.get_pixelv(pixel)
			if color.a>0: body.set_pixel(x,y,body.get_pixel(x,y).blend(color))

static func apply(player, variant, path: String) -> void:
	if head_fits.is_empty(): head_fits = JSON.parse_string(FileAccess.get_file_as_string(ROOT+"swim-head-fit.json")).clips
	var registration_path := path.get_base_dir().path_join("registration.json")
	var registration := {}
	if FileAccess.file_exists(registration_path):
		registration = JSON.parse_string(FileAccess.get_file_as_string(registration_path))
	elif path.ends_with("equipment/fitting/veld-swim-north/manifest.json"):
		var legacy: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(ROOT+"equipment/fitting/swim-north-registration.json"))
		var pose: Dictionary = legacy.characters.veld
		registration = {"overlay":"equipment/north/overlay.png", "frames":[]}
		for regions in pose.foregroundRects:
			registration.frames.append({"overlayTopLeft":pose.overlayTopLeft,"foregroundRects":regions})
	else: return
	for key in variant.frames:
		if not str(key).begins_with("swim-"): continue
		var direction: String = str(key).trim_prefix("swim-")
		var overlay := Image.new()
		if overlay.load_png_from_buffer(FileAccess.get_file_as_bytes(ROOT+registration.overlay)) != OK: continue
		var original_size := overlay.get_size()
		var scale := 0.75 if direction in ["east", "west"] else 0.85
		var width_scale := 0.82 if direction in ["east", "west"] else scale
		overlay.resize(roundi(original_size.x*width_scale),roundi(original_size.y*scale),Image.INTERPOLATE_NEAREST)
		for i in range(variant.frames[key].size()):
			var pose: Dictionary = registration.frames[i]
			var body: Image = player.frames[key][i].get_image()
			var fitted := body.duplicate() as Image
			var offset := Vector2i(pose.overlayTopLeft[0],pose.overlayTopLeft[1])
			offset += Vector2i((original_size-overlay.get_size())/2)
			if direction in ["east", "west"]:
				var clip := path.get_base_dir().get_base_dir().get_file().trim_suffix("-v2")
				var fit: Dictionary = head_fits[clip][i]
				var angle := deg_to_rad(float(fit.tiltDegrees))
				var pivot := Vector2(overlay.get_width()*0.5,overlay.get_height()*0.85)
				var visor_edge := Vector2(overlay.get_width()*(21.5/23.0 if direction=="east" else 1.5/24.0),overlay.get_height()*13.0/28.0)
				var anchor := (visor_edge-pivot).rotated(angle)+pivot
				var placement := Vector2(fit.faceEdge[0],fit.faceEdge[1])-anchor
				var bounds: Array = fit.headRect
				composite_tilted(fitted,overlay,placement,angle,Rect2i(bounds[0],bounds[1],bounds[2],bounds[3]),direction)
			else:
				fitted.blend_rect(overlay,Rect2i(Vector2i.ZERO,overlay.get_size()),offset)
			for region in pose.get("foregroundRects",[]):
				var rect := Rect2i(region[0],region[1],region[2]-region[0],region[3]-region[1])
				fitted.blend_rect(body,rect,rect.position)
			var texture := ImageTexture.create_from_image(fitted)
			for meta in variant.frames[key][i].get_meta_list():
				texture.set_meta(meta,variant.frames[key][i].get_meta(meta))
			variant.frames[key][i] = texture
