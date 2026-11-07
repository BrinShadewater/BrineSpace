extends VBoxContainer
## A visible recovery checklist independent of the room card/details disclosure.
const C=preload("res://scripts/companions.gd")
var game
var heading: Label
var steps: Array[Label]=[]
var status: Label
var next_link: RichTextLabel
func _ready()->void:
	add_theme_constant_override("separation",4)
	heading=Label.new();heading.add_theme_font_size_override("font_size",16);heading.add_theme_color_override("font_color",Color("a9e7d4"));add_child(heading)
	for i in range(4):
		var line:=Label.new();line.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;line.add_theme_font_size_override("font_size",16);add_child(line);steps.append(line)
	status=Label.new();status.name="RecoveryStatus";status.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;status.add_theme_font_size_override("font_size",16);add_child(status)
	next_link=RichTextLabel.new();next_link.name="NextRecovery";next_link.bbcode_enabled=true;next_link.fit_content=true;next_link.scroll_active=false
	next_link.add_theme_font_size_override("normal_font_size",16);next_link.add_theme_font_size_override("bold_font_size",16)
	next_link.meta_clicked.connect(func(value):game._locate_diagnostic_room(value));add_child(next_link)
	refresh()
func refresh()->void:
	if heading==null:return
	var cell: Vector2i=game.selected_room_cell
	visible=game.selected_card_id.is_empty() and game.hovered_card_id.is_empty() and C.surveyed_site(game,cell)
	if not visible:return
	var guidance:=C.recovery_guidance(game,cell)
	heading.text="RECOVERY COMPLETE" if guidance.complete else "RECOVERY / STEP %d OF 4"%guidance.step
	for i in range(4):
		var item: Dictionary=guidance.steps[i]
		steps[i].text="%s %d / %s"%["DONE" if item.done else "NOW" if item.current else "LATER",i+1,item.text]
		steps[i].add_theme_color_override("font_color",Color("a9e7d4") if item.current else Color("91a7a3") if item.done else Color("71858a"))
	status.text=guidance.detail
	next_link.visible=guidance.complete
	if guidance.complete:next_link.text=C.next_recovery_link(game,cell)
