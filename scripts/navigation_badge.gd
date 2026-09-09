extends Control

# Clip the source's baked exterior at the physical badge silhouette during drawing.
# Source pixels remain untouched; UVs retain the complete icon and metal surround.
var art: Texture2D
var badge_id := ""
var owner_button: Button
static var textures: Dictionary = {}
var last_button_state := -1

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
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		var style := button.get_theme_stylebox(state).duplicate() as StyleBox
		style.content_margin_left = 8
		style.content_margin_right = 8
		style.content_margin_top = 72
		style.content_margin_bottom = 8
		button.add_theme_stylebox_override(state, style)

func _process(_delta: float) -> void:
	if not is_instance_valid(owner_button): return
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
