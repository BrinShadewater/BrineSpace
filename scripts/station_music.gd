extends Node
## Two decks preserve music across scenes and overlap track boundaries.
const Bank = preload("res://scripts/suno_audio_bank.gd")
const Mix = preload("res://scripts/station_audio_mix.gd")
const Preferences = preload("res://scripts/title_settings.gd")
const CROSSFADE_SECONDS := 6.0
var player: AudioStreamPlayer
var outgoing: AudioStreamPlayer
var decks: Array[AudioStreamPlayer] = []
var playlist: Array = []
var track_index := -1
var transition_age := 0.0
var duck_remaining := 0.0
var duck_db := 0.0
var tracks_started := 0
var rest_remaining := 0.0
var music_rng := RandomNumberGenerator.new()

static func ensure(owner: Node) -> Node:
	var root := owner.get_tree().root
	if root.has_meta("station_music"):
		var existing = root.get_meta("station_music").get_ref()
		if is_instance_valid(existing): return existing
	var music := new()
	music.name = "StationMusic"
	root.set_meta("station_music", weakref(music))
	root.add_child.call_deferred(music)
	return music

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	music_rng.randomize()
	# Own a mutable playlist; clearing it on exit must not empty the next instance.
	playlist = (Bank.CLIPS.moonlit_canyon + Bank.CLIPS.moonlit_test_run).duplicate()
	# Cosmetic ordering must not advance the station simulation's random sequence.
	for i in range(playlist.size()-1,0,-1):
		var other := music_rng.randi_range(0,i)
		var clip = playlist[i]
		playlist[i] = playlist[other]
		playlist[other] = clip
	for i in range(2):
		var deck := AudioStreamPlayer.new()
		deck.bus = "Master"
		deck.volume_db = -80.0
		add_child(deck)
		deck.finished.connect(_on_finished.bind(deck))
		decks.append(deck)
	next_track()

func next_track() -> void:
	rest_remaining = 0.0
	tracks_started += 1
	outgoing = player if is_instance_valid(player) and player.playing else null
	player = decks[1] if player == decks[0] else decks[0]
	player.stop()
	track_index = (track_index + 1) % playlist.size()
	player.stream = playlist[track_index]
	player.volume_db = -80.0
	transition_age = 0.0
	player.play()

func _on_finished(deck: AudioStreamPlayer) -> void:
	if deck != player: return
	if tracks_started % 2 == 0:
		deck.stop()
		outgoing = null
		rest_remaining = music_rng.randf_range(18.0,30.0)
	else:
		next_track()

func duck(seconds: float) -> void:
	duck_remaining = maxf(duck_remaining,seconds)

func _exit_tree() -> void:
	for deck in decks:
		deck.stop()
		deck.stream = null
	playlist.clear()

func _set_level(deck: AudioStreamPlayer, envelope: float) -> void:
	var gain := Preferences.music_volume * envelope
	deck.volume_db = -80.0 if gain <= 0.0001 else maxf(-80.0,-23.0 + Mix.gain(deck.stream) + duck_db + linear_to_db(gain))

func _process(delta: float) -> void:
	duck_remaining = maxf(0.0,duck_remaining-delta)
	duck_db = move_toward(duck_db,-5.0 if duck_remaining > 0.0 else 0.0,delta*(25.0 if duck_remaining > 0.0 else 2.5))
	if rest_remaining > 0.0:
		rest_remaining = maxf(0.0,rest_remaining-delta)
		if rest_remaining <= 0.0: next_track()
		return
	if outgoing == null and tracks_started % 2 != 0 and player.stream.get_length()-player.get_playback_position() <= CROSSFADE_SECONDS:
		next_track()
	transition_age += delta
	var progress := clampf(transition_age/CROSSFADE_SECONDS,0.0,1.0)
	var ending := clampf((player.stream.get_length()-player.get_playback_position())/CROSSFADE_SECONDS,0.0,1.0) if tracks_started % 2 == 0 else 1.0
	_set_level(player,minf(sin(progress*PI*0.5),ending))
	if outgoing != null:
		_set_level(outgoing,cos(progress*PI*0.5))
		if progress >= 1.0:
			outgoing.stop()
			outgoing.stream = null
			outgoing = null
