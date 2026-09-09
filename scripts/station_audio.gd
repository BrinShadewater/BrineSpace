extends Node
## Owner-supplied Suno layers and events; synthesized receiver remains as a quiet bed.
const Bank = preload("res://scripts/suno_audio_bank.gd")
const Mix = preload("res://scripts/station_audio_mix.gd")
const Space = preload("res://scripts/station_audio_space.gd")
const Cues = preload("res://scripts/station_audio_cues.gd")
const Preferences = preload("res://scripts/title_settings.gd")
const Airlock = preload("res://scripts/airlock_cycle.gd")
const AirlockService = preload("res://scripts/airlock_service.gd")
const LAYER_ASSETS := {"machinery":"interior", "pressure":"ocean", "airlock":"airlock", "drone":"drone", "life_support":"interior"}
const LOCAL_LAYERS := ["machinery","airlock","drone","life_support","core","receiver","refrigeration","workshop"]
# Level dB, cooldown seconds, playback limit. One voice per event kind.
const EVENTS := {"placement":[-12.0,0.35,2.0], "power_on":[-21.0,6.0,4.0], "door":[-20.0,2.5,2.0], "cargo":[-18.0,2.0,2.5], "terminal":[-15.0,4.0,3.0], "discovery":[-13.0,5.0,5.0], "warning":[-13.0,20.0,2.5], "ui_select":[-22.0,0.08,0.1], "ui_reject":[-18.0,0.25,0.2], "power_off":[-24.0,8.0,1.2], "hull":[-30.0,45.0,2.6]}
const PRIORITY_EVENTS := ["warning","discovery","terminal","ui_end","ui_failure"]
const ACTIVITY_EVENTS := {"build_complete":[-20.0,2.0,0.65],"build_blocked":[-24.0,15.0,0.5],"launch":[-27.0,4.0,0.8],"footstep":[-25.0,0.6,0.12],"tools":[-27.0,3.0,0.35],"repair":[-27.0,3.0,0.6],"ui_end":[-18.0,4.0,2.0],"ui_failure":[-18.0,4.0,2.0]}
const UI_EVENTS := {"ui_comms":[-23.0,8.0,0.5],"ui_saved":[-21.0,1.0,0.35]}
const RECOVERY_EVENTS := {"all_clear":[-23.0,20.0,0.7],"crew_dispatch":[-23.0,2.0,0.4],"crew_awake":[-21.0,5.0,1.2],"airlock_pressure":[-26.0,2.0,1.5],"airlock_release":[-24.0,1.0,0.45],"airlock_ready":[-25.0,2.0,0.4],"ui_recall":[-23.0,2.0,0.45],"crew_return":[-22.0,3.0,0.6]}
var clear_pending := false
var clear_age := 0.0
const EXPANDED_EVENTS := {"swim":[-25.0,1.0,0.65],"suit":[-28.0,2.5,0.35],"bubbles":[-29.0,6.0,0.85],"mining_work":[-27.0,2.5,1.5],"salvage_work":[-27.0,2.5,1.2],"galley_work":[-29.0,9.0,0.65],"medical_work":[-31.0,12.0,0.9],"lab_work":[-31.0,10.0,1.0],"cultivation_work":[-29.0,10.0,1.4]}
const ROOM_EVENTS := ["galley_work","medical_work","lab_work","cultivation_work"]
var last_room_activity := -1000.0
const EQUIPMENT_EVENTS := {"helmet_lock":[-25.0,2.0,0.35],"helmet_release":[-26.0,2.0,0.45],"site_empty":[-24.0,8.0,0.75]}
var prior_helmets := {}
var prior_site_units := {}
var game
var receiver_only := false
var layers := {}
var layer_gains := {}
var elapsed := 0.0
var voices := {}
var last_event := {}
var variant_index := {}
var prior_powered := {}
var prior_airlocks := {}
var observation_time := 0.0
var prior_doors := {}
var warning_state := {}
var warning_last_played := -1000.0
var audio_rng := RandomNumberGenerator.new()
var listener: AudioListener2D
var source_cells := {}
var hull_remaining := 60.0
var ambience_duck_db := 0.0
var previous_drones := {}
var blocked_orders := {}
var work_observed_at := -1000.0
var crew_positions := {}
const VARIED_EVENTS := ["footstep","tools","repair","launch","hull","swim","suit","bubbles","mining_work","salvage_work","galley_work","cultivation_work"]
const FOLEY_EVENTS := ["footstep","tools","repair","swim","suit","bubbles"]
var last_foley := -1000.0
static var streams := {}

