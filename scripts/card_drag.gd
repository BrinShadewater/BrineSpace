extends CanvasLayer
## Drag a blueprint from the draft hand onto the station (owner playtest): pressing a card still
## selects it; dragging lifts a small copy that follows the pointer and tilts with its motion.
## Over the station the copy shrinks away into the room placement preview, so the card becomes
## the room, and releasing there places it through the normal grid click. Releasing elsewhere,
## or a right click, puts the card back.

const DRAG_THRESHOLD := 12.0
const GHOST_SIZE := Vector2(150, 190)

var game
var card_id := ""
var hand_index := -1
var press_at := Vector2.ZERO
var pressing := false
var dragging := false
var over_station := false
var ghost: Control
var tilt := 0.0
var last_mouse := Vector2.ZERO

# Smoothing rates (per second) for the ghost's glide, size and fade (owner playtest, Sept 17:
# the hand-to-room hand-off should feel smoother). Over the station the card slides into the
# hovered cell, shrinks to the cell's size and dissolves into the room preview; a drop plays a
# short settle ring on the cell.
const FOLLOW_RATE := 20.0
const MORPH_RATE := 14.0

func _ready() -> void:
	layer = 40
	process_mode = Node.PROCESS_MODE_ALWAYS
	set_process(false)

func _process(delta: float) -> void:
	if not dragging or not is_instance_valid(ghost):
		set_process(false)
		return
	var reduced: bool = game.Preferences.reduced_motion
	var target_position := pointer - ghost.pivot_offset
	var target_scale := 1.0
	var target_alpha := 1.0
	if over_station:
		var cell_rect := _cell_screen_rect(_cell_under_pointer())
		target_position = cell_rect.get_center() - ghost.pivot_offset
		target_scale = clampf(cell_rect.size.x / GHOST_SIZE.x, 0.2, 1.0)
		target_alpha = 0.0
	var follow := 1.0 if reduced else 1.0 - exp(-FOLLOW_RATE * delta)
	var morph := 1.0 if reduced else 1.0 - exp(-MORPH_RATE * delta)
	ghost.position = ghost.position.lerp(target_position, follow)
	ghost.scale = ghost.scale.lerp(Vector2.ONE * target_scale, morph)
	ghost.modulate.a = lerpf(ghost.modulate.a, target_alpha, morph)
	tilt = 0.0 if reduced else lerpf(tilt, 0.0, 1.0 - exp(-6.0 * delta))
	ghost.rotation = lerpf(ghost.rotation, 0.0 if over_station else tilt, morph)

func _cell_screen_rect(cell: Vector2i) -> Rect2:
	var size: float = game.get_cell_size()
	var xform: Transform2D = game.grid_view.get_global_transform_with_canvas()
	var top_left: Vector2 = xform * (Vector2(cell) * size)
	var bottom_right: Vector2 = xform * ((Vector2(cell) + Vector2.ONE) * size)
	return Rect2(top_left, bottom_right - top_left)

func _settle_ring(cell: Vector2i) -> void:
	if game.Preferences.reduced_motion: return
	var rect := _cell_screen_rect(cell)
	var ring := Panel.new()
	ring.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var style := StyleBoxFlat.new()
	style.draw_center = false
	style.border_color = Color("9ff3df")
	style.set_border_width_all(3)
	style.set_corner_radius_all(6)
	ring.add_theme_stylebox_override("panel", style)
	ring.position = rect.position
	ring.size = rect.size
	ring.pivot_offset = rect.size * 0.5
	ring.scale = Vector2.ONE * 0.9
	add_child(ring)
	var tween := ring.create_tween().set_parallel().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_property(ring, "scale", Vector2.ONE * 1.06, 0.3)
	tween.tween_property(ring, "modulate:a", 0.0, 0.3)
	tween.chain().tween_callback(ring.queue_free)

func begin(id: String, index: int, at: Vector2) -> void:
	card_id = id
	hand_index = index
	press_at = at
	last_mouse = at
	pressing = true
	dragging = false

func is_dragging() -> bool:
	return dragging

