extends Control

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const SynergyManagerScript := preload("res://scripts/synergy_manager.gd")
const DiscoveryManagerScript := preload("res://scripts/discovery_manager.gd")
const OrbitManagerScript := preload("res://scripts/orbit_manager.gd")
const MetaStateScript := preload("res://scripts/meta_state.gd")
const GridCanvasScript := preload("res://scripts/grid_canvas.gd")
const RunManagerScript := preload("res://scripts/run_manager.gd")

const GRID_SIZE := 40
const CELL_SIZE := 720
const GRID_PIXEL_SIZE := GRID_SIZE * CELL_SIZE
const BASE_CYCLE_SECONDS := 20.0
const DISCOVERY_BURST_SECONDS := 1.2
const HAND_SIZE := 3
const REROLL_RECOVERY_CYCLES := 4
const REROLL_RECOVERY_CAP := 3
const DEFAULT_GRID_ZOOM := 0.855
const MIN_GRID_ZOOM := DEFAULT_GRID_ZOOM * 0.02
const UI_ACCENT := Color("#2d7f6b")
const UI_ACCENT_BRIGHT := Color("#4fa38d")
const UI_ACCENT_DARK := Color("#0d2f2b")
const UI_PANEL_LARGE := "res://brineui/panel_large_vertical_9slice.png"
const UI_PANEL_MEDIUM := "res://brineui/panel_medium_horizontal_9slice.png"
const UI_PANEL_TOOLTIP := "res://brineui/panel_small_tooltip_9slice.png"
const UI_PANEL_WARNING := "res://brineui/panel_warning_9slice.png"
const UI_PANEL_MINIMAL := "res://brineui/panel_minimal_9slice.png"
const UI_BUTTON_NORMAL := "res://brineui/button_normal.png"
const UI_BUTTON_HOVER := "res://brineui/button_hover.png"
const UI_BUTTON_PRESSED := "res://brineui/button_pressed.png"
const UI_DIVIDER_HORIZONTAL := "res://brineui/divider_horizontal.png"
const UI_DIVIDER_VERTICAL := "res://brineui/divider_vertical.png"
const UI_TERMINAL_PANEL := "res://brineui/terminal_panel_9slice.png"
const UI_TERMINAL_PANEL_LARGE := "res://brineui/terminal_panel_large_9slice.png"
const UI_TERMINAL_PANEL_WARNING := "res://brineui/terminal_panel_warning_9slice.png"
const UI_TERMINAL_BUTTON_NORMAL := "res://brineui/terminal_button_normal.png"
const UI_TERMINAL_BUTTON_HOVER := "res://brineui/terminal_button_hover.png"
const UI_TERMINAL_BUTTON_PRESSED := "res://brineui/terminal_button_pressed.png"
const UI_TERMINAL_DIVIDER_HORIZONTAL := "res://brineui/terminal_divider_horizontal.png"
const UI_TERMINAL_DIVIDER_VERTICAL := "res://brineui/terminal_divider_vertical.png"
const RESOURCE_TOOLTIPS := {
	"metal": "Build material for rooms, repairs, and station expansion.",
	"power": "Reserve energy. Powered rooms consume it each cycle.",
	"oxygen": "Life support supply consumed by crew.",
	"water": "Reclaimed water for advanced bio systems. Hover a learned pattern to inspect its yield.",
	"food": "Crew survival supply consumed each cycle.",
	"data": "Research currency for unlocks and recovered memories.",
	"biomass": "Organic stock for hydroponics, cloning, and bio rooms.",
	"rare": "Advanced construction material from unusual POIs.",
	"integrity": "Station hull condition. At zero, the reboot cycle fails.",
	"crew": "Living workers currently aboard the station.",
	"corruption": "Anomalous contamination risk."
}
const RESOURCE_ICON_PATHS := {
	"metal": "res://Brine icons/icons_64/resource_icon_metal_chunk.png",
	"power": "res://Brine icons/icons_64/resource_icon_power_lightning.png",
	"oxygen": "res://Brine icons/icons_64/resource_icon_o2.png",
	"water": "res://Brine icons/icons_64/resource_icon_water_drop.png",
	"food": "res://Brine icons/icons_64/resource_icon_leaf_food.png",
	"data": "res://Brine icons/icons_64/resource_icon_data.png",
	"biomass": "res://Brine icons/icons_64/resource_icon_biomass_growth.png",
	"rare_minerals": "res://Brine icons/icons_64/resource_icon_rare_minerals.png",
	"rare": "res://Brine icons/icons_64/resource_icon_rare_minerals.png",
	"integrity": "res://Brine icons/icons_64/resource_icon_integrity.png",
	"crew": "res://Brine icons/icons_64/resource_icon_crew.png",
	"corruption": "res://Brine icons/icons_64/resource_icon_corruption.png",
	"anomaly": "res://Brine icons/icons_64/anomaly_icon_spiral.png",
	"orbit": "res://Brine icons/icons_64/orbit_icon_moon_asteroid.png",
	"fire": "res://Brine icons/icons_64/status_icon_fire_flame.png",
	"freeze": "res://Brine icons/icons_64/status_icon_freeze_snowflake.png",
	"sensor": "res://Brine icons/icons_64/system_icon_eye_sensor.png"
}
const RESOLUTION_OPTIONS := [
	Vector2i(1280, 720),
	Vector2i(1600, 900),
	Vector2i(1920, 1080),
	Vector2i(2560, 1440)
]
const ROOM_ART_VARIANT_COUNTS := {
	"battery_array": 3,
	"corner": 9,
	"corridor": 6,
	"crew_hab": 4,
	"crew_lounge": 6,
	"hydroponics_bay": 4,
	"life_support": 2,
	"maintenance_bay": 2,
	"mining_drone_bay": 2,
	"reactor": 4,
	"research_lab": 2,
	"salvage_drone_bay": 2,
	"shield_generator": 3,
	"solar_array": 3,
	"storage_bay": 5,
	"xeno_lab": 2
}
const BASE_STORAGE_CAPACITY := {
	"metal": 40,
	"power": 12,
	"oxygen": 30,
	"water": 30,
	"food": 30,
	"data": 30,
	"biomass": 20,
	"rare_minerals": 10,
	"integrity": 100
}
const RESONANCE_TIERS := [
	{"name": "DORMANT", "threshold": 0, "reward": {}},
	{"name": "ALIGNED", "threshold": 30, "reward": {"metal": 4}},
	{"name": "RESONANT", "threshold": 90, "reward": {"data": 6}},
	{"name": "HARMONIC", "threshold": 180, "reward": {"rare_minerals": 2}},
	{"name": "TRANSCENDENT", "threshold": 320, "reward": {"data": 10, "integrity": 5}}
]

var resources := {
	"metal": 18,
	"power": 6,
	"oxygen": 8,
	"water": 0,
	"food": 8,
	"data": 0,
	"biomass": 2,
	"rare_minerals": 1,
	"integrity": 100
}
var run_earned := {}
var occupied := {}
var placed_rooms := []
var hand := []
var draw_pile: Array[String] = []
var discard_pile: Array[String] = []
var rerolls_remaining := 3
var reroll_recovery_progress := 0
var selected_doctrines: Array[String] = []
var pending_doctrines: Array[String] = []
var run_directives := []
var directive_index := 0
var completed_directives: Array[String] = []
var run_victory := false
var expedition_mode := false
var run_rewards_recorded := false
var run_awarded_research := 0
var selected_card_id := ""
var hovered_card_id := ""
var selected_rotation := 0
var selected_room_cell := Vector2i(-1, -1)
var hover_cell := Vector2i(-1, -1)
var cycle := 0
var crew_count := 0
var had_crew := false
var corruption := 0
var orbit_decay := 0
var active_synergies := {}
var connected_synergy_links := []
var active_synergy_links := []
var synergy_stabilization_progress := {}
var run_discovered_synergy_ids: Array[String] = []
var run_stabilized_synergy_ids: Array[String] = []
var run_decrypted_blueprint_ids: Array[String] = []
var prototype_card_seen_cycle := {}
var discovery_bursts := []
var resonance_score := 0
var resonance_tier_index := 0
var links_formed := 0
var largest_cascade := 0
var last_cascade_size := 0
var meta := MetaStateScript.new()
var orbit := OrbitManagerScript.new()
var rng := RandomNumberGenerator.new()
var running := true
var admin_mode := false
var testing_free_build := false
var testing_disable_failures := false
var grid_zoom := DEFAULT_GRID_ZOOM * 0.52
var paused := false
var menu_open := false
var pause_before_menu := false
var visual_time_seconds := 0.0
var time_speed_index := 0
var time_speeds := [1.0, 2.0, 4.0]
var completed_pois := []
var expired_pois := []
var power_generated := 0
var power_used := 0
var power_capacity := 12
var unpowered_rooms := []
var powered_room_cells := {}
var unpowered_room_cells := {}
var offline_reasons := {}
var last_cycle_delta := {}
var test_walker_cell := Vector2i(-1, -1)
var test_walker_next_cell := Vector2i(-1, -1)
var test_walker_previous_cell := Vector2i(-1, -1)
var test_walker_progress := 0.0
var test_walker_speed := 0.10
var test_walker_state := "idle"
var test_walker_break_timer := 0.0
var test_walker_direction := "south"

var grid_view: Control
var grid_scroll: ScrollContainer
var resource_bar: Container
var cycle_label: Label
var resonance_label: Label
var hand_box: HBoxContainer
var hand_count_label: Label
var reroll_button: Button
var preview_texture: TextureRect
var preview_name_label: Label
var preview_tags_label: Label
var inspector_label: RichTextLabel
var orbital_objective_label: Label
var archive_label: RichTextLabel
var journal_layer: CanvasLayer
var journal_button: Button
var pause_before_journal := false
var room_operation_button: Button
var routing_label: Label
var log_label: RichTextLabel
var placement_label: Label
var controls_state_label: Label
var zoom_label: Label
var zoom_slider: HSlider
var pause_button: Button
var speed_buttons := []
var view_mode_button: Button
var solar_meter: ProgressBar
var solar_time_label: Label
var cascade_toast: PanelContainer
var cascade_toast_label: Label
var cascade_toast_tween: Tween
var toast_messages: Array[String] = []
var toast_playing := false
var summary_layer: CanvasLayer
var summary_panel: PanelContainer
var summary_title_label: Label
var summary_text: Label
var continue_expedition_button: Button
var end_expedition_button: Button
var doctrine_layer: CanvasLayer
var doctrine_buttons := {}
var doctrine_selection_label: Label
var doctrine_pair_preview_label: Label
var doctrine_confirm_button: Button
var menu_layer: CanvasLayer
var menu_panel: PanelContainer
var menu_status_label: Label
var resolution_buttons: Array[Button] = []
var borderless_fullscreen_button: Button
var last_preview_room_id := ""
var last_previewing_card := false
var last_windowed_resolution := Vector2i(2560, 1440)
var resource_labels := {}
var resource_chips := {}
var resource_icon_rects := {}

var tick_timer: Timer
var log_lines := []
var card_textures := {}
var ui_textures := {}
var resource_icon_textures := {}
var room_texture_paths := {
	"battery_array": "res://rooms/batteryarray.png",
	"biodome": "res://rooms/biodome.png",
	"clone_lab": "res://rooms/clonelab.png",
	"brine_core": "res://rooms/brinecore.png",
	"crew_hab": "res://rooms/crewhab.png",
	"cryo_chamber": "res://rooms/cryolab.png",
	"data_archive": "res://rooms/holographiccore.png",
	"hydroponics_bay": "res://rooms/hydroponics.png",
	"life_support": "res://rooms/lifesupport1.png",
	"mining_drone_bay": "res://rooms/miningdronebay.png",
	"ore_refinery": "res://rooms/orerefinery.png",
	"quarantine_cell": "res://rooms/quaratinecell.png",
	"reactor": "res://rooms/reactor.png",
	"research_lab": "res://rooms/researchlab2.png",
	"salvage_drone_bay": "res://rooms/salvagedronebay1.png",
	"solar_array": "res://rooms/solararray.png",
	"storage_bay": "res://rooms/storagebay1.png",
	"med_bay": "res://rooms/medbay.png",
	"xeno_lab": "res://rooms/xenolab.png",
	"anomaly_lab": "res://rooms/anomolylab.png",
	"bio_lab": "res://rooms/biolab.png",
	"command_center": "res://rooms/commandcenter.png",
	"corridor": "res://rooms/corridor1.png",
	"corner": "res://rooms/corner.png",
	"crew_lounge": "res://rooms/crewlounge1.png",
	"holographic_core": "res://rooms/holographiccore.png",
	"maintenance_bay": "res://rooms/maintenancebay.png",
	"med_center": "res://rooms/medcenter.png",
	"med_office": "res://rooms/medoffice.png",
	"radio_lab": "res://rooms/radiolab.png",
	"shield_generator": "res://rooms/sheildgenerator1.png"
}

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_configure_window_scaling()
	rng.randomize()
	_apply_ui_font()
	_load_ui_textures()
	_load_resource_icon_textures()
	_load_card_textures()
	_build_ui()
	_start_reboot_cycle()

func _configure_window_scaling() -> void:
	var window := get_window()
	window.content_scale_size = Vector2i(1920, 1080)
	window.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	window.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_EXPAND
	window.min_size = Vector2i(960, 540)

func _apply_ui_font() -> void:
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Cascadia Mono", "Consolas", "Lucida Console"])
	font.font_weight = 500
	var ui_theme := Theme.new()
	ui_theme.default_font = font
	ui_theme.default_font_size = 14
	theme = ui_theme

func _process(delta: float) -> void:
	_update_discovery_bursts(delta)
	if running and not paused:
		visual_time_seconds += delta * time_speeds[time_speed_index]
		_update_test_walker(delta * time_speeds[time_speed_index])
	_update_camera_pan(delta)
	_refresh_solar_meter()

