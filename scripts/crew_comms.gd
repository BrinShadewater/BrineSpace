extends CanvasLayer
## Portrait transmissions, using approved native-resolution concept crops.
const Architects=preload("res://scripts/architects.gd")
const Dialogue=preload("res://scripts/crew_dialogue.gd")
const Companions=preload("res://scripts/companions.gd")
# Companions who answer a click. Margot keeps her pet interaction.
const TALKING_COMPANIONS := ["josh","river"]
# Seconds between the architect stepping out of the core pod and BRINE's first words.
const OPENING_DELAY := 2.0
var game
var panel: PanelContainer
var portrait: TextureRect
var bubbles: Control
var speaker: Label
var body: RichTextLabel
var next_button: Button
var pending: Array=[]
var history: Array=[]
var archive_path:=""
var archive_writable:=true
var seen: Dictionary={}
var current: Dictionary={}
var reveal:=0.0
var character_delay:=0.0
var brine_portrait: Texture2D
var history_picker: OptionButton
var speed_picker: OptionButton
var text_speed:=1.0
var event_clock:=0.0
var poll_clock:=0.0
var last_ambient:=-60.0
var observed_crew: Dictionary={}
var greeting_sent:=false
var opening_enabled:=false
var heading: Label
var replies: HBoxContainer
var talk_id:=""
var contact_picker: OptionButton
var minimized:=false
var holds_pause:=false
var pause_before_dialogue:=false
var inbox_button: Button
var health_button: Button
var room_status: Label
const WAKE_LINES={"marsh":"Systems responsive. There is a gap in my records. I would prefer to find out why.","bill":"Still breathing. I will take a look around before we call this place habitable.","veld":"I remember the last reading. I would like to know why it changed while I was asleep.","branforth":"I can hear a bearing somewhere. Give me a moment to decide how worried to be."}
const FINISH_LINES={"marsh":"Inspection complete. I have separated observed faults from suspected ones.","bill":"Inspection finished. Nothing moved that was supposed to stay still.","veld":"The readings are recorded. I have questions. That is preferable to having no readings.","branforth":"Check complete. The equipment can keep working. I suggest we let it."}
var finished_seconds:=0.0
var opening_wait:=0.0
var companion_talks: Dictionary={}
func _ready() -> void:
	layer=25
	panel=PanelContainer.new(); add_child(panel)
	panel.theme=preload("res://scripts/title_button_style.gd").menu_theme()
	var style:=StyleBoxFlat.new(); style.bg_color=Color("102329"); style.border_color=Color("4d827e")
	style.set_border_width_all(2); style.set_content_margin_all(10)
	panel.add_theme_stylebox_override("panel",style)
	var row:=HBoxContainer.new(); row.add_theme_constant_override("separation",12); panel.add_child(row)
	portrait=TextureRect.new(); portrait.custom_minimum_size=Vector2(96,108)
	portrait.expand_mode=TextureRect.EXPAND_IGNORE_SIZE; portrait.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	portrait.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR; row.add_child(portrait)
	bubbles=preload("res://scripts/brine_comms_bubbles.gd").new(); portrait.add_child(bubbles)
	var column:=VBoxContainer.new(); column.size_flags_horizontal=Control.SIZE_EXPAND_FILL; row.add_child(column)
	var title:=HBoxContainer.new(); column.add_child(title)
	speaker=Label.new(); speaker.add_theme_font_size_override("font_size",16)
	speaker.size_flags_horizontal=Control.SIZE_EXPAND_FILL; speaker.text_overrun_behavior=TextServer.OVERRUN_TRIM_ELLIPSIS
	title.add_child(speaker)
	var close:=Button.new(); close.text="X"; close.tooltip_text="Close comms"; close.pressed.connect(minimize); title.add_child(close)
	body=RichTextLabel.new(); body.bbcode_enabled=false; body.scroll_following=true
	body.custom_minimum_size=Vector2(0,74); body.size_flags_vertical=Control.SIZE_EXPAND_FILL
	body.add_theme_font_size_override("normal_font_size",16); column.add_child(body)
	# Clicking anywhere on the transmission moves on (buttons keep their own clicks).
	body.mouse_filter=Control.MOUSE_FILTER_PASS; portrait.mouse_filter=Control.MOUSE_FILTER_PASS
	panel.gui_input.connect(_on_panel_input)
	next_button=Button.new(); next_button.text="Next"; next_button.size_flags_horizontal=Control.SIZE_SHRINK_END
	next_button.pressed.connect(advance); column.add_child(next_button)
	# Retain archive/context data helpers without exposing the former control panel.
	var stored:=Control.new(); add_child(stored); stored.hide()
	heading=Label.new(); stored.add_child(heading)
	room_status=Label.new(); stored.add_child(room_status)
	replies=HBoxContainer.new(); stored.add_child(replies)
	health_button=Button.new(); replies.add_child(health_button)
	history_picker=OptionButton.new(); stored.add_child(history_picker)
	speed_picker=OptionButton.new(); stored.add_child(speed_picker)
	contact_picker=OptionButton.new(); stored.add_child(contact_picker)
	inbox_button=Button.new(); stored.add_child(inbox_button)
	text_speed=1.0
	load_archive(); refresh_history(); panel.hide()
