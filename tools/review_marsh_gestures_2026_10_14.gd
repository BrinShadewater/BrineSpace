extends "res://tests/playtest_marsh_crew_chat.gd"
const Normal=preload("res://scripts/marsh_npc.gd")
var output:String="res://output/marsh-gestures-2026-10-14/"+("before-native/" if "--before" in OS.get_cmdline_user_args() else "after-native/")
var movie_samples:Array=[]
var marker:ColorRect
var marker_layer:CanvasLayer

func freeze():
	super.freeze()
	game.hand_panel.hide()
	if "--before" in OS.get_cmdline_user_args():game.grid_view.marsh_player.load_manifest("res://character/marsh-crew-chat-v2/manifest.json",true)

func selected_chat_file(direction:String,slot:int)->String:
	if not "--before" in OS.get_cmdline_user_args():return super.selected_chat_file(direction,slot)
	var before:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-gestures-review-2026-10-14/selected-before.json"))
	return "res://"+str(before["crew-chat-"+direction].files[slot].path).replace("\\","/")

func run():
	if not OS.get_environment("APPDATA").contains("marsh-gestures-2026-10-14"):
		push_error("Explicit scratch APPDATA required");quit(1);return
	if DisplayServer.get_name()=="headless":quit(2);return
	seed(20261014)
	DirAccess.make_dir_recursive_absolute(output)
	preload("res://scripts/title_settings.gd").reduced_motion=true
	marker_layer=CanvasLayer.new();marker_layer.layer=1000;root.add_child(marker_layer)
	marker=ColorRect.new();marker.size=Vector2(8,8);marker_layer.add_child(marker)
	await super.run()
	var f=FileAccess.open(output+"report.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":movie_samples,"scope":"Actual reciprocal four-facing conversations and four disk checkpoint restores, plus four physical-impact fall/recovery triggers. Native scene and selected renderer,30Hz advancing simulation with rendered sample marker. Conversation crops skip the three-second listening wait; not real-time capture or full-library furniture/death acceptance."},"\t"));f.close()
	print("MARSH GESTURES: ",checks," checks, ",failures," failures; ",movie_samples.size()," samples")
	marker_layer.queue_free()
	quit(1 if failures else 0)

func capture(label:String):
	if not label.ends_with("-finished"):return
	var direction:String=label.trim_suffix("-finished")
	var m=game.marsh_npc;var b=game.bill_npc
	reset(m);reset(b);m.battery=100;m.returning_to_pod=false;m.recharge_docked=false;m.injury_phase="";m.injury_pending=false
	check(positions(direction),"reachable movie partner placement "+direction)
	game.visual_time_seconds=100.0
	var player=game.grid_view.marsh_player
	player.current_key="";player.motion={};player.phase=0;player.last_time=-1;player.started=0
	Social.advance(game,.1)
	check(m.goal=="social" and b.goal=="social","movie uses reciprocal normal social chooser")
	await settle()
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	await settle()
	var canvas:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*(game.get_marsh_position()+Vector2(0,game.get_cell_size()*.038))
	var region:=Rect2i(Vector2i(canvas)-Vector2i(200,220),Vector2i(400,400))
	var foot:Vector2=m.foot
	var index:=0
	for hold in range(6):
		await sample("chat-"+direction,index,region);index+=1;game.visual_time_seconds+=1.0/30.0
	Social.advance(game,3.000001)
	check(m.animation_state()=="crew-chat","Marsh takes actual speaking turn for movie")
	var seen:Dictionary={}
	for step in range(40):
		if step>0:Social.advance(game,1.0/30.0);game.visual_time_seconds+=1.0/30.0
		await sample("chat-"+direction,index,region);index+=1
		seen[movie_samples[-1].slot]=true
		check(m.foot==foot,"conversation keeps physical foot")
	check(seen.size()==8,"all eight conversational holds observed")
	Social.advance(game,2.0)
	check(m.goal.is_empty() and b.goal.is_empty(),"movie conversation releases both partners")
	for hold in range(6):
		game.visual_time_seconds+=1.0/30.0;await sample("chat-"+direction,index,region);index+=1
	game.paused=false;m.direction=direction
	game.visual_time_seconds=200.0;player.current_key="";player.motion={};player.phase=0;player.last_time=-1;player.started=0
	check(m.receive_physical_damage(game,"animation review fixture"),"actual nonfatal impact trigger "+direction)
	m.update(game,.000001)
	seen.clear();index=0
	for step in range(100):
		await sample("injury-"+direction,index,region);index+=1
		check(m.foot==foot and not m.dead,"nonfatal reaction keeps root and android alive")
		if m.injury_phase.is_empty():break
		seen[movie_samples[-1].key+"/"+str(movie_samples[-1].slot)]=true
		var before:Dictionary=m.snapshot();game.paused=true;m.update(game,.3)
		check(m.snapshot()==before,"pause preserves injury clock")
		game.paused=false;m.update(game,1.0/30.0);game.visual_time_seconds+=1.0/30.0
	check(seen.size()==12 and m.injury_phase.is_empty(),"all fall/rise holds complete normally")
	for hold in range(6):
		game.visual_time_seconds+=1.0/30.0;await sample("injury-"+direction,index,region);index+=1

func sample(case_label:String,index:int,region:Rect2i):
	var actor=game.marsh_npc
	var texture:Texture2D=game.grid_view._get_marsh_frame(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var slot:int=game.grid_view.marsh_player.frames[key].find(texture)
	check(slot>=0,"selected source hold present")
	var marker_index:int=movie_samples.size()+1
	marker.color=Color8(marker_index%256,(marker_index/256)%256,150)
	game.grid_view.queue_redraw()
	var image:Image
	for attempt in range(20):
		await process_frame;await RenderingServer.frame_post_draw;image=root.get_texture().get_image()
		if image.get_pixel(2,2).is_equal_approx(marker.color):break
	check(image.get_pixel(2,2).is_equal_approx(marker.color),"current rendered sample observed")
	check(game.grid_view._get_marsh_frame(game)==texture,"selected source frozen during draw")
	check(Rect2i(Vector2i.ZERO,image.get_size()).encloses(region),"native crop inside viewport")
	var name:String=case_label+"-%03d.png"%index
	check(image.get_region(region).save_png(output+name)==OK,"native crop saved")
	check(texture.get_image().save_png(output+"source-"+name)==OK,"actual source saved")
	var at:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*(game.get_marsh_position()+Vector2(0,game.get_cell_size()*.038))
	check(region.encloses(Rect2i(Vector2i(at)-Vector2i(100,140),Vector2i(200,190))),"complete reaction or gesture inside crop")
	movie_samples.append({"direction":case_label,"index":index,"file":name,"durationMs":1000.0/30.0,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"canvasPosition":[at.x,at.y],"region":[region.position.x,region.position.y,400,400],"playerPhase":game.grid_view.marsh_player.phase,"actionElapsed":actor.action_elapsed(),"snapshotValid":Normal.valid_marsh_snapshot(actor.snapshot())})
