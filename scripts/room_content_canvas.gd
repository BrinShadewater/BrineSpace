extends Node2D
## Per-room command retention preserves prop/crew depth order without a raster cache.
const STATE_FIELDS = ["quarter","operating","machine_clock","actor_clock","actor","external_actor_texture","walking","actor_direction","drone_deployed","hatch_open","recovery","architect_pod","cycle_pose"]
var draw_origin := Vector2.ZERO
var draw_scale := 1.0
var clip_region := Rect2(-100000,-100000,200000,200000)
var cull_props := not OS.get_cmdline_user_args().has("--draw-all-props")
var slots: Array = []
var view_state := {}
var static_state := {}
var renderer
var profile_enabled := false
var prepare_usec := 0
var draw_usec := 0
var static_redraws := 0
var live_redraws := 0
var skipped_props := 0

class DrawSlot extends Node2D:
	var item := {}
	var key: Array = []
	var bounds := Rect2()
	var live := true
	var draw_transform: Array = []
	func _draw() -> void:
		get_parent().paint(self)

func submit(view, queue: Array) -> void:
	var started := Time.get_ticks_usec() if profile_enabled else 0
	draw_usec = 0
	var expanded: Array = []
	for item in queue:
		if item.kind == "prop" and view.has_method("retained_prop_passes"):
			for part in view.retained_prop_passes(item.prop):
				var entry: Dictionary = item.duplicate()
				entry.kind = "prop_pass"
				entry.method = part.method
				entry.live = part.live
				expanded.append(entry)
		elif item.kind == "prop" and view.has_method("draw_prop_base"):
			var base: Dictionary = item.duplicate()
			base.kind = "prop_base"
			expanded.append(base)
			if not item.prop.registration.get("dressing",false):
				var effect: Dictionary = item.duplicate()
				effect.kind = "prop_effects"
				expanded.append(effect)
		else: expanded.append(item)
	queue = expanded
	renderer = view
	view_state = {}
	for field in STATE_FIELDS:
		if field in view: view_state[field] = view.get(field)
	# Shared room views are reconfigured for other rooms before child draws run.
	view_state = view_state.duplicate(true)
	static_state = view_state.duplicate()
	static_state.erase("machine_clock")
	static_state.erase("actor_clock")
	static_state.erase("actor")
	static_state.erase("external_actor_texture")
	static_state.erase("walking")
	static_state.erase("actor_direction")
	while slots.size() < queue.size():
		var slot := DrawSlot.new()
		add_child(slot)
		slots.append(slot)
	for i in range(slots.size()):
		var slot: DrawSlot = slots[i]
		if i >= queue.size():
			slot.hide()
			continue
		var item: Dictionary = queue[i]
		var next_transform := [draw_origin,draw_scale]
		var transform_changed: bool = next_transform != slot.draw_transform
		slot.draw_transform = next_transform
		var next_key := [view.get_instance_id(),item,static_state]
		var changed: bool = next_key != slot.key
		if changed:
			slot.key = next_key.duplicate(true)
			slot.item = item.duplicate(true)
			slot.live = true
			if item.kind in ["prop","prop_base","prop_effects","prop_pass"]:
				# Unclassified props stay live. BRINE's dressing includes animated screens.
				if view.has_method("is_animated_prop"):
					slot.live = view.is_animated_prop(item.prop)
				if item.prop.registration.get("dressing",false) and view.has_method("draw_computer_display"):
					slot.live = true
				if item.kind == "prop_base": slot.live = false
				if item.kind == "prop_effects": slot.live = true
				if item.kind == "prop_pass": slot.live = item.live
				slot.bounds = view.prop_visual_bounds(item.prop).grow(64)
		var visible_now: bool = item.kind not in ["prop","prop_base","prop_effects","prop_pass"] or not cull_props or clip_region.intersects(slot.bounds)
		if not visible_now:
			slot.hide()
			skipped_props += 1
			continue
		var was_hidden := not slot.visible
		slot.show()
		if changed or transform_changed or slot.live or was_hidden:
			slot.queue_redraw()

	if profile_enabled: prepare_usec = Time.get_ticks_usec()-started

func paint(slot: DrawSlot) -> void:
	var started := Time.get_ticks_usec() if profile_enabled else 0
	var saved := {}
	for field in view_state:
		saved[field] = renderer.get(field)
		renderer.set(field,view_state[field])
	var previous_painter: CanvasItem = renderer.painter
	var previous_actor: Vector2 = renderer.actor
	var previous_texture: Texture2D = renderer.external_actor_texture
	slot.draw_set_transform(draw_origin,0,Vector2.ONE*draw_scale)
	renderer.painter = slot
	match slot.item.kind:
		"prop": renderer.draw_registered_prop(slot.item.prop)
		"prop_pass": renderer.call(slot.item.method,slot.item.prop)
		"prop_base": renderer.draw_prop_base(slot.item.prop)
		"prop_effects": renderer.draw_prop_animation(slot.item.prop)
		"actor": renderer.draw_actor()
		"crew":
			renderer.actor = slot.item.member.position
			renderer.external_actor_texture = slot.item.member.texture
			renderer.draw_actor()
	renderer.painter = previous_painter
	renderer.actor = previous_actor
	renderer.external_actor_texture = previous_texture
	for field in saved: renderer.set(field,saved[field])
	if slot.live: live_redraws += 1
	else: static_redraws += 1

	if profile_enabled: draw_usec += Time.get_ticks_usec()-started
