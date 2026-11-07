extends SceneTree
const Save=preload("res://scripts/run_save.gd")
var game
var failures:=0
func check(ok:bool,message:String)->void:
	if not ok:failures+=1;print("FAIL: ",message)
func _initialize()->void:run.call_deferred()
func run()->void:
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://pattern-checkpoint.meta";game.run_save_path="user://pattern-checkpoint.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.minimize();game.toast_playing=true
	var before:Dictionary=Save.capture(game).duplicate(true)
	game._award_synergy_stabilization(game.SynergyManagerScript.get_synergy("closed_air_loop"))
	var after:Dictionary=Save.capture(game).duplicate(true)
	var paid:int=game.meta.total_research_points
	check(Save.restore(game,before),"Earlier checkpoint restores after stabilization was earned")
	check(game.meta.stabilized_synergy_ids.has("closed_air_loop"),"Profile keeps earned progress when the checkpoint is older")
	check(not game._synergy_bonus_doubled("closed_air_loop"),"Older checkpoint cannot turn a current-loop reward into an inherited double")
	check(game.meta.total_research_points==paid,"Continue does not pay Archived Data again")
	check(Save.restore(game,after),"Post-stabilization checkpoint restores")
	check(not game._synergy_bonus_doubled("closed_air_loop"),"Post-stabilization Continue also waits for next loop")
	var legacy:Dictionary=after.duplicate(true);legacy.erase("inherited_stabilized_synergies")
	check(Save.restore(game,legacy),"Checkpoint without the new optional field remains loadable")
	check(not game._synergy_bonus_doubled("closed_air_loop"),"Legacy current-loop list preserves the known new reward timing")
	var invalid:Dictionary=after.duplicate(true);invalid.inherited_stabilized_synergies={"closed_air_loop":1}
	check(not Save.restore(game,invalid),"Malformed inherited bonus state is rejected")
	check(not Save.problem(invalid).is_empty(),"Disk validation also rejects malformed inherited bonuses")
	game._start_reboot_cycle();game.set_process(false);game.tick_timer.stop()
	check(game._synergy_bonus_doubled("closed_air_loop"),"A real next loop inherits the doubled bonus")
	game.free()
	var music=root.get_node_or_null("StationMusic")
	if music!=null:music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	await create_timer(.2).timeout
	print("STABILIZATION CHECKPOINT failures=",failures);quit(1 if failures else 0)
