extends SceneTree
const OUT="res://output/veld-seated-north-station-v1/"
const PACK="res://character/veld-seated-north-coherent-v1/"
const LIFE=preload("res://scripts/crew_life.gd")
var checks:=0
var failures:=0
var game
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var uid_path="res://tests/test_veld_seated_north_station.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid=FileAccess.open(uid_path,FileAccess.WRITE);uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://veld-seat-station.meta";game.run_save_path="user://veld-seat-station.loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for other in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:other.active=false
	var cell:=Vector2i(20,20);var npc=game.veld_npc;var grid=game.grid_view;var player=grid.veld_player
	player.load_manifest(PACK+"bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet",PACK+"helmet-manifest.json"),"Fixture-only paired seated candidate")
	var records:=[];var station_audit:=[]
	for rotation in range(4):
		game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.selected_rotation=rotation;game._place_room("crew_lounge",cell,true);game.powered_room_cells[cell]=true
		await npc.rebuild(game)
		var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);var chosen:Dictionary={}
		for station in stations:
			if station.get("mode","")=="sit" and station.get("facing","")=="north" and npc.can_stand((Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point)):
				chosen=station;break
		station_audit.append({"rotation":rotation,"stations":stations,"props":npc.geometry[cell].get("props",[]),"chosen":chosen})
		check(not chosen.is_empty(),"Actual lounge provides a clear north seated approach")
		if chosen.is_empty():continue
		game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
		game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		for equipped in [false,true]:
			npc.active=true;npc.dead=false;npc.state="idle";npc.stage="";npc.goal="fatigue";npc.path.clear();npc.expedition.clear();npc.helmet_equipped=equipped;npc.movement_medium="dry";npc.goal_cell=cell;npc.direction="north";npc.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(chosen.point);npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0
			check(LIFE.begin(npc,chosen) and npc.stage=="life_sit" and not npc.bunk_motion_active(),"Actual lounge chooses chair-height seated stage")
			var foot:Vector2=npc.foot
			for elapsed in [0.0,.079999,.08,.18,.32,.48,.64,.799]:
				npc.stage="life_sit";npc.timer=.8-elapsed
				var before:Texture2D=grid._get_veld_live_frame_source(game)
				var before_at:Vector2=foot-(Vector2(cell)+Vector2.ONE*.5)*384+LIFE.offset(npc)
				var before_depth:float=LIFE.seated_draw_depth(npc,before,before_at)
				var retained:float=npc.interrupted_sit_rise_seconds(game)
				npc.stage="life_rise";npc.timer=retained
				var after:Texture2D=grid._get_veld_live_frame_source(game)
				var after_at:Vector2=foot-(Vector2(cell)+Vector2.ONE*.5)*384+LIFE.offset(npc)
				check(after.get_image().get_data()==before.get_image().get_data(),"Interrupted rise retains exact source pose")
				check(after_at.distance_to(before_at)<.0001,"Interrupted rise retains furniture contact position")
				check(is_equal_approx(LIFE.seated_draw_depth(npc,after,after_at),before_depth),"Interrupted rise retains registered seat depth")
				check(npc.foot==foot and npc.valid_veld_snapshot(npc.snapshot()),"Interrupted room pose snapshot valid and navigation foot fixed")
			for phase in [["entry","life_sit",.8],["down-1","life_sit",.72],["down-2","life_sit",.62],["down-3","life_sit",.48],["down-4","life_sit",.32],["down-5","life_sit",.16],["held","life_seated",7.4],["rise-0","life_rise",.8],["rise-1","life_rise",.64],["rise-2","life_rise",.48],["rise-3","life_rise",.32],["rise-4","life_rise",.18],["rise-5","life_rise",.08],["exit","life_rise",0.0]]:
				npc.stage=phase[1];npc.timer=phase[2];game.visual_time_seconds=400;player.current_key="";player.last_time=-1
				var texture:Texture2D=grid._get_veld_live_frame_source(game)
				check(texture!=null and texture.get_meta("crew_standing_height")==148.0,"Candidate uses canonical ruler")
				check(npc.foot==foot,"Seated visual offset leaves navigation foot unchanged")
				check(texture.get_meta("crew_seat_contact_depth",false),"Candidate opts into registered chair contact ordering")
				var at:Vector2=foot-(Vector2(cell)+Vector2.ONE*.5)*384+LIFE.offset(npc)
				var expected:float=maxf(at.y,float(chosen.seat_depth)) if phase[0] not in ["entry","exit"] else at.y
				check(is_equal_approx(LIFE.seated_draw_depth(npc,texture,at),expected),"Seat depth is registered chair front or natural depth")
				texture.remove_meta("crew_seat_contact_depth")
				check(is_equal_approx(LIFE.seated_draw_depth(npc,texture,at),at.y),"Legacy/unmarked texture depth unchanged")
				texture.set_meta("crew_seat_contact_depth",true)
				check(game.has_dr_veld(),"Actor admitted to actual room renderer")
				# Retained surfaces submit child drawing after the grid draw. Wait for
				# the actual crew slot, rather than capturing the previous room frame.
				var submitted:=false
				for attempt in 60:
					grid.queue_redraw();await process_frame
					if grid.content_canvases.has(cell):
						for slot in grid.content_canvases[cell].slots:
							if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture and is_equal_approx(slot.item.sort_y,expected):submitted=true
					if submitted:break
				check(submitted,"Actual retained crew slot contains candidate texture")
				await RenderingServer.frame_post_draw
				var filename:String="rotation-%d-%s-%s.png"%[rotation,"helmet" if equipped else "bare",phase[0]]
				check(root.get_texture().get_image().save_png(OUT+filename)==OK,"Actual lounge candidate capture")
				records.append({"rotation":rotation,"equipped":equipped,"phase":phase[0],"station":chosen,"lifeOffset":LIFE.offset(npc),"physicalFoot":foot,"screenshot":filename})
				if phase[0]=="held":
					# Keep source/position fixed and remove only the opt-in depth hook
					# to preserve an actual uncorrected furniture occlusion comparison.
					texture.remove_meta("crew_seat_contact_depth")
					var depth_submitted:=false
					for attempt in 60:
						grid.queue_redraw();await process_frame
						for slot in grid.content_canvases[cell].slots:
							if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture and is_equal_approx(slot.item.sort_y,slot.item.member.position.y):depth_submitted=true
						if depth_submitted:break
					check(depth_submitted,"Legacy depth submitted with unchanged pose")
					await RenderingServer.frame_post_draw
					check(root.get_texture().get_image().save_png(OUT+filename.replace("held","legacy-depth"))==OK,"Uncorrected depth comparison capture")
					texture.set_meta("crew_seat_contact_depth",true)
			npc.active=false
	var file:=FileAccess.open(OUT+"contacts.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"Default lounge four rotations, fixture-only candidate, prescribed stages; not natural routing/service-loss/Continue or owner layout acceptance","records":records,"stationAudit":station_audit},"\t"));file.close()
	check(records.size()==112,"Four actual rotations, both equipment variants, all source poses and joins")
	check(root.get_texture().get_image().save_png(OUT+"final.png")==OK,"Fresh actual lounge capture")
	print("VELD SEATED NORTH STATION: %d checks,%d failures; %d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