func _build_ui() -> void:
	var backdrop := ColorRect.new()
	backdrop.name = "SpaceBackdrop"
	backdrop.color = Color("#02060d")
	backdrop.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(backdrop)

	var root := Control.new()
	root.name = "Root"
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(root)

	var top_shell := PanelContainer.new()
	top_shell.name = "TopCommandBar"
	top_shell.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_shell.offset_bottom = 104
	root.add_child(top_shell)
	_apply_panel_style(top_shell, Color("#060b10"), Color("#15232c"))

	var top_bar := HBoxContainer.new()
	top_bar.name = "TopBar"
	top_bar.add_theme_constant_override("separation", 10)
	top_shell.add_child(top_bar)

	var identity := VBoxContainer.new()
	identity.custom_minimum_size = Vector2(172, 0)
	identity.add_theme_constant_override("separation", 0)
	top_bar.add_child(identity)
	var title := Label.new()
	title.text = "BrineSpace"
	title.add_theme_font_size_override("font_size", 26)
	title.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	title.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.9))
	identity.add_child(title)
	var subtitle := Label.new()
	subtitle.text = "RECOVER · CONNECT · DISCOVER"
	subtitle.add_theme_font_size_override("font_size", 10)
	subtitle.add_theme_color_override("font_color", Color("#536874"))
	identity.add_child(subtitle)

	var resources_row := GridContainer.new()
	resources_row.columns = 6
	resources_row.name = "Resources"
	resources_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	resources_row.add_theme_constant_override("h_separation", 6)
	resources_row.add_theme_constant_override("v_separation", 4)
	top_bar.add_child(resources_row)
	resource_bar = resources_row

	var cycle_status := Label.new()
	cycle_status.name = "CycleLabel"
	cycle_status.add_theme_font_size_override("font_size", 18)
	cycle_status.add_theme_color_override("font_color", Color("#c4d1da"))
	top_bar.add_child(cycle_status)
	cycle_label = cycle_status

	var resonance_chip := PanelContainer.new()
	resonance_chip.name = "ResonanceChip"
	resonance_chip.custom_minimum_size = Vector2(166, 54)
	resonance_chip.tooltip_text = "Placement cascades build Resonance. Stack several links with one room to score faster and unlock tier rewards."
	_apply_panel_style(resonance_chip, Color("#050d10"), Color("#285849"))
	top_bar.add_child(resonance_chip)
	var resonance_status := Label.new()
	resonance_status.name = "ResonanceLabel"
	resonance_status.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	resonance_status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	resonance_status.add_theme_font_size_override("font_size", 12)
	resonance_status.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	resonance_chip.add_child(resonance_status)
	resonance_label = resonance_status
	var journal := Button.new()
	journal.text = "JOURNAL [J]"
	journal.custom_minimum_size = Vector2(130, 44)
	journal.tooltip_text = "Your recovered patterns and their blueprint rewards. Reading pauses the station."
	journal.pressed.connect(_toggle_journal)
	_style_hud_button(journal, false)
	top_bar.add_child(journal)
	journal_button = journal

	var menu_button := Button.new()
	menu_button.text = "MENU"
	menu_button.custom_minimum_size = Vector2(82, 44)
	menu_button.pressed.connect(_toggle_menu)
	_style_hud_button(menu_button, false)
	top_bar.add_child(menu_button)

	var middle := Control.new()
	middle.name = "Center"
	middle.set_anchors_preset(Control.PRESET_FULL_RECT)
	middle.offset_top = 112
	middle.offset_right = -438
	middle.offset_bottom = -344
	root.add_child(middle)

	var grid_frame := PanelContainer.new()
	grid_frame.name = "GridFrame"
	grid_frame.set_anchors_preset(Control.PRESET_FULL_RECT)
	middle.add_child(grid_frame)
	_apply_panel_style(grid_frame, Color("#02060a"), Color("#101c25"))

	var scroll := ScrollContainer.new()
	scroll.name = "GridScroll"
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_SHOW_NEVER
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_SHOW_NEVER
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid_frame.add_child(scroll)
	grid_scroll = scroll

	var grid := GridCanvasScript.new()
	grid.name = "GridView"
	grid.custom_minimum_size = Vector2(GRID_SIZE * get_cell_size(), GRID_SIZE * get_cell_size())
	grid.cell_clicked.connect(_on_grid_clicked)
	grid.cell_secondary_clicked.connect(_on_grid_secondary_clicked)
	grid.cell_hovered.connect(_on_grid_hovered)
	scroll.add_child(grid)
	grid_view = grid

	var objective_panel := PanelContainer.new()
	objective_panel.name = "OrbitalObjective"
	objective_panel.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	objective_panel.offset_left = 24
	objective_panel.offset_top = -220
	objective_panel.offset_right = 370
	objective_panel.offset_bottom = -16
	middle.add_child(objective_panel)
	_apply_panel_style(objective_panel, Color("#071018"), Color("#152a35"))
	var objective_text := Label.new()
	objective_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	objective_text.add_theme_font_size_override("font_size", 13)
	objective_text.add_theme_color_override("font_color", Color("#8fa3ae"))
	objective_panel.add_child(objective_text)
	orbital_objective_label = objective_text

	var cascade_panel := PanelContainer.new()
	cascade_panel.name = "CascadeToast"
	cascade_panel.visible = false
	cascade_panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cascade_panel.set_anchors_preset(Control.PRESET_CENTER_TOP)
	cascade_panel.offset_left = -235
	cascade_panel.offset_top = 78
	cascade_panel.offset_right = 235
	cascade_panel.offset_bottom = 146
	_apply_panel_style(cascade_panel, Color("#061b18"), UI_ACCENT_BRIGHT)
	middle.add_child(cascade_panel)
	cascade_toast = cascade_panel
	var cascade_text := Label.new()
	cascade_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cascade_text.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	cascade_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	cascade_text.mouse_filter = Control.MOUSE_FILTER_IGNORE
	cascade_text.add_theme_font_size_override("font_size", 15)
	cascade_text.add_theme_color_override("font_color", Color("#b9f5df"))
	cascade_panel.add_child(cascade_text)
	cascade_toast_label = cascade_text

	var viewport_tools := HBoxContainer.new()
	viewport_tools.name = "ViewportTools"
	viewport_tools.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	viewport_tools.offset_left = -330
	viewport_tools.offset_top = 18
	viewport_tools.offset_right = -18
	viewport_tools.offset_bottom = 58
	viewport_tools.add_theme_constant_override("separation", 10)
	middle.add_child(viewport_tools)
	var recenter_button := Button.new()
	recenter_button.text = "FIT STATION [F]"
	recenter_button.pressed.connect(_fit_station_view)
	_style_hud_button(recenter_button, false)
	viewport_tools.add_child(recenter_button)
	var view_button := Button.new()
	view_button.text = "■ NORMAL VIEW"
	view_button.pressed.connect(_toggle_admin_view_button)
	_style_hud_button(view_button, false)
	viewport_tools.add_child(view_button)
	view_mode_button = view_button

	var side_scroll := ScrollContainer.new()
	side_scroll.name = "SideScroll"
	side_scroll.set_anchors_preset(Control.PRESET_RIGHT_WIDE)
	side_scroll.offset_left = -426
	side_scroll.offset_top = 112
	side_scroll.offset_right = -8
	side_scroll.offset_bottom = -8
	side_scroll.custom_minimum_size = Vector2(418, 0)
	side_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_SHOW_NEVER
	side_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_SHOW_NEVER
	root.add_child(side_scroll)

	var side := VBoxContainer.new()
	side.name = "SidePanel"
	side.custom_minimum_size = Vector2(396, 0)
	side.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	side.add_theme_constant_override("separation", 14)
	side_scroll.add_child(side)

	var inspector_panel := PanelContainer.new()
	inspector_panel.name = "PreviewPanel"
	inspector_panel.custom_minimum_size = Vector2(0, 480)
	side.add_child(inspector_panel)
	_apply_panel_style(inspector_panel, Color("#071018"), Color("#152a35"))
	var preview_box := VBoxContainer.new()
	preview_box.add_theme_constant_override("separation", 8)
	inspector_panel.add_child(preview_box)
	var preview_header := HBoxContainer.new()
	preview_box.add_child(preview_header)
	var preview_header_left := Label.new()
	preview_header_left.text = "■ PREVIEW"
	preview_header_left.add_theme_font_size_override("font_size", 16)
	preview_header_left.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	preview_header.add_child(preview_header_left)
	var preview_header_right := Label.new()
	preview_header_right.text = "ANALYSIS"
	preview_header_right.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	preview_header_right.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	preview_header_right.add_theme_font_size_override("font_size", 12)
	preview_header_right.add_theme_color_override("font_color", Color("#4f6470"))
	preview_header.add_child(preview_header_right)
	var preview_details := HBoxContainer.new()
	preview_details.add_theme_constant_override("separation", 14)
	preview_box.add_child(preview_details)
	var preview_image := TextureRect.new()
	preview_image.custom_minimum_size = Vector2(96, 96)
	preview_image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	preview_image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	preview_image.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	preview_details.add_child(preview_image)
	preview_texture = preview_image
	var preview_texts := VBoxContainer.new()
	preview_texts.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	preview_details.add_child(preview_texts)
	var preview_name := Label.new()
	preview_name.text = "No Selection"
	preview_name.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	preview_name.add_theme_font_size_override("font_size", 22)
	preview_name.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	preview_texts.add_child(preview_name)
	preview_name_label = preview_name
	var preview_tags := Label.new()
	preview_tags.text = "SYSTEM IDLE"
	preview_tags.add_theme_font_size_override("font_size", 11)
	preview_tags.add_theme_color_override("font_color", Color("#8a9a9a"))
	_add_label_panel_style(preview_tags, Color("#071018"), Color("#253946"))
	preview_texts.add_child(preview_tags)
	preview_tags_label = preview_tags
	var inspector_text := RichTextLabel.new()
	inspector_text.name = "Text"
	inspector_text.bbcode_enabled = true
	inspector_text.scroll_active = true
	inspector_text.fit_content = false
	inspector_text.custom_minimum_size = Vector2(0, 284)
	inspector_text.add_theme_color_override("default_color", Color("#8fa3ae"))
	inspector_text.add_theme_font_size_override("normal_font_size", 13)
	inspector_text.add_theme_font_size_override("bold_font_size", 14)
	inspector_text.add_theme_constant_override("line_separation", 2)
	preview_box.add_child(inspector_text)
	inspector_label = inspector_text
	room_operation_button = Button.new()
	room_operation_button.text = "SELECT A BUILT ROOM TO CONTROL"
	room_operation_button.custom_minimum_size.y = 34
	room_operation_button.pressed.connect(_toggle_inspected_room)
	_style_hud_button(room_operation_button, false)
	preview_box.add_child(room_operation_button)

	var routing_panel := PanelContainer.new()
	routing_panel.name = "RoutingPanel"
	routing_panel.visible = false
	routing_panel.custom_minimum_size = Vector2(0, 150)
	side.add_child(routing_panel)
	_apply_panel_style(routing_panel, Color("#071018"), Color("#152a35"))
	var routing_text := Label.new()
	routing_text.name = "Text"
	routing_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	routing_panel.add_child(routing_text)
	routing_label = routing_text

	var controls_panel := PanelContainer.new()
	controls_panel.name = "ControlsPanel"
	controls_panel.custom_minimum_size = Vector2(0, 170)
	side.add_child(controls_panel)
	_apply_panel_style(controls_panel, Color("#071018"), Color("#152a35"))
	var controls_box := VBoxContainer.new()
	controls_box.name = "ControlsBox"
	controls_box.add_theme_constant_override("separation", 8)
	controls_panel.add_child(controls_box)
	var controls_header := HBoxContainer.new()
	controls_box.add_child(controls_header)
	var controls_title := Label.new()
	controls_title.text = "■ CONTROLS"
	controls_title.add_theme_font_size_override("font_size", 16)
	controls_title.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	controls_header.add_child(controls_title)
	var controls_state := Label.new()
	controls_state.text = "RUNNING"
	controls_state.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	controls_state.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	controls_state.add_theme_font_size_override("font_size", 11)
	controls_state.add_theme_color_override("font_color", Color("#4f6470"))
	controls_header.add_child(controls_state)
	controls_state_label = controls_state
	var controls := HBoxContainer.new()
	controls.name = "Controls"
	controls.add_theme_constant_override("separation", 8)
	controls_box.add_child(controls)
	var pause_label := Label.new()
	pause_label.text = "TIME"
	pause_label.custom_minimum_size = Vector2(66, 0)
	pause_label.add_theme_color_override("font_color", Color("#4f6470"))
	controls.add_child(pause_label)
	var pause := Button.new()
	pause.name = "Pause"
	pause.text = "|| PAUSE"
	pause.toggle_mode = true
	pause.custom_minimum_size = Vector2(0, 42)
	pause.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	pause.pressed.connect(_toggle_pause)
	_style_hud_button(pause, false)
	controls.add_child(pause)
	pause_button = pause
	var speed_row := HBoxContainer.new()
	speed_row.add_theme_constant_override("separation", 8)
	controls_box.add_child(speed_row)
	var speed_label := Label.new()
	speed_label.text = "SPEED"
	speed_label.tooltip_text = "Controls cycle timer speed and station animation speed."
	speed_label.custom_minimum_size = Vector2(66, 0)
	speed_label.add_theme_color_override("font_color", Color("#4f6470"))
	speed_row.add_child(speed_label)
	for i in range(3):
		var speed_button := Button.new()
		speed_button.text = "%d x" % int(time_speeds[i])
		speed_button.toggle_mode = true
		speed_button.button_pressed = i == time_speed_index
		speed_button.pressed.connect(_set_time_speed.bind(i))
		_style_hud_button(speed_button, i == time_speed_index)
		speed_row.add_child(speed_button)
		speed_buttons.append(speed_button)

	var zoom_row := HBoxContainer.new()
	zoom_row.name = "ZoomControls"
	controls_box.add_child(zoom_row)
	var zoom_title := Label.new()
	zoom_title.text = "ZOOM"
	zoom_title.custom_minimum_size = Vector2(66, 0)
	zoom_title.add_theme_color_override("font_color", Color("#4f6470"))
	zoom_row.add_child(zoom_title)
	var zoom_control := HSlider.new()
	zoom_control.min_value = MIN_GRID_ZOOM / DEFAULT_GRID_ZOOM
	zoom_control.max_value = 1.0
	zoom_control.step = 0.01
	zoom_control.value = grid_zoom / DEFAULT_GRID_ZOOM
	zoom_control.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	zoom_control.value_changed.connect(_on_zoom_changed)
	_style_hud_slider(zoom_control)
	zoom_row.add_child(zoom_control)
	self.zoom_slider = zoom_control
	var zoom_value := Label.new()
	zoom_value.name = "ZoomValue"
	zoom_row.add_child(zoom_value)
	zoom_label = zoom_value

	var solar_row := HBoxContainer.new()
	solar_row.name = "SolarCycle"
	solar_row.add_theme_constant_override("separation", 8)
	controls_box.add_child(solar_row)
	var solar_title := Label.new()
	solar_title.text = "CYCLE"
	solar_title.tooltip_text = "Time remaining until the next automatic cycle."
	solar_title.custom_minimum_size = Vector2(66, 0)
	solar_title.add_theme_color_override("font_color", Color("#4f6470"))
	solar_row.add_child(solar_title)
	var solar_bar := ProgressBar.new()
	solar_bar.min_value = 0
	solar_bar.max_value = 1
	solar_bar.value = 1
	solar_bar.show_percentage = false
	solar_bar.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_style_hud_progress(solar_bar)
	solar_row.add_child(solar_bar)
	solar_meter = solar_bar
	var solar_label := Label.new()
	solar_label.text = "--"
	solar_label.custom_minimum_size = Vector2(48, 0)
	solar_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	solar_label.add_theme_color_override("font_color", Color("#8fa3ae"))
	solar_row.add_child(solar_label)
	solar_time_label = solar_label

	var placement_status := Label.new()
	placement_status.name = "PlacementStatus"
	placement_status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	placement_status.custom_minimum_size = Vector2(0, 56)
	placement_status.add_theme_color_override("font_color", Color("#9aa8b3"))
	controls_box.add_child(placement_status)
	placement_label = placement_status

	var log_panel := PanelContainer.new()
	log_panel.name = "NotificationsPanel"
	log_panel.custom_minimum_size = Vector2(0, 190)
	log_panel.size_flags_vertical = Control.SIZE_EXPAND_FILL
	side.add_child(log_panel)
	_apply_panel_style(log_panel, Color("#071018"), Color("#152a35"))
	var log_text := RichTextLabel.new()
	log_text.name = "Text"
	log_text.bbcode_enabled = true
	log_text.scroll_active = true
	log_text.add_theme_color_override("default_color", Color("#b8c6cf"))
	log_text.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.65))
	log_text.add_theme_font_size_override("normal_font_size", 12)
	log_text.add_theme_constant_override("line_separation", 3)
	log_text.custom_minimum_size = Vector2(0, 120)
	log_panel.add_child(log_text)
	log_label = log_text

	var bottom := PanelContainer.new()
	bottom.name = "BottomHand"
	bottom.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bottom.offset_left = 8
	bottom.offset_right = -438
	bottom.offset_top = -332
	bottom.offset_bottom = -8
	root.add_child(bottom)
	_apply_panel_style(bottom, Color("#071018"), Color("#15232c"))
	var bottom_box := HBoxContainer.new()
	bottom_box.add_theme_constant_override("separation", 18)
	bottom.add_child(bottom_box)
	var draft_status := VBoxContainer.new()
	draft_status.custom_minimum_size = Vector2(148, 0)
	draft_status.add_theme_constant_override("separation", 12)
	bottom_box.add_child(draft_status)
	var blueprint_title := Label.new()
	blueprint_title.text = "DRAFT HAND"
	blueprint_title.add_theme_font_size_override("font_size", 12)
	blueprint_title.add_theme_color_override("font_color", Color("#4f6470"))
	draft_status.add_child(blueprint_title)
	var hand_count := Label.new()
	hand_count.text = "%d/%d" % [HAND_SIZE, HAND_SIZE]
	hand_count.add_theme_font_size_override("font_size", 30)
	hand_count.add_theme_color_override("font_color", Color("#c4d1da"))
	draft_status.add_child(hand_count)
	hand_count_label = hand_count
	var draft_hint := Label.new()
	draft_hint.text = "Build to draw.\nRMB rerolls one.\nR rotates.\nSpace pauses."
	draft_hint.add_theme_font_size_override("font_size", 14)
	draft_hint.add_theme_color_override("font_color", Color("#536874"))
	draft_status.add_child(draft_hint)
	var discard_all_button := Button.new()
	discard_all_button.text = "REROLL HAND · 3"
	discard_all_button.custom_minimum_size = Vector2(150, 38)
	discard_all_button.pressed.connect(_discard_all_cards)
	_style_hud_button(discard_all_button, false)
	draft_status.add_child(discard_all_button)
	reroll_button = discard_all_button
	var card_row := HBoxContainer.new()
	card_row.name = "CardRow"
	card_row.add_theme_constant_override("separation", 12)
	card_row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bottom_box.add_child(card_row)
	hand_box = card_row

	summary_layer = CanvasLayer.new()
	summary_layer.name = "SummaryLayer"
	summary_layer.layer = 19
	summary_layer.visible = false
	add_child(summary_layer)
	var summary_shade := ColorRect.new()
	summary_shade.color = Color(0.0, 0.02, 0.04, 0.84)
	summary_shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	summary_shade.mouse_filter = Control.MOUSE_FILTER_STOP
	summary_layer.add_child(summary_shade)
	var summary_center := CenterContainer.new()
	summary_center.set_anchors_preset(Control.PRESET_FULL_RECT)
	summary_center.mouse_filter = Control.MOUSE_FILTER_STOP
	summary_layer.add_child(summary_center)
	var summary := PanelContainer.new()
	summary.name = "SummaryPanel"
	summary.custom_minimum_size = Vector2(760, 620)
	summary_center.add_child(summary)
	_apply_panel_style(summary, Color("#071018"), Color("#1f5260"))
	summary_panel = summary
	var summary_vbox := VBoxContainer.new()
	summary.add_child(summary_vbox)
	var summary_title := Label.new()
	summary_title.text = "Reboot Summary"
	summary_title.add_theme_font_size_override("font_size", 24)
	summary_vbox.add_child(summary_title)
	summary_title_label = summary_title
	var summary_scroll := ScrollContainer.new()
	summary_scroll.custom_minimum_size = Vector2(740, 480)
	summary_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	summary_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	summary_vbox.add_child(summary_scroll)
	var summary_body := Label.new()
	summary_body.name = "Text"
	summary_body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	summary_body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	summary_scroll.add_child(summary_body)
	summary_text = summary_body
	continue_expedition_button = Button.new()
	continue_expedition_button.text = "CONTINUE EXPEDITION · KEEP EXPERIMENTING"
	continue_expedition_button.custom_minimum_size.y = 44
	continue_expedition_button.pressed.connect(_continue_expedition)
	_style_hud_button(continue_expedition_button, true)
	summary_vbox.add_child(continue_expedition_button)
	var reboot_button := Button.new()
	reboot_button.text = "Start New Reboot Cycle"
	reboot_button.custom_minimum_size.y = 40
	_style_hud_button(reboot_button, false)
	reboot_button.pressed.connect(_start_reboot_cycle)
	summary_vbox.add_child(reboot_button)

	_build_journal_overlay()
	_build_doctrine_overlay()
	_build_menu_overlay()

	tick_timer = Timer.new()
	tick_timer.wait_time = _cycle_wait_seconds()
	tick_timer.timeout.connect(_on_tick_timer_timeout)
	add_child(tick_timer)
	tick_timer.start()
	tick_timer.paused = paused
	_apply_grid_zoom()
	_refresh_flow_controls()
	_hide_grid_scrollbars.call_deferred()

func _apply_panel_style(panel: PanelContainer, bg_color := Color(0.035, 0.055, 0.075, 0.92), border_color := Color(0.18, 0.28, 0.34, 0.9)) -> void:
	var panel_path := UI_TERMINAL_PANEL
	var patch_margin := 16
	if panel.name == "PreviewPanel" or panel.name == "NotificationsPanel" or panel.name == "SummaryPanel":
		panel_path = UI_TERMINAL_PANEL_LARGE
		patch_margin = 20
	if panel.name == "SummaryPanel":
		panel_path = UI_TERMINAL_PANEL_WARNING
	var texture_style := _make_texture_stylebox(panel_path, patch_margin, 26, 26, 22, 22)
	if texture_style != null:
		if panel.name == "TopCommandBar" or panel.name == "BottomHand" or panel.name == "GridFrame":
			texture_style.content_margin_left = 16
			texture_style.content_margin_right = 16
			texture_style.content_margin_top = 10
			texture_style.content_margin_bottom = 10
		elif panel.name == "ControlsPanel" or panel.name == "OrbitalObjective":
			texture_style.content_margin_left = 24
			texture_style.content_margin_right = 24
			texture_style.content_margin_top = 20
			texture_style.content_margin_bottom = 20
		elif panel.name == "PreviewPanel" or panel.name == "NotificationsPanel":
			texture_style.content_margin_left = 30
			texture_style.content_margin_right = 34
			texture_style.content_margin_top = 26
			texture_style.content_margin_bottom = 26
		panel.add_theme_stylebox_override("panel", texture_style)
		return
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.025, 0.035, 0.045, 0.90)
	style.border_color = Color(0.18, 0.25, 0.29, 0.92)
	style.border_width_left = 1
	style.border_width_top = 1
	style.border_width_right = 1
	style.border_width_bottom = 1
	style.corner_radius_top_left = 0
	style.corner_radius_top_right = 0
	style.corner_radius_bottom_left = 0
	style.corner_radius_bottom_right = 0
	style.content_margin_left = 24
	style.content_margin_right = 24
	style.content_margin_top = 20
	style.content_margin_bottom = 20
	if panel.name == "TopCommandBar" or panel.name == "BottomHand" or panel.name == "GridFrame":
		style.bg_color = Color(0.018, 0.028, 0.036, 0.84)
		style.content_margin_left = 18
		style.content_margin_right = 18
		style.content_margin_top = 12
		style.content_margin_bottom = 12
	if panel.name == "ControlsPanel" or panel.name == "OrbitalObjective":
		style.content_margin_left = 22
		style.content_margin_right = 22
		style.content_margin_top = 18
		style.content_margin_bottom = 18
	if panel.name == "PreviewPanel" or panel.name == "NotificationsPanel":
		style.content_margin_left = 28
		style.content_margin_right = 34
		style.content_margin_top = 24
		style.content_margin_bottom = 24
	panel.add_theme_stylebox_override("panel", style)

func _style_hud_button(button: BaseButton, active := false) -> void:
	var normal_style := _make_texture_stylebox(UI_TERMINAL_BUTTON_NORMAL, 12, 14, 14, 7, 7)
	var hover_style := _make_texture_stylebox(UI_TERMINAL_BUTTON_HOVER, 12, 14, 14, 7, 7)
	var pressed_style := _make_texture_stylebox(UI_TERMINAL_BUTTON_PRESSED, 12, 14, 14, 7, 7)
	if normal_style != null:
		button.add_theme_stylebox_override("normal", normal_style)
	if hover_style != null:
		button.add_theme_stylebox_override("hover", hover_style)
	if pressed_style != null:
		button.add_theme_stylebox_override("pressed", pressed_style)
	button.add_theme_color_override("font_color", Color("#83b894") if active else Color("#8a9a9a"))
	button.add_theme_color_override("font_hover_color", Color("#a8d7b0"))
	button.add_theme_color_override("font_pressed_color", Color("#d7f5d2"))
	button.add_theme_font_size_override("font_size", 12)

func _panel_texture_for(panel: PanelContainer) -> String:
	match panel.name:
		"TopCommandBar", "BottomHand", "GridFrame":
			return UI_PANEL_MEDIUM
		"SummaryPanel":
			return UI_PANEL_WARNING
		"OrbitalObjective", "ControlsPanel":
			return UI_PANEL_MEDIUM
		"PreviewPanel", "NotificationsPanel", "ArchivePanel", "RoutingPanel":
			return UI_PANEL_LARGE
		_:
			return UI_PANEL_LARGE

func _make_texture_stylebox(path: String, patch_margin: int, content_left: int, content_right: int, content_top: int, content_bottom: int) -> StyleBoxTexture:
	var texture: Texture2D = ui_textures.get(path)
	if texture == null:
		return null
	var style := StyleBoxTexture.new()
	style.texture = texture
	style.set_texture_margin(SIDE_LEFT, patch_margin)
	style.set_texture_margin(SIDE_RIGHT, patch_margin)
	style.set_texture_margin(SIDE_TOP, patch_margin)
	style.set_texture_margin(SIDE_BOTTOM, patch_margin)
	style.content_margin_left = content_left
	style.content_margin_right = content_right
	style.content_margin_top = content_top
	style.content_margin_bottom = content_bottom
	return style

func _style_hud_slider(slider: HSlider) -> void:
	var track := StyleBoxFlat.new()
	track.bg_color = Color("#0c1819")
	track.border_color = Color("#26383b")
	track.border_width_top = 1
	track.border_width_bottom = 1
	track.content_margin_top = 4
	track.content_margin_bottom = 4
	slider.add_theme_stylebox_override("slider", track)
	var grabber := StyleBoxFlat.new()
	grabber.bg_color = Color("#7fbf91")
	grabber.border_color = Color("#a7d9ad")
	grabber.border_width_left = 1
	grabber.border_width_top = 1
	grabber.border_width_right = 1
	grabber.border_width_bottom = 1
	grabber.corner_radius_top_left = 1
	grabber.corner_radius_top_right = 1
	grabber.corner_radius_bottom_left = 1
	grabber.corner_radius_bottom_right = 1
	slider.add_theme_stylebox_override("grabber_area", grabber)
	slider.add_theme_stylebox_override("grabber_area_highlight", grabber)

