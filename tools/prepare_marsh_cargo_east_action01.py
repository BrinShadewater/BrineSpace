"""Build normal timed-action fixture; East unload is a seeded valid action, not arrival."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/review_marsh_carry_all_paths02_actor.gd').read_text()
prefix=source.split('\tvar axes=')[0]
prefix=prefix.replace('carry-all-paths-02-2026-10-02','cargo-east-action-01-2026-10-02')
prefix=prefix.replace('opposite-01-unselected/family-manifest.json','opposite-01-unselected/family-manifest.json')
prefix=prefix.replace('\tplayer.load_manifest(MANIFEST,true)','\tplayer.load_manifest("res://character/marsh-cargo-held-material-v1/east-unload-01-unselected/manifest.json",true)')
tail='''
	var cases:Array=[]
	for action in ["pickup","unload"]:
		actor=Normal.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction="east";actor.state="idle";actor.goal="curiosity";actor.goal_cell=cell
		actor.path=PackedVector2Array();actor.stage="workshop_work" if action=="pickup" else "workshop_unload"
		actor.timer=.02 if action=="pickup" else 2.0;actor.activity="sorting recovered components" if action=="pickup" else "stowing recovered parts"
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		game.paused=false;game.visual_time_seconds=100.0;player.current_key="";player.motion={}
		if action=="pickup":
			actor.update(game,.02)
			check(actor.stage=="workshop_pickup" and is_equal_approx(actor.timer,.52),"normal work-to-pickup transition")
		var key:String=action+"-east";var wanted:String="workshop_"+action
		check(is_equal_approx(player.cycle_seconds(key),.52) and player.frames[key].size()==4,"selected four-frame520ms staged action")
		var seen:Dictionary={};var restores:=0;var first_capture:int=captures.size();var first_sample:int=samples.size();var exited:=false
		for step in range(115):
			var elapsed:float=actor.action_elapsed()
			if actor.stage!=wanted:exited=true;break
			check(actor.animation_state()==action and elapsed>=0,"normal timed action state/elapsed")
			var texture:Texture2D=game.grid_view._get_marsh_frame(game);var slot:int=player.frames[key].find(texture)
			check(slot>=0 and slot<4,"actual renderer selects staged action source")
			var expected:int=mini(3,int(floor((elapsed+.000001)/.13)))
			check(slot==expected,"actual selected130ms phase boundary")
			if not seen.has(slot):
				check(slot==seen.size(),"four action phases ordered")
				seen[slot]=true;await capture(key+" normal timer phase%d"%slot,slot);captures.back()["expectedKey"]=key
				var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
				check(Normal.valid_marsh_snapshot(saved),"timed action snapshot valid")
				var restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"action actor/player restored exactly")
				game.paused=true;restored.update(game,.5)
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"paused action root/source held")
				game.paused=false;actor=restored;restores+=1
			if action=="unload" and elapsed>=.52:check(slot==3,"workshop two-second timer holds authored final idle after520ms")
			samples.append({"action":action,"elapsed":elapsed,"timer":actor.timer,"stage":actor.stage,"slot":slot,"foot":[actor.foot.x,actor.foot.y]})
			actor.update(game,.02);game.visual_time_seconds+=.02
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		check(exited and seen.size()==4 and restores==4,"normal action exit/all four phases/restores")
		if action=="pickup":check(actor.stage=="workshop_carry" and not actor.path.is_empty(),"normal pickup creates carry route")
		else:check(actor.stage!="workshop_unload" and actor.action_elapsed()<0,"normal unload timer exits action")
		cases.append({"action":action,"slots":seen.keys(),"actorRestores":restores,"captureStart":first_capture,"captureCount":captures.size()-first_capture,"sampleStart":first_sample,"samples":samples.size()-first_sample,"exitStage":actor.stage,"exitState":actor.state,"exitDirection":actor.direction})
		print("ACTION DONE "+action+" samples="+str(samples.size()-first_sample))
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"samples":samples,"scope":"Normal Marsh.update/main/grid/player staged East workshop pickup entered from work timer; East unload seeded valid action. Four130ms frames,normal .52pickup and2secondunload finalidle hold,actor/player restores andpause. NOT actual workshop arrival (it forcesNorth),expedition/fullsave/TitleContinue/contactfilm/normal admission/fullsetacceptance."},"\\t"));file.close()
	print("MARSH EAST ACTION: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures]);quit(1 if failures else 0)
'''
out=ROOT/'tools/review_marsh_cargo_east_action01_actor.gd';out.write_text(prefix+tail)
(ROOT/'tools/review_marsh_cargo_east_action01_actor.gd.uid').write_text('uid://dm9cargoact1v05\n')
print('normal timed-action fixture prepared; East unload arrival not claimed')
