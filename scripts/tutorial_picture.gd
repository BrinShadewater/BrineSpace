extends VBoxContainer
## Native screenshots with numbered callouts. No player state or recipe lookup.
const EXAMPLES := {
	2: ["res://assets/tutorial/building.png", "BUILDING", "1 — A completed corridor meets the core at a matching doorway. 2 — The inspector identifies the selected room. Before building, use the blueprint preview to check its door orientation and construction requirements."],
	3: ["res://assets/tutorial/resources.png", "RESOURCES", "1 — Watch stored Power and its change. 2 — Inspect the selected room's operating state and requirements. Example values are not a target balance."],
	6: ["res://assets/tutorial/mining.png", "MINING", "1 — The bay inspector reports operation, battery and route conditions. 2 — Metal is credited when cargo docks, not when drilling begins."],
	7: ["res://assets/tutorial/recovery.png", "RECOVERY", "1 — Follow the recovery checklist for the surveyed site. 2 — The action button shows the next step or its blocker. Crew wards and companion containers have different wake requirements."],
	9: ["res://assets/tutorial/progression.png", "PROGRESSION", "1 — Archived Data is your spendable persistent balance. 2 — Choose upgrades, blueprints or crew. Character cards distinguish owned, purchasable and unmet characters. This is a staged example, not your profile."],
}
var topic := 0
var preview: TextureRect
var enlarge: Button
var expanded_dialog: AcceptDialog
func _ready() -> void:
	var entry: Array = EXAMPLES[topic]
	var frame := AspectRatioContainer.new()
	frame.ratio = 16.0 / 9.0
	frame.custom_minimum_size.y = 340
	frame.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	add_child(frame)
	preview = TextureRect.new()
	preview.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	frame.add_child(preview)
	var caption := Label.new()
	caption.text = entry[2]
	caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	caption.add_theme_font_size_override("font_size", 18)
	add_child(caption)
	enlarge = Button.new()
	enlarge.text = "ENLARGE " + str(entry[1]) + " EXAMPLE"
	enlarge.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	enlarge.custom_minimum_size.y = 40
	enlarge.pressed.connect(_enlarge)
	add_child(enlarge)
	visibility_changed.connect(_load_picture)
	_load_picture()

func _load_picture() -> void:
	if not is_visible_in_tree() or preview.texture != null: return
	var image := Image.new()
	if image.load(EXAMPLES[topic][0]) == OK:
		preview.texture = ImageTexture.create_from_image(image)
	else:
		push_error("Tutorial screenshot missing: " + str(EXAMPLES[topic][0]))

func _enlarge() -> void:
	if is_instance_valid(expanded_dialog): return
	var dialog := AcceptDialog.new()
	expanded_dialog = dialog
	dialog.title = "TUTORIAL // " + str(EXAMPLES[topic][1])
	dialog.ok_button_text = "BACK TO GUIDE"
	dialog.theme = preload("res://scripts/title_button_style.gd").menu_theme()
	dialog.add_theme_stylebox_override("panel", preload("res://scripts/title_button_style.gd")._flat("10232e", "596664", 12))
	dialog.exclusive = true
	dialog.dialog_close_on_escape = true
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation", 12)
	dialog.add_child(body)
	var picture := TextureRect.new()
	picture.name = "ExampleImage"
	picture.texture = preview.texture
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_child(picture)
	var caption := Label.new()
	caption.name = "ExampleCaption"
	caption.text = EXAMPLES[topic][2]
	# Give wrapped text a starting width before AcceptDialog measures its minimum.
	# Otherwise it initially wraps at one character and grows the window offscreen.
	caption.custom_minimum_size.x = 600
	caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	caption.add_theme_font_size_override("font_size", 18)
	body.add_child(caption)
	add_child(dialog)
	preload("res://scripts/title_settings.gd").apply_menu_text(dialog)
	var scroll := _guide_scroll()
	var position_before := scroll.scroll_vertical if scroll != null else 0
	dialog.confirmed.connect(_close_example.bind(dialog, position_before))
	dialog.canceled.connect(_close_example.bind(dialog, position_before))
	dialog.popup_centered(Vector2i(get_viewport_rect().size * 0.9))
	dialog.get_ok_button().grab_focus()

func _guide_scroll() -> ScrollContainer:
	var ancestor := get_parent()
	while ancestor != null:
		if ancestor is ScrollContainer: return ancestor
		ancestor = ancestor.get_parent()
	return null

func _close_example(dialog: AcceptDialog, position_before: int) -> void:
	dialog.hide()
	dialog.queue_free()
	enlarge.grab_focus()
	# Returning keyboard focus can invoke the archive's automatic scrolling.
	await get_tree().process_frame
	if not is_inside_tree(): return
	var scroll := _guide_scroll()
	if scroll != null: scroll.scroll_vertical = position_before
