extends SceneTree
## Native-size badge board; always run through the isolated APPDATA wrapper.
const Style = preload("res://scripts/title_button_style.gd")
const Widgets = preload("res://scripts/ui_widgets.gd")
const Badges = preload("res://scripts/ui_badges.gd")
const Database = preload("res://scripts/room_database.gd")
var checks := 0
var failures := 0
var samples: Array[PanelContainer] = []
func _initialize() -> void: run.call_deferred()
func check(value: bool, message: String) -> void:
	checks += 1
	if not value:
		failures += 1
		push_error(message)
func heading(text: String, size := 18) -> Label:
	var result := Widgets.text_label(text,size)
	result.autowrap_mode = TextServer.AUTOWRAP_OFF
	return result
func family(grid: GridContainer, title: String, detail: String) -> VBoxContainer:
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(668,220)
	grid.add_child(panel)
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation",16)
	panel.add_child(body)
	body.add_child(heading(title,21))
	body.add_child(Widgets.text_label(detail,15,true))
	return body
func line(body: VBoxContainer, entries: Array, compact := false) -> void:
	var flow := HFlowContainer.new()
	flow.add_theme_constant_override("h_separation",10)
	flow.add_theme_constant_override("v_separation",10)
	body.add_child(flow)
	for entry in entries:
		var item := Badges.make(entry[0],entry[1],entry[2],entry[3] if entry.size()>3 else -1,compact)
		flow.add_child(item)
		samples.append(item)
func run() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://output/ui-badges-2026-10-02"))
	var viewport := SubViewport.new()
	viewport.size = Vector2i(1440,900)
	viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var stage := Control.new()
	stage.theme = Style.menu_theme()
	stage.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	viewport.add_child(stage)
	var background := ColorRect.new()
	background.color = Color("0a1d25")
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	stage.add_child(background)
	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left","right","top","bottom"]: margin.add_theme_constant_override("margin_"+side,28)
	stage.add_child(margin)
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation",18)
	margin.add_child(body)
	body.add_child(heading("BRINESPACE / BADGES",30))
	body.add_child(Widgets.text_label("Matte inset plates  ·  muted department paint  ·  original icon artwork  ·  native display sizes",17,true))
	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation",18)
	grid.add_theme_constant_override("v_separation",18)
	body.add_child(grid)
	var rooms := family(grid,"ROOM STATUS","Readable state labels with a small, quiet painted rim.")
	line(rooms,[["Online","power","online"],["Paused","pause","disabled"],["Needs repair","repair","warning"]])
	line(rooms,[["No input","warning","warning"],["Hull intact","hull_intact","online"]],true)
	var crew := family(grid,"CREW ACTIVITY","Compact enough for a portrait row or expanded character panel.")
	line(crew,[["Working","working","online"],["Resting","resting","normal"],["Idle","idle","normal"]])
	line(crew,[["Unassigned","unassigned","warning"],["Assigned","assigned_room","online"]],true)
	var research := family(grid,"ARCHIVE & RESEARCH","Clear labels for existing discovery and ownership states.")
	line(research,[["Discovered","search","research"],["Stabilized","confirm","online"]])
	line(research,[["Locked","locked","disabled"],["Owned","unlocked","online"],["Archived data","archived_data","normal",8]],true)
	var alerts := family(grid,"ALERTS & COUNTS","Muted warning colours; labels and symbols carry the meaning.")
	line(alerts,[["Low reserve","warning","warning"],["Fault","diagnostics","danger"],["Fire","fire","danger"]])
	line(alerts,[["New records","journal","research",3],["Crew","crew","normal",12],["Alerts","warning","warning",108]],true)
	var departments := family(grid,"DEPARTMENT TAGS","Existing department colours softened for the interface.")
	var dept_flow := HFlowContainer.new()
	dept_flow.add_theme_constant_override("h_separation",10)
	dept_flow.add_theme_constant_override("v_separation",10)
	departments.add_child(dept_flow)
	for entry in [["Engineering","repair"],["Life Support","oxygen"],["Science","sensor"],["Operations","diagnostics"],["Recreation","resting"],["Anomaly","anomaly"],["Robotics","data"]]:
		var item := Badges.department(entry[0],entry[1],Database.CATEGORY_COLORS[entry[0]],true)
		dept_flow.add_child(item)
		samples.append(item)
	var density := family(grid,"SIZE & DENSITY","36 px standard / 28 px compact. Count segments keep their own space.")
	line(density,[["Archived data","archived_data","normal",28]])
	line(density,[["Archived data","archived_data","normal",28],["Online","power","online"]],true)
	for frame in range(5): await process_frame
	await RenderingServer.frame_post_draw
	check(grid.get_global_rect().end.y <= 900,"Board fits viewport")
	for item in samples:
		check(item.get_node("Content/Icon").texture != null,"Badge icon exists")
		check(item.get_node("Content").get_global_rect().end.x <= item.get_global_rect().end.x,"Badge contents fit plate")
		check(item.get_node("Content/Caption").size.y >= item.get_node("Content/Caption").get_minimum_size().y,"Caption fits height")
	var capped := Badges.make("Alerts","warning","warning",108)
	check(capped.get_node("Content/Count").text == "99+","Large counts retain compact cap")
	capped.free()
	var zero := Badges.make("Crew","crew","normal",0)
	check(zero.get_node("Content/Count").text == "0","Zero count remains visible")
	zero.free()
	var absent := Badges.make("Idle","idle")
	check(not absent.has_node("Content/Count"),"Omitted count creates no segment")
	absent.free()
	check(viewport.get_texture().get_image().save_png("res://output/ui-badges-2026-10-02/badges-audition.png") == OK,"Board saves")
	print("BADGE AUDITION: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
