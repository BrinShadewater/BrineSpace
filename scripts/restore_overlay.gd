extends CanvasLayer
## Root-owned overlay: gameplay can stay completely disabled during restoration.
func _ready() -> void:
	layer = 100
	process_mode = Node.PROCESS_MODE_ALWAYS
	var backdrop := ColorRect.new()
	backdrop.color = Color("07151f")
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Cascadia Mono","Consolas","Lucida Console"])
	var ui_theme := Theme.new()
	ui_theme.default_font = font
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
	var title := Label.new()
	title.text = "RESTORING STATION"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size",26)
	title.add_theme_color_override("font_color",Color("7ac4b5"))
	column.add_child(title)
	var detail := Label.new()
	detail.text = "Verifying crew routes. The doors remember."
	detail.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	column.add_child(detail)
	if not preload("res://scripts/title_settings.gd").reduced_motion:
		var progress := ProgressBar.new()
		progress.indeterminate = true
		progress.show_percentage = false
		progress.custom_minimum_size.y = 6
		column.add_child(progress)
	preload("res://scripts/title_settings.gd").apply_menu_text(column)
