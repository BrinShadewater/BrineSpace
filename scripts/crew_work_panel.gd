extends VBoxContainer
const Work=preload("res://scripts/crew_primary_work.gd")
const Architects=preload("res://scripts/architects.gd")
var game
var choice: OptionButton
var assign_button: Button
var info: Label
var clock := 0.0
func _ready():
	add_theme_constant_override("separation",6)
	assign_button=Button.new();game._style_hud_button(assign_button,false)
	assign_button.custom_minimum_size=Vector2(0,38)
	assign_button.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	assign_button.clip_text=false
	assign_button.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	assign_button.pressed.connect(func():
		var id: String=Architects.IDS[choice.selected]
		var actor=Architects.actor_for(game,id)
		Work.assign(game,id,Vector2i(-1,-1) if actor.primary_room==game.selected_room_cell else game.selected_room_cell)
		refresh())
	var action_row := HBoxContainer.new()
	action_row.add_theme_constant_override("separation", 10)
	add_child(action_row)
	action_row.add_child(assign_button)
	preload("res://scripts/ui_icons.gd").apply(assign_button, "assign_workplace")
	choice=OptionButton.new()
	for id in Architects.IDS:choice.add_item(Architects.NAMES[id])
	choice.custom_minimum_size=Vector2(0,38)
	choice.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	choice.item_selected.connect(func(_i):refresh())
	action_row.add_child(choice)
	info=Label.new();info.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;info.add_theme_font_size_override("font_size",14)
	var notes := preload("res://scripts/ui_widgets.gd").disclosure("WORKPLACE NOTES",info)
	notes.name = "WorkplaceNotes"
	notes.get_node("DisclosureHeader").set_meta("inspector_styled",true)
	add_child(notes)
	notes.get_node("DisclosureHeader").toggled.connect(func(open: bool):
		if open: refresh())
	refresh()
func _process(delta):
	clock+=delta
	if clock>=0.5:clock=0;refresh()
func refresh():
	if choice==null:return
	var cell: Vector2i=game.selected_room_cell
	visible=game.selected_card_id.is_empty() and game.hovered_card_id.is_empty() and game.occupied.has(cell) and game.occupied[cell].id not in ["corridor","corner","tee_corridor","moonbay"]
	if not visible:return
	for i in range(choice.item_count):choice.set_item_disabled(i,not Architects.present(game,Architects.IDS[i]))
	if choice.is_item_disabled(choice.selected):
		for i in range(choice.item_count):
			if not choice.is_item_disabled(i):choice.select(i);break
	var id: String=Architects.IDS[choice.selected]
	var actor=Architects.actor_for(game,id)
	var owner := ""
	for other in Architects.IDS:
		if other!=id and Architects.present(game,other) and not Architects.actor_for(game,other).dead and Architects.actor_for(game,other).primary_room==cell:owner=Architects.NAMES[other]
	assign_button.text="CLEAR PRIMARY JOB" if actor.primary_room==cell else "ASSIGN PRIMARY\nWORKPLACE"
	assign_button.disabled=not Architects.present(game,id) or actor.dead or not owner.is_empty()
	var hint := "Clear this crew member's current primary job." if actor.primary_room==cell else "Set this room as the selected crew member's primary workplace."
	if not Architects.present(game,id): hint = "Recover this crew member before assigning a workplace."
	elif actor.dead: hint = "This crew member is unavailable. Choose an active crew member."
	elif not owner.is_empty(): hint = "Assigned to %s. Select them and clear their primary job first." % owner
	preload("res://scripts/title_button_style.gd").set_hint(assign_button,hint)
	var key:=Work.reward(id,game.occupied[cell])
	var home: String=game.occupied.get(actor.primary_room,{}).get("display_name","Unassigned")
	info.text="PRIMARY JOB / %s\n%s\n%s" % [home,actor.activity,("Fit bonus: +1 %s per cycle while working here; fatigue rises 20%% slower." % key.capitalize()) if not key.is_empty() else "General posting / no specialty bonus."]
	if actor.needs_air():info.text+="\nHunger %d%% / fatigue %d%%. Meals and rest take priority at 65%%." % [roundi(actor.needs.hunger),roundi(actor.needs.fatigue)]
	else:info.text+="\nAndroid / returns to charging pod when battery is low."
	if not owner.is_empty():info.text+="\nWorkplace assigned to "+owner
	if actor.needs_air() and actor.needs.hunger>=65 and int(game.resources.food)<=0:info.text+="\nMeal unavailable / station Food depleted."
	# Route advice is only consumed by the expanded notes. Opening refreshes it immediately.
	if info.is_visible_in_tree() and actor.needs_air() and (actor.needs.hunger>=65 or actor.needs.fatigue>=65) and not Work.break_needed(game,actor):info.text+="\nNeeds waiting / provide reachable, operating meal and rest rooms."
