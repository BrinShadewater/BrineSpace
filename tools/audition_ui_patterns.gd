extends SceneTree
## Native widget audition and layout checks. Run with a scratch APPDATA profile.
const Style = preload("res://scripts/title_button_style.gd")
const Widgets = preload("res://scripts/ui_widgets.gd")
var viewport: SubViewport
var checks := 0
func check(value: bool, message: String) -> void:
	checks += 1
	if not value: push_error(message); quit(1)
func _initialize() -> void: run.call_deferred()
func label(text: String, size := 18) -> Label:
	var node := Label.new()
	node.text = text
	node.add_theme_font_size_override("font_size",size)
	node.add_theme_color_override("font_color",Color("d5dcd7"))
	return node
func sample(parent: GridContainer, title: String, hint: String) -> VBoxContainer:
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(668,270)
	panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(panel)
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation",12)
	panel.add_child(body)
	body.add_child(label(title,21))
	var caption := label(hint,15)
	caption.add_theme_color_override("font_color",Color("80979b"))
	body.add_child(caption)
	return body
func run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://output/ui-components-extended-2026-10-01"))
	viewport = SubViewport.new()
	viewport.size = Vector2i(1440,1100)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var stage := Control.new()
	stage.theme = Style.menu_theme()
	stage.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	stage.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	viewport.add_child(stage)
	var background := ColorRect.new()
	background.color = Color("0a1d25")
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	stage.add_child(background)
	var margins := MarginContainer.new()
	margins.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left","right","top","bottom"]: margins.add_theme_constant_override("margin_"+side,28)
	stage.add_child(margins)
	var stack := VBoxContainer.new()
	stack.add_theme_constant_override("separation",18)
	margins.add_child(stack)
	stack.add_child(label("BRINESPACE / MATCHING COMPONENTS II",30))
	stack.add_child(label("Matte gunmetal  ·  muted petrol  ·  cream type  ·  restrained indicator lights",17))
	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation",18)
	grid.add_theme_constant_override("v_separation",18)
	stack.add_child(grid)
	var notes := sample(grid,"NOTIFICATIONS & WARNINGS","A shared message hierarchy with restrained state indicators.")
	notes.add_child(Widgets.notice("PATTERN STABILIZED","A recovered pattern will carry into the next loop.","confirm","selected"))
	notes.add_child(Widgets.notice("OXYGEN RESERVE LOW","Inspect the room forecast before the next cycle.","oxygen","warning"))
	var confirmations := sample(grid,"CONFIRMATION CARDS","Clear consequence text, familiar actions and roomy spacing.")
	var dialog := Widgets.confirmation("REPAIR HULL?","Spend 2 Metal to seal this room’s damaged boundary.","REPAIR HULL")
	confirmations.add_child(dialog)
	var portraits := sample(grid,"PORTRAIT LIST ROWS","Your original portraits, with a quiet selected-row treatment.")
	var Architects = preload("res://scripts/architects.gd")
	var portrait := Architects.selection_portrait("bill")
	var selected_row := Widgets.portrait_row("MAJOR BILL","Primary workplace: BRINE Core",portrait,true)
	portraits.add_child(selected_row)
	portraits.add_child(Widgets.portrait_row("DR. VELD","Awaiting assignment",Architects.selection_portrait("veld")))
	var loading_body := sample(grid,"LOADING & MULTI-STAGE STATUS","Progress and stage labels without bright flashing signals.")
	var loading := Widgets.loading("SCANNING ARCHIVE","8 of 18 records indexed",44)
	loading_body.add_child(loading)
	var stages := HBoxContainer.new()
	stages.add_theme_constant_override("separation",8)
	loading_body.add_child(stages)
	for item in [["MAPPED","selected"],["INDEXING","normal"],["PENDING","disabled"]]: stages.add_child(Widgets.badge(item[0],item[1]))
	var empty_body := sample(grid,"EMPTY & FILTERED STATES","Short explanation and a direct route back to the content.")
	var empty := Widgets.empty_state("NO MATCHING SIGNALS","Clear the search and filter to scan this archive again.")
	empty_body.add_child(empty)
	var reset := Button.new()
	reset.text = "CLEAR SEARCH & FILTER"
	reset.custom_minimum_size.y = 38
	empty.get_node("Body").add_child(reset)
	var shortcuts := sample(grid,"SHORTCUT HINTS","Small metal keycaps alongside readable action labels.")
	for pair in [["Fit station","Recenter station view"],["Rotate blueprint","Rotate the selected blueprint"],["Pause","Pause or resume the loop"]]:
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation",14)
		row.add_child(Widgets.keycap(preload("res://scripts/title_settings.gd").key_name(pair[0])))
		row.add_child(Widgets.text_label(pair[1],16))
		shortcuts.add_child(row)
	for frame in range(5): await process_frame
	await RenderingServer.frame_post_draw
	check(selected_row.get_child(0).get_node("Portrait").texture == portrait,"Crew rows retain the supplied original portrait")
	check(selected_row.get_theme_stylebox("panel").state == "selected","Selected row uses the muted selected treatment")
	check(loading.get_node("Body/LoadingProgress").value == 44,"Loading display uses supplied progress")
	check(empty.name == "ArchiveEmptyState" and empty.get_node("Body").get_child_count() == 3,"Empty state accommodates caller actions")
	var accepted := {"value":false}
	var cancelled := {"value":false}
	dialog.get_node("Body/Actions/ConfirmAction").pressed.connect(func(): accepted.value = true)
	dialog.get_node("Body/Actions/CancelAction").pressed.connect(func(): cancelled.value = true)
	dialog.get_node("Body/Actions/ConfirmAction").pressed.emit()
	dialog.get_node("Body/Actions/CancelAction").pressed.emit()
	check(accepted.value and cancelled.value,"Confirmation actions remain connectable")
	check(grid.get_global_rect().end.y <= 1100,"Extended families fit audition")
	check(viewport.get_texture().get_image().save_png("res://output/ui-components-extended-2026-10-01/components-audition.png") == OK,"Extended audition saves")
	var archive = preload("res://scripts/title_archive.gd").new()
	archive.mode = "codex"
	archive.meta_state = preload("res://scripts/meta_state.gd").new()
	archive.meta_state.save_path = "user://extended-ui-meta.json"
	viewport.add_child(archive)
	await process_frame
	archive.search.text = "ui_fixture_no_such_signal_2731"
	archive._populate_cards()
	await process_frame
	viewport.size = Vector2i(1280,720)
	await process_frame
	await RenderingServer.frame_post_draw
	check(archive.find_child("ArchiveEmptyState",true,false) != null,"Actual Codex uses the matching empty-state component")
	var clear_button = archive.find_child("ResetCodexSearch",true,false)
	check(clear_button != null,"Actual Codex preserves Clear Search action")
	check(clear_button.get_global_rect().end.x <= viewport.size.x,"Codex empty-state action fits a compact window")
	check(viewport.get_texture().get_image().save_png("res://output/ui-components-extended-2026-10-01/codex-empty-state.png") == OK,"Actual compact Codex capture saves")
	clear_button.pressed.emit()
	check(archive.search.text.is_empty() and not archive.visible_entries.is_empty(),"Clearing the empty state restores Codex entries")
	archive.queue_free()
	await process_frame
	print("Matching components: %d checks PASS" % checks)
	quit()