func _style_hud_progress(progress: ProgressBar) -> void:
	var background := StyleBoxFlat.new()
	background.bg_color = Color("#091314")
	background.border_color = Color("#26383b")
	background.border_width_left = 1
	background.border_width_top = 1
	background.border_width_right = 1
	background.border_width_bottom = 1
	background.corner_radius_top_left = 1
	background.corner_radius_top_right = 1
	background.corner_radius_bottom_left = 1
	background.corner_radius_bottom_right = 1
	progress.add_theme_stylebox_override("background", background)
	var fill := StyleBoxFlat.new()
	fill.bg_color = Color("#6fae79")
	fill.border_color = Color("#9fd0a5")
	fill.border_width_top = 1
	fill.border_width_bottom = 1
	progress.add_theme_stylebox_override("fill", fill)

func _build_journal_overlay() -> void:
	journal_layer = CanvasLayer.new()
	journal_layer.name = "DiscoveryJournal"
	journal_layer.layer = 18
	journal_layer.visible = false
	add_child(journal_layer)
	var shade := ColorRect.new()
	shade.color = Color(0.0, 0.02, 0.04, 0.88)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	journal_layer.add_child(shade)
	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	journal_layer.add_child(center)
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(940, 760)
	_apply_panel_style(panel, Color("#071018"), UI_ACCENT_BRIGHT)
	center.add_child(panel)
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation", 18)
	panel.add_child(body)
	var title := Label.new()
	title.text = "BRINE / DISCOVERY JOURNAL"
	title.add_theme_font_size_override("font_size", 26)
	title.add_theme_color_override("font_color", Color("#a9e7d4"))
	body.add_child(title)
	var subtitle := Label.new()
	subtitle.text = "Only what you have learned. No hidden recipes.\nKeep connected rooms supplied for 3 consecutive cycles to stabilize a pattern."
	subtitle.add_theme_color_override("font_color", Color("#92aeb8"))
	body.add_child(subtitle)
	archive_label = RichTextLabel.new()
	archive_label.bbcode_enabled = true
	archive_label.custom_minimum_size = Vector2(900, 570)
	archive_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
	archive_label.add_theme_font_size_override("normal_font_size", 16)
	archive_label.add_theme_constant_override("line_separation", 6)
	body.add_child(archive_label)
	var close := Button.new()
	close.text = "RETURN TO STATION  [J / ESC]"
	close.custom_minimum_size.y = 44
	close.pressed.connect(_toggle_journal)
	_style_hud_button(close, false)
	body.add_child(close)
	journal_layer.set_meta("close_button", close)

func _journal_is_open() -> bool:
	return journal_layer != null and journal_layer.visible

func _gameplay_input_blocked() -> bool:
	return menu_open or _journal_is_open() or (summary_layer != null and summary_layer.visible) or (doctrine_layer != null and doctrine_layer.visible)

func _toggle_journal() -> void:
	if journal_layer == null:
		return
	if _journal_is_open():
		journal_layer.visible = false
		_set_paused(pause_before_journal)
		return
	if _gameplay_input_blocked():
		return
	pause_before_journal = paused
	journal_layer.visible = true
	get_viewport().gui_release_focus()
	var close_button: Button = journal_layer.get_meta("close_button")
	close_button.grab_focus()
	_set_paused(true)
	_refresh_archive()

func _toggle_inspected_room() -> void:
	if _gameplay_input_blocked() or not running or room_operation_button == null:
		return
	var cell: Vector2i = room_operation_button.get_meta("cell", Vector2i(-1, -1))
	if not occupied.has(cell) or occupied[cell]["id"] == "brine_core":
		return
	var room: Dictionary = occupied[cell]
	room["suspended"] = not room.get("suspended", false)
	if room["suspended"]:
		powered_room_cells.erase(cell)
		offline_reasons[cell] = "SUSPENDED"
		unpowered_room_cells[cell] = true
		active_synergy_links = DiscoveryManagerScript.functioning_links(connected_synergy_links, powered_room_cells)
		active_synergies.clear()
		for link in active_synergy_links:
			active_synergies[link["id"]] = link
	_log("%s %s." % [room["display_name"], "suspended" if room["suspended"] else "scheduled to resume next cycle"], false)
	_refresh_all()

func _build_doctrine_overlay() -> void:
	doctrine_layer = CanvasLayer.new()
	doctrine_layer.name = "DoctrineLayer"
	doctrine_layer.layer = 18
	doctrine_layer.visible = false
	add_child(doctrine_layer)

	var shade := ColorRect.new()
	shade.color = Color(0.0, 0.02, 0.04, 0.88)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	shade.mouse_filter = Control.MOUSE_FILTER_STOP
	doctrine_layer.add_child(shade)

	var center := CenterContainer.new()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_STOP
	doctrine_layer.add_child(center)

	var panel := PanelContainer.new()
	panel.name = "DoctrinePanel"
	panel.custom_minimum_size = Vector2(930, 690)
	panel.mouse_filter = Control.MOUSE_FILTER_STOP
	center.add_child(panel)
	_apply_panel_style(panel, Color("#071018"), Color("#285849"))

	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 14)
	panel.add_child(box)
	var eyebrow := Label.new()
	eyebrow.text = "BRINE // REBOOT CONFIGURATION"
	eyebrow.add_theme_font_size_override("font_size", 12)
	eyebrow.add_theme_color_override("font_color", Color("#607784"))
	box.add_child(eyebrow)
	var title := Label.new()
	title.text = "Choose Two Station Doctrines"
	title.add_theme_font_size_override("font_size", 30)
	title.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	box.add_child(title)
	var intro := Label.new()
	intro.text = "Your doctrine pair determines this reboot's blueprint deck, combo routes, and mastery bonuses."
	intro.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	intro.add_theme_font_size_override("font_size", 14)
	intro.add_theme_color_override("font_color", Color("#9aabb2"))
	box.add_child(intro)

	var grid := GridContainer.new()
	grid.columns = 2
	grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 12)
	grid.add_theme_constant_override("v_separation", 12)
	box.add_child(grid)
	doctrine_buttons.clear()
	for doctrine_id_value in RunManagerScript.DOCTRINE_ORDER:
		var doctrine_id := str(doctrine_id_value)
		var button := Button.new()
		button.toggle_mode = true
		button.custom_minimum_size = Vector2(420, 98)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.focus_mode = Control.FOCUS_NONE
		button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.pressed.connect(_on_doctrine_button_pressed.bind(doctrine_id))
		grid.add_child(button)
		doctrine_buttons[doctrine_id] = button

	var pair_preview := Label.new()
	pair_preview.custom_minimum_size = Vector2(0, 42)
	pair_preview.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	pair_preview.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	pair_preview.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	pair_preview.add_theme_font_size_override("font_size", 11)
	pair_preview.add_theme_color_override("font_color", Color("#6f9c91"))
	box.add_child(pair_preview)
	doctrine_pair_preview_label = pair_preview

	var selection_status := Label.new()
	selection_status.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	selection_status.add_theme_font_size_override("font_size", 13)
	selection_status.add_theme_color_override("font_color", Color("#8fa3ae"))
	box.add_child(selection_status)
	doctrine_selection_label = selection_status
	var confirm := Button.new()
	confirm.text = "BEGIN REBOOT"
	confirm.custom_minimum_size = Vector2(0, 56)
	confirm.disabled = true
	confirm.pressed.connect(_confirm_doctrines)
	_style_hud_button(confirm, true)
	box.add_child(confirm)
	doctrine_confirm_button = confirm
	var footer := Label.new()
	footer.text = "Mastery persists between runs. Higher ranks grant starting resources when that doctrine is selected."
	footer.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	footer.add_theme_font_size_override("font_size", 11)
	footer.add_theme_color_override("font_color", Color("#536874"))
	box.add_child(footer)
	_refresh_doctrine_overlay()

func _on_doctrine_button_pressed(doctrine_id: String) -> void:
	if pending_doctrines.has(doctrine_id):
		pending_doctrines.erase(doctrine_id)
	elif pending_doctrines.size() < 2:
		pending_doctrines.append(doctrine_id)
	_refresh_doctrine_overlay()

func _refresh_doctrine_overlay() -> void:
	if doctrine_selection_label == null:
		return
	for doctrine_id_value in RunManagerScript.DOCTRINE_ORDER:
		var doctrine_id := str(doctrine_id_value)
		var button: Button = doctrine_buttons.get(doctrine_id)
		if button == null:
			continue
		var data: Dictionary = RunManagerScript.doctrine(doctrine_id)
		var mastery := meta.get_doctrine_mastery(doctrine_id)
		var rank := meta.get_doctrine_rank(doctrine_id)
		var next_threshold := meta.get_next_doctrine_rank_threshold(doctrine_id)
		var mastery_text := "MAX" if next_threshold < 0 else "%d/%d" % [mastery, next_threshold]
		button.text = "%s\n%s\nMASTERY R%d · %s  ·  RANK BONUS %s" % [
			data["name"],
			data["description"],
			rank,
			mastery_text,
			_format_cost(data.get("mastery_bonus", {})).to_upper()
		]
		button.tooltip_text = "Rank bonus: %s per rank" % _format_cost(data.get("mastery_bonus", {}))
		var selected := pending_doctrines.has(doctrine_id)
		button.set_pressed_no_signal(selected)
		button.disabled = pending_doctrines.size() >= 2 and not selected
		_style_hud_button(button, selected)
	doctrine_selection_label.text = "%d/2 SELECTED%s" % [
		pending_doctrines.size(),
		"  ·  %s" % RunManagerScript.doctrine_pair_name(pending_doctrines) if not pending_doctrines.is_empty() else ""
	]
	if doctrine_pair_preview_label != null:
		doctrine_pair_preview_label.text = _doctrine_pair_preview_text()
	doctrine_confirm_button.disabled = pending_doctrines.size() != 2

func _doctrine_pair_preview_text() -> String:
	if pending_doctrines.size() < 2:
		return "Select one more doctrine to reveal deck breadth, crossover rooms, and available link patterns." if pending_doctrines.size() == 1 else "Pair profile will reveal deck breadth, crossover rooms, and available link patterns."
	var deck := RunManagerScript.build_deck(pending_doctrines, meta.unlocked_room_ids)
	var unique_rooms := {}
	for room_id_value in deck:
		unique_rooms[str(room_id_value)] = true
	var possible_synergies: Array[String] = []
	for synergy_value in SynergyManagerScript.all_synergies():
		var synergy: Dictionary = synergy_value
		if not meta.discovered_synergy_ids.has(str(synergy.get("id", ""))):
			continue
		var available := true
		for room_id_value in synergy.get("rooms", []):
			var room_id := str(room_id_value)
			if room_id != "brine_core" and not unique_rooms.has(room_id):
				available = false
				break
		if available:
			possible_synergies.append(str(synergy.get("name", "Unknown Pattern")))
	var first_rooms: Array = RunManagerScript.doctrine(str(pending_doctrines[0])).get("rooms", [])
	var second_rooms: Array = RunManagerScript.doctrine(str(pending_doctrines[1])).get("rooms", [])
	var crossover_names: Array[String] = []
	for room_id_value in first_rooms:
		var room_id := str(room_id_value)
		if second_rooms.has(room_id) and unique_rooms.has(room_id):
			crossover_names.append(str(RoomDatabaseScript.get_room(room_id).get("display_name", room_id)))
	var crossover_text := _preview_name_list(crossover_names, 3) if not crossover_names.is_empty() else "complementary pools"
	return "PAIR PROFILE  ·  %d BLUEPRINTS  ·  %d UNIQUE ROOMS  ·  %d LEARNED LINK PATTERNS\nCROSSOVER  %s  ·  LEARNED ROUTES  %s" % [
		deck.size(),
		unique_rooms.size(),
		possible_synergies.size(),
		crossover_text,
		_preview_name_list(possible_synergies, 3)
	]

func _preview_name_list(names: Array[String], visible_count: int) -> String:
	var visible_names: Array[String] = []
	for index in range(mini(names.size(), visible_count)):
		visible_names.append(names[index])
	var text := " · ".join(visible_names)
	if names.size() > visible_count:
		text += " +%d" % (names.size() - visible_count)
	return text if not text.is_empty() else "none"

func _show_doctrine_selection() -> void:
	pending_doctrines.clear()
	running = false
	_set_paused(true, false)
	doctrine_layer.visible = true
	_refresh_doctrine_overlay()

func _confirm_doctrines() -> void:
	if pending_doctrines.size() != 2:
		return
	selected_doctrines.assign(pending_doctrines)
	doctrine_layer.visible = false
	_build_run_deck()
	_roll_run_directives()
	_apply_doctrine_mastery_bonuses()
	_draw_hand()
	running = true
	_set_paused(false, false)
	_log("Reboot doctrines locked: %s." % RunManagerScript.doctrine_pair_name(selected_doctrines), false)
	_log("Directive 1/3 received: %s." % _current_directive().get("name", "Unknown"))
	_refresh_all()

func _apply_doctrine_mastery_bonuses() -> void:
	var total_bonus := {}
	for doctrine_id_value in selected_doctrines:
		var doctrine_id := str(doctrine_id_value)
		var rank := meta.get_doctrine_rank(doctrine_id)
		if rank <= 0:
			continue
		var data: Dictionary = RunManagerScript.doctrine(doctrine_id)
		_add_to_delta(total_bonus, data.get("mastery_bonus", {}), rank)
	for key in total_bonus:
		resources[key] = int(resources.get(key, 0)) + int(total_bonus[key])
	_clamp_power_reserve()
	_clamp_resource_storage()
	if not total_bonus.is_empty():
		_log("Doctrine mastery supplied %s." % _format_cost(total_bonus), false)

func _build_menu_overlay() -> void:
	menu_layer = CanvasLayer.new()
	menu_layer.name = "MenuLayer"
	menu_layer.layer = 20
	menu_layer.visible = false
	add_child(menu_layer)
	var shade := ColorRect.new()
	shade.name = "Dimmer"
	shade.color = Color(0.0, 0.03, 0.05, 0.72)
	shade.set_anchors_preset(Control.PRESET_FULL_RECT)
	shade.mouse_filter = Control.MOUSE_FILTER_STOP
	menu_layer.add_child(shade)
	var center := CenterContainer.new()
	center.name = "MenuCenter"
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_STOP
	menu_layer.add_child(center)
	var panel := PanelContainer.new()
	panel.name = "PauseMenu"
	panel.custom_minimum_size = Vector2(560, 650)
	panel.mouse_filter = Control.MOUSE_FILTER_STOP
	center.add_child(panel)
	_apply_panel_style(panel, Color("#071018"), Color("#1f5260"))
	menu_panel = panel
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 10)
	panel.add_child(box)
	var title := Label.new()
	title.text = "BRINE"
	title.add_theme_font_size_override("font_size", 34)
	title.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	box.add_child(title)
	var subtitle := Label.new()
	subtitle.text = "REBOOT CYCLE CONTROL"
	subtitle.add_theme_font_size_override("font_size", 12)
	subtitle.add_theme_color_override("font_color", Color("#536874"))
	box.add_child(subtitle)
	var status := Label.new()
	status.text = ""
	status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	status.add_theme_font_size_override("font_size", 13)
	status.add_theme_color_override("font_color", Color("#8fa3ae"))
	box.add_child(status)
	menu_status_label = status
	var separator := Label.new()
	separator.text = "────────────────────────────"
	separator.add_theme_color_override("font_color", Color("#18313c"))
	box.add_child(separator)
	_add_menu_display_options(box)
	_add_menu_button(box, "Resume Cycle", _close_menu)
	_add_menu_button(box, "Recenter Station", _menu_recenter_station)
	_add_menu_button(box, "Toggle Admin View", _menu_toggle_admin_view)
	end_expedition_button = Button.new()
	end_expedition_button.text = "Conclude Expedition · Bank Research"
	end_expedition_button.custom_minimum_size.y = 44
	end_expedition_button.pressed.connect(_end_expedition)
	_style_hud_button(end_expedition_button, false)
	box.add_child(end_expedition_button)
	_add_menu_button(box, "Restart Reboot Cycle", _menu_restart_cycle)
	_add_menu_button(box, "Quit To Desktop", _menu_quit_game)
	var hint := Label.new()
	hint.text = "ESC toggles this menu. Space pauses time."
	hint.add_theme_font_size_override("font_size", 11)
	hint.add_theme_color_override("font_color", Color("#536874"))
	box.add_child(hint)

func _add_menu_display_options(parent: Control) -> void:
	var section_title := Label.new()
	section_title.text = "DISPLAY"
	section_title.add_theme_font_size_override("font_size", 13)
	section_title.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	parent.add_child(section_title)

	var resolution_label := Label.new()
	resolution_label.text = "RESOLUTION"
	resolution_label.add_theme_color_override("font_color", Color("#8fa3ae"))
	parent.add_child(resolution_label)
	var preset_grid := GridContainer.new()
	preset_grid.columns = 2
	preset_grid.add_theme_constant_override("h_separation", 8)
	preset_grid.add_theme_constant_override("v_separation", 8)
	parent.add_child(preset_grid)
	resolution_buttons.clear()
	for i in range(RESOLUTION_OPTIONS.size()):
		var resolution: Vector2i = RESOLUTION_OPTIONS[i]
		var button := Button.new()
		button.text = "%d x %d" % [resolution.x, resolution.y]
		button.toggle_mode = true
		button.custom_minimum_size = Vector2(250, 38)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.focus_mode = Control.FOCUS_NONE
		button.pressed.connect(_on_resolution_button_pressed.bind(i))
		_style_hud_button(button, i == _closest_resolution_option())
		preset_grid.add_child(button)
		resolution_buttons.append(button)

	var fullscreen := Button.new()
	fullscreen.name = "BorderlessFullscreen"
	fullscreen.text = "BORDERLESS FULLSCREEN: OFF"
	fullscreen.toggle_mode = true
	fullscreen.custom_minimum_size = Vector2(0, 44)
	fullscreen.focus_mode = Control.FOCUS_NONE
	fullscreen.pressed.connect(_on_borderless_fullscreen_button_pressed)
	_style_hud_button(fullscreen, false)
	parent.add_child(fullscreen)

	var separator := Label.new()
	separator.text = "────────────────────────────"
	separator.add_theme_color_override("font_color", Color("#18313c"))
	parent.add_child(separator)
	borderless_fullscreen_button = fullscreen

func _add_menu_button(parent: Control, text: String, callable: Callable) -> void:
	var button := Button.new()
	button.text = text
	button.custom_minimum_size = Vector2(0, 54)
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.focus_mode = Control.FOCUS_NONE
	button.mouse_filter = Control.MOUSE_FILTER_STOP
	button.pressed.connect(callable)
	if text == "Restart Reboot Cycle" or text == "Quit To Desktop":
		_style_danger_button(button)
	else:
		_style_hud_button(button, text == "Resume Cycle")
	parent.add_child(button)

func _style_danger_button(button: BaseButton) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.06, 0.025, 0.03, 0.68)
	style.border_color = Color("#5f3138")
	style.border_width_left = 1
	style.border_width_top = 1
	style.border_width_right = 1
	style.border_width_bottom = 1
	style.corner_radius_top_left = 0
	style.corner_radius_top_right = 0
	style.corner_radius_bottom_left = 0
	style.corner_radius_bottom_right = 0
	style.content_margin_left = 12
	style.content_margin_right = 12
	style.content_margin_top = 6
	style.content_margin_bottom = 6
	button.add_theme_stylebox_override("normal", style)
	var hover_style := style.duplicate()
	hover_style.bg_color = Color(0.10, 0.04, 0.05, 0.82)
	hover_style.border_color = Color("#a84b56")
	button.add_theme_stylebox_override("hover", hover_style)
	button.add_theme_stylebox_override("pressed", hover_style)
	button.add_theme_color_override("font_color", Color("#ff8b94"))
	button.add_theme_color_override("font_hover_color", Color("#ffc0c6"))
	button.add_theme_font_size_override("font_size", 13)

func _hide_grid_scrollbars() -> void:
	if grid_scroll == null:
		return
	var h_bar := grid_scroll.get_h_scroll_bar()
	var v_bar := grid_scroll.get_v_scroll_bar()
	if h_bar != null:
		h_bar.visible = false
		h_bar.modulate = Color(1, 1, 1, 0)
	if v_bar != null:
		v_bar.visible = false
		v_bar.modulate = Color(1, 1, 1, 0)

