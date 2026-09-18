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
	assign_button.custom_minimum_size=Vector2(240,34)
	assign_button.size_flags_horizontal=Control.SIZE_SHRINK_BEGIN
	assign_button.clip_text=false
	assign_button.autowrap_mode=TextServer.AUTOWRAP_OFF
	assign_button.pressed.connect(func():
		var id: String=Architects.IDS[choice.selected]
		var actor=Architects.actor_for(game,id)
		Work.assign(game,id,Vector2i(-1,-1) if actor.primary_room==game.selected_room_cell else game.selected_room_cell)
		refresh())
	add_child(assign_button)
	choice=OptionButton.new()
	for id in Architects.IDS:choice.add_item(Architects.NAMES[id])
	choice.custom_minimum_size=Vector2(240,32)
	choice.size_flags_horizontal=Control.SIZE_SHRINK_BEGIN
	choice.item_selected.connect(func(_i):refresh())
	add_child(choice)
	info=Label.new();info.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;info.add_theme_font_size_override("font_size",12);add_child(info)
	refresh()
func _process(delta):
	clock+=delta
	if clock>=0.5:clock=0;refresh()
func refresh():
	if choice==null:return
	var cell: Vector2i=game.selected_room_cell
	visible=game.selected_card_id.is_empty() and game.occupied.has(cell) and game.occupied[cell].id not in ["corridor","corner","tee_corridor"]
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
	assign_button.text="CLEAR PRIMARY JOB" if actor.primary_room==cell else "ASSIGN PRIMARY WORKPLACE"
	assign_button.disabled=not Architects.present(game,id) or actor.dead or not owner.is_empty()
	var key:=Work.reward(id,game.occupied[cell])
	var home: String=game.occupied.get(actor.primary_room,{}).get("display_name","Unassigned")
	info.text="PRIMARY JOB / %s\n%s\n%s" % [home,actor.activity,("Fit bonus: +1 %s per cycle while working here; fatigue rises 20%% slower." % key.capitalize()) if not key.is_empty() else "General posting / no specialty bonus."]
	if actor.needs_air():info.text+="\nHunger %d%% / fatigue %d%%. Meals and rest take priority at 65%%." % [roundi(actor.needs.hunger),roundi(actor.needs.fatigue)]
	else:info.text+="\nAndroid / returns to charging pod when battery is low."
	if not owner.is_empty():info.text+="\nWorkplace assigned to "+owner
	if actor.needs_air() and actor.needs.hunger>=65 and int(game.resources.food)<=0:info.text+="\nMeal unavailable / station Food depleted."
	if actor.needs_air() and (actor.needs.hunger>=65 or actor.needs.fatigue>=65) and not Work.break_needed(game,actor):info.text+="\nNeeds waiting / provide reachable, operating meal and rest rooms."