func transmit(id: String, message: String, key: String="", urgent: bool=false) -> bool:
	if (id!="brine" and not Architects.NAMES.has(id)) or message.strip_edges().is_empty(): return false
	if not key.is_empty() and seen.has(key): return false
	if pending.size()>=8: return false
	var first_waiting := pending.is_empty()
	if not key.is_empty(): seen[key]=true
	var entry: Dictionary={"speaker":id,"text":message,"urgent":urgent}
	if not key.is_empty(): entry.key=key
	if urgent:
		var index:=0
		while index<pending.size() and pending[index].get("urgent",false): index+=1
		pending.insert(index,entry)
	else: pending.append(entry)
	if first_waiting and is_instance_valid(game) and game.has_method("play_station_sound"): game.play_station_sound("ui_comms")
	if minimized: minimized=false; current={}
	return true
# Save/Continue keeps what was already said. Without it every Continue replayed the crew
# wake lines and BRINE's greeting into the history (an owner playtest history held the
# same line up to ten times).
func snapshot() -> Dictionary:
	return {"seen":seen.keys(),"greeting_sent":greeting_sent}

func restore_state(data: Variant) -> void:
	if not data is Dictionary or not data.get("seen") is Array: return
	var said := {}
	for key in data.seen:
		if key is String and key.length() <= 128:
			said[key]=true
			seen[key]=true
	greeting_sent=greeting_sent or data.get("greeting_sent",false)==true
	# A keyed line queued while the checkpoint loaded (a greeting on a slow Continue) was already said.
	for index in range(pending.size()-1,-1,-1):
		if said.has(str(pending[index].get("key",""))): pending.remove_at(index)
	if said.has(str(current.get("key",""))):
		if not history.is_empty() and history.back().get("key","")==current.key:
			history.pop_back()
			save_archive()
		var queued: Array=pending.duplicate()
		dismiss()
		pending=queued

func show_next() -> void:
	talk_id=""
	if pending.is_empty(): dismiss(); return
	current=pending.pop_front(); history.append(current.duplicate())
	if history.size()>30: history.pop_front()
	save_archive()
	refresh_history()
	present_current()
func present_current() -> void:
	_hold_pause()
	minimized=false; inbox_button.hide(); finished_seconds=0.0
	heading.text="COMMS // PRIORITY TRANSMISSION" if current.get("urgent",false) else "COMMS // INCOMING TRANSMISSION"
	var style: StyleBoxFlat=panel.get_theme_stylebox("panel").duplicate()
	style.border_color=Color("b98a60") if current.get("urgent",false) else Color("4d827e")
	panel.add_theme_stylebox_override("panel",style)
	replies.hide()
	room_status.text=current.get("room_status",""); room_status.visible=not room_status.text.is_empty()
	if current.speaker=="brine":
		portrait.custom_minimum_size=Vector2(150,150)
		if brine_portrait==null:
			var image:=Image.new()
			preload("res://scripts/safe_image.gd").load_png(image, "res://character/brine-comms-v14/portrait.png")
			var framed := AtlasTexture.new()
			framed.atlas = ImageTexture.create_from_image(image)
			var crop: Rect2 = bubbles.PORTRAIT_CROP
			framed.region = Rect2(crop.position * Vector2(image.get_size()), crop.size * Vector2(image.get_size()))
			brine_portrait = framed
		portrait.texture=brine_portrait
	else:
		portrait.custom_minimum_size=Vector2(150,150)
		portrait.texture=Companions.portrait(current.speaker) if Companions.NAMES.has(current.speaker) else Architects.selection_portrait(current.speaker)
	bubbles.visible=current.speaker=="brine"
	speaker.text="BRINE // STATION CORE" if current.speaker=="brine" else speaker_name(current.speaker)
	body.text=current.text; body.visible_characters=0; reveal=0; character_delay=0.0
	next_button.text="Next"; next_button.show(); panel.show()
