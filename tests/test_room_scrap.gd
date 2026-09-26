extends SceneTree
## Scrapping a room (owner, Sept 26): half its Metal back, never the core, a rescue ward,
## a crew hab, an occupied room, or a room whose removal cuts others off from the core.
const Scrap=preload("res://scripts/room_scrap.gd")
var failures := 0

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func run() -> void:
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	var stem="user://room_scrap_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	var core := Vector2i(20,20)
	for cell in [Vector2i(20,21),Vector2i(20,22)]: game.wrecks.erase(cell)
	game._place_room("corridor",Vector2i(20,21),true)
	game._place_room("corridor",Vector2i(20,22),true)
	check(game._connected_neighbor_cells(Vector2i(20,22)).has(Vector2i(20,21)), "Fixture chain is connected")
	check(Scrap.refund(game.RoomDatabaseScript.get_room("corridor")) == 1, "Corridor refunds half its 2 Metal")
	check(Scrap.refund(game.RoomDatabaseScript.get_room("solar_array")) == 2, "Solar array refunds half its 4 Metal")
	check(not Scrap.blocker(game, core).is_empty(), "BRINE Core cannot be scrapped")
	check(not Scrap.blocker(game, Vector2i(20,21)).is_empty(), "A room holding others to the core cannot be scrapped")
	check(Scrap.blocker(game, Vector2i(20,22)).is_empty(), "A leaf corridor can be scrapped: %s" % Scrap.blocker(game, Vector2i(20,22)))
	# Crew inside block it.
	var actor=game.bill_npc
	var saved_foot: Vector2=actor.foot
	var saved_active: bool=actor.active
	actor.active=true;actor.dead=false
	actor.foot=(Vector2(20,22)+Vector2.ONE*0.5)*384
	check(not Scrap.blocker(game, Vector2i(20,22)).is_empty(), "A room with crew inside cannot be scrapped")
	actor.foot=saved_foot
	actor.primary_room=Vector2i(20,22);actor.goal_cell=Vector2i(20,22);actor.goal="curiosity";actor.path=PackedVector2Array([Vector2(1,1)])
	# Scrap the leaf.
	game.resources.metal=0
	var gained: int=Scrap.scrap(game, Vector2i(20,22))
	check(gained == 1 and int(game.resources.metal) == 1, "Scrapping refunds Metal (%d, now %s)" % [gained, game.resources.metal])
	check(not game.occupied.has(Vector2i(20,22)) and not game.placed_rooms.any(func(r): return r.pos==Vector2i(20,22)), "Scrapped room is gone")
	check(not game.powered_room_cells.has(Vector2i(20,22)), "Scrapped room draws no power")
	check(actor.primary_room != Vector2i(20,22), "Crew lose a scrapped primary workplace")
	check(actor.goal != "curiosity" or actor.goal_cell != Vector2i(20,22), "Crew drop a goal in the scrapped room")
	check(Scrap.scrap(game, Vector2i(20,22)) == 0, "Scrapping empty seabed does nothing")
	# The now-leaf first corridor can go too.
	check(Scrap.blocker(game, Vector2i(20,21)).is_empty(), "After its neighbour goes, the first corridor is a leaf")
	# Through the inspector: press twice to confirm.
	game.running=true;game.paused=false
	game.selected_room_cell=Vector2i(20,21);game.hovered_card_id="";game.selected_card_id=""
	game._refresh_inspector()
	check(game.room_scrap_button.visible and not game.room_scrap_button.disabled and game.room_scrap_button.text.contains("+1"), "Inspector offers SCRAP for a leaf room (%s)" % game.room_scrap_button.text)
	game._scrap_inspected_room()
	check(game.occupied.has(Vector2i(20,21)) and game.room_scrap_button.text.begins_with("CONFIRM"), "First press only arms the scrap")
	game._scrap_inspected_room()
	check(not game.occupied.has(Vector2i(20,21)), "Second press scraps the room")
	game.selected_room_cell=core;game._refresh_inspector()
	check(game.room_scrap_button.visible and game.room_scrap_button.disabled, "The core shows SCRAP disabled, with the reason as its tooltip")
	actor.active=saved_active
	game.free()
	print("ROOM SCRAP failures=", failures)
	quit(0 if failures == 0 else 1)
