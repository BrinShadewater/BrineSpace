extends SceneTree
const Social=preload("res://scripts/crew_social.gd")
var failures:=0
func check(ok: bool,message: String):
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.selected_architect="bill";game.meta.save_path="user://social-%d.meta" % OS.get_process_id();game.run_save_path=game.meta.save_path+".loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=false;game.Architects.advance_core(game,10)
	game.recovered_crew.append({"architect_id":"veld","alive":true,"name":"Veld"})
	game.resources.food=30;game.resources.oxygen=30
	var cell:=Vector2i(20,20)
	game.powered_room_cells[cell]=true
	var a=game.bill_npc;var b=game.veld_npc
	a.rebuild(game);b.rebuild(game)
	var found:=false
	for first in a.room_nodes[cell]:
		for second in b.room_nodes[cell]:
			a.foot=a.graph.get_point_position(first);b.foot=b.graph.get_point_position(second)
			if a.foot.y>7980 and b.foot.y>7980 and a.foot.distance_to(b.foot)>=80 and Social.nearby(a,b):found=true;break
		if found:break
	check(found,"Reachable distinct social positions exist")
	for actor in [a,b]:
		actor.active=true;actor.goal="";actor.stage="";actor.path.clear();actor.timer=0;actor.social_cooldown=0;actor.needs.hunger=20;actor.needs.fatigue=20;actor.needs.curiosity=60
	Social.advance(game,0.1)
	check(a.goal=="social" and b.goal=="social","Nearby crew autonomously form one reciprocal conversation")
	check(a.social_partner=="veld" and b.social_partner=="bill","Partners reference each other")
	a.update(game,0.1);b.update(game,0.1)
	check(a.goal=="social" and b.goal=="social" and a.timer==6 and b.timer==6,"Actor routines preserve paired timer ownership")
	var saved_a: Dictionary=a.snapshot();var saved_b: Dictionary=b.snapshot()
	check(a.valid_snapshot(saved_a) and b.valid_snapshot(saved_b),"Conversation snapshots validate")
	game.paused=true;Social.advance(game,2)
	check(a.timer==6 and b.timer==6,"Pause freezes both conversation timers")
	game.paused=false;Social.advance(game,1)
	check(a.state!=b.state,"One speaker and one listener")
	if DisplayServer.get_name()!="headless":
		game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(0.65,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all()
		await process_frame;await process_frame
		game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/crew-social.png")
	Social.advance(game,3)
	check(a.state=="idle" and b.state=="interact","Partners take turns speaking")
	Social.advance(game,2)
	check(a.goal=="" and b.goal=="" and is_equal_approx(a.needs.curiosity,45.022),"Completed exchange releases both and relieves curiosity")
	Social.advance(game,0.1)
	check(a.goal!="social","Cooldown prevents immediate repeat")
	a.restore_snapshot(game,saved_a);b.restore_snapshot(game,saved_b)
	Social.advance(game,0.1)
	check(a.goal=="social" and b.goal=="social","Restored pair resumes")
	a.needs.hunger=70;Social.advance(game,0.1)
	check(a.goal=="" and b.goal=="","Urgent hunger releases both partners")
	a.restore_snapshot(game,saved_a);b.restore_snapshot(game,saved_b)
	a.goal="fire-retreat";Social.advance(game,0.1)
	check(a.goal=="fire-retreat" and b.goal=="","Emergency goal survives and partner is released")
	a.social_cooldown=0;b.social_cooldown=0;a.goal="construction";Social.advance(game,0.1)
	check(a.goal=="construction" and b.goal!="social","Conversations never claim an active builder")
	var invalid: Dictionary=saved_a.duplicate(true);invalid.social_cooldown=NAN
	check(not a.valid_snapshot(invalid),"Invalid cooldown rejected")
	print("CREW SOCIAL failures=",failures)
	game.queue_free();await process_frame;quit(1 if failures else 0)
