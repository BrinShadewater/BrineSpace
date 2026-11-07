extends SceneTree
## Actual owner galley geometry/rendering; source injection, fixture-facing contacts.
const OUT="res://output/veld-dry-death-station-candidate-v1/"
const Flood=preload("res://scripts/room_flooding.gd")
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://veld-ground-station.meta";game.run_save_path="user://veld-ground-station.loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for other in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:other.active=false
	var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("galley",cell,true);game.powered_room_cells[cell]=true
	var actor=game.veld_npc;await actor.rebuild(game);var geometry:Dictionary=actor.geometry[cell];var stations:Array=actor.RoomActivity.stations(geometry)
	check(not stations.is_empty(),"Actual galley service contact")
	if failures:quit(1);return
	var contacts:=[["counter",Vector2(stations[0].point)]]
	for y in range(-80,81,16):
		var local:=Vector2(0,y)
		if actor.can_stand((Vector2(cell)+Vector2.ONE*.5)*384+local):contacts.append(["aisle",local]);break
	check(contacts.size()==2,"Actual aisle floor contact")
	var grid=game.grid_view;var player=grid.veld_player
	player.load_manifest("res://character/veld-death-ground-family-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-death-ground-family-v1/helmet-manifest.json"),"Candidate pair")
	game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
	game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	var records:=[]
	for contact in contacts:
		for facing in ["east","west","north","south"]:
			for helmet in [false,true]:
				actor.active=true;actor.dead=false;actor.state="kneel";actor.stage="";actor.timer=0;actor.path.clear();actor.goal="";actor.expedition.clear();actor.moonbay_assignment.clear();actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.direction=facing;actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+contact[1];actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0;actor.water_death_motion.clear();actor.water_death_last_frame=null
				check(actor.can_stand(actor.foot),"Normal navigation anchor clear")
				var foot:Vector2=actor.foot;game.visual_time_seconds=300;player.current_key="";player.motion.clear();player.last_time=-1
				grid._get_veld_frame_source(game);game.visual_time_seconds=301;var incoming=grid._get_veld_frame_source(game)
				for phase in ["before-kneel","entry","first-interior","terminal"]:
					if phase=="entry":Flood.kill(game,actor,"veld","fixture collapse contact")
					if phase=="first-interior":game.visual_time_seconds=301.180001
					if phase=="terminal":game.visual_time_seconds=304
					var texture:Texture2D=grid._get_veld_frame_source(game)
					check(texture!=null,"Actual renderer resolves pose")
					if phase=="entry":check(texture==incoming,"Exact actual contact entry")
					if phase!="before-kneel":check(actor.dead and actor.state=="death-ground" and actor.foot==foot,"Death anchor retained")
					grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
					var name:String="%s-%s-%s-%s.png"%[contact[0],facing,"helmet" if helmet else "bare",phase]
					check(root.get_texture().get_image().save_png(OUT+name)==OK,"Native furnished-room capture")
					var extent:Rect2=texture.get_meta("crew_alpha_extent");extent.position+=Vector2(contact[1])+Vector2(0,384*.038)
					var overlaps:=[]
					for prop in geometry.get("props",[]):
						for rect in actor.Geometry.prop_collision_rects(prop):
							if extent.intersects(rect):overlaps.append(str(prop.get("id",prop.get("name","prop"))))
					var screen:Vector2=grid.get_global_transform_with_canvas()*game.get_dr_veld_position()
					records.append({"contact":contact[0],"direction":facing,"helmet":helmet,"phase":phase,"foot":foot,"screen":screen,"projectionExtent":extent,"projectionProxyOverlaps":overlaps,"screenshot":name})
				actor.active=false
	var file:=FileAccess.open(OUT+"contacts.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"actual galley owner geometry/native rendering; authored contact fixtures, projection-box overlap is a conservative visual proxy and not physical floor collision proof","records":records},"\t"));file.close()
	await RenderingServer.frame_post_draw;check(root.get_texture().get_image().save_png(OUT+"final-room.png")==OK,"Final native room")
	print("VELD DRY DEATH STATION CANDIDATE: %d checks,%d failures,%d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
