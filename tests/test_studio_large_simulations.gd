extends SceneTree
## Studio large-room simulations (owner, Sept 29): the tidal plant fills and drains, the moonbay sends its
## sub out and brings it back, on the same tables the live game uses, and nothing else changes.
const Effects = preload("res://scripts/studio_effect_preview.gd")
const StudioView = preload("res://rooms/large-rooms/studio_view.gd")
var failures := 0

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		push_error(label)

func ids(room_id: String) -> Array:
	var e = Effects.new()
	e.room_id = room_id
	return e.actions().map(func(a): return a[1])

func run_for(e, seconds: float) -> void:
	var t := 0.0
	while t < seconds:
		e.advance(0.05)
		t += 0.05

func _init() -> void: call_deferred("run")

func run() -> void:
	check(ids("tidal_power_plant").has("tidal_fill") and ids("tidal_power_plant").has("tidal_drain"), "Tidal plant offers fill and drain")
	check(ids("moonbay").has("sub_out") and ids("moonbay").has("sub_back"), "Moonbay offers send out and bring back")
	check(not ids("hydroponics_farm").has("tidal_fill") and not ids("storage_depot").has("sub_out"), "Rooms with no machine state offer nothing")

	var e = Effects.new()
	e.room_id = "tidal_power_plant"
	check(e.tidal_state().is_empty() and not e.active(), "Idle tidal preview leaves the room's own state")
	e.start("tidal_fill")
	run_for(e, 3.0)
	var half: Dictionary = e.tidal_state()
	check(absf(float(half.water) - 0.5) < 0.05 and not half.spinning, "Halfway through the fill the chamber is half full and still")
	run_for(e, 6.0)
	check(float(e.tidal_state().water) >= 1.0 and e.tidal_state().spinning, "Once full the rotor spins")
	var angle_a: float = e.tidal_state().rotor_angle
	run_for(e, 0.5)
	check(e.tidal_state().rotor_angle != angle_a, "The rotor keeps turning")
	e.start("tidal_drain")
	run_for(e, 2.5)
	check(absf(float(e.tidal_state().water) - 0.5) < 0.06 and not e.tidal_state().spinning, "Draining takes the water down and stops the rotor")
	e.clear()
	check(e.tidal_state().is_empty() and not e.active(), "Clear returns control to the room")

	var m = Effects.new()
	m.room_id = "moonbay"
	m.start("sub_back")
	check(m.moonbay.is_empty(), "Bringing the sub back with none out does nothing")
	m.start("sub_out")
	check(not m.moonbay.is_empty() and m.active(), "Send sub out starts the trip")
	run_for(m, 3.5)
	check(m.moonbay.phase == "flood" and not m.moonbay.station_open, "The inner door seals, then the chamber floods")
	run_for(m, 6.0)
	check(m.moonbay.phase == "launch" and m.moonbay.ocean_open and float(m.moonbay.chamber_water) >= 1.0, "The sea gate opens on a full chamber")
	run_for(m, 3.2)
	check(m.moonbay.phase == "outbound" and not m.moonbay.ocean_open, "The sub waits outside")
	run_for(m, 20.0)
	check(m.moonbay.phase == "outbound", "It waits until told to return")
	m.start("sub_back")
	run_for(m, 3.2)
	check(m.moonbay.phase == "drain", "The sub returns and the chamber starts to drain")
	run_for(m, 6.2)
	check(m.moonbay.is_empty() and not m.active(), "Drained, the room returns to its own idle state")

	# The view takes the preview state.
	var view = StudioView.new()
	check("tidal_chamber" in view and "moonbay_mission" in view, "Large-room view takes preview state")
	e.room_id = "tidal_power_plant"
	e.start("tidal_fill")
	e.apply(view)
	check(not view.tidal_chamber.is_empty(), "apply hands the tidal state to the view")
	m.start("sub_out")
	m.apply(view)
	check(str(view.moonbay_mission.phase) == "seal", "apply hands the moonbay state to the view")

	check(not ids("tidal_power_plant").has("flood") and ids("tidal_power_plant").has("clear"), "Large-room bar drops Flood, keeps Clear")
	check(ids("airlock").has("flood"), "Small rooms keep Flood")

	print("studio large simulations: %d failure(s)" % failures)
	quit(1 if failures > 0 else 0)
