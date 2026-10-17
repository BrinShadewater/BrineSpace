extends Node2D
const PreparedScreens=preload("res://scripts/prepared_library_screens.gd")
const BaseTriangles=preload("res://scripts/library_base_triangles.gd")
var combine_library_bases:=not OS.get_cmdline_user_args().has("--separate-library-bases")
var combine_ordinary_bases:=not OS.get_cmdline_user_args().has("--separate-ordinary-bases")
var ordinary_builds:=0
var ordinary_draws:=0
var triangle_builds:=0
var triangle_draws:=0
## Per-room command retention preserves prop/crew depth order without a raster cache.
const STATE_FIELDS = ["drone_visual","survey_status","survey_clock","flood_water","flood_clock","quarter","operating","machine_clock","actor_clock","actor","external_actor_texture","walking","actor_direction","drone_deployed","hatch_open","recovery","architect_pod","cycle_pose","caution_active","carriers"]
const LIVE_STATE_FIELDS = ["drone_visual","survey_status","survey_clock","flood_water","flood_clock","machine_clock","actor_clock","carriers","actor","external_actor_texture","walking","actor_direction"]
var split_library_layers := not OS.get_cmdline_user_args().has("--combined-library-layers")
var reuse_cheap_keys := not OS.get_cmdline_user_args().has("--uncached-slot-keys")
var retain_frozen_effects := not OS.get_cmdline_user_args().has("--reference-frozen-prop-effects")
var draw_origin := Vector2.ZERO
var draw_scale := 1.0
var clip_region := Rect2(-100000,-100000,200000,200000)
var cull_props := not OS.get_cmdline_user_args().has("--draw-all-props")
var slots: Array = []
var view_state := {}
var static_state := {}
var renderer
var state_fields: Array[String] = []
var profile_enabled := false
var prepare_usec := 0
var draw_usec := 0
var static_redraws := 0
var live_redraws := 0
var skipped_props := 0

# The ordinary split library effect pass reads only these three values. Keeping
# its context separate avoids rebinding and restoring every shared room field.
class LibraryDrawContext extends RefCounted:
	var painter: CanvasItem
	var operating := false
	var machine_clock := 0.0
var library_draw_context := LibraryDrawContext.new()
var screen_patterns:=PreparedScreens.FramePatterns.new()
var simple_library_paints := 0

func _can_draw_simple_library(slot) -> bool:
	if slot.item.kind != "library_live" or not view_state.has("operating") or not view_state.has("machine_clock"):
		return false
	var prop: Dictionary = slot.item.prop
	var reg: Dictionary = prop.registration
	return prop.get("layout_flip",Vector2.ZERO) == Vector2.ONE and not prop.get("custom_library_draw",false) and not prop.has("portable_view") and not reg.has("drone_dock") and not reg.has("aquarium")

func _paint_simple_library(slot) -> void:
	slot.draw_set_transform(draw_origin,0,Vector2.ONE*draw_scale)
	library_draw_context.painter = slot
	library_draw_context.operating = view_state.operating
	library_draw_context.machine_clock = view_state.machine_clock
	var artwork: Dictionary = slot.item.prop.duplicate()
	artwork.id = artwork.get("copy_source",artwork.id)
	var library=preload("res://scripts/room_asset_library.gd")
	if library.is_station_prop(str(artwork.get("copy_source",artwork.get("variant_source",artwork.id)))):
		var compiled:PreparedScreens.Prepared=slot.prepared_screens
		if compiled==null or not is_same(slot.prepared_screens_item,slot.item):
			var reg:Dictionary=artwork.registration
			var scale_value:float=artwork.rect.size.x/reg.width
			var anchor:=Vector2(artwork.rect.get_center().x,artwork.rect.end.y)
			compiled=PreparedScreens.build(reg,anchor,scale_value)
			slot.prepared_screens=compiled;slot.prepared_screens_item=slot.item
		PreparedScreens.draw(library_draw_context,compiled,screen_patterns)
		if artwork.registration.has("effects") and library_draw_context.operating:library.draw_effects(library_draw_context,artwork,artwork.registration.effects)
	else:library.draw_live(library_draw_context,artwork)
	library_draw_context.painter = null
	if profile_enabled: simple_library_paints += 1

