extends VBoxContainer
const Service=preload("res://scripts/airlock_service.gd")
const Hints=preload("res://scripts/title_button_style.gd")
const Badges=preload("res://scripts/ui_badges.gd")
const Icons=preload("res://scripts/ui_icons.gd")
const Architects=preload("res://scripts/architects.gd")
var game
var choice: OptionButton
var refill: Button
var action: Button
var status: Label
var elapsed:=0.0
var feedback_until:=0
var cycle_button: Button
var cycle_status: Label
var cycle_badges := HFlowContainer.new()
var expedition_button: Button
var expedition_kind: OptionButton
const Cycle=preload("res://scripts/airlock_cycle.gd")
func _ready() -> void:
	add_theme_constant_override("separation",6)
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
	refill=Button.new()
	game._style_hud_button(refill,false)
	refill.pressed.connect(func(): Service.request(game,str(choice.get_item_metadata(choice.selected)),game.selected_room_cell,true))
	add_child(refill)
	var gear_row := HBoxContainer.new()
	gear_row.name = "LockerActions"
	gear_row.add_theme_constant_override("separation",10)
	add_child(gear_row)
	move_child(gear_row,action.get_index())
	action.reparent(gear_row)
	refill.reparent(gear_row)
	status=Label.new()
	status.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	status.add_theme_font_size_override("font_size",14)
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
	cycle_status.add_theme_font_size_override("font_size",14)
	add_child(cycle_status)
	cycle_badges.name = "AirlockReadouts"
	cycle_badges.add_theme_constant_override("h_separation",6)
	cycle_badges.add_theme_constant_override("v_separation",6)
	add_child(cycle_badges)
	expedition_kind=OptionButton.new()
	expedition_kind.add_item("MINE MINERALS // 2 METAL")
	expedition_kind.add_item("SALVAGE SCRAP // 1 METAL + 1 DATA")
	expedition_kind.select(1)
	expedition_kind.item_selected.connect(func(_index): refresh())
	add_child(expedition_kind)
	expedition_button = Button.new()
	game._style_hud_button(expedition_button,false)
	expedition_button.pressed.connect(func():
		var id := str(choice.get_item_metadata(choice.selected))
		var actor = Architects.actor_for(game,id)
		if not actor.expedition.is_empty(): preload("res://scripts/crew_expedition.gd").request_recall(game,actor)
		elif not preload("res://scripts/crew_expedition.gd").dispatch(game,id,game.selected_room_cell,"mining" if expedition_kind.selected==0 else "salvage"):
			status.text = "No reachable surveyed %s within return range. Clear a shorter route or build a closer airlock." % ("mineral deposit" if expedition_kind.selected==0 else "scrap pile")
			feedback_until = Time.get_ticks_msec()+3500
		refresh()
	)
	add_child(expedition_button)
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
	if not visible: return
	for i in range(choice.item_count): choice.set_item_disabled(i,not Architects.present(game,str(choice.get_item_metadata(i))))
	if choice.is_item_disabled(choice.selected):
		for i in range(choice.item_count):
			if not choice.is_item_disabled(i):
				choice.select(i)
				break
	var id:=str(choice.get_item_metadata(choice.selected))
	var actor=Architects.actor_for(game,id)
	var expedition_reason := preload("res://scripts/crew_expedition.gd").reason(game,id,cell)
	expedition_kind.disabled=not actor.expedition.is_empty()
	if not actor.expedition.is_empty(): expedition_kind.select(0 if actor.expedition.get("kind","salvage")=="mining" else 1)
	var mission_label := "MINING" if expedition_kind.selected==0 else "SALVAGE"
	expedition_button.text = "RECALL EXPEDITION" if not actor.expedition.is_empty() else (mission_label+" EXPEDITION // BATTERY" if not actor.needs_air() else mission_label+" EXPEDITION // 2 OXYGEN")
	expedition_button.disabled = actor.expedition.is_empty() and not expedition_reason.is_empty()
	Hints.set_hint(expedition_button,expedition_reason if actor.expedition.is_empty() and not expedition_reason.is_empty() else ("Marsh needs no helmet or Oxygen. Battery reserve limits his trip; return to the charging pod afterward." if not actor.needs_air() else "Recover one finite load from the nearest surveyed site of the selected type. Minerals yield 2 Metal; scrap yields 1 Metal and 1 Data. Cargo arrives after safe return. Tank lasts 60 seconds underwater."))
	var active_work: bool=actor.helmet_action_active() or not actor.locker_request.is_empty() or Service.refilling(actor)
	action.text="RETURN DIVING HELMET" if actor.helmet_equipped else "FIT DIVING HELMET"
	action.disabled=not actor.needs_air() or not actor.expedition.is_empty() or not Service.ready(game,cell) or not Architects.present(game,id) or not actor.active or actor.dead or active_work or Service.busy(game,cell,actor) or actor.movement_medium!="dry" or not actor.stage.is_empty()
	Icons.apply(refill,"power" if not actor.needs_air() else "oxygen")
	Icons.apply(expedition_button,"back" if not actor.expedition.is_empty() else "orbit")
	refill.text="BATTERY // %d%%" % roundi(actor.battery) if not actor.needs_air() else "REFILL OXYGEN // %.0f / 60s" % actor.tank_oxygen
	if not actor.needs_air(): action.text="ANDROID // NO HELMET REQUIRED"
	refill.disabled=action.disabled or not actor.helmet_equipped
	if Time.get_ticks_msec()>=feedback_until:
		status.text=actor.activity if active_work else "Locker gear is reusable."
		if not Service.ready(game,cell): status.text="Lockers need a powered, active airlock."
	var room: Dictionary=game.occupied[cell]
	var pose:=Cycle.pose(room)
	cycle_button.text="FLOOD & OPEN OUTER HATCH" if pose.phase=="dry" else "CLOSE OUTER HATCH & DRAIN"
	cycle_button.disabled=not Service.ready(game,cell) or not pose.phase in ["dry","exterior","sealed_exterior"] or (pose.phase=="dry" and not Cycle.exterior_clear(game,room))
	if preload("res://scripts/crew_expedition.gd").reserved(game,cell):
		cycle_button.disabled = true
		action.disabled = true
		status.text = actor.activity
	Icons.apply(cycle_button,"doors_open" if pose.phase=="dry" else "doors_closed")
	Badges.update(cycle_badges,[["WATER","water","normal","%d%%" % roundi(pose.water*100)],["PRESSURE","sensor","normal","%d%%" % roundi(pose.pressure*100)]])
	cycle_status.text=Cycle.LABELS[pose.phase]
	if pose.phase=="dry":
		var obstruction:=Cycle.exterior_problem(game,room)
		if not obstruction.is_empty(): cycle_status.text+="\n"+obstruction
	if not Service.ready(game,cell): cycle_status.text+="\n"+("ROOM SUSPENDED" if room.get("suspended",false) else "POWER OFF")+" / CYCLE HELD"

	var locker_hint := "Fit or return reusable diving gear at this airlock."
	if not Architects.present(game,id): locker_hint = "Recover this crew member before assigning locker work."
	elif actor.dead or not actor.active: locker_hint = "This crew member is unavailable. Choose an active crew member."
	elif not actor.needs_air(): locker_hint = "Androids need no diving helmet. Their trips use battery reserve."
	elif not actor.expedition.is_empty(): locker_hint = "Recall the expedition and wait for the crew member to return."
	elif game.occupied[cell].get("suspended",false): locker_hint = "Resume the airlock before using its lockers."
	elif not Service.ready(game,cell): locker_hint = "Supply Power to an operating airlock before using the lockers."
	elif active_work: locker_hint = "Wait for the current locker action to finish."
	elif Service.busy(game,cell,actor): locker_hint = "Another crew member is using these lockers. Wait for them to finish."
	elif actor.movement_medium!="dry": locker_hint = "Bring this crew member inside onto a dry floor before changing gear."
	elif not actor.stage.is_empty(): locker_hint = "Wait for this crew member's current transition to finish."
	Hints.set_hint(action,locker_hint)
	Hints.set_hint(refill,(locker_hint if action.disabled else "Fit a diving helmet before refilling its tank.") if refill.disabled else "Refill the helmet tank at the locker; station Oxygen is required.")
	var hatch_hint := "Cycle the chamber before crossing the outer hatch."
	if preload("res://scripts/crew_expedition.gd").reserved(game,cell): hatch_hint = "An expedition owns this airlock cycle. Wait for the crew to return."
	elif not Service.ready(game,cell): hatch_hint = "Resume and power this airlock to cycle its hatches."
	elif not pose.phase in ["dry","exterior","sealed_exterior"]: hatch_hint = "Wait for the current chamber cycle to finish."
	elif pose.phase=="dry" and not Cycle.exterior_clear(game,room): hatch_hint = Cycle.exterior_problem(game,room)+" Clear the exterior hatch tile first."
	Hints.set_hint(cycle_button,hatch_hint)

	if not actor.expedition.is_empty(): Hints.set_hint(expedition_button,"Recall this expedition and wait for a safe return through the airlock.")
