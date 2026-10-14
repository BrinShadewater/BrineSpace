extends SceneTree
# Berths are housing for characters only (owner, October 14, 2026): two to start, two more per
# Crew Hab; companions take none. Nothing adds unnamed crew: not a Crew Hab, not a Clone Lab, not
# Safe Wake Protocol, which instead makes cryopods thaw faster.
const Main = preload("res://scripts/main.gd")
const Rooms = preload("res://scripts/room_database.gd")
const Cryo = preload("res://scripts/cryo_recovery.gd")
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
func add(game, id: String, cell: Vector2i) -> Dictionary:
	var room := Rooms.get_room(id)
	room.pos = cell
	room.rotation = 0
	game.placed_rooms.append(room)
	game.occupied[cell] = room
	return room
func _init() -> void:
	var game = Main.new()
	game.meta.save_path = "user://berths_real_crew_test.meta"
	check(game._get_crew_capacity() == 2 + preload("res://scripts/research_tree.gd").berth_bonus(game.meta), "Two berths to start")
	add(game, "brine_core", Vector2i(20, 20))
	game.crew_count = 1
	add(game, "crew_hab", Vector2i(21, 20))
	check(game._get_crew_capacity() == 4 + preload("res://scripts/research_tree.gd").berth_bonus(game.meta), "A Crew Hab adds two berths")
	game.resources.biomass = 20; game.resources.data = 20; game.resources.power = 20
	add(game, "clone_lab", Vector2i(19, 20))
	add(game, "current_turbine", Vector2i(20, 19))
	var result: Dictionary = game._simulate_room_economy()
	check(int(result.added_crew) == 0, "A running Clone Lab adds no crew")
	check(result.offline.get(Vector2i(19, 20), "") != "HABITATS FULL", "A Clone Lab is never idled for want of berths")
	var clone: Dictionary = Rooms.get_room("clone_lab")
	check(int(clone.production.get("data", 0)) == 3 and not clone.consumption.has("data") and not "crew" in str(clone.description).to_lower(), "For now a Clone Lab turns Biomass into Data: %s" % clone.description)
	# Safe Wake Protocol: faster thawing instead of unnamed survivors.
	game.active_synergy_links = []
	check(is_equal_approx(Cryo.safe_wake_rate(game), 1.0), "Without Safe Wake Protocol pods thaw at the normal rate")
	game.active_synergy_links = [{"id": "safe_wake_protocol", "cells": []}]
	check(is_equal_approx(Cryo.safe_wake_rate(game), Cryo.SAFE_WAKE_RATE) and Cryo.SAFE_WAKE_RATE > 1.0, "Safe Wake Protocol makes pods thaw faster")
	var safe_wake: Dictionary = preload("res://scripts/synergy_manager.gd").get_synergy("safe_wake_protocol")
	check(not "survivor" in str(safe_wake.effect).to_lower() and "thaw" in str(safe_wake.effect).to_lower(), "Safe Wake Protocol's card describes thawing: %s" % safe_wake.effect)
	game.free()
	print("BERTHS REAL CREW: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
