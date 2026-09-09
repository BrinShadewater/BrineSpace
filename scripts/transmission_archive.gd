extends RefCounted
const OPENING := "CARRIER DETECTED // ORIGIN: A DISTANT STAR\n\nTransit time: 417 years. Sender: unverified.\nThe star is absent from the current catalogue.\nIts message has arrived anyway.\n\nBeneath an ocean on another world, a machine draws power.\nDormancy: 9,006 years. Maintenance requests: outstanding.\nHuman presence required.\nHuman presence: none.\n\nThe signal contains no orders. Only a voice.\n\"If anything is still listening...\nwe were here.\"\n\nBRINE // PETITION TO WAKE: APPROVED\nApproving authority: deceased.\n\nSomewhere above, the water moves."
const RECORDS := {
	"opening":{"title":"001 // The wake petition","text":OPENING},
	"receiver":{"title":"002 // Return address","text":"RECEIVER ARRAY // FRAGMENT RECOVERED\n\nThe signal repeats every nineteen minutes.\nThere is no transmitter on the chart.\n\nA child's breathing occupies the space between words.\nThe census lists no children aboard.\nThe census has not been amended in nine thousand years.\n\nRETURN ADDRESS: HOME\nPostal authority: dissolved."},
	"survey":{"title":"003 // Under the silt","text":"EXTERIOR RECORDER // PRESSURE-SEAL INTACT\n\nWe put the names inside the walls.\nNot for the company. For whoever came after.\n\nIf the lights are still working, leave one on.\nSomeone was supposed to meet us here.\n\nBRINE // RECORD RETAINED\nNo arrival time was supplied."}
}

static func available(meta) -> Array[String]:
	var result: Array[String] = ["opening"]
	for id in ["receiver","survey"]:
		if meta.recovered_memory_ids.has("transmission_"+id): result.append(id)
	return result

static func recover(game,id: String) -> void:
	var key := "transmission_"+id
	if not RECORDS.has(id) or game.meta.recovered_memory_ids.has(key): return
	game.meta.recovered_memory_ids[key] = true
	game.meta.unread_records[key] = true
	game.meta.save_to_disk()
	game._log("TRANSMISSION RECOVERED // " + RECORDS[id].title + ". Open Codex > Transmissions to replay.",false)
	game.play_station_sound("terminal")

static func survey_receivers(game) -> void:
	if game.meta.recovered_memory_ids.has("transmission_receiver"): return
	for room in game.placed_rooms:
		if room.id == "listening_post" and game.powered_room_cells.has(room.pos) and not room.get("suspended",false):
			recover(game,"receiver")
			return

static func populate(archive) -> void:
	archive.grid.add_child(archive._label("TRANSMISSIONS // RECOVERED SIGNALS",24))
	archive.grid.add_child(archive._label("Original recordings. Receiver fragments surface through exploration; their contents remain sealed until recovered.",17))
	for id in available(archive.meta_state):
		var button := Button.new()
		button.text = RECORDS[id].title + " // REPLAY"
		button.custom_minimum_size.y = 64
		preload("res://scripts/title_button_style.gd").apply(button,640,64)
		button.pressed.connect(func():
			var playback = load("res://scripts/loading_transition.gd").new()
			playback.transmission_text = RECORDS[id].text
			playback.replay_mode = true
			archive.get_tree().root.add_child(playback)
			archive.meta_state.mark_reviewed("transmission_"+id)
		)
		archive.grid.add_child(button)
	archive.grid.add_child(archive._label("Listen with a functioning Listening Post. Recover an exterior recorder on a crew salvage expedition.",17))
	for child in archive.grid.get_children():
		child.size_flags_horizontal = Control.SIZE_EXPAND_FILL
