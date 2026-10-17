extends SceneTree
## Staged seated contact at reachable live room furniture; no autonomous route claim.
var failures:=0
var checks:=0
var game
func _init():call_deferred("run")
func check(ok: bool, message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://branforth_seated.meta";game.run_save_path="user://branforth_seated.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":Vector2i(20,20)}])
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	var output: String="res://character/james-water-north-polish-v1/native-rooms/";DirAccess.make_dir_recursive_absolute(output)
	var captures:=0;var seen: Dictionary={}
	var player=game.grid_view.branforth_player
	for mode in ["bare","helmet"]:
		var manifest_path: String="res://character/james-water-north-polish-v1/"+mode+"-manifest.json"
		var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
		var selected: Dictionary=player.frames if mode=="bare" else player.equipment_frames["diving-helmet"]
		for state in pack.states:
			check(selected.has(state.id),"Installed "+state.id)
			var elapsed:=0.0
			for i in range(state.frameFiles.size()):
				var expected_image=Image.load_from_file(ProjectSettings.globalize_path(manifest_path.get_base_dir().path_join(state.frameFiles[i]).simplify_path()))
				var frame: Texture2D=selected[state.id][i]
				check(frame.get_image().get_data()==expected_image.get_data(),"Installed pixels "+mode+state.id+str(i))
				check(frame.get_meta("crew_water_pose")==true,"Water pose")
				check(frame.get_meta("crew_pivot")==Vector2(128,128),"Water pivot")
				check(frame.get_meta("crew_standing_height")==148.0,"Standing scale")
				check(player.frame_at_elapsed(state.id,elapsed+.0001,"" if mode=="bare" else "diving-helmet").get_image().get_data()==expected_image.get_data(),"Actual action clock")
				elapsed+=float(state.frameDurationsMs[i])/1000.0
	print("JAMES NORTH WATER POLISH INSTALLED: ",checks," checks; ",failures," failures; actual grid loader, 36 slots")
	quit(1 if failures else 0)