func _start_reboot_cycle() -> void:
	if journal_layer != null:
		journal_layer.visible = false
	resources = {
		"metal": 18,
		"power": 6,
		"oxygen": 8,
		"water": 0,
		"food": 8,
		"data": 0,
		"biomass": 2,
		"rare_minerals": 1,
		"integrity": 100
	}
	run_earned = {}
	log_lines.clear()
	occupied.clear()
	placed_rooms.clear()
	hand.clear()
	draw_pile.clear()
	discard_pile.clear()
	rerolls_remaining = 3
	reroll_recovery_progress = 0
	selected_doctrines.clear()
	pending_doctrines.clear()
	run_directives.clear()
	directive_index = 0
	completed_directives.clear()
	run_victory = false
	expedition_mode = false
	run_rewards_recorded = false
	run_awarded_research = 0
	selected_card_id = ""
	hovered_card_id = ""
	selected_rotation = 0
	selected_room_cell = Vector2i(-1, -1)
	hover_cell = Vector2i(-1, -1)
	cycle = 0
	crew_count = 0
	had_crew = false
	corruption = 0
	orbit_decay = 0
	active_synergies.clear()
	connected_synergy_links.clear()
	active_synergy_links.clear()
	synergy_stabilization_progress.clear()
	run_discovered_synergy_ids.clear()
	run_stabilized_synergy_ids.clear()
	run_decrypted_blueprint_ids.clear()
	prototype_card_seen_cycle.clear()
	discovery_bursts.clear()
	resonance_score = 0
	resonance_tier_index = 0
	links_formed = 0
	largest_cascade = 0
	last_cascade_size = 0
	completed_pois.clear()
	expired_pois.clear()
	power_generated = 0
	power_used = 0
	power_capacity = _get_power_capacity()
	unpowered_rooms.clear()
	powered_room_cells.clear()
	unpowered_room_cells.clear()
	offline_reasons.clear()
	last_cycle_delta.clear()
	var center_index := int(float(GRID_SIZE) * 0.5)
	test_walker_cell = Vector2i(center_index, center_index)
	test_walker_next_cell = Vector2i(-1, -1)
	test_walker_previous_cell = Vector2i(-1, -1)
	test_walker_progress = 0.0
	test_walker_state = "idle"
	test_walker_break_timer = 1.5
	test_walker_direction = "south"
	visual_time_seconds = 0.0
	orbit = OrbitManagerScript.new()
	running = false
	_set_paused(true, false)
	summary_layer.visible = false
	if summary_title_label != null:
		summary_title_label.text = "Reboot Summary"
	if cascade_toast_tween != null and cascade_toast_tween.is_valid():
		cascade_toast_tween.kill()
	toast_messages.clear()
	toast_playing = false
	cascade_toast.visible = false
	_place_room("brine_core", Vector2i(center_index, center_index), true)
	_clamp_resource_storage()
	_center_grid_on_station()
	_show_doctrine_selection()
	_log("Reboot Cycle staged. Select two doctrines to compile the blueprint deck.", false)
	_refresh_all()

func _draw_hand() -> void:
	hand.clear()
	_refill_hand()
	selected_card_id = hand[0] if not hand.is_empty() else ""

func _build_run_deck() -> void:
	draw_pile = RunManagerScript.build_deck(selected_doctrines, meta.unlocked_room_ids)
	discard_pile.clear()
	draw_pile.shuffle()
	if draw_pile.has("mining_drone_bay"):
		draw_pile.erase("mining_drone_bay")
		draw_pile.append("mining_drone_bay")
	if draw_pile.has("solar_array"):
		draw_pile.erase("solar_array")
		draw_pile.append("solar_array")

func _refill_hand() -> void:
	while hand.size() < HAND_SIZE:
		if draw_pile.is_empty():
			_reshuffle_discard_pile()
		if draw_pile.is_empty():
			break
		var attempts := draw_pile.size()
		var drawn := false
		while attempts > 0:
			attempts -= 1
			var id := str(draw_pile.pop_back())
			if not hand.has(id) or attempts == 0:
				hand.append(id)
				if prototype_card_seen_cycle.has(id) and int(prototype_card_seen_cycle[id]) < 0:
					prototype_card_seen_cycle[id] = cycle
				drawn = true
				break
			draw_pile.push_front(id)
		if not drawn:
			break

func _reshuffle_discard_pile() -> void:
	if discard_pile.is_empty():
		return
	draw_pile.assign(discard_pile)
	discard_pile.clear()
	draw_pile.shuffle()
	_log("Blueprint discard pile recycled into the draw stack.", false)

func _clear_prototype_marker(id: String) -> void:
	prototype_card_seen_cycle.erase(id)

func _expire_prototype_markers() -> void:
	for room_id_value in prototype_card_seen_cycle.keys():
		var room_id := str(room_id_value)
		var first_seen_cycle := int(prototype_card_seen_cycle[room_id])
		if first_seen_cycle >= 0 and cycle > first_seen_cycle + 1:
			prototype_card_seen_cycle.erase(room_id)

func _on_grid_clicked(cell: Vector2i) -> void:
	if _gameplay_input_blocked():
		return
	if not running:
		return
	if occupied.has(cell):
		selected_card_id = ""
		selected_room_cell = cell
		last_preview_room_id = str(occupied[cell].get("id", ""))
		last_previewing_card = false
		_refresh_all()
		return
	if selected_card_id.is_empty():
		return
	var problem := get_placement_problem(selected_card_id, cell)
	if not problem.is_empty():
		_log("Placement rejected: %s" % problem, false)
		return
	if not testing_free_build:
		_spend(RoomDatabaseScript.get_room(selected_card_id)["cost"])
	var built_card_id := selected_card_id
	_place_room(built_card_id, cell)
	_clamp_power_reserve()
	hand.erase(built_card_id)
	discard_pile.append(built_card_id)
	_refill_hand()
	selected_card_id = hand[0] if not hand.is_empty() else ""
	selected_rotation = 0
	_refresh_all()

func _on_grid_secondary_clicked(_cell: Vector2i) -> void:
	if _gameplay_input_blocked():
		return
	selected_card_id = ""
	selected_rotation = 0
	_refresh_all()

func _on_grid_hovered(cell: Vector2i) -> void:
	if _gameplay_input_blocked():
		return
	if hover_cell == cell:
		return
	hover_cell = cell
	if occupied.has(cell):
		last_preview_room_id = str(occupied[cell].get("id", ""))
		last_previewing_card = false
	_refresh_placement_status()
	_refresh_inspector()
	grid_view.queue_redraw()

func _can_place(id: String, cell: Vector2i) -> bool:
	return get_placement_problem(id, cell).is_empty()

func get_placement_problem(id: String, cell: Vector2i) -> String:
	if cell.x < 0 or cell.y < 0 or cell.x >= GRID_SIZE or cell.y >= GRID_SIZE:
		return "outside station grid."
	if occupied.has(cell):
		return "cell already contains %s." % occupied[cell]["display_name"]
	var room := RoomDatabaseScript.get_room(id)
	if room.is_empty():
		return "unknown blueprint."
	if not testing_free_build and not _can_afford(room.get("cost", {})):
		return "cannot afford %s." % _format_cost(room.get("cost", {}))
	if placed_rooms.is_empty():
		return ""
	var mismatch := ""
	for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
		var neighbor_pos: Vector2i = cell + offset
		if occupied.has(neighbor_pos):
			if _doors_connect(id, selected_rotation, offset, occupied[neighbor_pos]):
				return ""
			mismatch = "door does not match adjacent %s. Rotate with R." % occupied[neighbor_pos]["display_name"]
	if not mismatch.is_empty():
		return mismatch
	return "must connect to an adjacent door."

func _place_room(id: String, cell: Vector2i, free := false) -> void:
	var previous_link_keys := _active_synergy_link_keys()
	var room := RoomDatabaseScript.get_room(id).duplicate(true)
	room["pos"] = cell
	room["rotation"] = selected_rotation if not free else 0
	if ROOM_ART_VARIANT_COUNTS.has(id):
		room["art_variant"] = rng.randi_range(0, int(ROOM_ART_VARIANT_COUNTS[id]) - 1)
	placed_rooms.append(room)
	occupied[cell] = room
	if not free:
		_log("Built %s at %s." % [room["display_name"], cell])
		if id == "crew_hab" and resources["oxygen"] > 0 and resources["food"] > 0:
			crew_count += 1
			had_crew = true
			_log("A survivor claims the new Crew Hab.")
	if test_walker_cell == Vector2i(-1, -1):
		test_walker_cell = cell
	_check_synergies()
	if not free:
		_resolve_placement_cascade(cell, previous_link_keys)
	_apply_unlocks()
	if not free:
		_check_directive_progress()
	if free:
		_center_grid_on_station_deferred()

func _advance_cycle() -> void:
	if not running:
		return
	cycle += 1
	last_cycle_delta = _apply_room_economy()
	_advance_draft_recovery()
	_advance_synergy_discovery_cycle()
	_apply_orbit_event()
	_apply_life_support()
	_emit_warnings()
	_apply_unlocks()
	_check_directive_progress()
	_expire_prototype_markers()
	_refresh_all()
	if running:
		_check_fail_conditions()

func _advance_draft_recovery() -> void:
	if rerolls_remaining >= REROLL_RECOVERY_CAP:
		reroll_recovery_progress = 0
		return
	reroll_recovery_progress += 1
	if reroll_recovery_progress >= REROLL_RECOVERY_CYCLES:
		reroll_recovery_progress = 0
		rerolls_remaining += 1
		_log("Draft buffer reconstructed. One reroll restored.")

func _simulate_room_economy(known_bonuses_only := false, simulated_cycle := -1) -> Dictionary:
	# Spend shared start-of-cycle inputs once. Outputs become next cycle's inputs.
	var delta := {}
	var working_cells := {}
	var offline := {}
	var power_failures := []
	var input_budget := resources.duplicate()
	var generation := 0
	for room in placed_rooms:
		if not room.get("suspended", false):
			generation += int(room.get("production", {}).get("power", 0))
	input_budget["power"] = generation + maxi(int(resources["power"]), 0)
	var reserve_start := int(resources["power"])
	var added_crew := 0
	for room in _rooms_by_power_priority():
		var cell: Vector2i = room["pos"]
		if room.get("suspended", false):
			offline[cell] = "SUSPENDED"
			continue
		var missing: Array[String] = []
		var consumption: Dictionary = room.get("consumption", {})
		for key in consumption:
			if int(input_budget.get(key, 0)) < int(consumption[key]):
				missing.append(str(key).replace("_", " ").to_upper())
		if not missing.is_empty():
			offline[cell] = "NEEDS %s" % _join_strings(missing, " + ")
			if missing.has("POWER"):
				power_failures.append(room["display_name"])
			continue
		if room["id"] == "clone_lab" and crew_count + added_crew >= _get_crew_capacity():
			offline[cell] = "HABITATS FULL"
			continue
		for key in consumption:
			input_budget[key] = int(input_budget.get(key, 0)) - int(consumption[key])
		working_cells[cell] = true
		_add_to_delta(delta, _without_key(room.get("production", {}), "power"), 1)
		_add_to_delta(delta, _without_key(consumption, "power"), -1)
		if room["id"] == "research_lab" and crew_count > 0:
			_add_to_delta(delta, {"data": 1}, 1)
		if room["id"] == "clone_lab":
			added_crew += 1
	var links := DiscoveryManagerScript.functioning_links(connected_synergy_links, working_cells)
	var bonus_links := []
	for link in links:
		if not known_bonuses_only or meta.discovered_synergy_ids.has(link["id"]):
			bonus_links.append(link)
	_add_to_delta(delta, SynergyManagerScript.cycle_bonus(bonus_links), 1)
	var tick := cycle if simulated_cycle < 0 else simulated_cycle
	for link in bonus_links:
		if link["id"] == "safe_wake_protocol" and tick % 3 == 0 and crew_count + added_crew < _get_crew_capacity():
			added_crew += 1
			break
	var used := generation + maxi(reserve_start, 0) - int(input_budget["power"])
	var final_power := clampi(int(input_budget["power"]) + int(delta.get("power", 0)), 0, _get_power_capacity())
	delta["power"] = final_power - reserve_start
	return {"delta": delta, "working_cells": working_cells, "offline": offline,
		"power_failures": power_failures, "links": links, "generation": generation,
		"power_used": used, "added_crew": added_crew}

func _apply_room_economy() -> Dictionary:
	var result := _simulate_room_economy()
	powered_room_cells = result["working_cells"]
	offline_reasons = result["offline"]
	unpowered_room_cells = offline_reasons.duplicate()
	unpowered_rooms = result["power_failures"]
	power_generated = result["generation"]
	power_used = result["power_used"]
	power_capacity = _get_power_capacity()
	active_synergy_links = result["links"]
	active_synergies.clear()
	for link in active_synergy_links:
		active_synergies[str(link.get("id", ""))] = link
	if not unpowered_rooms.is_empty():
		_log("Power shortage: %s offline this cycle." % _join_strings(unpowered_rooms))
	if int(result["added_crew"]) > 0:
		crew_count += int(result["added_crew"])
		had_crew = true
		_log("Recovery systems welcome %d survivor(s)." % int(result["added_crew"]))
	if active_synergies.has("containment_sector") and corruption > 0:
		corruption -= 1
		_log("Containment Sector filters one level of corruption.")
	var delta: Dictionary = result["delta"]
	_apply_delta(delta)
	_clamp_power_reserve()
	return delta

func _get_crew_capacity() -> int:
	var capacity := 2 # Emergency berths aboard the core.
	for room in placed_rooms:
		if room["id"] == "crew_hab":
			capacity += 2
	return capacity

func _apply_orbit_event() -> void:
	var event := orbit.advance(cycle, _get_poi_work_capacities())
	if not event.get("triggered", false):
		return
	if event.get("completed", false):
		completed_pois.append(event["name"])
	else:
		expired_pois.append(event["name"])
	_log(event.get("message", "An orbital event passes over BRINE."))
	_apply_delta(event.get("effect", {}))
	if event.has("damage"):
		resources["integrity"] -= event["damage"]
	if event.has("corruption"):
		corruption += event["corruption"]
	if event["name"] == "Frozen Escape Pod" and event.get("completed", false):
		if crew_count < _get_crew_capacity():
			crew_count += 1
			had_crew = true
			_log("Life Support thaws a survivor from the escape pod.")
		else:
			_apply_delta({"data": 3})
			_log("Habitats full. Pod telemetry recovered; its occupant remains in safe stasis.")
	_clamp_power_reserve()

func _apply_life_support() -> void:
	if crew_count <= 0:
		return
	resources["food"] -= crew_count
	resources["oxygen"] -= crew_count
	last_cycle_delta["food"] = last_cycle_delta.get("food", 0) - crew_count
	last_cycle_delta["oxygen"] = last_cycle_delta.get("oxygen", 0) - crew_count
	if resources["food"] < 0 or resources["oxygen"] < 0:
		var deaths := 1
		crew_count = max(crew_count - deaths, 0)
		resources["integrity"] -= 5
		_log("Crew life support collapse. One crew lost, station integrity damaged.")

func _emit_warnings() -> void:
	var net := _project_cycle_delta()
	if power_generated + int(resources["power"]) < _project_power_demand():
		_log("Warning: projected Power shortfall next cycle. Lower-priority rooms may go offline.")
	elif resources["power"] <= max(2, int(_get_power_capacity() * 0.2)):
		_log("Warning: Power reserve low.")
	if crew_count > 0:
		if resources["oxygen"] + net.get("oxygen", 0) <= 0:
			_log("Warning: Oxygen will collapse soon without Life Support or Hydroponics.")
		if resources["food"] + net.get("food", 0) <= 0:
			_log("Warning: Food will collapse soon without Hydroponics.")
	if resources["integrity"] <= 20:
		_log("Warning: Station Integrity critical.")
	if corruption >= 7:
		_log("Warning: Corruption approaching maximum.")

func _check_synergies() -> void:
	var result := SynergyManagerScript.evaluate(placed_rooms, occupied)
	connected_synergy_links = result.get("links", [])

func _advance_synergy_discovery_cycle() -> void:
	var transition := DiscoveryManagerScript.advance_cycle(
		active_synergy_links,
		synergy_stabilization_progress,
		meta.discovered_synergy_ids,
		meta.stabilized_synergy_ids
	)
	synergy_stabilization_progress = transition["progress"]
	for id_value in transition["new_discovery_ids"]:
		_handle_synergy_discovery(str(id_value))
	for id_value in transition["new_stabilization_ids"]:
		_handle_synergy_stabilization(str(id_value))

func _handle_synergy_discovery(synergy_id: String) -> void:
	if not meta.discover_synergy(synergy_id):
		return
	if not run_discovered_synergy_ids.has(synergy_id):
		run_discovered_synergy_ids.append(synergy_id)
	var synergy := _synergy_by_id(synergy_id)
	for link_value in active_synergy_links:
		var link: Dictionary = link_value
		if str(link.get("id", "")) != synergy_id:
			continue
		var cells: Array = link.get("cells", [])
		if cells.size() >= 2:
			var color_text := str(synergy.get("fx_color", "55E6FF")).trim_prefix("#")
			discovery_bursts.append({
				"cells": cells.duplicate(),
				"color": Color("#%s" % color_text),
				"remaining": DISCOVERY_BURST_SECONDS
			})
		break
	_log(str(synergy.get("message", "BRINE recovered a functioning room pattern.")))
	_queue_center_toast("PATTERN DISCOVERED\n%s" % str(synergy.get("name", synergy_id)).to_upper())

func _update_discovery_bursts(delta: float) -> void:
	if discovery_bursts.is_empty():
		return
	for index in range(discovery_bursts.size() - 1, -1, -1):
		var burst: Dictionary = discovery_bursts[index]
		burst["remaining"] = float(burst.get("remaining", 0.0)) - delta
		if float(burst["remaining"]) <= 0.0:
			discovery_bursts.remove_at(index)
	if grid_view != null:
		grid_view.queue_redraw()

func _handle_synergy_stabilization(synergy_id: String) -> void:
	_award_synergy_stabilization(SynergyManagerScript.get_synergy(synergy_id))

func _award_synergy_stabilization(synergy: Dictionary) -> void:
	var synergy_id := str(synergy.get("id", ""))
	if synergy_id.is_empty() or not meta.stabilize_synergy(synergy_id):
		return
	if not run_stabilized_synergy_ids.has(synergy_id):
		run_stabilized_synergy_ids.append(synergy_id)
	var synergy_name := str(synergy.get("name", synergy_id))
	var unlock_id := str(synergy.get("unlock_room_id", ""))
	if not unlock_id.is_empty():
		if meta.unlock_room(unlock_id):
			draw_pile.append(unlock_id)
			prototype_card_seen_cycle[unlock_id] = -1
			run_decrypted_blueprint_ids.append(unlock_id)
			var room_name := str(RoomDatabaseScript.get_room(unlock_id).get("display_name", unlock_id))
			_log("Pattern stabilized: %s. Blueprint decrypted: %s." % [synergy_name, room_name])
			_queue_center_toast("BLUEPRINT DECRYPTED\n%s" % room_name.to_upper())
		else:
			_log("Pattern stabilized: %s. Blueprint already present in the archive." % synergy_name)
			_queue_center_toast("PATTERN STABILIZED\n%s" % synergy_name.to_upper())
		return
	var terminal_reward: Dictionary = synergy.get("terminal_reward", {})
	var research := int(terminal_reward.get("research", 0))
	if research > 0:
		meta.add_research_points(research)
		_log("Pattern stabilized: %s. +%d Research." % [synergy_name, research])
		_queue_center_toast("PATTERN STABILIZED\n+%d RESEARCH" % research)

func _synergy_by_id(synergy_id: String) -> Dictionary:
	return SynergyManagerScript.get_synergy(synergy_id)

func _synergy_display_name(synergy_id: String) -> String:
	if not meta.discovered_synergy_ids.has(synergy_id):
		return "UNRESOLVED PATTERN"
	var synergy := SynergyManagerScript.get_synergy(synergy_id)
	return str(synergy.get("name", synergy_id.replace("_", " ").capitalize()))

func _resolve_placement_cascade(cell: Vector2i, previous_link_keys: Dictionary) -> void:
	var new_links: Array = []
	for link in connected_synergy_links:
		if previous_link_keys.has(str(link.get("key", ""))):
			continue
		if link.get("cells", []).has(cell):
			new_links.append(link)
	if new_links.is_empty():
		last_cascade_size = 0
		return

	var pulse := {}
	var names: Array[String] = []
	for link in new_links:
		_add_to_delta(pulse, link.get("bonus", {}), 1)
		names.append(_synergy_display_name(str(link.get("id", ""))))
	if new_links.size() > 1:
		_add_to_delta(pulse, {"data": new_links.size() - 1}, 1)
	if not pulse.is_empty():
		_apply_delta(pulse)
		_clamp_power_reserve()
		_clamp_resource_storage()

	var resonance_gain := 0
	for combo_index in range(new_links.size()):
		resonance_gain += 10 * (combo_index + 1)
	resonance_score += resonance_gain
	links_formed += new_links.size()
	last_cascade_size = new_links.size()
	largest_cascade = maxi(largest_cascade, last_cascade_size)
	_log("CASCADE x%d: %s. +%d Resonance%s" % [
		new_links.size(),
		_join_strings(names, " + "),
		resonance_gain,
		" | Pulse: %s" % _format_cost(pulse) if not pulse.is_empty() else ""
	])
	_check_resonance_tiers()
	_show_cascade_toast(new_links.size(), resonance_gain, pulse)

func _active_synergy_link_keys() -> Dictionary:
	var keys := {}
	for link in connected_synergy_links:
		keys[str(link.get("key", ""))] = true
	return keys

func _check_resonance_tiers() -> void:
	while resonance_tier_index + 1 < RESONANCE_TIERS.size():
		var next_tier: Dictionary = RESONANCE_TIERS[resonance_tier_index + 1]
		if resonance_score < int(next_tier["threshold"]):
			break
		resonance_tier_index += 1
		var reward: Dictionary = next_tier.get("reward", {})
		if not reward.is_empty():
			_apply_delta(reward)
			_clamp_power_reserve()
			_clamp_resource_storage()
		_log("RESONANCE TIER %s reached. BRINE recovered %s." % [next_tier["name"], _format_cost(reward)])

