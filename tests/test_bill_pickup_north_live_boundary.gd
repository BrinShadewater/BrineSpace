extends SceneTree
const Expedition=preload("res://scripts/crew_expedition.gd")
var checks:=0
var failures:=0
var report:=[]
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch user profile")
	if failures:quit(1);return
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://boundary.meta";game.run_save_path="user://boundary.loop"
	root.add_child(game);current_scene=game;game.set_process(false);game.tick_timer.stop()
	var grid=game.grid_view;var player=grid.human_water_player
	player.load_manifest("res://character/bill-salvage-north-coherent-v1/manifest.json",true)
	player.load_manifest("res://character/bill-swim-pickup-north-coherent-v1/manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/bill-salvage-helmet-north-coherent-v1/manifest.json"),"Working helmet injection")
	check(player.load_equipment_manifest("diving-helmet","res://character/bill-swim-pickup-helmet-north-coherent-v1/manifest.json"),"Pickup helmet injection")
	var home:=Vector2i(20,19);var target:=Vector2i(20,16)
	game.wrecks.erase(home);game._place_room("airlock",home,true)
	game.occupied[home].rotation=0;game.powered_room_cells[home]=true;game.running=true;game.hardware.power=true
	var actor=game.bill_npc
	var viewport:=SubViewport.new();viewport.size=Vector2i(420,180);viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
	var bg:=ColorRect.new();bg.size=Vector2(420,180);bg.color=Color("22343e");viewport.add_child(bg)
	var title:=Label.new();title.position=Vector2(8,8);viewport.add_child(title)
	var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;viewport.add_child(sprite)
	for gear in [false,true]:
		for recall in [false,true]:
			var name:String=("helmet" if gear else "bare")+("-recall" if recall else "-nominal")
			var folder:String="res://output/bill-pickup-north-live-boundary-v1/"+name
			DirAccess.make_dir_recursive_absolute(folder)
			game.drone_fleet.sites={target:game.drone_fleet.Sites.make_site("salvage",3)}
			actor.active=true;actor.dead=false;actor.stage="";actor.state="idle";actor.direction="north";actor.helmet_equipped=gear;actor.movement_medium="exterior";actor.breath_oxygen=100;actor.tank_oxygen=100
			actor.foot=Vector2(8064,6336);actor.expedition={"kind":"salvage","phase":"salvage","home":home,"target":target,"elapsed":0.0,"cargo":{},"recall":false,"route":PackedVector2Array(),"sea_route":PackedVector2Array([actor.foot+Vector2(0,384),actor.foot])}
			player.current_key="";player.current_equipment="";player.motion.clear();player.last_time=-1;player.phase=0;game.visual_time_seconds=0
			var samples:=[];var photographed:=0;var first_return:Dictionary={};var pickup_seen:=false
			for tick in range(480):
				var before:String=actor.expedition.phase
				if recall and tick==73:actor.expedition.recall=true
				if tick>0:Expedition.advance(game,actor,1.0/60.0)
				game.visual_time_seconds=float(tick)/60.0
				var state:String=actor.animation_state();var texture:Texture2D=grid._get_human_frame_source(state,actor.direction)
				check(texture!=null,"Actual renderer source "+name+str(tick))
				var phase:String=actor.expedition.phase
				if phase=="pickup":pickup_seen=true;check(actor.expedition.cargo.is_empty() and game.drone_fleet.sites[target].units==3,"No early extraction")
				if phase=="return" and first_return.is_empty():
					first_return={"tick":tick,"direction":actor.direction,"state":state,"motion":player.motion.duplicate(true),"currentKey":player.current_key}
					check(state==("swim" if recall else "swim-carry"),"Return boundary stays prone")
				if not first_return.is_empty() and tick==int(first_return.tick)+1:
					check(actor.direction=="south","Return route changes facing")
					check(player.motion.get("clip","")==("swim-turn-north-south" if recall else "swim-carry-turn-north-south"),"Actual return uses selected half-turn")
				var capture:bool=(recall and tick>=68) or (not recall and tick>=319)
				if capture:
					sprite.texture=texture;var factor:=82.0/148.0;sprite.scale=Vector2.ONE*factor;sprite.position=Vector2(210,100)-texture.get_meta("crew_pivot")*factor
					title.text=name+" / "+phase+" / "+actor.direction+" / "+str(tick)
					await RenderingServer.frame_post_draw
					check(viewport.get_texture().get_image().save_png(folder.path_join("%03d.png"%photographed))==OK,"Native moving sample")
					photographed+=1;samples.append({"tick":tick,"phase":phase,"elapsed":actor.expedition.elapsed,"state":state,"direction":actor.direction,"motion":player.motion.duplicate(true)})
				if not first_return.is_empty() and tick>=int(first_return.tick)+80:
					check(player.motion.get("clip","")=="","Return half-turn finishes")
					break
			check(pickup_seen,"Actual controller enters pickup")
			check(not first_return.is_empty(),"Actual controller returns")
			check(samples.back().tick>=int(first_return.tick)+80,"Full return half-turn sampled")
			check(game.drone_fleet.sites[target].units==(3 if recall else 2),"Retained extraction rule")
			check(actor.expedition.cargo.is_empty()==recall,"Recall preserves empty cargo")
			report.append({"name":name,"samples":samples,"firstReturn":first_return,"captures":photographed})
	var file=FileAccess.open("res://output/bill-pickup-north-live-boundary-v1/timeline.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"\t"));file.close()
	viewport.queue_free();game.queue_free();print("BILL LIVE BOUNDARY: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