func speaker_name(id: String) -> String:
	if id=="brine": return "BRINE"
	return Companions.NAMES[id] if Companions.NAMES.has(id) else Architects.NAMES.get(id,id)

# A click on the transmission skips straight to the next line, or closes it after the last
# (owner playtest). The Next button still finishes a line that is typing out first.
func _on_panel_input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed and event.button_index==MOUSE_BUTTON_LEFT): return
	panel.accept_event()
	skip()

func skip() -> void:
	if current.is_empty(): return
	if pending.is_empty(): minimize()
	else: show_next()
	update_replies()

func advance() -> void:
	if body.visible_characters<body.get_total_character_count():
		body.visible_characters=body.get_total_character_count(); reveal=body.visible_characters
		next_button.text="Next"; next_button.show(); finished_seconds=0.0
	else:
		if pending.is_empty(): minimize()
		else: show_next()
	update_replies()
func dismiss() -> void:
	_release_pause()
	minimized=false; inbox_button.hide()
	pending.clear(); current={}; talk_id=""; replies.hide(); panel.hide()
func reopen() -> void:
	finished_seconds=0.0
	minimized=false; inbox_button.hide()
	if not current.is_empty(): _hold_pause(); panel.show(); return
	if not pending.is_empty(): show_next(); return
	if not history.is_empty():
		replay_history(history.size()); return
	else:
		transmit("brine","I have mapped thirty-seven ways to run out of oxygen. I recommend none of them.")
	show_next()
func _process(delta: float) -> void:
	if game is Control and is_instance_valid(game.comms_button):
		game.comms_button.text="COMMS (%d)"%pending.size() if not pending.is_empty() else "COMMS"
	event_clock+=delta
	poll_clock+=delta
	if game!=null and not greeting_sent and game.startup_complete and not game.paused and core_awake():
		opening_wait+=delta
		if opening_wait>=OPENING_DELAY: poll_clock=maxf(poll_clock,1.0)
	if game!=null and game.startup_complete and not game.paused and poll_clock>=1.0:
		poll_clock=0.0; observe_game()
	if game!=null and (game._gameplay_input_blocked() or not game.startup_complete):
		panel.hide(); inbox_button.hide(); return
	if minimized:
		panel.hide(); place_inbox(); return
	if current.is_empty() and not pending.is_empty(): show_next()
	elif not current.is_empty(): _hold_pause(); panel.show()
	if not panel.visible: return
	if bubbles.visible: bubbles.advance(delta)
	place_panel()
	character_delay-=delta
	while character_delay<=0.0 and body.visible_characters<body.get_total_character_count():
		body.visible_characters+=1
		var letter: String=body.text.substr(body.visible_characters-1,1)
		character_delay+=(0.36 if letter in [".","!","?"] else (0.18 if letter in [",",";",":"] else 0.075))/text_speed
	update_replies()
func room_built(id: String) -> void:
	var lines: Dictionary={
		"pressure_control":"The manifold is in place. I would prefer to hear about a pressure change from a gauge, rather than the walls.",
		"listening_post":"The listening bank is ready. Let us find out which sounds belong to the station.",
		"crew_hab":"A berth, a little privacy, and a door that closes. That is a respectable beginning."}
	if not lines.has(id): return
	var who: String=game.meta.selected_architect
	if id=="listening_post" and game.has_dr_veld(): who="veld"
	elif id=="pressure_control" and game.has_chief_branforth(): who="branforth"
	transmit(who,lines[id],"built/"+id)

