extends SceneTree
const OUT="res://output/bill-death-ground-contact-mortality-v1/"
const FLOOD=preload("res://scripts/room_flooding.gd")
const Save=preload("res://scripts/run_save.gd")
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	print("BILL GROUND STATION CANDIDATE profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-ground-station.meta";game.run_save_path="user://bill-ground-station.loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("galley",cell,true);game.powered_room_cells[cell]=true
	var actor=game.bill_npc;await actor.rebuild(game);var data:Dictionary=actor.geometry[cell];var stations:Array=actor.RoomActivity.stations(data)
	check(not stations.is_empty(),"Actual galley offers service contact");if failures:quit(2);return
	var contacts:=[["counter",Vector2(stations[0].point)]]
	for y in range(-80,81,16):
		var local:=Vector2(0,y)
		if actor.can_stand((Vector2(cell)+Vector2.ONE*.5)*384+local):contacts.append(["aisle",local]);break
	check(contacts.size()==2,"Actual geometry offers separate aisle floor point")
	var grid=game.grid_view;var player=grid.human_water_player;player.load_manifest("res://character/bill-death-ground-contact-family-v1/manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/bill-death-ground-contact-family-v1/helmet-manifest.json"),"Candidate paired gear loaded")
	grid.human_animations["death-ground"]={}
	for d in ["east","west","north","south"]:
		var key:String="death-ground-"+d;grid.human_animations["death-ground"][d]=player.frames[key];grid.human_animation_timing[key]=player.timing[key]
	grid.human_equipment_frames=player.equipment_frames
	game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
	game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	var cases:=0;var restores:=0;var captures:=0
	for contact in contacts:
		for d in ["east","west","north","south"]:
			for gear in [false,true]:
				for cause in ["air","food"]:
					for before in ["kneel","repair"]:
						actor=game.bill_npc
						actor.active=true;actor.dead=false;actor.state=before;actor.stage="";actor.timer=0;actor.path.clear();actor.goal="curiosity";actor.expedition.clear();actor.moonbay_assignment.clear();actor.helmet_equipped=gear;actor.movement_medium="dry";actor.direction=d;actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+contact[1]
						await actor.rebuild(game)
						var foot:Vector2=actor.foot
						game.resources.food=0 if cause=="food" else 100;game.resources.oxygen=0 if cause=="air" else 100
						actor.tank_oxygen=.01 if cause=="air" else 60;actor.breath_oxygen=.01 if cause=="air" else 15;actor.starvation=89.99 if cause=="food" else 0
						var expected:String="lateral" if contact[0]=="counter" and d in ["north","south"] else ""
						var key:String="death-ground-"+("lateral-" if expected=="lateral" else "")+d
						var equipment:String="diving-helmet" if gear else ""
						grid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=100
						grid._get_human_frame_source(before,d);game.visual_time_seconds=101;grid._get_human_frame_source(before,d)
						FLOOD.step_crew(game,actor,"bill",.02);cases+=1
						check(actor.dead and actor.state=="death-ground","Actual survival-trigger dry death")
						check(actor.death_ground_variant==expected,"Actual contact choice: "+contact[0]+d+str(gear)+cause+before)
						check(actor.foot==foot and actor.path.is_empty() and actor.goal.is_empty(),"Mortality preserves anchor and cancels intent")
						check(grid._get_human_frame_source("death-ground",d)==player.frame_at_elapsed(key,actor.death_entry_seconds,equipment),"Chosen lowered entry rendered")
						game.visual_time_seconds=104
						var terminal:Texture2D=player.frame_at_elapsed(key,99,equipment)
						check(grid._get_human_frame_source("death-ground",d)==terminal,"Chosen terminal rendered")
						check(grid._get_human_frame_source("death-ground",d)==terminal,"Paused terminal stable")
						if cause=="food" and before=="repair":
							for elapsed in [.65,2.0]:
								grid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=200
								grid._get_human_frame_source("death-ground",d);game.visual_time_seconds=200+elapsed
								var pixels:PackedByteArray=grid._get_human_frame_source("death-ground",d).get_image().get_data();var phase:float=actor.death_entry_seconds
								check(Save.write(game,game.run_save_path)==OK,"Write actual death checkpoint: "+Save.last_error)
								var saved:Dictionary=Save.read(game.run_save_path);check(not saved.is_empty(),"Read actual checkpoint")
								if not saved.is_empty():
									check(await Save.restore(game,saved),"Production disk restoration")
									actor=game.bill_npc
									game.set_process(false);game.tick_timer.stop();game.run_save_path="user://bill-ground-station.loop"
									check(actor.dead and actor.death_ground_variant==expected and is_equal_approx(actor.death_entry_seconds,phase),"Saved variant and prefix restored")
									check(actor.direction==d and actor.helmet_equipped==gear and actor.foot==foot,"Dead identity and contact restored")
									check(grid._get_human_frame_source("death-ground",d).get_image().get_data()==pixels,"Exact chosen mid-fall/terminal pixels restored")
									restores+=1
							grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
							check(root.get_texture().get_image().save_png(OUT+"%s-%s-%s-terminal.png"%[contact[0],d,"helmet" if gear else "bare"])==OK,"Actual restored terminal room capture");captures+=1
						actor.active=false
	check(cases==64 and restores==32 and captures==16,"Full64 mortality/32 disk-restore/16 capture matrix")
	await RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")==OK,"Fresh native proof")
	print("BILL GROUND CONTACT MORTALITY: %d checks,%d failures; %d cases,%d restores,%d captures"%[checks,failures,cases,restores,captures]);quit(1 if failures else 0)
