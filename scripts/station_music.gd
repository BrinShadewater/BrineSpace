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
# Per slot: crossfade straight into the next track, or fade out and rest. Set by _order_playlist
# so the pairing is a property of the running order, not of how many tracks have played.
var pair_with_next: Array[bool] = []
var track_index := -1
var transition_age := 0.0
var duck_remaining := 0.0
var duck_db := 0.0
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
	_order_playlist()
	for i in range(2):
		var deck := AudioStreamPlayer.new()
		deck.bus = "Master"
		deck.volume_db = -80.0
		add_child(deck)
		deck.finished.connect(_on_finished.bind(deck))
		decks.append(deck)
	next_track()

# The rotation plays a pair back to back, then rests. Tracks that share a crossfade are chosen to
# sit close in brightness: the six seconds they overlap are the one moment two tracks are heard at
# once, and a dark ambient sliding into a bright one reads as a mistake rather than a transition.
# The bigger steps are saved for the rests, where silence resets the ear anyway.
func _order_playlist() -> void:
	# Own a mutable playlist; clearing it on exit must not empty the next instance.
	var clips: Array = (Bank.CLIPS.moonlit_canyon + Bank.CLIPS.moonlit_test_run + Bank.CLIPS.tracks_v1).duplicate()
	# Cosmetic ordering must not advance the station simulation's random sequence.
	clips.sort_custom(func(a, b): return Mix.brightness(a) < Mix.brightness(b))
	var single: Array = []
	if clips.size() % 2 == 1:
		# One track has to play alone. It should be the one with no close neighbour - dropping the
		# last of the sorted list instead would leave its lonely neighbour in somebody's crossfade.
		var loneliest := 0
		var best := INF
		for candidate in range(clips.size()):
			var rest: Array = clips.duplicate()
			rest.remove_at(candidate)
			var widest := 0.0
			for slot in range(0,rest.size(),2):
				widest = maxf(widest,absf(Mix.brightness(rest[slot])-Mix.brightness(rest[slot+1])))
			if widest < best:
				best = widest
				loneliest = candidate
		single = [clips[loneliest]]
		clips.remove_at(loneliest)
	var pairs: Array = []
	var index := 0
	while index + 1 < clips.size():
		var pair: Array = [clips[index], clips[index+1]]
		if music_rng.randi_range(0,1) == 1: pair.reverse()
		pairs.append(pair)
		index += 2
	for i in range(pairs.size()-1,0,-1):
		var other := music_rng.randi_range(0,i)
		var pair: Array = pairs[i]
		pairs[i] = pairs[other]
		pairs[other] = pair
	if not single.is_empty(): pairs.append(single) # alone, and last: a rotation opens on a pair
	playlist = []
	pair_with_next = []
	for pair in pairs:
		for slot in range(pair.size()):
			playlist.append(pair[slot])
			pair_with_next.append(slot == 0 and pair.size() == 2)

func next_track() -> void:
	rest_remaining = 0.0
	outgoing = player if is_instance_valid(player) and player.playing else null
	player = decks[1] if player == decks[0] else decks[0]
	player.stop()
	track_index += 1
	if track_index >= playlist.size():
		# A fresh pairing each time round; the same nine tracks in the same order for a whole
		# session is the other way music stops sounding composed.
		var last = playlist[playlist.size()-1]
		_order_playlist()
		track_index = 0
		if playlist.size() > 2 and playlist[0] == last:
			playlist.append(playlist.pop_front())
			pair_with_next.append(pair_with_next.pop_front())
	player.stream = playlist[track_index]
	player.volume_db = -80.0
	transition_age = 0.0
	player.play()

func _on_finished(deck: AudioStreamPlayer) -> void:
	if deck != player: return
	if not bool(pair_with_next[track_index]):
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
	if outgoing == null and bool(pair_with_next[track_index]) and player.stream.get_length()-player.get_playback_position() <= CROSSFADE_SECONDS:
		next_track()
	transition_age += delta
	var progress := clampf(transition_age/CROSSFADE_SECONDS,0.0,1.0)
	var ending := clampf((player.stream.get_length()-player.get_playback_position())/CROSSFADE_SECONDS,0.0,1.0) if not bool(pair_with_next[track_index]) else 1.0
	_set_level(player,minf(sin(progress*PI*0.5),ending))
	if outgoing != null:
		_set_level(outgoing,cos(progress*PI*0.5))
		if progress >= 1.0:
			outgoing.stop()
			outgoing.stream = null
			outgoing = null
