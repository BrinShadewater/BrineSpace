extends SceneTree
## Real controller/grid boundaries across all six visual work phases, directions and gear.
const Expedition = preload("res://scripts/crew_expedition.gd")
var checks := 0
var failures := 0
var report := []
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"), "Scratch profile")
	if failures: quit(1); return
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://phases.meta"; game.run_save_path = "user://phases.loop"
	root.add_child(game); current_scene = game; game.set_process(false); game.tick_timer.stop()
	var grid = game.grid_view; var player = grid.human_water_player
	player.load_manifest("res://character/bill-salvage-pickup-family-v1/bare-manifest.json", true)
	check(player.load_equipment_manifest("diving-helmet", "res://character/bill-salvage-pickup-family-v1/helmet-manifest.json"), "Candidate family equipment")
	var home := Vector2i(20,19); var target := Vector2i(20,16)
	game.wrecks.erase(home); game._place_room("airlock", home, true)
	game.occupied[home].rotation = 0; game.powered_room_cells[home] = true; game.running = true; game.hardware.power = true
	var actor = game.bill_npc
	for direction in ["east", "west", "north", "south"]:
		var return_direction: String = {"east":"west", "west":"east", "north":"south", "south":"north"}[direction]
		var approach: Vector2 = {"east":Vector2(-384,0), "west":Vector2(384,0), "north":Vector2(0,384), "south":Vector2(0,-384)}[direction]
		for gear in [false,true]:
			for recall in [false,true]:
				for offset in 6:
					var name: String = direction + (" helmet" if gear else " bare") + (" recall" if recall else " nominal") + " phase " + str(offset)
					game.drone_fleet.sites = {target:game.drone_fleet.Sites.make_site("salvage",3)}
					actor.active = true; actor.dead = false; actor.stage = ""; actor.state = "idle"; actor.direction = direction; actor.helmet_equipped = gear; actor.movement_medium = "exterior"; actor.breath_oxygen = 100; actor.tank_oxygen = 100
					actor.foot = Vector2(8064,6336); actor.expedition = {"kind":"salvage", "phase":"salvage", "home":home, "target":target, "elapsed":0.0, "cargo":{}, "recall":false, "route":PackedVector2Array(), "sea_route":PackedVector2Array([actor.foot+approach,actor.foot])}
					player.current_key = ""; player.current_equipment = ""; player.motion.clear(); player.last_time = -1; player.phase = 0
					var first_return := -1; var pickup_seen := false; var exits := []; var previous: Texture2D; var previous_phase := ""
					for tick in 480:
						if recall and tick == 73: actor.expedition.recall = true
						if tick > 0: Expedition.advance(game, actor, 1.0/60.0)
						game.visual_time_seconds = float(tick)/60.0 + offset*.14
						var state: String = actor.animation_state(); var texture: Texture2D = grid._get_human_frame_source(state,actor.direction)
						check(texture != null, name + " renderer")
						var phase: String = actor.expedition.phase
						if phase == "pickup":
							pickup_seen = true
							check(actor.expedition.cargo.is_empty() and game.drone_fleet.sites[target].units == 3, name + " no early extraction")
							check(texture == player.frame_at_elapsed("swim-pickup-"+direction, actor.action_elapsed(), "diving-helmet" if gear else ""), name + " pickup clock independent of visual offset")
						if phase != previous_phase and previous != null:
							exits.append({"tick":tick, "from":previous_phase, "to":phase, "visualOffset":offset*.14, "previousPixelHash":previous.get_image().get_data().hex_encode().sha256_text(), "nextPixelHash":texture.get_image().get_data().hex_encode().sha256_text()})
						if phase == "return" and first_return < 0:
							first_return = tick
							check(state == ("swim" if recall else "swim-carry"), name + " prone return boundary")
						if first_return >= 0 and tick == first_return+1:
							check(actor.direction == return_direction, name + " return heading")
							check(player.motion.get("clip", "") == ("swim-turn-" if recall else "swim-carry-turn-")+direction+"-"+return_direction, name + " selected return half-turn")
						previous = texture; previous_phase = phase
						if first_return >= 0 and tick >= first_return+80:
							check(player.motion.get("clip", "") == "", name + " half-turn completes")
							break
					check(pickup_seen and first_return >= 0, name + " pickup and return reached")
					check(game.drone_fleet.sites[target].units == (3 if recall else 2), name + " extraction rule")
					check(actor.expedition.cargo.is_empty() == recall, name + " cargo rule")
					report.append({"name":name, "exits":exits, "firstReturnTick":first_return})
	var file = FileAccess.open("res://output/bill-work-pickup-phase-boundaries-v1/timeline.json", FileAccess.WRITE); file.store_string(JSON.stringify(report,"\t")); file.close()
	game.queue_free(); print("BILL PHASE BOUNDARIES: %d checks,%d failures; %d routes" % [checks,failures,report.size()]); quit(1 if failures else 0)
