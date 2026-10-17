extends SceneTree
## Focused selected-art review through the real lounge activity and grid renderer.
var game
var failures:=0
var checks:=0
func check(ok: bool,why: String):
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init():call_deferred("run")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var args:=OS.get_cmdline_user_args()
	var actor: String=args[0] if not args.is_empty() else "branforth"
	if actor not in ["veld","branforth"]:quit(2);return
	var sleeping: bool=true
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch APPDATA required")
	if failures:quit(2);return
	var room_id: String="crew_hab" if sleeping else "crew_lounge"
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://seating-review-%d.meta"%OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame

	# Explicit retained room-art fixture, not the current station-prop bunk layout.
	var store=preload("res://scripts/room_layout_store.gd")
	store.loaded=true;store.data={};store.defaults_path="res://character/james-north-rest-polish-v1/no-layout-overrides.json"
	var retained=preload("res://rooms/whole-room/crew_hab_view.gd").new()
	retained.embedded=true;retained.hide();game.grid_view.add_child(retained)
	game.grid_view.crew_hab_view=retained
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	game.crew_comms.set_process(false);game.crew_comms.minimize()
	for npc in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:npc.active=false
	var cell:=Vector2i(20,20)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear()
	game.selected_rotation=0;game._place_room(room_id,cell,true)
	game.powered_room_cells[cell]=true
	var npc=game.veld_npc if actor=="veld" else game.branforth_npc
	npc.rebuild(game);npc.active=true
	npc.decision_rng=RandomNumberGenerator.new();npc.decision_rng.seed=881
	var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	var entry: int=npc.nearest_in_room(center,cell,false)
	check(entry>=0,"Lounge has navigation entry")
	if entry<0:quit(1);return
	npc.foot=npc.graph.get_point_position(entry)
	for key in npc.needs:npc.needs[key]=0.0
	npc.needs.fatigue=100.0;npc.service_preferences.fatigue=[room_id]
	npc.choose_goal(game)
	for step in range(1000):
		if npc.path.is_empty():break
		npc.move(0.1)
	check(npc.path.is_empty(),"Lounge approach completes")
	check(npc.begin_room_activity(),"Activity begins at actual furniture")
	check(npc.stage==("life_lie" if sleeping else "life_sit"),"Furniture selects expected transition")
	check(npc.direction=="north","Authored furniture uses north-facing rest")
	npc.timer=0.01;npc.update(game,0.02)
	check(npc.stage==("life_sleep" if sleeping else "life_seated"),"Resting pose reached")
	game.selected_card_id="";game.selected_room_cell=cell
	game._set_grid_zoom(1.3,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all()
	await process_frame
	game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
	game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	var player=game.grid_view.veld_player if actor=="veld" else game.grid_view.branforth_player
	if "north-seating-candidate" in args:
		check(actor=="veld" and not sleeping,"North seating candidate scope")
		player.load_manifest("res://character/veld-identity-correction-v1/review/seated-north-body-01/trial-manifest.json",true)
	npc.helmet_equipped=true
	var frame: Texture2D=player.equipment_frames["diving-helmet"]["sleep-north" if sleeping else "sit-idle-north"][0]
	check(frame.get_meta("crew_standing_height")==148.0,"Grid uses selected detailed revision")
	if sleeping and frame.has_meta("crew_rest_head_offset"):
		var life=preload("res://scripts/crew_life.gd")
		var local: Vector2=npc.foot-center
		var station: Dictionary=npc.RoomActivity.at(npc.geometry[cell],local)
		check(station.has("rest_head"),"Retained authored berth has pillow anchor")
		if not station.has("rest_head"):quit(1);return
		var correction: Vector2=life.head_alignment(npc,player)
		check((Vector2(station.rest_point)+correction+Vector2(frame.get_meta("crew_rest_head_offset"))).distance_to(station.rest_head)<0.01,"Sleep head reaches authored pillow")
		var saved_timer: float=npc.timer
		npc.stage="life_lie";npc.timer=0.8
		check(life.head_alignment(npc,player).length()<0.01,"No head correction before lie-down")
		npc.timer=0.4
		check(life.head_alignment(npc,player).distance_to(correction*0.5)<0.01,"Lie-down eases head alignment")
		npc.stage="life_get_up";npc.timer=0.0
		check(life.head_alignment(npc,player).length()<0.01,"Get-up removes head correction")
		npc.stage="life_sleep";npc.timer=saved_timer

	var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-north-rest-polish-v1/bare-manifest.json"))
	for state in manifest.states:
		var key: String=state.id
		check(player.frames[key].size()==6,"Six authored slots "+key)
		var elapsed: float=0.0
		for slot in range(6):
			var tex: Texture2D=player.frames[key][slot]
			var disk:=Image.load_from_file("res://character/james-north-rest-polish-v1/"+state.frameFiles[slot])
			check(tex.get_image().get_data()==disk.get_data(),"Exact authored pixels "+key+str(slot))
			check(tex.get_meta("crew_pivot")==Vector2(128,224),"Pivot "+key)
			check(tex.get_meta("crew_standing_height")==148.0,"Scale metadata "+key)
			check(tex.get_meta("crew_depth_offset")==state.depthOffsets[slot],"Furniture depth "+key)
			check(player.frame_at_elapsed(key,elapsed+float(state.frameDurationsMs[slot])/2000.0)==tex,"Simulation clock slot "+key+str(slot))
			elapsed+=float(state.frameDurationsMs[slot])/1000.0
		check(absf(player.cycle_seconds(key)-elapsed)<0.001,"Cycle duration "+key)
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var out: String="res://character/james-north-rest-polish-v1/retained-berth-helmet/"+actor+"/seating-room/"
	if "north-seating-candidate" in args:out="res://character/james-north-rest-polish-v1/retained-berth-helmet/veld/seating-north-candidate-01/"
	DirAccess.make_dir_recursive_absolute(out)
	root.get_texture().get_image().save_png(out+("berth-q0-north.png" if sleeping else "lounge-q0-north.png"))
	if "north-seating-candidate" in args:
		var samples: Array=[]
		for phase in ["life_sit","life_rise"]:
			npc.stage=phase;npc.timer=0.8
			for sample in range(8):
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var filename: String="%s-%02d.png"%[phase,sample]
				root.get_texture().get_image().save_png(out+filename)
				samples.append({"file":filename,"stage":npc.stage,"elapsed":0.8-npc.timer,"offset":str(preload("res://scripts/crew_life.gd").offset(npc))})
				npc.update(game,0.1)
		var record:=FileAccess.open(out+"transition-samples.json",FileAccess.WRITE)
		if record:record.store_string(JSON.stringify(samples,"\t"));record.close()

	var rest_timer: float=npc.timer
	for action in ["lie-down","sleep","get-up"]:
		var key: String=action+"-north"
		var elapsed: float=0.0
		for slot in range(6):
			npc.stage="life_lie" if action=="lie-down" else ("life_get_up" if action=="get-up" else "life_sleep")
			var midpoint: float=elapsed+float(player.timing[key].durations[slot])/2000.0
			npc.timer=rest_timer if action=="sleep" else 0.8-midpoint
			player.current_key=key;player.phase=midpoint
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(out+"%s-%02d.png"%[action,slot])
			# An opaque furniture layer can hide the body while loader checks pass.
			var visible:=root.get_texture().get_image().get_region(Rect2i(330,123,270,177))
			npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			var background:=root.get_texture().get_image().get_region(Rect2i(330,123,270,177))
			npc.active=true
			check(visible.get_data()!=background.get_data(),"Actor visible in retained berth "+action+str(slot))

			elapsed+=float(player.timing[key].durations[slot])/1000.0
		npc.stage="life_sleep";npc.timer=rest_timer
	var geometry_file:=FileAccess.open("res://character/james-north-rest-polish-v1/retained-berth-helmet/geometry.json",FileAccess.WRITE)
	var stations: Array=preload("res://scripts/crew_room_activity.gd").stations(npc.geometry[cell])
	geometry_file.store_string(JSON.stringify({"actor":actor,"direction":npc.direction,"foot":str(npc.foot),"offset":str(preload("res://scripts/crew_life.gd").offset(npc)),"stations":stations},"\t"));geometry_file.close()
	print("JAMES RETAINED HELMET BERTH: ",checks," checks; ",failures," failures; direction=",npc.direction," stage=",npc.stage," foot=",npc.foot," render_offset=",preload("res://scripts/crew_life.gd").offset(npc))
	quit(1 if failures else 0)
