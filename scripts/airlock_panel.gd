extends VBoxContainer
const Service=preload("res://scripts/airlock_service.gd")
const Architects=preload("res://scripts/architects.gd")
var game
var choice: OptionButton
var action: Button
var status: Label
var elapsed:=0.0
var feedback_until:=0
var cycle_button: Button
var cycle_status: Label
const Cycle=preload("res://scripts/airlock_cycle.gd")
func _ready() -> void:
	choice=OptionButton.new()
	for id in Architects.IDS:
		choice.add_item(Architects.NAMES[id])
		choice.set_item_metadata(choice.item_count-1,id)
	add_child(choice)
	choice.item_selected.connect(func(_index): refresh())
	action=Button.new()
	action.custom_minimum_size.y=32
	game._style_hud_button(action,false)
	action.pressed.connect(func():
		if Service.request(game,str(choice.get_item_metadata(choice.selected)),game.selected_room_cell): refresh()
		else:
			feedback_until=Time.get_ticks_msec()+2500
			status.text="No clear locker route. Crew may be occupied."
	)
	add_child(action)
	status=Label.new()
	status.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	status.add_theme_font_size_override("font_size",12)
	add_child(status)
	cycle_button=Button.new()
	game._style_hud_button(cycle_button,false)
	cycle_button.pressed.connect(func():
		var cell: Vector2i=game.selected_room_cell
		if game.occupied.has(cell): Cycle.request(game,cell,Cycle.state(game.occupied[cell]).phase=="dry")
		refresh()
	)
	add_child(cycle_button)
	cycle_status=Label.new()
	cycle_status.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	cycle_status.add_theme_font_size_override("font_size",12)
	add_child(cycle_status)
	refresh()
func _process(delta: float) -> void:
	elapsed+=delta
	if elapsed>=0.25:
		elapsed=0
		refresh()
func refresh() -> void:
	if choice==null: return
	var cell: Vector2i=game.selected_room_cell
	visible=game.selected_card_id.is_empty() and game.occupied.has(cell) and game.occupied[cell].id=="airlock"
	# Keep the inspector's total height stable when its locker controls appear.
	game.inspector_label.custom_minimum_size.y=70 if visible else 210
	if not visible: return
	for i in range(choice.item_count): choice.set_item_disabled(i,not Architects.present(game,str(choice.get_item_metadata(i))))
	if choice.is_item_disabled(choice.selected):
		for i in range(choice.item_count):
			if not choice.is_item_disabled(i):
				choice.select(i)
				break
	var id:=str(choice.get_item_metadata(choice.selected))
	var actor=Architects.actor_for(game,id)
	var active_work: bool=actor.helmet_action_active() or not actor.locker_request.is_empty()
	action.text="RETURN DIVING HELMET" if actor.helmet_equipped else "FIT DIVING HELMET"
	action.disabled=not Service.ready(game,cell) or not Architects.present(game,id) or not actor.active or actor.dead or active_work or Service.busy(game,cell,actor) or actor.movement_medium!="dry" or not actor.stage.is_empty()
	if Time.get_ticks_msec()>=feedback_until:
		status.text=actor.activity if active_work else "Locker gear is reusable."
		if not Service.ready(game,cell): status.text="Lockers need a powered, active airlock."
	var room: Dictionary=game.occupied[cell]
	var pose:=Cycle.pose(room)
	cycle_button.text="FLOOD & OPEN OUTER HATCH" if pose.phase=="dry" else "CLOSE OUTER HATCH & DRAIN"
	cycle_button.disabled=not Service.ready(game,cell) or not pose.phase in ["dry","exterior"] or (pose.phase=="dry" and not Cycle.exterior_clear(game,room))
	cycle_status.text="%s\nWater %d%% / pressure %d%%" % [Cycle.LABELS[pose.phase],roundi(pose.water*100),roundi(pose.pressure*100)]
	if pose.phase=="dry" and not Cycle.exterior_clear(game,room): cycle_status.text+="\nClear the exterior hatch approach."
	if not Service.ready(game,cell): cycle_status.text+="\nPOWER OFF / CYCLE HELD"
