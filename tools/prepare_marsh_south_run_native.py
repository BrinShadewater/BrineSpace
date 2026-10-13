"""Prepare actual actor/renderer staged run study in a clear furnished site."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'tools/review_marsh_south_collapse_actor.gd').read_text()
prefix=src.split('\tvar player = game.grid_view.marsh_player')[0]
prefix=prefix.replace('south-collapse-actor-01-2026-10-02','south-run-actor-04-v2-2026-10-02').replace('marsh-south-collapse-material-v1/candidate-01','marsh-south-run-material-v1/candidate-04').replace('collapse-study','run-study')
tail='''	var route_start := Vector2.INF
	for dx in [-30.0,0.0,30.0]:
		for dy in [-100.0,-85.0,-70.0]:
			var candidate: Vector2 = desired+Vector2(dx,dy)
			var clear := true
			for travel in range(0,169,4):
				var point := candidate+Vector2(0,travel)
				if not actor.can_stand(point): clear=false
				for side in [-25.0,25.0]:
					if not actor.can_stand(point+Vector2(side,-45)):clear=false
			if clear and actor.segment_clear(candidate,candidate+Vector2(0,168)):route_start=candidate;break
		if route_start.is_finite():break
	check(route_start.is_finite(),"clear168world South segment with whole-body envelope")
	if not route_start.is_finite():quit(1);return
	actor.foot=route_start;actor.state="idle";actor.goal="";actor.path=PackedVector2Array()
	var player=game.grid_view.marsh_player
	var old_stride:float=player.strides["run-south"]
	player.load_manifest(MANIFEST,true)
	check(player.strides["run-south"]==old_stride,"staged override retains selected distance cadence")
	check(is_equal_approx(player.cycle_seconds("run-south"),.6),"six100ms cycle retained")
	game.visual_time_seconds=100.0;player.current_key=""
	await capture("selected idle before run",-1)
	actor.state="walk";actor.goal="curiosity";actor.path=PackedVector2Array([route_start+Vector2(0,168)])
	game.paused=false
	var seen:Dictionary={};var previous_slot:=-1;var wraps:=0;var restores:=0;var left_run:=false
	for step in range(95):
		var before:Vector2=actor.foot
		actor.move(.02)
		game.visual_time_seconds=100.02+step*.02
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		var running:bool=actor.run_motion_active()
		var slot:int=player.frames["run-south"].find(texture) if running else -1
		check(actor.direction=="south" and actor.foot.x==route_start.x,"actual movement keeps South heading/root axis")
		check(actor.foot.y>=before.y and actor.foot.y<=route_start.y+168,"actual controller progresses within route")
		if running:
			check(slot>=0 and slot<6,"normal grid uses staged run source")
			check(absf(actor.foot.distance_to(before)-69.0*.02)<.001,"normal run rate is69world/sec within submillimetre world-coordinate precision")
			if previous_slot==5 and slot==0:wraps+=1
			if slot!=previous_slot and previous_slot>=0:check(slot==(previous_slot+1)%6,"distance gait advances phase order including wrap")
			if not seen.has(slot):
				seen[slot]=true
				await capture("actual South run pose%d"%slot,slot)
				var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
				check(Normal.valid_marsh_snapshot(saved),"moving normal run snapshot validates")
				var restored=Normal.new();game.marsh_npc=restored
				await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true)
				player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"run actor/player restore preserves root and source")
				game.paused=true;restored.update(game,.5)
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"pause freezes moving actor and source")
				game.paused=false;actor=restored;restores+=1
			previous_slot=slot
		else:
			left_run=true
			check(actor.foot.distance_to(route_start+Vector2(0,168))<=Normal.RUN_STOP_DISTANCE+1.4,"run only stops within normal hysteresis range")
			check(texture not in player.frames["run-south"],"normal slowing hands off from run sources")
		if step%1==0:samples.append({"elapsed":(step+1)*.02,"slot":slot,"running":running,"foot":[actor.foot.x,actor.foot.y],"playerPhase":player.phase})
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(seen.size()==6 and restores==6 and wraps>=2,"all six phases restored and cycle wraps twice")
	check(left_run,"normal controller slows near destination")
	await capture("normal walk after run",-2)
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"actorRestores":restores,"wraps":wraps,"strideDistanceCells":old_stride,"scope":"Normal Marsh.move/run guards/rate, main/grid/player with explicit staged run manifest on clear168world furnished-room segment; controlled95x20ms simulation/render samples, six actor+player restores/pause holds, near-destination walk. No fullRunSave/TitleContinue or realtime film/contact acceptance."},"\\t"));file.close()
	print("MARSH SOUTH RUN ACTOR: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures])
	quit(1 if failures else 0)
'''
target=ROOT/'tools/review_marsh_south_run_actor.gd';assert not target.exists();target.write_text(prefix+tail,encoding='utf-8');target.with_suffix('.gd.uid').write_text('uid://cm3shrunm8v80\n')
print('Prepared staged actual normal run actor study and paired UID.')
