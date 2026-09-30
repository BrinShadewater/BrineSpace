extends SceneTree
## Large-room supporting equipment (owner, Sept 29): the tidal plant, hydroponics farm and storage depot start with
## their four small pieces as ordinary movable props at the old positions; the Moonbay keeps its machinery fixed.
const LargeView = preload("res://rooms/large-rooms/studio_view.gd")
const Store = preload("res://scripts/room_layout_store.gd")
const Library = preload("res://scripts/room_asset_library.gd")
var failures := 0

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		push_error(label)

func prop_named(props: Array, id: String) -> Dictionary:
	for prop in props:
		if str(prop.id) == id: return prop
	return {}

func _init() -> void: call_deferred("run")

func run() -> void:
	var saved_data = Store.data
	Store.data = {}
	Store.revision += 1
	for id in ["tidal_power_plant", "hydroponics_farm", "storage_depot"]:
		var features: Array = LargeView.VIEWS[id].FEATURES
		for quarter in range(4):
			var live: Array = LargeView.live_props(id, quarter)
			check(live.size() == 4, "%s rotation %d shows its four pieces with no saved layout" % [id, quarter])
			check(LargeView.VIEWS[id].fixed_bounds_for_rotation(quarter).size() == 1, id + " fixes only its centerpiece")
			for feature in features:
				var prop := prop_named(live, "library/" + str(feature.path).get_file().get_basename())
				var source: Rect2 = feature.rect
				var expected := source.get_center().rotated(float(quarter) * PI * 0.5)
				check(not prop.is_empty() and prop.rect.get_center().distance_to(expected) < 3.0 and absf(prop.rect.size.x - source.size.x) < 2.0,
					"%s rotation %d keeps %s at its old position and size" % [id, quarter, str(feature.path).get_file()])
	var moonbay: Array = LargeView.live_props("moonbay", 0)
	check(moonbay.is_empty() and LargeView.feature_seed("moonbay", 0).is_empty(), "Moonbay equipment stays fixed machinery")
	check(LargeView.VIEWS["moonbay"].fixed_bounds_for_rotation(0).size() == 5, "Moonbay keeps all its fixed bounds")

	# Owner edits win over the seed: moved, resized, hidden and deleted.
	var id := "tidal_power_plant"
	var ids: Array = LargeView.feature_seed(id, 0).keys().filter(func(key): return not str(key).begins_with("size/"))
	var layout := {ids[0]: [-40.0, 60.0], "size/" + ids[0]: [1.5, 1.5], ids[1]: null, "hidden/" + ids[2]: true}
	Store.data = {Store.key("room-" + id, 0): layout}
	Store.revision += 1
	var live: Array = LargeView.live_props(id, 0)
	check(live.size() == 3, "A deleted piece stays deleted")
	var moved := prop_named(live, ids[0])
	check(moved.rect.position.distance_to(Vector2(-40, 60)) < 0.01, "A moved piece stays where the owner put it")
	check(prop_named(live, ids[1]).is_empty(), "The deleted piece is gone")
	check(bool(prop_named(live, ids[2]).get("layout_hidden", false)), "A hidden piece stays hidden")
	check(not prop_named(live, ids[3]).is_empty(), "Untouched pieces keep their default place")
	check(LargeView.live_props(id, 1).size() == 4, "Other rotations keep their own defaults")

	Store.data = saved_data
	Store.revision += 1
	print("large room props: %d failure(s)" % failures)
	quit(1 if failures > 0 else 0)
