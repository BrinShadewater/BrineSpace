extends CanvasLayer
## Root-owned overlay: gameplay can stay completely disabled during restoration.
var heading := "RESTORING STATION"
var message := "Verifying crew routes. The doors remember."
var detail: Label
func _ready() -> void:
	layer = 100
	process_mode = Node.PROCESS_MODE_ALWAYS
	var backdrop := ColorRect.new()
	backdrop.color = Color("07151f")
	var ui_theme := preload("res://scripts/title_button_style.gd").menu_theme()
	ui_theme.default_font_size = 16
	backdrop.theme = ui_theme
	backdrop.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(backdrop)
	backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var center := CenterContainer.new()
	backdrop.add_child(center)
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var column := VBoxContainer.new()
	column.custom_minimum_size.x = 460
	column.add_theme_constant_override("separation",24)
	center.add_child(column)
	var loading := preload("res://scripts/ui_widgets.gd").loading(heading,message,0)
	loading.name = "RestoreProgress"
	loading.add_theme_stylebox_override("panel",preload("res://scripts/ui_widgets.gd").surface("field","normal",18))
	column.add_child(loading)
	detail = loading.get_node("Body").get_child(1)
	var progress: ProgressBar = loading.get_node("Body/LoadingProgress")
	progress.indeterminate = true
	progress.visible = not preload("res://scripts/title_settings.gd").reduced_motion
	preload("res://scripts/title_settings.gd").apply_menu_text(column)
