"""Prepare independent normal catalog/full-checkpoint running regression fixture."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tests/test_marsh_west_damage_production.gd').read_text()
prefix=source.split('\tfor key in ["death-ground-west"')[0]
prefix=prefix.replace('west-damage','south-run').replace('"west"','"south"').replace('"-west"','"-south"').replace('Normal damage family: full saves, actual visible Title Continues, exact drawn joins.','Normal running: full saves, actual visible Title Continues, exact source/root/phase joins.').replace('No test binding or West gait hook: normal update/renderer own both.','No test bindings or custom player: normal update/renderer own movement.')
route='''	check(player.frames["run-south"].size()==6 and player.timing["run-south"].loop,"normal selected six-frame loop")
	check(is_equal_approx(player.strides["run-south"],.11027027027027027),"normal selected run distance cadence")
	for slot in range(6):
		var expected=Image.load_from_file("res://character/marsh-south-run-material-v1/candidate-05/%03d.png"%slot)
		check(player.frames["run-south"][slot].get_image().get_data()==expected.get_data(),"normal factory loaded exact05 source "+str(slot))
	var route_start:=Vector2.INF
	for dx in [-30.0,0.0,30.0]:
		for dy in [-100.0,-85.0,-70.0]:
			var candidate:Vector2=desired+Vector2(dx,dy);var clear:=true
			for travel in range(0,169,4):
				var point:=candidate+Vector2(0,travel)
				if not actor.can_stand(point):clear=false
				for side in [-25.0,25.0]:
					if not actor.can_stand(point+Vector2(side,-45)):clear=false
			if clear and actor.segment_clear(candidate,candidate+Vector2(0,168)):route_start=candidate;break
		if route_start.is_finite():break
	check(route_start.is_finite(),"normal clear168world South route/body envelope")
	if not route_start.is_finite():quit(1);return
	actor=reset_actor(cell,route_start);game.visual_time_seconds=100.0
	game.grid_view._get_marsh_frame(game);await save_case("idle-before",cell,camera)
	actor.state="walk";actor.goal="curiosity";actor.path=PackedVector2Array([route_start+Vector2(0,168)])
	var seen:Dictionary={};var walk_saved:=false
	for step in range(95):
		tick(.02)
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		if actor.run_motion_active():
			var slot:int=player.frames["run-south"].find(texture)
			check(slot>=0 and slot<6,"normal full update drives selected run source")
			if not seen.has(slot):seen[slot]=true;await save_case("run-%d"%slot,cell,camera)
		elif not walk_saved:
			check(seen.size()==6,"six running holds precede normal slowing")
			await save_case("walk-after",cell,camera);walk_saved=true
	check(seen.size()==6 and walk_saved and checkpoints.size()==8,"idle six run phases and slowing walk checkpoints")
	current_scene=null;game.queue_free();await process_frame
'''
restore=source.split('\tfor item in checkpoints:')[1].split('\tvar cases: Array=[]')[0]
restore='\tfor item in checkpoints:'+restore
restore=restore.replace('west-damage','south-run')
start=restore.index('\t\tif actor.dead:');end=restore.index('\t\tcheck(Marsh.valid_marsh_snapshot',start)
restore=restore[:start]+'''		if item.case.begins_with("run-"):
			check(actor.run_motion_active(),"restored ongoing run classification "+item.case)
			var before:Vector2=actor.foot;var phase_before:float=player.phase
			tick(.02)
			check(actor.foot.y>before.y and actor.direction=="south" and actor.run_motion_active(),"continued normal route progresses after unpause "+item.case)
			check(player.current_key=="run-south" and player.phase>phase_before,"continued distance phase advances without idle reset "+item.case)
		else:
			check(not actor.run_motion_active(),"restored nonrun endpoint stays nonrun "+item.case)
'''+restore[end:]
tail='''	var cases:Array=[]
	for item in checkpoints:cases.append({"case":item.case,"disk":item.disk})
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"checkpoints":cases,"captures":records,"scope":"Normal ordered catalog and exact Marsh factory/main/grid/player.8full RunSave checkpoints/8fresh actual visible TitleContinues: selectedidle,six running phases,normal slowing walk. Whole actor/player/source/root parity,pause and ongoing route/distance phase after unpause. Prescribed clear168world furnished site, world/peers paused, normal costs/failures. Provisional master/material/contacts; no natural traffic/equipment or continuous film acceptance."},"\\t"));file.close()
	print("MARSH SOUTH RUN NORMAL: %dchecks,%dcheckpoints,%dviews,%dfailures"%[checks,checkpoints.size(),records.size(),failures])
	quit(1 if failures else 0)
'''
target=ROOT/'tests/test_marsh_south_run_production.gd';assert not target.exists();target.write_text(prefix+route+restore+tail,encoding='utf-8');target.with_suffix('.gd.uid').write_text('uid://cp6shrunb2v83\n')
print('Prepared independent normal eight-checkpoint running/Continue fixture and UID.')