static func tone(kind: String) -> AudioStreamWAV:
	if streams.has(kind): return streams[kind]
	const RATE := 22050
	const FRAMES := RATE * 4
	var bytes := PackedByteArray()
	bytes.resize(FRAMES*2)
	var random := RandomNumberGenerator.new()
	random.seed = 811
	var filtered := 0.0
	for i in range(FRAMES):
		var t := float(i)/RATE
		var noise := random.randf_range(-1.0,1.0)
		filtered = lerpf(filtered,noise,0.025)
		var sample := 0.0
		match kind:
			"machinery": sample = sin(TAU*48*t)*0.34 + sin(TAU*96*t)*0.12 + filtered*0.5
			"pressure": sample = sin(TAU*33*t)*sin(PI*t/4)*0.22 + filtered*0.7
			"receiver": sample = noise*0.12 + sin(TAU*760*t)*pow(maxf(0,sin(TAU*0.75*t)),12)*0.10
		# Seamless loop endpoints; keep headroom when layers overlap.
		var edge := minf(1.0,minf(t,4.0-t)/0.04)
		bytes.encode_s16(i*2,int(clampf(sample*edge,-1,1)*32767))
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_16_BITS
	stream.mix_rate = RATE
	stream.data = bytes
	stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	stream.loop_end = FRAMES
	streams[kind] = stream
	return stream

func _ready() -> void:
	name = "StationAudio"
	audio_rng.randomize() # Cosmetic variation must not consume the gameplay RNG.
	hull_remaining = audio_rng.randf_range(55.0,95.0)
	if is_instance_valid(game):
		listener = AudioListener2D.new()
		add_child(listener)
		listener.position = Space.listener_position(game)
		listener.make_current()
	for kind in (["receiver"] if receiver_only else ["machinery","pressure","receiver","airlock","drone","life_support","core","refrigeration","workshop"]):
		var player = AudioStreamPlayer2D.new() if is_instance_valid(game) and kind in LOCAL_LAYERS else AudioStreamPlayer.new()
		if LAYER_ASSETS.has(kind):
			var choices: Array = Bank.CLIPS[LAYER_ASSETS[kind]]
			var source: AudioStream = choices[audio_rng.randi_range(0,choices.size()-1)]
			layer_gains[kind] = Mix.gain(source)
			var stream: AudioStreamOggVorbis = source.duplicate()
			stream.loop = true
			player.stream = stream
		elif kind in ["core","refrigeration","workshop"]:
			player.stream = Cues.get_stream(kind)
		else:
			player.stream = tone(kind)
		player.volume_db = -80
		add_child(player)
		if player is AudioStreamPlayer2D: Space.configure(player,game,Vector2(20,20))
		if kind not in ["airlock","drone"]:
			player.play(audio_rng.randf()*player.stream.get_length() if kind in ["machinery","pressure"] else 0.0)
		layers[kind] = player
	if is_instance_valid(game):
		prior_powered = game.powered_room_cells.duplicate()
		_observe_station(false)
	if receiver_only: play_event("terminal")

func play_event(kind: String, cell := Vector2.INF) -> bool:
	if event_settings(kind).is_empty(): return false
	if is_instance_valid(game) and (not game.running or game.paused) and not kind.begins_with("ui_"): return false
	var settings: Array = event_settings(kind)
	if elapsed - float(last_event.get(kind,-1000.0)) < float(settings[1]) or voices.has(kind): return false
	if kind in ROOM_EVENTS and elapsed-last_room_activity < 4.0: return false
	if kind in FOLEY_EVENTS and elapsed-last_foley < 0.6: return false
	if kind in FOLEY_EVENTS:
		for other in FOLEY_EVENTS:
			if voices.has(other): return false
	var choices: Array = Bank.CLIPS[kind] if Bank.CLIPS.has(kind) else [Cues.get_stream(kind)]
	if kind == "warning":
		var specialized := warning_cue(warning_state)
		if not specialized.is_empty(): choices = [Cues.get_stream(specialized)]
	if not variant_index.has(kind): variant_index[kind] = audio_rng.randi_range(0,choices.size()-1)
	var index := int(variant_index[kind]) % choices.size()
	variant_index[kind] = index+1
	if cell == Vector2.INF and kind == "cargo": cell = source_cells.get("drone",Vector2.INF)
	var spatial := cell != Vector2.INF and is_instance_valid(game) and kind not in PRIORITY_EVENTS
	var player = AudioStreamPlayer2D.new() if spatial else AudioStreamPlayer.new()
	player.stream = choices[index]
	player.volume_db = float(settings[0]) + Mix.gain(player.stream)
	if kind in VARIED_EVENTS:
		player.pitch_scale = audio_rng.randf_range(0.96,1.04)
		player.volume_db += audio_rng.randf_range(-1.0,0.5)
	add_child(player)
	if spatial: Space.configure(player,game,cell)
	var original_gain: float = player.volume_db
	player.volume_db = -80.0 if Preferences.effects_volume <= 0.0 else original_gain + linear_to_db(Preferences.effects_volume)
	player.play()
	voices[kind] = {"player":player,"age":0.0,"gain":original_gain,"duck":0.0,"cell":cell}
	last_event[kind] = elapsed
	if kind in ROOM_EVENTS: last_room_activity = elapsed
	if kind in FOLEY_EVENTS: last_foley = elapsed
	if kind in PRIORITY_EVENTS and Preferences.effects_volume > 0.0 and get_tree().root.has_meta("station_music"):
		var music = get_tree().root.get_meta("station_music").get_ref()
		if is_instance_valid(music): music.duck(player.stream.get_length()+0.5)
	return true

