extends VBoxContainer
## Crew dispatch and live mission controls for a built Moonbay.

const Hints = preload("res://scripts/title_button_style.gd")
const Badges = preload("res://scripts/ui_badges.gd")
const Icons = preload("res://scripts/ui_icons.gd")
const Widgets = preload("res://scripts/ui_widgets.gd")
const Mission = preload("res://scripts/moonbay_missions.gd")
const Architects = preload("res://scripts/architects.gd")
const ORDERS := ["survey", "recover", "deep_access"]
var game
var crew_choice: OptionButton
var order_choice: OptionButton
var target_choice: OptionButton
var launch_button: Button
var helmet_button: Button
var refill_button: Button
var recall_button: Button
var repair_button: Button
var status: Label
var mission_badges := HFlowContainer.new()
var mission_meter := ProgressBar.new()
var clock := 0.0
var feedback := ""
var feedback_until := 0

func _ready() -> void:
	add_theme_constant_override("separation",6)
	crew_choice = OptionButton.new()
	for id in Architects.IDS:
		crew_choice.add_item(Architects.NAMES[id])
		crew_choice.set_item_metadata(crew_choice.item_count-1,id)
	add_child(crew_choice)
	helmet_button = _button("FIT DIVING HELMET")
	helmet_button.pressed.connect(func(): _helmet(false))
	refill_button = _button("REFILL HELMET TANK")
	refill_button.pressed.connect(func(): _helmet(true))
	Icons.apply(refill_button,"oxygen")
	var gear_row := HBoxContainer.new()
	gear_row.name = "LockerActions"
	gear_row.add_theme_constant_override("separation",10)
	add_child(gear_row)
	move_child(gear_row,helmet_button.get_index())
	helmet_button.reparent(gear_row)
	refill_button.reparent(gear_row)
	order_choice = OptionButton.new()
	for title in ["SURVEY CONTACT", "RECOVER CARGO", "DEEP ACCESS"]: order_choice.add_item(title)
	order_choice.item_selected.connect(func(_index): refresh())
	add_child(order_choice)
	target_choice = OptionButton.new()
	add_child(target_choice)
	launch_button = _button("ASSIGN CREW / PREPARE MINI-SUB")
	Icons.apply(launch_button,"orbit")
	launch_button.pressed.connect(_launch)
	recall_button = _button("RECALL MINI-SUB")
	Icons.apply(recall_button,"back")
	recall_button.pressed.connect(_recall)
	repair_button = _button("REPAIR MINI-SUB / 4 METAL")
	Icons.apply(repair_button,"repair")
	repair_button.pressed.connect(_repair)
	mission_badges.name = "MissionReadouts"
	mission_badges.add_theme_constant_override("h_separation",6)
	mission_badges.add_theme_constant_override("v_separation",6)
	add_child(mission_badges)
	mission_meter.name = "MissionProgress"
	mission_meter.show_percentage = false
	mission_meter.custom_minimum_size.y = 10
	mission_meter.add_theme_stylebox_override("background",Widgets.track("081d23","414e54",4))
	mission_meter.add_theme_stylebox_override("fill",Widgets.track("416d6d","668581",4))
	add_child(mission_meter)
	status = Label.new()
	status.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	status.add_theme_font_size_override("font_size",14)
	add_child(status)
	refresh()

func _button(label: String) -> Button:
	var button := Button.new()
	button.text = label
	button.custom_minimum_size = Vector2(280,34)
	game._style_hud_button(button,false)
	add_child(button)
	return button

func _process(delta: float) -> void:
	clock += delta
	if clock >= 0.25:
		clock = 0.0
		refresh()

func _room() -> Dictionary:
	var room: Dictionary = game.occupied.get(game.selected_room_cell,{})
	return room if room.get("id","")=="moonbay" else {}

func _targets(order: String) -> Array[Vector2i]:
	var cells: Array[Vector2i] = []
	for cell in game.drone_fleet.sites:
		var site: Dictionary = game.drone_fleet.sites[cell]
		if not site.get("active",false) or int(site.get("units",0))<=0: continue
		if order=="survey" and site.get("discovered",false): continue
		if order=="recover" and not site.get("discovered",false): continue
		if order=="deep_access" and (not site.get("discovered",false) or not site.get("moonbay_deep",false)): continue
		cells.append(cell)
	cells.sort_custom(func(a,b): return (Vector2(a)-Vector2(game.selected_room_cell)).length_squared() < (Vector2(b)-Vector2(game.selected_room_cell)).length_squared())
	return cells