class DrawSlot extends Node2D:
	var item := {}
	var prepared_screens:PreparedScreens.Prepared
	var prepared_screens_item:Dictionary={}
	var key: Array = []
	var bounds := Rect2()
	var live := true
	var frozen_effects := false
	var draw_transform: Array = []
	func _draw() -> void:
		get_parent().paint(self)

func expanded_prop_entries(view, item: Dictionary) -> Array:
	# Authored wall registrations own their drawing; inherited machinery passes
	# address the older source atlas and cannot draw these replacement sections.
	if item.prop.get("library_asset",false):
		var prop: Dictionary = item.prop
		var reg: Dictionary = prop.registration
		if split_library_layers and not prop.get("custom_library_draw",false) and not prop.has("portable_view") and not reg.has("drone_dock") and not reg.has("aquarium") and (not reg.get("operating_screens",[]).is_empty() or not reg.get("effects",[]).is_empty()):
			# Adjacent slots keep each prop's body/effects together in the depth order.
			var base: Dictionary = item.duplicate()
			base.kind = "library_base"
			var live: Dictionary = item.duplicate()
			live.kind = "library_live"
			return [base,live]
		return [item]
	if item.prop.get("full_wall",false):
		return [item]
	if view.has_method("retained_prop_passes"):
		var parts: Array = []
		for part in view.retained_prop_passes(item.prop):
			var entry: Dictionary = item.duplicate()
			entry.kind = "prop_pass"
			entry.method = part.method
			entry.live = part.live
			parts.append(entry)
		return parts
	if view.has_method("draw_prop_base"):
		var split: Array = []
		var base: Dictionary = item.duplicate()
		base.kind = "prop_base"
		split.append(base)
		if not item.prop.registration.get("dressing",false):
			var effect: Dictionary = item.duplicate()
			effect.kind = "prop_effects"
			split.append(effect)
		return split
	return [item]