func reset_after_restore() -> void:
	for voice in voices.values():
		voice.player.stop()
		voice.player.queue_free()
	voices.clear()
	prior_powered = game.powered_room_cells.duplicate()
	_observe_station(false)
	clear_pending = false
	clear_age = 0.0

static func warning_cue(conditions: Dictionary) -> String:
	if conditions.has("oxygen"): return "warning_oxygen"
	if conditions.has("integrity"): return "warning_hull"
	if conditions.has("power_shortfall") or conditions.has("power_reserve"): return "warning_power"
	return ""

func event_settings(kind: String) -> Array:
	if kind=="companion_chirp":return [-30.0,18.0,0.5]
	for group in [EVENTS,ACTIVITY_EVENTS,UI_EVENTS,RECOVERY_EVENTS,EXPANDED_EVENTS,EQUIPMENT_EVENTS]:
		if group.has(kind): return group[kind]
	return []

func update_warnings(conditions: Dictionary) -> void:
	if not is_instance_valid(game) or not game.running or game.paused: return
	var changed := false
	for key in conditions:
		if not warning_state.has(key): changed = true
	if not conditions.is_empty():
		clear_pending = false
		clear_age = 0.0
	elif not warning_state.is_empty():
		clear_pending = true
		clear_age = 0.0
	warning_state = conditions.duplicate()
	# Notify new risks; unchanged conditions only get a 90-second reminder.
	if not conditions.is_empty() and (changed or elapsed-warning_last_played >= 90.0):
		if play_event("warning"): warning_last_played = elapsed

func _exit_tree() -> void:
	for child in get_children():
		if child is AudioStreamPlayer or child is AudioStreamPlayer2D:
			child.stop()
			child.stream = null
	voices.clear()
	layers.clear()

func targets() -> Dictionary:
	if receiver_only: return {"receiver":-29.0}
	if not is_instance_valid(game) or not game.running: return {"machinery":-80.0,"pressure":-80.0,"receiver":-80.0,"airlock":-80.0,"drone":-80.0,"life_support":-80.0,"core":-80.0,"refrigeration":-80.0,"workshop":-80.0}
	var powered: bool = not game.powered_room_cells.is_empty()
	var listening := false
	var flooding := false
	var moving := false
	var life_support := false
	var core := false
	var draining := false
	for room in game.placed_rooms:
		if game.powered_room_cells.has(room.pos) and not room.get("suspended",false):
			if room.id in ["life_support","hydroponics_bay","biodome"]: life_support = true
			if room.id == "brine_core": core = true
		if room.id == "listening_post" and game.powered_room_cells.has(room.pos): listening = true
		if room.id == "airlock" and not game.paused and AirlockService.ready(game,room.pos):
			if Airlock.state(room).phase == "flooding": flooding = true
			if Airlock.state(room).phase == "draining": draining = true
	if not game.paused:
		for drone in game.drone_fleet.drones.values():
			if drone.phase in ["launching","outbound","returning","docking"]: moving = true
	return {
		"machinery":-28.0 if powered else -80.0,
		"pressure":lerpf(-35.0,-27.0,clampf((65.0-float(game.resources.integrity))/45.0,0.0,1.0)),
		"receiver":-36.0 if listening else -80.0,
		"airlock":-17.0 if flooding else (-20.0 if draining else -80.0),
		"drone":-30.0 if moving else -80.0,
		"life_support":-32.0 if life_support else -80.0,
		"core":-33.0 if core else -80.0,
		"refrigeration":-32.0 if source_cells.has("refrigeration") else -80.0,
		"workshop":-35.0 if source_cells.has("workshop") and not game.paused else -80.0
	}

