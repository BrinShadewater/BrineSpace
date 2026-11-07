"""Exercise other arrival arcs and snapshot validation, not invented route claims."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_cargo_delivery02_actor.gd').read_text().split('\tvar cases:Array=[]')[0]
s=s.replace('cargo-delivery-02-2026-10-02','cargo-arrival-branches-01-2026-10-02')
tail='''
	var cases:Array=[]
	for incoming in ["east","south","north"]:
		actor=Normal.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction=incoming;actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=cell
		actor.path=PackedVector2Array();actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		actor.arrive();game.paused=false;player.current_key="";player.motion={}
		check(actor.stage=="workshop_unload" and actor.direction=="north" and is_equal_approx(actor.timer,2),"actual arrive method keeps North/state/2second timer")
		var duration:float=0 if incoming=="north" else (.8 if incoming=="south" else .4)
		var turn_key:String="" if incoming=="north" else "carry-turn-"+incoming+"-north"
		var seen:Dictionary={};var turn_seen:Dictionary={};var unload_seen:Dictionary={};var restores:=0
		for step in range(100):
			var elapsed:float=step*.02;var expected_key:String=turn_key if elapsed<duration-.0000001 else "unload-north"
			var expected_elapsed:float=elapsed if expected_key==turn_key else elapsed-duration
			var texture:Texture2D=game.grid_view._get_marsh_frame(game);var slot:int=player.frames[expected_key].find(texture)
			check(actor.foot==start and actor.stage=="workshop_unload" and is_equal_approx(actor.timer,2-elapsed),"presentation turn never moves root or extends timer")
			check(slot>=0,"independent .4/.8/0 arrival boundary chooses expected source key")
			if expected_key=="unload-north":
				check(slot==mini(3,int(floor((expected_elapsed+.000001)/.13))),"shifted lowering uses4x130ms phases")
				unload_seen[slot]=true
			else:turn_seen[slot]=true
			var signature:String=expected_key+":"+str(slot)
			if not seen.has(signature):
				seen[signature]=true;var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
				check(Normal.valid_marsh_snapshot(saved),"arrival snapshot validates")
				var old:Dictionary=saved.duplicate(true);old.erase("workshop_arrival_origin")
				check(Normal.valid_marsh_snapshot(old),"old prototype snapshot without arrival field remains valid")
				for bad in [42,"north","other"]:
					var invalid:Dictionary=saved.duplicate(true);invalid.workshop_arrival_origin=bad
					check(not Normal.valid_marsh_snapshot(invalid),"malformed arrival origin rejected")
				if incoming!="north":
					var invalid:Dictionary=saved.duplicate(true);invalid.direction="east"
					check(not Normal.valid_marsh_snapshot(invalid),"arrival metadata outside North unload rejected")
				var restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"arrival snapshot restores exact root/source")
				game.paused=true;restored.update(game,.5)
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"paused arrival holds timer/root/source")
				game.paused=false;actor=restored;restores+=1
			samples.append({"incoming":incoming,"elapsed":elapsed,"key":expected_key,"slot":slot})
			actor.update(game,.02)
		check(actor.stage!="workshop_unload","arrival plus lowering exits within unchanged2seconds")
		check(turn_seen.size()==(0 if incoming=="north" else (9 if incoming=="south" else 5)) and unload_seen.size()==4,"all branch turn/lowering phases covered")
		cases.append({"incoming":incoming,"turnDuration":duration,"turnSlots":turn_seen.keys(),"unloadSlots":unload_seen.keys(),"actorRestores":restores,"samples":100})
		print("ARRIVAL BRANCH DONE "+incoming+" restores="+str(restores))
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"samples":samples,"scope":"Actual arrive method invoked from valid seeded incoming East/South/North states; normal timer update/grid source selection,root unchanged,quarter400/opposite800/direct0,4x130lowering,2secondtotal. Snapshot restore/pause/malformed-origin rejection/old-field compatibility. Not complete routes or visual/contact/fullSave/TitleContinue/fullset acceptance."},"\\t"));file.close()
	print("MARSH ARRIVAL BRANCHES: %dchecks,%dfailures"%[checks,failures]);quit(1 if failures else 0)
'''
(ROOT/'tools/review_marsh_cargo_arrival_branches01_actor.gd').write_text(s+tail)
(ROOT/'tools/review_marsh_cargo_arrival_branches01_actor.gd.uid').write_text('uid://dt7cargoarr1v11\n')
finger=(ROOT/'tools/fingerprint_marsh_cargo_delivery02.py').read_text().replace('cargo_delivery02','cargo_arrival_branches01');(ROOT/'tools/fingerprint_marsh_cargo_arrival_branches01.py').write_text(finger)
print('remaining arrival-clock/snapshot branches prepared, route scope explicit')
