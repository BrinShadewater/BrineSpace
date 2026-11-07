extends SceneTree
const Report = preload("res://scripts/expedition_report.gd")
class AudioSpy extends RefCounted:
	var events: Array[String] = []
	var summary_panel: PanelContainer
	var summary_stats: HFlowContainer
	var station_sound
	func play_station_sound(kind: String) -> void: events.append(kind)
	func play_reward_tick(_progress: float) -> bool: events.append("ui_reward_tick"); return true
const Counter = preload("res://scripts/reward_count.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
var sounds: Array[String] = []
func _initialize() -> void: run.call_deferred()
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)
func make_counter(value: int, prefix := ""):
	sounds.clear()
	var figure := Label.new()
	figure.add_theme_font_override("font",preload("res://scripts/ui_fonts.gd").interface_font())
	figure.text = prefix + str(value)
	root.add_child(figure)
	var count := Counter.new()
	count.sound_requested.connect(func(kind: String): sounds.append(kind))
	count.configure(figure, value, prefix, 0.0, true)
	count.set_process(false)
	return count
func run() -> void:
	Preferences.reduced_motion = false
	for value in [1,7,123456789]:
		var count = make_counter(value,"+")
		var number_font: Font = count.figure.get_theme_font("font")
		var thin_width := number_font.get_string_size("1111",HORIZONTAL_ALIGNMENT_LEFT,-1,44).x
		var round_width := number_font.get_string_size("8888",HORIZONTAL_ALIGNMENT_LEFT,-1,44).x
		check(is_equal_approx(thin_width,round_width), "Animated interface digits occupy equal width")
		var previous := 0
		for step in range(16):
			count._process(0.08)
			var current: int = count.figure.text.to_int()
			check(current >= previous and current <= value, "Counts remain monotonic and never overshoot")
			previous = current
		check(sounds.count("ui_reward_chime") == 1, "Hero chimes exactly once")
		check(sounds.count("ui_reward_tick") <= 11, "Tick count stays bounded even for large rewards")
		check(count.finished and count.figure.text == "+%d" % value, "Exact final value independent of magnitude")
		check(count.figure.scale == Vector2.ONE and count.figure.pivot_offset == Vector2.ZERO, "Landing restores the original text transform")
		check(count.figure.self_modulate == Color.WHITE, "Landing restores normal text brightness")
		count.figure.free()
	var zero = make_counter(0)
	check(zero.finished and not zero.landed, "Zero skips count and sparkle")
	check(sounds.is_empty(), "Zero rewards stay silent")
	zero.figure.free()
	Preferences.reduced_motion = true
	var reduced = make_counter(99,"x")
	check(reduced.finished and not reduced.landed and reduced.figure.text == "x99", "Reduced motion shows final value immediately")
	check(sounds.is_empty(), "Reduced motion does not produce orphan ticks or chimes")
	reduced.figure.free()
	Preferences.reduced_motion = false
	var hidden = make_counter(81)
	hidden.figure.hide(); hidden._process(0.01)
	check(hidden.finished and hidden.figure.text == "81", "Leaving the report settles rather than replaying later")
	check(sounds.is_empty(), "Leaving during the reveal does not chime offscreen")
	hidden.figure.free()
	var changed = make_counter(37)
	Preferences.reduced_motion = true; changed._process(0.01)
	check(changed.finished and not changed.landed, "Enabling reduced motion during a reveal settles immediately")
	check(sounds.is_empty(), "Settling from a preference change stays silent")
	changed.figure.free()
	Preferences.reduced_motion = false
	var small = make_counter(15)
	small.prominent = false
	small._process(0.2)
	check(sounds.count("ui_reward_tick") == 1, "Changing number emits a tick")
	small._process(0.001)
	check(sounds.count("ui_reward_tick") == 1, "Fast frames cannot flood tick requests")
	small._process(0.8); small._process(0.2)
	check(sounds.count("ui_reward_land") == 1 and not sounds.has("ui_reward_chime"), "Small figures land with one softer tone")
	small.figure.free()
	Preferences.reduced_motion = false
	var stalled = make_counter(67,"+")
	stalled._process(2.0)
	check(stalled.landed and not stalled.finished, "Slow frame still starts a visible landing with the chime")
	check(stalled.figure.text == "+67" and sounds.count("ui_reward_chime") == 1, "Slow frame settles exact value and emits one chime")
	check(stalled.figure.scale.x > 1.0, "Data landing receives a small settling pulse")
	check(stalled.figure.self_modulate.r > 1.0, "Final value and landing pulse begin together after a stall")
	stalled._process(0.2)
	check(not stalled.finished and sounds.count("ui_reward_chime") == 1, "Landing gets its full visible duration without a repeat chime")
	stalled._process(0.2)
	check(stalled.finished, "Landing completes after its own duration")
	stalled.figure.free()
	Preferences.reduced_motion = false
	var rhythmic = make_counter(10000,"+")
	var previous_text: String = rhythmic.figure.text
	var last_beat := -1.0
	var first_gap := 0.0
	var last_gap := 0.0
	for frame in range(60):
		var event_count := sounds.size()
		rhythmic._process(1.0 / 120.0)
		if rhythmic.figure.text != previous_text:
			check(sounds.size() == event_count + 1 and sounds.back() == "ui_reward_tick", "Every visible count step gets a matching tick request")
			if last_beat >= 0.0:
				var gap: float = rhythmic.elapsed - last_beat
				check(gap >= 0.06, "Visible steps leave a readable rhythmic gap")
				if first_gap == 0.0: first_gap = gap
				last_gap = gap
			last_beat = rhythmic.elapsed
			previous_text = rhythmic.figure.text
	check(last_gap > first_gap, "Tick rhythm slows as the count approaches its landing")
	rhythmic.figure.free()
	for fps in [30,60,144]:
		var cadence = make_counter(10000,"+")
		cadence.duration = 0.9; cadence.delay = 0.12
		var final_tick := -1.0
		for frame in range(fps * 2):
			var event_count := sounds.size()
			cadence._process(1.0 / float(fps))
			if sounds.size() > event_count and sounds.back() == "ui_reward_tick": final_tick = cadence.elapsed
			if cadence.landed: break
		check(final_tick > 0 and cadence.elapsed - final_tick >= 0.09, "Final tick leaves room for chime at %d FPS" % fps)
		check(sounds.count("ui_reward_chime") == 1 and cadence.figure.text == "+10000", "Exact single landing at %d FPS" % fps)
		cadence.figure.free()
	var interrupted = make_counter(23,"+")
	interrupted._process(2.0)
	check(interrupted.figure.scale.x > 1.0, "Data pulse is active at landing")
	var landed_sounds := sounds.size()
	interrupted.figure.hide(); interrupted._process(0.01)
	check(interrupted.finished and interrupted.figure.scale == Vector2.ONE and interrupted.figure.pivot_offset == Vector2.ZERO, "Interrupting the pulse restores the text transform")
	check(sounds.size() == landed_sounds, "Interrupting an active landing does not add another sound")
	interrupted.figure.free()
	var spy := AudioSpy.new()
	Report._reveal_sound("ui_reward_tick",spy,false)
	check(spy.events.is_empty(), "Secondary counters do not compete with the lead ticking rhythm")
	Report._reveal_sound("ui_reward_land",spy,false)
	Report._reveal_sound("ui_reward_tick",spy,true)
	Report._reveal_sound("ui_reward_chime",spy,true)
	check(spy.events == ["ui_reward_land","ui_reward_tick","ui_reward_chime"], "Lead ticks and distinct landing accents retain audio routing")
	var hero_state := Counter.new()
	hero_state.landed = true
	var late_spy := AudioSpy.new()
	Report._reveal_sound("ui_reward_land",late_spy,false,null,hero_state)
	check(late_spy.events.is_empty(), "Late small-figure tone cannot crowd an already landed Data chime")
	hero_state.landed = false
	Report._reveal_sound("ui_reward_land",late_spy,false,null,hero_state)
	check(late_spy.events == ["ui_reward_land"], "Normal small landings remain audible before the main finish")
	hero_state.free()
	for data_value in [0,1]:
		var sample := AudioSpy.new()
		sample.station_sound = AudioSpy.new()
		sample.summary_panel = PanelContainer.new()
		root.add_child(sample.summary_panel)
		var layout := VBoxContainer.new()
		sample.summary_panel.add_child(layout)
		var data_label := Label.new()
		data_label.name = "ExpeditionEarnings"; data_label.text = "+%d" % data_value
		layout.add_child(data_label)
		sample.summary_stats = HFlowContainer.new()
		layout.add_child(sample.summary_stats)
		for total in [1,24]:
			var tile := PanelContainer.new()
			var column := VBoxContainer.new()
			var text := Label.new(); text.text = str(total)
			sample.summary_stats.add_child(tile); tile.add_child(column); column.add_child(text)
		Report.animate(sample)
		var animated = sample.summary_stats.get_child(1).get_child(0).get_child(0).get_node("RewardCount")
		animated.set_process(false); animated._process(0.25)
		check(sample.station_sound.events == ["ui_reward_tick"], "Data %d and one-step figures do not silence the useful tick leader" % data_value)
		var hero_count = data_label.get_node("RewardCount")
		hero_count.set_process(false); hero_count._process(2.0)
		check(sample.events.count("ui_reward_chime") == (1 if data_value == 1 else 0), "Small Data retains the correct final chime")
		sample.summary_panel.free()
	Preferences.reduced_motion = false
	print("REWARD COUNT: %s failures=%d" % ["PASS" if failures == 0 else "FAIL",failures])
	quit(0 if failures == 0 else 1)
