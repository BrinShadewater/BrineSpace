extends SceneTree
const OUT="res://output/bill-death-ground-contact-station-v1/"
const FLOOD=preload("res://scripts/room_flooding.gd")
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
	var records:=[]
	for contact in contacts:
		for d in ["east","west","north","south"]:
			for gear in [false,true]:
				actor.active=true;actor.dead=false;actor.state="kneel";actor.stage="";actor.timer=0;actor.path.clear();actor.goal="";actor.expedition.clear();actor.moonbay_assignment.clear();actor.helmet_equipped=gear;actor.movement_medium="dry";actor.direction=d;actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+contact[1];actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
				check(actor.can_stand(actor.foot),"Standing anchor clear in actual geometry")
				var foot:Vector2=actor.foot;game.visual_time_seconds=300;grid.human_animation_key="";grid.human_animation_last_time=-1
				# Show the last kneeling pose before interruption: art join evidence,
				# not a claim that this is a galley activity chosen by the controller.
				grid._get_human_frame_source("kneel",d);game.visual_time_seconds=301
				var prior_crown:float=grid._get_human_frame_source("kneel",d).get_meta("crew_alpha_extent").position.y
				for phase in ["before-kneel","entry","terminal"]:
					if phase=="entry":
						FLOOD.kill(game,actor,"bill","fixture collapse contact");grid.human_animation_key="";grid.human_animation_last_time=-1
						var expected:String="lateral" if contact[0]=="counter" and d in ["north","south"] else ""
						check(actor.death_ground_variant==expected,"Contact-aware corpse variant: "+contact[0]+d+str(gear))
					if phase=="terminal":game.visual_time_seconds=303
					var texture:Texture2D=grid._get_human_frame_source(actor.animation_state(),d)
					if phase=="entry":
						check(is_equal_approx(actor.death_entry_seconds,.55) if d in ["north","south"] else texture.get_meta("crew_alpha_extent").position.y>=prior_crown-.5,"Authored axial kneel or side entry without lift")
						check(actor.death_entry_seconds>0,"Lowered phase retained")
					if phase!="before-kneel":check(actor.dead and actor.state=="death-ground" and actor.foot==foot,"Actual kill holds anchor")
					grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
					var name:String="%s-%s-%s-%s.png"%[contact[0],d,"helmet" if gear else "bare",phase]
					check(root.get_texture().get_image().save_png(OUT+name)==OK,"Native room collapse capture")
					var extent:Rect2=texture.get_meta("crew_alpha_extent");records.append({"contact":contact[0],"direction":d,"gear":gear,"phase":phase,"foot":foot,"local":contact[1],"extent":extent,"variant":actor.death_ground_variant,"screenshot":name})
				actor.active=false
	var file:=FileAccess.open(OUT+"contacts.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"actual galley geometry and native rendering; fixture-facing/kn eel interruption audit, clearance/joins require visual judgement","records":records},"\t"));file.close()
	await RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")==OK,"Fresh final native contact view")
	print("BILL GROUND STATION CANDIDATE: %d checks,%d failures; %d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
