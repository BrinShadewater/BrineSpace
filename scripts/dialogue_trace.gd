extends RefCounted
## TEMPORARY diagnostic (owner playtest note 17, September 2026). Every character line the comms
## panel accepts is written here together with the construction work outstanding at that moment,
## and every finished room writes its own marker. A line about a room that appears above that
## room's COMPLETE marker is the one speaking too early. Delete this file and its two call sites
## once the offending line is named.

const PATH := "user://dialogue_trace.log"

static var enabled := true
static var started := false
# A probe sets this to exercise the writer under -s; play sessions never touch it.
static var force := false

# A test or tool started with -s replaces the main loop with its own script, exactly as the
# performance monitor checks: those runs must never write into the player's folder.
static func _writing(game) -> bool:
	if not enabled or game == null or not is_instance_valid(game): return false
	if force: return true
	var tree: SceneTree = game.get_tree() if game.has_method("get_tree") else null
	return tree != null and tree.get_script() == null

static func _stamp(game) -> String:
	return "[cycle %03d / %7.1f s]" % [int(game.get("cycle")), float(game.get("visual_time_seconds"))]

# What the builders are working on right now, so a line can be read against it.
static func _outstanding(game) -> String:
	var fleet = game.get("drone_fleet")
	if fleet == null or fleet.orders.is_empty(): return "nothing under construction"
	var parts: Array[String] = []
	for order in fleet.orders:
		var builder: String = str(order.get("builder", ""))
		parts.append("%s@%s %.1f/%.1f s%s" % [
			str(order.get("id", "?")),
			str(order.get("pos", "?")),
			float(order.get("work", 0.0)),
			preload("res://scripts/crew_construction.gd").WORK_SECONDS,
			" by " + builder if not builder.is_empty() else " unstarted",
		])
	return "building: " + "; ".join(parts)

static func _write(game, line: String) -> void:
	var file := FileAccess.open(PATH, FileAccess.READ_WRITE if started else FileAccess.WRITE)
	if file == null: return
	if started: file.seek_end()
	else:
		started = true
		file.store_line("# Brine Space dialogue trace // note 17 // %s" % Time.get_datetime_string_from_system())
	file.store_line(line)
	file.close()

static func line_said(game, speaker: String, key: String, text: String) -> void:
	if not _writing(game): return
	_write(game, "%s %-10s %-28s %s | %s" % [
		_stamp(game),
		speaker,
		("(" + key + ")") if not key.is_empty() else "(unkeyed)",
		text.substr(0, 90),
		_outstanding(game),
	])

static func room_complete(game, room_id: String, cell: Vector2i) -> void:
	if not _writing(game): return
	_write(game, "%s COMPLETE   %s at %s | %s" % [_stamp(game), room_id, cell, _outstanding(game)])
