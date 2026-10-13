extends SceneTree
## Diagnostic source/root audition only. No mortality or normal selection edits.
const LIFE=preload("res://scripts/crew_life.gd")
const OUT="res://output/veld-lounge-partial-fall-north-contact-v1/"
const CELL=Vector2i(20,21)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(OUT)
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true);game.meta.save_path="user://veld-lounge-fall-contact.meta";game.run_save_path="user://veld-lounge-fall-contact.loop";game.Preferences.save_path="user://veld-lounge-fall-contact.cfg"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game._set_paused(true,false)
	for other in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:other.active=false
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant real site")
	game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.powered_room_cells[CELL]=true
	var actor=game.veld_npc;await actor.rebuild(game)
	var station:Dictionary={}
	for candidate in actor.RoomActivity.stations(actor.geometry[CELL]):
		if candidate.get("mode","")=="sit" and candidate.facing=="north" and actor.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(candidate.point)):station=candidate;break
	check(not station.is_empty(),"Actual clear North lounge station")
	if failures:quit(1);return
	var player=game.grid_view.veld_player
	player.load_manifest("res://character/veld-lounge-partial-fall-north-v1/bare-manifest.json",true);check(player.frames.has("death-lounge-partial-north"),"Fixture-only bare source pack")
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-lounge-partial-fall-north-v1/helmet-manifest.json"),"Fixture-only helmet source pack")
	game.summary_layer.visible=false;game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var records:Array=[]
	for equipped in [false,true]:
		actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="fatigue";actor.path.clear();actor.expedition.clear();actor.helmet_equipped=equipped;actor.movement_medium="dry";actor.goal_cell=CELL;actor.direction="north";actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point)
		actor.needs={"hunger":0.0,"fatigue":20.0,"curiosity":0.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
		check(LIFE.begin(actor,station),"Actual lounge stage dispatch")
		var foot:Vector2=actor.foot
		var pool:Dictionary=player.equipment_frames["diving-helmet"] if equipped else player.frames
		var timing:Dictionary=player.equipment_timing["diving-helmet"] if equipped else player.timing
		var sources:Array=pool["death-lounge-partial-north"]
		for pose in 6:
			# Audition a prescribed root path through the existing LIFE offset API.
			# Partial-entry/buckle retain partial chair root; brace half-way, roll/rest at floor.
			var seat_amount:float=[.3125,.3125,.15625,0.0,0.0,0.0][pose]
			actor.stage="life_sit";actor.timer=.8*(1-seat_amount)
			pool["sit-down-north"]=[sources[pose]];timing["sit-down-north"]={"durations":[1000],"loop":false}
			sources[pose].set_meta("crew_seat_contact_depth",pose<2)
			player.current_key="";player.last_time=-1;game.visual_time_seconds=400
			var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
			check(texture==sources[pose],"Exact audition source submitted")
			check(actor.foot==foot,"Physical navigation foot unchanged")
			var submitted:=false;var rendered:Dictionary={}
			for attempt in 90:
				game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				if game.grid_view.content_canvases.has(CELL):
					for slot in game.grid_view.content_canvases[CELL].slots:
						if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture:
							submitted=true;rendered={"position":slot.item.member.position,"depth":slot.item.sort_y}
				if submitted:break
			check(submitted,"Actual retained room crew source")
			var name:String=("helmet" if equipped else "bare")+"-pose-%d"%pose
			check(root.get_texture().get_image().save_png(OUT+name+"-room.png")==OK,"Actual room capture")
			check(texture.get_image().save_png(OUT+name+"-source.png")==OK,"Exact source capture")
			records.append({"name":name,"pose":pose,"equipped":equipped,"station":station,"physicalFoot":foot,"offset":LIFE.offset(actor),"seatAmount":seat_amount,"rendered":rendered})
	var file=FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"records":records,"scope":"Default rotation0 North lounge, paired source poses; fixture-only prescribed seat-root path through LIFE offset, no mortality/Continue/normal installation proof"},"\t"));file.close()
	check(root.get_texture().get_image().save_png(OUT+"final.png")==OK,"Fresh final native capture")
	print("VELD PARTIAL LOUNGE FALL CONTACT: %d checks,%d failures;12 native source poses"%[checks,failures]);quit(1 if failures else 0)

