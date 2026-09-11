extends Control

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const SynergyManagerScript := preload("res://scripts/synergy_manager.gd")
const DiscoveryManagerScript := preload("res://scripts/discovery_manager.gd")
const OrbitManagerScript := preload("res://scripts/orbit_manager.gd")
const MetaStateScript := preload("res://scripts/meta_state.gd")
const GridCanvasScript := preload("res://scripts/grid_canvas.gd")
const RunManagerScript := preload("res://scripts/run_manager.gd")
const RunSave := preload("res://scripts/run_save.gd")
var run_save_path := RunSave.PATH
var run_save_id := ""

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
const Preferences = preload("res://scripts/title_settings.gd")
const ROOM_ART_VARIANT_COUNTS := {
	"battery_array": 1,
	"corner": 3,
	"corridor": 3,
	"tee_corridor": 3,
	"crew_hab": 4,
	"crew_lounge": 1,
	"hydroponics_bay": 1,
	"life_support": 2,
	"maintenance_bay": 1,
	"mining_drone_bay": 1,
	"reactor": 1,
	"research_lab": 1,
	"salvage_drone_bay": 1,
	"shield_generator": 1,
	"solar_array": 1,
	"storage_bay": 1,
	"xeno_lab": 1
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
const WreckField := preload("res://scripts/wreck_field.gd")
var wrecks: Dictionary = {}
var drone_fleet = preload("res://scripts/drone_fleet.gd").new()
const CryoRecovery := preload("res://scripts/cryo_recovery.gd")
var recovered_crew: Array = []
const Architects := preload("res://scripts/architects.gd")
var architect_run: Dictionary = {}
var last_meta_warning := ""
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
var inspector_selection_key := ""
var selected_rotation := 0
var selected_room_cell := Vector2i(-1, -1)
var guide_box: VBoxContainer
var guide_label: Label
var discovery_review_button: Button
var inspector_focus_button: Button
var guide_replay := false
var toast_record_keys := {}
var current_toast_record := ""
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
var run_discovered_character_ids: Array[String] = []
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
var time_speeds := RunManagerScript.TIME_SPEEDS.duplicate()
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
const BillNPC = preload("res://scripts/bill_npc.gd")
var bill_npc = BillNPC.new()
const VeldNPC = preload("res://scripts/veld_npc.gd")
var veld_npc = VeldNPC.new()
const BranforthNPC = preload("res://scripts/branforth_npc.gd")
var branforth_npc = BranforthNPC.new()
const MarshNPC = preload("res://scripts/marsh_npc.gd")
var marsh_npc = MarshNPC.new()
const Companions = preload("res://scripts/companions.gd")
var companion_actors := {}
var companion_roster := {}

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
var placement_feedback: Label
var placement_label: Label
var controls_state_label: Label
var zoom_label: Label
var zoom_slider: HSlider
var pause_button: Button
var speed_buttons := []
var view_mode_button: Button
var solar_meter: ProgressBar
var solar_time_label: Label
var cycle_counter_label: Label
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
var pause_pages: Dictionary = {}
var pause_page := "main"
var pause_page_title: Label
var pause_page_opener: Control
var menu_panel: PanelContainer
var menu_status_label: Label
var menu_save_feedback: Label
var menu_resume_button: Button
var menu_center: CenterContainer
var menu_archive: Control
var menu_section_opener: Control
var menu_transition: Tween
var last_preview_room_id := ""
var last_previewing_card := false
var resource_labels := {}
var resource_chips := {}
var resource_icon_rects := {}

var tick_timer: Timer
var log_lines := []
var event_history: Array = []
var flood_alert_button: Button
var construction_button: Button
var operations_refresh := 0.0
var journal_tabs: TabBar
var history_search: LineEdit
var diagnostics_button: Button
var history_tools: HBoxContainer
var history_filter: OptionButton
var journal_scroll_positions := {}
var journal_searches := {}
var menu_workspace := {}
var journal_last_tab := 0
var journal_opener: Control
var inspected_resource := ""
var camera_pan_remainder := Vector2.ZERO
var camera_pan_velocity := Vector2.ZERO
var camera_zoom_target := -1.0
var camera_view_revision := 0
var camera_viewport_size := Vector2.ZERO
var camera_zoom_center := Vector2.ZERO
var card_textures := {}
var ui_textures := {}
var resource_icon_textures := {}
var startup_complete := false
var station_sound: Node
var room_texture_paths := preload("res://scripts/room_card_art.gd").PATHS

var crew_comms
var comms_button: Button
var hardware: Dictionary=preload("res://scripts/station_hardware.gd").DEFAULTS.duplicate()
var hardware_panel

func _ready() -> void:
	Preferences.initialize(get_window())
	preload("res://scripts/station_music.gd").ensure(self)
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_configure_window_scaling()
	rng.randomize()
	_apply_ui_font()
	_load_ui_textures()
	_load_resource_icon_textures()
	_load_card_textures()
	_build_ui()
	_start_reboot_cycle()
	get_tree().auto_accept_quit = false
	var fresh_comms_opening: bool=RunSave.pending.is_empty()
	if not RunSave.pending.is_empty():
		var checkpoint: Dictionary = RunSave.pending
		RunSave.pending = {}
		if not await RunSave.restore_staged(self, checkpoint):
			_log("Checkpoint unavailable. A new loop is staged.", false)
	startup_complete = true
	crew_comms=preload("res://scripts/crew_comms.gd").new()
	crew_comms.opening_enabled=fresh_comms_opening
	crew_comms.game=self
	crew_comms.archive_path=run_save_path+".comms.json"
	add_child(crew_comms)
	var sound := preload("res://scripts/station_audio.gd").new()
	sound.game = self
	station_sound = sound
	add_child(sound)

func play_station_sound(kind: String, cell := Vector2.INF) -> void:
	if is_instance_valid(station_sound): station_sound.play_event(kind,cell)

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
		preload("res://scripts/airlock_cycle.gd").advance(self,delta * time_speeds[time_speed_index])
		_update_test_walker(delta * time_speeds[time_speed_index])
		_update_wreck_clearance(delta * time_speeds[time_speed_index])
		CryoRecovery.advance(self, delta * time_speeds[time_speed_index])
		Architects.advance_core(self,delta * time_speeds[time_speed_index])
	_update_camera_pan(delta)
	_update_camera_zoom(delta)
	_refresh_solar_meter()
	if is_instance_valid(placement_feedback) and placement_feedback.visible:
		_position_placement_feedback()
	operations_refresh += delta
	if operations_refresh >= 0.5:
		operations_refresh = 0.0
		_refresh_construction_button()
		if is_instance_valid(guide_box) and guide_box.visible: _refresh_learning_ui()
		preload("res://scripts/flood_alerts.gd").refresh(self)
		if not meta.last_error.is_empty() and meta.last_error != last_meta_warning:
			_log("PROGRESSION NOT SAVED // " + meta.last_error,true)
		last_meta_warning = meta.last_error
		if wrecks.has(selected_room_cell) or drone_fleet.sites.has(selected_room_cell):
			_refresh_inspector()
		elif occupied.has(selected_room_cell) and occupied[selected_room_cell].id in ["mining_drone_bay","salvage_drone_bay"]:
			_refresh_inspector()
		elif drone_fleet.reserved(selected_room_cell): _refresh_inspector()
		elif occupied.has(selected_room_cell) and (inspector_had_water or float(occupied[selected_room_cell].get("water_level",0))>0 or float(occupied[selected_room_cell].get("hull_crack",0))>0): _refresh_inspector()

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
	top_shell.offset_bottom = 124
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

	var navigation_row := HBoxContainer.new()
	navigation_row.name = "NavigationRow"
	navigation_row.add_theme_constant_override("separation", 12)
	navigation_row.custom_minimum_size.x = 540
	navigation_row.alignment = BoxContainer.ALIGNMENT_CENTER
	top_bar.add_child(navigation_row)
	var journal := Button.new()
	journal.text = "JOURNAL [J]"
	journal.custom_minimum_size = Vector2(130, 44)
	journal.tooltip_text = "Your recovered patterns and their blueprint rewards. Reading pauses the station."
	journal.pressed.connect(_toggle_journal)
	_style_hud_button(journal, false)
	preload("res://scripts/navigation_badge.gd").apply_top(journal, "journal")
	navigation_row.add_child(journal)
	journal_button = journal

	var menu_button := Button.new()
	menu_button.text = "MENU"
	menu_button.custom_minimum_size = Vector2(82, 44)
	menu_button.pressed.connect(_toggle_menu)
	_style_hud_button(menu_button, false)
	preload("res://scripts/navigation_badge.gd").apply_top(menu_button, "menu")
	navigation_row.add_child(menu_button)

	var middle := Control.new()
	middle.name = "Center"
	middle.set_anchors_preset(Control.PRESET_FULL_RECT)
	middle.offset_top = 132
	middle.offset_right = -560
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
	scroll.resized.connect(_resize_grid_view)

	var grid := GridCanvasScript.new()
	grid.name = "GridView"
	grid.custom_minimum_size = Vector2(GRID_SIZE * get_cell_size(), GRID_SIZE * get_cell_size())
	grid.cell_clicked.connect(_on_grid_clicked)
	grid.cell_secondary_clicked.connect(_on_grid_secondary_clicked)
	grid.cell_hovered.connect(_on_grid_hovered)
	scroll.add_child(grid)
	grid_view = grid

	placement_feedback = Label.new()
	placement_feedback.name = "PlacementFeedback"
	placement_feedback.position = Vector2(24,64)
	placement_feedback.size = Vector2(440,0)
	placement_feedback.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	placement_feedback.mouse_filter = Control.MOUSE_FILTER_IGNORE
	placement_feedback.add_theme_font_size_override("font_size",17)
	var feedback_font := SystemFont.new()
	feedback_font.font_names = PackedStringArray(["Segoe UI","Arial","sans-serif"])
	placement_feedback.add_theme_font_override("font",feedback_font)
	var feedback_style := StyleBoxFlat.new()
	feedback_style.bg_color = Color(0.025,0.07,0.09,0.96)
	feedback_style.set_content_margin_all(12)
	placement_feedback.add_theme_stylebox_override("normal",feedback_style)
	placement_feedback.hide()
	middle.add_child(placement_feedback)

	var objective_panel := PanelContainer.new()
	objective_panel.name = "OrbitalObjective"
	objective_panel.visible = false
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
	var objective_box := VBoxContainer.new()
	objective_panel.add_child(objective_box)
	objective_box.add_child(objective_text)
	construction_button = Button.new()
	construction_button.text = "CONSTRUCTION / 0"
	_style_hud_button(construction_button, false)
	construction_button.pressed.connect(func() -> void:
		if _gameplay_input_blocked(): return
		_toggle_journal()
		journal_tabs.current_tab = 6
		_refresh_archive())
	objective_box.add_child(construction_button)
	flood_alert_button=Button.new()
	flood_alert_button.text="FLOOD / CLEAR"
	_style_hud_button(flood_alert_button,false)
	flood_alert_button.pressed.connect(func():
		var cell: Vector2i=flood_alert_button.get_meta("target",Vector2i(-1,-1))
		if occupied.has(cell):
			selected_card_id=""
			selected_room_cell=cell
			_restore_grid_view_center((Vector2(cell)+Vector2.ONE*0.5)/40.0)
			_refresh_all())
	objective_box.add_child(flood_alert_button)
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
	cascade_panel.gui_input.connect(func(event: InputEvent) -> void:
		if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT and not current_toast_record.is_empty():
			cascade_panel.accept_event()
			_review_discovery_key(current_toast_record)
	)

	var viewport_tools := HBoxContainer.new()
	viewport_tools.name = "ViewportTools"
	viewport_tools.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	viewport_tools.offset_left = -450
	viewport_tools.offset_top = 18
	viewport_tools.offset_right = -18
	viewport_tools.offset_bottom = 58
	viewport_tools.add_theme_constant_override("separation", 10)
	middle.add_child(viewport_tools)
	var find_button := Button.new()
	find_button.name = "FindRoomButton"
	find_button.text = "FIND ROOM"
	find_button.tooltip_text = "Search installed rooms by name, type or problem · Ctrl+F"
	find_button.pressed.connect(_open_station_search)
	_style_hud_button(find_button,false)
	viewport_tools.add_child(find_button)
	var recenter_button := Button.new()
	recenter_button.text = "FIT STATION [F]"
	recenter_button.set_meta("key_hint", "FIT STATION [{Fit station}]")
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
	side_scroll.offset_left = -548
	side_scroll.offset_top = 132
	side_scroll.offset_right = -8
	side_scroll.offset_bottom = -8
	side_scroll.custom_minimum_size = Vector2(540, 0)
	side_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_SHOW_NEVER
	side_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	side_scroll.follow_focus = true
	side_scroll.mouse_force_pass_scroll_events = false
	root.add_child(side_scroll)

	var side := VBoxContainer.new()
	guide_box = VBoxContainer.new()
	guide_box.hide()
	guide_label = Label.new()
	guide_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	guide_label.add_theme_font_size_override("font_size", 15)
	guide_label.add_theme_color_override("font_color", Color("b9dce5"))
	guide_box.add_child(guide_label)
	var skip_guide := Button.new()
	skip_guide.text = "SKIP GUIDE"
	skip_guide.custom_minimum_size.y = 40
	skip_guide.pressed.connect(_finish_guide)
	preload("res://scripts/title_button_style.gd").apply(skip_guide, 380, 40)
	guide_box.add_child(skip_guide)
	side.add_child(guide_box)
	discovery_review_button = Button.new()
	discovery_review_button.custom_minimum_size.y = 48
	discovery_review_button.add_theme_font_size_override("font_size", 15)
	discovery_review_button.pressed.connect(_review_latest_discovery)
	_style_hud_button(discovery_review_button, false)
	preload("res://scripts/navigation_badge.gd").apply_top(discovery_review_button, "archive")
	navigation_row.add_child(discovery_review_button)
	navigation_row.move_child(discovery_review_button, 0)
	side.name = "SidePanel"
	side.custom_minimum_size = Vector2(518, 0)
	side.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	side.add_theme_constant_override("separation", 10)
	side_scroll.add_child(side)
	diagnostics_button = Button.new()
	diagnostics_button.text = "STATION DIAGNOSTICS"
	diagnostics_button.pressed.connect(func():
		_toggle_journal()
		journal_tabs.current_tab = 1
		_refresh_archive())
	_style_hud_button(diagnostics_button, false)
	preload("res://scripts/navigation_badge.gd").apply_top(diagnostics_button, "diagnostics")
	navigation_row.add_child(diagnostics_button)
	navigation_row.move_child(diagnostics_button, 1)
	comms_button=Button.new(); comms_button.text="COMMS"
	comms_button.pressed.connect(func():
		if is_instance_valid(crew_comms): crew_comms.reopen())
	preload("res://scripts/title_button_style.gd").apply(comms_button,380,40)
	# Retained button reference for comms compatibility; hardware owns visible access.
	side.add_child(comms_button); comms_button.hide()
	hardware_panel=preload("res://scripts/hardware_panel.gd").new(); hardware_panel.game=self
	construction_button.reparent(side)
	construction_button.hide()
	flood_alert_button.reparent(side)
	flood_alert_button.hide()

	var inspector_panel := PanelContainer.new()
	inspector_panel.name = "PreviewPanel"
	inspector_panel.custom_minimum_size = Vector2(0, 520)
	side.add_child(inspector_panel)
	_apply_panel_style(inspector_panel, Color("#071018"), Color("#152a35"))
	var inspector_style: StyleBox = inspector_panel.get_theme_stylebox("panel").duplicate()
	inspector_style.set_content_margin_all(14)
	inspector_panel.add_theme_stylebox_override("panel", inspector_style)
	var reading_font := SystemFont.new()
	reading_font.font_names = PackedStringArray(["Segoe UI", "Arial", "sans-serif"])
	var reading_theme := Theme.new()
	reading_theme.default_font = reading_font
	inspector_panel.theme = reading_theme
	var preview_box := VBoxContainer.new()
	preview_box.add_theme_constant_override("separation", 8)
	inspector_panel.add_child(preview_box)
	var preview_header := HBoxContainer.new()
	preview_box.add_child(preview_header)
	var preview_header_left := Label.new()
	preview_header_left.text = "■ INSPECTOR"
	preview_header_left.add_theme_font_size_override("font_size", 16)
	preview_header_left.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	preview_header.add_child(preview_header_left)
	var preview_header_right := Label.new()
	preview_header_right.text = "CLICK TO SELECT"
	preview_header_right.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	preview_header_right.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	preview_header_right.add_theme_font_size_override("font_size", 12)
	preview_header_right.add_theme_color_override("font_color", Color("#8fa3ae"))
	preview_header.add_child(preview_header_right)
	var preview_details := HBoxContainer.new()
	preview_details.add_theme_constant_override("separation", 14)
	preview_box.add_child(preview_details)
	var preview_image := TextureRect.new()
	preview_image.custom_minimum_size = Vector2(72, 72)
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
	inspector_text.custom_minimum_size = Vector2(0, 330)
	inspector_text.size_flags_vertical = Control.SIZE_EXPAND_FILL
	inspector_text.mouse_filter = Control.MOUSE_FILTER_STOP
	inspector_text.mouse_force_pass_scroll_events = false
	inspector_text.add_theme_color_override("default_color", Color("#c8d6dc"))
	inspector_text.add_theme_font_size_override("normal_font_size", 18)
	inspector_text.add_theme_font_size_override("bold_font_size", 18)
	inspector_text.add_theme_constant_override("line_separation", 2)
	preview_box.add_child(inspector_text)
	inspector_focus_button = Button.new()
	inspector_focus_button.text = "LOCATE ROOM & CONNECTIONS"
	inspector_focus_button.custom_minimum_size.y = 42
	inspector_focus_button.add_theme_font_size_override("font_size", 14)
	inspector_focus_button.pressed.connect(_focus_inspected_room)
	preload("res://scripts/title_button_style.gd").apply(inspector_focus_button, 380, 42)
	preview_box.add_child(inspector_focus_button)
	# Retain the internal selection anchor for focus links without a visible action.
	inspector_focus_button.hide()
	inspector_text.meta_clicked.connect(_inspector_action)
	inspector_label = inspector_text
	side.sort_children.connect(_fit_sidebar_inspector.bind(side_scroll, side, inspector_panel))
	side_scroll.resized.connect(side.queue_sort)
	room_operation_button = preload("res://scripts/industrial_room_switch.gd").new()
	room_operation_button.text = "SELECT A BUILT ROOM TO CONTROL"
	room_operation_button.custom_minimum_size.y = 34
	room_operation_button.pressed.connect(_toggle_inspected_room)
	_style_hud_button(room_operation_button, false)
	preview_box.add_child(room_operation_button)
	var airlock_panel=preload("res://scripts/airlock_panel.gd").new()
	airlock_panel.game=self
	preview_box.add_child(airlock_panel)

	side.add_child(hardware_panel)

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
	controls_panel.custom_minimum_size = Vector2(0, 0)
	side.add_child(controls_panel)
	_apply_panel_style(controls_panel, Color("#071018"), Color("#152a35"))
	var compact_style: StyleBox = controls_panel.get_theme_stylebox("panel").duplicate()
	compact_style.set_content_margin_all(12)
	controls_panel.add_theme_stylebox_override("panel", compact_style)
	var controls_box := VBoxContainer.new()
	controls_box.name = "ControlsBox"
	controls_box.add_theme_constant_override("separation", 4)
	controls_panel.add_child(controls_box)
	var controls_header := HBoxContainer.new()
	controls_box.add_child(controls_header)
	var controls_title := Label.new()
	controls_title.text = "TIME / CYCLE"
	controls_title.add_theme_font_size_override("font_size", 16)
	controls_title.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	controls_header.add_child(controls_title)
	var controls_state := Label.new()
	controls_state.text = "RUNNING"
	controls_state.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	controls_state.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	controls_state.add_theme_font_size_override("font_size", 11)
	controls_state.add_theme_color_override("font_color", Color("#8fa3ae"))
	controls_header.add_child(controls_state)
	controls_state_label = controls_state
	var controls := HBoxContainer.new()
	controls.name = "Controls"
	controls.add_theme_constant_override("separation", 8)
	controls_box.add_child(controls)
	var pause_label := Label.new()
	pause_label.text = "TIME"
	pause_label.custom_minimum_size = Vector2(66, 0)
	pause_label.add_theme_color_override("font_color", Color("#8fa3ae"))
	controls.add_child(pause_label)
	pause_label.hide()
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
	controls.add_child(speed_row)
	var speed_label := Label.new()
	speed_label.text = "SPEED"
	speed_label.tooltip_text = "Controls cycle timer speed and station animation speed."
	speed_label.custom_minimum_size = Vector2(66, 0)
	speed_label.add_theme_color_override("font_color", Color("#8fa3ae"))
	speed_row.add_child(speed_label)
	speed_label.hide()
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
	zoom_title.add_theme_color_override("font_color", Color("#8fa3ae"))
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
	solar_title.text = "CYCLE %03d" % cycle
	cycle_counter_label = solar_title
	solar_title.tooltip_text = "Time remaining until the next automatic cycle."
	solar_title.custom_minimum_size = Vector2(66, 0)
	solar_title.add_theme_color_override("font_color", Color("#8fa3ae"))
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
	placement_status.visible = false
	var detail_toggle := Button.new()
	detail_toggle.text = "View options"
	detail_toggle.tooltip_text = "Zoom and placement details"
	detail_toggle.tooltip_text = "Expand view details. Use the Placement guides hotkey to toggle indicators; physical doorway openings remain visible. Rebind it in Settings."
	detail_toggle.toggle_mode = true
	_style_hud_button(detail_toggle, false)
	solar_row.add_child(detail_toggle)
	zoom_row.visible = false
	detail_toggle.toggled.connect(func(expanded: bool) -> void:
		zoom_row.visible = expanded
		placement_status.visible = expanded)
	placement_label = placement_status

	var log_panel := PanelContainer.new()
	log_panel.name = "NotificationsPanel"
	log_panel.visible = false # Full event history is available in the Journal.
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
	bottom.offset_right = -560
	bottom.offset_top = -380
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
	blueprint_title.add_theme_color_override("font_color", Color("#8fa3ae"))
	draft_status.add_child(blueprint_title)
	var hand_count := Label.new()
	hand_count.text = "%d/%d" % [HAND_SIZE, HAND_SIZE]
	hand_count.add_theme_font_size_override("font_size", 30)
	hand_count.add_theme_color_override("font_color", Color("#c4d1da"))
	draft_status.add_child(hand_count)
	hand_count_label = hand_count
	var draft_hint := Label.new()
	draft_hint.text = "Build to draw.\nRMB rerolls one.\nR rotates.\nSpace pauses."
	draft_hint.set_meta("key_hint", "Build to draw.\nRMB rerolls one.\n{Rotate blueprint} rotates.\n{Pause} pauses.")
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
	summary_center.theme = preload("res://scripts/title_button_style.gd").menu_theme()
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
	summary_vbox.add_theme_constant_override("separation", 12)
	summary.add_child(summary_vbox)
	var summary_title := Label.new()
	summary_title.text = "Reboot Summary"
	summary_title.add_theme_font_size_override("font_size", 24)
	summary_vbox.add_child(summary_title)
	summary_title_label = summary_title
	var summary_scroll := ScrollContainer.new()
	summary_scroll.focus_mode = Control.FOCUS_ALL
	summary_scroll.follow_focus = true
	summary_scroll.custom_minimum_size = Vector2(740, 480)
	summary_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	summary_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	summary_vbox.add_child(summary_scroll)
	var summary_body := Label.new()
	summary_body.name = "Text"
	summary_body.add_theme_font_size_override("font_size", 17)
	summary_body.add_theme_color_override("font_color", Color("bdd5df"))
	summary_body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	summary_body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	summary_scroll.add_child(summary_body)
	summary_text = summary_body
	continue_expedition_button = Button.new()
	continue_expedition_button.text = "CONTINUE EXPEDITION · KEEP EXPERIMENTING"
	continue_expedition_button.custom_minimum_size.y = 44
	continue_expedition_button.pressed.connect(_continue_expedition)
	preload("res://scripts/title_button_style.gd").apply(continue_expedition_button, 740, 52, true)
	summary_vbox.add_child(continue_expedition_button)
	var reboot_button := Button.new()
	reboot_button.text = "Start New Reboot Cycle"
	reboot_button.custom_minimum_size.y = 40
	preload("res://scripts/title_button_style.gd").apply(reboot_button, 740, 52)
	reboot_button.pressed.connect(_choose_restart_architect)
	summary_vbox.add_child(reboot_button)
	_add_menu_button(summary_vbox, "Settings", _open_overlay_settings)
	_add_menu_button(summary_vbox, "Review Discoveries", _review_latest_discovery)
	summary_layer.set_meta("default_button", reboot_button)
	_add_menu_button(summary_vbox, "Return to Title", _menu_return_title)

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
	button.add_theme_color_override("font_color", Color("#b0e3cf") if active else Color("#abc5ca"))
	button.add_theme_color_override("font_hover_color", Color("#d1f2eb"))
	button.add_theme_color_override("font_pressed_color", Color("#d7f5d2"))
	button.add_theme_font_size_override("font_size", 14)

	button.add_theme_stylebox_override("focus", preload("res://scripts/title_button_style.gd").panel(100, 40, "focus"))
	button.add_theme_color_override("font_disabled_color", Color("#637f89"))

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
	center.theme = preload("res://scripts/title_button_style.gd").menu_theme()
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
	title.text = "BRINE / STATION JOURNAL"
	title.add_theme_font_size_override("font_size", 26)
	title.add_theme_color_override("font_color", Color("#a9e7d4"))
	body.add_child(title)
	var subtitle := Label.new()
	subtitle.text = "Recovered patterns, system diagnostics and the loop's recorded failures.\nThe station remembers. Occasionally, that is useful."
	subtitle.add_theme_color_override("font_color", Color("#92aeb8"))
	body.add_child(subtitle)
	journal_tabs = TabBar.new()
	for tab_title in ["Patterns", "Station Health", "Reserves", "Event History", "Rooms", "Crew", "Construction"]:
		journal_tabs.add_tab(tab_title)
	journal_tabs.tab_changed.connect(_journal_tab_changed)
	body.add_child(journal_tabs)
	history_tools = HBoxContainer.new()
	history_tools.add_theme_constant_override("separation", 12)
	body.add_child(history_tools)
	history_search = LineEdit.new()
	history_search.placeholder_text = "Search room, cycle (C03), or message · Ctrl+F"
	history_search.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	history_search.custom_minimum_size.y = 40
	history_search.clear_button_enabled = true
	history_search.max_length = 128
	history_search.text_submitted.connect(func(_query):
		if journal_tabs.current_tab!=4: return
		var matches: Array = preload("res://scripts/station_navigation.gd").rooms(self,history_search.text,_simulate_room_economy(true,cycle+1))
		if not matches.is_empty(): _locate_diagnostic_room("%d,%d" % [matches[0].pos.x,matches[0].pos.y]))
	history_search.text_changed.connect(func(_query):
		journal_searches[journal_tabs.current_tab] = _query
		_refresh_archive()
		archive_label.get_v_scroll_bar().set_deferred("value", 0.0))
	history_search.visible = false
	history_tools.add_child(history_search)
	history_filter = OptionButton.new()
	for category in ["All events", "Problems", "Discoveries", "Construction"]:
		history_filter.add_item(category)
	history_filter.item_selected.connect(func(_index):
		_refresh_archive()
		archive_label.get_v_scroll_bar().set_deferred("value", 0.0))
	history_tools.add_child(history_filter)
	history_tools.visible = false
	archive_label = RichTextLabel.new()
	archive_label.bbcode_enabled = true
	archive_label.focus_mode = Control.FOCUS_ALL
	archive_label.custom_minimum_size = Vector2(900, 460)
	archive_label.meta_clicked.connect(_locate_diagnostic_room)
	archive_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
	archive_label.add_theme_font_size_override("normal_font_size", 16)
	archive_label.add_theme_constant_override("line_separation", 6)
	body.add_child(archive_label)
	var close := Button.new()
	close.text = "RETURN TO STATION  [J / ESC]"
	close.set_meta("key_hint", "RETURN TO STATION  [{Journal} / ESC]")
	close.custom_minimum_size.y = 44
	close.pressed.connect(_toggle_journal)
	_style_hud_button(close, false)
	body.add_child(close)
	journal_layer.set_meta("close_button", close)
	preload("res://scripts/title_button_style.gd").apply(close, 900, 52)
	_add_menu_button(body, "Settings", _open_overlay_settings)

func _journal_is_open() -> bool:
	return journal_layer != null and journal_layer.visible

func _gameplay_input_blocked() -> bool:
	return is_instance_valid(menu_archive) or menu_open or _journal_is_open() or (summary_layer != null and summary_layer.visible) or (doctrine_layer != null and doctrine_layer.visible)

func _toggle_journal() -> void:
	if journal_layer == null:
		return
	if _journal_is_open():
		journal_layer.visible = false
		if is_instance_valid(journal_opener) and journal_opener.is_visible_in_tree():
			journal_opener.grab_focus()
		else:
			journal_button.grab_focus()
		_set_paused(pause_before_journal)
		return
	if _gameplay_input_blocked():
		return
	pause_before_journal = paused
	journal_opener = get_viewport().gui_get_focus_owner()
	journal_layer.visible = true
	preload("res://scripts/title_settings.gd").apply_menu_text(journal_layer)
	get_viewport().gui_release_focus()
	var close_button: Button = journal_layer.get_meta("close_button")
	close_button.grab_focus()
	_set_paused(true)
	_refresh_archive()

func _toggle_inspected_room() -> void:
	if _gameplay_input_blocked() or not running or room_operation_button == null:
		return
	var cell: Vector2i = room_operation_button.get_meta("cell", Vector2i(-1, -1))
	if Companions.is_site(self,cell) and not wrecks[cell].recovered:
		Companions.toggle(self,cell)
		return
	if drone_fleet.sites.has(cell) and not occupied.has(cell):
		drone_fleet.sites[cell].active = not drone_fleet.sites[cell].active
		_refresh_all()
		return
	if WreckField.blocks(wrecks,cell):
		_toggle_wreck_work(cell)
		return
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

func _toggle_wreck_work(cell: Vector2i) -> void:
	if Companions.is_site(self,cell):
		Companions.toggle(self,cell);return
	if not running or not WreckField.blocks(wrecks,cell):
		return
	var wreck: Dictionary = wrecks[cell]
	if not wreck.active and wreck.kind not in ["cryo","charging"] and not drone_fleet.has_worker("mining" if wreck.kind=="basalt" else "salvage",placed_rooms):
		_log("A %s Drone Bay is required for this job." % ("Mining" if wreck.kind=="basalt" else "Salvage"),false)
		return
	if wreck.kind in ["cryo","charging"] and not wreck.active:
		if not CryoRecovery.accessible(self,cell) or WreckField.busy(wrecks,cell): return
		if not wreck.paid:
			if resources.get("metal",0)<CryoRecovery.REPAIR_METAL: return
			resources.metal -= CryoRecovery.REPAIR_METAL
			wreck.paid = true
	if wreck.active:
		wreck.active = false
	elif WreckField.reachable(occupied,cell) and not WreckField.busy(wrecks,cell):
		wreck.active = true
	else:
		return
	_log("%s: %s." % [WreckField.NAMES[wreck.kind],("repair scheduled" if wreck.kind in ["cryo","charging"] else "clearance scheduled") if wreck.active else "work halted; progress retained"],false)
	_refresh_all()

func _update_wreck_clearance(delta: float) -> void:
	if not hardware.power or hardware.doors: return
	if not running or paused:
		return
	var working: Dictionary = _simulate_room_economy().working_cells
	var built: Array = drone_fleet.advance(delta,placed_rooms,working,wrecks,int(resources.get("power",0)),true)
	if drone_fleet.power_spent > 0:
		_apply_delta({"power":-drone_fleet.power_spent})
		_refresh_all()
	if not drone_fleet.delivered.is_empty():
		_apply_delta(drone_fleet.delivered)
		play_station_sound("cargo")
		_refresh_all()
	for order in built:
		var prior_rotation := selected_rotation
		selected_rotation = order.rotation
		_place_room(order.id,order.pos,false,true)
		selected_rotation = prior_rotation
	if not built.is_empty(): _refresh_all()
	var completed := WreckField.advance(wrecks,occupied,delta,drone_fleet.clearance_seconds)
	for cell in completed:
		if Companions.is_site(self,cell):
			Companions.connect_room(self,cell);continue
		if wrecks[cell].kind in ["cryo","charging"]:
			# The paid restoration preserves the discovered room, its orientation and occupants.
			_place_room("cryo_chamber",cell,true)
			occupied[cell].rotation = wrecks[cell].rotation
			occupied[cell]["recovered_derelict"] = true
			occupied[cell].display_name = "Charging Chamber" if wrecks[cell].kind=="charging" else "Recovered Cryo Ward"
			_check_synergies()
			_check_directive_progress()
			_log("Charging chamber connected. Restore power. The machine still has someone to finish." if wrecks[cell].kind=="charging" else "Cryo ward pressure restored. Compartment joined. Its occupants await power and a free berth.",false)
			continue
		if wrecks[cell].kind == "basalt":
			_log("Rock cleared at %s. Construction footprint secured." % cell,false)
			continue
		var amount: int = WreckField.YIELDS[wrecks[cell].kind]
		_log("Wreck cleared at %s. %d metal recovered; storage receives cargo on docking." % [cell,amount],false)
	if not completed.is_empty():
		_refresh_all()

func _refresh_wreck_inspector(cell: Vector2i) -> void:
	if Companions.is_site(self,cell):
		Companions.inspect(self,cell);return
	var wreck: Dictionary = wrecks[cell]
	if wreck.kind in ["cryo","charging"]:
		_refresh_cryo_inspector(cell)
		return
	if wreck.kind == "basalt":
		_refresh_rock_inspector(cell)
		return
	var fraction := float(wreck.progress)/WreckField.DURATION
	var accessible := WreckField.reachable(occupied,cell)
	var busy := WreckField.busy(wrecks,cell)
	preview_name_label.text = WreckField.NAMES[wreck.kind]
	preview_name_label.add_theme_color_override("font_color",Color("c39861"))
	preview_tags_label.text = "WRECK / 1 CELL / BLOCKS CONSTRUCTION"
	preview_texture.texture = grid_view.wreck_view.texture(wreck.kind,"wreck")
	var state: String = drone_fleet.clearance_status(cell,_simulate_room_economy().working_cells) if wreck.active and not paused else "PAUSED" if wreck.progress>0 or wreck.active else "AWAITING DISMANTLING"
	var has_bay: bool = drone_fleet.has_worker("salvage",placed_rooms)
	var note := "A Salvage Drone Bay dispatches the cutter. Work begins after arrival."
	if not has_bay:
		note = "Requires a Salvage Drone Bay."
	elif not accessible:
		note = "Extend the station to a neighboring cell to reach this wreck."
	elif busy:
		note = "The salvage rig is assigned elsewhere. Pause that job first."
	inspector_label.text = "%s\n\nProgress: %d%% / %.0f seconds remaining\nMetal salvage: %d (delivered on docking; storage capacity applies)\n\n%s\n\nNo recoverable occupants. This compartment can only be dismantled. Construction becomes available after the last frame is cleared; normal room costs still apply.\n\n[color=#698782]It held pressure once. I would not ask it twice.[/color]" % [state,roundi(fraction*100),WreckField.DURATION-float(wreck.progress),WreckField.YIELDS[wreck.kind],note]
	room_operation_button.set_meta("cell",cell)
	room_operation_button.disabled = not running or (not wreck.active and (not accessible or busy or not has_bay))
	room_operation_button.text = "PAUSE SALVAGE" if wreck.active else "RESUME SALVAGE" if wreck.progress>0 else "DISMANTLE & SALVAGE"
	room_operation_button.tooltip_text = "Progress freezes with the game. Metal is awarded once, on completion."

func _refresh_cryo_inspector(cell: Vector2i) -> void:
	var ward: Dictionary = wrecks[cell]
	var charging: bool = ward.kind=="charging"
	preview_name_label.text = ("Charging Chamber" if ward.cleared else "Derelict Charging Chamber") if charging else ("Recovered Cryo Ward" if ward.cleared else "Derelict Cryo Ward")
	preview_tags_label.text = "ANDROID // WHITE-FLUID CHARGING POD" if charging else "MEDICAL // %d OCCUPIED POD(S) AT DISCOVERY" % ward.pods.size()
	preview_texture.texture = preload("res://scripts/marsh_charging_art.gd").texture(Architects.pod_for_display(self,ward.pods[0]).recovered) if charging else preload("res://scripts/architect_cryo_art.gd").frame(ward.pods[0].get("architect_id","bill"),0)
	inspector_focus_button.set_meta("cell",cell)
	inspector_focus_button.disabled = false
	var lines: Array[String] = [CryoRecovery.status(self,cell)]
	if not ward.cleared:
		lines.append("Repair hull and reconnect utilities: %d Metal, %.0f seconds. Payment is retained through pauses." % [CryoRecovery.REPAIR_METAL,WreckField.DURATION])
		lines.append("Repair: %d%%. Connect a matching door to reach this ward. One shared exterior rig." % roundi(ward.progress/WreckField.DURATION*100))
	else:
		lines.append("Restore power to start the pump. White fluid flows through the tubes into Marsh for %.0f seconds, then he wakes. A free berth is needed to join the crew. Power loss or suspension retains charge." % CryoRecovery.CHARGE_SECONDS if charging else "Station compartment online when powered. Each thaw takes %.0f seconds and requires food, oxygen and a free berth. Suspension retains progress." % CryoRecovery.WAKE_SECONDS)
	for pod in ward.pods:
		lines.append("%s // %s" % [pod.name,"ADDED TO ROSTER" if pod.recovered else ("CHARGE %d%%" if charging else "STASIS / thaw %d%%") % roundi(pod.wake/CryoRecovery.duration(ward)*100)])
	if charging and ward.pods[0].recovered and not marsh_npc.dead:
		lines.append(marsh_npc.battery_status()+"\nNo helmet or breathing requirement. Returns at 35% battery. Recharging draws 1 Power per 25% restored; a full battery lasts about five minutes.")
	lines.append("\nCREW ROSTER // RECOVERED SURVIVORS")
	if recovered_crew.is_empty(): lines.append("No recovered crew recorded.")
	for member in recovered_crew: lines.append("%s // %s" % [member.name,"ABOARD" if member.alive else "DECEASED"])
	lines.append("\n[color=#698782]Their clocks stopped. Mine did not.[/color]")
	inspector_label.text = "\n\n".join(lines)
	room_operation_button.set_meta("cell",cell)
	if ward.cleared:
		room_operation_button.text = "RESUME ROOM" if occupied[cell].get("suspended",false) else "SUSPEND ROOM"
		room_operation_button.disabled = not running
	else:
		room_operation_button.text = "PAUSE REPAIR" if ward.active else "RESUME REPAIR" if ward.paid else "REPAIR & CONNECT // 8 METAL"
		room_operation_button.disabled = not running or (not ward.active and (not CryoRecovery.accessible(self,cell) or WreckField.busy(wrecks,cell) or (not ward.paid and resources.get("metal",0)<CryoRecovery.REPAIR_METAL)))
	room_operation_button.tooltip_text = "Repair preserves this compartment and its occupants. Wake progress freezes with pause, suspension, power loss or full berths."

func _refresh_rock_inspector(cell: Vector2i) -> void:
	var rock: Dictionary = wrecks[cell]
	var accessible := WreckField.reachable(occupied,cell)
	var busy := WreckField.busy(wrecks,cell)
	preview_name_label.text = "Basalt Outcrop"
	preview_name_label.add_theme_color_override("font_color",Color("a7b5ab"))
	preview_tags_label.text = "ROCK / 1 CELL / BLOCKS CONSTRUCTION"
	preview_texture.texture = grid_view.rock_view.texture()
	var state: String = drone_fleet.clearance_status(cell,_simulate_room_economy().working_cells) if rock.active and not paused else "PAUSED" if rock.progress>0 or rock.active else "AWAITING EXCAVATION"
	var has_bay: bool = drone_fleet.has_worker("mining",placed_rooms)
	var note := "A Mining Drone Bay dispatches the drill. Work begins after arrival."
	if not has_bay:
		note = "Requires a Mining Drone Bay."
	elif not accessible:
		note = "Extend the station to a neighboring cell to reach this rock."
	elif busy:
		note = "The salvage rig is assigned elsewhere. Pause that job first."
	inspector_label.text = "%s\n\nProgress: %d%% / %.0f seconds remaining\n\n%s\n\nBreak and remove this section before building here. Neighboring rock remains in place. Excavation recovers 4 Metal, delivered on docking. The drill returns to recharge from station Power; cuts remain between trips. Normal room costs apply after clearance.\n\n[color=#698782]The ocean placed this here. It neglected to file a permit.[/color]" % [state,roundi(float(rock.progress)/WreckField.DURATION*100),WreckField.DURATION-float(rock.progress),note]
	room_operation_button.set_meta("cell",cell)
	room_operation_button.disabled = not running or (not rock.active and (not accessible or busy or not has_bay))
	room_operation_button.text = "PAUSE EXCAVATION" if rock.active else "RESUME EXCAVATION" if rock.progress>0 else "BREAK & CLEAR ROCK"
	room_operation_button.tooltip_text = "A Mining Drone clears this cell. Progress freezes with the game."

func _build_doctrine_overlay() -> void:
	# Empty compatibility layer for older scene consumers; selection is retired.
	doctrine_layer = CanvasLayer.new()
	doctrine_layer.visible = false
	add_child(doctrine_layer)

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
		button.text = "%s\n%s\nRANK %d · MASTERY %s\nPER RANK  %s" % [
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
		button.add_theme_font_size_override("font_size", 15)
	doctrine_selection_label.text = "%d/2 SELECTED%s" % [
		pending_doctrines.size(),
		"  ·  %s" % RunManagerScript.doctrine_pair_name(pending_doctrines) if not pending_doctrines.is_empty() else ""
	]
	if doctrine_pair_preview_label != null:
		doctrine_pair_preview_label.text = _doctrine_pair_preview_text()
	doctrine_confirm_button.disabled = pending_doctrines.size() != 2
	doctrine_confirm_button.text = "BEGIN REBOOT" if pending_doctrines.size() == 2 else "SELECT %d MORE DOCTRINE%s" % [2 - pending_doctrines.size(), "S" if pending_doctrines.is_empty() else ""]
	if pending_doctrines.size() == 2:
		doctrine_selection_label.text += "  ·  Select either doctrine again to change the pair."
	preload("res://scripts/title_settings.gd").apply_menu_text(doctrine_layer)

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
	# Compatibility entry point: new loops no longer choose doctrines.
	_confirm_doctrines()

func _confirm_doctrines() -> void:
	selected_doctrines.clear()
	pending_doctrines.clear()
	run_directives.clear()
	directive_index = 0
	doctrine_layer.hide()
	expedition_mode = true
	_build_run_deck()
	_draw_hand()
	running = true
	_set_paused(false, false)
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
	center.theme = preload("res://scripts/title_button_style.gd").menu_theme()
	center.set_anchors_preset(Control.PRESET_FULL_RECT)
	center.mouse_filter = Control.MOUSE_FILTER_STOP
	menu_layer.add_child(center)
	menu_center = center
	var panel := PanelContainer.new()
	panel.name = "PauseMenu"
	panel.custom_minimum_size = Vector2(620, 580)
	panel.mouse_filter = Control.MOUSE_FILTER_STOP
	center.add_child(panel)
	_apply_panel_style(panel, Color("#10232e"), Color("#3c6b7d"))
	menu_panel = panel
	var menu_scroll := ScrollContainer.new()
	menu_scroll.custom_minimum_size = Vector2(570, 540)
	menu_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	menu_scroll.follow_focus = true
	panel.add_child(menu_scroll)
	var box := VBoxContainer.new()
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	box.add_theme_constant_override("separation", 10)
	menu_scroll.add_child(box)
	var title := Label.new()
	title.text = "BRINE"
	title.add_theme_font_size_override("font_size", 34)
	title.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	box.add_child(title)
	var subtitle := Label.new()
	subtitle.text = "PAUSED"
	pause_page_title = subtitle
	subtitle.add_theme_font_size_override("font_size", 15)
	subtitle.add_theme_color_override("font_color", Color("#8daab6"))
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
	for id in ["main", "station", "exit"]:
		var page := VBoxContainer.new()
		page.name = "PausePage_" + id
		page.add_theme_constant_override("separation", 12)
		page.visible = id == "main"
		box.add_child(page)
		pause_pages[id] = page
	var primary: VBoxContainer = pause_pages.main
	_add_menu_button(primary, "Resume Cycle", _close_menu)
	_add_menu_button(primary, "Save Game", _menu_save_game)
	_add_menu_button(primary, "Settings", _open_shared_menu.bind("settings"))
	_add_menu_button(primary, "Station & Archives", _show_pause_page.bind("station"))
	_add_menu_button(primary, "End or Leave Loop", _show_pause_page.bind("exit"))
	var station: VBoxContainer = pause_pages.station
	_add_menu_button(station,"Crew Comms",func(): _close_menu(); crew_comms.reopen())
	_add_menu_button(station, "Codex", _open_shared_menu.bind("codex"))
	_add_menu_button(station, "Meta Progression", _open_shared_menu.bind("progression"))
	_add_menu_button(station, "Recenter Station", _menu_recenter_station)
	_add_menu_button(station, "Replay First-loop Guide", _replay_guide)
	if OS.is_debug_build():
		_add_menu_button(station, "Toggle Admin View", _menu_toggle_admin_view)
	_add_menu_button(station, "Back", _pause_page_back)
	var exits: VBoxContainer = pause_pages.exit
	_add_menu_button(exits, "Save & Return to Title", _menu_return_title)
	_add_menu_button(exits, "Save & Quit", _menu_quit_game)
	_add_menu_button(exits, "Restart Reboot Cycle", _menu_restart_cycle)
	end_expedition_button = Button.new()
	end_expedition_button.text = "End Expedition & Collect Research"
	end_expedition_button.pressed.connect(_end_expedition)
	preload("res://scripts/title_button_style.gd").apply(end_expedition_button, 480, 54)
	exits.add_child(end_expedition_button)
	_add_menu_button(exits, "Back", _pause_page_back)
	menu_save_feedback = Label.new()
	menu_save_feedback.name = "SaveFeedback"
	menu_save_feedback.text = ""
	menu_save_feedback.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	menu_save_feedback.add_theme_font_size_override("font_size", 15)
	menu_save_feedback.add_theme_color_override("font_color", Color("9ab9c3"))
	box.add_child(menu_save_feedback)
	var hint := Label.new()
	hint.text = "Esc: Back / Return to Station"
	hint.tooltip_text = "Escape returns from a submenu, then closes the pause menu."
	hint.add_theme_font_size_override("font_size", 14)
	hint.add_theme_color_override("font_color", Color("#8daab6"))
	box.add_child(hint)

func _add_menu_button(parent: Control, text: String, callable: Callable) -> void:
	var button := Button.new()
	button.text = {
		"Resume Cycle":"Return to Station",
		"Station & Archives":"Help & Station",
		"End or Leave Loop":"Leave Game",
		"Codex":"Codex & Discoveries",
		"Meta Progression":"Research & Unlocks",
		"Replay First-loop Guide":"Show Building Guide",
		"Save & Return to Title":"Save & Return to Title",
		"Save & Quit":"Save & Quit to Desktop",
		"Restart Reboot Cycle":"End Loop & Start Again"
	}.get(text,text)
	button.name = text.replace(" ", "")
	button.tooltip_text = {
		"Save Game": "Records the active loop. Continue restores it paused from the title screen.",
		"Save & Return to Title": "Records the active loop before opening the title screen.",
		"Save & Quit": "Records the active loop before closing the game.",
		"Restart Reboot Cycle": "Records this attempt before starting a new loop.",
		"Recenter Station": "Fits the station into view without changing its rooms."
	}.get(text, "")
	button.custom_minimum_size = Vector2(0, 54)
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.focus_mode = Control.FOCUS_ALL
	button.mouse_filter = Control.MOUSE_FILTER_STOP
	button.pressed.connect(callable)
	button.add_theme_font_size_override("font_size", 17)
	preload("res://scripts/title_button_style.gd").apply(button, 480, 54, text == "Resume Cycle")
	if text == "Codex": preload("res://scripts/navigation_badge.gd").apply(button, "codex")
	parent.add_child(button)
	if text == "Resume Cycle":
		menu_resume_button = button

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
	hardware=preload("res://scripts/station_hardware.gd").DEFAULTS.duplicate()
	if is_instance_valid(crew_comms): crew_comms.reset_for_loop()
	if menu_save_feedback != null:
		menu_save_feedback.text = "Record this loop to continue it from the title screen."
		menu_save_feedback.add_theme_color_override("font_color", Color("9ab9c3"))
	run_save_id = "%s-%s" % [Time.get_unix_time_from_system(), Time.get_ticks_usec()]
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
	event_history.clear()
	journal_scroll_positions.clear()
	journal_searches.clear()
	menu_workspace.clear()
	inspected_resource = ""
	if history_search != null:
		history_search.text = ""
		history_filter.select(0)
		archive_label.get_v_scroll_bar().set_deferred("value", 0.0)
	occupied.clear()
	placed_rooms.clear()
	wrecks = WreckField.initial()
	architect_run=Architects.begin(self)
	Companions.begin(self)
	for resource_id in Architects.starting_supplies(architect_run.selected):
		resources[resource_id] += Architects.STARTING_SUPPLIES[architect_run.selected][resource_id]
	drone_fleet.restore(null)
	recovered_crew.clear()
	hand.clear()
	draw_pile.clear()
	discard_pile.clear()
	rerolls_remaining = 3
	reroll_recovery_progress = 0
	grid_view.door_wet_history.clear()
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
	run_discovered_character_ids.clear()
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
	bill_npc = BillNPC.new()
	veld_npc = VeldNPC.new()
	branforth_npc = BranforthNPC.new()
	marsh_npc = MarshNPC.new()
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
	toast_record_keys.clear()
	current_toast_record = ""
	toast_playing = false
	cascade_toast.visible = false
	_place_room("brine_core", Vector2i(center_index, center_index), true)
	_clamp_resource_storage()
	_center_grid_on_core()
	_show_doctrine_selection()
	_log("Station systems restored. The water is still outside. For now.", false)
	_refresh_all()

func _draw_hand() -> void:
	hand.clear()
	_refill_hand()
	selected_card_id = hand[0] if not hand.is_empty() else ""
	selected_rotation = _default_card_rotation(selected_card_id)

func _build_run_deck() -> void:
	draw_pile = RunManagerScript.build_deck(selected_doctrines, meta.unlocked_room_ids)
	discard_pile.clear()
	_shuffle_draw_pile()
	# Stage existing foundation copies, without adding cards or revealing locks.
	# Retain the opening hand; offer a second affordable generator on first build.
	for id in ["corridor", "life_support", "current_turbine", "hydroponics_bay", "mining_drone_bay", "solar_array"]:
		if draw_pile.has(id):
			draw_pile.erase(id)
			draw_pile.append(id)

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
	_shuffle_draw_pile()
	_log("Blueprint discard pile recycled into the draw stack.", false)

func _shuffle_draw_pile() -> void:
	# Use the saved RNG instead of the unsaved global random stream.
	for index in range(draw_pile.size() - 1, 0, -1):
		var other := rng.randi_range(0, index)
		var card := draw_pile[index]
		draw_pile[index] = draw_pile[other]
		draw_pile[other] = card

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
	if drone_fleet.sites.has(cell) and drone_fleet.sites[cell].discovered and not occupied.has(cell) and (drone_fleet.sites[cell].units>0 or selected_card_id.is_empty()):
		selected_card_id = ""
		selected_room_cell = cell
		_refresh_all()
		return
	if drone_fleet.reserved(cell):
		selected_card_id = ""
		selected_room_cell = cell
		_refresh_all()
		return
	if WreckField.blocks(wrecks,cell):
		selected_card_id = ""
		selected_room_cell = cell
		last_preview_room_id = ""
		last_previewing_card = false
		_refresh_all()
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
		play_station_sound("ui_reject")
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
	selected_rotation = _default_card_rotation(selected_card_id)
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
	_refresh_placement_status()
	grid_view.queue_redraw()

func _can_place(id: String, cell: Vector2i) -> bool:
	return get_placement_problem(id, cell).is_empty()

func get_placement_problem(id: String, cell: Vector2i) -> String:
	if preload("res://scripts/crew_expedition.gd").reserved(self,cell): return "crew expedition return route reserved. Recall the crew before building here."
	if drone_fleet.reserved(cell): return "construction already scheduled here."
	if drone_fleet.Sites.blocks(drone_fleet.sites,cell): return "resource deposit occupies this cell. Select it to inspect extraction."
	if cell.x < 0 or cell.y < 0 or cell.x >= GRID_SIZE or cell.y >= GRID_SIZE:
		return "outside station grid."
	if occupied.has(cell):
		return "cell already contains %s." % occupied[cell]["display_name"]
	if WreckField.blocks(wrecks,cell):
		return "rock occupies this cell. Select it to break and clear." if wrecks[cell].kind == "basalt" else "wreckage occupies this cell. Select it to dismantle and salvage."
	var room := RoomDatabaseScript.get_room(id)
	if room.is_empty():
		return "unknown blueprint."
	if room.has("fixed_rotation") and selected_rotation != int(room.fixed_rotation):
		return "%s has a fixed orientation; doors: %s." % [room.display_name,_join_strings(get_room_doors(room)," / ")]
	if not testing_free_build and not _can_afford(room.get("cost", {})):
		return "Need %s more to build." % _format_cost(_missing_cost(room.get("cost", {})))
	if placed_rooms.is_empty():
		return ""
	var mismatch := ""
	for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
		var neighbor_pos: Vector2i = cell + offset
		if occupied.has(neighbor_pos):
			if _doors_connect(id, selected_rotation, offset, occupied[neighbor_pos]):
				return ""
			mismatch = "Door does not match %s. Rotate with %s." % [occupied[neighbor_pos]["display_name"], Preferences.key_name("Rotate blueprint")]
	if not mismatch.is_empty():
		if room.has("fixed_rotation"): return "connect %s through a matching %s door." % [room.display_name,_join_strings(get_room_doors(room)," / ")]
		return mismatch
	return "must connect to an adjacent door."

func _place_room(id: String, cell: Vector2i, free := false, construction_complete := false) -> void:
	var build_rotation: int=int(RoomDatabaseScript.get_room(id).get("fixed_rotation",selected_rotation))
	if not free and drone_fleet.Sites.blocks(drone_fleet.sites,cell): return
	if not free and WreckField.blocks(wrecks,cell):
		return
	if not free and not testing_free_build and not construction_complete:
		drone_fleet.enqueue(id,cell,build_rotation)
		play_station_sound("placement",Vector2(cell))
		_log("Construction scheduled: %s. Materials reserved." % RoomDatabaseScript.get_room(id).display_name,false)
		return
	var previous_link_keys := _active_synergy_link_keys()
	var room := RoomDatabaseScript.get_room(id).duplicate(true)
	room["pos"] = cell
	room["rotation"] = build_rotation if not free else 0
	if ROOM_ART_VARIANT_COUNTS.has(id):
		room["art_variant"] = rng.randi_range(0, int(ROOM_ART_VARIANT_COUNTS[id]) - 1)
	placed_rooms.append(room)
	occupied[cell] = room
	if not free:
		_log("Built %s at %s." % [room["display_name"], cell])
		play_station_sound("build_complete" if construction_complete else "placement",Vector2(cell))
		if is_instance_valid(crew_comms): crew_comms.room_built(id)
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
	preload("res://scripts/transmission_archive.gd").survey_receivers(self)
	preload("res://scripts/listening_post.gd").tick(self)
	preload("res://scripts/local_incidents.gd").seed(self)
	preload("res://scripts/rare_branch_control.gd").tick(self)
	preload("res://scripts/local_incidents.gd").resolve(self)
	_advance_draft_recovery()
	_advance_synergy_discovery_cycle()
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
	if not hardware.power:
		for room in placed_rooms: offline[room.pos]="MASTER POWER OFF"
		return {"delta":{},"working_cells":{},"offline":offline,"generator_outputs":{},"power_failures":[],"links":[],"generation":0,"power_used":0,"added_crew":0}
	var power_failures := []
	var input_budget := resources.duplicate()
	var generation := 0
	var generator_outputs := {}
	var generators := {}
	# Generators reserve their stored fuel before consumers. Never count unfuelled
	# output, and never spend that fuel twice in the ordinary operation pass.
	for room in placed_rooms:
		if int(room.get("production", {}).get("power", 0)) <= 0:
			continue
		var cell: Vector2i = room.pos
		generators[cell] = true
		if not hardware.pumps and int(room.get("production",{}).get("water",0))>0:
			offline[cell]="PUMPS OFF"
			continue
		if room.get("suspended", false):
			offline[cell] = "SUSPENDED"
			continue
		if preload("res://scripts/rare_branch_control.gd").offline(room):
			offline[cell] = "ISOLATED" if room.get("isolated", false) else "FLOODED"
			continue
		if room.id == "current_turbine" and not _turbine_intake_clear(room):
			offline[cell] = "INTAKE BLOCKED"
			continue
		var fuel: Dictionary = room.get("consumption", {})
		var missing: Array[String] = []
		for key in fuel:
			if int(input_budget.get(key, 0)) < int(fuel[key]):
				missing.append(str(key).replace("_", " ").to_upper())
		if not missing.is_empty():
			offline[cell] = "NEEDS %s" % _join_strings(missing, " + ")
			continue
		for key in fuel:
			input_budget[key] = int(input_budget.get(key, 0)) - int(fuel[key])
		_add_to_delta(delta, _without_key(fuel, "power"), -1)
		_add_to_delta(delta, _without_key(room.get("production", {}), "power"), 1)
		generation += int(room.production.power)
		generator_outputs[cell] = int(room.production.power)
		working_cells[cell] = true
	# Heat recovery depends only on reactors that passed this cycle's checks.
	for room in placed_rooms:
		if room.id != "heat_recovery": continue
		var cell: Vector2i = room.pos
		generators[cell] = true
		if not hardware.pumps and int(room.get("production",{}).get("water",0))>0:
			offline[cell]="PUMPS OFF"
			continue
		if room.get("suspended", false):
			offline[cell] = "SUSPENDED"
			continue
		if preload("res://scripts/rare_branch_control.gd").offline(room):
			offline[cell] = "ISOLATED" if room.get("isolated", false) else "FLOODED"
			continue
		var recovered := 0
		for offset in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
			var adjacent: Vector2i = cell + offset
			if occupied.has(adjacent) and occupied[adjacent].id == "reactor" and working_cells.has(adjacent):
				recovered += 2
		if recovered == 0:
			offline[cell] = "NEEDS ACTIVE REACTOR"
			continue
		generation += mini(recovered, 4)
		generator_outputs[cell] = mini(recovered, 4)
		working_cells[cell] = true
	input_budget["power"] = generation + maxi(int(input_budget["power"]), 0)
	var reserve_start := int(resources["power"])
	var added_crew := 0
	for room in _rooms_by_power_priority():
		var cell: Vector2i = room["pos"]
		if generators.has(cell): continue
		if preload("res://scripts/rare_branch_control.gd").offline(room):
			offline[cell]="ISOLATED" if room.get("isolated",false) else "FLOODED"
			continue
		if not hardware.pumps and int(room.get("production",{}).get("water",0))>0:
			offline[cell]="PUMPS OFF"
			continue
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
		if room.get("flooded",false) and room.get("flood_compatible",false):_add_to_delta(delta,{"biomass":2},1)
		if room.id not in ["mining_drone_bay","salvage_drone_bay"]:
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
			var finite_ward := false
			for cell in link.get("cells",[]):
				if occupied.has(cell) and occupied[cell].get("recovered_derelict",false): finite_ward=true
			if finite_ward: continue # Occupants are released once by their emergence sequence.
			added_crew += 1
			break
	var used := generation + maxi(reserve_start, 0) - int(input_budget["power"])
	var final_power := clampi(int(input_budget["power"]) + int(delta.get("power", 0)), 0, _get_power_capacity())
	delta["power"] = final_power - reserve_start
	return {"delta": delta, "working_cells": working_cells, "offline": offline, "generator_outputs":generator_outputs,
		"power_failures": power_failures, "links": links, "generation": generation,
		"power_used": used, "added_crew": added_crew}

func _turbine_intake_cell(room: Dictionary) -> Vector2i:
	var offsets := [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]
	return Vector2i(room.get("pos", Vector2i.ZERO)) + offsets[posmod(int(room.get("rotation", 0)), 4)]

func _turbine_intake_clear(room: Dictionary) -> bool:
	var intake := _turbine_intake_cell(room)
	return intake.x >= 0 and intake.y >= 0 and intake.x < GRID_SIZE and intake.y < GRID_SIZE and not occupied.has(intake) and not WreckField.blocks(wrecks, intake) and not drone_fleet.Sites.blocks(drone_fleet.sites, intake) and not drone_fleet.reserved(intake)

func _apply_room_economy() -> Dictionary:
	var result := _simulate_room_economy()
	drone_fleet.synchronize(placed_rooms)
	for room in placed_rooms:
		var cell: Vector2i = room.pos
		var before: String = str(offline_reasons.get(cell, "FUNCTIONING"))
		var after: String = str(result.offline.get(cell, "FUNCTIONING"))
		if before != after:
			_log("%s at %s: %s -> %s" % [room.display_name, cell, before, after], false)
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
	# Legacy entry point retained for old fixtures; orbital POIs are retired.
	pass

func _breathing_crew_count() -> int:
	return maxi(0,crew_count-int(Architects.present(self,"marsh") and not marsh_npc.dead))

func _apply_life_support() -> void:
	if crew_count <= 0:
		return
	resources["food"] -= crew_count
	resources["oxygen"] -= _breathing_crew_count()
	last_cycle_delta["food"] = last_cycle_delta.get("food", 0) - crew_count
	last_cycle_delta["oxygen"] = last_cycle_delta.get("oxygen", 0) - _breathing_crew_count()

func _emit_warnings() -> void:
	var net := _project_cycle_delta()
	var audible_warnings := {}
	if power_generated + int(resources.power) < _project_power_demand(): audible_warnings["power_shortfall"] = true
	elif resources.power <= max(2,int(_get_power_capacity()*0.2)): audible_warnings["power_reserve"] = true
	if resources.integrity <= 20: audible_warnings["integrity"] = true
	if corruption >= 7: audible_warnings["corruption"] = true
	if crew_count > 0:
		if resources.oxygen + net.get("oxygen",0) <= 0: audible_warnings["oxygen"] = true
		if resources.food + net.get("food",0) <= 0: audible_warnings["food"] = true
	if is_instance_valid(station_sound): station_sound.update_warnings(audible_warnings)
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
	if is_instance_valid(crew_comms): crew_comms.transmit("brine","A new connection. The station has done something I did not predict. I have recorded it. That does not mean I understand it.","discovery/"+synergy_id)
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
	_log("Pattern discovered: %s. %s" % [synergy.get("name", "Recovered pattern"), synergy.get("message", "BRINE recovered a functioning room pattern.")])
	_queue_center_toast("PATTERN DISCOVERED\n%s\nClick to review · Saved in Archive" % str(synergy.get("name", synergy_id)).to_upper(), "synergy:" + synergy_id)

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
	play_station_sound("discovery")
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
			_queue_center_toast("BLUEPRINT DECRYPTED\n%s\nClick to review · Saved in Archive" % room_name.to_upper(), "room:" + unlock_id)
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

func _queue_center_toast(message: String, record_key := "") -> void:
	if toast_messages.has(message):
		return
	if toast_messages.size() >= 3:
		toast_record_keys.erase(toast_messages.pop_front())
	if not record_key.is_empty():
		toast_record_keys[message] = record_key
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
	current_toast_record = str(toast_record_keys.get(message, ""))
	toast_record_keys.erase(message)
	cascade_toast.mouse_filter = Control.MOUSE_FILTER_STOP if not current_toast_record.is_empty() else Control.MOUSE_FILTER_IGNORE
	cascade_toast.visible = true
	if Preferences.reduced_motion:
		cascade_toast.modulate = Color.WHITE
		cascade_toast.scale = Vector2.ONE
		cascade_toast_tween = create_tween()
		cascade_toast_tween.tween_interval(3.5 if not current_toast_record.is_empty() else 2.0)
		cascade_toast_tween.tween_callback(_finish_center_toast)
		return
	cascade_toast.modulate = Color(1, 1, 1, 0)
	cascade_toast.scale = Vector2(0.96, 0.96)
	cascade_toast.pivot_offset = cascade_toast.size * 0.5
	cascade_toast_tween = create_tween()
	cascade_toast_tween.set_parallel(true)
	cascade_toast_tween.tween_property(cascade_toast, "modulate:a", 1.0, 0.12)
	cascade_toast_tween.tween_property(cascade_toast, "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	cascade_toast_tween.chain().tween_interval(3.5 if not current_toast_record.is_empty() else 1.15)
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
	return {} # Timed reconstruction directives are retired.

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

func _discovered_character_names() -> String:
	var names: Array[String] = []
	for id in run_discovered_character_ids:
		names.append(Architects.NAMES.get(id, Companions.NAMES.get(id, id)))
	return _join_strings(names) if not names.is_empty() else "None"

func _show_reboot_summary(reason: String, victory := false, archived := false) -> void:
	RunSave.clear_run(run_save_id, run_save_path)
	running = false
	play_station_sound("ui_end" if archived or victory else "ui_failure")
	run_victory = run_victory or victory
	var earned := int(float(max(resources["data"], 0)) / 5.0) + int(float(resonance_score) / 50.0)
	var award := maxi(0, earned - run_awarded_research)
	run_awarded_research += award
	meta.add_research_points(award)
	var previous_doctrine_ranks := {}
	for doctrine_id_value in selected_doctrines:
		var doctrine_id := str(doctrine_id_value)
		previous_doctrine_ranks[doctrine_id] = meta.get_doctrine_rank(doctrine_id)
	if not run_rewards_recorded:
		meta.record_run([], victory, resonance_score)
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
	discoveries += "\nCharacters discovered: " + _discovered_character_names()
	summary_text.text = "%s\n\n%s\n\nCycles survived: %d\nCrew remaining: %d\nResonance: %d\nLinks formed: %d / Best cascade: x%d\nResearch awarded: %d\nTotal research: %d" % [reason, discoveries, cycle, crew_count, resonance_score, links_formed, largest_cascade, award, meta.total_research_points]
	summary_text.text += "\nResources earned: %s" % (_format_cost(run_earned) if not run_earned.is_empty() else "None")
	summary_layer.visible = true
	var ranks_gained: Array[String] = []
	for id in previous_doctrine_ranks:
		if meta.get_doctrine_rank(id) > int(previous_doctrine_ranks[id]):
			ranks_gained.append("%s → rank %d" % [RunManagerScript.doctrine(id).name, meta.get_doctrine_rank(id)])
	var pattern_research := 0
	for id in run_stabilized_synergy_ids:
		pattern_research += int(SynergyManagerScript.get_synergy(id).get("terminal_reward", {}).get("research", 0))
	var retained := "WHAT SURVIVES\nNew patterns: %d / Stabilized: %d / New blueprints: %d\nResearch banked: %d from score / %d from patterns\nLearned patterns, unlocked blueprints and recovered characters remain in your profile.\n\n" % [run_discovered_synergy_ids.size(), run_stabilized_synergy_ids.size(), run_decrypted_blueprint_ids.size(), run_awarded_research, pattern_research]
	summary_text.text = "OUTCOME // " + reason + "\n\n" + retained + "RUN RECORD\n" + summary_text.text.trim_prefix(reason + "\n\n")
	_refresh_learning_ui()
	preload("res://scripts/title_settings.gd").apply_menu_text(summary_layer)
	if is_instance_valid(continue_expedition_button) and continue_expedition_button.visible:
		continue_expedition_button.grab_focus()
	elif summary_layer.has_meta("default_button"):
		var default_button := summary_layer.get_meta("default_button") as Button
		if is_instance_valid(default_button):
			default_button.grab_focus()
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
	_log("Expedition extended. No directive deadlines; life support remains active.")
	_refresh_all()

func _end_expedition() -> void:
	if not expedition_mode or not running:
		return
	menu_open = false
	if menu_layer != null:
		menu_layer.visible = false
	_show_reboot_summary("Expedition archived. Your station's discoveries remain with BRINE.",false,true)

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

func _finish_guide() -> void:
	meta.guide_completed = true
	meta.save_to_disk()
	_refresh_learning_ui()

func _replay_guide() -> void:
	guide_replay = true
	meta.guide_completed = false
	meta.save_to_disk()
	_close_menu()
	_refresh_learning_ui()

func _refresh_learning_ui() -> void:
	if guide_box == null:
		return
	guide_box.hide() # The sidebar tutorial has been retired.
	guide_label.max_lines_visible = 5
	guide_label.text_overrun_behavior = TextServer.OVERRUN_NO_TRIMMING
	guide_label.text = preload("res://scripts/station_ui_insights.gd").guide(self)
	if not guide_replay and not meta.guide_completed and not run_stabilized_synergy_ids.is_empty():
		_finish_guide()
		return
	discovery_review_button.visible = true
	discovery_review_button.text = "ARCHIVE\n%d NEW" % meta.unread_records.size()

func _review_latest_discovery() -> void:
	var key := "" if meta.unread_records.is_empty() else str(meta.unread_records.keys().back())
	_review_discovery_key(key)

func _review_discovery_key(key: String) -> void:
	var section := "progression" if key.begins_with("mastery:") else "codex"
	if _gameplay_input_blocked() and not menu_open:
		_open_overlay_settings()
	else:
		if not menu_open:
			_open_menu()
		_open_shared_menu(section)
	if not is_instance_valid(menu_archive):
		return
	menu_archive.show_section(section)
	if section == "codex" and not key.is_empty():
		var id := key.get_slice(":", 1)
		var synergy := key.begins_with("synergy:")
		menu_archive.codex_tabs.current_tab = 1 if synergy else 0
		menu_archive.search.text = str(SynergyManagerScript.get_synergy(id).get("name", "")) if synergy else str(RoomDatabaseScript.get_room(id).get("display_name", ""))
		menu_archive._populate_cards()
	if section == "codex":
		meta.mark_reviewed(key)
		menu_archive._populate_cards()
	_refresh_learning_ui()

func _focus_inspected_room() -> void:
	var cell: Vector2i = inspector_focus_button.get_meta("cell", Vector2i(-1, -1))
	if not occupied.has(cell) and not WreckField.blocks(wrecks,cell) and not drone_fleet.reserved(cell):
		return
	selected_card_id = ""
	hovered_card_id = ""
	selected_room_cell = cell
	hover_cell = cell
	var center := (Vector2(cell) + Vector2.ONE * 0.5) * get_cell_size()
	grid_scroll.scroll_horizontal = maxi(0, int(center.x - grid_scroll.size.x * 0.5))
	grid_scroll.scroll_vertical = maxi(0, int(center.y - grid_scroll.size.y * 0.5))
	grid_view.queue_redraw()

func _refresh_all() -> void:
	_refresh_learning_ui()
	Preferences.apply_key_hints(self)
	_refresh_resources()
	_refresh_cards()
	_refresh_inspector()
	_refresh_orbital_objective()
	if _journal_is_open():
		_refresh_archive()
	elif journal_button != null:
		journal_button.text = "JOURNAL [%s]\n%d LEARNED" % [Preferences.key_name("Journal"), meta.discovered_synergy_ids.size()]
	_refresh_routing()
	_refresh_placement_status()
	_refresh_log()
	_refresh_view_mode_button()
	_refresh_menu_status()
	grid_view.queue_redraw()

func _refresh_orbital_objective() -> void:
	if orbital_objective_label == null:
		return
	orbital_objective_label.text = "STATION RESTORATION\n%d learned / %d stabilized this loop\n\nRestore rooms. Sustain the crew.\nKeep useful patterns functioning." % [run_discovered_synergy_ids.size(), run_stabilized_synergy_ids.size()]
	var learning: Array[String] = preload("res://scripts/station_ui_insights.gd").learning(self)
	if not learning.is_empty():
		orbital_objective_label.text = "PATTERN WATCH\n" + learning[0] + ("\n+%d more in Journal / Patterns" % (learning.size()-1) if learning.size()>1 else "")
	orbital_objective_label.tooltip_text = "Patterns stabilize after three consecutive functioning cycles."

func _on_zoom_changed(value: float) -> void:
	_request_grid_zoom(DEFAULT_GRID_ZOOM * value)

func _request_grid_zoom(value: float) -> void:
	if camera_zoom_target<0.0: camera_zoom_center=_grid_view_center_ratio()
	camera_zoom_target=clampf(value,_minimum_map_zoom(),DEFAULT_GRID_ZOOM)

func _update_camera_zoom(delta: float) -> void:
	if camera_zoom_target<0.0: return
	if _gameplay_input_blocked():
		camera_zoom_target=-1.0
		return
	var target := camera_zoom_target
	var next := lerpf(grid_zoom,target,1.0-exp(-18.0*delta))
	if absf(next-target)<0.0005: next=target
	_set_grid_zoom(next,true,camera_zoom_center)
	if next!=target: camera_zoom_target=target

func _set_grid_zoom(value: float, update_slider := true, target_center := Vector2.INF) -> void:
	camera_view_revision += 1
	camera_zoom_target=-1.0
	var center_ratio := _grid_view_center_ratio() if target_center == Vector2.INF else target_center
	grid_zoom = clampf(value, _minimum_map_zoom(), DEFAULT_GRID_ZOOM)
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
	var revision := camera_view_revision
	await get_tree().process_frame
	if revision == camera_view_revision: _restore_grid_view_center(center_ratio)

func _toggle_pause() -> void:
	if _gameplay_input_blocked():
		return
	_set_paused(not paused, true)

func _set_paused(value: bool, write_log := false) -> void:
	if not value and is_instance_valid(crew_comms) and crew_comms.holds_pause:
		value = true
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
	menu_workspace = preload("res://scripts/workspace_state.gd").capture(self)
	menu_open = true
	_show_pause_page("main")
	pause_before_menu = paused
	menu_resume_button.text = "Return to Station · Paused" if pause_before_menu else "Resume Cycle"
	_set_paused(true, false)
	menu_layer.visible = true
	if menu_transition and menu_transition.is_running():
		menu_transition.kill()
	menu_center.modulate.a = 1.0
	if not Preferences.reduced_motion:
		menu_center.modulate.a = 0.0
		menu_transition = create_tween()
		menu_transition.tween_property(menu_center, "modulate:a", 1.0, 0.16)
	Preferences.apply_menu_text(menu_center)
	menu_resume_button.grab_focus()
	_refresh_menu_status()
	_refresh_all()
	if grid_view != null:
		grid_view.queue_redraw()

func _close_menu() -> void:
	if is_instance_valid(menu_archive):
		menu_archive._close()
		return
	if menu_layer == null:
		return
	menu_open = false
	_set_paused(pause_before_menu, false)
	menu_layer.visible = false
	_refresh_all()
	preload("res://scripts/workspace_state.gd").restore(self,menu_workspace)
	if menu_workspace.get("camera_center") is Vector2: _restore_grid_view_center(menu_workspace.camera_center)
	if grid_view != null:
		grid_view.queue_redraw()

func _refresh_menu_status() -> void:
	if end_expedition_button != null:
		end_expedition_button.visible = expedition_mode and running
	if menu_status_label == null:
		return
	menu_status_label.text = "Cycle %03d  |  Integrity %d%%  |  Crew %d  |  View %s" % [cycle, resources.get("integrity", 0), crew_count, "ADMIN" if admin_mode else "NORMAL"]
	if not meta.last_error.is_empty():
		menu_status_label.text += "\nPROGRESSION NOT SAVED // " + meta.last_error

func _open_shared_menu(section: String) -> void:
	if not menu_open or is_instance_valid(menu_archive):
		return
	menu_section_opener = get_viewport().gui_get_focus_owner()
	menu_archive = preload("res://scripts/title_archive.gd").new()
	menu_archive.meta_state = meta
	menu_archive.mode = section
	menu_archive.in_game = true
	menu_center.hide()
	menu_layer.add_child(menu_archive)
	menu_archive.closed.connect(func() -> void:
		menu_archive = null
		menu_center.show()
		Preferences.apply_menu_text(menu_center)
		if is_instance_valid(menu_section_opener):
			menu_section_opener.grab_focus()
		else:
			menu_resume_button.grab_focus()
	)

func _open_overlay_settings() -> void:
	if not doctrine_layer.visible and not journal_layer.visible and not summary_layer.visible:
		_open_menu()
		_open_shared_menu("settings")
		return
	if is_instance_valid(menu_archive):
		return
	var source: CanvasLayer = doctrine_layer if doctrine_layer.visible else (journal_layer if journal_layer.visible else summary_layer)
	var opener := get_viewport().gui_get_focus_owner()
	source.hide()
	menu_archive = preload("res://scripts/title_archive.gd").new()
	menu_archive.meta_state = meta
	menu_archive.mode = "settings"
	menu_archive.in_game = true
	menu_layer.show()
	menu_center.hide()
	menu_layer.add_child(menu_archive)
	menu_archive.closed.connect(func() -> void:
		menu_archive = null
		menu_layer.hide()
		menu_center.show()
		source.show()
		Preferences.apply_menu_text(source)
		if is_instance_valid(opener):
			opener.grab_focus()
	)

func _menu_recenter_station() -> void:
	_center_grid_on_station_deferred()
	_close_menu()

func _menu_toggle_admin_view() -> void:
	admin_mode = not admin_mode
	_log("Admin topology overlay %s." % ("enabled" if admin_mode else "hidden"), false)
	_refresh_menu_status()
	_refresh_all()

func _choose_restart_architect() -> void:
	var opener := get_viewport().gui_get_focus_owner()
	var layer := CanvasLayer.new()
	layer.layer = 100
	var picker = preload("res://scripts/architect_selection.gd").new()
	picker.meta_state = meta
	layer.add_child(picker)
	add_child(layer)
	picker.closed.connect(func():
		layer.queue_free()
		if menu_open: _show_pause_page("exit")
		elif is_instance_valid(opener): opener.grab_focus()
	)
	picker.chosen.connect(func(_id: String):
		layer.queue_free()
		menu_open = false
		menu_layer.visible = false
		_start_reboot_cycle()
	)

func _menu_restart_cycle() -> void:
	if running and not _save_active_loop(): return
	_choose_restart_architect()

func _menu_quit_game() -> void:
	if not running or _save_active_loop():
		preload("res://scripts/audio_shutdown.gd").request(self)
	else:
		_open_menu()
		menu_status_label.text = RunSave.last_error if not RunSave.last_error.is_empty() else meta.last_error

func _save_active_loop() -> bool:
	var error := RunSave.write(self, run_save_path)
	if error != OK:
		menu_save_feedback.text = "SAVE FAILED // " + RunSave.last_error
		menu_save_feedback.add_theme_color_override("font_color", Color("ffb5a8"))
		return false
	if meta.save_to_disk() != OK:
		menu_save_feedback.text = "LOOP RECORDED / PROGRESSION NOT SAVED // " + meta.last_error
		menu_save_feedback.add_theme_color_override("font_color", Color("ffb5a8"))
		return false
	menu_save_feedback.text = "LOOP RECORDED // Cycle %03d. Continue is available on the title screen." % cycle
	menu_save_feedback.add_theme_color_override("font_color", Color("91e2dd"))
	return true

func _menu_save_game() -> void:
	play_station_sound("ui_saved" if _save_active_loop() else "ui_reject")

func _menu_return_title() -> void:
	if running and not _save_active_loop():
		return
	get_tree().change_scene_to_file("res://scenes/title_screen.tscn")

func _notification(what: int) -> void:
	if get_meta("restoring_checkpoint",false):
		if what == NOTIFICATION_WM_CLOSE_REQUEST: preload("res://scripts/audio_shutdown.gd").request(self)
		return
	if what == NOTIFICATION_WM_WINDOW_FOCUS_OUT and Preferences.pause_unfocused and running and not paused:
		_set_paused(true, false)
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		_menu_quit_game()

func _exit_tree() -> void:
	get_tree().auto_accept_quit = true

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
	if cycle_counter_label != null:
		cycle_counter_label.text = "CYCLE %03d" % cycle
	if solar_meter == null or solar_time_label == null or tick_timer == null:
		return
	var wait: float = maxf(float(tick_timer.wait_time), 0.01)
	var left: float = clampf(float(tick_timer.time_left), 0.0, wait)
	var progress: float = 1.0 - (left / wait)
	solar_meter.value = progress
	var caption: String = "HOLD" if paused else "%02ds" % int(ceil(left))
	if solar_time_label.text != caption:
		solar_time_label.text = caption

func _set_time_speed(index: int) -> void:
	var remaining_fraction := 1.0
	if tick_timer != null and not tick_timer.is_stopped():
		remaining_fraction = clampf(tick_timer.time_left / maxf(tick_timer.wait_time, 0.01), 0.0, 1.0)
	time_speed_index = clampi(index, 0, time_speeds.size() - 1)
	for i in range(speed_buttons.size()):
		speed_buttons[i].set_pressed_no_signal(i == time_speed_index)
		_style_hud_button(speed_buttons[i], i == time_speed_index)
	if tick_timer != null:
		var duration := _cycle_wait_seconds()
		tick_timer.start(maxf(0.001, duration * remaining_fraction))
		# start(time) changes wait_time too; subsequent cycles need the full duration.
		tick_timer.wait_time = duration
		tick_timer.paused = paused
	_log("Time speed set to %dx." % int(time_speeds[time_speed_index]), false)

func _cycle_wait_seconds() -> float:
	return BASE_CYCLE_SECONDS / time_speeds[time_speed_index]

func _update_camera_pan(delta: float) -> void:
	if _gameplay_input_blocked():
		camera_pan_remainder = Vector2.ZERO
		camera_pan_velocity = Vector2.ZERO
		return
	if grid_scroll == null:
		return
	var direction := Vector2.ZERO
	if Input.is_key_pressed(int(Preferences.keys["Pan left"])):
		direction.x -= 1.0
	if Input.is_key_pressed(int(Preferences.keys["Pan right"])):
		direction.x += 1.0
	if Input.is_key_pressed(int(Preferences.keys["Pan up"])):
		direction.y -= 1.0
	if Input.is_key_pressed(int(Preferences.keys["Pan down"])):
		direction.y += 1.0
	if direction == Vector2.ZERO:
		camera_pan_remainder = Vector2.ZERO
		camera_pan_velocity = Vector2.ZERO
		return
	# Brief acceleration; release stops immediately for precise placement.
	camera_pan_velocity=camera_pan_velocity.lerp(direction.normalized(),1.0-exp(-16.0*delta))
	_pan_grid(camera_pan_velocity, delta)

func _pan_grid(direction: Vector2, delta: float) -> void:
	var travel := direction.limit_length(1.0) * 1050.0 * delta + camera_pan_remainder
	var pixels := Vector2i(int(travel.x), int(travel.y))
	camera_pan_remainder = travel - Vector2(pixels)
	grid_scroll.scroll_horizontal += pixels.x
	grid_scroll.scroll_vertical += pixels.y

func _apply_grid_zoom() -> void:
	grid_zoom = maxf(grid_zoom, _minimum_map_zoom())
	if zoom_slider != null:
		# Updating the slider range must not queue a user zoom and cancel startup centering.
		var signals_blocked := zoom_slider.is_blocking_signals()
		zoom_slider.set_block_signals(true)
		zoom_slider.min_value = _minimum_map_zoom() / DEFAULT_GRID_ZOOM
		zoom_slider.set_value_no_signal(grid_zoom / DEFAULT_GRID_ZOOM)
		zoom_slider.set_block_signals(signals_blocked)
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
	var revision := camera_view_revision
	await get_tree().process_frame
	if grid_scroll == null or revision != camera_view_revision:
		return
	_set_grid_zoom(grid_zoom,true,(Vector2(Architects.CORE_CELL)+Vector2.ONE*0.5)/float(GRID_SIZE))

func _center_grid_on_station() -> void:
	var revision := camera_view_revision
	await get_tree().process_frame
	if revision == camera_view_revision: _center_grid_on_station_now()

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
	# Fit uses its destination immediately; preserving the old center first can
	# rebuild a different visible room set before the deferred station centering.
	_set_grid_zoom(minf(fit_zoom, DEFAULT_GRID_ZOOM * 0.60),true,bounds.get_center()/float(GRID_SIZE))

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
	var forecast := _simulate_room_economy(true, cycle + 1)
	var net := _project_cycle_delta(forecast)
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
	for key in net:
		var chip_id: String = "rare" if key == "rare_minerals" else str(key)
		if resource_chips.has(chip_id):
			resource_chips[chip_id].tooltip_text = _reserve_forecast(str(key), int(net[key])) + "\nClick or press Enter for room contributions. Estimates can change with events and inputs."
	if diagnostics_button != null:
		var risk: Dictionary = forecast.offline
		var suspended := 0
		for reason in risk.values():
			if reason == "SUSPENDED":
				suspended += 1
		diagnostics_button.text = "DIAGNOSTICS\n%d ALERTS" % (risk.size() - suspended)
		diagnostics_button.tooltip_text = "Forecast room interruptions, locate affected rooms, and inspect reserves."

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
		var resource_id: String = "rare_minerals" if id == "rare" else id
		if BASE_STORAGE_CAPACITY.has(resource_id) or resource_id=="crew":
			chip.tooltip_text += "\nClick or press Enter for the crew roster." if resource_id=="crew" else "\nClick or press Enter for room contributions."
			chip.focus_mode = Control.FOCUS_ALL
			chip.mouse_entered.connect(func(): chip.self_modulate = Color("b4fff1"))
			chip.mouse_exited.connect(func():
				if not chip.has_focus(): chip.self_modulate = Color.WHITE)
			chip.mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
			chip.focus_entered.connect(func(): chip.self_modulate = Color("b4fff1"))
			chip.focus_exited.connect(func(): chip.self_modulate = Color.WHITE)
			chip.gui_input.connect(func(event: InputEvent):
				if (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT) or event.is_action_pressed("ui_accept"):
					chip.accept_event()
					_open_resource_details(resource_id, chip))
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
	var chip_style: StyleBoxFlat = chip_panel.get_theme_stylebox("panel") as StyleBoxFlat if chip_panel.has_theme_stylebox_override("panel") else StyleBoxFlat.new()
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

func _project_cycle_delta(forecast: Dictionary = {}) -> Dictionary:
	var result: Dictionary = _simulate_room_economy(true, cycle + 1) if forecast.is_empty() else forecast
	# Crew upkeep belongs to the projection, never to the shared room result.
	var delta: Dictionary = result["delta"].duplicate()
	var projected_crew := crew_count + int(result["added_crew"])
	if projected_crew > 0:
		_add_to_delta(delta, {"food": projected_crew, "oxygen": _breathing_crew_count()+int(result["added_crew"])}, -1)
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
		card_slot.custom_minimum_size = Vector2(234, 344)
		card_slot.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		card_slot.mouse_filter = Control.MOUSE_FILTER_IGNORE
		var card := PanelContainer.new()
		card.name = "%sCard" % id
		card.position = Vector2(0, 14)
		card.size = Vector2(224, 320)
		card.custom_minimum_size = Vector2(224, 320)
		card.mouse_filter = Control.MOUSE_FILTER_STOP
		card.set_meta("card_id", id)
		card.set_meta("category_color", category_color)
		card.set_meta("rest_position", card.position)
		card.set_meta("affordable", _can_afford(room.get("cost", {})))
		card.tooltip_text = _blueprint_decision(room)
		_apply_card_style(card, category_color, selected_card_id == id, _can_afford(room.get("cost", {})))
		card.mouse_entered.connect(_on_card_hovered.bind(id, card))
		card.mouse_exited.connect(_on_card_unhovered.bind(id, card))
		card.gui_input.connect(_on_card_gui_input.bind(id))
		var body := VBoxContainer.new()
		body.add_theme_constant_override("separation", 5)
		body.mouse_filter = Control.MOUSE_FILTER_IGNORE
		card.add_child(body)
		var image_wrap := Control.new()
		image_wrap.custom_minimum_size = Vector2(0, 128)
		image_wrap.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(image_wrap)
		var image := TextureRect.new()
		image.set_anchors_preset(Control.PRESET_FULL_RECT)
		image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		if id in ["cold_store", "galley", "salvage_workshop", "current_turbine", "biomass_digester", "heat_recovery", "airlock", "construction_drone_bay", "mycelium_nursery", "life_support", "hydroponics_bay", "reactor", "med_bay", "crew_hab", "cryo_chamber", "clone_lab", "data_archive", "biodome", "xeno_lab", "med_office","med_center","holographic_core","bio_lab","anomaly_lab", "battery_array", "research_lab", "maintenance_bay", "storage_bay", "ore_refinery", "mining_drone_bay", "salvage_drone_bay", "crew_lounge", "command_center", "quarantine_cell", "solar_array", "radio_lab", "shield_generator", "tidal_condenser", "gravity_loom", "brine_core", "corridor", "corner", "tee_corridor", "pressure_control", "listening_post", "isolation_vault"]:
			image.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		image.texture = card_textures.get(id)
		image.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		image.mouse_filter = Control.MOUSE_FILTER_IGNORE
		image_wrap.add_child(image)
		var badge := Label.new()
		badge.text = room["rarity"].to_upper()
		badge.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		badge.set_anchors_preset(Control.PRESET_TOP_RIGHT)
		badge.position = Vector2(-84, 8)
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
			prototype_badge.position = Vector2(0, 102)
			prototype_badge.custom_minimum_size = Vector2(112, 22)
			prototype_badge.add_theme_font_size_override("font_size", 10)
			prototype_badge.add_theme_color_override("font_color", Color("#d8fff2"))
			prototype_badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
			_add_label_panel_style(prototype_badge, Color("#0b3029"), UI_ACCENT_BRIGHT)
			image_wrap.add_child(prototype_badge)
		var name_label := Label.new()
		name_label.text = "■ %s" % room["display_name"]
		name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		name_label.add_theme_font_size_override("font_size", 20)
		name_label.add_theme_color_override("font_color", Color("#f2f7fb"))
		name_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(name_label)
		var output_label := RichTextLabel.new()
		output_label.bbcode_enabled = true
		output_label.fit_content = true
		output_label.scroll_active = false
		output_label.text = _primary_output_line(room)
		output_label.add_theme_font_size_override("normal_font_size", 15)
		output_label.add_theme_color_override("default_color", Color("#8fa3ae"))
		output_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		body.add_child(output_label)
		var cost_label := RichTextLabel.new()
		cost_label.bbcode_enabled = true
		cost_label.fit_content = true
		cost_label.scroll_active = false
		cost_label.text = "[color=#607784]COST[/color]  %s" % _format_resource_list(room.get("cost", {}), 14)
		cost_label.add_theme_font_size_override("normal_font_size", 15)
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
		synergy_label.visible = false # Full known links live in the clicked inspector.
		body.add_child(synergy_label)
		var footer_label := Label.new()
		footer_label.text = "CLICK TO SELECT" if _can_afford(room.get("cost", {})) else "SHORT: " + _format_cost(_missing_cost(room.get("cost", {})))
		footer_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		footer_label.add_theme_font_size_override("font_size", 12)
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
	slot.custom_minimum_size = Vector2(146, 320)
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
	if room.id=="heat_recovery": return "Power 0–4 · heat recovery"
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
	return preload("res://scripts/safe_image.gd").raw_texture(path)

func _load_card_textures() -> void:
	for id in room_texture_paths:
		var texture := _load_card_thumbnail(room_texture_paths[id])
		if texture != null:
			card_textures[id] = texture

func _load_card_thumbnail(path: String) -> Texture2D:
	return preload("res://scripts/safe_image.gd").raw_texture(path)

func _default_card_rotation(id: String) -> int:
	if id=="corner":
		return preload("res://rooms/underwater/corridor_geometry.gd").next_corner_rotation(placed_rooms,drone_fleet.orders)
	return int(RoomDatabaseScript.get_room(id).get("fixed_rotation",0)) if not id.is_empty() else 0

func _on_card_pressed(id: String) -> void:
	if _gameplay_input_blocked() or not running:
		return
	_clear_prototype_marker(id)
	selected_card_id = id
	play_station_sound("ui_select")
	last_preview_room_id = id
	last_previewing_card = true
	selected_rotation = _default_card_rotation(id)
	_refresh_cards()
	_refresh_inspector()

func _on_card_hovered(id: String, card: Control) -> void:
	if _gameplay_input_blocked() or not running:
		return
	if not is_instance_valid(card) or not card is PanelContainer:
		return
	card.pivot_offset = card.size * 0.5
	var rest_position: Vector2 = card.get_meta("rest_position", card.position)
	card.position = rest_position if Preferences.reduced_motion else rest_position + Vector2(0, -14)
	card.scale = Vector2.ONE if Preferences.reduced_motion else Vector2(1.02, 1.02)
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
	selected_rotation = _default_card_rotation(selected_card_id)
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
	selected_rotation = _default_card_rotation(selected_card_id)
	_log("Draft hand rerolled. %d charge%s remain." % [rerolls_remaining, "s" if rerolls_remaining != 1 else ""], false)
	_refresh_all()

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode==KEY_F8:
		preload("res://scripts/room_layout_editor.gd").open(self)
		get_viewport().set_input_as_handled()
		return
	if menu_archive != null:
		return
	if event is InputEventKey and event.pressed and not event.echo and event.ctrl_pressed and event.keycode==KEY_F and not _gameplay_input_blocked():
		_open_station_search()
		get_viewport().set_input_as_handled()
		return
	if _journal_is_open() and event is InputEventKey and event.pressed and not event.echo:
		if event.ctrl_pressed and event.keycode == KEY_F:
			journal_tabs.current_tab = 3 if journal_tabs.current_tab==3 else 4
			history_search.grab_focus()
			history_search.select_all()
			get_viewport().set_input_as_handled()
			return
		if event.keycode == KEY_ESCAPE and history_search.has_focus() and not history_search.text.is_empty():
			history_search.text = ""
			_refresh_archive()
			archive_label.get_v_scroll_bar().set_deferred("value", 0.0)
			get_viewport().set_input_as_handled()
			return
	var scope: Node = null
	if menu_open:
		scope = menu_center
	elif summary_layer != null and summary_layer.visible:
		scope = summary_layer
	elif doctrine_layer != null and doctrine_layer.visible:
		scope = doctrine_layer
	elif _journal_is_open():
		scope = journal_layer
	if scope != null:
		preload("res://scripts/title_button_style.gd").contain_tab(event, scope)

func _unhandled_input(event: InputEvent) -> void:
	if is_instance_valid(menu_archive):
		return
	if doctrine_layer != null and doctrine_layer.visible:
		if event.is_action_pressed("ui_cancel"):
			_menu_return_title()
			get_viewport().set_input_as_handled()
		return
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		if _journal_is_open():
			_toggle_journal()
		elif summary_layer.visible:
			_menu_return_title()
		elif menu_open and pause_page != "main":
			_pause_page_back()
		else:
			_toggle_menu()
		get_viewport().set_input_as_handled()
		return
	if Preferences.pressed(event, "Journal"):
		_toggle_journal()
		get_viewport().set_input_as_handled()
		return
	if _gameplay_input_blocked():
		return
	if Preferences.pressed(event, "Placement guides"):
		Preferences.placement_guides = not Preferences.placement_guides
		Preferences.save(get_window())
		grid_view.queue_redraw()
		_refresh_placement_status()
		get_viewport().set_input_as_handled()
		return
	if Preferences.pressed(event, "Fit station"):
		_fit_station_view()
		get_viewport().set_input_as_handled()
		return
	if Preferences.pressed(event, "Pause"):
		_toggle_pause()
		get_viewport().set_input_as_handled()
		return
	if Preferences.pressed(event, "Rotate blueprint"):
		_rotate_selected_room()
		get_viewport().set_input_as_handled()
		return
	if Preferences.pressed(event, "Admin view") and OS.is_debug_build():
		admin_mode = not admin_mode
		_log("Admin topology overlay %s." % ("enabled" if admin_mode else "hidden"), false)
		_refresh_all()
		get_viewport().set_input_as_handled()
		return
	if event is InputEventMouseButton and event.pressed and event.shift_pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			_request_grid_zoom((camera_zoom_target if camera_zoom_target>=0 else grid_zoom) + Preferences.zoom_step())
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			_request_grid_zoom((camera_zoom_target if camera_zoom_target>=0 else grid_zoom) - Preferences.zoom_step())

func _rotate_selected_room() -> void:
	if selected_card_id.is_empty():
		return
	var blueprint:=RoomDatabaseScript.get_room(selected_card_id)
	if blueprint.has("fixed_rotation"):
		selected_rotation=int(blueprint.fixed_rotation)
		_log("%s: fixed orientation; doors: %s." % [blueprint.display_name,_join_strings(get_room_doors(blueprint)," / ")],false)
		_refresh_all()
		return
	selected_rotation = (selected_rotation + 1) % 4
	_refresh_all()

func _doors_connect(new_id: String, room_rotation: int, offset: Vector2i, neighbor: Dictionary) -> bool:
	var new_side := _side_from_offset(offset)
	var neighbor_side := _opposite_side(new_side)
	return _room_doors(new_id, room_rotation).has(new_side) and _room_doors(neighbor["id"], int(neighbor.get("rotation", 0))).has(neighbor_side)

var room_door_cache: Dictionary = {}

func _room_doors(room_id: String, room_rotation: int) -> Array:
	# Blueprint ports are fixed. Avoid cloning a complete room definition for
	# every adjacency check in rendering, water, navigation and construction.
	var key := "%s:%d" % [room_id, room_rotation]
	if room_door_cache.has(key): return room_door_cache[key].duplicate()
	if room_id == "reactor":
		return ["north", "east", "south", "west"]
	var room := RoomDatabaseScript.get_room(room_id)
	var layout := RoomDatabaseScript.get_layout(room.get("layout", "cross"))
	var doors: Array = layout.get("doors", [])
	var rotated := []
	for door in doors:
		rotated.append(_rotate_side(str(door), room_rotation))
	room_door_cache[key] = rotated
	return rotated.duplicate()

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
	if grid_view == null:
		return
	preload("res://scripts/room_flooding.gd").advance(self,delta)
	preload("res://scripts/crew_construction.gd").reconcile(self)
	var previous_status := _walker_status()
	var previous_veld_status := _veld_status()
	var previous_branforth_status := _branforth_status()
	for actor in [bill_npc, veld_npc, branforth_npc, marsh_npc]:
		var architect_id := "bill" if actor==bill_npc else "veld" if actor==veld_npc else "marsh" if actor==marsh_npc else "branforth"
		if not Architects.present(self,architect_id): continue
		if not actor.expedition.is_empty():
			preload("res://scripts/crew_expedition.gd").advance(self,actor,delta)
			continue
		actor.avoidance_position = Vector2.INF
		actor.avoidance_positions.clear()
		for peer in Companions.all_actors(self):
			if peer != actor and peer.active: actor.avoidance_positions.append(peer.foot)
		if actor != bill_npc: actor.room_cache = bill_npc.room_cache
		preload("res://scripts/airlock_service.gd").check_service(self,actor)
		actor.hardware_doors_locked=hardware.doors
		actor.update(self, delta)
	Companions.advance(self,delta)
	if delta > 0:
		preload("res://scripts/crew_passage.gd").update(Companions.all_actors(self))
	if bill_npc.active:
		test_walker_previous_cell = test_walker_cell
		test_walker_cell = bill_npc.cell_at(bill_npc.foot)
		test_walker_next_cell = Vector2i(-1, -1)
		test_walker_state = bill_npc.animation_state()
		test_walker_direction = bill_npc.direction
		if _walker_status() != previous_status or _veld_status() != previous_veld_status or _branforth_status() != previous_branforth_status:
			_refresh_placement_status()

func has_dr_veld() -> bool:
	return veld_npc.active and (not veld_npc.expedition.is_empty() or occupied.has(veld_npc.cell_at(veld_npc.foot)))

func get_dr_veld_position() -> Vector2:
	return (veld_npc.foot / 384.0 - Vector2(0, 0.038)) * get_cell_size()

func _veld_status() -> String:
	return "%s | hunger %d / fatigue %d" % [veld_npc.activity, roundi(veld_npc.needs.hunger), roundi(veld_npc.needs.fatigue)]

func has_chief_branforth() -> bool:
	return branforth_npc.active and (not branforth_npc.expedition.is_empty() or occupied.has(branforth_npc.cell_at(branforth_npc.foot)))

func get_chief_branforth_position() -> Vector2:
	return (branforth_npc.foot / 384.0 - Vector2(0, 0.038)) * get_cell_size()

func _branforth_status() -> String:
	return "%s | hunger %d / fatigue %d" % [branforth_npc.activity, roundi(branforth_npc.needs.hunger), roundi(branforth_npc.needs.fatigue)]

func has_marsh() -> bool:
	return marsh_npc.active and (not marsh_npc.recharge_docked or marsh_npc.dead) and (not marsh_npc.expedition.is_empty() or occupied.has(marsh_npc.cell_at(marsh_npc.foot)))

func get_marsh_position() -> Vector2:
	return (marsh_npc.foot / 384.0 - Vector2(0, 0.038)) * get_cell_size()

func _marsh_status() -> String:
	return "%s | hunger %d / fatigue %d" % [marsh_npc.activity, roundi(marsh_npc.needs.hunger), roundi(marsh_npc.needs.fatigue)]

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
	if room.get("branch_owner",Vector2i(-1,-1))!=neighbor.get("branch_owner",Vector2i(-1,-1)):return false
	var side := _side_from_offset(offset)
	var opposite := _opposite_side(side)
	return get_room_doors(room).has(side) and get_room_doors(neighbor).has(opposite)

func get_test_walker_position() -> Vector2:
	if bill_npc.active:
		return (bill_npc.foot / 384.0 - Vector2(0, 0.038)) * get_cell_size()
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
	if bill_npc.active:
		return bill_npc.direction
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
	return not bill_npc.expedition.is_empty() or (occupied.has(test_walker_cell) and (architect_run.is_empty() or bill_npc.active))

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
		if i < count and occupied.get(cell, {}).get("id", "") == "gravity_loom":
			# The broad low ring needs a square perimeter, not diagonal chords.
			var next_index: int = (index + step + order.size()) % order.size()
			var directions := [Vector2.UP, Vector2.RIGHT, Vector2.DOWN, Vector2.LEFT]
			points.append(_cell_center(cell) + (directions[index] + directions[next_index]) * get_cell_size() * 0.30)
		if i < count and occupied.get(cell, {}).get("id", "") == "reactor":
			# The south-facing chamber needs a corner waypoint: a straight
			# diagonal between cardinal anchors clips its ground footprint once
			# the rendered crew foot offset is included.
			var next_index: int = (index + step + order.size()) % order.size()
			var directions := [Vector2.UP, Vector2.RIGHT, Vector2.DOWN, Vector2.LEFT]
			points.append(_cell_center(cell) + (directions[index] + directions[next_index]) * get_cell_size() * 0.20)
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

func _refresh_harvest_inspector(cell: Vector2i) -> void:
	var site: Dictionary = drone_fleet.sites[cell]
	preview_name_label.text = drone_fleet.Sites.NAMES[site.kind]
	preview_tags_label.text = "SURVEYED / FINITE RESOURCE / " + ("DEPLETED" if site.units==0 else "EXTRACTION")
	preview_texture.texture = grid_view.harvest_site_art.texture("mining" if site.kind=="mining" else "frame")
	var remaining := {}
	for key in drone_fleet.Sites.LOADS[site.kind]: remaining[key] = drone_fleet.Sites.LOADS[site.kind][key]*site.units
	var status := "WAITING FOR A REACHABLE DRONE"
	if site.units==0: status = "DEPLETED / footprint available for construction"
	elif not site.active: status = "EXTRACTION PAUSED / progress retained"
	elif not drone_fleet.has_worker(site.kind,placed_rooms): status = "REQUIRES " + ("MINING" if site.kind=="mining" else "SALVAGE") + " DRONE BAY"
	else:
		for drone in drone_fleet.drones.values():
			if drone.job=="harvest" and Vector2i(drone.target)==cell:
				status = drone_fleet.battery_status(drone.home,int(resources.power),powered_room_cells.has(drone.home),paused)
				break
	inspector_label.text = "%s\n\nRemaining: %s\nLoads: %d / %d\nCurrent load: %d%%\n\nDrones choose the nearest reachable surveyed site. Extraction stops when its material is gone. Cargo enters storage at the bay; storage limits apply. Expand the station to survey farther seabed.\n\n[color=#698782]I have counted what remains. It is not an inexhaustible number.[/color]" % [status,_format_cost(remaining),site.units,site.capacity,roundi(site.progress/6.0*100)]
	room_operation_button.set_meta("cell",cell)
	room_operation_button.disabled = not running or site.units==0
	room_operation_button.text = "DEPOSIT EXHAUSTED" if site.units==0 else "PAUSE EXTRACTION" if site.active else "RESUME EXTRACTION"
	room_operation_button.tooltip_text = "Pause this target without losing extracted material or partial work."

var inspector_had_water := false

func _refresh_inspector() -> void:
	if inspector_label == null: return
	var inspected: Dictionary = occupied.get(selected_room_cell,{})
	inspector_had_water = float(inspected.get("water_level",0))>0 or float(inspected.get("hull_crack",0))>0
	hovered_card_id = "" # Discard legacy checkpoint hover state; inspection is click-based.
	var key := "%s:%s" % [selected_card_id,selected_room_cell]
	var scroll_value: float = inspector_label.get_v_scroll_bar().value if key == inspector_selection_key else 0.0
	inspector_selection_key = key
	_refresh_inspector_contents()
	inspector_label.get_v_scroll_bar().set_deferred("value",scroll_value)

func _refresh_inspector_contents() -> void:
	inspector_focus_button.disabled = true
	if hovered_card_id.is_empty() and selected_card_id.is_empty():
		var site_cell: Vector2i = selected_room_cell
		if drone_fleet.sites.has(site_cell) and drone_fleet.sites[site_cell].discovered and not occupied.has(site_cell):
			_refresh_harvest_inspector(site_cell)
			return
	if hovered_card_id.is_empty() and selected_card_id.is_empty():
		var order_cell: Vector2i = selected_room_cell
		var order: Dictionary = drone_fleet.order_at(order_cell)
		if not order.is_empty():
			var blueprint := RoomDatabaseScript.get_room(order.id)
			preview_name_label.text = blueprint.display_name
			preview_texture.texture = card_textures.get(order.id)
			preview_tags_label.text = "CONSTRUCTION / MATERIALS PAID"
			var build_status: String=drone_fleet.construction_status(order_cell,_simulate_room_economy().working_cells)
			if order.has("builder"):
				var builder=get(str(order.builder)+"_npc")
				if builder.state!="weld": build_status=Architects.NAMES[order.builder]+" / "+str(builder.activity)
			if paused: build_status="PAUSED / "+build_status
			inspector_label.text = build_status+"\n\nMaterials reserved. The connecting seal stays closed until assembly finishes.\n\nAn available architect builds from inside the station. Powered Construction Drone Bays take unassigned jobs."
			room_operation_button.text = "CONSTRUCTION IN PROGRESS"
			room_operation_button.disabled = true
			return
	if hovered_card_id.is_empty() and selected_card_id.is_empty():
		var wreck_cell := selected_room_cell
		if not occupied.has(wreck_cell) and WreckField.blocks(wrecks,wreck_cell):
			_refresh_wreck_inspector(wreck_cell)
			return
	var room := {}
	var previewing_card := false
	if not hovered_card_id.is_empty():
		room = RoomDatabaseScript.get_room(hovered_card_id)
		previewing_card = true
	elif not selected_card_id.is_empty():
		room = RoomDatabaseScript.get_room(selected_card_id)
		previewing_card = true
	elif occupied.has(selected_room_cell):
		room = occupied[selected_room_cell]
	if room.is_empty() and not last_preview_room_id.is_empty():
		room = RoomDatabaseScript.get_room(last_preview_room_id)
		previewing_card = last_previewing_card
	if not previewing_card and room.has("pos") and Companions.is_site(self,room.pos):
		Companions.inspect(self,room.pos);return
	if not previewing_card and room.get("recovered_derelict",false):
		_refresh_cryo_inspector(room.pos)
		return
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
			"[color=#70848a]Click a room, construction site or blueprint to inspect it.[/color]",
			"[color=#70848a]Station integrity:[/color] [color=#c9d3ce]%d%%[/color]" % resources["integrity"],
			"",
			_preview_divider(),
			"",
			"[color=#34484b]BRINE waits beneath the water. Select a module to read its pattern.[/color]",
			"",
			_preview_divider()
		], "\n")
		return
	preview_texture.texture = card_textures.get(room["id"])
	preview_name_label.text = room["display_name"]
	preview_name_label.add_theme_color_override("font_color", UI_ACCENT_BRIGHT)
	preview_tags_label.text = "CLASS: %s     %s" % [str(room.get("category", "")).to_upper(), str(room.get("rarity", "")).to_upper()]
	preview_tags_label.add_theme_color_override("font_color", Color("#95a7a0"))
	var preview_lines: Array[String] = []
	if previewing_card:
		preview_lines.append("[b]Build cost:[/b] " + _format_cost(room.get("cost",{})))
		var shortfall := _missing_cost(room.get("cost",{}))
		preview_lines.append("[color=#eaa88b]Need " + _format_cost(shortfall) + " more[/color]" if not shortfall.is_empty() and not testing_free_build else "[color=#abd2b5]Materials available[/color]")
		preview_lines.append("[b]" + ("Cargo per load: " if room.id in ["mining_drone_bay","salvage_drone_bay"] else "Output / cycle: ") + "[/b]" + (_format_cost(room.production) if not room.get("production",{}).is_empty() else "None"))
		preview_lines.append("[b]Inputs / cycle:[/b] " + (_format_cost(room.consumption) if not room.get("consumption",{}).is_empty() else "None"))
		if room.has("fixed_rotation"): preview_lines.append("Fixed orientation. Doors: " + _join_strings(get_room_doors(room)," / "))
	if not previewing_card and room.has("pos"):
		var operation := str(offline_reasons.get(room["pos"], "FUNCTIONING" if powered_room_cells.has(room["pos"]) else "AWAITING CYCLE"))
		preview_lines.append("[color=#f0c67a]CURRENT STATUS // %s[/color]" % operation)
		preview_lines.append(preload("res://scripts/station_ui_insights.gd").remedy(operation))
		var forecast := _simulate_room_economy(true, cycle + 1)
		preview_lines.append("[color=#9fdfdc]NEXT CYCLE FORECAST // %s[/color]" % str(forecast.offline.get(room.pos, "INPUTS AVAILABLE")))
		var next_reason := str(forecast.offline.get(room.pos,""))
		if not next_reason.is_empty() and next_reason != operation:
			preview_lines.append(preload("res://scripts/station_ui_insights.gd").remedy(next_reason))
		preview_lines.append(preload("res://scripts/station_navigation.gd").actions(room.pos,next_reason if not next_reason.is_empty() else operation))
		if room.id in ["construction_drone_bay","mining_drone_bay","salvage_drone_bay","brine_core"]:
			preview_lines.append(preload("res://scripts/station_ui_insights.gd").power_demand(self))
		preview_lines.append("Forecast uses current shared inputs and learned bonuses; events can change the outcome.")
	if not previewing_card:
		preview_lines.append(_preview_divider())
		preview_lines.append("[color=#%s]%s[/color]" % [UI_ACCENT_BRIGHT.to_html(false),"CARGO / EXTRACTION LOAD" if room.id in ["mining_drone_bay","salvage_drone_bay"] else "BASE OUTPUT / FUNCTIONING CYCLE"])
		preview_lines.append(_format_effect_rows(room.get("production", {}), "+", false,room.id not in ["mining_drone_bay","salvage_drone_bay"]))
	if room.id in ["mining_drone_bay","salvage_drone_bay"]:
		preview_lines.append(drone_fleet.battery_status(room.get("pos",Vector2i(-1,-1)),int(resources.power),powered_room_cells.has(room.get("pos",Vector2i(-1,-1))),paused))
		preview_lines.append("Extracts one load per 6 seconds from a finite surveyed site. Cargo enters storage on return. Battery supports 12 seconds of extraction; 1 station Power restores 6 seconds at the bay. Keep an exterior route open.")
	if not previewing_card and not room.get("consumption", {}).is_empty():
		preview_lines.append("[color=#c85b61]REQUIRED INPUT / CYCLE[/color]")
		preview_lines.append(_format_effect_rows(room.get("consumption", {}), "-", true))
	if not room.get("storage", {}).is_empty():
		preview_lines.append("[color=#7f929c]STORAGE[/color]")
		preview_lines.append("[color=#9fb2bc]%s[/color]" % _format_storage(room.get("storage", {})))
	preview_lines.append(_preview_divider())
	preview_lines.append("[b]Room details[/b]\n" + str(room.get("description","")))
	_append_room_synergy_preview(preview_lines, room)
	preview_lines.append(_preview_divider())
	preview_lines.append("[color=#596d77]%s[/color]" % _room_flavor_line(room))
	if not previewing_card and room.get("id","")=="listening_post":preview_lines.append(preload("res://scripts/listening_post.gd").inspector(self,room))
	if not previewing_card and room.get("id","") in ["pressure_control","isolation_vault"]:preview_lines.append(preload("res://scripts/rare_branch_control.gd").inspector(self,room))
	if not previewing_card and room.get("local_incident",false) and float(room.get("hull_crack",0))<=0:preview_lines.append("[color=#e6aa72]LOCAL CONTAINMENT FAULT[/color]\n[url=repair:%d:%d]Repair containment — 2 Metal[/url]" % [room.pos.x,room.pos.y])
	if room.get("tags",[]).has("containment_risk"):preview_lines.append("Containment fault risk: a functioning risk room can develop a local fault every 8 cycles. Uncontained faults spread through connected doors and damage Integrity. Repair costs 2 Metal per room.")
	if not previewing_card: preview_lines.push_front(preload("res://scripts/room_flooding.gd").inspector(self,room))
	inspector_label.text = _join_strings(preview_lines, "\n")
	inspector_focus_button.disabled = previewing_card or not room.has("pos")
	inspector_focus_button.set_meta("cell", room.get("pos", Vector2i(-1, -1)))

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
		lines.append("[color=#9aafb9]No recovered patterns for this room yet.[/color]")
	for synergy in relevant:
		if room.has("pos"):
			var local_count := 0
			var connected_here := false
			for link in connected_synergy_links:
				if link.id == synergy.id and link.get("cells", []).has(room.pos):
					connected_here = true
			for link in active_synergy_links:
				if link.id == synergy.id and link.get("cells", []).has(room.pos):
					local_count += 1
			lines.append("[color=#9fdfdc]%s[/color]" % ("FUNCTIONING AT THIS ROOM" if local_count > 0 else ("CONNECTED HERE · CHECK BOTH PARTNERS' INPUTS" if connected_here else "NOT CONNECTED HERE · MATCH THE PARTNER'S DOORS")))
			lines.append("[color=#8fa3ae]Station-wide pattern record:[/color]")
		lines.append(_format_synergy_line(synergy))
	if unknown_count > 0:
		lines.append("[color=#9aafb9]UNKNOWN PATTERNS REMAIN: %d[/color]" % unknown_count)
		lines.append("[color=#9aafb9]Power experimental configurations to recover them.[/color]")

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
		return "[color=#adbdc6]None[/color]"
	var rows: Array[String] = []
	for key in values:
		var id := str(key)
		var amount := int(values[key])
		var prefix_text := prefix
		if prefix_text.is_empty() and amount > 0:
			prefix_text = "+"
		var value_color := "#d9e6ec"
		if negative:
			value_color = "#e38d92"
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
		rows.append("%s     [color=%s]%s%d[/color] [color=#8d9ba2]%s[/color]   [color=#adbdc6]%s[/color]" % [
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
	if journal_button != null:
		journal_button.text = "JOURNAL [%s]\n%d LEARNED" % [Preferences.key_name("Journal"), meta.discovered_synergy_ids.size()]
	if journal_tabs != null:
		history_search.visible = journal_tabs.current_tab in [3,4]
		history_tools.visible = journal_tabs.current_tab in [3,4]
		history_filter.visible = journal_tabs.current_tab == 3
		history_search.placeholder_text = "Search name, type or problem (e.g. needs power) · Enter to locate" if journal_tabs.current_tab==4 else "Search room, cycle (C03), or message · Ctrl+F"
		if journal_tabs.current_tab > 0:
			_refresh_diagnostics_page()
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
	lines.append_array(preload("res://scripts/station_ui_insights.gd").learning(self))
	lines.push_front("[color=#a9e7d4]%d LEARNED  /  %d STABILIZED  /  %d BLUEPRINTS AVAILABLE[/color]\n" % [discovered_count, stabilized_count, meta.unlocked_room_ids.size()])
	if discovered_count == 0:
		lines.append("[color=#a7bac1]An empty record, a station full of possibilities.\n\nConnect different rooms through matching doors. Let them function.\nWatch the rooms themselves for the first sign of a discovery.\n\nStabilized blueprints stay with you across reboots, and a new prototype\nis placed on top of your current draw pile.[/color]\n")
	var unknown_count := SynergyManagerScript.all_synergies().size() - discovered_count
	if unknown_count > 0:
		lines.append("[color=#718a97]UNKNOWN PATTERNS REMAIN: %d[/color]" % unknown_count)
	_set_journal_text(_join_strings(lines, "\n"))
	if journal_button != null:
		journal_button.text = "JOURNAL [%s]\n%d LEARNED" % [Preferences.key_name("Journal"), discovered_count]

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
	lines.append(preload("res://scripts/station_ui_insights.gd").power_demand(self))
	routing_label.text = _join_strings(lines, "\n")

func _refresh_placement_status() -> void:
	if is_instance_valid(placement_feedback): placement_feedback.visible = not selected_card_id.is_empty() and not _gameplay_input_blocked()
	if selected_card_id.is_empty():
		placement_label.tooltip_text = ""
		placement_label.text = "■ %s     VIEW: %s\nMajor Bill: %s" % ["HALTED" if paused else "RUNNING", "ADMIN" if admin_mode else "NORMAL", _walker_status()]
		if has_dr_veld(): placement_label.text += "\nDr. Veld: " + _veld_status()
		if has_chief_branforth(): placement_label.text += "\nChief Branforth: " + _branforth_status()
		return
	var room := RoomDatabaseScript.get_room(selected_card_id)
	var problem := get_placement_problem(selected_card_id, hover_cell)
	var doors := _room_doors(selected_card_id, selected_rotation)
	if problem.is_empty():
		placement_label.text = "PLACING: %s\nDoors: %s     %s rotates blueprint" % [room["display_name"], _join_strings(doors), Preferences.key_name("Rotate blueprint")]
	else:
		placement_label.text = "BLOCKED: %s\n%s" % [room["display_name"], problem]
	if selected_card_id == "current_turbine":
		var turbine_preview := {"pos":hover_cell,"rotation":selected_rotation}
		var intake_names := ["NORTH","EAST","SOUTH","WEST"]
		placement_label.text += "\nINTAKE %s: %s" % [intake_names[posmod(selected_rotation,4)], "CLEAR" if _turbine_intake_clear(turbine_preview) else "BLOCKED — NO POWER"]
	placement_label.text += "\n" + _placement_connections(selected_card_id, hover_cell)
	placement_label.tooltip_text = _blueprint_decision(room)
	if is_instance_valid(placement_feedback):
		placement_feedback.text = placement_label.text.replace("PLACING:","READY TO BUILD:")
		placement_feedback.add_theme_color_override("font_color",Color("d5e5dc") if problem.is_empty() else Color("f0bd99"))

func _position_placement_feedback() -> void:
	if not is_instance_valid(grid_scroll) or not is_instance_valid(grid_view): return
	var area := grid_scroll.get_global_rect().grow(-8)
	placement_feedback.size.x = minf(440,area.size.x)
	var point := grid_view.get_global_transform() * (Vector2(hover_cell + Vector2i.RIGHT) * get_cell_size())
	point += Vector2(12,8)
	point.x = clampf(point.x,area.position.x,maxf(area.position.x,area.end.x-placement_feedback.size.x))
	point.y = clampf(point.y,area.position.y,maxf(area.position.y,area.end.y-placement_feedback.size.y))
	placement_feedback.global_position = point

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

func _reserve_forecast(key: String, change: int) -> String:
	var reserve := int(resources.get(key, 0))
	var outlook := "No depletion at this rate"
	if reserve <= 0:
		outlook = "Reserve currently empty"
	if change < 0:
		outlook = "~%d cycles to empty at this rate" % ceili(float(maxi(reserve, 0)) / -change)
	var next := clampi(reserve + change, 0, _get_resource_capacity(key))
	return "%s: %d stored · %+d / cycle · next reserve %d\n%s" % [key.replace("_", " ").capitalize(), reserve, change, next, outlook]

func _blueprint_decision(room: Dictionary) -> String:
	var missing := _missing_cost(room.get("cost", {}))
	var affordability := "Build cost available" if missing.is_empty() else "Short: " + _format_cost(missing)
	if room.id in ["mining_drone_bay","salvage_drone_bay"]:
		return "%s\nCargo per extracted load: %s\nRequires a surveyed finite deposit and exterior route. Bay upkeep: 1 Power/cycle; battery recharge uses additional stored Power." % [affordability,_format_cost(room.production)]
	return "%s\nRequired each functioning cycle: %s\nBase output each functioning cycle: %s\nShared inputs determine operation. Select to inspect learned patterns." % [affordability, _format_cost(room.get("consumption", {})), _format_cost(room.get("production", {}))]

func _placement_connections(room_id: String, cell: Vector2i) -> String:
	var matches := 0
	var mismatches := 0
	var learned: Array[String] = []
	for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
		var neighbor_cell: Vector2i = cell + offset
		if not occupied.has(neighbor_cell):
			continue
		var neighbor: Dictionary = occupied[neighbor_cell]
		if not _doors_connect(room_id, selected_rotation, offset, neighbor):
			mismatches += 1
			continue
		matches += 1
		for recipe in SynergyManagerScript.all_synergies():
			if not meta.discovered_synergy_ids.has(recipe.id):
				continue
			var partners: Array = recipe.get("rooms", [])
			if partners.size() == 2 and room_id != str(neighbor.id) and partners.has(room_id) and partners.has(neighbor.id) and not learned.has(str(recipe.name)):
				learned.append(str(recipe.name))
	var result := "%d door matches · %d unmatched neighbors" % [matches, mismatches]
	if not learned.is_empty():
		result += "\nKnown links: " + ", ".join(learned) + " · requires both rooms functioning"
	return result

func _inspector_action(value: Variant) -> void:
	var link := str(value)
	if link.begins_with("floodcancel:") or link.begins_with("floodassign:"):
		var parts := link.split(":")
		var cell := Vector2i(int(parts[1]),int(parts[2]))
		if parts[0]=="floodcancel": preload("res://scripts/hull_repair.gd").cancel(self,cell)
		elif parts.size()==4: preload("res://scripts/hull_repair.gd").reassign(self,cell,parts[3])
		_refresh_all()
	elif link.begins_with("floodrepair:"):
		var parts := link.split(":")
		var cell := Vector2i(int(parts[1]),int(parts[2]))
		preload("res://scripts/hull_repair.gd").request(self,cell)
		_refresh_all()
	elif link.begins_with("resource:"):
		_open_resource_details(link.trim_prefix("resource:"),inspector_focus_button)
	elif link.begins_with("resume:") or link.contains(","):
		_locate_diagnostic_room(value)
	else:
		_listening_action(value)

func _locate_diagnostic_room(value: Variant) -> void:
	if str(value)=="pet:margot":
		if Companions.can_pet(self,true):
			if _journal_is_open():_toggle_journal()
			Companions.pet_margot(self)
		return
	if str(value).begins_with("resource:"):
		inspected_resource = str(value).trim_prefix("resource:")
		journal_tabs.current_tab = 2
		_refresh_archive()
		return
	if str(value) == "all_resources":
		inspected_resource = ""
		_refresh_archive()
		archive_label.get_v_scroll_bar().set_deferred("value", 0.0)
		return
	var resume_room := str(value).begins_with("resume:")
	var parts := str(value).trim_prefix("resume:").split(",")
	if parts.size() != 2 or not parts[0].is_valid_int() or not parts[1].is_valid_int():
		return
	var cell := Vector2i(int(parts[0]), int(parts[1]))
	if not occupied.has(cell) and not drone_fleet.reserved(cell):
		return
	if _journal_is_open(): _toggle_journal()
	selected_card_id = ""
	hovered_card_id = ""
	selected_room_cell = cell
	hover_cell = cell
	_refresh_inspector()
	inspector_focus_button.set_meta("cell", cell)
	_focus_inspected_room()
	if resume_room and occupied.has(cell) and occupied[cell].get("suspended",false): _toggle_inspected_room()

func _open_resource_details(resource_id: String, opener: Control) -> void:
	if _gameplay_input_blocked() or (not BASE_STORAGE_CAPACITY.has(resource_id) and resource_id!="crew"):
		return
	inspected_resource = "" if resource_id=="crew" else resource_id
	opener.grab_focus()
	_toggle_journal()
	journal_tabs.current_tab = 5 if resource_id=="crew" else 2
	_refresh_archive()
	archive_label.get_v_scroll_bar().set_deferred("value", 0.0)

func _resource_contribution_lines(resource_id: String, forecast: Dictionary) -> Array[String]:
	var lines: Array[String] = ["\n[b]ROOM CONTRIBUTIONS // BASE RATES[/b]"]
	for room in placed_rooms:
		var produced := int(room.get("production", {}).get(resource_id, 0))
		var consumed := int(room.get("consumption", {}).get(resource_id, 0))
		if resource_id=="power" and room.id=="heat_recovery":
			var cell: Vector2i=room.pos
			lines.append("[url=%d,%d]%s · %s[/url]\nReclaims 2 per adjacent active Reactor, capped at 4.\nForecast: +%d Power · %s\n" % [cell.x,cell.y,room.display_name,cell,int(forecast.get("generator_outputs",{}).get(cell,0)),forecast.offline.get(cell,"INPUTS AVAILABLE")])
			continue
		if produced == 0 and consumed == 0:
			continue
		var cell: Vector2i = room.pos
		var status: String = str(forecast.offline.get(cell, "INPUTS AVAILABLE"))
		lines.append("[url=%d,%d]%s · %s[/url]\nBase output +%d · required input %d / cycle\nForecast: %s\n" % [cell.x, cell.y, room.display_name, cell, produced, consumed, status])
	if lines.size() == 1:
		lines.append("No installed rooms have base rates for this resource.")
	if resource_id in ["food", "oxygen"]:
		lines.append("Projected crew upkeep: %d / cycle" % ((_breathing_crew_count() if resource_id=="oxygen" else crew_count) + int(forecast.added_crew)))
	lines.append("Base rates describe each room, not a second net forecast. Operation, learned bonuses, special effects and storage limits are reflected in the reserve estimate above.")
	return lines

func _journal_tab_changed(index: int) -> void:
	if archive_label == null:
		return
	journal_scroll_positions[journal_last_tab] = archive_label.get_v_scroll_bar().value
	if journal_last_tab in [3,4]: journal_searches[journal_last_tab] = history_search.text
	journal_last_tab = index
	history_search.set_block_signals(true)
	history_search.text = str(journal_searches.get(index,""))
	history_search.set_block_signals(false)
	_refresh_archive()
	archive_label.get_v_scroll_bar().set_deferred("value", float(journal_scroll_positions.get(index, 0.0)))

func _set_journal_text(value: String) -> void:
	if archive_label.text == value:
		return
	var position := archive_label.get_v_scroll_bar().value
	archive_label.text = value
	archive_label.get_v_scroll_bar().set_deferred("value", position)

func _history_matches_category(line: String) -> bool:
	var text := line.to_lower()
	match history_filter.selected:
		1:
			for token in ["warning", "shortage", "shortfall", "needs ", "collapse", "critical", "rejected", "run complete"]:
				if text.contains(token): return true
			return false
		2:
			return text.contains("pattern") or text.contains("blueprint decrypted") or text.contains("resonance tier")
		3:
			return text.contains("built ") or text.contains("cleared at") or text.contains("suspended") or text.contains("resume next cycle")
	return true

func _refresh_diagnostics_page() -> void:
	var lines: Array[String] = []
	match journal_tabs.current_tab:
		1:
			lines.append("[b]STATION HEALTH // NEXT CYCLE[/b]\nCurrent supplies and learned patterns. Select a room to locate it.\n")
			var forecast: Dictionary = _simulate_room_economy(true, cycle + 1)
			var priorities: Array[String] = preload("res://scripts/station_ui_insights.gd").priorities(self,forecast)
			if not priorities.is_empty():
				lines.append("[color=#efb777][b]FIRST PRIORITIES[/b]\n" + "\n\n".join(priorities) + "[/color]\n\nALL INTERRUPTIONS\n")
			var alerts := 0
			var ordered_rooms := placed_rooms.duplicate()
			ordered_rooms.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
				var a_held: bool = forecast.offline.get(a.pos, "") == "SUSPENDED"
				var b_held: bool = forecast.offline.get(b.pos, "") == "SUSPENDED"
				return not a_held if a_held != b_held else str(a.display_name) < str(b.display_name))
			for room in ordered_rooms:
				var cell: Vector2i = room.pos
				if not forecast.offline.has(cell):
					continue
				alerts += 1
				var reason: String = str(forecast.offline[cell])
				var remedy: String = preload("res://scripts/station_ui_insights.gd").remedy(reason)
				if reason == "SUSPENDED":
					remedy = "Select this room, then choose Resume Room. Operation is evaluated next cycle."
				lines.append("[url=%d,%d][color=#efb777]%s · %s[/color][/url]\nObserved: %s\nForecast: %s\n%s\n" % [cell.x, cell.y, room.display_name, cell, str(offline_reasons.get(cell, "FUNCTIONING" if powered_room_cells.has(cell) else "AWAITING CYCLE")), reason, remedy])
				lines.append(preload("res://scripts/station_navigation.gd").actions(cell,reason)+"\n")
			if alerts == 0:
				lines.append("No room interruptions forecast. A rare interval of competence.")
			lines.append("\nSUPPLY WATCH")
			var net := _project_cycle_delta()
			for key in net:
				if int(net[key]) < 0:
					lines.append(_reserve_forecast(str(key), int(net[key])))
		2:
			lines.append("[b]RESERVES // PROJECTED NEXT CYCLE[/b]\nIncludes crew upkeep and learned bonuses. Storage caps apply.\nEstimates only: events and changing inputs can alter these rates.\n")
			var forecast := _simulate_room_economy(true, cycle + 1)
			var net := _project_cycle_delta(forecast)
			if inspected_resource.is_empty() or inspected_resource == "power":
				lines.append("\n" + preload("res://scripts/station_ui_insights.gd").power_demand(self) + "\n")
			if not inspected_resource.is_empty():
				lines.append("[url=all_resources]SHOW ALL RESERVES[/url]\n")
				lines.append(_reserve_forecast(inspected_resource, int(net.get(inspected_resource, 0))))
				lines.append_array(_resource_contribution_lines(inspected_resource, forecast))
			else:
				for key in BASE_STORAGE_CAPACITY:
					lines.append(_reserve_forecast(str(key), int(net.get(key, 0))) + "\n")
			lines.append("Estimates hold current rates constant. Shared-input shortages, crew changes, events and undiscovered effects can change these rates. An empty reserve is not itself a prediction of the run's outcome.")
		3:
			lines.append("[b]EVENT HISTORY // LATEST FIRST[/b]\nLast 1,000 events from this loop; retained in checkpoints.\n")
			var query := history_search.text.strip_edges().to_lower()
			var found := 0
			for i in range(event_history.size() - 1, -1, -1):
				var line := str(event_history[i])
				if _history_matches_category(line) and (query.is_empty() or line.to_lower().contains(query)):
					lines.append(line.replace("[", "[lb]"))
					found += 1
			if found == 0:
				lines.append("No matching records. Clear the search and choose All events to inspect the full retained history.")
			lines.insert(1, "%d matching / %d retained · Escape clears the focused search" % [found, event_history.size()])
		4:
			var forecast := _simulate_room_economy(true, cycle + 1)
			var rooms: Array = preload("res://scripts/station_navigation.gd").rooms(self,history_search.text,forecast)
			lines.append("[b]INSTALLED ROOMS // %d OF %d[/b]\nSearch name, type or problem. Select a result to locate it.\n" % [rooms.size(),placed_rooms.size()])
			for room in rooms:
				var cell: Vector2i = room.pos
				var reason: String = str(forecast.offline.get(cell,"INPUTS AVAILABLE"))
				lines.append("[url=%d,%d]%s · %s[/url]\n%s · Forecast: %s\n%s\n" % [cell.x,cell.y,room.display_name,cell,room.category,reason,preload("res://scripts/station_navigation.gd").actions(cell,reason)])
			if rooms.is_empty(): lines.append("No installed rooms match. Try a room name, department or NEEDS resource.")
		5:
			lines.append("[b]COMPANIONS[/b] // Separate from architect berths")
			for id in Companions.IDS:
				lines.append("%s // %s"%[Companions.NAMES[id],companion_actors[id].activity if companion_roster.has(id) else "Unlocked for future selection" if meta.unlocked_companion_ids.has(id) else "Not yet recovered"])
				if companion_roster.has(id) and companion_actors[id].active:
					var companion_cell: Vector2i=companion_actors[id].cell_at(companion_actors[id].foot)
					lines.append("[url=%d,%d]LOCATE %s[/url]"%[companion_cell.x,companion_cell.y,Companions.NAMES[id].to_upper()])
					if id=="margot":lines.append("[url=pet:margot]PET MARGOT[/url]\n" if Companions.can_pet(self,true) else "Pet Margot // %s\n"%Companions.pet_refusal(self))
			lines.append("[b]CREW ROSTER // %d / %d BERTHS[/b]\nRecovered occupants join after their wake sequence completes.\n" % [crew_count,_get_crew_capacity()])
			var named_alive := 0
			for member in recovered_crew:
				named_alive += int(member.alive)
				var origin_text := "Awakened in BRINE Core." if member.id=="core_architect" else ("Awakened in charging chamber %s." if member.get("architect_id","")=="marsh" else "Recovered from cryo ward %s.") % member.origin
				lines.append("[url=%d,%d]%s[/url] // %s\n%s\n" % [member.origin.x,member.origin.y,member.name,"ABOARD" if member.alive else "DECEASED",origin_text])
			for id in Architects.IDS:
				var actor = Architects.actor_for(self,id)
				if actor.active and not actor.dead: lines.append("Marsh: "+actor.battery_status()+"\n" if not actor.needs_air() else "%s: tank %.0fs / breath %.0fs / starvation %.0f of 90s\n" % [Architects.NAMES[id],actor.tank_oxygen,actor.breath_oxygen,actor.starvation])
			if recovered_crew.is_empty(): lines.append("No recovered survivors recorded. The sealed wards remain quiet.\n")
			if crew_count>named_alive: lines.append("Other station crew: %d\n" % (crew_count-named_alive))
			for cell in wrecks:
				var ward: Dictionary = wrecks[cell]
				if ward.kind not in ["cryo","charging"]: continue
				var waiting := 0
				for pod in ward.pods: waiting += int(not pod.recovered)
				lines.append("Ward %s // %d in stasis // %s" % [cell,waiting,CryoRecovery.status(self,cell)])
		6:
			lines.append("[b]CONSTRUCTION QUEUE[/b]\nSelect a paid order to locate its footprint. Closing this journal restores the previous pause state.\n")
			lines.append_array(preload("res://scripts/station_ui_insights.gd").construction(self))
	_set_journal_text("\n".join(lines))

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
	if bill_npc.active:
		return "%s | hunger %d / fatigue %d" % [bill_npc.activity, roundi(bill_npc.needs.hunger), roundi(bill_npc.needs.fatigue)]
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
	event_history.append("[C%02d] %s" % [cycle, message])
	if event_history.size() > 1000:
		event_history.pop_front()
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

func _refresh_construction_button() -> void:
	if not is_instance_valid(construction_button): return
	var count: int = drone_fleet.orders.size()
	var blocked := 0
	for drone in drone_fleet.drones.values():
		if drone.order.is_empty(): continue
		count += 1
		if not drone.bootstrap and not powered_room_cells.has(drone.home): blocked += 1
	var caption := "CONSTRUCTION / %d%s" % [count, " / %d OFFLINE" % blocked if blocked>0 else (" / PAUSED" if paused and count>0 else "")]
	if construction_button.text != caption: construction_button.text = caption
	construction_button.tooltip_text = "Paid orders, builder phases and blocked jobs. Select an order to locate its footprint."

func _minimum_map_zoom() -> float:
	if grid_scroll == null: return MIN_GRID_ZOOM
	return maxf(MIN_GRID_ZOOM, maxf(grid_scroll.size.x,grid_scroll.size.y) / (GRID_SIZE * float(CELL_SIZE)))

func _show_pause_page(id: String) -> void:
	if not pause_pages.has(id): return
	if id != "main": pause_page_opener = get_viewport().gui_get_focus_owner()
	pause_page = id
	for key in pause_pages: pause_pages[key].visible = key == id
	pause_page_title.text = {"main":"PAUSED", "station":"HELP & STATION", "exit":"LEAVE GAME"}[id]
	for child in pause_pages[id].get_children():
		if child is Button and child.visible and not child.disabled:
			child.grab_focus()
			break

func _pause_page_back() -> void:
	_show_pause_page("main")
	if is_instance_valid(pause_page_opener) and pause_page_opener.is_visible_in_tree():
		pause_page_opener.grab_focus()

func _listening_action(value: Variant) -> void:
	var parts:=str(value).split(":")
	if parts.size()==3 and parts[0]=="repair":
		preload("res://scripts/local_incidents.gd").repair(self,Vector2i(int(parts[1]),int(parts[2])))
		_refresh_all()
		return
	if parts.size()>=4 and parts[0]=="branch":
		var cell:=Vector2i(int(parts[1]),int(parts[2]))
		if not occupied.has(cell) or occupied[cell].id not in ["pressure_control","isolation_vault"]:return
		var control=preload("res://scripts/rare_branch_control.gd")
		if parts[3]=="select" and parts.size()==8:control.select(self,occupied[cell],Vector2i(int(parts[4]),int(parts[5])),Vector2i(int(parts[6]),int(parts[7])))
		elif parts[3]=="commit":
			if not control.commit(self,occupied[cell]):_log("Branch operation unavailable: check power, crew and current connections.",false)
		elif parts[3]=="release":control.release(self,occupied[cell])
		_refresh_all()
		return
	if parts.size()!=4 or parts[0]!="listen":return
	if preload("res://scripts/listening_post.gd").begin(self,Vector2i(int(parts[1]),int(parts[2])),parts[3]):
		_refresh_all()

func _open_station_search() -> void:
	if _gameplay_input_blocked(): return
	_toggle_journal()
	journal_tabs.current_tab = 4
	_refresh_archive()
	history_search.grab_focus()
	history_search.select_all()

func _fit_sidebar_inspector(scroll: ScrollContainer, side: VBoxContainer, panel: PanelContainer) -> void:
	# Keep time controls reachable while allowing the reading area to grow without the guide.
	var remaining := scroll.size.y
	for child in side.get_children():
		if child == panel or not child.visible: continue
		remaining -= child.get_combined_minimum_size().y + side.get_theme_constant("separation")
	var height := clampf(remaining, 360.0, 520.0)
	panel.custom_minimum_size.y = height
	inspector_label.custom_minimum_size.y = clampf(height - 190.0, 180.0, 330.0)

func _resize_grid_view() -> void:
	var previous_size := camera_viewport_size
	camera_viewport_size = grid_scroll.size
	if previous_size == Vector2.ZERO:
		_apply_grid_zoom.call_deferred()
		return
	var center := (Vector2(grid_scroll.scroll_horizontal, grid_scroll.scroll_vertical) + previous_size * 0.5) / (GRID_SIZE * get_cell_size())
	var revision := camera_view_revision
	await get_tree().process_frame
	# A deliberate fit or focus request takes precedence over automatic resize work.
	if revision == camera_view_revision: _set_grid_zoom(grid_zoom, true, center)

# Diagnostic capture is separate from the player's checkpoint write path.
func capture_bug_report_snapshot() -> Dictionary:
	if not startup_complete or get_meta("restoring_checkpoint",false):
		return {"status":"unavailable", "reason":"station initialization or restoration in progress"}
	for member in [bill_npc,veld_npc,branforth_npc,marsh_npc,grid_view,tick_timer]:
		if not is_instance_valid(member):
			return {"status":"unavailable", "reason":"station component unavailable"}
	return {"status":"captured", "snapshot":RunSave.capture(self)}
