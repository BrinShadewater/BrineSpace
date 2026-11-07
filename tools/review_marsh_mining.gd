extends "res://tools/review_marsh_water_actions.gd"
## Four complete mineral trips, with actual route facings and mineral accounting.
func run():
	if not OS.get_environment("APPDATA").contains("marsh-water-actions") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1600,900);seed(20261015)
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://mining.meta";game.run_save_path="user://mining.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.dismiss();game.tick_timer.stop()
	capture_dir="res://output/marsh-mining-2026-10-15/native"
	DirAccess.make_dir_recursive_absolute(capture_dir);expedition_kind="mining"
	for rotation in range(4):
		north_route=rotation==3
		await journey("delivery",rotation)
	check(not game.testing_free_build and not game.testing_disable_failures,"normal economy/failure flags retained")
	var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"journeys":reports,"kind":expedition_kind,"reward":{"metal":2},"scope":"Four actual dispatch mineral journeys on prescribed station/site fixtures, production pathfinding and actor update. Native captures sample unique source holds; not real-time FPS evidence."},"  "));f.close()
	game.free();print("MARSH MINING NATIVE: ",checks," checks; ",reports.size()," complete trips; failures=",failures)
	quit(1 if failures else 0)
