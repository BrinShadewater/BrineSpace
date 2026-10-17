extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/release-rest-review-v350/"
const ORIGIN=Vector2i(20,20)
const LIFE=preload("res://scripts/crew_life.gd")
var game
var checks:=0
var failures:=0
var captures:Array=[]
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:
	if a==null or b==null:return false
	var aa:Texture2D=a.diffuse_texture if a is CanvasTexture else a
	var bb:Texture2D=b.diffuse_texture if b is CanvasTexture else b
	return aa.get_image().get_data()==bb.get_image().get_data()
func _init()->void:call_deferred("run")
func capture(label:String,npc)->void:
	game.hand_panel.hide();game.card_drag.hide()
	var center:Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var screenshot:Image=root.get_texture().get_image()
	var world:=Rect2(center-Vector2.ONE*game.get_cell_size()*.4,Vector2.ONE*game.get_cell_size()*.8)
	var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:Image=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	check(crop.get_width()>0 and crop.get_height()>0,"Visible native crop")
	check(crop.save_png(OUT+label+".png")==OK,"Save native pose crop")
	captures.append({"file":label+".png","time":game.visual_time_seconds,"motion":game.grid_view.branforth_player.motion.duplicate(true),"foot":[npc.foot.x,npc.foot.y]})
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Isolated APPDATA")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://james-rest350.meta";game.run_save_path="user://james-rest350.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	game.running=true;game.Architects.advance_core(game,10)
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player
	var cases:Array=[]
	for room_id in ["crew_hab","crew_lounge"]:
		for rotation in range(4):
			game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.powered_room_cells.clear()
			game.selected_rotation=rotation;game._place_room(room_id,ORIGIN,true);game.occupied[ORIGIN].rotation=rotation;game.powered_room_cells[ORIGIN]=true
			check(int(game.occupied[ORIGIN].rotation)==rotation,"Fixture exercises requested actual room rotation")
			npc.rebuild(game)
			var stations:Array=npc.RoomActivity.stations(npc.geometry[ORIGIN])
			check(not stations.is_empty(),"Authored rest furniture provides a station")
			if stations.is_empty():continue
			var station:Dictionary=stations[0]
			for gear in ["","diving-helmet"]:
				npc.active=true;npc.dead=false;npc.goal="fatigue";npc.goal_cell=ORIGIN;npc.stage="";npc.state="idle";npc.path.clear();npc.expedition.clear();npc.movement_medium="dry";npc.helmet_equipped=not gear.is_empty();npc.bunk_motion.clear()
				npc.foot=(Vector2(ORIGIN)+Vector2.ONE*.5)*384+Vector2(station.point);npc.direction=station.facing;npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0;npc.air_recovery=0
				check(npc.can_stand(npc.foot),"Actual registered furniture approach standable")
				check(npc.begin_room_activity(),"Actual room activity dispatcher enters rest")
				var foot:Vector2=npc.foot;var entry:String=npc.stage;var duration:float=LIFE.seconds(npc,entry)
				var label:String=("bare" if gear.is_empty() else "helmet")+"-"+room_id+"-"+str(rotation)
				player.current_key="";player.motion.clear();player.last_time=-1;game.visual_time_seconds=100.0
				for amount in [0.0,.5,.999]:
					npc.timer=duration*(1.0-amount);game.visual_time_seconds=100+duration*amount
					check(game.grid_view._get_branforth_frame_source(game)!=null,"Normal selected entry pose available")
					await capture(label+"-entry-"+str(amount),npc)
				npc.timer=.01;npc.update(game,.02)
				check(npc.stage==("life_sleep" if room_id=="crew_hab" else "life_seated"),"Actual update enters held rest")
				check(npc.foot==foot,"Rest retains physical furniture approach")
				game.visual_time_seconds+=.1;game.grid_view._get_branforth_frame_source(game);await capture(label+"-held",npc)
				var saved:Dictionary=npc.snapshot();npc.restore_snapshot(game,saved)
				check(npc.stage==saved.stage and npc.foot==foot and npc.helmet_equipped==not gear.is_empty(),"Actual actor snapshot preserves held rest and gear")
				game.powered_room_cells.erase(ORIGIN);npc.update(game,.01)
				var exit:String="life_get_up" if room_id=="crew_hab" else "life_rise"
				check(npc.stage==exit and npc.goal.is_empty(),"Actual service power loss starts finite exit")
				duration=LIFE.seconds(npc,exit)
				for amount in [0.0,.5,.999]:
					npc.timer=duration*(1.0-amount);game.visual_time_seconds+=.1
					check(game.grid_view._get_branforth_frame_source(game)!=null,"Normal selected exit pose available")
					await capture(label+"-exit-"+str(amount),npc)
					check(npc.foot==foot,"Interrupted exit retains physical contact")
				npc.timer=.01;npc.update(game,.02)
				check(npc.stage.is_empty() and npc.foot==foot,"Finite exit completes before new route")
				cases.append({"room":room_id,"rotation":rotation,"gear":gear,"station":station,"entry":entry,"exit":exit})
				game.powered_room_cells[ORIGIN]=true;npc.active=false
	if not FileAccess.file_exists(OUT+"native_probe.gd.uid"):FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	FileAccess.open(OUT+"native-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"scope":"Normal James actor and renderer, first actual rest station in each of four authored habitation/lounge rotations, both gears. Actual activity entry, update into held rest, actor snapshot restoration, service power loss and finite exit. Prescribed renderer samples, no autonomous goal selection/arrival, whole-run disk restore or continuous motion claim."},"\t"))
	print("JAMES NATIVE REST checks=",checks," failures=",failures," cases=",cases.size()," captures=",captures.size());game.queue_free();await process_frame;quit(0 if failures==0 else 1)
