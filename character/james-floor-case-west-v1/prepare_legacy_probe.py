from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'normal_checkpoint_probe.gd').read_text()
s=s[:s.index('\tfor mode in ["bare","helmet"]:')]
s+='''\tfor mode in ["bare","helmet"]:
		npc=game.BranforthNPC.new();game.branforth_npc=npc;npc.preview_player=player
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="dry"
		npc.helmet_equipped=mode=="helmet";npc.foot=contact;npc.direction="east"
		npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.stage="workshop_unload";npc.state="idle";npc.timer=1.55
		player.return_plan.clear();player.motion.clear();player.current_key="";player.last_source.clear();player.last_time=-1
		game.visual_time_seconds=100.0
		for room in game.placed_rooms:room.erase(FLOOR.FIELD);game.powered_room_cells[room.pos]=true
		var initial:Texture2D=game.grid_view._get_branforth_frame(game)
		var legacy:Dictionary=SAVE.capture(game);legacy.erase("james_cargo_return")
		check(SAVE.problem(legacy).is_empty(),"Legacy packet with no extension valid")
		var bytes:PackedByteArray=var_to_bytes(legacy)
		var path:String="user://legacy-james-"+mode+".save"
		var file:=FileAccess.open(path,FileAccess.WRITE);file.store_string(bytes.hex_encode().sha256_text()+"\\n");file.store_buffer(bytes);file.close()
		var loaded:Dictionary=SAVE.read(path)
		check(not loaded.is_empty() and not loaded.has("james_cargo_return"),"Actual normal legacy checksum reader")
		player.return_plan={"stale":true}
		check(await SAVE.restore_staged(game,loaded),"Actual normal legacy restore")
		npc=game.branforth_npc;player=game.grid_view.branforth_player;view=game.grid_view._bill_room_view(game.occupied[ORIGIN])
		check(player.return_plan.is_empty() and npc.preview_player==player,"Legacy restore clears old session return and binds normal player")
		check(game.paused and game.visual_time_seconds==100.0 and npc.stage=="workshop_unload" and npc.direction=="east" and npc.timer==1.55,"Legacy actor/clock/action preserved")
		var resumed:Texture2D=game.grid_view._get_branforth_frame(game)
		check(resumed.get_image().get_data()==initial.get_image().get_data(),"Legacy unchanged East source whole RGBA exact")
		check(FLOOR.payload(game.occupied[ORIGIN]).is_empty(),"Legacy case metadata not invented")
		await record_case(view,npc,mode+"-legacy-normal-v1-restored")
		results.append({"legacy":true,"mode":mode,"sourceExact":true,"extensionAbsent":true,"stalePlanCleared":true})
		game.paused=false
	for path in [OUT+"legacy_normal_probe.gd.uid"]:
		if not FileAccess.file_exists(path):
			var uid:=FileAccess.open(path,FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var output:=FileAccess.open(OUT+"legacy-normal-evidence.json",FileAccess.WRITE)
	output.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Two legacy-shaped extension-absent packets from unchanged East normal cargo action, both gears. Normal checksum read/restore_staged, stale session plan cleared, exact source/action/timer/clock and no invented case. Native restored source/room pairs. No historical owner save or title/new-process legacy Continue."},"  "))
	print("JAMES LEGACY NORMAL: ",checks,"checks;",failures,"failures;2cases")
	quit(0 if failures==0 else 1)
'''
(p/'legacy_normal_probe.gd').write_text(s)
prior=json.loads((p/'normal_checkpoint_probe-inputs.json').read_bytes());paths=[r/k for k in prior]+[p/'legacy_normal_probe.gd']
(p/'legacy-normal-inputs.json').write_text(json.dumps({str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},indent=2)+'\n')
print('Two extension-absent East cargo legacy cases prepared; no owner checkpoint used.')