func _observe_station(audible := true) -> void:
	if not is_instance_valid(game): return
	source_cells = Space.sources(game)
	_observe_work(audible)
	if audible:
		for cell in prior_powered:
			if game.occupied.has(cell) and not game.powered_room_cells.has(cell):
				play_event("power_off",Vector2(cell))
				break
	for cell in game.powered_room_cells:
		if audible and not prior_powered.has(cell): play_event("power_on",Vector2(cell))
	prior_powered = game.powered_room_cells.duplicate()
	var phases := {}
	for room in game.placed_rooms:
		if room.id != "airlock": continue
		var phase: String = Airlock.state(room).phase
		phases[room.pos] = phase
		if audible and phase != prior_airlocks.get(room.pos,phase) and phase in ["flooding","draining"]:
			play_event("door",Vector2(room.pos))
		if audible and phase != prior_airlocks.get(room.pos,phase) and AirlockService.ready(game,room.pos):
			if phase in ["equalizing","depressurizing"]: play_event("airlock_pressure",Vector2(room.pos))
			elif phase in ["opening_outer","opening_inner"]: play_event("airlock_release",Vector2(room.pos))
			elif phase in ["dry","exterior"]: play_event("airlock_ready",Vector2(room.pos))
	prior_airlocks = phases
	# Reuse actual visible door frames; sound only a completed closure.
	var doors := {}
	if is_instance_valid(game.grid_view):
		for entry in game.grid_view.door_surface_key:
			if not entry is Array or entry.size() != 7: continue
			var key := str(entry[0])+":"+str(entry[1])
			var frame := int(entry[2])
			doors[key] = frame
			if audible and frame == 0 and int(prior_doors.get(key,0)) > 0: play_event("door",Vector2(entry[0]))
	prior_doors = doors

func _observe_work(audible: bool) -> void:
	if audible and elapsed-work_observed_at < 0.8: return
	work_observed_at = elapsed
	var site_units := {}
	for cell in game.drone_fleet.sites:
		var site: Dictionary = game.drone_fleet.sites[cell]
		site_units[cell] = int(site.units)
		if audible and site.get("discovered",false) and int(prior_site_units.get(cell,site.units)) > 0 and int(site.units) == 0:
			if Space.screen_position(game,Vector2(cell)).distance_to(Space.listener_position(game)) < game.get_cell_size()*3.0:
				play_event("site_empty",Vector2(cell))
	prior_site_units = site_units
	var blocked := {}
	for home in game.drone_fleet.drones:
		var drone: Dictionary = game.drone_fleet.drones[home]
		if audible and previous_drones.get(home,drone.phase) == "docked" and drone.phase in ["launching","outbound"]:
			play_event("launch",Vector2(home))
		previous_drones[home] = drone.phase
		if not drone.get("order",{}).is_empty() and not drone.get("bootstrap",false) and not game.powered_room_cells.has(home):
			blocked[drone.order.pos] = true
	for order in game.drone_fleet.orders:
		var route_available := false
		for drone in game.drone_fleet.drones.values():
			if drone.kind != "construction": continue
			if not game.drone_fleet.Routes.find_path(drone.home,order.pos,game.drone_fleet.route_blockers).is_empty():
				route_available = true
				break
		if not route_available: blocked[order.pos] = true
	for cell in blocked:
		if audible and not blocked_orders.has(cell): play_event("build_blocked",Vector2(cell))
	blocked_orders = blocked
	var nearest := INF
	var chosen_kind := ""
	var chosen_cell := Vector2.ZERO
	for id in preload("res://scripts/architects.gd").IDS:
		var actor = preload("res://scripts/architects.gd").actor_for(game,id)
		var helmet_changed: bool = prior_helmets.has(id) and prior_helmets[id] != actor.helmet_equipped
		prior_helmets[id] = actor.helmet_equipped
		var moved: bool = crew_positions.has(id) and actor.foot.distance_to(crew_positions[id]) > 2.0
		crew_positions[id] = actor.foot
		if not actor.active: continue
		var cell: Vector2 = actor.foot/384.0-Vector2.ONE*0.5
		var distance := Space.screen_position(game,cell).distance_to(Space.listener_position(game))
		if distance > game.get_cell_size()*2.5 or distance >= nearest: continue
		if audible and helmet_changed: play_event("helmet_lock" if actor.helmet_equipped else "helmet_release",cell)
		var kind := "footstep" if moved and actor.state == "walk" else ("tools" if actor.activity in ["checking equipment","inspecting recovered machinery"] else "")
		if actor.state == "repair": kind = "repair"
		if actor.movement_medium != "dry":
			kind = ""
			if moved:
				var roll := audio_rng.randf()
				kind = "swim" if roll < 0.65 else ("suit" if roll < 0.85 else "bubbles")
		if kind.is_empty(): continue
		nearest = distance
		chosen_kind = kind
		chosen_cell = cell
	if audible and not chosen_kind.is_empty(): play_event(chosen_kind,chosen_cell)
	if audible:
		var work_kind := ""
		var work_cell := Vector2.ZERO
		var work_distance: float = game.get_cell_size()*3.0
		for kind in ["mining_work","salvage_work"]+ROOM_EVENTS:
			if not source_cells.has(kind): continue
			if kind in ROOM_EVENTS and elapsed-last_room_activity < 4.0: continue
			var cell: Vector2 = source_cells[kind]
			var distance := Space.screen_position(game,cell).distance_to(Space.listener_position(game))
			var settings: Array = event_settings(kind)
			if voices.has(kind) or elapsed-float(last_event.get(kind,-1000.0)) < float(settings[1]): continue
			if distance < work_distance:
				work_distance = distance
				work_kind = kind
				work_cell = cell
		if not work_kind.is_empty(): play_event(work_kind,work_cell)

