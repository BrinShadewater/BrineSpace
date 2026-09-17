extends SceneTree
# Settings > Accessibility > Draft hand backdrop (owner playtest): off, the station view runs
# behind the hand and only the reroll button, cards and draw/discard pile remain.
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
var grid_clicks := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	Preferences.save_path = "user://hand_backdrop_%d.cfg" % OS.get_process_id()
	var Store = preload("res://scripts/room_layout_store.gd")
	Store.path = "user://hand_backdrop_layouts_%d.json" % OS.get_process_id(); Store.loaded = true; Store.data = {}
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://hand_backdrop_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://hand_backdrop_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	game.crew_comms.set_process(false)
	game.selected_card_id = "" # A probe click must not schedule construction.
	game.grid_view.cell_clicked.connect(func(_cell): grid_clicks += 1)
	for i in range(3): await process_frame
	check(Preferences.hand_backdrop, "Backdrop defaults on")
	var framed_bottom: float = game.grid_scroll.get_global_rect().end.y
	var hand: Rect2 = game.hand_panel.get_global_rect()
	check(framed_bottom < hand.position.y + 40, "With the backdrop, the station view stops above the hand")
	# An empty spot in the hand, right of the draw pile.
	var empty := Vector2(hand.end.x - 30, hand.get_center().y)
	check(not _hand_control_at(game, empty), "Probe point is clear of hand controls")
	_click(empty)
	check(grid_clicks == 0, "The backdrop keeps clicks off the station")

	# Toggling moves only the view's bottom edge; before the fix the station jumped half of it (168 px).
	var core_before: Vector2 = _core_on_screen(game)
	Preferences.hand_backdrop = false
	game._refresh_all()
	for i in range(4): await process_frame
	check(_core_on_screen(game).distance_to(core_before) < 2.0, "The station holds still when the view grows: moved %.1f px" % _core_on_screen(game).distance_to(core_before))
	for label in game.hand_chrome: check(not label.visible, "Hand title, count and hints hide")
	check(game.reroll_button.is_visible_in_tree(), "Reroll button stays")
	var cards := 0
	var pile := false
	for child in game.hand_box.get_children():
		if child.name == "DeckSlot": pile = child.is_visible_in_tree() and child.has_node("DrawPile") and child.has_node("DiscardPile")
		elif child.is_visible_in_tree(): cards += 1
	check(cards > 0 and pile, "Cards and the draw/discard pile stay: %d cards" % cards)
	check(game.hand_panel.get_theme_stylebox("panel") is StyleBoxEmpty, "Backdrop panel is hidden")
	# The station frame keeps its own bottom margin inside the screen edge.
	check(game.grid_scroll.get_global_rect().end.y >= hand.end.y - 24, "Station view runs behind the hand: view ends %.0f, hand ends %.0f" % [game.grid_scroll.get_global_rect().end.y, hand.end.y])
	check(game.hand_panel.get_global_rect().is_equal_approx(hand), "Cards keep their place")
	_click(empty)
	check(grid_clicks == 1, "Clicks between floating cards reach the station")
	game.crew_comms.open_brine()
	game.crew_comms.place_panel()
	check(game.crew_comms.panel.get_global_rect().end.y <= hand.position.y, "Comms pops up above the floating hand")
	check(Preferences.save(game.get_window()) == OK, "Setting saves")
	var saved := ConfigFile.new()
	check(saved.load(Preferences.save_path) == OK and saved.get_value("display", "hand_backdrop", true) == false, "Setting persists")
	game.crew_comms.dismiss()

	# Each re-centre rounds the scroll to whole pixels, so judge each toggle on its own.
	core_before = _core_on_screen(game)
	Preferences.hand_backdrop = true
	game._refresh_all()
	for i in range(4): await process_frame
	check(_core_on_screen(game).distance_to(core_before) < 2.0, "The station holds still when the view shrinks: moved %.1f px" % _core_on_screen(game).distance_to(core_before))
	for label in game.hand_chrome: check(label.visible, "Hand chrome returns")
	check(absf(game.grid_scroll.get_global_rect().end.y - framed_bottom) < 1.0, "Station view returns above the hand")
	_click(empty)
	check(grid_clicks == 1, "Backdrop blocks station clicks again")

	# The toggle on the hand folds it away and brings it back (owner playtest).
	game.hand_toggle_button.emit_signal("pressed")
	for i in range(4): await process_frame
	check(not game.hand_box.is_visible_in_tree() and not game.reroll_button.is_visible_in_tree(), "Folded hand hides cards, pile and reroll")
	check(game.hand_toggle_button.is_visible_in_tree() and game.hand_toggle_button.text == "SHOW HAND", "The toggle stays to bring the hand back")
	check(game.grid_scroll.get_global_rect().end.y > framed_bottom + 200, "The station view reclaims the hand's space")
	check(game.hand_toggle_button.get_global_rect().end.y <= game.get_node("Root").size.y, "The toggle stays on screen")
	game.hand_toggle_button.emit_signal("pressed")
	for i in range(4): await process_frame
	check(game.hand_box.is_visible_in_tree() and game.reroll_button.is_visible_in_tree() and game.hand_toggle_button.text == "HIDE HAND", "Pressing again restores the hand")
	check(absf(game.grid_scroll.get_global_rect().end.y - framed_bottom) < 1.0 and game.hand_panel.get_global_rect().is_equal_approx(hand), "The hand and view return to their places")
	# Card-shaped hand as a row or a fan, and a hovered card pops up (owner playtest).
	game.running = true
	check(Preferences.hand_layout == "row" and not game.hand_box.has_node("FanRow"), "The hand starts as a row of cards")
	var row_card: Control = _first_card(game)
	check(row_card != null and row_card.size == game.DraftCard.CARD_SIZE, "Row cards are card-sized")
	Preferences.reduced_motion = true
	game._on_card_hovered(row_card.get_meta("card_id"), row_card)
	check(row_card.position == row_card.get_meta("rest_position"), "Reduced motion keeps a hovered card in place")
	Preferences.reduced_motion = false
	game._on_card_hovered(row_card.get_meta("card_id"), row_card)
	await create_timer(0.25).timeout
	check(row_card.position.y < row_card.get_meta("rest_position").y - 10 and row_card.scale.x > 1.0, "A hovered card pops up")
	game._on_card_unhovered(row_card.get_meta("card_id"), row_card)
	await create_timer(0.25).timeout
	check(row_card.position == row_card.get_meta("rest_position") and row_card.scale == Vector2.ONE, "It settles back when the pointer leaves")
	game.hand_layout_button.emit_signal("pressed")
	for i in range(6): await process_frame
	check(Preferences.hand_layout == "fan" and game.hand_box.has_node("FanRow") and game.hand_layout_button.text == "LAYOUT: FAN", "The layout toggle fans the hand")
	var fanned: Array = game.hand_box.get_node("FanRow").get_children()
	check(fanned.size() == game.hand.size(), "Every card is in the fan")
	if fanned.size() >= 3:
		check(fanned[0].rotation < 0.0 and fanned[-1].rotation > 0.0 and fanned[0].size == game.DraftCard.CARD_SIZE, "Outer cards turn outward and keep card size: rot %.3f / %.3f size %s" % [fanned[0].rotation, fanned[-1].rotation, fanned[0].size])
		var outer: Control = fanned[0]
		game._on_card_hovered(outer.get_meta("card_id"), outer)
		await create_timer(0.25).timeout
		check(is_zero_approx(outer.rotation) and outer.get_index() == fanned.size() - 1, "A hovered fanned card straightens and comes to the front")
		game._on_card_unhovered(outer.get_meta("card_id"), outer)
		await create_timer(0.25).timeout
		check(outer.get_index() == 0 and outer.rotation < 0.0, "It returns to its place in the fan")
	var layout_saved := ConfigFile.new()
	check(layout_saved.load(Preferences.save_path) == OK and layout_saved.get_value("display", "hand_layout", "") == "fan", "The hand layout persists")
	game.hand_layout_button.emit_signal("pressed")
	for i in range(4): await process_frame
	check(Preferences.hand_layout == "row" and not game.hand_box.has_node("FanRow"), "Pressing again returns to the row")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(Preferences.save_path))
	print("HAND BACKDROP %s: toggle hides chrome, keeps cards/reroll/pile, extends the station view and passes clicks" % ("PASS" if failures == 0 else "FAIL"))
	quit(1 if failures else 0)

func _first_card(game) -> Control:
	for slot in game.hand_box.get_children():
		for child in slot.get_children():
			if child.has_meta("card_id"): return child
	return null

func _core_on_screen(game) -> Vector2:
	return game.grid_view.get_global_transform() * ((Vector2(20, 20) + Vector2.ONE * 0.5) * game.get_cell_size())

func _click(point: Vector2) -> void:
	for pressed in [true, false]:
		var event := InputEventMouseButton.new()
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = pressed
		event.position = point
		event.global_position = point
		root.push_input(event, true)

func _hand_control_at(game, point: Vector2) -> bool:
	for node in game.hand_panel.find_children("*", "Control", true, false):
		if node is BaseButton or (node is PanelContainer and node.get_parent() == game.hand_box):
			if node.is_visible_in_tree() and node.get_global_rect().has_point(point): return true
	return false
