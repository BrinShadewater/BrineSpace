extends RefCounted
const Architects=preload("res://scripts/architects.gd")
static var shelf_timelines: Dictionary = {}

static func helmet_on_shelf(game, cell: Vector2i) -> bool:
	# Lockers provide reusable gear. A staged spare is visible when not servicing
	# an actor; active handoffs derive solely from the saved action timer.
	for id in Architects.IDS:
		var actor = Architects.actor_for(game, id)
		if not actor.active or actor.dead or not actor.helmet_action_active() or actor.cell_at(actor.foot) != cell: continue
		var key: String = id + "/" + actor.state
		if not shelf_timelines.has(key):
			var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-underwater-v1/locker/%s-%s-east/manifest.json" % [id, actor.state]))
			var clip: Dictionary = manifest.states[0]
			var total := 0.0
			for duration in clip.frameDurationsMs: total += float(duration) / 1000.0
			var event_id := "take-helmet-from-locker" if actor.state == "equip-helmet" else "release-helmet-to-locker"
			for event in clip.events:
				if event.id == event_id:
					shelf_timelines[key] = {"total": total, "event": float(event.timeMs) / 1000.0}
			assert(shelf_timelines.has(key), "Locker sequence needs its handoff marker")
		var timeline: Dictionary = shelf_timelines[key]
		var elapsed: float = timeline.total - actor.timer
		return elapsed < timeline.event if actor.state == "equip-helmet" else elapsed >= timeline.event
	return true

static func ready(game,cell: Vector2i) -> bool:
	return game.running and game.occupied.has(cell) and game.occupied[cell].id=="airlock" and not game.occupied[cell].get("suspended",false) and game.powered_room_cells.has(cell)

static func locker(game,cell: Vector2i) -> Dictionary:
	if not game.occupied.has(cell) or game.occupied[cell].id!="airlock": return {}
	var geometry: Dictionary=game.grid_view.bill_room_geometry(game.occupied[cell],[])
	for prop in geometry.props:
		if prop.id=="suit_lockers":
			var point: Vector2=(Vector2(cell)+Vector2.ONE*0.5)*384.0+Vector2(prop.rect.position.x-28,prop.rect.end.y+6)
			return {"id":"airlock:%d:%d" % [cell.x,cell.y],"cell":cell,"interaction_point":point,"facing":"east"}
	return {}

static func busy(game,cell: Vector2i,requester=null) -> bool:
	for id in Architects.IDS:
		var actor=Architects.actor_for(game,id)
		if actor==requester or not actor.active or actor.dead: continue
		if not actor.locker_request.is_empty() and actor.locker_request.locker.cell==cell: return true
		if actor.helmet_action_active() and actor.cell_at(actor.foot)==cell: return true
	return false

static func request(game,id: String,cell: Vector2i, refill := false) -> bool:
	if not Architects.IDS.has(id) or not Architects.present(game,id) or not ready(game,cell): return false
	var actor=Architects.actor_for(game,id)
	if not actor.needs_air(): return false
	if not actor.expedition.is_empty(): return false
	if busy(game,cell,actor) or not actor.locker_request.is_empty(): return false
	if actor.topology(game)!=actor.signature: actor.rebuild(game)
	var target:=locker(game,cell)
	if target.is_empty() or not actor.request_helmet_at_locker(actor.helmet_equipped if refill else not actor.helmet_equipped,target,refill): return false
	game._log("%s: diving locker assigned. Check the seal twice." % Architects.NAMES[id],false)
	return true

static func check_service(game,actor) -> void:
	var cell: Vector2i=actor.cell_at(actor.foot)
	var pending: bool=not actor.locker_request.is_empty() and str(actor.locker_request.locker.id).begins_with("airlock:")
	if pending: cell=actor.locker_request.locker.cell
	var local_action: bool=actor.helmet_action_active() and game.occupied.has(cell) and game.occupied[cell].id=="airlock"
	if (pending or local_action) and not ready(game,cell):
		actor.cancel_helmet_action()
		actor.locker_request.clear()
		actor.path.clear()
		actor.goal=""
		actor.state="idle"
		actor.timer=1.0
		actor.activity="diving locker offline"