func _input(event: InputEvent) -> void:
	if not pressing: return
	if event is InputEventMouseMotion:
		var at: Vector2 = event.position
		pointer = at
		if not dragging and at.distance_to(press_at) >= DRAG_THRESHOLD and game.selected_card_id == card_id:
			_start_drag()
		if dragging:
			_follow(at)
			get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton and not event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if dragging:
			get_viewport().set_input_as_handled()
			pointer = event.position
			var drop_cell: Vector2i = _cell_under_pointer()
			var drop := over_station
			_finish()
			if drop:
				var before: bool = game.occupied.has(drop_cell) or game.drone_fleet.reserved(drop_cell)
				game._on_grid_clicked(drop_cell)
				if not before and (game.occupied.has(drop_cell) or game.drone_fleet.reserved(drop_cell)): _settle_ring(drop_cell)
		else:
			pressing = false
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_RIGHT and dragging:
		get_viewport().set_input_as_handled()
		_finish()

func _mouse() -> Vector2:
	return game.get_node("Root").get_global_mouse_position()

var pointer := Vector2.ZERO

func _start_drag() -> void:
	dragging = true
	ghost = _build_ghost()
	add_child(ghost)
	ghost.position = pointer - ghost.pivot_offset
	_set_source_faded(true)
	_follow(pointer)
	set_process(true)

func _follow(at: Vector2) -> void:
	var velocity := at - last_mouse
	last_mouse = at
	var reduced: bool = game.Preferences.reduced_motion
	tilt = 0.0 if reduced else lerpf(tilt, clampf(velocity.x * 0.012, -0.3, 0.3), 0.35)
	var inside: bool = game.station_clear_rect().has_point(at) and not game.hand_panel.get_global_rect().has_point(at)
	if inside:
		game._on_grid_hovered(_cell_under_pointer())
	# _process glides the ghost toward the pointer, or into the hovered cell over the station.
	over_station = inside

func _cell_under_pointer() -> Vector2i:
	var local: Vector2 = game.grid_view.get_global_transform_with_canvas().affine_inverse() * pointer
	var size: float = game.get_cell_size()
	return Vector2i(floori(local.x / size), floori(local.y / size))

func _finish() -> void:
	pressing = false
	dragging = false
	over_station = false
	tilt = 0.0
	if is_instance_valid(ghost): ghost.queue_free()
	ghost = null
	_set_source_faded(false)

func _set_source_faded(faded: bool) -> void:
	for slot in game.hand_box.get_children():
		for card in [slot] + slot.get_children():
			if card is Control and card.get_meta("hand_index", -2) == hand_index and card.get_meta("card_id", "") == card_id:
				card.modulate.a = 0.3 if faded else 1.0

func _build_ghost() -> Control:
	var room: Dictionary = game.RoomDatabaseScript.get_room(card_id)
	var color: Color = game.RoomDatabaseScript.category_color(room["category"])
	var panel := PanelContainer.new()
	panel.name = "DragGhost"
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.custom_minimum_size = GHOST_SIZE
	panel.size = GHOST_SIZE
	panel.pivot_offset = GHOST_SIZE * 0.5
	panel.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.03, 0.06, 0.08, 0.96)
	style.border_color = color
	style.set_border_width_all(3)
	style.set_corner_radius_all(10)
	style.set_content_margin_all(7)
	style.shadow_color = Color(0, 0, 0, 0.55)
	style.shadow_size = 14
	style.shadow_offset = Vector2(0, 8)
	panel.add_theme_stylebox_override("panel", style)
	var column := VBoxContainer.new()
	column.mouse_filter = Control.MOUSE_FILTER_IGNORE
	column.add_theme_constant_override("separation", 4)
	panel.add_child(column)
	var title := Label.new()
	title.text = str(room["display_name"])
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.clip_text = true
	title.add_theme_font_size_override("font_size", 13)
	title.add_theme_color_override("font_color", Color("e2ecee"))
	column.add_child(title)
	var art := TextureRect.new()
	art.custom_minimum_size = Vector2(0, 136)
	art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	art.texture = game.card_textures.get(card_id)
	art.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	column.add_child(art)
	return panel
