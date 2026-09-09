extends SceneTree
## Run: Godot --headless --path . --script res://tests/test_suno_audio.gd
const Bank = preload("res://scripts/suno_audio_bank.gd")
const Music = preload("res://scripts/station_music.gd")
const Mix = preload("res://scripts/station_audio_mix.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _init() -> void:
	call_deferred("run")
func run() -> void:
	Preferences.save_path = "user://audio_test_%d.cfg" % OS.get_process_id()
	var count := 0
	for clips in Bank.CLIPS.values():
		for clip in clips:
			count += 1
			check(clip.get_length() > 0.1,"Imported clip has duration: "+clip.resource_path)
			check(Mix.GAIN_DB.has(clip.resource_path),"Every runtime clip has a measured gain")
	check(count == 27,"All 27 owner files are runtime dependencies")
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://audio_test_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://audio_test_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = false
	var sound = game.station_sound
	sound.set_process(false)
	for kind in sound.voices: check(kind == "ui_comms","Startup does not replay restored room effects")
	game.crew_comms.set_process(false)
	sound._process(1.0)
	sound.last_event.clear()
	game.crew_comms.pending.clear()
	check(game.crew_comms.transmit("brine","Audio fixture report.","audio/report"),"New comms report accepted")
	check(sound.voices.has("ui_comms"),"Incoming report emits a receiver cue")
	sound._process(0.6)
	sound.last_event.clear()
	game.crew_comms.transmit("brine","Second report.","audio/report-two")
	check(not sound.voices.has("ui_comms"),"Queued follow-up does not repeat the receiver cue")
	check(not game.crew_comms.transmit("brine","Duplicate.","audio/report"),"Duplicate report stays silent")
	game.paused = true
	game._menu_save_game()
	check(FileAccess.file_exists(game.run_save_path) and sound.voices.has("ui_saved"),"Manual save has confirmation even while paused")
	sound._process(0.5)
	check(not sound.voices.has("ui_saved"),"Paused menu cue finishes normally")
	game.paused = false
	check(sound.layers.machinery is AudioStreamPlayer2D and sound.layers.pressure is AudioStreamPlayer,"Local machinery is positional; ocean stays global")
	for key in ["machinery","pressure","airlock","drone"]:
		check(sound.layers[key].stream is AudioStreamOggVorbis and sound.layers[key].stream.loop,"Runtime layer loops: "+key)
	check(sound.play_event("placement"),"First event plays")
	check(not sound.play_event("placement"),"Burst events do not stack")
	var first = sound.voices.placement.player.stream
	sound._process(2.2)
	check(not sound.voices.has("placement"),"Long effect stops within playback budget")
	check(sound.play_event("placement"),"Event plays again after cooldown")
	check(sound.voices.placement.player.stream != first,"Repeated events rotate supplied variants")
	Preferences.effects_volume = 0.0
	sound._process(0.01)
	check(sound.voices.placement.player.volume_db <= -80.0,"Effects control mutes an active cue")
	Preferences.effects_volume = 1.0
	Preferences.ambience_volume = 0.0
	sound._process(0.01)
	check(sound.layers.pressure.volume_db <= -80.0,"Ambience control mutes the ocean")
	Preferences.ambience_volume = 1.0
	game.paused = true
	sound._process(0.1)
	check(sound.voices.placement.player.stream_paused,"Pause holds active effects")
	check(not sound.play_event("cargo"),"Pause rejects new gameplay effects")
	check(sound.targets().drone == -80 and sound.targets().airlock == -80,"Pause silences moving systems")
	game.paused = false
	sound._process(3.0)
	sound.prior_powered.clear()
	game.powered_room_cells[game.placed_rooms[0].pos] = true
	sound._observe_station()
	check(sound.voices.has("power_on"),"Newly powered rooms trigger startup sound")
	game.resources.power = 0
	game._emit_warnings()
	check(sound.voices.has("warning"),"Actual warning event triggers audio")
	check(not sound.play_event("warning"),"Warnings are rate limited")
	sound._process(25.0)
	game._emit_warnings()
	check(not sound.voices.has("warning"),"Unchanged risk does not repeat every cycle")
	sound.update_warnings({})
	sound.update_warnings({"oxygen":true})
	check(sound.voices.has("warning"),"A new risk notifies after the cooldown")
	sound.update_warnings({})
	sound._process(1.0)
	check(not sound.voices.has("all_clear"),"Recovery waits for stable conditions")
	sound.update_warnings({"oxygen":true})
	sound._process(3.5)
	check(not sound.voices.has("all_clear"),"A returning risk cancels recovery feedback")
	sound.update_warnings({})
	game.paused = true
	sound._process(5.0)
	check(not sound.voices.has("all_clear"),"Pause does not advance recovery confirmation")
	game.paused = false
	sound._process(3.1)
	check(sound.voices.has("all_clear"),"Stable cleared risks produce recovery feedback")
	sound._process(1.0)
	sound.last_event.erase("all_clear")
	sound._process(4.0)
	check(not sound.voices.has("all_clear"),"Recovery notification does not repeat")
	for kind in sound.RECOVERY_EVENTS:
		sound._process(3.0)
		sound.last_event.clear()
		check(sound.play_event(kind),"Recovery cue is playable: "+kind)
	var cell := Vector2i(20,19)
	game._place_room("airlock",cell,true)
	game.powered_room_cells[cell] = true
	var original_rooms: Array = game.placed_rooms
	game.placed_rooms = [{"id":"corridor","category":"Engineering","pos":cell}]
	check(not sound.Space.sources(game).has("machinery"),"Corridors do not impersonate machinery")
	game.placed_rooms = original_rooms
	game.occupied[cell].airlock_cycle = {"phase":"flooding","elapsed":1.0}
	check(sound.targets().airlock > -80,"Powered flooding chamber sounds")
	game.occupied[cell].airlock_cycle.phase = "draining"
	check(sound.targets().airlock > -80,"Draining has a quieter water layer")
	game.occupied[cell].airlock_cycle.phase = "flooding"
	sound._process(0.2)
	check(sound.layers.airlock.playing,"Flooding starts its loop")
	game.powered_room_cells.erase(cell)
	check(sound.targets().airlock == -80,"Unpowered chamber is silent")
	sound._process(0.8)
	check(sound.voices.has("power_off"),"A room losing power has a shutdown cue")
	check(not sound.layers.airlock.playing,"Stopped motion releases its audio playback promptly")
	var saved_drones: Dictionary = game.drone_fleet.drones.duplicate(true)
	game.drone_fleet.drones = {cell:{"phase":"outbound"}}
	check(sound.targets().drone > -80,"Moving drone sounds")
	game.drone_fleet.drones[cell].phase = "docked"
	check(sound.targets().drone == -80,"Docked drone is silent")
	game.drone_fleet.drones = saved_drones
	check(sound.layers.size() == 9 and sound.layers.refrigeration.stream.loop_mode == AudioStreamWAV.LOOP_FORWARD,"New room beds loop within the fixed nine-layer budget")
	var saved_orders: Array = game.drone_fleet.orders.duplicate(true)
	game.drone_fleet.orders.clear()
	game.drone_fleet.drones = {cell:{"phase":"docked","home":cell,"kind":"construction","bootstrap":false,"order":{},"position":Vector2(cell)}}
	sound._observe_work(false)
	game.drone_fleet.drones[cell].phase = "launching"
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(sound.voices.has("launch"),"Drone departure triggers its launch cue")
	game.drone_fleet.drones[cell].order = {"pos":cell}
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(sound.voices.has("build_blocked"),"Assigned builder power loss triggers blocked feedback")
	sound._process(1.0)
	sound.last_event.erase("build_blocked")
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(not sound.voices.has("build_blocked"),"Unchanged blocked work stays quiet")
	game.drone_fleet.drones = saved_drones
	game.drone_fleet.orders = saved_orders
	var actors := []
	for id in preload("res://scripts/architects.gd").IDS:
		var actor = preload("res://scripts/architects.gd").actor_for(game,id)
		actors.append({"actor":actor,"active":actor.active,"foot":actor.foot,"state":actor.state,"medium":actor.movement_medium,"helmet":actor.helmet_equipped})
		actor.active = false
	var nearby = actors[0].actor
	nearby.active = true
	nearby.movement_medium = "dry"
	nearby.foot = (game.grid_view.get_global_transform().affine_inverse()*sound.Space.listener_position(game))/game.get_cell_size()*384.0
	nearby.state = "walk"
	sound._observe_work(false)
	nearby.foot += Vector2(8,0)
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(sound.voices.has("footstep"),"Nearby moving dry crew emits a footstep")
	sound._process(1.0)
	nearby.state = "repair"
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(sound.voices.has("repair"),"Nearby repair animation emits repair Foley")
	sound._process(1.0)
	nearby.helmet_equipped = false
	sound._observe_work(false)
	nearby.helmet_equipped = true
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(sound.voices.has("helmet_lock"),"Confirmed helmet fitting triggers its seal")
	sound._process(1.0)
	nearby.helmet_equipped = false
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(sound.voices.has("helmet_release"),"Confirmed helmet removal triggers release")
	sound._process(1.0)
	sound.last_event.erase("helmet_release")
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(not sound.voices.has("helmet_release"),"Unchanged equipment stays quiet")
	nearby.foot += Vector2(40000,0)
	nearby.state = "walk"
	sound.last_event.erase("footstep")
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(not sound.voices.has("footstep"),"Distant crew stays silent")
	sound._process(2.0) # Drain earlier equipment-test Foley before the independent swim check.
	nearby.foot = (game.grid_view.get_global_transform().affine_inverse()*sound.Space.listener_position(game))/game.get_cell_size()*384.0
	nearby.movement_medium = "exterior"
	sound._observe_work(false)
	nearby.foot += Vector2(8,0)
	sound.elapsed += 3.0
	sound.last_foley = -1000.0
	sound._observe_work(true)
	check(sound.voices.has("swim") or sound.voices.has("suit") or sound.voices.has("bubbles"),"Nearby moving underwater crew emits water/suit Foley")
	check(not sound.voices.has("footstep"),"Underwater movement does not emit dry footsteps")
	for entry in actors:
		entry.actor.active = entry.active
		entry.actor.foot = entry.foot
		entry.actor.state = entry.state
		entry.actor.movement_medium = entry.medium
		entry.actor.helmet_equipped = entry.helmet
	var room_backup: Array = game.placed_rooms
	var power_backup: Dictionary = game.powered_room_cells.duplicate()
	var center_cell := Vector2i(((game.grid_view.get_global_transform().affine_inverse()*sound.Space.listener_position(game))/game.get_cell_size()-Vector2.ONE*0.5).round())
	var site_backup: Dictionary = game.drone_fleet.sites
	game.drone_fleet.sites = {center_cell:{"units":1,"discovered":true}}
	sound._observe_work(false)
	game.drone_fleet.sites[center_cell].units = 0
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(sound.voices.has("site_empty"),"Newly depleted nearby deposit gives feedback")
	sound._process(1.0)
	sound.last_event.erase("site_empty")
	sound.elapsed += 1.0
	sound._observe_work(true)
	check(not sound.voices.has("site_empty"),"Empty deposit does not repeat its cue")
	game.drone_fleet.sites = site_backup
	game.placed_rooms = [{"id":"galley","pos":center_cell},{"id":"med_bay","pos":center_cell+Vector2i.RIGHT},{"id":"research_lab","pos":center_cell+Vector2i.DOWN},{"id":"hydroponics_bay","pos":center_cell+Vector2i.LEFT}]
	for room in game.placed_rooms: game.powered_room_cells[room.pos] = true
	var activity_sources: Dictionary = sound.Space.sources(game)
	for kind in sound.ROOM_EVENTS: check(activity_sources.has(kind),"Functioning room supplies its activity source: "+kind)
	sound.source_cells = activity_sources
	sound.elapsed += 15.0
	sound.last_event.clear()
	sound.last_room_activity = -1000.0
	sound._observe_work(true)
	var room_audible := false
	for kind in sound.ROOM_EVENTS: room_audible = room_audible or sound.voices.has(kind)
	check(room_audible,"Nearby functioning room emits activity through the observer")
	game.placed_rooms[0].suspended = true
	check(not sound.Space.sources(game).has("galley_work"),"Suspended room activity is silent")
	game.powered_room_cells.clear()
	check(not sound.Space.sources(game).has("medical_work"),"Nonfunctioning room activity is silent")
	game.placed_rooms = room_backup
	game.powered_room_cells = power_backup
	sound.source_cells = sound.Space.sources(game)
	game.drone_fleet.drones = {cell:{"phase":"working","kind":"mining","position":Vector2(cell),"battery":2.0}}
	check(sound.Space.sources(game).has("mining_work"),"Active mining provides a work sound source")
	game.drone_fleet.drones[cell].kind = "salvage"
	check(sound.Space.sources(game).has("salvage_work"),"Active salvage provides a work sound source")
	game.drone_fleet.drones[cell].battery = 0.0
	check(not sound.Space.sources(game).has("salvage_work"),"Exhausted drone work is silent")
	game.drone_fleet.drones[cell].battery = 2.0
	game.drone_fleet.drones[cell].phase = "returning"
	check(not sound.Space.sources(game).has("salvage_work"),"Returning drone no longer emits work activity")
	game.drone_fleet.drones = saved_drones
	for kind in sound.EXPANDED_EVENTS:
		sound._process(15.0)
		sound.last_event.clear()
		sound.last_foley = -1000.0
		sound.last_room_activity = -1000.0
		check(sound.play_event(kind),"Expanded activity cue plays: "+kind)
	for condition in ["oxygen","integrity","power_reserve"]:
		sound._process(3.0)
		sound.warning_state = {condition:true}
		sound.last_event.erase("warning")
		check(sound.play_event("warning"),"Specialized warning starts")
		check(sound.voices.warning.player.stream == sound.Cues.get_stream(sound.warning_cue(sound.warning_state)),"Hazard selects its distinct warning stream: "+condition)
	check(sound.warning_cue({"oxygen":true,"integrity":true,"power_reserve":true}) == "warning_oxygen","Simultaneous risks select one priority warning")
	check(sound.layers.size() == 9,"Expanded activity does not add continuous layers")
	sound._process(5.0)
	sound.last_event.clear()
	sound.last_foley = -1000.0
	check(sound.play_event("footstep"),"Variation fixture starts a footstep")
	var step = sound.voices.footstep.player
	check(step.pitch_scale >= 0.96 and step.pitch_scale <= 1.04,"Foley pitch stays within a subtle range")
	check(not sound.play_event("tools"),"Different crew cues share a burst limit")
	# Force the slow edge to verify cleanup follows actual playback duration.
	step.pitch_scale = 0.96
	var original_length: float = step.stream.get_length()
	sound._process(original_length+0.001)
	check(sound.voices.has("footstep"),"Slower cue keeps its tail beyond the unpitched duration")
	sound._process(0.1)
	check(not sound.voices.has("footstep"),"Varied cue is released after its pitched duration")
	for kind in sound.ACTIVITY_EVENTS:
		sound._process(5.0)
		sound.last_event.clear()
		check(sound.play_event(kind),"Created activity cue plays: "+kind)
		sound._process(3.0)
		check(not sound.voices.has(kind),"Activity cue releases: "+kind)
	for kind in sound.EVENTS:
		sound._process(25.0)
		sound.last_event.clear() # Ambient creaks may fire during simulated time advancement.
		check(sound.play_event(kind),"Event stream playable: "+kind)
	var music = Music.ensure(game)
	# Clear prior cues and exercise a tiny click before priority masking.
	sound._process(10.0)
	sound.last_event.clear()
	check(sound.play_event("ui_select"),"Short UI cue starts")
	sound._process(0.02)
	check(is_equal_approx(sound.voices.ui_select.player.volume_db,float(sound.voices.ui_select.gain)),"Short cue retains its attack")
	sound._process(0.2)
	check(not sound.voices.has("ui_select"),"Short cue releases after its duration")
	check(sound.play_event("warning"),"Priority cue starts for ambience check")
	sound._process(0.2)
	check(is_equal_approx(sound.ambience_duck_db,-3.0),"Priority cue gently lowers ambience")
	Preferences.effects_volume = 0.0
	sound._process(0.25)
	check(sound.ambience_duck_db > -3.0 and sound.ambience_duck_db < 0.0,"Muted effects release ambience duck gradually")
	sound._process(2.0)
	check(is_zero_approx(sound.ambience_duck_db),"Ambience returns after priority audio is muted")
	Preferences.effects_volume = 1.0
	await process_frame
	check(Music.ensure(game) == music,"Playlist is singleton across callers")
	check(music.playlist.size() == 4 and music.player.playing,"All four Moonlit tracks in playing playlist")
	music.set_process(false)
	music._process(7.0)
	var previous = music.player
	music.player.seek(music.player.stream.get_length()-5.0)
	music._process(0.1)
	check(music.outgoing == previous and music.player != previous,"Track boundary starts the second deck automatically")
	music._process(2.9)
	check(music.player.playing and music.outgoing.playing,"Both tracks overlap during the crossfade")
	check(music.player.volume_db > -60.0 and music.outgoing.volume_db > -60.0,"Crossfade has no silent midpoint")
	var retiring = music.outgoing
	music._process(3.1)
	check(music.outgoing == null and not retiring.playing,"Finished fade releases the previous track")
	music.duck(2.0)
	music._process(0.25)
	check(music.duck_db <= -4.0,"Priority cue gently lowers music")
	music._process(5.0)
	check(is_zero_approx(music.duck_db),"Music returns after the cue")
	var tracks := {}
	for i in range(4):
		tracks[music.player.stream.resource_path] = true
		music.next_track()
	check(tracks.size() == 4,"Track completion advances through every Moonlit track")
	music.tracks_started = 2
	music.player.finished.emit()
	check(music.rest_remaining >= 18.0 and music.rest_remaining <= 30.0 and not music.player.playing,"Every second track leaves a bounded quiet interval")
	music._process(31.0)
	check(music.rest_remaining == 0.0 and music.player.playing,"Music resumes after its quiet interval")
	Preferences.music_volume = 0.0
	music._process(5.0)
	check(music.player.volume_db <= -80,"Music can be silenced independently")
	if music.outgoing != null: check(music.outgoing.volume_db <= -80,"Music mute covers both crossfade decks")
	Preferences.music_volume = 0.37
	Preferences.effects_volume = 0.62
	Preferences.ambience_volume = 0.41
	check(Preferences.save(root) == OK,"Audio preference saves")
	var config := ConfigFile.new()
	config.load(Preferences.save_path)
	check(is_equal_approx(float(config.get_value("audio","music_volume")),0.37),"Music volume persists")
	check(is_equal_approx(float(config.get_value("audio","effects_volume")),0.62),"Effects volume persists")
	check(is_equal_approx(float(config.get_value("audio","ambience_volume")),0.41),"Ambience volume persists")
	Preferences.muted = true
	Preferences.apply_runtime(root)
	check(AudioServer.is_bus_mute(0) and music.player.bus == "Master","Master mute covers soundtrack")
	Preferences.muted = false
	Preferences.mute_unfocused = true
	Preferences._on_focus(false)
	check(AudioServer.is_bus_mute(0),"Focus-loss mute covers all audio")
	Preferences._on_focus(true)
	check(not AudioServer.is_bus_mute(0),"Focus restores audio")
	game.expedition_mode = true
	sound.last_event.clear()
	game._end_expedition()
	check(not game.running and sound.voices.has("ui_end"),"Conclude Expedition plays its outcome after the run stops")
	sound._process(0.5)
	check(sound.voices.has("ui_end"),"Outcome cue survives stopped gameplay")
	sound._process(2.0)
	check(not sound.voices.has("ui_end"),"Outcome cue ends cleanly")
	game.queue_free()
	await process_frame
	check(is_instance_valid(music) and music.player.playing,"Playlist survives gameplay scene exit")
	music.queue_free()
	await process_frame
	await create_timer(0.15).timeout # Let the audio mixer release stopped Ogg playback.
	print("SUNO AUDIO PASS" if failures == 0 else "SUNO AUDIO FAIL: %d" % failures)
	quit(failures)
