extends SceneTree
const Save=preload("res://scripts/run_save.gd")
const Flood=preload("res://scripts/room_flooding.gd")
const CORE=Vector2i(20,20)
var checks:=0
var failures:=0
var restores:=0
func check(ok:bool,why:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init()->void:call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://water-death-continue.meta";game.run_save_path="user://water-death-continue.loop";game.Preferences.save_path="user://water-death-continue.cfg"
	game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="veld"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	return game
func run()->void:
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	for facing in ["east","west","north","south"]:
		for helmet in [false,true]:
			var game=await fresh()
			game.paused=false;game.Architects.advance_core(game,10);game.paused=true
			# Recover the site's existing Bill pod as the survivor. Preserve the
			# architect roster and all-characters-lost/resource failure rules.
			var ward:=Vector2i(-1,-1)
			var site:Dictionary={}
			for cell in game.wrecks:
				for pod in game.wrecks[cell].get("pods",[]):
					if pod.get("architect_id","")=="bill":ward=cell;site=game.wrecks[cell].duplicate(true);break
				if not site.is_empty():break
			check(not site.is_empty(),"Existing Bill pod found")
			if site.is_empty():game.queue_free();await process_frame;quit(1);return
			game.wrecks.erase(ward);game._place_room("cryo_chamber",ward,true)
			game.occupied[ward].rotation=site.rotation;game.occupied[ward].recovered_derelict=true
			site.progress=preload("res://scripts/wreck_field.gd").DURATION;site.active=false;site.cleared=true;site.paid=true;game.wrecks[ward]=site
			for pod in site.pods:
				if pod.get("architect_id","")!="bill":continue
				check(game.Architects.release(game,pod,ward),"Survivor released through actual cryopod navigation")
				pod.wake=7.0;pod.recovered=true
				game.recovered_crew.append({"id":pod.id,"name":pod.name,"architect_id":"bill","origin":ward,"alive":true});game.crew_count+=1
			check(Save.problem(Save.capture(game)).is_empty(),"Whole checkpoint fixture valid before death: "+Save.problem(Save.capture(game)))
			if failures:game.queue_free();await process_frame;quit(1);return
			var actor=game.veld_npc
			await actor.rebuild(game)
			check(actor.active and game.Architects.present(game,"veld"),"Normal recovered Veld")
			actor.state="idle";actor.direction=facing;actor.helmet_equipped=helmet;actor.stage="";actor.goal="";actor.path.clear();actor.movement_medium="flooded";actor.air_was_low=false;actor.breath_oxygen=15;actor.tank_oxygen=60;actor.water_death_last_frame=null
			game.occupied[CORE].water_level=1;game.resources.oxygen=100;game.resources.food=100
			var point:=Vector2.INF
			for y in range(48,337,24):
				for x in range(48,337,24):
					actor.foot=Vector2(CORE)*384+Vector2(x,y)
					if actor.action_pose_clear("transition") and actor.swim_segment_clear(actor.foot,actor.foot,facing,facing,true):point=actor.foot;break
				if point.is_finite():break
			check(point.is_finite(),"Existing furnished core has clear entrance")
			if not point.is_finite():game.queue_free();await process_frame;continue
			actor.foot=point
			game.visual_time_seconds=11.25
			var incoming=game.grid_view._get_veld_frame_source(game)
			actor.breath_oxygen=.01;actor.tank_oxygen=.01
			Flood.step_crew(game,actor,"veld",.02)
			check(actor.dead and actor.state=="death-water","Actual oxygen death before disk save")
			check(game.running,"Surviving recovered character keeps loop active")
			if not game.running:game.queue_free();await process_frame;quit(1);return
			var motion:Dictionary=actor.water_death_motion.duplicate(true)
			var death_at:float=game.visual_time_seconds
			var terminal_pixels:=PackedByteArray()
			for elapsed in [.10,.60,3.0]:
				game.visual_time_seconds=death_at+elapsed
				var shown=game.grid_view._get_veld_frame_source(game)
				var pixels:PackedByteArray=shown.get_image().get_data()
				terminal_pixels=pixels
				var foot:Vector2=actor.foot
				check(game.running and not game.testing_free_build and not game.testing_disable_failures,"Normal checkpoint eligibility")
				var written:int=Save.write(game,game.run_save_path)
				check(written==OK,"Disk checkpoint writes: "+Save.last_error)
				if written!=OK:continue # Never mistake an older checkpoint for this phase.
				var disk:Dictionary=Save.read(game.run_save_path)
				check(not disk.is_empty(),"Disk checkpoint reads: "+Save.last_error)
				if disk.is_empty():continue
				game.queue_free();await process_frame
				game=await fresh()
				check(await Save.restore_staged(game,disk),"Fresh-scene staged Continue: "+Save.last_error)
				game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.run_save_path="user://water-death-continue.loop"
				actor=game.veld_npc;restores+=1
				check(actor.dead and actor.state=="death-water" and actor.foot==foot,"Continue preserves corpse and world anchor")
				check(actor.water_death_motion==motion,"Continue preserves source selectors and death clock")
				var restored=game.grid_view._get_veld_frame_source(game)
				check(restored!=null and restored.get_image().get_data()==pixels,"Fresh loader retains exact incoming/interior/terminal pixels")
				check(is_equal_approx(game.visual_time_seconds,death_at+elapsed),"Continue preserves visual clock")
				game._process(.5)
				check(game.paused and game.grid_view._get_veld_frame_source(game).get_image().get_data()==pixels,"Paused Continue freezes death pose")
				if elapsed==.10:check(pixels==incoming.get_image().get_data(),"Saved entrance remains actual last drawn frame")
			game.occupied[CORE].water_level=0;game.paused=false
			check(game.running,"Draining exercises active flooding step")
			Flood.advance(game,.02);game.paused=true
			check(actor.movement_medium=="flooded" and actor.dead,"Normal draining skips dead actor medium mutation")
			check(game.grid_view._get_veld_frame_source(game).get_image().get_data()==terminal_pixels,"Restored terminal corpse persists after draining")
			print("CONTINUE GROUP ",facing," helmet=",helmet," restores=",restores," failures=",failures)
			game.queue_free();await process_frame
	print("VELD WATER DEATH CONTINUE: %d checks,%d failures,%d fresh-scene disk restores"%[checks,failures,restores])
	quit(1 if failures else 0)