func refresh() -> void:
	if crew_choice==null: return
	var room := _room()
	visible = game.selected_card_id.is_empty() and game.hovered_card_id.is_empty() and not room.is_empty()
	if not visible: return
	var state := Mission.mission_state(room)
	if state.phase != "idle":
		var order_index: int = ORDERS.find(str(state.order))
		if order_index >= 0: order_choice.select(order_index)
		for index in range(crew_choice.item_count):
			if crew_choice.get_item_metadata(index)==state.crew: crew_choice.select(index); break
	var order: String = ORDERS[order_choice.selected]
	var former: Variant = target_choice.get_item_metadata(target_choice.selected) if target_choice.selected>=0 else null
	target_choice.clear()
	var destinations: Array[Vector2i] = _targets(order)
	if state.phase != "idle": destinations.assign([Vector2i(state.target)])
	for cell in destinations:
		var site: Dictionary = game.drone_fleet.sites.get(cell,{"discovered":true,"kind":"CONTACT"})
		var label: String = "%s / %d,%d%s" % ["UNSURVEYED CONTACT" if not site.get("discovered",false) else str(site.get("kind","site")).to_upper(),cell.x,cell.y," / HAZARD" if site.get("hazardous",false) else ""]
		target_choice.add_item(label)
		target_choice.set_item_metadata(target_choice.item_count-1,cell)
		if cell==former: target_choice.select(target_choice.item_count-1)
	if target_choice.selected<0 and target_choice.item_count>0: target_choice.select(0)
	if target_choice.item_count==0: target_choice.text = "NO CONTACTS FOR THIS ORDER"
	for i in range(crew_choice.item_count): crew_choice.set_item_disabled(i,not Architects.present(game,str(crew_choice.get_item_metadata(i))))
	if state.phase=="idle" and (crew_choice.selected<0 or crew_choice.is_item_disabled(crew_choice.selected)):
		for i in range(crew_choice.item_count):
			if not crew_choice.is_item_disabled(i): crew_choice.select(i); break
	var crew_id: String = str(crew_choice.get_item_metadata(crew_choice.selected)) if crew_choice.selected>=0 else ""
	var crew_issue: String = Mission.crew_problem(game,room,crew_id)
	var actor = Architects.actor_for(game,crew_id) if Architects.IDS.has(crew_id) else null
	var locker_ready: bool = actor != null and Architects.present(game,crew_id) and actor.needs_air() and actor.active and not actor.dead and actor.moonbay_assignment.is_empty() and actor.expedition.is_empty() and not actor.helmet_action_active() and actor.locker_request.is_empty() and preload("res://scripts/airlock_service.gd").ready(game,room.pos)
	helmet_button.disabled = not locker_ready
	helmet_button.text = "RETURN DIVING HELMET" if actor != null and actor.helmet_equipped else "FIT DIVING HELMET"
	refill_button.disabled = not locker_ready or not actor.helmet_equipped
	var ready: bool = state.phase=="idle" and int(state.damage)==0 and target_choice.item_count>0 and crew_issue.is_empty() and game.running and not game.paused and game.hardware.power and not game.unpowered_room_cells.has(room.pos)
	launch_button.disabled = not ready
	crew_choice.disabled = state.phase!="idle"
	order_choice.disabled = state.phase!="idle"
	target_choice.disabled = state.phase!="idle" or target_choice.item_count==0
	recall_button.visible = state.phase!="idle"
	recall_button.disabled = state.get("recall",false)
	repair_button.visible = state.phase=="idle" and int(state.damage)>0
	repair_button.disabled = int(game.resources.get("metal",0))<Mission.REPAIR_METAL
	var launch_hint := "Assign the selected crew and order to this destination."
	if state.phase!="idle": launch_hint = "The mini-sub is already on a mission. Recall it or wait for its return."
	elif int(state.damage)>0: launch_hint = "Repair the mini-sub for 4 Metal before launching."
	elif target_choice.item_count==0: launch_hint = "No eligible contacts for this order. Choose another order or survey more seabed."
	elif not crew_issue.is_empty(): launch_hint = crew_issue
	elif not game.running: launch_hint = "Start an expedition before dispatching crew."
	elif game.paused: launch_hint = "Resume Time/Cycle before launching the mini-sub."
	elif not game.hardware.power or game.unpowered_room_cells.has(room.pos): launch_hint = "Supply Power to this Moonbay before launching."
	Hints.set_hint(launch_button,launch_hint)
	Hints.set_hint(recall_button,"Recall already requested; wait for the mini-sub's safe return." if state.get("recall",false) else "Recall the mini-sub through its safe return cycle.")
	Hints.set_hint(repair_button,"Need %d more Metal to repair the mini-sub." % maxi(0,Mission.REPAIR_METAL-int(game.resources.get("metal",0))) if repair_button.disabled else "Spend 4 Metal to repair the docked mini-sub.")
	var locker_hint := "Fit or return reusable diving gear at the Moonbay locker."
	if actor==null or not Architects.present(game,crew_id): locker_hint = "Choose a recovered crew member."
	elif not actor.needs_air(): locker_hint = "Androids do not use diving helmets."
	elif actor.dead or not actor.active: locker_hint = "Choose an active crew member."
	elif state.phase!="idle": locker_hint = "Wait for the mini-sub to return before using the locker."
	elif not actor.moonbay_assignment.is_empty() or not actor.expedition.is_empty(): locker_hint = "Wait for this crew member's mission to finish."
	elif actor.helmet_action_active() or not actor.locker_request.is_empty(): locker_hint = "Wait for the current locker action to finish."
	elif not preload("res://scripts/airlock_service.gd").ready(game,room.pos): locker_hint = "Resume and power the Moonbay before using its locker."
	Hints.set_hint(helmet_button,locker_hint)
	Hints.set_hint(refill_button,(locker_hint if helmet_button.disabled else "Fit a diving helmet before refilling its tank.") if refill_button.disabled else "Refill the helmet tank; station Oxygen is required.")
	mission_meter.visible = state.phase != "idle"
	var readings: Array = []
	if state.phase != "idle":
		mission_meter.value = clampf(100.0*float(state.progress)/maxf(1.0,Mission._duration(room,state)),0,100)
		readings.append([str(state.phase).replace("_"," "),"orbit","normal","%d%%" % roundi(mission_meter.value)])
		readings.append(["WATER","water","normal","%d%%" % roundi(float(state.chamber_water)*100)])
		if state.recall: readings.append(["RECALL","back","warning"])
	else:
		readings.append(["DAMAGED" if int(state.damage)>0 else "IDLE","repair" if int(state.damage)>0 else "idle","warning" if int(state.damage)>0 else "normal"])
	Badges.update(mission_badges,readings)
	if Time.get_ticks_msec()<feedback_until:
		status.text = feedback
	elif state.phase!="idle":
		var pilot: String = Architects.NAMES.get(state.crew,str(state.crew))
		status.text = "%s / %s\n%s" % [pilot,str(state.order).replace("_"," ").to_upper(),str(state.last_result)]
	else:
		status.text = "MINI-SUB DAMAGED / 4 METAL TO REPAIR" if int(state.damage)>0 else ("NO CONTACTS FOR THIS ORDER" if target_choice.item_count==0 else (crew_issue if not crew_issue.is_empty() else "Wet bay ready. The airlock will cycle before boarding."))
		if not str(state.last_result).is_empty(): status.text += "\n"+str(state.last_result)

func _launch() -> void:
	if target_choice.selected<0 or crew_choice.selected<0: return
	var problem: String = Mission.dispatch(game,_room(),str(crew_choice.get_item_metadata(crew_choice.selected)),target_choice.get_item_metadata(target_choice.selected),ORDERS[order_choice.selected])
	if problem.is_empty(): game._log("Moonbay mission dispatched. The chamber remains dry until the crew boards.")
	else: _feedback(problem)
	refresh()

func _helmet(refill: bool) -> void:
	if crew_choice.selected<0: return
	var id := str(crew_choice.get_item_metadata(crew_choice.selected))
	if not preload("res://scripts/airlock_service.gd").request(game,id,_room().pos,refill):
		_feedback("The suit locker is unavailable. Clear the crew member's current action and check power.")
	refresh()

func _recall() -> void:
	if Mission.recall(game,_room()): game._log("Moonbay recall acknowledged. Returning by the safe cycle.")
	refresh()

func _repair() -> void:
	var problem: String = Mission.repair(game,_room())
	if problem.is_empty(): game._log("Mini-sub repaired. Four Metal spent.")
	else: _feedback(problem)
	refresh()

func _feedback(message: String) -> void:
	feedback = message
	feedback_until = Time.get_ticks_msec()+3000