func place_panel() -> void:
	var area:=Rect2(Vector2.ZERO,get_viewport().get_visible_rect().size)
	if game!=null and is_instance_valid(game.grid_scroll): area=game.grid_scroll.get_global_rect()
	panel.set_anchors_preset(Control.PRESET_TOP_LEFT)
	panel.size=Vector2(minf(720,area.size.x-32),170)
	panel.position=Vector2(area.get_center().x-panel.size.x*0.5,area.end.y-panel.size.y-16)

func open_brine() -> void:
	talk_id=""
	current={"speaker":"brine","text":"I have mapped thirty-seven ways to run out of oxygen. I recommend none of them."}
	record_reply()

func refresh_history() -> void:
	history_picker.clear(); history_picker.add_item("Message history (%d)"%history.size())
	for entry in history:
		var name: String=speaker_name(entry.speaker)
		history_picker.add_item(name+"  -  "+str(entry.text).left(42))
func replay_history(index: int) -> void:
	talk_id=""
	if index<=0 or index>history.size(): return
	current=history[index-1].duplicate(); present_current()
func announce(id: String, message: String, key: String, urgent: bool=false) -> bool:
	if event_clock-last_ambient<45.0: return false
	if not transmit(id,message,key,urgent): return false
	last_ambient=event_clock; return true
# The station wakes first: lights, screens and the core pod play out, and BRINE speaks two
# seconds after the architect steps out. The greeting used to arrive a second in, and the
# pause it holds froze the whole wake sequence behind the dialogue (owner playtest).
func core_awake() -> bool:
	var run = game.get("architect_run")
	if not run is Dictionary or run.get("core",{}).is_empty(): return true
	return run.core.get("recovered",false)

func opening_ready() -> bool:
	var run = game.get("architect_run")
	if not run is Dictionary or run.get("core",{}).is_empty(): return true # Legacy checkpoints have no core pod.
	return core_awake() and opening_wait>=OPENING_DELAY

func observe_game() -> void:
	if not greeting_sent:
		if not opening_ready(): return
		greeting_sent=announce("brine","You are awake. The station is still holding pressure. I would like to keep both of those statements true.","opening")
		if greeting_sent and opening_enabled:
			var starter: String=game.meta.selected_architect
			transmit(starter,WAKE_LINES[starter],"opening/crew")
			transmit("brine","First objective: connect a power room to the Core. Select a power blueprint, rotate it to match the doors, then place it. Construction takes time.","opening/objective")
		for id in Architects.IDS:
			var actor=Architects.actor_for(game,id)
			observed_crew[id]={"active":actor.active,"completion":int(actor.completed_activity.get("serial",0))}
		return
	var forecast: Dictionary={}
	if event_clock-last_ambient>=45.0: forecast=game._project_cycle_delta()
	for resource in ["oxygen","power","food","water"]:
		if float(game.resources.get(resource,100))<=2 and float(forecast.get(resource,0))<0:
			if announce("brine",{"oxygen":"Oxygen reserves are critically low. Breathing more slowly is not a repair strategy.","power":"Power reserves are nearly exhausted. The dark is cheaper. It is not safer.","food":"Food reserves are nearly gone. I have no useful recipe for optimism.","water":"Water reserves are nearly gone. The ocean outside remains remarkably unhelpful."}[resource],"critical/"+resource,true): return
	for id in Architects.IDS:
		var actor=Architects.actor_for(game,id)
		var before: Dictionary=observed_crew.get(id,{})
		if actor.active and not actor.dead:
			if not before.get("active",false):
				if not seen.has("awake/"+id) and not announce(id,WAKE_LINES[id],"awake/"+id): continue
			var finished: Dictionary=actor.completed_activity
			if int(finished.get("serial",0))>int(before.get("completion",0)):
				var key: String="activity/"+id+"/"+str(finished.activity)
				var line: String="A short rest helps. A longer one can wait until the station is less interesting." if finished.activity=="resting beside the berth" else FINISH_LINES[id]
				if not seen.has(key) and not announce(id,line,key): continue
		observed_crew[id]={"active":actor.active,"completion":int(actor.completed_activity.get("serial",0))}