func submit(view, queue: Array) -> void:
	var started := Time.get_ticks_usec() if profile_enabled else 0
	draw_usec = 0
	var expanded: Array = []
	for item in queue:
		if item.kind == "prop": expanded.append_array(expanded_prop_entries(view,item))
		else: expanded.append(item)
	queue = expanded
	if renderer != view:
		state_fields.clear()
		for field in STATE_FIELDS:
			if field in view: state_fields.append(field)
	renderer = view
	view_state = {}
	for field in state_fields: view_state[field] = view.get(field)
	# Shared room views are reconfigured for other rooms before child draws run.
	view_state = view_state.duplicate(true)
	static_state = view_state.duplicate()
	for field in LIVE_STATE_FIELDS: static_state.erase(field)
	# Cheap slot key: view identity + layout apply serial + the static scalar
	# values, compared as a flat array instead of deep-walking prop dictionaries.
	var static_key: Array = [view.get_instance_id(),preload("res://scripts/room_layout_store.gd").apply_serial(view,int(view_state.get("quarter",0)))]
	for field in state_fields:
		if field not in LIVE_STATE_FIELDS: static_key.append(view_state[field])
	var compare_by_value: bool = view.has_method("props_rebuilt_each_configure")
	while slots.size() < queue.size():
		var slot := DrawSlot.new()
		add_child(slot)
		slots.append(slot)
	for i in range(slots.size()):
		var slot: DrawSlot = slots[i]
		if i >= queue.size():
			if slot.has_meta("triangle_base"):slot.remove_meta("triangle_base")
			slot.hide()
			continue
		var item: Dictionary = queue[i]
		var retains_geometry:bool=item.kind=="library_base" or (item.kind=="prop" and _ordinary_triangles_eligible(item.get("prop",{})))
		if (not retains_geometry or item.get("prop",{}).get("layout_hidden",false)) and slot.has_meta("triangle_base"):slot.remove_meta("triangle_base")
		var next_transform := [draw_origin,draw_scale]
		var transform_changed: bool = next_transform != slot.draw_transform
		slot.draw_transform = next_transform
		var changed: bool
		if reuse_cheap_keys and not compare_by_value and item.kind in ["prop","prop_base","prop_effects","prop_pass","library_base","library_live"]:
			# Prop entries are stable Dictionary objects (see _sorted_content_queue);
			# identity plus the static key covers every invalidating change, with
			# layout mutations signalled through the store's apply serial.
			var same_entry: bool = is_same(slot.item,item)
			if item.kind in ["library_base","library_live"]:
				# Expansion creates wrappers; the underlying prop remains stable.
				same_entry = slot.item.get("kind","") == item.kind and is_same(slot.item.get("prop"),item.prop)
			changed = not (same_entry and slot.key == static_key)
			if changed:
				slot.key = static_key.duplicate()
				slot.item = item
		else:
			var next_key := [view.get_instance_id(),item,static_state]
			changed = next_key != slot.key
			if changed:
				slot.key = next_key.duplicate(true)
				slot.item = item.duplicate(true)
		if changed:
			# Every changed item invalidates its slot-owned monitor geometry.
			slot.prepared_screens=null;slot.prepared_screens_item={}
			slot.live = true
			if item.kind in ["prop","prop_base","prop_effects","prop_pass","library_base","library_live"]:
				# Unclassified props stay live. BRINE's dressing includes animated screens.
				if view.has_method("is_animated_prop"):
					var animation_prop: Dictionary = item.prop
					if animation_prop.has("copy_source"):
						animation_prop = animation_prop.duplicate()
						animation_prop.id = animation_prop.copy_source
					# Drawing already resolves copied IDs; classification must agree.
					slot.live = view.is_animated_prop(animation_prop)
				if item.prop.registration.get("dressing",false) and view.has_method("draw_computer_display"):
					slot.live = true
				# Match the ordinary library draw path in paint(): fixed polygons only
				# change with slot state, while registered screens use the live clock.
				# Portable/custom artwork still belongs to its source renderer.
				if item.prop.get("library_asset",false) and not item.prop.get("custom_library_draw",false) and not item.prop.has("portable_view"):
					slot.live = item.prop.registration.has("drone_dock") or item.prop.registration.has("aquarium") or bool(view_state.get("operating",false)) and (not item.prop.registration.get("operating_screens",[]).is_empty() or not item.prop.registration.get("effects",[]).is_empty())
				if item.kind == "library_base": slot.live = false
				if item.kind == "prop_base": slot.live = false
				if item.kind == "prop_effects": slot.live = true
				if item.kind == "prop_pass": slot.live = item.live
				slot.bounds = view.prop_visual_bounds(item.prop).grow(64)
		var visible_now: bool = item.kind not in ["prop","prop_base","prop_effects","prop_pass","library_base","library_live"] or not cull_props or clip_region.intersects(slot.bounds)
		if not visible_now:
			slot.hide()
			skipped_props += 1
			continue
		var was_hidden := not slot.visible
		slot.show()
		if item.kind in ["prop","prop_base","prop_effects","prop_pass","library_base","library_live"]:
			preload("res://scripts/flood_visuals.gd").prop_material(slot,item.prop,float(view_state.get("flood_water",0)),float(view_state.get("flood_clock",0)),draw_origin,draw_scale)
		else: slot.material=null
		var motion_changed := refresh_frozen_effects(slot)
		if changed or transform_changed or (slot.live and not slot.frozen_effects) or was_hidden or motion_changed:
			slot.queue_redraw()

	if profile_enabled: prepare_usec = Time.get_ticks_usec()-started

func refresh_frozen_effects(slot: DrawSlot) -> bool:
	# Only the ordinary split library pass has a complete clock-free contract:
	# screens and effects both use time zero under Reduced Motion. Custom,
	# portable, aquarium and drone artwork keep their own update semantics.
	var frozen: bool = retain_frozen_effects and slot.item.get("kind","") == "library_live" and preload("res://scripts/title_settings.gd").reduced_motion
	var changed := frozen != slot.frozen_effects
	slot.frozen_effects = frozen
	return changed