func _show_cascade_toast(cascade_size: int, resonance_gain: int, pulse: Dictionary) -> void:
	var pulse_text := ""
	if not pulse.is_empty():
		pulse_text = "  ·  PULSE %s" % _format_cost(pulse).to_upper()
	_queue_center_toast("SIGNAL CASCADE x%d\n+%d RESONANCE%s" % [cascade_size, resonance_gain, pulse_text])

func _queue_center_toast(message: String) -> void:
	toast_messages.append(message)
	if not toast_playing:
		_play_next_center_toast()

func _play_next_center_toast() -> void:
	if toast_messages.is_empty():
		toast_playing = false
		return
	if cascade_toast == null or cascade_toast_label == null:
		toast_messages.clear()
		toast_playing = false
		return
	toast_playing = true
	_show_center_toast(toast_messages.pop_front())

func _show_center_toast(message: String) -> void:
	if cascade_toast == null or cascade_toast_label == null:
		return
	if cascade_toast_tween != null and cascade_toast_tween.is_valid():
		cascade_toast_tween.kill()
	cascade_toast_label.text = message
	cascade_toast.visible = true
	cascade_toast.modulate = Color(1, 1, 1, 0)
	cascade_toast.scale = Vector2(0.96, 0.96)
	cascade_toast.pivot_offset = cascade_toast.size * 0.5
	cascade_toast_tween = create_tween()
	cascade_toast_tween.set_parallel(true)
	cascade_toast_tween.tween_property(cascade_toast, "modulate:a", 1.0, 0.12)
	cascade_toast_tween.tween_property(cascade_toast, "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	cascade_toast_tween.chain().tween_interval(1.15)
	cascade_toast_tween.chain().tween_property(cascade_toast, "modulate:a", 0.0, 0.35)
	cascade_toast_tween.chain().tween_callback(_finish_center_toast)

func _finish_center_toast() -> void:
	if cascade_toast != null:
		cascade_toast.visible = false
	toast_playing = false
	_play_next_center_toast()

func _roll_run_directives() -> void:
	run_directives = RunManagerScript.roll_directives(rng, selected_doctrines)
	directive_index = 0
	completed_directives.clear()

func _current_directive() -> Dictionary:
	if expedition_mode:
		return {}
	if directive_index < 0 or directive_index >= run_directives.size():
		return {}
	return run_directives[directive_index]

func _directive_state() -> Dictionary:
	return {
		"rooms": maxi(0, placed_rooms.size() - 1),
		"resonance": resonance_score,
		"links": active_synergy_links.size(),
		"synergy_types": active_synergies.size(),
		"pois": completed_pois.size(),
		"doctrine_counts": RunManagerScript.count_doctrine_rooms(placed_rooms, selected_doctrines)
	}

func _check_directive_progress() -> void:
	if not running:
		return
	var directive := _current_directive()
	if directive.is_empty():
		return
	var progress := RunManagerScript.directive_progress(directive, _directive_state())
	if progress >= int(directive.get("target", 0)):
		_complete_current_directive()
		return
	if cycle > int(directive.get("deadline", 0)):
		_show_reboot_summary("Directive deadline missed: %s." % directive.get("name", "UNKNOWN DIRECTIVE"), false)

func _complete_current_directive() -> void:
	var directive := _current_directive()
	if directive.is_empty():
		return
	completed_directives.append(str(directive.get("name", "UNKNOWN DIRECTIVE")))
	var reward: Dictionary = directive.get("reward", {})
	var resource_reward: Dictionary = reward.get("resources", {})
	if not resource_reward.is_empty():
		_apply_delta(resource_reward)
		_clamp_power_reserve()
		_clamp_resource_storage()
	rerolls_remaining += int(reward.get("rerolls", 0))
	if rerolls_remaining >= REROLL_RECOVERY_CAP:
		reroll_recovery_progress = 0
	_log("DIRECTIVE COMPLETE: %s. Reward: %s." % [directive["name"], _format_directive_reward(reward)])
	if directive_index + 1 >= run_directives.size():
		run_victory = true
		_show_reboot_summary("All reconstruction directives complete. BRINE has stabilized this orbital sector.", true)
		return
	var completed_number := directive_index + 1
	directive_index += 1
	_queue_center_toast("DIRECTIVE %d/%d COMPLETE\n%s" % [completed_number, run_directives.size(), _format_directive_reward(reward).to_upper()])
	_log("Directive %d/%d received: %s." % [directive_index + 1, run_directives.size(), _current_directive().get("name", "UNKNOWN")])

func _format_directive_reward(reward: Dictionary) -> String:
	var parts: Array[String] = []
	var resource_reward: Dictionary = reward.get("resources", {})
	if not resource_reward.is_empty():
		parts.append(_format_cost(resource_reward))
	var rerolls := int(reward.get("rerolls", 0))
	if rerolls > 0:
		parts.append("%d reroll%s" % [rerolls, "s" if rerolls != 1 else ""])
	return _join_strings(parts) if not parts.is_empty() else "sector stability"

func _apply_unlocks() -> void:
	pass

func _check_fail_conditions() -> void:
	if testing_disable_failures:
		return
	var reason := ""
	if resources["integrity"] <= 0:
		reason = "Station Integrity reached 0."
	elif unpowered_rooms.has("BRINE Core"):
		reason = "BRINE Core lost power."
	elif resources["oxygen"] <= -10:
		reason = "Oxygen collapse overwhelmed the station."
	elif had_crew and crew_count <= 0:
		reason = "Crew population reached 0."
	elif corruption >= 10:
		reason = "Corruption reached maximum."
	elif orbit_decay >= 10:
		reason = "Orbit decay reached maximum."
	if not reason.is_empty():
		_show_reboot_summary(reason)

func _show_reboot_summary(reason: String, victory := false) -> void:
	running = false
	run_victory = run_victory or victory
	var earned := int(float(max(resources["data"], 0)) / 5.0) + int(float(resonance_score) / 50.0)
	var award := maxi(0, earned - run_awarded_research)
	run_awarded_research += award
	meta.add_research_points(award)
	var previous_doctrine_ranks := {}
	for doctrine_id_value in selected_doctrines:
		var doctrine_id := str(doctrine_id_value)
		previous_doctrine_ranks[doctrine_id] = meta.get_doctrine_rank(doctrine_id)
	var mastery_gain := 0
	if not run_rewards_recorded:
		mastery_gain = meta.record_run(selected_doctrines, victory, resonance_score)
		run_rewards_recorded = true
	var synergy_names := []
	for id in meta.discovered_synergy_ids:
		synergy_names.append(id.replace("_", " ").capitalize())
	if summary_title_label != null:
		summary_title_label.text = "Station Stabilized" if victory else ("Expedition Complete" if expedition_mode else "Reboot Summary")
	if continue_expedition_button != null:
		continue_expedition_button.visible = victory and not expedition_mode
	var discoveries := "Patterns discovered: %s\nPatterns stabilized: %s\nBlueprints decrypted: %s" % [
		_join_strings(_synergy_names_for_ids(run_discovered_synergy_ids)) if not run_discovered_synergy_ids.is_empty() else "None",
		_join_strings(_synergy_names_for_ids(run_stabilized_synergy_ids)) if not run_stabilized_synergy_ids.is_empty() else "None",
		_join_strings(_room_names_for_ids(run_decrypted_blueprint_ids)) if not run_decrypted_blueprint_ids.is_empty() else "None"
	]
	summary_text.text = "%s\n\n%s\n\nDoctrines: %s\nDirectives completed: %d/%d\nCycles survived: %d\nCrew remaining: %d\nResonance score: %d (%s)\nLinks formed: %d · Best cascade: x%d\nResearch awarded: %d\nDoctrine mastery: %s\nMastery gained: +%d each\nTotal research: %d\nStabilized reboots: %d\nDiscovered synergies: %s" % [
		reason,
		discoveries,
		RunManagerScript.doctrine_pair_name(selected_doctrines) if not selected_doctrines.is_empty() else "None selected",
		completed_directives.size(),
		run_directives.size(),
		cycle,
		crew_count,
		resonance_score,
		RESONANCE_TIERS[resonance_tier_index]["name"],
		links_formed,
		largest_cascade,
		award,
		_format_doctrine_mastery_summary(previous_doctrine_ranks),
		mastery_gain,
		meta.total_research_points,
		meta.total_victories,
		_join_strings(synergy_names) if synergy_names.size() > 0 else "None"
	]
	summary_text.text += "\nPOIs completed: %s\nResources earned: %s" % [
		_join_strings(completed_pois) if completed_pois.size() > 0 else "None",
		_format_cost(run_earned) if not run_earned.is_empty() else "None"
	]
	summary_text.text += "\nPOIs expired: %s" % [_join_strings(expired_pois) if expired_pois.size() > 0 else "None"]
	summary_layer.visible = true
	if journal_layer != null:
		journal_layer.visible = false
	_set_paused(true, false)
	_log("Run complete: %s" % reason)

func _continue_expedition() -> void:
	if not run_victory or expedition_mode or summary_layer == null or not summary_layer.visible:
		return
	expedition_mode = true
	summary_layer.visible = false
	running = true
	_set_paused(false)
	if tick_timer != null:
		tick_timer.start()
	_log("Expedition extended. No directive deadlines; life support and orbital hazards remain active.")
	_refresh_all()

func _end_expedition() -> void:
	if not expedition_mode or not running:
		return
	menu_open = false
	if menu_layer != null:
		menu_layer.visible = false
	_show_reboot_summary("Expedition archived. Your station's discoveries remain with BRINE.")

func _format_doctrine_mastery_summary(previous_ranks: Dictionary) -> String:
	if selected_doctrines.is_empty():
		return "None"
	var parts: Array[String] = []
	for doctrine_id_value in selected_doctrines:
		var doctrine_id := str(doctrine_id_value)
		var data := RunManagerScript.doctrine(doctrine_id)
		var short_name := str(data.get("short_name", doctrine_id.to_upper()))
		var mastery := meta.get_doctrine_mastery(doctrine_id)
		var rank := meta.get_doctrine_rank(doctrine_id)
		var next_threshold := meta.get_next_doctrine_rank_threshold(doctrine_id)
		var progress_text := "MAX" if next_threshold < 0 else "%d/%d" % [mastery, next_threshold]
		var rank_up_text := "  RANK UP" if rank > int(previous_ranks.get(doctrine_id, rank)) else ""
		parts.append("%s R%d %s%s" % [short_name, rank, progress_text, rank_up_text])
	return "  ·  ".join(parts)

func _synergy_names_for_ids(ids: Array) -> Array[String]:
	var names: Array[String] = []
	for id_value in ids:
		var synergy := SynergyManagerScript.get_synergy(str(id_value))
		names.append(str(synergy.get("name", str(id_value).replace("_", " ").capitalize())))
	return names

func _room_names_for_ids(ids: Array) -> Array[String]:
	var names: Array[String] = []
	for id_value in ids:
		var room_id := str(id_value)
		names.append(str(RoomDatabaseScript.get_room(room_id).get("display_name", room_id.replace("_", " ").capitalize())))
	return names

func _refresh_all() -> void:
	_refresh_resources()
	_refresh_cards()
	_refresh_inspector()
	_refresh_orbital_objective()
	_refresh_archive()
	_refresh_routing()
	_refresh_placement_status()
	_refresh_log()
	_refresh_view_mode_button()
	_refresh_menu_status()
	grid_view.queue_redraw()

func _refresh_orbital_objective() -> void:
	if orbital_objective_label == null:
		return
	if expedition_mode:
		orbital_objective_label.text = "OPEN EXPEDITION\nSector secured. Keep experimenting.\n%d learned · %d stabilized this run\n\n%s" % [run_discovered_synergy_ids.size(), run_stabilized_synergy_ids.size(), orbit.get_panel_text().replace("\n", " · ")]
		return
	var directive := _current_directive()
	if directive.is_empty():
		orbital_objective_label.text = "RECONSTRUCTION DIRECTIVE\nAWAITING DOCTRINE PAIR\n──────────────\nSelect two doctrines to compile this reboot.\n\nORBIT\n%s" % orbit.get_panel_text()
		return
	var directive_state := _directive_state()
	var deadline := int(directive.get("deadline", 0))
	var remaining := maxi(0, deadline - cycle)
	orbital_objective_label.text = "DIRECTIVE %d/%d  ·  LIMIT C%02d\n%s\nPROGRESS %s  ·  %d CYCLES LEFT\nREWARD %s\n\nORBIT  %s" % [
		directive_index + 1,
		run_directives.size(),
		deadline,
		directive.get("name", "UNKNOWN"),
		RunManagerScript.directive_progress_text(directive, directive_state),
		remaining,
		_format_directive_reward(directive.get("reward", {})).to_upper(),
		orbit.get_panel_text().replace("\n", "  ·  ")
	]
	orbital_objective_label.tooltip_text = str(directive.get("briefing", ""))

func _on_zoom_changed(value: float) -> void:
	_set_grid_zoom(DEFAULT_GRID_ZOOM * value, false)

func _set_grid_zoom(value: float, update_slider := true) -> void:
	var center_ratio := _grid_view_center_ratio()
	grid_zoom = clamp(value, MIN_GRID_ZOOM, DEFAULT_GRID_ZOOM)
	if update_slider and zoom_slider != null:
		zoom_slider.set_value_no_signal(grid_zoom / DEFAULT_GRID_ZOOM)
	_apply_grid_zoom()
	_restore_grid_view_center(center_ratio)
	_restore_grid_view_center_deferred(center_ratio)
	_refresh_placement_status()

func _grid_view_center_ratio() -> Vector2:
	if grid_scroll == null:
		return Vector2(0.5, 0.5)
	var full_size: float = max(GRID_SIZE * get_cell_size(), 1.0)
	var center: Vector2 = Vector2(grid_scroll.scroll_horizontal, grid_scroll.scroll_vertical) + grid_scroll.get_rect().size * 0.5
	return Vector2(clamp(center.x / full_size, 0.0, 1.0), clamp(center.y / full_size, 0.0, 1.0))

func _restore_grid_view_center(center_ratio: Vector2) -> void:
	if grid_scroll == null:
		return
	var full_size: float = GRID_SIZE * get_cell_size()
	var viewport_size: Vector2 = grid_scroll.get_rect().size
	grid_scroll.scroll_horizontal = int(max(center_ratio.x * full_size - viewport_size.x * 0.5, 0.0))
	grid_scroll.scroll_vertical = int(max(center_ratio.y * full_size - viewport_size.y * 0.5, 0.0))

func _restore_grid_view_center_deferred(center_ratio: Vector2) -> void:
	await get_tree().process_frame
	_restore_grid_view_center(center_ratio)

func _toggle_pause() -> void:
	if _gameplay_input_blocked():
		return
	_set_paused(not paused, true)

func _set_paused(value: bool, write_log := false) -> void:
	paused = value
	if tick_timer != null:
		tick_timer.paused = paused
	if pause_button != null:
		pause_button.set_pressed_no_signal(paused)
		pause_button.text = "▶ RESUME" if paused else "|| PAUSE"
		_style_hud_button(pause_button, paused)
	if controls_state_label != null:
		controls_state_label.text = "PAUSED" if paused else "RUNNING"
	_refresh_flow_controls()
	if write_log:
		_log("Time paused." if paused else "Time resumed.", false)
	if grid_view != null:
		grid_view.queue_redraw()

func _refresh_flow_controls() -> void:
	if pause_button != null:
		pause_button.set_pressed_no_signal(paused)
		pause_button.text = "▶ RESUME" if paused else "|| PAUSE"
		_style_hud_button(pause_button, paused)
	if controls_state_label != null:
		if paused:
			controls_state_label.text = "PAUSED"
		else:
			controls_state_label.text = "RUNNING"

func _toggle_menu() -> void:
	if menu_open:
		_close_menu()
	else:
		_open_menu()

func _open_menu() -> void:
	if menu_layer == null or _gameplay_input_blocked():
		return
	menu_open = true
	pause_before_menu = paused
	_set_paused(true, false)
	menu_layer.visible = true
	_refresh_menu_status()
	_refresh_all()
	if grid_view != null:
		grid_view.queue_redraw()

func _close_menu() -> void:
	if menu_layer == null:
		return
	menu_open = false
	_set_paused(pause_before_menu, false)
	menu_layer.visible = false
	_refresh_all()
	if grid_view != null:
		grid_view.queue_redraw()

func _refresh_menu_status() -> void:
	if end_expedition_button != null:
		end_expedition_button.visible = expedition_mode and running
	if menu_status_label == null:
		return
	var doctrine_name := RunManagerScript.doctrine_pair_name(selected_doctrines) if not selected_doctrines.is_empty() else "Not selected"
	var directive_status := "%d/%d" % [mini(directive_index + 1, run_directives.size()), run_directives.size()] if not run_directives.is_empty() else "Not started"
	menu_status_label.text = "Cycle %03d  |  Integrity %d%%  |  Crew %d  |  View %s\nDoctrines: %s  |  Directive: %s" % [
		cycle,
		resources.get("integrity", 0),
		crew_count,
		"ADMIN" if admin_mode else "NORMAL",
		doctrine_name,
		directive_status
	]
	_refresh_display_menu_state()

func _refresh_display_menu_state() -> void:
	var active_resolution := _closest_resolution_option()
	for i in range(resolution_buttons.size()):
		var button := resolution_buttons[i]
		if button == null:
			continue
		var active := i == active_resolution and not _is_borderless_fullscreen()
		button.set_pressed_no_signal(active)
		_style_hud_button(button, active)
	if borderless_fullscreen_button != null:
		var fullscreen := _is_borderless_fullscreen()
		borderless_fullscreen_button.set_pressed_no_signal(fullscreen)
		borderless_fullscreen_button.text = "BORDERLESS FULLSCREEN: ON" if fullscreen else "BORDERLESS FULLSCREEN: OFF"
		_style_hud_button(borderless_fullscreen_button, fullscreen)

func _closest_resolution_option() -> int:
	var current_size := DisplayServer.window_get_size()
	var best_index := 0
	var best_distance := INF
	for i in range(RESOLUTION_OPTIONS.size()):
		var resolution: Vector2i = RESOLUTION_OPTIONS[i]
		var distance := absf(float(resolution.x - current_size.x)) + absf(float(resolution.y - current_size.y))
		if distance < best_distance:
			best_distance = distance
			best_index = i
	return best_index

func _on_resolution_button_pressed(index: int) -> void:
	if index < 0 or index >= RESOLUTION_OPTIONS.size():
		return
	last_windowed_resolution = RESOLUTION_OPTIONS[index]
	_apply_window_resolution(RESOLUTION_OPTIONS[index])
	_refresh_menu_status()

func _apply_window_resolution(window_size_value: Vector2i) -> void:
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_BORDERLESS, false)
	await get_tree().process_frame
	DisplayServer.window_set_size(window_size_value)
	get_window().size = window_size_value
	var screen_size := DisplayServer.screen_get_size(DisplayServer.window_get_current_screen())
	var window_position := Vector2i(
		maxi(0, int((screen_size.x - window_size_value.x) * 0.5)),
		maxi(0, int((screen_size.y - window_size_value.y) * 0.5))
	)
	DisplayServer.window_set_position(window_position)
	get_window().position = window_position
	if menu_open:
		_refresh_menu_status()

func _on_borderless_fullscreen_button_pressed() -> void:
	var enabled := not _is_borderless_fullscreen()
	if enabled:
		var screen := DisplayServer.window_get_current_screen()
		var screen_position := DisplayServer.screen_get_position(screen)
		var screen_size := DisplayServer.screen_get_size(screen)
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_BORDERLESS, true)
		DisplayServer.window_set_position(screen_position)
		DisplayServer.window_set_size(screen_size)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_BORDERLESS, false)
		_apply_window_resolution(last_windowed_resolution)
	_refresh_menu_status()

func _is_borderless_fullscreen() -> bool:
	if DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN:
		return true
	if not DisplayServer.window_get_flag(DisplayServer.WINDOW_FLAG_BORDERLESS):
		return false
	var screen_size := DisplayServer.screen_get_size(DisplayServer.window_get_current_screen())
	var window_size := DisplayServer.window_get_size()
	return window_size.x >= screen_size.x and window_size.y >= screen_size.y

func _menu_recenter_station() -> void:
	_center_grid_on_station_deferred()
	_close_menu()

func _menu_toggle_admin_view() -> void:
	admin_mode = not admin_mode
	_log("Admin topology overlay %s." % ("enabled" if admin_mode else "hidden"), false)
	_refresh_menu_status()
	_refresh_all()

func _menu_restart_cycle() -> void:
	menu_open = false
	if menu_layer != null:
		menu_layer.visible = false
	_start_reboot_cycle()

func _menu_quit_game() -> void:
	get_tree().quit()

func _toggle_admin_view_button() -> void:
	admin_mode = not admin_mode
	_log("Admin topology overlay %s." % ("enabled" if admin_mode else "hidden"), false)
	_refresh_all()

