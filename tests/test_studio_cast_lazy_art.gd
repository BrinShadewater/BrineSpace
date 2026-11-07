extends SceneTree
# The Studio's cast decodes a frame when it is first drawn. Decoding every member's whole
# set as the Studio opened held it closed for 3.4 s with seven members shown (owner report,
# October 13, 2026). Tools that build an actor themselves still get every frame at once.
const Cast := preload("res://scripts/room_scale_cast.gd")
const Actor := preload("res://scripts/room_scale_preview.gd")
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
func _init() -> void: call_deferred("run")
func decoded(actor) -> int:
	var count := 0
	for key in actor.player.frames:
		for texture in actor.player.frames[key]:
			if texture.get_size().x > 0: count += 1
	return count
func run() -> void:
	var cast = Cast.new()
	for index in range(cast.actors.size()):
		var actor = cast.actors[index]
		var who: String = str(Actor.CAST[index].name)
		cast.set_mode(index, Actor.WALKING)
		check(not actor.player.frames.is_empty(), who + " has clips after being shown")
		# Packs that mirror one side into the other decode their source frames on loading.
		var early := decoded(actor)
		var total := 0
		for key in actor.player.frames: total += actor.player.frames[key].size()
		check(early * 2 < total, "%s decodes on first draw, not on loading: %d of %d decoded early" % [who, early, total])
		actor.visible = true
		var drawn: Array = actor.members()
		check(drawn.size() == 1 and drawn[0].texture.get_size().x > 0, who + " draws a decoded frame")
		check(drawn.size() == 1 and drawn[0].texture.has_meta("crew_alpha_extent"), who + "'s drawn frame carries its measured extent")
	# An actor a tool builds for itself reads frames directly, so it decodes all of them.
	var plain = Actor.new()
	plain.load_art()
	var all := 0
	for key in plain.player.frames: all += plain.player.frames[key].size()
	check(all > 0 and decoded(plain) == all, "An actor built outside the Studio cast decodes every frame: %d of %d" % [decoded(plain), all])
	print("STUDIO CAST LAZY ART: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
