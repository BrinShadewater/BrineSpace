extends SceneTree
class BaselineJames extends "res://scripts/branforth_npc.gd":
	func station_arrival_facing(_station: Dictionary)->String:return ""
const OUT := "res://character/james-console-water-exit-turn-v1/"
var checks:=0
var failures:=0
var game
var results:Array=[]
var samples:Array=[]
var extent_cache:Dictionary={}
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func selected_extent(player,key:String,gear:String)->Array:
	var cache_key:=gear+"/"+key
	if extent_cache.has(cache_key):return extent_cache[cache_key]
	var row:Array=player.frames.get(key,[]) if gear.is_empty() else player.equipment_frames.get(gear,{}).get(key,[])
	var bounds:=Rect2();var first:=true
	for texture in row:
		var image:Image=texture.get_image();var used:Rect2=Rect2(image.get_used_rect());var factor:float=65.28/float(texture.get_meta("crew_standing_height"));var pivot:Vector2=texture.get_meta("crew_pivot")
		var rect:=Rect2((used.position-pivot)*factor,used.size*factor)
		bounds=rect if first else bounds.merge(rect);first=false
	extent_cache[cache_key]=[] if first else [bounds.position.x,bounds.position.y,bounds.end.x,bounds.end.y]
	return extent_cache[cache_key]