func load_archive() -> void:
	if archive_path.is_empty() or not FileAccess.file_exists(archive_path): return
	var parser:=JSON.new()
	var parsed: int=parser.parse(FileAccess.get_file_as_string(archive_path))
	var data=parser.data if parsed==OK else null
	if not data is Dictionary or data.get("version")!=1 or not data.get("messages") is Array:
		archive_writable=false; history_picker.tooltip_text="Comms archive could not be read; original file preserved."; return
	var checked: Array=[]
	for entry in data.messages:
		if not entry is Dictionary or not entry.get("speaker") is String or not entry.get("text") is String:
			archive_writable=false; return
		if entry.speaker!="brine" and not Architects.NAMES.has(entry.speaker) and not TALKING_COMPANIONS.has(entry.speaker): archive_writable=false; return
		if entry.text.length()>4096: archive_writable=false; return
		checked.append({"speaker":entry.speaker,"text":entry.text,"urgent":entry.get("urgent",false)==true})
	history=checked.slice(maxi(0,checked.size()-30))
func save_archive() -> void:
	if archive_path.is_empty() or not archive_writable: return
	var temporary:=archive_path+".tmp"
	var file:=FileAccess.open(temporary,FileAccess.WRITE)
	if file==null: history_picker.tooltip_text="Comms archive could not be saved."; return
	file.store_string(JSON.stringify({"version":1,"messages":history})); file.close()
	if DirAccess.rename_absolute(temporary,archive_path)!=OK: history_picker.tooltip_text="Comms archive could not be saved."

func update_replies() -> void:
	health_button.visible=game!=null and (current.get("health",false) or current.has("room_cell"))
	health_button.text="Locate room" if current.has("room_cell") else "Station Health"
	health_button.disabled=current.get("room_missing",false)
	if health_button.disabled: health_button.text="Room unavailable"
	replies.visible=not talk_id.is_empty() and not current.is_empty() and current.speaker==talk_id and body.visible_characters>=body.get_total_character_count()

func open_crew(id: String) -> bool:
	if game==null: return false
	if TALKING_COMPANIONS.has(id): return open_companion(id)
	if not Architects.IDS.has(id): return false
	var actor=Architects.actor_for(game,id)
	if not actor.active or actor.dead: return false
	# Preserve queued station messages while the player asks a crew member a question.
	talk_id=id
	current={"speaker":id,"text":Dialogue.greeting(id,actor.activity)}
	record_reply()
	return true

# Josh and River answer when clicked (owner playtest). They have no question replies.
func open_companion(id: String) -> bool:
	if not game.companion_roster.has(id) or not game.companion_actors.has(id): return false
	var actor=game.companion_actors[id]
	if not actor.active: return false
	talk_id=""
	var count: int=int(companion_talks.get(id,0))
	companion_talks[id]=count+1
	current={"speaker":id,"text":Dialogue.companion_greeting(id,actor.activity,actor.water.mode,count)}
	if id=="river" and game.has_method("play_station_sound"): game.play_station_sound("companion_chirp",actor.foot/384.0)
	record_reply()
	return true

func record_reply() -> void:
	history.append(current.duplicate())
	if history.size()>30: history.pop_front()
	save_archive(); refresh_history(); present_current(); place_panel()

func answer(topic: String) -> void:
	if talk_id.is_empty() or game==null: return
	var actor=Architects.actor_for(game,talk_id)
	if not actor.active or actor.dead:
		talk_id=""; replies.hide(); return
	var line: String=""
	var context: Dictionary={}
	if topic=="This room?":
		var cell:=Vector2i(floori(actor.foot.x/384.0),floori(actor.foot.y/384.0))
		var room: Dictionary=game.occupied.get(cell,{})
		if room.is_empty(): line="I am outside the station. We can discuss the furnishings when I am back inside."
		else:
			var forecast: Dictionary=game._simulate_room_economy(true,game.cycle+1)
			var observed: String=str(game.offline_reasons.get(cell,"FUNCTIONING" if game.powered_room_cells.has(cell) else "AWAITING CYCLE"))
			context={"room_cell":[cell.x,cell.y],"room_id":room.id,"room_status":"Observed: %s\nNext cycle: %s"%[observed,str(forecast.offline.get(cell,"INPUTS AVAILABLE"))]}
			var definition: Dictionary=preload("res://scripts/room_database.gd").get_room(room.id)
			var comment: String=Dialogue.room_comment(talk_id,room.id)
			if comment.is_empty(): comment=definition.get("description","I am still getting a feel for this room.")
			line="%s. %s" % [definition.get("display_name",room.id),comment]
	else:
		var forecast: Dictionary=game._project_cycle_delta()
		var worst: String=""
		var cycles:=INF
		for resource in ["oxygen","power","food","water"]:
			var change: float=float(forecast.get(resource,0))
			if change<0:
				var remaining: float=float(game.resources.get(resource,0))/-change
				if remaining<cycles: worst=resource; cycles=remaining
		line=Dialogue.resource_report(talk_id,worst,int(game.resources.get(worst,0)),-float(forecast.get(worst,0)))
	current={"speaker":talk_id,"text":line,"health":topic=="Needs attention?"}
	current.merge(context); record_reply()

