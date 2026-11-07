extends "res://tests/test_veld_seated_north_continue.gd"
const BREATH="res://character/veld-seated-north-breathing-source-v1/"
const FRONT_OUT="res://output/veld-seat-front-continue-v1/"
func _init():
	var path="res://tests/test_veld_seat_front_continue.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=await super.fresh()
	game.grid_view.veld_player.load_manifest(BREATH+"bare-manifest.json",true)
	check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet",BREATH+"helmet-manifest.json"),"Paired breathing in fresh checkpoint scene")
	return game
func photo(game,name:String,texture:Texture2D,depth:float):
	game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(2,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var ready:=false
	for attempt in 90:
		game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var submitted:=false
		if game.grid_view.content_canvases.has(CELL):
			for slot in game.grid_view.content_canvases[CELL].slots:
				if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture and is_equal_approx(slot.item.sort_y,depth):submitted=true
		var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
		ready=submitted and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
		if ready:break
	check(ready,"Native retained source/depth and camera after seat Continue")
	check(root.get_texture().get_image().save_png(FRONT_OUT+name)==OK,"Seat front/retained contact capture")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(FRONT_OUT)
	var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(game.veld_npc.active and game.Architects.present(game,"veld"),"Normal release")
	game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.occupied[CELL].rotation=2;game.powered_room_cells[CELL]=true;await game.veld_npc.rebuild(game)
	var records=[]
	for equipped in [false,true]:
		for legacy in [false,true]:
			var actor=game.veld_npc;var station:Dictionary=actor.RoomActivity.stations(actor.geometry[CELL])[0]
			prepare(actor,station,equipped)
			actor.stage="life_seated";actor.timer=6.6
			# Prescribed checkpoint compatibility cases, separate from natural route proof.
			if legacy:actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(64,96)
			var foot:Vector2=actor.foot;var offset:Vector2=LIFE.offset(actor)
			check(offset==Vector2(63.5,37) if legacy else absf(offset.x)<.1,"Retained legacy or aligned new front contact")
			game.visual_time_seconds=400;game.grid_view.veld_player.current_key="";game.grid_view.veld_player.last_time=-1
			game.grid_view._get_veld_live_frame_source(game);game.visual_time_seconds=400.8
			var texture:Texture2D=game.grid_view._get_veld_live_frame_source(game)
			var pixels=texture.get_image().get_data();var depth:float=LIFE.seated_draw_depth(actor,texture,position(actor))
			var name:String=("helmet" if equipped else "bare")+("-legacy" if legacy else "-front")
			await photo(game,name+"-before.png",texture,depth)
			check(actor.valid_veld_snapshot(actor.snapshot()),"Saved contact actor admissible")
			check(SAVE.write(game,game.run_save_path)==OK,"Actual seat contact checkpoint write: "+SAVE.last_error)
			var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Actual checkpoint read")
			game.queue_free();await process_frame;game=await fresh()
			check(await SAVE.restore_staged(game,disk),"Actual fresh-scene seat contact restore: "+SAVE.last_error)
			game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-seat-front-continue.loop"
			actor=game.veld_npc;var restored:Texture2D=game.grid_view._get_veld_live_frame_source(game)
			check(actor.foot==foot and actor.stage=="life_seated" and actor.timer==6.6 and actor.helmet_equipped==equipped,"Contact/action/gear retained")
			check(LIFE.offset(actor)==offset,"Exact old/new chair offset after Continue")
			check(restored.get_image().get_data()==pixels,"Exact displayed breathing source after Continue")
			check(is_equal_approx(LIFE.seated_draw_depth(actor,restored,position(actor)),depth),"Chair depth re-resolves after Continue")
			check(game.paused and is_equal_approx(game.visual_time_seconds,400.8),"Saved breathing visual clock/paused state")
			game._process(.5);check(actor.foot==foot and actor.timer==6.6 and LIFE.offset(actor)==offset,"Paused contact remains stable")
			await photo(game,name+"-after.png",restored,depth)
			records.append({"gear":equipped,"legacy":legacy,"offset":offset,"foot":foot,"depth":depth,"name":name})
			print("FRONT CONTINUE ",name," failures=",failures)
	var file=FileAccess.open(FRONT_OUT+"contacts.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"\t"));file.close()
	check(root.get_texture().get_image().save_png(FRONT_OUT+"final.png")==OK,"Fresh final")
	print("VELD SEAT FRONT CONTINUE: %d checks,%d failures;4 fresh disk restores"%[checks,failures]);quit(1 if failures else 0)