# The host skipped this room's configure/submit because none of its inputs
# changed. Only the machine clock moves (configure sets it to visual time), so
# refresh it and redraw the live slots; static slots stay retained.
func advance_live(clock: float, water := -1.0) -> void:
	# Nothing was prepared this frame; paints below accumulate draw time afresh.
	prepare_usec = 0
	draw_usec = 0
	if view_state.has("machine_clock"): view_state["machine_clock"] = clock
	if view_state.has("flood_clock"): view_state["flood_clock"] = clock
	# Submerged props animate through their shader: move its clock, the level (a draining room
	# changes it slightly every frame; the host keys only wet or dry) and the waterline, which is
	# in global coordinates and follows a held pan, without re-preparing the room.
	if water >= 0.0 and view_state.has("flood_water"): view_state["flood_water"] = water
	water = float(view_state.get("flood_water",0))
	if water > 0.001:
		for slot in slots:
			if slot.visible and slot.material != null and slot.item.kind in ["prop","prop_base","prop_effects","prop_pass","library_base","library_live"]:
				preload("res://scripts/flood_visuals.gd").prop_material(slot,slot.item.prop,water,clock,draw_origin,draw_scale)
	for slot in slots:
		if not slot.visible: continue
		var motion_changed := refresh_frozen_effects(slot)
		if (slot.live and not slot.frozen_effects) or motion_changed: slot.queue_redraw()

func _ordinary_triangles_eligible(prop:Dictionary)->bool:
	var reg:Dictionary=prop.get("registration",{})
	return combine_ordinary_bases and prop.get("library_asset",false) and not prop.get("custom_library_draw",false) and not prop.has("portable_view") and not reg.has("drone_dock") and not reg.has("aquarium")

func paint(slot: DrawSlot) -> void:
	var started := Time.get_ticks_usec() if profile_enabled else 0
	if slot.item.has("prop") and slot.item.prop.get("layout_hidden",false): return
	if _can_draw_simple_library(slot):
		_paint_simple_library(slot)
		if slot.live: live_redraws += 1
		else: static_redraws += 1
		if profile_enabled: draw_usec += Time.get_ticks_usec()-started
		return
	var saved := {}
	for field in view_state:
		saved[field] = renderer.get(field)
		renderer.set(field,view_state[field])
	var previous_painter: CanvasItem = renderer.painter
	var previous_actor: Vector2 = renderer.actor
	var previous_texture: Texture2D = renderer.external_actor_texture
	slot.draw_set_transform(draw_origin,0,Vector2.ONE*draw_scale)
	renderer.painter = slot
	if slot.item.kind in ["prop","prop_pass","prop_base","prop_effects","library_base","library_live"]:
		preload("res://scripts/room_layout_store.gd").draw_flip(renderer,slot,slot.item.prop,draw_origin,draw_scale)
	match slot.item.kind:
		"prop":
			var artwork: Dictionary=slot.item.prop.duplicate()
			artwork.id=artwork.get("copy_source",artwork.id)
			if artwork.get("library_asset",false) and not artwork.get("custom_library_draw",false):
				if _ordinary_triangles_eligible(artwork):
					var cache:Dictionary=slot.get_meta("triangle_base",{})
					if cache.is_empty() or cache.key!=artwork:
						cache={"key":artwork.duplicate(true),"geometry":BaseTriangles.build(artwork)}
						slot.set_meta("triangle_base",cache);ordinary_builds+=1
					BaseTriangles.draw(slot,cache.geometry,artwork.library_texture);ordinary_draws+=1
					preload("res://scripts/room_asset_library.gd").draw_live(renderer,artwork)
				else:preload("res://scripts/room_asset_library.gd").draw(renderer,artwork)
			else: renderer.draw_registered_prop(artwork)
		"library_base", "library_live":
			var artwork: Dictionary = slot.item.prop.duplicate()
			artwork.id = artwork.get("copy_source",artwork.id)
			if slot.item.kind == "library_base":
				if combine_library_bases:
					var cache:Dictionary=slot.get_meta("triangle_base",{})
					if cache.is_empty() or cache.key!=artwork:
						cache={"key":artwork.duplicate(true),"geometry":BaseTriangles.build(artwork)}
						slot.set_meta("triangle_base",cache);triangle_builds+=1
					BaseTriangles.draw(slot,cache.geometry,artwork.library_texture);triangle_draws+=1
				else:preload("res://scripts/room_asset_library.gd").draw_base(renderer,artwork)
			else: preload("res://scripts/room_asset_library.gd").draw_live(renderer,artwork)
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
