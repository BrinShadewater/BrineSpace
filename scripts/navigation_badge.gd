extends Control

# Clip the source's baked exterior at the physical badge silhouette during drawing.
# Source pixels remain untouched; UVs retain the complete icon and metal surround.
var art: Texture2D
var badge_id := ""
var owner_button: Button
static var textures: Dictionary = {}
static var plain_frames: Dictionary = {}
var last_button_state := -1
# Top navigation buttons centre the badge and caption together as one group.
var centre_in_button := false
var last_layout_key: Array = []
const TOP_BADGE := 56.0
const TOP_GAP := 4.0

static func create(id: String) -> Control:
	var badge = load("res://scripts/navigation_badge.gd").new()
	badge.badge_id = id
	if not textures.has(id):
		var image := Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, "res://brineui/navigation-badges-v3/%s.png" % id)
		textures[id] = ImageTexture.create_from_image(image)
	badge.art = textures[id]
	badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return badge

static func apply(button: Button, id: String, extent: float = 40.0) -> void:
	var badge = create(id)
	badge.owner_button = button
	badge.name = "NavigationBadge"
	button.add_child(badge)
	badge.set_anchors_preset(Control.PRESET_CENTER_LEFT)
	badge.position = Vector2(8, -extent / 2)
	badge.size = Vector2.ONE * extent
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		var style := button.get_theme_stylebox(state).duplicate() as StyleBox
		style.content_margin_left = extent + 16
		button.add_theme_stylebox_override(state, style)
	button.set_meta("navigation_badge", id)

static func apply_top(button: Button, id: String) -> void:
	apply(button, id, 56)
	button.custom_minimum_size = Vector2(112, 104)
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.add_theme_font_size_override("font_size", 11)
	var badge := button.get_node("NavigationBadge") as Control
	badge.set_anchors_preset(Control.PRESET_CENTER_TOP)
	badge.position = Vector2(-28, 8)
	badge.centre_in_button = true
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		var style := button.get_theme_stylebox(state).duplicate() as StyleBox
		style.content_margin_left = 8
		style.content_margin_right = 8
		style.content_margin_top = 72
		style.content_margin_bottom = 8
		if style is StyleBoxTexture: style.texture = plain_frame(style.texture)
		button.add_theme_stylebox_override(state, style)

# The shared HUD button frame has a faint highlight row 8 px from its top edge. Stretched
# across these tall buttons it read as a stray line along the top of every icon (owner
# playtest); the navigation buttons use a copy with that row filled from the one above.
static func plain_frame(texture: Texture2D) -> Texture2D:
	if texture == null: return texture
	var key := texture.get_instance_id()
	if not plain_frames.has(key):
		var image := texture.get_image()
		if image == null or image.get_height() <= 9:
			plain_frames[key] = texture
		else:
			image = image.duplicate()
			if image.is_compressed(): image.decompress()
			for x in range(image.get_width()): image.set_pixel(x, 8, image.get_pixel(x, 7))
			plain_frames[key] = ImageTexture.create_from_image(image)
	return plain_frames[key]

# Vertically centre the badge and its caption (one or two lines) inside the button.
func _centre_group() -> void:
	var font := owner_button.get_theme_font("font")
	var font_size := owner_button.get_theme_font_size("font_size")
	var lines := owner_button.text.count("\n") + 1
	var text_height := font.get_height(font_size) * lines if font != null else 16.0 * lines
	var group := TOP_BADGE + TOP_GAP + text_height
	var top := maxf(4.0, roundf((owner_button.size.y - group) / 2.0))
	position.y = top
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		var style := owner_button.get_theme_stylebox(state)
		style.content_margin_top = top + TOP_BADGE + TOP_GAP
		style.content_margin_bottom = maxf(4.0, owner_button.size.y - top - group)

func _process(_delta: float) -> void:
	if not is_instance_valid(owner_button): return
	if centre_in_button:
		var layout_key := [owner_button.text, owner_button.size]
		if layout_key != last_layout_key:
			last_layout_key = layout_key
			_centre_group()
	var state := int(owner_button.disabled) | (int(owner_button.button_pressed) << 1) | (int(owner_button.is_hovered()) << 2)
	if state != last_button_state:
		last_button_state = state
		queue_redraw()

func _draw() -> void:
	if art == null: return
	# Conservative octagon inside each authored metal border, excluding checkerboard.
	var bounds: Rect2 = {
		"codex": Rect2(82, 94, 1088, 1070),
		"archive": Rect2(90, 96, 1072, 1062),
		"diagnostics": Rect2(91, 88, 1070, 1068),
		"journal": Rect2(98, 104, 1056, 1048),
		"menu": Rect2(106, 116, 1040, 1022)
	}.get(badge_id, Rect2(100, 100, 1054, 1054))
	var bevel := 132.0
	var points := PackedVector2Array([
		Vector2(bevel,0),Vector2(bounds.size.x-bevel,0),
		Vector2(bounds.size.x,bevel),Vector2(bounds.size.x,bounds.size.y-bevel),
		Vector2(bounds.size.x-bevel,bounds.size.y),Vector2(bevel,bounds.size.y),
		Vector2(0,bounds.size.y-bevel),Vector2(0,bevel)])
	var uv := PackedVector2Array()
	var screen := PackedVector2Array()
	var side := minf(size.x, size.y)
	var origin := (size-Vector2.ONE*side)/2
	var tint := Color.WHITE
	if is_instance_valid(owner_button):
		if owner_button.disabled: tint = Color(0.5,0.5,0.5,0.6)
		elif owner_button.button_pressed:
			origin.y += 1
			tint = Color(0.78,0.78,0.78)
		elif owner_button.is_hovered(): tint = Color(1.08,1.08,1.08)
	for point in points:
		uv.append((bounds.position+point)/Vector2(art.get_size()))
		screen.append(origin+point/bounds.size*side)
	draw_polygon(screen,PackedColorArray([tint]),uv,art)