func _refresh_view_mode_button() -> void:
	if view_mode_button == null:
		return
	view_mode_button.text = "■ ADMIN VIEW" if admin_mode else "■ NORMAL VIEW"
	_style_hud_button(view_mode_button, admin_mode)
	if controls_state_label != null:
		controls_state_label.text = "PAUSED" if paused else "RUNNING"
	_refresh_flow_controls()

func _refresh_solar_meter() -> void:
	if solar_meter == null or solar_time_label == null or tick_timer == null:
		return
	var wait: float = maxf(float(tick_timer.wait_time), 0.01)
	var left: float = clampf(float(tick_timer.time_left), 0.0, wait)
	var progress: float = 1.0 - (left / wait)
	solar_meter.value = progress
	if paused:
		solar_time_label.text = "HOLD"
	else:
		solar_time_label.text = "%02ds" % int(ceil(left))

func _set_time_speed(index: int) -> void:
	time_speed_index = clampi(index, 0, time_speeds.size() - 1)
	for i in range(speed_buttons.size()):
		speed_buttons[i].set_pressed_no_signal(i == time_speed_index)
		_style_hud_button(speed_buttons[i], i == time_speed_index)
	if tick_timer != null:
		tick_timer.wait_time = _cycle_wait_seconds()
		tick_timer.start()
		tick_timer.paused = paused
	_log("Time speed set to %dx." % int(time_speeds[time_speed_index]), false)

func _cycle_wait_seconds() -> float:
	return BASE_CYCLE_SECONDS / time_speeds[time_speed_index]

func _update_camera_pan(delta: float) -> void:
	if _gameplay_input_blocked():
		return
	if grid_scroll == null:
		return
	var direction := Vector2.ZERO
	if Input.is_key_pressed(KEY_A):
		direction.x -= 1.0
	if Input.is_key_pressed(KEY_D):
		direction.x += 1.0
	if Input.is_key_pressed(KEY_W):
		direction.y -= 1.0
	if Input.is_key_pressed(KEY_S):
		direction.y += 1.0
	if direction == Vector2.ZERO:
		return
	direction = direction.normalized()
	var speed := 1050.0
	grid_scroll.scroll_horizontal += int(direction.x * speed * delta)
	grid_scroll.scroll_vertical += int(direction.y * speed * delta)

func _apply_grid_zoom() -> void:
	if grid_view != null:
		var grid_size_px := Vector2(GRID_SIZE * get_cell_size(), GRID_SIZE * get_cell_size())
		grid_view.custom_minimum_size = grid_size_px
		grid_view.size = grid_size_px
		grid_view.queue_redraw()
		# Godot 4.6 caches the largest child in get_minimum_size(), not sort.
		# Refresh that cache before applying new scroll limits and centering.
		if grid_scroll != null:
			grid_scroll.get_minimum_size()
			grid_scroll.queue_sort()
	if zoom_label != null:
		zoom_label.text = "%d%%" % int(round((grid_zoom / DEFAULT_GRID_ZOOM) * 100.0))

func get_cell_size() -> float:
	return float(CELL_SIZE) * grid_zoom

func _center_grid_on_core() -> void:
	await get_tree().process_frame
	if grid_scroll == null:
		return
	var core_pixel := Vector2(GRID_SIZE * get_cell_size(), GRID_SIZE * get_cell_size()) * 0.5
	var viewport_size := grid_scroll.get_rect().size
	grid_scroll.scroll_horizontal = int(max(core_pixel.x - viewport_size.x * 0.5, 0.0))
	grid_scroll.scroll_vertical = int(max(core_pixel.y - viewport_size.y * 0.5, 0.0))

func _center_grid_on_station() -> void:
	await get_tree().process_frame
	_center_grid_on_station_now()

func _center_grid_on_station_deferred() -> void:
	_center_grid_on_station.call_deferred()

func _fit_station_view() -> void:
	if grid_scroll == null or placed_rooms.is_empty():
		return
	var bounds := Rect2(Vector2(placed_rooms[0]["pos"]), Vector2.ONE)
	for room in placed_rooms:
		bounds = bounds.merge(Rect2(Vector2(room["pos"]), Vector2.ONE))
	var usable := grid_scroll.size - Vector2(120, 110)
	var fit_zoom := minf(usable.x / ((bounds.size.x + 0.6) * CELL_SIZE), usable.y / ((bounds.size.y + 0.6) * CELL_SIZE))
	_set_grid_zoom(minf(fit_zoom, DEFAULT_GRID_ZOOM * 0.60))
	_center_grid_on_station_deferred()

func _center_grid_on_station_now() -> void:
	if grid_scroll == null or placed_rooms.is_empty():
		return
	var min_cell := Vector2i(GRID_SIZE, GRID_SIZE)
	var max_cell := Vector2i.ZERO
	for room in placed_rooms:
		var pos: Vector2i = room["pos"]
		min_cell.x = mini(min_cell.x, pos.x)
		min_cell.y = mini(min_cell.y, pos.y)
		max_cell.x = maxi(max_cell.x, pos.x)
		max_cell.y = maxi(max_cell.y, pos.y)
	var center_cell := (Vector2(min_cell) + Vector2(max_cell) + Vector2.ONE) * 0.5
	var target_pixel := center_cell * get_cell_size()
	var viewport_size := grid_scroll.get_rect().size
	grid_scroll.scroll_horizontal = int(clamp(target_pixel.x - viewport_size.x * 0.5, 0.0, max(GRID_SIZE * get_cell_size() - viewport_size.x, 0.0)))
	grid_scroll.scroll_vertical = int(clamp(target_pixel.y - viewport_size.y * 0.5, 0.0, max(GRID_SIZE * get_cell_size() - viewport_size.y, 0.0)))

func _refresh_resources() -> void:
	var net := _project_cycle_delta()
	power_capacity = _get_power_capacity()
	_set_resource_chip("metal", "METAL\n%d/%d  %+d" % [resources["metal"], _get_resource_capacity("metal"), net.get("metal", 0)], Color("#9aa2a8"))
	_set_resource_chip("power", "POWER\n%d/%d  %+d" % [resources["power"], power_capacity, net.get("power", 0)], _critical_color(resources["power"], Color("#f5c542"), 2, 0))
	_set_resource_chip("oxygen", "OXYGEN\n%d/%d  %+d" % [resources["oxygen"], _get_resource_capacity("oxygen"), net.get("oxygen", 0)], _critical_color(resources["oxygen"], Color("#7fd4ff"), 2, 0))
	_set_resource_chip("water", "WATER\n%d/%d  %+d" % [int(resources.get("water", 0)), _get_resource_capacity("water"), net.get("water", 0)], Color("#719bff"))
	_set_resource_chip("food", "FOOD\n%d/%d  %+d" % [resources["food"], _get_resource_capacity("food"), net.get("food", 0)], _critical_color(resources["food"], Color("#f0903c"), 2, 0))
	_set_resource_chip("data", "DATA\n%d/%d  %+d" % [resources["data"], _get_resource_capacity("data"), net.get("data", 0)], Color("#4fd0e0"))
	_set_resource_chip("biomass", "BIOMASS\n%d/%d  %+d" % [resources["biomass"], _get_resource_capacity("biomass"), net.get("biomass", 0)], Color("#5fc46a"))
	_set_resource_chip("rare", "RARE\n%d/%d  %+d" % [resources["rare_minerals"], _get_resource_capacity("rare_minerals"), net.get("rare_minerals", 0)], Color("#b07ff0"))
	var integrity_color := Color.WHITE
	if resources["integrity"] < 10:
		integrity_color = Color("#ff3b3b")
	elif resources["integrity"] < 35:
		integrity_color = Color("#ff9f31")
	_set_resource_chip("integrity", "INTEGRITY\n%d%%" % resources["integrity"], integrity_color)
	_set_resource_chip("crew", "CREW\n%d/%d" % [crew_count, _get_crew_capacity()], Color.WHITE)
	var corruption_color := Color.WHITE if corruption < 7 else Color("#ff67b3")
	_set_resource_chip("corruption", "CORRUPTION\n%d/10" % corruption, corruption_color)
	cycle_label.text = "%03d\nCYCLE" % cycle
	var tier: Dictionary = RESONANCE_TIERS[resonance_tier_index]
	resonance_label.text = "RESONANCE\n%03d  ·  %s" % [resonance_score, tier["name"]]
	var next_text := "Maximum tier reached"
	if resonance_tier_index + 1 < RESONANCE_TIERS.size():
		var next_tier: Dictionary = RESONANCE_TIERS[resonance_tier_index + 1]
		next_text = "%d to %s" % [int(next_tier["threshold"]) - resonance_score, next_tier["name"]]
	resonance_label.tooltip_text = "%d active links · %d formed · best cascade x%d · %s" % [active_synergy_links.size(), links_formed, largest_cascade, next_text]

func _critical_color(value: int, normal: Color, warning_at: int, critical_at: int) -> Color:
	if value <= critical_at:
		return Color("#ff3b3b")
	if value <= warning_at:
		return Color("#ff9f31")
	return normal

func _set_resource_chip(id: String, text: String, color: Color) -> void:
	var label: Label
	if resource_labels.has(id):
		label = resource_labels[id]
	else:
		var chip := PanelContainer.new()
		chip.name = "%sChip" % id.capitalize()
		chip.custom_minimum_size = Vector2(124, 42)
		chip.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		chip.tooltip_text = str(RESOURCE_TOOLTIPS.get(id, "Station resource."))
		resource_bar.add_child(chip)
		resource_chips[id] = chip
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 6)
		row.mouse_filter = Control.MOUSE_FILTER_IGNORE
		chip.add_child(row)
		var icon := TextureRect.new()
		icon.custom_minimum_size = Vector2(24, 24)
		icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		icon.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
		row.add_child(icon)
		resource_icon_rects[id] = icon
		label = Label.new()
		label.name = id.capitalize()
		label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		label.add_theme_font_size_override("font_size", 12)
		label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.75))
		row.add_child(label)
		resource_labels[id] = label
	if resource_icon_rects.has(id):
		var icon_rect: TextureRect = resource_icon_rects[id]
		icon_rect.texture = _resource_icon_texture(id)
	var chip_panel: PanelContainer = resource_chips[id]
	var chip_style := StyleBoxFlat.new()
	chip_style.bg_color = Color("#050d10")
	var color_hex := color.to_html(false)
	var warning_state := text.contains(" -") or color_hex == "ff3b3b" or color_hex == "ff9f31"
	chip_style.border_color = Color("#663238") if warning_state else Color("#26383b")
	chip_style.border_width_left = 1
	chip_style.border_width_top = 1
	chip_style.border_width_right = 1
	chip_style.border_width_bottom = 1
	chip_style.corner_radius_top_left = 1
	chip_style.corner_radius_top_right = 1
	chip_style.corner_radius_bottom_left = 1
	chip_style.corner_radius_bottom_right = 1
	chip_style.content_margin_left = 6
	chip_style.content_margin_right = 6
	chip_style.content_margin_top = 4
	chip_style.content_margin_bottom = 4
	chip_panel.add_theme_stylebox_override("panel", chip_style)
	label.text = text
	label.add_theme_color_override("font_color", color)

func _resource_chip_bbcode(text: String, color: Color) -> String:
	var parts := text.split("\n")
	var title: String = parts[0] if parts.size() > 0 else text
	var value_line: String = parts[1] if parts.size() > 1 else ""
	var value_bits := value_line.split(" ", false)
	var main_value: String = value_bits[0] if value_bits.size() > 0 else value_line
	var delta: String = value_bits[value_bits.size() - 1] if value_bits.size() > 1 else ""
	var delta_color: String = "#86bf76"
	if delta.begins_with("-"):
		delta_color = "#d95b63"
	elif delta == "+0" or delta == "0":
		delta_color = "#677a7d"
	return "[color=#6f8080]%s[/color]\n[b][color=#%s]%s[/color][/b] [color=%s]%s[/color]" % [
		title,
		color.to_html(false),
		main_value,
		delta_color,
		delta
	]

func _resource_icon_texture(resource_id: String) -> Texture2D:
	var id := resource_id
	if id == "rare":
		id = "rare_minerals"
	if resource_icon_textures.has(id):
		return resource_icon_textures[id]
	return null

func _resource_icon_bbcode(resource_id: String, icon_size: int = 18) -> String:
	var id := resource_id
	if id == "rare":
		id = "rare_minerals"
	if RESOURCE_ICON_PATHS.has(id):
		return "[img=%dx%d]%s[/img]" % [icon_size, icon_size, str(RESOURCE_ICON_PATHS[id])]
	return RoomDatabaseScript.resource_icon(id)

func _project_cycle_delta() -> Dictionary:
	var result := _simulate_room_economy(true, cycle + 1)
	var delta: Dictionary = result["delta"]
	var projected_crew := crew_count + int(result["added_crew"])
	if projected_crew > 0:
		_add_to_delta(delta, {"food": projected_crew, "oxygen": projected_crew}, -1)
	return delta

func _add_to_delta(delta: Dictionary, values: Dictionary, multiplier: int) -> void:
	for key in values:
		delta[key] = delta.get(key, 0) + int(values[key]) * multiplier

func _without_key(values: Dictionary, removed_key: String) -> Dictionary:
	var filtered := {}
	for key in values:
		if key != removed_key:
			filtered[key] = values[key]
	return filtered

func _get_resource_capacity(resource_id: String) -> int:
	var capacity: int = int(BASE_STORAGE_CAPACITY.get(resource_id, 999))
	for room in placed_rooms:
		capacity += int(room.get("storage", {}).get(resource_id, 0))
	return capacity

func _get_power_capacity() -> int:
	return _get_resource_capacity("power")

func _project_power_demand() -> int:
	var demand := 0
	for room in placed_rooms:
		if not room.get("suspended", false):
			demand += int(room.get("consumption", {}).get("power", 0))
	return demand

func _get_poi_work_capacities() -> Dictionary:
	var capacities := {"mining": 0, "salvage": 0, "life_support": 0}
	for room in placed_rooms:
		if unpowered_room_cells.has(room["pos"]):
			continue
		match room["id"]:
			"mining_drone_bay":
				capacities["mining"] += 1
			"salvage_drone_bay":
				capacities["salvage"] += 1
			"life_support":
				capacities["life_support"] += 1
			"ore_refinery":
				capacities["mining"] += 1
	return capacities

func _clamp_power_reserve() -> void:
	power_capacity = _get_power_capacity()
	resources["power"] = clampi(int(resources["power"]), 0, power_capacity)

func _clamp_resource_storage() -> void:
	for key in BASE_STORAGE_CAPACITY.keys():
		if resources.has(key):
			resources[key] = mini(int(resources[key]), _get_resource_capacity(str(key)))

func _rooms_by_power_priority() -> Array:
	var rooms := placed_rooms.duplicate()
	rooms.sort_custom(_compare_power_priority)
	return rooms

func _compare_power_priority(a: Dictionary, b: Dictionary) -> bool:
	return _power_priority(a) < _power_priority(b)

func _power_priority(room: Dictionary) -> int:
	match room["id"]:
		"brine_core":
			return 0
		"life_support":
			return 10
		"reactor", "solar_array", "battery_array":
			return 20
		"crew_hab", "hydroponics_bay":
			return 30
		"research_lab", "data_archive":
			return 40
		"mining_drone_bay", "salvage_drone_bay", "ore_refinery":
			return 50
		_:
			return 60

func _refresh_cards() -> void:
	if hand_count_label != null:
		hand_count_label.text = "%d/%d" % [hand.size(), HAND_SIZE]
	if reroll_button != null:
		reroll_button.text = "REROLL HAND · %d" % rerolls_remaining
		if rerolls_remaining < REROLL_RECOVERY_CAP:
			reroll_button.text += "\n+1 IN %dC" % (REROLL_RECOVERY_CYCLES - reroll_recovery_progress)
		reroll_button.tooltip_text = "Rebuilds one reroll every %d cycles while below %d charges. Directive rewards may exceed this cap." % [REROLL_RECOVERY_CYCLES, REROLL_RECOVERY_CAP]
		reroll_button.disabled = rerolls_remaining <= 0 or not running
	for child in hand_box.get_children():
		child.queue_free()
	for id in hand:
		var room := RoomDatabaseScript.get_room(id)
		var category_color := RoomDatabaseScript.category_color(room["category"])
		var card_slot := Control.new()
		card_slot.custom_minimum_size = Vector2(286, 296)
		card_slot.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		card_slot.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var card := PanelContainer.new()
		card.name = "%sCard" % id
		card.position = Vector2(0, 14)
		card.size = Vector2(276, 272)
		card.custom_minimum_size = Vector2(276, 272)
		card.mouse_filter = Control.MOUSE_FILTER_STOP
		card.set_meta("card_id", id)
		card.set_meta("category_color", category_color)
		card.set_meta("rest_position", card.position)
		card.set_meta("affordable", _can_afford(room.get("cost", {})))
		_apply_card_style(card, category_color, selected_card_id == id, _can_afford(room.get("cost", {})))
		card.mouse_entered.connect(_on_card_hovered.bind(id, card))
		card.mouse_exited.connect(_on_card_unhovered.bind(id, card))
		card.gui_input.connect(_on_card_gui_input.bind(id))
		var body := VBoxContainer.new()
		body.add_theme_constant_override("separation", 5)
		body.mouse_filter = Control.MOUSE_FILTER_IGNORE
		card.add_child(body)
		var image_wrap := Control.new()
		image_wrap.custom_minimum_size = Vector2(0, 106)
		image_wrap.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(image_wrap)
		var image := TextureRect.new()
		image.set_anchors_preset(Control.PRESET_FULL_RECT)
		image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		image.texture = card_textures.get(id)
		image.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		image.mouse_filter = Control.MOUSE_FILTER_IGNORE
		image_wrap.add_child(image)
		var badge := Label.new()
		badge.text = room["rarity"].to_upper()
		badge.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		badge.position = Vector2(174, 8)
		badge.custom_minimum_size = Vector2(84, 22)
		badge.add_theme_font_size_override("font_size", 11)
		var rarity_color := _rarity_color(str(room.get("rarity", "common")))
		badge.add_theme_color_override("font_color", rarity_color.lightened(0.24))
		badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
		_add_label_panel_style(badge, Color("#08202a"), rarity_color)
		image_wrap.add_child(badge)
		if prototype_card_seen_cycle.has(id):
			var prototype_badge := Label.new()
			prototype_badge.text = "NEW PROTOTYPE"
			prototype_badge.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			prototype_badge.position = Vector2(8, 8)
			prototype_badge.custom_minimum_size = Vector2(112, 22)
			prototype_badge.add_theme_font_size_override("font_size", 10)
			prototype_badge.add_theme_color_override("font_color", Color("#d8fff2"))
			prototype_badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
			_add_label_panel_style(prototype_badge, Color("#0b3029"), UI_ACCENT_BRIGHT)
			image_wrap.add_child(prototype_badge)
		var name_label := Label.new()
		name_label.text = "■ %s" % room["display_name"]
		name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		name_label.add_theme_font_size_override("font_size", 17)
		name_label.add_theme_color_override("font_color", Color("#f2f7fb"))
		name_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(name_label)
		var output_label := RichTextLabel.new()
		output_label.bbcode_enabled = true
		output_label.fit_content = true
		output_label.scroll_active = false
		output_label.text = _primary_output_line(room)
		output_label.add_theme_font_size_override("normal_font_size", 13)
		output_label.add_theme_color_override("default_color", Color("#8fa3ae"))
		output_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(output_label)
		var cost_label := RichTextLabel.new()
		cost_label.bbcode_enabled = true
		cost_label.fit_content = true
		cost_label.scroll_active = false
		cost_label.text = "[color=#607784]COST[/color]  %s" % _format_resource_list(room.get("cost", {}), 14)
		cost_label.add_theme_font_size_override("normal_font_size", 11)
		cost_label.add_theme_color_override("default_color", Color("#607784") if _can_afford(room.get("cost", {})) else Color("#ff6c75"))
		cost_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(cost_label)
		var synergy_label := RichTextLabel.new()
		synergy_label.bbcode_enabled = true
		synergy_label.fit_content = true
		synergy_label.scroll_active = false
		synergy_label.text = _card_synergy_hint(id)
		synergy_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		synergy_label.add_theme_font_size_override("normal_font_size", 10)
		synergy_label.add_theme_color_override("default_color", Color("#6f9f8f"))
		synergy_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(synergy_label)
		var footer_label := Label.new()
		footer_label.text = "LMB BUILD   RMB REROLL"
		footer_label.add_theme_font_size_override("font_size", 10)
		footer_label.add_theme_color_override("font_color", Color("#3f5663"))
		footer_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(footer_label)
		card_slot.add_child(card)
		hand_box.add_child(card_slot)
	_add_deck_slot()

