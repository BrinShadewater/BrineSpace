extends HBoxContainer
## Compact crew vitals; selecting a portrait discloses live details to its right.
const Architects := preload("res://scripts/architects.gd")
const Buttons := preload("res://scripts/title_button_style.gd")
const Badges := preload("res://scripts/ui_badges.gd")
const Widgets := preload("res://scripts/ui_widgets.gd")
var game
var selected := ""
var portraits := HBoxContainer.new()
var details := PanelContainer.new()
var heading := Label.new()
var activity := Label.new()
var health := Label.new()
var room := Label.new()
var fatigue := ProgressBar.new()
var hunger := ProgressBar.new()
var health_meter := ProgressBar.new()
var oxygen := ProgressBar.new()
var compact_meters: Dictionary = {}
const VITAL_COLORS := {"HUNGER":"ddb569", "FATIGUE":"b199d8", "HEALTH":"85c79b", "OXYGEN":"7bc8e1"}
var status_badges := HFlowContainer.new()
var vital_badges := HFlowContainer.new()
var presence: Array = []
var clock := 0.0

func _ready() -> void:
	name = "CrewPortraitPanel"
	position = Vector2(18, 18)
	add_theme_constant_override("separation", 8)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(portraits)
	portraits.add_theme_constant_override("separation", 6)
	portraits.size_flags_vertical = Control.SIZE_SHRINK_BEGIN
	add_child(details)
	details.custom_minimum_size.x = 250
	details.add_theme_stylebox_override("panel", Buttons.panel_frame())
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 5)
	details.add_child(box)
	var title_row := HBoxContainer.new()
	box.add_child(title_row)
	heading.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	heading.add_theme_font_override("font", preload("res://scripts/ui_fonts.gd").interface_bold())
	title_row.add_child(heading)
	var close := Button.new()
	close.text = "‹"
	close.tooltip_text = "Collapse character details"
	close.pressed.connect(func(): selected = ""; refresh())
	Buttons.apply(close, 32, 28)
	title_row.add_child(close)
	for label in [activity, health, room]:
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		label.custom_minimum_size.x = 226
		label.add_theme_font_size_override("font_size", 14)
		box.add_child(label)
	health.hide()
	status_badges.name = "CrewStatusBadges"
	box.add_child(status_badges)
	vital_badges.name = "CrewVitalBadges"
	vital_badges.add_theme_constant_override("h_separation",6)
	vital_badges.add_theme_constant_override("v_separation",6)
	box.add_child(vital_badges)
	for pair in [["HUNGER", hunger], ["FATIGUE", fatigue], ["HEALTH", health_meter], ["OXYGEN", oxygen]]:
		var row := HBoxContainer.new()
		var caption := Label.new()
		caption.text = pair[0]
		caption.custom_minimum_size.x = 62
		caption.add_theme_font_size_override("font_size", 13)
		row.add_child(caption)
		var meter: ProgressBar = pair[1]
		style_meter(meter,str(pair[0]),false)
		row.add_child(meter)
		var value_label:=Label.new()
		value_label.custom_minimum_size.x=34
		value_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_RIGHT
		value_label.add_theme_font_size_override("font_size",13)
		value_label.add_theme_color_override("font_color",Color(VITAL_COLORS[pair[0]]))
		row.add_child(value_label)
		meter.set_meta("value_label",value_label)
		box.add_child(row)
	var focus := Button.new()
	focus.text = "FOCUS CHARACTER"
	focus.pressed.connect(func():
		if selected.is_empty(): return
		var actor = Architects.actor_for(game, selected)
		var center: Vector2 = actor.foot * game.get_cell_size() / 384.0
		game.grid_scroll.scroll_horizontal = maxi(0, int(center.x - game.grid_scroll.size.x * 0.5))
		game.grid_scroll.scroll_vertical = maxi(0, int(center.y - game.grid_scroll.size.y * 0.5))
		game.grid_view.queue_redraw())
	Buttons.apply(focus, 230, 32)
	box.add_child(focus)
	refresh()

func _process(delta: float) -> void:
	clock += delta
	if clock >= 0.25:
		clock = 0
		refresh()

