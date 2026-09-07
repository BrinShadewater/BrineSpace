extends RefCounted
## Optional presentation state. Invalid fields fall back without rejecting a loop.
static func capture(game) -> Dictionary:
	var positions: Dictionary = game.journal_scroll_positions.duplicate()
	positions[game.journal_tabs.current_tab] = game.archive_label.get_v_scroll_bar().value
	var searches: Dictionary = game.journal_searches.duplicate()
	if game.journal_tabs.current_tab in [3,4]: searches[game.journal_tabs.current_tab] = game.history_search.text
	var sidebar = game.get_node_or_null("Root/SideScroll")
	return {"version":1,"camera_center":game._grid_view_center_ratio(),"tab":game.journal_tabs.current_tab,"scrolls":positions,"searches":searches,"filter":game.history_filter.selected,"resource":game.inspected_resource,"inspector":game.inspector_label.get_v_scroll_bar().value,"sidebar":sidebar.scroll_vertical if sidebar else 0}

static func number(value: Variant, fallback := 0.0) -> float:
	return clampf(float(value),0.0,100000.0) if (value is float or value is int) and is_finite(float(value)) else fallback

static func center(game, checkpoint: Dictionary) -> Vector2:
	var workspace: Variant = checkpoint.get("workspace",{})
	if workspace is Dictionary and workspace.get("version")==1:
		var saved: Variant = workspace.get("camera_center")
		if saved is Vector2 and saved.is_finite(): return saved.clamp(Vector2.ZERO,Vector2.ONE)
	return ((Vector2(checkpoint.scroll)+game.grid_scroll.size*0.5)/(game.GRID_SIZE*game.get_cell_size())).clamp(Vector2.ZERO,Vector2.ONE)

static func restore(game, value: Variant) -> void:
	if not value is Dictionary or value.get("version")!=1: return
	var tab := clampi(int(number(value.get("tab"))),0,game.journal_tabs.tab_count-1)
	game.journal_scroll_positions.clear()
	game.journal_searches.clear()
	for index in range(game.journal_tabs.tab_count):
		if value.get("scrolls") is Dictionary: game.journal_scroll_positions[index] = number(value.scrolls.get(index))
		if index in [3,4] and value.get("searches") is Dictionary and value.searches.get(index) is String:
			game.journal_searches[index] = value.searches[index].left(128)
	game.journal_tabs.set_block_signals(true)
	game.journal_tabs.current_tab = tab
	game.journal_tabs.set_block_signals(false)
	game.journal_last_tab = tab
	game.history_search.set_block_signals(true)
	game.history_search.text = str(game.journal_searches.get(tab,""))
	game.history_search.set_block_signals(false)
	game.history_filter.select(clampi(int(number(value.get("filter"))),0,3))
	var resource: Variant = value.get("resource","")
	game.inspected_resource = resource if resource is String and game.BASE_STORAGE_CAPACITY.has(resource) else ""
	game._refresh_archive()
	game.archive_label.get_v_scroll_bar().set_deferred("value",float(game.journal_scroll_positions.get(tab,0.0)))
	game.inspector_label.get_v_scroll_bar().set_deferred("value",number(value.get("inspector")))
	var sidebar = game.get_node_or_null("Root/SideScroll")
	if sidebar: sidebar.set_deferred("scroll_vertical",int(number(value.get("sidebar"))))
