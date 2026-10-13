extends SceneTree
const OUT="res://output/bill-meal-counter-contact-candidate-v1/"
var game
var checks:=0
var failures:=0
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-meal-contact.meta";game.run_save_path="user://bill-meal-contact.loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	var cell:=Vector2i(20,20);var player=game.grid_view.human_water_player;var records:=[];var count:=0
	player.load_manifest("res://character/bill-meal-north-family-v1/manifest.json",true)
	player.load_manifest("res://character/bill-meal-south-family-v1/manifest.json",true)
	for q in range(4):
		game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=q;game._place_room("galley",cell,true);game.powered_room_cells[cell]=true
		var actor=game.bill_npc;await actor.rebuild(game)
		var data: Dictionary=actor.geometry[cell];var stations: Array=actor.RoomActivity.stations(data)
		check(not stations.is_empty(),"Galley offers actual registered contact q%d"%q)
		for station in stations:
			actor.active=true;actor.dead=false;actor.stage="";actor.state="idle";actor.timer=0;actor.path.clear();actor.movement_medium="dry";actor.helmet_equipped=false;actor.goal="curiosity";actor.goal_cell=cell;actor.inspection_return_pose=-1
			actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing;actor.breath_oxygen=15;actor.tank_oxygen=60;actor.starvation=0
			check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"Normal chooser starts bare meal at real station")
			check(actor.stage=="life_eat" and is_equal_approx(actor.timer,6),"Original bare six-second meal consumer")
			var contact: Vector2=actor.foot;var facing: String=actor.direction;var prop: Dictionary={}
			for item in data.get("props",[]):
				if item.id==station.prop:prop=item
			check(not prop.is_empty(),"Station identifies actual rendered counter")
			game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
			game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
			var samples: Array=[["eat-enter",2],["eat-enter",3],["eat",0],["drink-enter",2],["drink-enter",3],["drink",0]] if q==0 else [["eat-enter",3],["drink-enter",3]]
			for sample in samples:
				var action: String=sample[0];var pose: int=sample[1];var key: String=action+"-"+facing;var render_action: String="drink" if action.begins_with("drink") else "eat"
				actor.stage="life_drink" if render_action=="drink" else "life_eat";actor.timer=2 if render_action=="drink" else 4
				# Static candidate source injection into existing bare rendering, not a
				# claim that the activity clock already dispatches pickup/return phases.
				var texture: Texture2D=player.frames[key][pose]
				game.grid_view.human_animations[render_action][facing]=[texture];game.grid_view.human_animation_timing[render_action+"-"+facing]={"durations":[1000],"loop":true,"seconds":1.0}
				check(game.grid_view._get_human_frame_source(actor.animation_state(),facing)==texture,"Actual grid renders exact staged contact pose")
				game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var name: String="q%d-station%d-%s-%d.png"%[q,count,action,pose]
				check(root.get_texture().get_image().save_png(OUT+name)==OK,"Native actual galley candidate capture")
				check(actor.foot==contact and actor.can_stand(actor.foot),"Candidate art does not change actual contact geometry")
				records.append({"rotation":q,"station":station,"counter":prop,"action":action,"pose":pose,"source_key":key,"screenshot":name,"foot":actor.foot})
			count+=1;actor.active=false
	check(not records.is_empty(),"Contact evidence gathered")
	await RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")==OK,"Fresh native final contact view")
	var file:=FileAccess.open(OUT+"contacts.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"actual chooser/positions/room renderer with static candidate art injection; no new meal phase/interrupt/restore proof","stations":count,"captures":records},"\t"));file.close()
	print("BILL MEAL CONTACT CANDIDATES: %d checks,%d failures; %d stations/%d captures"%[checks,failures,count,records.size()]);quit(1 if failures else 0)
