extends SceneTree
## Saved layouts still name retired library props (owner layouts carry ~1,300). Applying a
## layout must not build them or decode their images: the live room discards them anyway,
## and decoding their sheets made the first navigation build of a station ~1.3 s slower.
const Library = preload("res://scripts/room_asset_library.gd")
var failures := 0

class FakeRoom extends Node:
	var room_id := "reactor"
	var props: Array = []

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	var retired := "library/tileset-f22-02"
	var station := "library/sp-reactor-1"
	var entries: Dictionary = Library.entries()
	check(entries.has(retired), "fixture: retired tileset prop is still in the catalog")
	check(entries.has(station), "fixture: station prop is in the catalog")
	var retired_source: String = str(entries.get(retired, {}).get("data", {}).get("source", ""))
	check(not retired_source.is_empty(), "fixture: retired prop has a source image")
	check(not Library.source_textures.has(retired_source), "fixture: retired image not decoded yet")
	var room := FakeRoom.new()
	Library.apply(room, {retired: [0, 0], station: [10, 10]})
	var ids: Array = room.props.map(func(p): return str(p.id))
	check(station in ids, "the station prop is placed")
	check(not retired in ids, "the retired prop is not built")
	check(not Library.source_textures.has(retired_source) and not Library.image_jobs.has(retired_source), "the retired prop's image is not decoded")
	room.free()
	print("RETIRED LAYOUT ENTRIES ", "PASS" if failures == 0 else "FAIL %d" % failures)
	quit(0 if failures == 0 else 1)