func _process(delta: float) -> void:
	elapsed += delta
	if clear_pending and is_instance_valid(game) and game.running and not game.paused:
		clear_age += delta
	if is_instance_valid(listener): listener.position = Space.listener_position(game)
	if is_instance_valid(game) and game.running and not game.paused:
		hull_remaining -= delta
		if hull_remaining <= 0.0:
			play_event("hull")
			hull_remaining = audio_rng.randf_range(55.0,95.0)
	observation_time += delta
	if observation_time >= 0.2:
		observation_time = 0.0
		_observe_station()
	var levels := targets()
	var priority_active := false
	if Preferences.effects_volume > 0.0 and (not is_instance_valid(game) or (game.running and not game.paused)):
		for important in PRIORITY_EVENTS:
			if voices.has(important): priority_active = true
	# Leave priority reports space without making the station disappear.
	ambience_duck_db = move_toward(ambience_duck_db,-3.0 if priority_active else 0.0,delta*(15.0 if priority_active else 2.0))
	for kind in layers:
		var player = layers[kind]
		var target := float(levels[kind])
		if player is AudioStreamPlayer2D:
			if source_cells.has(kind): Space.configure(player,game,source_cells[kind])
			else: target = -80.0
		if kind in ["airlock","drone"] and target > -80.0 and not player.playing: player.play()
		if target > -80.0: target += float(layer_gains.get(kind,0.0))
		var smoothing := 12.0 if kind in ["airlock","drone"] else 2.0
		# Keep an unscaled envelope so changing preferences does not fight the fade.
		var base: float = player.get_meta("base_amplitude",0.0001)
		base = lerpf(base,db_to_linear(target),1.0-exp(-delta*smoothing))
		player.set_meta("base_amplitude",base)
		player.volume_db = maxf(-80.0,linear_to_db(maxf(0.0001,base*Preferences.ambience_volume))+ambience_duck_db)
		if kind in ["airlock","drone"] and target <= -80.0 and player.volume_db <= -65.0: player.stop()
	for kind in voices.keys():
		var voice: Dictionary = voices[kind]
		var player = voice.player
		if player is AudioStreamPlayer2D: Space.configure(player,game,voice.cell)
		player.stream_paused = is_instance_valid(game) and game.paused and not kind.begins_with("ui_")
		if not player.stream_paused: voice.age += delta
		var settings: Array = event_settings(kind)
		var limit: float = minf(float(settings[2]),player.stream.get_length())/player.pitch_scale
		if voice.age >= limit or (is_instance_valid(game) and not game.running and not kind.begins_with("ui_")):
			player.stop()
			player.queue_free()
			voices.erase(kind)
		else:
			# Tiny clicks keep their attack; longer effects retain a soft tail.
			var fade_seconds := minf(0.2,limit*0.25)
			var fade := clampf((limit-float(voice.age))/fade_seconds,0.0001,1.0)
			var attenuation := -4.0 if priority_active and kind not in PRIORITY_EVENTS else 0.0
			voice.duck = move_toward(float(voice.duck),attenuation,delta*24.0)
			player.volume_db = -80.0 if Preferences.effects_volume <= 0.0 else float(voice.gain) + float(voice.duck) + linear_to_db(fade*Preferences.effects_volume)
	if clear_pending and clear_age >= 3.0 and play_event("all_clear"): clear_pending = false
