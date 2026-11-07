extends RefCounted
## Warnings before a crew member dies, and a clear notice when one does (owner playtest,
## Sept 17: every character died unnoticed). BRINE speaks each warning once per incident, as
## an urgent transmission that pauses the station; it re-arms once the danger passes.

const Architects = preload("res://scripts/architects.gd")
const AIR_WARNING_SECONDS := 8.0
const TANK_WARNING_SECONDS := 20.0
const STARVATION_WARNING := 0.5
const BATTERY_WARNING := 12.0

static func check(game, actor, id: String, unsafe_air: bool, starvation_limit: float) -> void:
	if actor.dead or not actor.active: return
	var name: String = Architects.NAMES.get(id, id)
	var place := _place(game, actor)
	var air_left: float = actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
	var air_danger: bool = actor.needs_air() and unsafe_air and air_left <= (TANK_WARNING_SECONDS if actor.helmet_equipped else AIR_WARNING_SECONDS)
	_warn(game, actor, id, "air", air_danger,
		"%s is running out of air%s: about %d seconds left. Get them to dry air or a helmet locker." % [name, place, ceili(air_left)])
	var starving: bool = float(actor.get("starvation")) >= starvation_limit * STARVATION_WARNING
	_warn(game, actor, id, "food", starving,
		"%s is starving%s. Without Food they have about %d seconds." % [name, place, ceili(starvation_limit - float(actor.get("starvation")))])
	if "battery" in actor and not actor.needs_air():
		var flat: bool = float(actor.battery) <= BATTERY_WARNING and not bool(actor.get("recharge_docked"))
		_warn(game, actor, id, "battery", flat,
			"%s's battery is nearly flat%s. Clear a route to the charging pod and keep it powered." % [name, place])

static func announce_death(game, id: String, cause: String) -> void:
	var name: String = Architects.NAMES.get(id, id)
	if is_instance_valid(game.get("crew_comms")) and game.crew_comms.has_method("transmit"):
		game.crew_comms.transmit("brine", "%s is gone: %s. I logged the time. It will not help them." % [name, cause], "", true)

static func _warn(game, actor, id: String, kind: String, active: bool, message: String) -> void:
	var flag := "danger_warned_" + kind
	if not active:
		if actor.has_meta(flag): actor.remove_meta(flag)
		return
	if actor.has_meta(flag): return
	actor.set_meta(flag, true)
	game._log("WARNING // " + message, true)
	if is_instance_valid(game.get("crew_comms")) and game.crew_comms.has_method("transmit"):
		game.crew_comms.transmit("brine", message, "", true)

static func _place(game, actor) -> String:
	var cell: Vector2i = actor.cell_at(actor.foot)
	var room: Dictionary = game.occupied.get(cell, {})
	return " in the %s" % room.get("display_name", "station") if not room.is_empty() else " outside the station"

static func living_crew(game) -> int:
	var alive := 0
	for id in Architects.IDS:
		var actor = Architects.actor_for(game, id)
		if actor != null and Architects.present(game, id) and actor.active and not actor.dead: alive += 1
	return alive
