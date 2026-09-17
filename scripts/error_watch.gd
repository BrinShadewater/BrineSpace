extends RefCounted
## Counts engine and script errors as they are written to the log (owner request, Sept 17: a
## session's log held 45 "mesh is null" errors that nothing reported). Godot has no error hook
## for GDScript, so this reads the new bytes of the running log every few seconds, groups the
## lines by their message, and keeps the first backtrace of each. The performance overlay shows
## the total and every bug report lists the groups.

const LOG_PATH := "user://logs/godot.log"
const MAX_GROUPS := 40
const CONTEXT_LINES := 4
var path := LOG_PATH
var offset := 0
var groups := {} # message -> {count, first_uptime_ms, context}
var total := 0
var carry := ""

func poll(uptime_ms: float) -> void:
	if not FileAccess.file_exists(path): return
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null: return
	var size := int(file.get_length())
	if size < offset: # The log was rotated or truncated; start again.
		offset = 0
		carry = ""
	if size == offset:
		file.close()
		return
	file.seek(offset)
	var text := carry + file.get_buffer(size - offset).get_string_from_utf8()
	offset = size
	file.close()
	var lines := text.split("\n")
	carry = lines[lines.size() - 1] if not text.ends_with("\n") else ""
	for index in range(lines.size() - (0 if carry.is_empty() else 1)):
		var line := lines[index].strip_edges()
		if not (line.begins_with("ERROR:") or line.begins_with("SCRIPT ERROR:") or line.begins_with("USER ERROR:")): continue
		total += 1
		var message := line
		if groups.has(message):
			groups[message].count += 1
			continue
		if groups.size() >= MAX_GROUPS: continue
		var context := PackedStringArray()
		for extra in range(index + 1, mini(index + 1 + CONTEXT_LINES, lines.size())):
			var next := lines[extra].strip_edges()
			if next.begins_with("ERROR:") or next.begins_with("SCRIPT ERROR:") or next.is_empty(): break
			context.append(next)
		groups[message] = {"count": 1, "first_uptime_ms": uptime_ms, "context": context}

func summary() -> Dictionary:
	var rows: Array = []
	var names: Array = groups.keys()
	names.sort_custom(func(a, b): return int(groups[a].count) > int(groups[b].count))
	for message in names:
		rows.append({"message": message, "count": int(groups[message].count), "first_uptime_ms": groups[message].first_uptime_ms, "context": groups[message].context})
	return {"total": total, "distinct": groups.size(), "groups": rows, "log": path}

func report_lines() -> PackedStringArray:
	var lines := PackedStringArray()
	if total == 0:
		lines.append("errors logged: none")
		return lines
	lines.append("errors logged: %d in %d kinds (most frequent first)" % [total, groups.size()])
	var data: Array = summary().groups
	for index in range(mini(8, data.size())):
		lines.append("  %dx %s" % [data[index].count, str(data[index].message).substr(0, 160)])
		if not data[index].context.is_empty(): lines.append("      " + str(data[index].context[0]).substr(0, 160))
	return lines