func refresh() -> void:
	var ids: Array = []
	for id in Architects.IDS:
		if Architects.present(game, id): ids.append(id)
	if ids != presence:
		presence = ids
		for child in portraits.get_children(): child.free()
		compact_meters.clear()
		for id in ids:
			var button := Button.new()
			button.name = id.capitalize() + "Portrait"
			button.custom_minimum_size = Vector2(70, 72)
			button.size_flags_vertical = Control.SIZE_SHRINK_BEGIN
			button.tooltip_text = Architects.NAMES[id]
			button.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
			Buttons.apply(button, 70, 72)
			var portrait := TextureRect.new()
			portrait.texture = Architects.selection_portrait(id)
			portrait.mouse_filter = Control.MOUSE_FILTER_IGNORE
			portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
			portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
			button.add_child(portrait)
			portrait.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
			portrait.offset_left = 5; portrait.offset_top = 5
			portrait.offset_right = -5; portrait.offset_bottom = -5
			button.pressed.connect(func(): selected = "" if selected == id else id; refresh())
			var unit := HBoxContainer.new()
			unit.name = id.capitalize()+"Vitals"
			unit.add_theme_constant_override("separation",4)
			portraits.add_child(unit)
			unit.add_child(button)
			var meters := VBoxContainer.new()
			meters.add_theme_constant_override("separation",4)
			meters.size_flags_vertical=Control.SIZE_SHRINK_CENTER
			unit.add_child(meters)
			compact_meters[id]={}
			for vital in VITAL_COLORS:
				var row := HBoxContainer.new()
				row.add_theme_constant_override("separation",3)
				meters.add_child(row)
				var caption := Label.new()
				caption.text={"HUNGER":"HU","FATIGUE":"FA","HEALTH":"HE","OXYGEN":"O2"}[vital]
				caption.custom_minimum_size.x=17
				caption.add_theme_font_size_override("font_size",10)
				caption.add_theme_color_override("font_color",Color(VITAL_COLORS[vital]))
				row.add_child(caption)
				var meter:=ProgressBar.new()
				style_meter(meter,vital,true)
				row.add_child(meter)
				compact_meters[id][vital]=meter
	visible = not ids.is_empty()
	if not ids.has(selected): selected = ""
	details.visible = not selected.is_empty()
	for id in ids:
		var member = Architects.actor_for(game,id)
		var values:=vital_values(member)
		for vital in compact_meters[id]: update_meter(compact_meters[id][vital],vital,values[vital],member)
	if selected.is_empty(): return
	var actor = Architects.actor_for(game, selected)
	heading.text = str(Architects.NAMES[selected]).to_upper()
	heading.add_theme_font_size_override("font_size", 17)
	activity.text = "ACTIVITY  " + str(actor.activity)
	health.text = "STATUS  " + ("DECEASED" if actor.dead else "ALIVE")
	Badges.update(status_badges,[["DECEASED" if actor.dead else "ALIVE","warning" if actor.dead else "health","danger" if actor.dead else "online"],["ASSIGNED" if game.occupied.has(actor.primary_room) else "UNASSIGNED","assigned_room" if game.occupied.has(actor.primary_room) else "unassigned","normal" if game.occupied.has(actor.primary_room) else "warning"]])
	room.text = "ASSIGNED ROOM  " + str(game.occupied.get(actor.primary_room, {}).get("display_name", "Unassigned"))
	var values:=vital_values(actor)
	for pair in [["HUNGER",hunger],["FATIGUE",fatigue],["HEALTH",health_meter],["OXYGEN",oxygen]]:
		update_meter(pair[1],pair[0],values[pair[0]],actor)
	vital_badges.hide()

static func vital_values(actor) -> Dictionary:
	var air_capacity:=60.0 if actor.helmet_equipped else 15.0
	var air: float=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
	return {"HUNGER":float(actor.needs.get("hunger",0)),"FATIGUE":float(actor.needs.get("fatigue",0)),
		"HEALTH":0.0 if actor.dead else clampf(100.0*(1.0-float(actor.starvation)/90.0),0,100),
		"OXYGEN":0.0 if actor.dead else clampf(100.0*air/air_capacity,0,100)}

static func style_meter(meter: ProgressBar, vital: String, compact: bool) -> void:
	meter.name=vital.capitalize()+"Meter"
	meter.custom_minimum_size=Vector2(34,10) if compact else Vector2(110,18)
	meter.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	meter.show_percentage=false
	meter.add_theme_font_size_override("font_size",12)
	meter.add_theme_color_override("font_color",Color("eff6f8"))
	meter.add_theme_color_override("font_outline_color",Color("10212b"))
	meter.add_theme_constant_override("outline_size",1)
	meter.add_theme_stylebox_override("background",Widgets.track("081d23","414e54",3))
	meter.add_theme_stylebox_override("fill",Widgets.track(VITAL_COLORS[vital],VITAL_COLORS[vital],3))

static func update_meter(meter: ProgressBar,vital: String,value: float,actor) -> void:
	var applicable: bool=actor.needs_air() or vital not in ["HUNGER","OXYGEN"]
	meter.value=value if applicable else 0.0
	meter.modulate.a=1.0 if applicable else 0.35
	if meter.has_meta("value_label"):
		meter.get_meta("value_label").text="%d%%"%roundi(value) if applicable else "N/A"
	var detail: String={"HUNGER":"Higher means hungrier. Meals take priority at 65%.","FATIGUE":"Higher means more tired. Rest takes priority at 65%.","HEALTH":"Remaining survival reserve; falls during starvation and recovers when Food is available.","OXYGEN":"Remaining helmet air (60 seconds at base rate)." if actor.helmet_equipped else "Remaining breath (15 seconds at base rate)."}[vital]
	meter.tooltip_text="%s: %d%%\n%s" % [vital.capitalize(),roundi(value),detail] if applicable else vital.capitalize()+": not required by this character."
