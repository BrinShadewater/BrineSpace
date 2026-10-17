extends SceneTree
const OUT := "res://character/james-rest-south-identity-v2/"
const CELL := Vector2i(20,20)
var game
var checks := 0
var failures := 0
var records: Array = []
func check(ok: bool, label: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(label)
func _init() -> void:
	call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if not "brine-james-native-" in OS.get_environment("APPDATA") or OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(OUT+"native")
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://james-south-rest.meta";game.run_save_path="user://james-south-rest.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Normal James core release")
	game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("corridor",CELL,true)
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player
	npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="dry";npc.state="idle"
	npc.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(0,70);npc.goal_cell=CELL;npc.direction="south";npc.bunk_motion.clear()
	game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(1.8,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0);game._refresh_all()
	await process_frame
	game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
	game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	for mode in ["bare","helmet"]:
		var gear: String="" if mode=="bare" else "diving-helmet"
		npc.helmet_equipped=mode=="helmet"
		var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+mode+"-manifest.json"))
		var selected: Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		for state in pack.states:
			npc.stage={"lie-down-south":"life_lie","sleep-south":"life_sleep","get-up-south":"life_get_up"}[state.id]
			player.current_key="";player.motion.clear();game.visual_time_seconds=100;npc.timer=10.4 if npc.stage=="life_sleep" else .8
			game.grid_view._get_branforth_frame(game)
			var elapsed:=0.0
			for i in range(state.frameFiles.size()):
				var disk:=Image.load_from_file(ProjectSettings.globalize_path((OUT+mode+"-manifest.json").get_base_dir().path_join(state.frameFiles[i])))
				var frame: Texture2D=selected[state.id][i]
				check(frame.get_image().get_data()==disk.get_data(),"Normal loader pixels "+mode+state.id+str(i))
				check(frame.get_meta("crew_pivot")==Vector2(128,224) and frame.get_meta("crew_standing_height")==148.0,"Fixed source ruler")
				check(frame.get_meta("crew_depth_offset")==state.depthOffsets[i],"Retained depth metadata")
				var midpoint: float=elapsed+float(state.frameDurationsMs[i])/2000.0
				check(player.frame_at_elapsed(state.id,midpoint,gear).get_image().get_data()==disk.get_data(),"Native action slot "+str(i))
				game.visual_time_seconds=100+midpoint;npc.timer=(10.4 if npc.stage=="life_sleep" else .8)-midpoint
				var rendered: Texture2D=game.grid_view._get_branforth_frame(game)
				check(rendered.get_image().get_data()==disk.get_data(),"Prescribed NPC life pose "+mode+state.id+str(i))
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var ref: String=OUT+"native/"+mode+"-"+state.id+"-"+str(i)+".png"
				check(root.get_texture().get_image().save_png(ref)==OK,"Native pose capture")
				records.append({"mode":mode,"key":state.id,"index":i,"elapsed":midpoint,"capture":ref})
				elapsed+=float(state.frameDurationsMs[i])/1000.0
			check(absf(player.cycle_seconds(state.id,gear)-elapsed)<.0001,"Native full cycle")
			if state.id=="sleep-south":check(frame_rest_anchor(selected[state.id][0],state),"Rest head metadata")
	var report:=FileAccess.open(OUT+"validate-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Normal loader and all36 prescribed South life-stage source slots via normal NPC renderer, native captures and clocks/metadata. No actual service navigation, furniture contact, disk Continue or gear-change journey; retained ordinary berths select North and specialized East bunk is separate."},"  "))
	if not FileAccess.file_exists(OUT+"validate.gd.uid"):
		var file:=FileAccess.open(OUT+"validate.gd.uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES SOUTH REST IDENTITY: ",checks," checks; ",failures," failures; native source captures ",records.size())
	quit(1 if failures else 0)
func frame_rest_anchor(frame: Texture2D,state: Dictionary) -> bool:
	return frame.get_meta("crew_rest_head_offset")==Vector2(state.restHeadOffset[0],state.restHeadOffset[1])