func _card_synergy_hint(room_id: String) -> String:
	var best_synergy := {}
	var best_score := -1
	for synergy in SynergyManagerScript.all_synergies():
		var synergy_id := str(synergy.get("id", ""))
		if not meta.discovered_synergy_ids.has(synergy_id):
			continue
		var room_ids: Array = synergy.get("rooms", [])
		if not room_ids.has(room_id):
			continue
		var score := 0
		if active_synergies.has(synergy_id):
			score = 3
		elif _connected_synergy_link_count(synergy_id) > 0:
			score = 2
		else:
			score = 1
		if score > best_score:
			best_score = score
			best_synergy = synergy
	if not best_synergy.is_empty():
		var partner_names: Array[String] = []
		for other_id_value in best_synergy.get("rooms", []):
			var other_id := str(other_id_value)
			if other_id == room_id:
				continue
			var other_room := RoomDatabaseScript.get_room(other_id)
			partner_names.append(str(other_room.get("display_name", _prettify_id(other_id))))
		var bonus := _format_resource_list(best_synergy.get("bonus", {}), 14)
		if bonus == "None":
			bonus = "special link"
		var stack_text := ""
		var active_count := _active_synergy_link_count(str(best_synergy["id"]))
		if active_count > 0:
			stack_text = " x%d" % active_count
		return "LINK%s  %s · %s -> %s" % [stack_text, best_synergy.get("name", "LEARNED PATTERN"), _join_strings(partner_names, " + "), bonus]
	return "LINK  EXPERIMENTAL CONFIGURATION"

func _add_deck_slot() -> void:
	var slot := PanelContainer.new()
	slot.name = "DeckSlot"
	slot.custom_minimum_size = Vector2(146, 260)
	slot.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	var texture_style := _make_texture_stylebox(UI_TERMINAL_PANEL, 16, 12, 12, 12, 12)
	if texture_style != null:
		slot.add_theme_stylebox_override("panel", texture_style)
	else:
		var style := StyleBoxFlat.new()
		style.bg_color = Color(0.02, 0.035, 0.045, 0.58)
		style.border_color = Color("#1c3038")
		style.border_width_left = 1
		style.border_width_top = 1
		style.border_width_right = 1
		style.border_width_bottom = 1
		style.content_margin_left = 10
		style.content_margin_right = 10
		style.content_margin_top = 8
		style.content_margin_bottom = 8
		slot.add_theme_stylebox_override("panel", style)
	var label := Label.new()
	label.text = "/////\n%d DRAW\n%d DISCARD" % [draw_pile.size(), discard_pile.size()]
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 18)
	label.add_theme_color_override("font_color", Color("#3e5360"))
	slot.add_child(label)
	hand_box.add_child(slot)

func _apply_card_style(card: PanelContainer, color: Color, selected: bool, affordable := true) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.02, 0.035, 0.045, 0.78) if not selected else Color(0.03, 0.07, 0.08, 0.88)
	if not affordable:
		style.bg_color = Color(0.018, 0.024, 0.03, 0.78) if not selected else Color(0.055, 0.065, 0.075, 0.88)
	style.border_color = UI_ACCENT_BRIGHT if selected else Color(color.r, color.g, color.b, 0.78)
	if not affordable and not selected:
		style.border_color = Color("#30424a")
	style.border_width_left = 3
	style.border_width_top = 2
	style.border_width_right = 2
	style.border_width_bottom = 2
	style.corner_radius_top_left = 0
	style.corner_radius_top_right = 0
	style.corner_radius_bottom_left = 0
	style.corner_radius_bottom_right = 0
	style.content_margin_left = 10
	style.content_margin_right = 10
	style.content_margin_top = 8
	style.content_margin_bottom = 8
	card.add_theme_stylebox_override("panel", style)
	if not affordable:
		card.modulate = Color(0.72, 0.76, 0.78, 0.78)
	elif selected:
		card.modulate = Color(1.06, 1.10, 1.06, 1.0)
	else:
		card.modulate = Color.WHITE

func _rarity_color(rarity: String) -> Color:
	match rarity.to_lower():
		"core":
			return Color("#bffaff")
		"common":
			return Color("#7f9ba3")
		"uncommon":
			return Color("#4fa38d")
		"rare":
			return Color("#b982ff")
		"derelict":
			return Color("#a86d45")
		_:
			return UI_ACCENT_BRIGHT

func _add_label_panel_style(label: Label, bg_color: Color, border_color: Color) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.02, 0.035, 0.045, 0.70)
	style.border_color = Color(border_color.r, border_color.g, border_color.b, 0.62)
	style.border_width_left = 1
	style.border_width_top = 1
	style.border_width_right = 1
	style.border_width_bottom = 1
	style.content_margin_left = 4
	style.content_margin_right = 4
	style.content_margin_top = 2
	style.content_margin_bottom = 2
	label.add_theme_stylebox_override("normal", style)

func _primary_output_line(room: Dictionary) -> String:
	var production: Dictionary = room.get("production", {})
	if production.is_empty():
		return "Support structure"
	return "+%s" % _format_resource_list(production, 16)

func _load_ui_textures() -> void:
	ui_textures.clear()
	for path in [
		UI_PANEL_LARGE,
		UI_PANEL_MEDIUM,
		UI_PANEL_TOOLTIP,
		UI_PANEL_WARNING,
		UI_PANEL_MINIMAL,
		UI_BUTTON_NORMAL,
		UI_BUTTON_HOVER,
		UI_BUTTON_PRESSED,
		UI_DIVIDER_HORIZONTAL,
		UI_DIVIDER_VERTICAL,
		UI_TERMINAL_PANEL,
		UI_TERMINAL_PANEL_LARGE,
		UI_TERMINAL_PANEL_WARNING,
		UI_TERMINAL_BUTTON_NORMAL,
		UI_TERMINAL_BUTTON_HOVER,
		UI_TERMINAL_BUTTON_PRESSED,
		UI_TERMINAL_DIVIDER_HORIZONTAL,
		UI_TERMINAL_DIVIDER_VERTICAL
	]:
		var texture := _load_raw_png_texture(str(path))
		if texture != null:
			ui_textures[path] = texture

func _load_resource_icon_textures() -> void:
	resource_icon_textures.clear()
	for id in RESOURCE_ICON_PATHS:
		var path := str(RESOURCE_ICON_PATHS[id])
		var texture := _load_raw_png_texture(path)
		if texture != null:
			resource_icon_textures[id] = texture

