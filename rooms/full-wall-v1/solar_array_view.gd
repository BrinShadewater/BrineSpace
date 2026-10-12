extends "res://rooms/underwater/thermal-control/solar_array_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("thermal-control-wall")
# A shared view alternates between station rooms. Keep at most four prepared
# layouts, with owned mutable copies; textures remain on the original view.
# Studio bypasses these snapshots, and layout/art registration edits invalidate them.
var retain_rotation_setup := not OS.get_cmdline_user_args().has("--rebuild-solar-rotations")
var rotation_setups := {}
var rotation_setup_hits := 0

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	var Store = preload("res://scripts/room_layout_store.gd")
	var rotation := posmod(q,4)
	var cacheable := retain_rotation_setup and reuse_embedded_geometry and embedded and not has_meta("layout_editor_preview") and dressing != null
	var key: Array = []
	if cacheable:
		key = [full_wall.layout_key(self),Store.shared_positions(full_wall.layout_key(self),rotation), Store.revision, Store.geometry_revision, life_items]
		if rotation_setups.has(rotation) and rotation_setups[rotation].key == key:
			var saved: Dictionary = rotation_setups[rotation]
			if quarter != rotation:
				var working: Dictionary = saved.get("working", {})
				# Retain owned rotation copies only while all their values still match
				# the immutable snapshot. Any mutation restores the original data.
				if working.is_empty() or working.layout != saved.layout or working.props != saved.props or working.profile != saved.profile:
					working = {"layout": saved.layout.duplicate(true), "props": saved.props.duplicate(true), "profile": saved.profile.duplicate(true)}
					saved["working"] = working
				layout = working.layout
				props = working.props
				dressing.profile = working.profile
				quarter = rotation
				pair_mode = 0
				actor = Vector2.ZERO
				set_meta("layout_apply_signature",saved.signature)
				set_meta("layout_apply_count",saved.count)
				rotation_setup_hits += 1
		else:
			# Rebuild authored furniture after edits, even if this is the same quarter.
			quarter = -1
	else:
		rotation_setups.clear()
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	full_wall.apply(self)
	if cacheable and (not rotation_setups.has(rotation) or rotation_setups[rotation].key != key):
		rotation_setups[rotation] = {"key":key.duplicate(true),"layout":layout.duplicate(true),"props":props.duplicate(true),"profile":dressing.profile.duplicate(true),"signature":get_meta("layout_apply_signature",-1),"count":get_meta("layout_apply_count",-1)}

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if full_wall.owns(prop):
		full_wall.draw(self,prop)
		return
	super.draw_registered_prop(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if full_wall.owns(prop): return false
	return super.is_animated_prop(prop)