func crew_at(point: Vector2, cell_size: float) -> String:
	if game==null: return ""
	var found: String=""
	var nearest:=INF
	for id in Architects.IDS+TALKING_COMPANIONS:
		var companion: bool=TALKING_COMPANIONS.has(id)
		if companion and not game.companion_roster.has(id): continue
		var actor=game.companion_actors[id] if companion else Architects.actor_for(game,id)
		if not actor.active or actor.dead: continue
		var foot: Vector2=actor.foot/384.0*cell_size
		# Match the rendered body height and canonical foot pivot: crew 74 units, Josh 70, River 44.
		var bounds:=Rect2(foot-Vector2(cell_size*0.055,cell_size*0.19),Vector2(cell_size*0.11,cell_size*0.21))
		if id=="josh": bounds=Rect2(foot-Vector2(cell_size*0.055,cell_size*0.18),Vector2(cell_size*0.11,cell_size*0.20))
		elif id=="river": bounds=Rect2(foot-Vector2(cell_size*0.045,cell_size*0.115),Vector2(cell_size*0.09,cell_size*0.135))
		var distance: float=point.distance_squared_to(bounds.get_center())
		if bounds.has_point(point) and distance<nearest: found=id; nearest=distance
	return found

func reset_for_loop() -> void:
	dismiss(); seen.clear(); observed_crew.clear()
	greeting_sent=false; opening_enabled=true; event_clock=0; poll_clock=0; last_ambient=-60; opening_wait=0.0

func refresh_contacts() -> void:
	contact_picker.clear(); contact_picker.add_item("Contact crew...")
	contact_picker.add_item("BRINE"); contact_picker.set_item_metadata(1,"brine")
	if game!=null:
		for id in Architects.IDS:
			var actor=Architects.actor_for(game,id)
			if not actor.active or actor.dead: continue
			contact_picker.add_item(Architects.NAMES[id])
			contact_picker.set_item_metadata(contact_picker.item_count-1,id)
	contact_picker.select(0)

func select_contact(index: int) -> void:
	if index<=0 or index>=contact_picker.item_count: return
	var id: String=str(contact_picker.get_item_metadata(index))
	contact_picker.select(0)
	if id=="brine": open_brine()
	else: open_crew(id)

func minimize() -> void:
	_release_pause()
	minimized=true; panel.hide(); place_inbox()

func _hold_pause() -> void:
	if holds_pause or not is_instance_valid(game): return
	pause_before_dialogue=game.paused
	holds_pause=true
	game._set_paused(true,false)

func _release_pause() -> void:
	if not holds_pause: return
	holds_pause=false
	if not is_instance_valid(game): return
	# A menu layered over dialogue must retain its own pause until it closes.
	if game.menu_open: game.pause_before_menu=pause_before_dialogue
	if game._journal_is_open(): game.pause_before_journal=pause_before_dialogue
	game._set_paused(true if game._gameplay_input_blocked() else pause_before_dialogue,false)

func place_inbox() -> void:
	inbox_button.hide()

func open_station_health() -> void:
	if game==null or game._gameplay_input_blocked(): return
	if current.has("room_cell"):
		var cell:=Vector2i(int(current.room_cell[0]),int(current.room_cell[1]))
		if not game.occupied.has(cell) or game.occupied[cell].id!=current.room_id:
			current["room_missing"]=true; update_replies(); return
		game._locate_diagnostic_room("%d,%d"%[cell.x,cell.y])
		minimize(); return
	game._toggle_journal()
	game.journal_tabs.current_tab=1
	game._refresh_archive()
	panel.hide()
