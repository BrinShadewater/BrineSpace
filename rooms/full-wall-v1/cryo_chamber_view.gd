extends "res://rooms/underwater/batch-two/cryo_chamber_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("cryo-support-wall")

var reuse_recovery_geometry := not OS.get_cmdline_user_args().has("--uncached-recovery-geometry")
var configured_geometry := {}
var configured_revision := -1

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	var revision: int = preload("res://scripts/room_layout_store.gd").revision
	if revision != configured_revision:
		configured_geometry.clear()
		configured_revision = revision
	var key := [posmod(q,4),recovery.is_empty(),recovery.get("pods",[]).size()]
	var cached: bool = reuse_recovery_geometry and configured_geometry.has(key)
	if cached:
		var state: Dictionary = configured_geometry[key]
		quarter = posmod(q,4)
		pair_mode = 0
		embedded = true
		layout = state.layout.duplicate(true)
		props = state.props.duplicate(true)
		for name in state.profiles:
			get(name).profile = state.profiles[name].duplicate(true)
	elif not recovery.is_empty():
		full_wall.restore_profiles(self)
	# Keep door state, power, actors and animation clocks live on every call.
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	if not cached and recovery.is_empty(): full_wall.apply(self)
	if not cached and reuse_recovery_geometry and cryo_dressing != null:
		var profiles := {}
		for name in full_wall.profiles:
			if get(name) != null: profiles[name] = get(name).profile.duplicate(true)
		configured_geometry[key] = {"layout":layout.duplicate(true),"props":props.duplicate(true),"profiles":profiles}

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

