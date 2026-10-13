"""Four normal work-to-delivery sequences; retain automatically chosen routes."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_cargo_side_action02_actor.gd').read_text().split('\tvar cases:Array=[]')[0]
s=s.replace('cargo-side-action-02-2026-10-02','cargo-delivery-01-2026-10-02')
s=s.replace('\tplayer.load_manifest("res://character/marsh-cargo-held-material-v1/east-unload-02-unselected/manifest.json",true)\n\tplayer.load_manifest("res://character/marsh-cargo-held-material-v1/west-unload-02-unselected/manifest.json",true)','\tplayer.load_manifest("res://character/marsh-carry-turn-material-v1/opposite-01-unselected/family-manifest.json",true)\n\tplayer.load_manifest("res://character/marsh-cargo-held-material-v1/side02-cross-review/family-manifest.json",true)')
tail='''
	var cases:Array=[]
	for origin in ["east","west","south","north"]:
		actor=Normal.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction=origin;actor.state="idle";actor.goal="curiosity";actor.goal_cell=cell
		actor.path=PackedVector2Array();actor.stage="workshop_work";actor.timer=.02;actor.activity="sorting recovered components"
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		game.paused=false;game.visual_time_seconds=100.0;player.current_key="";player.motion={}
		actor.update(game,.02)
		check(actor.stage=="workshop_pickup" and is_equal_approx(actor.timer,.52),"normal work enters pickup")
		var seen:Dictionary={};var pickup_seen:Dictionary={};var unload_seen:Dictionary={};var stages:Array=[];var joins:Array=[]
		var restores:=0;var first_capture:int=captures.size();var first_sample:int=samples.size();var carried:=false;var unloaded:=false;var completed:=false
		var previous_stage:String=actor.stage;var previous_key:="";var previous_slot:=-1;var previous_texture:Texture2D=null
		for step in range(1600):
			if unloaded and actor.stage!="workshop_unload":completed=true;break
			if stages.is_empty() or stages.back()!=actor.stage:stages.append(actor.stage)
			if actor.stage=="workshop_carry":carried=true
			if actor.stage=="workshop_unload":
				if not unloaded:check(carried and actor.direction=="north" and actor.path.is_empty() and is_equal_approx(actor.timer,2),"automatic carry arrival enters North unload")
				unloaded=true
			var texture:Texture2D=game.grid_view._get_marsh_frame(game)
			var key:String=actor.animation_state()+"-"+actor.direction if actor.action_elapsed()>=0 else str(player.motion.get("clip",""))
			if key.is_empty():key="carry-"+actor.direction
			check(player.frames.has(key),"actual complete-route source key loaded")
			if not player.frames.has(key):break
			var slot:int=player.frames[key].find(texture)
			check(slot>=0,"actual complete-route source is in declared clip")
			if slot<0:break
			if actor.stage=="workshop_pickup":pickup_seen[slot]=true
			if actor.stage=="workshop_unload":
				unload_seen[slot]=true
				if actor.action_elapsed()>=.52:check(slot==3,"actual delivery holds authored final North idle")
			if actor.stage!=previous_stage:
				joins.append({"fromStage":previous_stage,"toStage":actor.stage,"fromKey":previous_key,"fromSlot":previous_slot,"toKey":key,"toSlot":slot,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction})
				if actor.stage=="workshop_carry":check(pickup_seen.size()==4 and not actor.path.is_empty(),"all pickup phases create real automatic carry route")
				if actor.stage=="workshop_unload":check(key=="unload-north" and slot==0,"actual arrival uses exact North unload0")
			var signature:String=key+":"+str(slot)
			if not seen.has(signature):
				seen[signature]=true;await capture(origin+" complete delivery "+signature,slot);captures.back()["expectedKey"]=key;captures.back()["case"]=origin
				var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
				check(Normal.valid_marsh_snapshot(saved),"complete-route actor snapshot valid")
				var restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"complete-route phase root/source restored exactly")
				game.paused=true;restored.update(game,.5)
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"complete-route restored pause holds")
				game.paused=false;actor=restored;restores+=1
			samples.append({"case":origin,"step":step,"stage":actor.stage,"key":key,"slot":slot,"elapsed":actor.action_elapsed(),"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"remainingRoute":actor.path.size()})
			previous_stage=actor.stage;previous_key=key;previous_slot=slot;previous_texture=texture
			actor.update(game,.02);game.visual_time_seconds+=.02
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		check(completed and carried and unloaded and pickup_seen.size()==4 and unload_seen.size()==4,"complete normal pickup/carry/arrival/unload lifecycle finishes")
		check(stages==["workshop_pickup","workshop_carry","workshop_unload"],"exact normal lifecycle stage order")
		cases.append({"origin":origin,"stages":stages,"pickupSlots":pickup_seen.keys(),"unloadSlots":unload_seen.keys(),"completed":completed,"actorRestores":restores,"captureStart":first_capture,"captureCount":captures.size()-first_capture,"sampleStart":first_sample,"samples":samples.size()-first_sample,"joins":joins,"exitStage":actor.stage,"exitPose":actor.animation_state(),"exitElapsed":actor.action_elapsed()})
		print("DELIVERY DONE "+origin+" samples="+str(samples.size()-first_sample)+" views="+str(captures.size()-first_capture))
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"samples":samples,"scope":"Four initial facing normal Marsh.update work->pickup->automatically planned carry route/turns->actual North arrival->unload/hold/exit. Staged cardinal/turn/heldfamily02,normal main/grid/player,actor-player restores/pause. No route/facing override after work begins. Furnished free fixture,normalflagsfalse. NOT expedition/fullRunSave/visibleTitleContinue/continuouscontact/normaladmission/fullsetacceptance."},"\\t"));file.close()
	print("MARSH COMPLETE DELIVERY: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures]);quit(1 if failures else 0)
'''
(ROOT/'tools/review_marsh_cargo_delivery01_actor.gd').write_text(s+tail)
(ROOT/'tools/review_marsh_cargo_delivery01_actor.gd.uid').write_text('uid://dr5cargodel1v09\n')
print('four facing normal complete delivery fixture prepared')
