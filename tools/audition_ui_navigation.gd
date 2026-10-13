extends SceneTree
## Native widget audition and layout checks. Run with a scratch APPDATA profile.
const Style = preload("res://scripts/title_button_style.gd")
const Widgets = preload("res://scripts/ui_widgets.gd")
var viewport: SubViewport
var checks := 0
var failures := 0
func check(value: bool, message: String) -> void:
	checks += 1
	if not value:
		failures += 1
		push_error(message)
func _initialize() -> void: run.call_deferred()
func label(text: String, size := 18) -> Label:
	var node := Label.new()
	node.text = text
	node.add_theme_font_size_override("font_size",size)
	node.add_theme_color_override("font_color",Color("d5dcd7"))
	return node
func sample(parent: GridContainer, title: String, hint: String) -> VBoxContainer:
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(668,250)
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
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://output/ui-navigation-2026-10-01"))
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
	stack.add_child(label("BRINESPACE / MATCHING COMPONENTS III",30))
	stack.add_child(label("Matte gunmetal  ·  muted petrol  ·  cream type  ·  restrained indicator lights",17))
	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation",18)
	grid.add_theme_constant_override("v_separation",18)
	stack.add_child(grid)
	var filter_body := sample(grid,"FILTER CHIPS","Compact choices that wrap instead of spilling off the panel.")
	var filters := Widgets.filter_chips(["ALL ROOMS","ENGINEERING","LIFE SUPPORT","SCIENCE"],1)
	filter_body.add_child(filters)
	filter_body.add_child(Widgets.text_label("Department filter  ·  one selection at a time",16,true))
	var resource_body := sample(grid,"RESOURCE READOUTS","Shared icons and readable amounts, with quiet cycle deltas.")
	var resources := HBoxContainer.new()
	resources.add_theme_constant_override("separation",12)
	resource_body.add_child(resources)
	for entry in [["metal",38,2],["oxygen",12,-1],["archived_data",8,0]]:
		var tile := Widgets.resource_tile(entry[0],entry[1],entry[2])
		tile.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		resources.add_child(tile)
	var route_body := sample(grid,"BREADCRUMB NAVIGATION","Small navigation links and a clearly marked current section.")
	var route := Widgets.breadcrumbs(["ARCHIVE","ROOMS","LIFE SUPPORT"])
	route_body.add_child(route)
	route_body.add_child(Widgets.text_label("Keep your place while inspecting a record.",16,true))
	var sorting_body := sample(grid,"SORTING CONTROLS","The active column shows direction; click it again to reverse.")
	var sort_seen := {"index":-1,"ascending":true}
	var sorting := Widgets.sort_controls(["NAME","COST","RARITY"],0,func(index: int, ascending: bool): sort_seen.index=index;sort_seen.ascending=ascending)
	sorting_body.add_child(sorting)
	sorting_body.add_child(Widgets.text_label("NAME ↑    Alphabetical order",16,true))
	var pages_body := sample(grid,"PAGINATION","Readable position with muted, disabled boundary controls.")
	var page_seen := {"value":-1}
	var pages := Widgets.pagination(8,0,func(page: int): page_seen.value=page)
	pages_body.add_child(pages)
	pages_body.add_child(Widgets.pagination(8,7))
	var details_body := sample(grid,"EXPANDABLE DETAILS","Quiet headers reveal additional information when needed.")
	var summary := Widgets.text_label("A functioning room must have its required inputs. Check the next-cycle forecast for interruptions.",16,true)
	var details := Widgets.disclosure("NEXT CYCLE / DETAILS",summary,true)
	details_body.add_child(details)
	details_body.add_child(Widgets.disclosure("KNOWN PATTERNS",Widgets.text_label("Recovered patterns appear here.",16,true)))
	for frame in range(5): await process_frame
	await RenderingServer.frame_post_draw
	check(grid.get_global_rect().end.y <= 1000,"Navigation families fit audition")
	check(viewport.get_texture().get_image().save_png("res://output/ui-navigation-2026-10-01/components-audition.png") == OK,"Navigation audition saves")
	check(filters.get_child(1).button_pressed,"Filter starts at supplied choice")
	filters.get_child(2).button_pressed = true
	check(filters.get_child(2).button_pressed and not filters.get_child(1).button_pressed,"Filters select exclusively")
	var invalid_filter := Widgets.filter_chips(["ALL","KNOWN"],99)
	stage.add_child(invalid_filter)
	check(invalid_filter.get_child(1).button_pressed,"Invalid filter index clamps to a real choice")
	invalid_filter.queue_free()
	check(resources.get_child(0).get_child(0).get_node("Amount").text == "38","Resource readout shows caller amount")
	check(resources.get_child(1).get_child(0).get_node("Change").text == "-1 / CYCLE","Negative resource delta remains explicit")
	check(resources.get_child(2).get_child(0).get_child(0).get_node("ResourceIcon").texture == preload("res://scripts/ui_icons.gd").texture("archived_data"),"Archived Data retains the new shared badge")
	var back := {"value":-1}
	route.get_child(0).pressed.connect(func(): back.value=int(route.get_child(0).get_meta("path_index")))
	route.get_child(0).pressed.emit()
	check(back.value == 0,"Breadcrumb routes expose caller-owned actions")
	check(route.get_child(route.get_child_count()-1) is Label,"Current route is a reading label")
	sorting.get_child(0).pressed.emit()
	check(not sort_seen.ascending and sort_seen.index == 0,"Clicking active sort reverses direction")
	sorting.get_child(1).pressed.emit()
	check(sort_seen.index == 1 and sort_seen.ascending,"Changing sort column starts ascending")
	check(sorting.get_child(1).button_pressed and not sorting.get_child(0).button_pressed,"Sorting has one active column")
	check(pages.get_node("PreviousPage").disabled,"Previous page is disabled at first page")
	pages.get_node("NextPage").pressed.emit()
	check(page_seen.value == 1 and pages.get_node("PageReadout").text == "2 / 8","Next page advances caller callback and readout")
	pages.get_node("PreviousPage").pressed.emit()
	check(page_seen.value == 0,"Previous page returns to first page")
	pages.get_node("PreviousPage").pressed.emit()
	check(pages.get_meta("page") == 0,"Pagination stays within lower bound")
	check(pages_body.get_child(3).get_node("NextPage").disabled,"Next page is disabled at last page")
	var none := Widgets.pagination(0,-3)
	stage.add_child(none)
	check(none.get_node("PreviousPage").disabled and none.get_node("NextPage").disabled,"Empty pagination has safe disabled boundaries")
	none.queue_free()
	check(summary.visible,"Expanded details show supplied content")
	details.get_node("DisclosureHeader").button_pressed = false
	check(not summary.visible,"Collapsing details hides content")
	details.get_node("DisclosureHeader").button_pressed = true
	check(summary.visible,"Expanding details restores content")
	var compact := Widgets.filter_chips(["ALL ROOMS","ENGINEERING","LIFE SUPPORT","SCIENCE"],0)
	compact.position = Vector2(20,20)
	compact.size = Vector2(320,180)
	stage.add_child(compact)
	await process_frame
	for button in compact.get_children(): check(button.get_global_rect().end.x <= compact.get_global_rect().end.x+.5,"Filter chip stays within compact width")
	check(compact.get_child(3).position.y > compact.get_child(0).position.y,"Filters wrap on compact panels")
	print("Navigation components: %d checks, %d failures" % [checks,failures])
	quit(1 if failures > 0 else 0)
