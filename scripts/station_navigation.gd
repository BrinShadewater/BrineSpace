extends RefCounted
## Search only installed rooms; never expose undiscovered catalog entries.
static func rooms(game, query: String, forecast: Dictionary) -> Array:
	var matches: Array = []
	var tokens := query.strip_edges().to_lower().split(" ",false)
	for room in game.placed_rooms:
		var status := str(forecast.offline.get(room.pos,"FUNCTIONING inputs available"))
		var observed := str(game.offline_reasons.get(room.pos,""))
		var haystack := ("%s %s %s %s %s %s" % [room.display_name,room.id,room.category,room.pos,status,observed]).to_lower()
		var matched := true
		for token in tokens:
			if not haystack.contains(token):
				matched = false
				break
		if matched: matches.append(room)
	matches.sort_custom(func(a: Dictionary,b: Dictionary):
		return str(a.pos)<str(b.pos) if a.display_name==b.display_name else str(a.display_name)<str(b.display_name))
	return matches

static func actions(cell: Vector2i, reason: String) -> String:
	var links: Array[String] = ["[url=%d,%d]INSPECT / LOCATE[/url]" % [cell.x,cell.y]]
	if reason=="SUSPENDED": links.append("[url=resume:%d,%d]RESUME NEXT CYCLE[/url]" % [cell.x,cell.y])
	if reason.begins_with("NEEDS "):
		for resource in ["power","oxygen","food","water","metal","data","biomass"]:
			if reason.to_lower().contains(resource): links.append("[url=resource:%s]REVIEW %s SUPPLY[/url]" % [resource,resource.to_upper()])
	return "  ·  ".join(links)
