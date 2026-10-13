extends SceneTree
const OUT="res://output/bill-meal-continue-producer-v1/"
const SAVE=preload("res://scripts/run_save.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	var game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-meal-continue.meta";game.run_save_path="user://bill-meal-continue.loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for npc in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:npc.active=false
	var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("galley",cell,true);game.powered_room_cells[cell]=true
	var actor=game.bill_npc;await actor.rebuild(game);var stations:Array=actor.RoomActivity.stations(actor.geometry[cell]);check(stations.size()==2,"Two actual galley contacts")
	var cases:=[]
	for k in stations.size():
		var station:Dictionary=stations[k]
		for kind in ["eat","drink"]:
			var duration:=6.0 if kind=="eat" else 3.0
			for sample in [["draw",.3,false],["use",.73,false],["stow",duration-.14,false],["cancel-draw",.3,true],["cancel-use",.73,true]]:
				actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.timer=0;actor.goal="hunger";actor.goal_cell=cell;actor.path.clear();actor.expedition.clear();actor.moonbay_assignment.clear();actor.helmet_equipped=false;actor.movement_medium="dry";actor.meal_return_kind="";actor.meal_return_pose=-1;actor.inspection_return_pose=-1
				actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing;actor.needs.hunger=90;actor.breath_oxygen=15;actor.tank_oxygen=60;actor.starvation=0
				game.powered_room_cells[cell]=true;check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"Normal chooser starts at actual contact")
				actor.stage="life_"+kind;actor.timer=duration-float(sample[1])
				if sample[2]:game.powered_room_cells.erase(cell);actor.update(game,.00000001)
				var id:String="contact-%d-%s-%s"%[k,kind,sample[0]];var checkpoint:String="user://bill-meal-continue-"+id+".save";var expected:String="user://bill-meal-continue-"+id+".png"
				var texture:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
				check(actor.valid_bill_snapshot(actor.snapshot()),"Producer meal state validates")
				check(SAVE.write(game,checkpoint)==OK,"Production checkpoint: "+SAVE.last_error)
				var saved:Dictionary=SAVE.read(checkpoint);check(not saved.is_empty(),"Production checkpoint readable")
				check(texture.get_image().save_png(expected)==OK,"Expected exact producer pixels")
				cases.append({"id":id,"checkpoint":checkpoint,"expectedImage":expected,"direction":actor.direction,"helmet":false,"foot":[actor.foot.x,actor.foot.y],"stage":actor.stage,"timer":actor.timer,"pose":actor.animation_state(),"returnKind":actor.meal_return_kind,"returnPose":actor.meal_return_pose,"hunger":actor.needs.hunger,"station":station})
	check(cases.size()==20,"Two contacts/two actions/five phases checkpoint matrix")
	var file:=FileAccess.open(OUT+"continue-cases.json",FileAccess.WRITE);file.store_string(JSON.stringify(cases,"\t"));file.close()
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")==OK,"Fresh producer capture")
	print("BILL MEAL CONTINUE PRODUCER: %d checks,%d failures; %d checkpoints"%[checks,failures,cases.size()]);quit(1 if failures else 0)