func _load_raw_png_texture(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var resource := ResourceLoader.load(path)
		if resource is Texture2D:
			return resource
	var image := Image.new()
	var error := image.load(path)
	if error != OK:
		return null
	var texture := ImageTexture.create_from_image(image)
	return texture

func _load_card_textures() -> void:
	for id in room_texture_paths:
		var texture := _load_card_thumbnail(room_texture_paths[id])
		if texture != null:
			card_textures[id] = texture

func _load_card_thumbnail(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var resource := ResourceLoader.load(path)
		if resource is Texture2D:
			return resource
	var image := Image.new()
	var error := image.load(path)
	if error != OK:
		return null
	return ImageTexture.create_from_image(image)

func _on_card_pressed(id: String) -> void:
	if _gameplay_input_blocked() or not running:
		return
	_clear_prototype_marker(id)
	selected_card_id = id
	last_preview_room_id = id
	last_previewing_card = true
	selected_rotation = 0
	_refresh_cards()
	_refresh_inspector()

func _on_card_hovered(id: String, card: Control) -> void:
	if _gameplay_input_blocked() or not running:
		return
	if not is_instance_valid(card) or not card is PanelContainer:
		return
	hovered_card_id = id
	last_preview_room_id = id
	last_previewing_card = true
	card.pivot_offset = card.size * 0.5
	var rest_position: Vector2 = card.get_meta("rest_position", card.position)
	card.position = rest_position + Vector2(0, -22)
	card.scale = Vector2(1.035, 1.035)
	var color: Color = card.get_meta("category_color", UI_ACCENT_BRIGHT)
	var affordable: bool = card.get_meta("affordable", true)
	_apply_card_style(card, color.lightened(0.18), true, affordable)
	card.move_to_front()
	_refresh_inspector()

func _on_card_unhovered(id: String, card: Control) -> void:
	if _gameplay_input_blocked():
		return
	if not is_instance_valid(card) or not card is PanelContainer:
		return
	if hovered_card_id == id:
		hovered_card_id = ""
	var rest_position: Vector2 = card.get_meta("rest_position", card.position)
	card.position = rest_position
	card.scale = Vector2.ONE
	var color: Color = card.get_meta("category_color", UI_ACCENT_BRIGHT)
	var affordable: bool = card.get_meta("affordable", true)
	_apply_card_style(card, color, selected_card_id == id, affordable)
	_refresh_inspector()

func _on_card_gui_input(event: InputEvent, id: String) -> void:
	if _gameplay_input_blocked() or not running:
		get_viewport().set_input_as_handled()
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		_on_card_pressed(id)
		get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_RIGHT:
		_discard_card(id)
		get_viewport().set_input_as_handled()

func _discard_selected_card() -> void:
	if selected_card_id.is_empty():
		return
	_discard_card(selected_card_id)

func _discard_card(id: String) -> void:
	if _gameplay_input_blocked() or not running or not hand.has(id):
		return
	if rerolls_remaining <= 0:
		_log("No blueprint rerolls remain. Build from the current hand.", false)
		return
	if rerolls_remaining >= REROLL_RECOVERY_CAP:
		reroll_recovery_progress = 0
	rerolls_remaining -= 1
	hand.erase(id)
	discard_pile.append(id)
	_refill_hand()
	selected_card_id = hand[0] if not hand.is_empty() else ""
	hovered_card_id = ""
	_log("Blueprint rerolled: %s. %d charge%s remain." % [RoomDatabaseScript.get_room(id).get("display_name", id), rerolls_remaining, "s" if rerolls_remaining != 1 else ""], false)
	_refresh_all()

func _discard_all_cards() -> void:
	if _gameplay_input_blocked() or not running or hand.is_empty():
		return
	if rerolls_remaining <= 0:
		_log("No blueprint rerolls remain. Build from the current hand.", false)
		return
	if rerolls_remaining >= REROLL_RECOVERY_CAP:
		reroll_recovery_progress = 0
	rerolls_remaining -= 1
	for id_value in hand:
		discard_pile.append(str(id_value))
	hand.clear()
	selected_card_id = ""
	hovered_card_id = ""
	_refill_hand()
	selected_card_id = hand[0] if not hand.is_empty() else ""
	_log("Draft hand rerolled. %d charge%s remain." % [rerolls_remaining, "s" if rerolls_remaining != 1 else ""], false)
	_refresh_all()

func _unhandled_input(event: InputEvent) -> void:
	if doctrine_layer != null and doctrine_layer.visible:
		return
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		if _journal_is_open():
			_toggle_journal()
		else:
			_toggle_menu()
		get_viewport().set_input_as_handled()
		return
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_J:
		_toggle_journal()
		get_viewport().set_input_as_handled()
		return
	if _gameplay_input_blocked():
		return
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_F:
		_fit_station_view()
		get_viewport().set_input_as_handled()
		return
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_SPACE:
		_toggle_pause()
		get_viewport().set_input_as_handled()
		return
	if event.is_action_pressed("rotate_room"):
		_rotate_selected_room()
		get_viewport().set_input_as_handled()
		return
	if event.is_action_pressed("toggle_admin_mode"):
		admin_mode = not admin_mode
		_log("Admin topology overlay %s." % ("enabled" if admin_mode else "hidden"), false)
		_refresh_all()
		get_viewport().set_input_as_handled()
		return
	if event is InputEventMouseButton and event.pressed and event.shift_pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			_set_grid_zoom(grid_zoom + 0.05)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			_set_grid_zoom(grid_zoom - 0.05)

func _rotate_selected_room() -> void:
	if selected_card_id.is_empty():
		return
	selected_rotation = (selected_rotation + 1) % 4
	_refresh_all()

func _doors_connect(new_id: String, room_rotation: int, offset: Vector2i, neighbor: Dictionary) -> bool:
	var new_side := _side_from_offset(offset)
	var neighbor_side := _opposite_side(new_side)
	return _room_doors(new_id, room_rotation).has(new_side) and _room_doors(neighbor["id"], int(neighbor.get("rotation", 0))).has(neighbor_side)

func _room_doors(room_id: String, room_rotation: int) -> Array:
	if room_id == "reactor":
		return ["north", "east", "south", "west"]
	var room := RoomDatabaseScript.get_room(room_id)
	var layout := RoomDatabaseScript.get_layout(room.get("layout", "cross"))
	var doors: Array = layout.get("doors", [])
	var rotated := []
	for door in doors:
		rotated.append(_rotate_side(str(door), room_rotation))
	return rotated

func _side_from_offset(offset: Vector2i) -> String:
	if offset == Vector2i.UP:
		return "north"
	if offset == Vector2i.RIGHT:
		return "east"
	if offset == Vector2i.DOWN:
		return "south"
	return "west"

func _opposite_side(side: String) -> String:
	match side:
		"north":
			return "south"
		"east":
			return "west"
		"south":
			return "north"
		_:
			return "east"

func _rotate_side(side: String, rotation_steps: int) -> String:
	var sides := ["north", "east", "south", "west"]
	var index := sides.find(side)
	if index < 0:
		return side
	return sides[(index + rotation_steps) % sides.size()]

func get_room_doors(room: Dictionary) -> Array:
	return _room_doors(room["id"], int(room.get("rotation", 0)))

func get_room_layout(room: Dictionary) -> Dictionary:
	return RoomDatabaseScript.get_layout(room.get("layout", "cross"))

func _update_test_walker(delta: float) -> void:
	if not occupied.has(test_walker_cell):
		return
	if test_walker_state == "idle":
		test_walker_break_timer -= delta
		if test_walker_break_timer > 0.0:
			return
	if test_walker_next_cell == Vector2i(-1, -1) or not occupied.has(test_walker_next_cell):
		test_walker_next_cell = _choose_walker_next_cell(test_walker_cell)
		test_walker_progress = 0.0
		if test_walker_next_cell == Vector2i(-1, -1):
			test_walker_state = "idle"
			test_walker_break_timer = 0.8
			return
		test_walker_direction = _direction_for_offset(test_walker_next_cell - test_walker_cell)
		_choose_walker_motion_state()
	test_walker_progress += delta * test_walker_speed
	if test_walker_progress >= 1.0:
		test_walker_previous_cell = test_walker_cell
		test_walker_cell = test_walker_next_cell
		test_walker_progress = 0.0
		if rng.randf() < 0.07:
			test_walker_state = "idle"
			test_walker_break_timer = rng.randf_range(0.20, 0.75)
			test_walker_next_cell = Vector2i(-1, -1)
		else:
			test_walker_next_cell = _choose_walker_next_cell(test_walker_cell)
			if test_walker_next_cell == Vector2i(-1, -1):
				test_walker_state = "idle"
				test_walker_break_timer = rng.randf_range(0.35, 1.0)
			else:
				test_walker_direction = _direction_for_offset(test_walker_next_cell - test_walker_cell)
				_choose_walker_motion_state()

func _choose_walker_motion_state() -> void:
	if rng.randf() < 0.22:
		test_walker_state = "run"
		test_walker_speed = 0.28
	else:
		test_walker_state = "walk"
		test_walker_speed = rng.randf_range(0.11, 0.16)

func _choose_walker_next_cell(cell: Vector2i) -> Vector2i:
	var neighbors := _connected_neighbor_cells(cell)
	if neighbors.is_empty():
		return Vector2i(-1, -1)
	if neighbors.size() > 1 and neighbors.has(test_walker_previous_cell):
		neighbors.erase(test_walker_previous_cell)
	return neighbors[rng.randi_range(0, neighbors.size() - 1)]

func _connected_neighbor_cells(cell: Vector2i) -> Array:
	var neighbors := []
	if not occupied.has(cell):
		return neighbors
	for offset in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
		var neighbor_cell: Vector2i = cell + offset
		if occupied.has(neighbor_cell) and _placed_rooms_connected(occupied[cell], occupied[neighbor_cell], offset):
			neighbors.append(neighbor_cell)
	return neighbors

func _placed_rooms_connected(room: Dictionary, neighbor: Dictionary, offset: Vector2i) -> bool:
	var side := _side_from_offset(offset)
	var opposite := _opposite_side(side)
	return get_room_doors(room).has(side) and get_room_doors(neighbor).has(opposite)

func get_test_walker_position() -> Vector2:
	if test_walker_next_cell == Vector2i(-1, -1) or not occupied.has(test_walker_next_cell):
		return _room_idle_anchor(test_walker_cell)
	var offset := test_walker_next_cell - test_walker_cell
	var exit_side := _side_from_offset(offset)
	var entry_side := _opposite_side(exit_side)
	var start_side := exit_side
	if test_walker_previous_cell != Vector2i(-1, -1) and test_walker_previous_cell != test_walker_next_cell:
		var previous_offset := test_walker_previous_cell - test_walker_cell
		if abs(previous_offset.x) + abs(previous_offset.y) == 1:
			start_side = _side_from_offset(previous_offset)
	var path_points: Array = []
	path_points.append_array(_room_path_to_door(test_walker_cell, start_side, exit_side))
	path_points.append(_door_point(test_walker_cell, exit_side))
	path_points.append(_door_point(test_walker_next_cell, entry_side))
	path_points.append_array(_room_path_from_door(test_walker_next_cell, entry_side))
	return _sample_polyline(_dedupe_path_points(path_points), test_walker_progress)

func get_test_walker_direction() -> String:
	if test_walker_next_cell == Vector2i(-1, -1):
		return test_walker_direction
	return _direction_for_offset(test_walker_next_cell - test_walker_cell)

func _direction_for_offset(offset: Vector2i) -> String:
	if offset == Vector2i.UP:
		return "north"
	if offset == Vector2i.RIGHT:
		return "east"
	if offset == Vector2i.DOWN:
		return "south"
	return "west"

func get_test_walker_state() -> String:
	return test_walker_state

func has_test_walker() -> bool:
	return occupied.has(test_walker_cell)

func _cell_center(cell: Vector2i) -> Vector2:
	var cell_size := get_cell_size()
	return Vector2(cell) * cell_size + Vector2(cell_size, cell_size) * 0.5

func _door_point(cell: Vector2i, side: String) -> Vector2:
	var center := _cell_center(cell)
	var cell_size := get_cell_size()
	match side:
		"north":
			return center + Vector2(0, -cell_size * 0.5 + 4)
		"east":
			return center + Vector2(cell_size * 0.5 - 4, cell_size * 0.035)
		"south":
			return center + Vector2(0, cell_size * 0.5 - 4)
		_:
			return center + Vector2(-cell_size * 0.5 + 4, cell_size * 0.035)

func _room_walk_anchor(cell: Vector2i, door_side: String) -> Vector2:
	if not occupied.has(cell):
		return _cell_center(cell)
	var room: Dictionary = occupied[cell]
	if str(get_room_layout(room).get("path", "")) != "perimeter":
		return _cell_center(cell)
	return _perimeter_walk_anchor(cell, door_side)

func _room_idle_anchor(cell: Vector2i) -> Vector2:
	if not occupied.has(cell):
		return _cell_center(cell)
	var room: Dictionary = occupied[cell]
	if str(get_room_layout(room).get("path", "")) == "perimeter":
		if test_walker_previous_cell != Vector2i(-1, -1):
			var previous_offset := test_walker_previous_cell - cell
			if abs(previous_offset.x) + abs(previous_offset.y) == 1:
				return _perimeter_walk_anchor(cell, _side_from_offset(previous_offset))
		return _perimeter_walk_anchor(cell, "south")
	return _cell_center(cell)

func _room_path_to_door(cell: Vector2i, from_side: String, to_side: String) -> Array:
	if not occupied.has(cell):
		return [_cell_center(cell)]
	var room: Dictionary = occupied[cell]
	if str(get_room_layout(room).get("path", "")) != "perimeter":
		return [_cell_center(cell)]
	return _perimeter_points_between(cell, from_side, to_side)

func _room_path_from_door(cell: Vector2i, side: String) -> Array:
	if not occupied.has(cell):
		return [_cell_center(cell)]
	var room: Dictionary = occupied[cell]
	if str(get_room_layout(room).get("path", "")) != "perimeter":
		return [_cell_center(cell)]
	return [_perimeter_walk_anchor(cell, side)]

func _perimeter_walk_anchor(cell: Vector2i, door_side: String) -> Vector2:
	var center := _cell_center(cell)
	var cell_size := get_cell_size()
	var offset := cell_size * 0.30
	match door_side:
		"north":
			return center + Vector2(0, -offset)
		"east":
			return center + Vector2(offset, 0)
		"south":
			return center + Vector2(0, offset)
		_:
			return center + Vector2(-offset, 0)

func _perimeter_points_between(cell: Vector2i, from_side: String, to_side: String) -> Array:
	var order := ["north", "east", "south", "west"]
	var from_index := order.find(from_side)
	var to_index := order.find(to_side)
	if from_index < 0 or to_index < 0:
		return [_perimeter_walk_anchor(cell, to_side)]
	var clockwise_steps := (to_index - from_index + order.size()) % order.size()
	var counter_steps := (from_index - to_index + order.size()) % order.size()
	var step := 1 if clockwise_steps <= counter_steps else -1
	var count: int = mini(clockwise_steps, counter_steps)
	var points: Array = []
	var index := from_index
	for i in range(count + 1):
		points.append(_perimeter_walk_anchor(cell, str(order[index])))
		index = (index + step + order.size()) % order.size()
	return points

func _dedupe_path_points(points: Array) -> Array:
	var cleaned: Array = []
	for point_value in points:
		var point: Vector2 = point_value
		if cleaned.is_empty() or (cleaned[cleaned.size() - 1] as Vector2).distance_to(point) > 0.5:
			cleaned.append(point)
	return cleaned

func _sample_polyline(points: Array, progress: float) -> Vector2:
	if points.size() < 2:
		return Vector2.ZERO
	var lengths: Array[float] = []
	var total_length: float = 0.0
	for i in range(points.size() - 1):
		var start: Vector2 = points[i]
		var end: Vector2 = points[i + 1]
		var length: float = max(start.distance_to(end), 0.001)
		lengths.append(length)
		total_length += length
	var target_distance: float = clampf(progress, 0.0, 1.0) * total_length
	var walked: float = 0.0
	for i in range(lengths.size()):
		var segment_length: float = lengths[i]
		if target_distance <= walked + segment_length:
			var local_t: float = (target_distance - walked) / segment_length
			return (points[i] as Vector2).lerp(points[i + 1] as Vector2, local_t)
		walked += segment_length
	return points[points.size() - 1] as Vector2

func get_current_poi_name() -> String:
	return orbit.get_current_poi_name()

func get_current_poi_progress() -> float:
	return orbit.get_current_poi_progress()

func _refresh_inspector() -> void:
	var room := {}
	var previewing_card := false
	if not hovered_card_id.is_empty():
		room = RoomDatabaseScript.get_room(hovered_card_id)
		previewing_card = true
	elif occupied.has(hover_cell):
		room = occupied[hover_cell]
	elif not selected_card_id.is_empty():
		room = RoomDatabaseScript.get_room(selected_card_id)
		previewing_card = true
	elif occupied.has(selected_room_cell):
		room = occupied[selected_room_cell]
	if room.is_empty() and not last_preview_room_id.is_empty():
		room = RoomDatabaseScript.get_room(last_preview_room_id)
		previewing_card = last_previewing_card
	if room_operation_button != null:
		var can_control: bool = not previewing_card and room.has("pos") and room.get("id", "") != "brine_core"
		room_operation_button.disabled = not can_control or not running
		room_operation_button.set_meta("cell", room.get("pos", Vector2i(-1, -1)))
		room_operation_button.text = ("RESUME ROOM" if room.get("suspended", false) else "SUSPEND ROOM") if can_control else "SELECT A BUILT ROOM TO CONTROL"
		room_operation_button.tooltip_text = "Suspended rooms stop production and links. Resuming takes effect next cycle."
	if room.is_empty():
		preview_texture.texture = null
		preview_name_label.text = "No Selection"
		preview_tags_label.text = "SYSTEM IDLE"
		preview_name_label.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
		inspector_label.text = _join_strings([
			"[color=#70848a]Hover a room or card for analysis.[/color]",
			"[color=#70848a]Station integrity:[/color] [color=#c9d3ce]%d%%[/color]" % resources["integrity"],
			"",
			_preview_divider(),
			"",
			"[color=#34484b]BRINE waits in low orbit. Select a module to read its pattern.[/color]",
			"",
			_preview_divider()
		], "\n")
		return
	preview_texture.texture = card_textures.get(room["id"])
	preview_name_label.text = room["display_name"]
	var category_color: Color = RoomDatabaseScript.category_color(str(room.get("category", "")))
	var category_hex: String = category_color.to_html(false)
	preview_name_label.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	preview_tags_label.text = "CLASS: %s     %s" % [str(room.get("category", "")).to_upper(), str(room.get("rarity", "")).to_upper()]
	preview_tags_label.add_theme_color_override("font_color", Color("#95a7a0"))
	var preview_lines: Array[String] = []
	preview_lines.append("[color=#7f929c]CLASS:[/color] [color=#%s]%s[/color]" % [category_hex, str(room.get("category", "")).to_upper()])
	preview_lines.append("[color=#b9c6cc]%s[/color]" % room.get("description", ""))
	if not previewing_card and room.has("pos"):
		var operation := str(offline_reasons.get(room["pos"], "FUNCTIONING" if powered_room_cells.has(room["pos"]) else "AWAITING CYCLE"))
		preview_lines.append("[color=#f0c67a]%s[/color]" % operation)
		preview_lines.append("")
		_append_room_synergy_preview(preview_lines, room)
	preview_lines.append("")
	preview_lines.append(_preview_divider())
	preview_lines.append("[color=#%s]EFFECTS[/color]" % UI_ACCENT_BRIGHT.to_html(false))
	preview_lines.append(_format_effect_rows(room.get("production", {}), "+", false))
	if not room.get("consumption", {}).is_empty():
		preview_lines.append("")
		preview_lines.append("[color=#c85b61]DRAWS[/color]")
		preview_lines.append(_format_effect_rows(room.get("consumption", {}), "-", true))
	if previewing_card:
		preview_lines.append("")
		preview_lines.append(_preview_divider())
		preview_lines.append("[color=#c85b61]BUILD COST[/color]")
		preview_lines.append(_format_effect_rows(room.get("cost", {}), "", false, false))
	if not room.get("storage", {}).is_empty():
		preview_lines.append("")
		preview_lines.append("[color=#7f929c]STORAGE[/color]")
		preview_lines.append("[color=#9fb2bc]%s[/color]" % _format_storage(room.get("storage", {})))
	if previewing_card and not testing_free_build and not _can_afford(room.get("cost", {})):
		preview_lines.append("")
		preview_lines.append("[color=#ff4d5a]MISSING: %s[/color]" % _format_resource_list(_missing_cost(room.get("cost", {}))))
	preview_lines.append("")
	preview_lines.append(_preview_divider())
	if previewing_card:
		_append_room_synergy_preview(preview_lines, room)
	var capacities := _get_poi_work_capacities()
	preview_lines.append("")
	preview_lines.append(_preview_divider())
	preview_lines.append("[color=#596d77]%s[/color]" % _room_flavor_line(room))
	preview_lines.append("")
	preview_lines.append("[color=#4f6470]%s[/color]" % orbit.get_panel_text().replace("\n", "  ·  "))
	preview_lines.append("[color=#607784]Capacity: Mining %d | Salvage %d | Life %d[/color]" % [capacities.get("mining", 0), capacities.get("salvage", 0), capacities.get("life_support", 0)])
	inspector_label.text = _join_strings(preview_lines, "\n")

func _append_room_synergy_preview(lines: Array, room: Dictionary) -> void:
	var room_id := str(room.get("id", ""))
	var relevant: Array = []
	var unknown_count := 0
	for synergy in SynergyManagerScript.all_synergies():
		if meta.discovered_synergy_ids.has(synergy["id"]):
			if synergy.get("rooms", []).has(room_id):
				relevant.append(synergy)
		else:
			unknown_count += 1
	lines.append("[color=#%s]SYNERGIES[/color]" % UI_ACCENT_BRIGHT.to_html(false))
	lines.append("[color=#607784]%d learned for this room[/color]" % relevant.size())
	if relevant.is_empty():
		lines.append("[color=#33515e]No recovered patterns for this room yet.[/color]")
	for synergy in relevant:
		lines.append(_format_synergy_line(synergy))
	if unknown_count > 0:
		lines.append("[color=#405663]UNKNOWN PATTERNS REMAIN: %d[/color]" % unknown_count)
		lines.append("[color=#405663]Power experimental configurations to recover them.[/color]")

func _format_synergy_line(synergy: Dictionary) -> String:
	var room_ids: Array = synergy.get("rooms", [])
	var room_names: Array[String] = []
	var active := active_synergies.has(synergy["id"])
	for id_value in room_ids:
		var id := str(id_value)
		var room := RoomDatabaseScript.get_room(id)
		var color := "#607784"
		if _has_room(id):
			color = "#%s" % RoomDatabaseScript.category_color(room.get("category", "")).to_html(false)
		var room_name := str(room.get("display_name", _prettify_id(id)))
		if active:
			room_name = "◆ %s" % room_name
		room_names.append("[color=%s]%s[/color]" % [color, room_name])
	var bonus_text := _format_resource_list(synergy.get("bonus", {}))
	if bonus_text == "None":
		bonus_text = str(synergy.get("effect", "Special effect restored."))
	else:
		bonus_text = "%s  —  %s" % [bonus_text, synergy.get("effect", "")]
	var active_count := _active_synergy_link_count(str(synergy["id"]))
	var status := _synergy_runtime_status(str(synergy["id"]))
	if active_count > 1:
		status += " x%d" % active_count
	var result := "[color=#c4d1da]• %s[/color]\n[color=#%s]%s[/color]\n[color=#8fa3ae]%s[/color]\n[color=#8ccf6f]%s[/color]\n[color=#ecc98d]%s[/color]" % [synergy["name"], str(synergy.get("fx_color", "4fa38d")).trim_prefix("#"), status, _join_strings(room_names, " + "), str(synergy.get("effect", bonus_text)), _synergy_reward_text(synergy)]
	return result

func _synergy_reward_text(synergy: Dictionary) -> String:
	if not meta.discovered_synergy_ids.has(synergy.get("id", "")):
		return ""
	var stabilized := meta.stabilized_synergy_ids.has(synergy["id"])
	var target := str(synergy.get("unlock_room_id", ""))
	if not target.is_empty():
		var name := str(RoomDatabaseScript.get_room(target).get("display_name", target))
		return "BLUEPRINT %s · %s" % ["DECRYPTED" if stabilized else "AT 3 CYCLES", name]
	return "RESEARCH %s · +%d" % ["RECOVERED" if stabilized else "AT 3 CYCLES", int(synergy.get("terminal_reward", {}).get("research", 0))]

func _active_synergy_link_count(synergy_id: String) -> int:
	var count := 0
	for link in active_synergy_links:
		if str(link.get("id", "")) == synergy_id:
			count += 1
	return count

func _connected_synergy_link_count(synergy_id: String) -> int:
	var count := 0
	for link in connected_synergy_links:
		if str(link.get("id", "")) == synergy_id:
			count += 1
	return count

func _synergy_runtime_status(synergy_id: String) -> String:
	var is_active := _active_synergy_link_count(synergy_id) > 0
	var is_connected := _connected_synergy_link_count(synergy_id) > 0
	var is_stabilized := meta.stabilized_synergy_ids.has(synergy_id)
	if is_active and is_stabilized:
		return "ACTIVE · STABILIZED"
	if is_active:
		var progress := int(synergy_stabilization_progress.get(synergy_id, 0))
		var required := int(SynergyManagerScript.get_synergy(synergy_id).get("stabilize_cycles", 3))
		return "ACTIVE · STABILIZING %d/%d" % [progress, required]
	if is_connected:
		return "DORMANT · RESTORE ROOM SUPPLIES"
	return "STABILIZED" if is_stabilized else "DISCOVERED"

func _preview_divider() -> String:
	return "[color=#34434a]────────────────────────[/color]"

func _format_effect_rows(values: Dictionary, prefix: String, negative: bool, per_cycle := true) -> String:
	if values.is_empty():
		return "[color=#526670]None[/color]"
	var rows: Array[String] = []
	for key in values:
		var id := str(key)
		var amount := int(values[key])
		var prefix_text := prefix
		if prefix_text.is_empty() and amount > 0:
			prefix_text = "+"
		var value_color := "#d9e6ec"
		if negative:
			value_color = "#b65b62"
		elif id == "biomass" or id == "food":
			value_color = "#8ccf6f"
		elif id == "oxygen" or id == "water":
			value_color = "#79bde8"
		elif id == "power":
			value_color = "#e1c34e"
		elif id == "rare_minerals":
			value_color = "#b982ff"
		elif id == "data":
			value_color = "#62d6d2"
		rows.append("%s     [color=%s]%s%d[/color] [color=#8d9ba2]%s[/color]   [color=#526670]%s[/color]" % [
			_resource_icon_bbcode(id, 22),
			value_color,
			prefix_text,
			amount,
			"/ cycle" if per_cycle else "once",
			id.replace("_", " ").capitalize()
		])
	return _join_strings(rows, "\n")

func _room_flavor_line(room: Dictionary) -> String:
	match str(room.get("category", "")):
		"Bio":
			return "\"Water in. Air out. Keep it clean.\""
		"Engineering":
			return "\"If it hums, it can be persuaded.\""
		"Science":
			return "\"Every signal is a memory trying to surface.\""
		"Medical":
			return "\"Warm the room before you wake the dead.\""
		"Anomaly":
			return "\"Containment is just curiosity with manners.\""
		"Drone":
			return "\"Small machines remember the work.\""
		"Core":
			return "\"BRINE listens through the walls.\""
		_:
			return "\"Station pattern recovered.\""

func _preview_room(room: Dictionary, title: String) -> String:
	if room.is_empty():
		return "No room data."
	var adjacent_synergies := []
	for synergy in active_synergies.values():
		if synergy.get("rooms", []).has(room["id"]):
			adjacent_synergies.append(synergy["name"])
	var missing := "None"
	if not testing_free_build and not _can_afford(room.get("cost", {})):
		missing = _format_cost(room.get("cost", {}))
	return "%s\n%s | %s\nCost: %s\nProduces: %s\nConsumes: %s\nMissing: %s\nPossible synergies: %s" % [
		title,
		room["display_name"],
		room["category"],
		_format_cost(room.get("cost", {})),
		_format_cost(room.get("production", {})),
		_format_cost(room.get("consumption", {})),
		missing,
		_join_strings(adjacent_synergies) if adjacent_synergies.size() > 0 else "None active"
	]

func _refresh_archive() -> void:
	if archive_label == null:
		return
	var lines: Array[String] = []
	var discovered_count := 0
	var stabilized_count := 0
	# Working, unfinished experiments come first, with stable ID order for ties.
	var recipes := SynergyManagerScript.all_synergies().duplicate()
	recipes.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		var a_priority := _active_synergy_link_count(str(a["id"])) > 0 and not meta.stabilized_synergy_ids.has(a["id"])
		var b_priority := _active_synergy_link_count(str(b["id"])) > 0 and not meta.stabilized_synergy_ids.has(b["id"])
		return str(a["id"]) < str(b["id"]) if a_priority == b_priority else a_priority)
	for synergy in recipes:
		if meta.discovered_synergy_ids.has(synergy["id"]):
			discovered_count += 1
			if meta.stabilized_synergy_ids.has(synergy["id"]):
				stabilized_count += 1
			lines.append(_format_synergy_line(synergy) + "\n")
	lines.push_front("[color=#a9e7d4]%d LEARNED  /  %d STABILIZED  /  %d BLUEPRINTS AVAILABLE[/color]\n" % [discovered_count, stabilized_count, meta.unlocked_room_ids.size()])
	if discovered_count == 0:
		lines.append("[color=#a7bac1]An empty record, a station full of possibilities.\n\nConnect different rooms through matching doors. Let them function.\nWatch the rooms themselves for the first sign of a discovery.\n\nStabilized blueprints stay with you across reboots, and a new prototype\nis placed on top of your current draw pile.[/color]\n")
	var unknown_count := SynergyManagerScript.all_synergies().size() - discovered_count
	if unknown_count > 0:
		lines.append("[color=#718a97]UNKNOWN PATTERNS REMAIN: %d[/color]" % unknown_count)
	archive_label.text = _join_strings(lines, "\n")
	if journal_button != null:
		journal_button.text = "JOURNAL [J]\n%d LEARNED" % discovered_count

func _prettify_id(id: String) -> String:
	return id.replace("_", " ").capitalize()

func _refresh_routing() -> void:
	var lines := ["Power Routing", "Reserve %d/%d | Used %d/%d" % [resources["power"], _get_power_capacity(), power_used, power_generated]]
	for room in _rooms_by_power_priority():
		var need := int(room.get("consumption", {}).get("power", 0))
		if need <= 0:
			continue
		var state := "OFF" if unpowered_room_cells.has(room["pos"]) else "ON"
		lines.append("%s P%d: %s (%d)" % [state, _power_priority(room), room["display_name"], need])
	if lines.size() == 2:
		lines.append("No powered rooms beyond passive generation.")
	routing_label.text = _join_strings(lines, "\n")

func _refresh_placement_status() -> void:
	if selected_card_id.is_empty():
		placement_label.text = "■ %s     VIEW: %s\nMajor Bill: %s" % ["HALTED" if paused else "RUNNING", "ADMIN" if admin_mode else "NORMAL", _walker_status()]
		return
	var room := RoomDatabaseScript.get_room(selected_card_id)
	var problem := get_placement_problem(selected_card_id, hover_cell)
	var doors := _room_doors(selected_card_id, selected_rotation)
	if problem.is_empty():
		placement_label.text = "PLACING: %s\nDoors: %s     R rotates blueprint" % [room["display_name"], _join_strings(doors)]
	else:
		placement_label.text = "BLOCKED: %s\n%s" % [room["display_name"], problem]

func _refresh_log() -> void:
	var recent_lines := log_lines.slice(max(0, log_lines.size() - 24), log_lines.size())
	recent_lines.reverse()
	if recent_lines.is_empty():
		log_label.text = "[color=#%s]■ STATION LOG[/color]\n\n[color=#4f6470]No signals logged.[/color]" % UI_ACCENT_BRIGHT.to_html(false)
		return
	var formatted := ["[color=#%s]■ STATION LOG[/color]  [color=#4f6470]LATEST FIRST[/color]" % UI_ACCENT_BRIGHT.to_html(false), ""]
	for line in recent_lines:
		var text := str(line)
		if text.contains("Warning") or text.contains("collapse") or text.contains("critical") or text.contains("shortfall"):
			formatted.append("%s [color=#d95b63]%s[/color]" % [_resource_icon_bbcode("fire", 14), text])
		elif text.contains("Built") or text.contains("online") or text.contains("unlocked"):
			formatted.append("[color=#84b684]%s[/color]" % text)
		elif text.contains("Anomaly") or text.contains("corruption"):
			formatted.append("%s [color=#b982ff]%s[/color]" % [_resource_icon_bbcode("anomaly", 14), text])
		else:
			formatted.append("[color=#94a2a0]%s[/color]" % text)
	log_label.text = _join_strings(formatted, "\n")

func _format_cost(cost: Dictionary) -> String:
	if cost.is_empty():
		return "free"
	var parts := []
	for key in cost:
		parts.append("%s %d" % [key.capitalize(), cost[key]])
	return _join_strings(parts)

func _format_resource_list(values: Dictionary, icon_size: int = 16) -> String:
	if values.is_empty():
		return "None"
	var parts: Array[String] = []
	for key in values:
		var id := str(key)
		var resource_name := id.replace("_", " ").capitalize()
		parts.append("%s %s %d" % [_resource_icon_bbcode(id, icon_size), resource_name, int(values[key])])
	return _join_strings(parts)

func _missing_cost(cost: Dictionary) -> Dictionary:
	var missing := {}
	for key in cost:
		var available := int(resources.get(key, 0))
		var required := int(cost[key])
		if available < required:
			missing[key] = required - available
	return missing

func _format_storage(storage: Dictionary) -> String:
	if storage.is_empty():
		return "Storage: none"
	var parts := []
	for key in storage:
		var id := str(key)
		parts.append("%s %s cap +%d" % [_resource_icon_bbcode(id, 16), id.capitalize(), storage[key]])
	return _join_strings(parts)

func _walker_status() -> String:
	if not has_test_walker():
		return "not spawned"
	if test_walker_state == "idle":
		return "taking a break at %s" % str(test_walker_cell)
	if test_walker_next_cell == Vector2i(-1, -1):
		return "waiting for connected rooms"
	return "%s %s to %s" % [test_walker_state, str(test_walker_cell), str(test_walker_next_cell)]

func _join_strings(values: Array, separator := ", ") -> String:
	var text := ""
	for value in values:
		if not text.is_empty():
			text += separator
		text += str(value)
	return text

func _can_afford(cost: Dictionary) -> bool:
	for key in cost:
		if resources.get(key, 0) < cost[key]:
			return false
	return true

func _spend(cost: Dictionary) -> void:
	_apply_delta(cost, -1)

func _apply_delta(delta: Dictionary, multiplier := 1) -> void:
	for key in delta:
		var before: int = int(resources.get(key, 0))
		var change: int = int(delta[key]) * multiplier
		var after: int = before + change
		if change > 0 and BASE_STORAGE_CAPACITY.has(key):
			after = mini(after, _get_resource_capacity(str(key)))
		resources[key] = after
		if change > 0:
			run_earned[key] = run_earned.get(key, 0) + max(after - before, 0)

func _has_room(id: String) -> bool:
	for room in placed_rooms:
		if room["id"] == id:
			return true
	return false

func _log(message: String, show_in_panel := true) -> void:
	if show_in_panel:
		log_lines.append("[C%02d] %s" % [cycle, message])
		if log_lines.size() > 80:
			log_lines.pop_front()
	if is_node_ready():
		_refresh_log()

func _on_tick_timer_timeout() -> void:
	if running and not paused:
		_advance_cycle()

func get_visual_time_seconds() -> float:
	return visual_time_seconds
