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
	panel.custom_minimum_size = Vector2(668,196)
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
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://output/ui-components-2026-10-01"))
	viewport = SubViewport.new()
	viewport.size = Vector2i(1440,1000)
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
	stack.add_child(label("BRINESPACE / MATCHING COMPONENTS",30))
	stack.add_child(label("Matte gunmetal  ·  muted petrol  ·  cream type  ·  restrained indicator lights",17))
	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation",18)
	grid.add_theme_constant_override("v_separation",18)
	stack.add_child(grid)
	var tabs_body := sample(grid,"TABS & SECTIONS","Clear selection with a painted inset and a small status strip.")
	var tabs := TabBar.new()
	for title in ["ROOMS","CREW","PATTERNS","LOCKED"]: tabs.add_tab(title)
	tabs.set_tab_disabled(3,true)
	tabs_body.add_child(tabs)
	var fields := sample(grid,"SEARCH & ENTRY","Recessed surfaces, readable placeholders and quiet focus.")
	var search := LineEdit.new()
	search.placeholder_text = "Search recovered rooms…"
	search.clear_button_enabled = true
	fields.add_child(search)
	var typed := LineEdit.new()
	typed.text = "Engineering"
	fields.add_child(typed)
	var sliders := sample(grid,"SLIDERS & METERS","Muted green-blue fill; the slider keeps its tactile metal handle.")
	var slider := HSlider.new()
	slider.value = 64
	slider.custom_minimum_size.y = 28
	sliders.add_child(slider)
	var meter := ProgressBar.new()
	meter.value = 64
	meter.custom_minimum_size.y = 24
	sliders.add_child(meter)
	var toggles := sample(grid,"TOGGLES & CHECKS","Matte metal switches, small indicator and clear check marks.")
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation",32)
	toggles.add_child(row)
	for enabled in [false,true]:
		var toggle := CheckButton.new()
		toggle.text = "ON" if enabled else "OFF"
		toggle.button_pressed = enabled
		toggle.add_theme_constant_override("icon_max_width",52)
		row.add_child(toggle)
	var check_row := HBoxContainer.new()
	toggles.add_child(check_row)
	for enabled in [false,true]:
		var box := CheckBox.new()
		box.text = "Show labels" if enabled else "Show guides"
		box.button_pressed = enabled
		check_row.add_child(box)
	var menus := sample(grid,"DROPDOWNS & MENU ROWS","Action buttons retain their hull fittings; menus stay compact.")
	var option := OptionButton.new()
	for caption in ["MEDIUM EFFECTS","LOW EFFECTS","HIGH EFFECTS"]: option.add_item(caption)
	menus.add_child(option)
	var choice := Label.new()
	choice.text = "✓  Medium effects                         Recommended"
	choice.add_theme_stylebox_override("normal",Widgets.surface("menu","hover"))
	menus.add_child(choice)
	var badges := sample(grid,"STATE BADGES","Small signals for ordinary, active, warning and fault states.")
	var badge_row := HBoxContainer.new()
	badge_row.add_theme_constant_override("separation",8)
	badges.add_child(badge_row)
	for entry in [["IDLE","normal"],["ONLINE","selected"],["LOW RESERVE","warning"],["OFFLINE","danger"]]:
		badge_row.add_child(Widgets.badge(entry[0],entry[1]))
	badges.add_child(label("The indicator carries the state; the label remains readable.",16))
	var tips := sample(grid,"TOOLTIPS & NOTICES","Thin matte edges around short, useful messages.")
	var tip := label("REPAIR HULL\nRestore this room’s sealed boundary. Requires 2 Metal.",17)
	tip.add_theme_stylebox_override("normal",Widgets.surface("field"))
	tips.add_child(tip)
	var scroll_body := sample(grid,"SCROLLING & LIST ROWS","Narrow rails with a readable metal grip and roomy entries.")
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size.y = 100
	scroll_body.add_child(scroll)
	var list := VBoxContainer.new()
	list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(list)
	for title in ["Life Support","Mining Drone Bay","Solar Array","Data Archive","Hydroponics Bay","Med Bay"]:
		var item := label(title,17)
		item.add_theme_stylebox_override("normal",Widgets.surface("field"))
		list.add_child(item)
	for frame in range(5): await process_frame
	await RenderingServer.frame_post_draw
	check(tabs.get_theme_stylebox("tab_selected").get_script() == preload("res://scripts/ui_component_style.gd"),"Tabs share the matte inset surface")
	check(search.get_theme_stylebox("normal").get_script() == preload("res://scripts/ui_component_style.gd"),"Fields share the matte inset surface")
	check(option.get_popup().get_theme_stylebox("panel").get_script() == preload("res://scripts/ui_component_style.gd"),"Dropdown popup inherits shared surface")
	check(stage.theme.get_stylebox("panel","PanelContainer").get_script() == preload("res://scripts/terminal_frame_style.gd"),"Previous panel frames remain intact")
	check(meter.get_theme_stylebox("fill").bg_color == Color("416d6d"),"Meters keep muted green-blue fill")
	tabs.current_tab = 1
	check(tabs.current_tab == 1,"Tabs remain interactive")
	slider.value = 35
	check(slider.value == 35,"Slider remains interactive")
	check(grid.get_global_rect().end.y <= 1000,"All component families fit audition")
	check(viewport.get_texture().get_image().save_png("res://output/ui-components-2026-10-01/components-audition.png") == OK,"Audition image saves successfully")
	print("Matching components: %d checks PASS" % checks)
	quit()