func _init()->void:call_deferred("run")
func capture(label: String,npc) -> String:
	var center: Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var file: String=OUT+"arrival-captures/"+label+".png"
	check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
	check(crop.save_png(file)==OK,"Save route capture")
	if label.ends_with("-000"):
		var texture: Texture2D=game.grid_view._get_branforth_frame(game)
		var used: Rect2i=texture.get_image().get_used_rect();var sc: float=cell_size*.17/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot")
		var actor_world:=Rect2(center+(Vector2(used.position)-pivot)*sc,Vector2(used.size)*sc).grow(3)
		var actor_screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*actor_world
		var roi:=Rect2i(actor_screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size())))
		var before: PackedByteArray=screenshot.get_region(roi).get_data()
		npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var after: PackedByteArray=root.get_texture().get_image().get_region(roi).get_data();var differences:=0
		for i in range(mini(before.size(),after.size())):
			if absi(int(before[i])-int(after[i]))>=5:differences+=1
		check(differences>25,"Actor on/off render difference "+label)
		npc.active=true;game.grid_view.queue_redraw();await process_frame
	return file
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-workstation-routes.meta";game.run_save_path="user://james-workstation-routes.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var selected_actor=game.branforth_npc;var baseline_actor=BaselineJames.new();var baseline_profile:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/chief-engineer-branforth-v2/clearance.json"));baseline_actor.swim_clearance=baseline_profile.swim.duplicate(true);baseline_actor.tread_clearance=baseline_profile.tread.duplicate(true);baseline_actor.action_clearance=baseline_profile.actions.duplicate(true);var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])
	for id in ["life_support","pressure_control","listening_post"]:
		for q in range(4):
			game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear();game.selected_rotation=q;game._place_room(id,cell,true);game.occupied[cell].rotation=q;game.occupied[cell].water_level=0.0;game.powered_room_cells[cell]=true
			for variant in ["baseline","installed"]:
				var npc=baseline_actor if variant=="baseline" else selected_actor;game.branforth_npc=npc;npc.rebuild(game)
				for mode in ["bare","helmet"]:
					var gear:String="" if mode=="bare" else "diving-helmet"
					for incoming in ["east","south","west","north"]:
						npc.active=true;npc.dead=false;npc.movement_medium="dry";npc.helmet_equipped=mode=="helmet";npc.primary_room=Vector2i(-1,-1);npc.expedition.clear();npc.path.clear();npc.stage="";npc.state="idle";npc.goal="";npc.direction=incoming;npc.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":100.0};npc.visits.clear();npc.decision_rng.seed=1234
						var offset:Vector2={"east":Vector2(-64,0),"south":Vector2(0,-64),"west":Vector2(64,0),"north":Vector2(0,64)}[incoming]
						var nearest:Vector2=Vector2.INF;var distance:float=INF
						for node in npc.room_nodes.get(cell,[]):
							var at:Vector2=npc.graph.get_point_position(node)
							if not npc.spawn_clear(at):continue
							if at.distance_squared_to(center+offset)<distance:nearest=at;distance=at.distance_squared_to(center+offset)
						check(nearest.is_finite(),"Available actual start node")
						if not nearest.is_finite():continue
						npc.foot=nearest;npc.choose_goal(game)
						var planned:PackedVector2Array=npc.path.duplicate();var station:Dictionary={} if planned.is_empty() else npc.RoomActivity.at(npc.geometry[cell],planned[-1]-center)
						var service:bool=not station.is_empty();var desired:String=str(station.get("facing",""));var heading:String=incoming;var previous:Vector2=nearest
						for at in planned:heading=npc.travel_heading(previous,at,heading);previous=at
						if variant=="installed" and service:check(heading==desired,"Planned final heading matches actual workstation "+id+str(q)+mode+incoming)
						var player=game.grid_view.branforth_player;player.motion.clear();player.current_key="";player.current_equipment=gear;player.last_time=-1;player.phase=0;game.visual_time_seconds=100
						var ticks:=0;var before:Texture2D=null;var seen:Dictionary={}
						while not npc.path.is_empty() and ticks<1500:
							var old_foot:Vector2=npc.foot;var old_heading:String=npc.direction
							npc.move(.04);game.visual_time_seconds+=.04
							if variant=="installed":check(npc.travel_segment_clear(old_foot,npc.foot,old_heading),"Traversed clearance "+variant+" "+id+str(q)+mode+incoming+" "+str(old_foot-center)+"->"+str(npc.foot-center)+" "+old_heading+"->"+npc.direction)
							var tex:Texture2D=game.grid_view._get_branforth_frame(game);check(tex!=null,"Normal grid route pose")
							seen[player.motion.get("clip","") if not str(player.motion.get("clip","")).is_empty() else player.current_key]=true
							if not npc.path.is_empty():before=tex
							ticks+=1
						check(npc.path.is_empty(),"Actual route finishes")
						var after:Texture2D=game.grid_view._get_branforth_frame(game)
						var arrival_clip:String=player.motion.get("clip","");var stop_frames:Array=[]
						var stop_extent:Array=selected_extent(player,"swim-stop-"+npc.direction,gear)
						var specific_stop:bool=not stop_extent.is_empty() and npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,false,stop_extent)
						var generic_stop:bool=npc.action_pose_clear("transition")
						var snap:bool=service and heading!=npc.direction
						if variant=="installed" and service:check(not snap,"Actual move/arrival preserves final heading")
						if variant=="installed" and service and npc.animation_state()=="tread":
							var stop_key:String="swim-stop-"+npc.direction
							check(arrival_clip==stop_key,"Actual route arrival begins selected straight stop")
							var metadata_extent:Array=player.clip_extent(stop_key,gear)
							for axis in range(4):check(absf(float(metadata_extent[axis])-float(stop_extent[axis]))<.001,"Loaded alpha bounds equal independently inspected selected pixels")
							var stop_start:float=game.visual_time_seconds;var elapsed:=.001
							for slot in range(player.timing[stop_key].durations.size()):
								game.visual_time_seconds=stop_start+elapsed
								var shown:Texture2D=game.grid_view._get_branforth_frame(game)
								var expected:Texture2D=player.frame_at_elapsed(stop_key,elapsed,gear)
								check(player.motion.get("clip","")==stop_key,"Stop remains active throughout authored slots")
								check(shown.get_image().get_data()==expected.get_image().get_data(),"Normal grid shows authored stop slot")
								check(game.grid_view._water_transition_clear(npc),"Complete selected stop silhouette fits equipment")
								var frozen:Texture2D=game.grid_view._get_branforth_frame(game);check(shown.get_image().get_data()==frozen.get_image().get_data(),"Paused stop holds exact pixels")
								if q==1 and incoming=="east":await capture(id+"-"+mode+"-"+str(slot).pad_zeros(3),npc)
								stop_frames.append(shown);elapsed+=float(player.timing[stop_key].durations[slot])/1000
							game.visual_time_seconds=stop_start+player.cycle_seconds(stop_key,gear)+.001
							var terminal:Texture2D=game.grid_view._get_branforth_frame(game)
							check(player.motion.get("clip","")=="" and npc.animation_state()=="tread","Finite stop finishes into treading")
							stop_frames.append(terminal)

						results.append({"room":id,"rotation":q,"variant":variant,"mode":mode,"incoming":incoming,"service":service,"goal":npc.goal,"desired":desired,"plannedHeading":heading,"arrivedHeading":npc.direction,"facingSnap":snap,"ticks":ticks,"routePoints":planned.size(),"selectedClips":seen.keys(),"endPoint":str(npc.foot-center),"arrivalClip":arrival_clip,"stopSlots":stop_frames.size()-1 if not stop_frames.is_empty() else 0,"finalClip":player.motion.get("clip",""),"finalPose":npc.animation_state(),"genericStopAllowed":generic_stop,"selectedStopAllowed":specific_stop,"selectedStopExtent":stop_extent})
						if q==1 and incoming=="east" and before!=null and after!=null:samples.append({"label":variant+" "+mode+" "+id+" "+heading+"->"+npc.direction,"before":before,"after":after,"stopFrames":stop_frames})
	for baseline in results:
		if baseline.variant!="baseline" or not baseline.service:continue
		var matched:=false
		for installed in results:
			if installed.variant=="installed" and installed.room==baseline.room and installed.rotation==baseline.rotation and installed.mode==baseline.mode and installed.incoming==baseline.incoming:
				matched=true;check(installed.service,"Previously reachable station remains reachable")
		check(matched,"Baseline case has installed counterpart")
	game.branforth_npc=selected_actor
	if DisplayServer.get_name()!="headless":
		var vp:=SubViewport.new();vp.size=Vector2i(1500,maxi(1,samples.size())*135);vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);var bg:=ColorRect.new();bg.size=Vector2(vp.size);bg.color=Color("303b40");vp.add_child(bg)
		for i in range(samples.size()):
			var title:=Label.new();title.text=samples[i].label;title.position=Vector2(8,i*135);vp.add_child(title)
			var textures:Array=[samples[i].before,samples[i].after];textures.append_array(samples[i].stopFrames)
			for column in range(textures.size()):
				var tex:Texture2D=textures[column];var sprite:=Sprite2D.new();sprite.texture=tex;sprite.centered=false;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;sprite.scale=Vector2.ONE*82.0/148.0;sprite.position=Vector2(80+column*165,i*135+85)-tex.get_meta("crew_pivot")*82.0/148.0;vp.add_child(sprite)
		await RenderingServer.frame_post_draw;check(vp.get_texture().get_image().save_png(OUT+"native-dry-equipment-contact.png")==OK,"Save route arrival pairs")
	var file:=FileAccess.open(OUT+"dry-equipment-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Baseline subclass disables new heading hook vs normal James;3rooms x4rotations x2gear x4seeded starts;actual choose_goal,route search,smoothing,move,arrive and normal grid playback;not exterior/traffic or full visual continuity acceptance."},"  "));file.close()
	print("JAMES DRY EQUIPMENT: ",checks," checks; ",failures," failures; ",results.size()," actual goal/movement cases")
	quit(1 if failures else 0)
