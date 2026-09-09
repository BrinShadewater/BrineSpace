extends Control
const Architects = preload("res://scripts/architects.gd")
const Database = preload("res://scripts/room_database.gd")
var rooms: Array = []
var portrait: Texture2D
func configure(data: Dictionary) -> void:
	custom_minimum_size = Vector2(380,84)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	rooms.clear()
	portrait = null
	for room in data.get("state",{}).get("placed_rooms",[]):
		if room is Dictionary and room.get("pos") is Vector2i: rooms.append(room.duplicate(true))
	var identity: String = str(data.get("architects",{}).get("selected",""))
	if Architects.NAMES.has(identity): portrait = Architects.selection_portrait(identity)
	tooltip_text = "Saved station schematic. Only installed rooms are shown."
	queue_redraw()
static func summary(data: Dictionary) -> String:
	var state: Dictionary = data.get("state",{})
	var identity: String = str(data.get("architects",{}).get("selected",""))
	var warnings: Array[String] = []
	var resources: Dictionary = state.get("resources",{})
	var delta: Dictionary = state.get("last_cycle_delta",{})
	for key in ["oxygen","food","power"]:
		var amount := int(resources.get(key,0))
		if amount<=0: warnings.append("%s EMPTY" % key.to_upper())
		elif int(delta.get(key,0))<0 and amount+int(delta[key])<=0: warnings.append("%s LOW AT LAST RATE" % key.to_upper())
	return "CYCLE %03d · %d ROOMS\n%s\n%s" % [int(state.get("cycle",0)),state.get("placed_rooms",[]).size(),Architects.NAMES.get(identity,"Architect not recorded")," · ".join(warnings) if not warnings.is_empty() else "No critical reserve warning recorded"]
func _draw() -> void:
	draw_style_box(_panel(),Rect2(Vector2.ZERO,size))
	if rooms.is_empty(): return
	var bounds := Rect2(Vector2(rooms[0].pos),Vector2.ONE)
	for room in rooms: bounds = bounds.merge(Rect2(Vector2(room.pos),Vector2.ONE))
	var area := Rect2(8,8,size.x-88,size.y-16)
	var scale_value := minf(area.size.x/bounds.size.x,area.size.y/bounds.size.y)
	var origin := area.get_center()-bounds.size*scale_value*0.5
	for room in rooms:
		var rect := Rect2(origin+(Vector2(room.pos)-bounds.position)*scale_value,Vector2.ONE*scale_value).grow(-0.6)
		var color: Color = Database.category_color(str(room.get("category","Core")))
		draw_rect(rect,color.darkened(0.45))
		draw_rect(rect,color,false,1.0)
		if room.get("suspended",false): draw_line(rect.position,rect.end,Color("edab79"),1.0)
	if portrait: draw_texture_rect(portrait,Rect2(size.x-64,12,56,59.5),false)
func _panel() -> StyleBoxFlat:
	var panel := StyleBoxFlat.new()
	panel.bg_color = Color("0a1d25")
	panel.border_color = Color("345b6c")
	panel.set_border_width_all(1)
	return panel
