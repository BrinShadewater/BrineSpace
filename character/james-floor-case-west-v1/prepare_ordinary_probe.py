from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'normal_checkpoint_probe.gd').read_text()
s=s[:s.index('\tfor mode in ["bare","helmet"]:')]
s+='''\tfor mode in ["bare","helmet"]:
		for scenario in ["cue","large","loss_before","loss_after"]:
			game.occupied.clear();game.placed_rooms=original_rooms.duplicate(true);game.powered_room_cells.clear()
			for room in game.placed_rooms:room.erase(FLOOR.FIELD);game.occupied[room.pos]=room;game.powered_room_cells[room.pos]=true
			npc=game.BranforthNPC.new();game.branforth_npc=npc;npc.preview_player=player
			npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="dry"
			npc.helmet_equipped=mode=="helmet";npc.foot=contact;npc.direction="west"
			npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.stage="workshop_unload";npc.state="idle";npc.timer=2.0
			player.return_plan.clear();player.motion.clear();player.current_key="";player.last_source.clear();player.last_time=-1
			game.visual_time_seconds=100.0;game.grid_view._get_branforth_frame(game)
			var anchor:Vector2=contact-center
			if scenario=="cue":
				npc.update(game,.36);game.visual_time_seconds+=.36;game.grid_view._get_branforth_frame(game)
				check(FLOOR.payload(game.occupied[ORIGIN]).is_empty(),"Ordinary no case before actual cue")
				npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
				check(FLOOR.payload(game.occupied[ORIGIN]).get("anchor")==anchor,"Ordinary release owns exact floor anchor")
				check(player.return_plan.is_empty() and npc.stage=="workshop_unload","Ordinary timed action retained")
			elif scenario=="large":
				npc.update(game,2.1);game.visual_time_seconds+=2.1;game.grid_view._get_branforth_frame(game)
				check(FLOOR.payload(game.occupied[ORIGIN]).get("anchor")==anchor,"Large ordinary completion retains crossed cue")
				check(player.return_plan.is_empty(),"Ordinary completion does not fabricate interruption plan")
			else:
				var elapsed:float=.15 if scenario=="loss_before" else .42
				npc.update(game,elapsed);game.visual_time_seconds+=elapsed;game.grid_view._get_branforth_frame(game)
				var owned_before:Dictionary=FLOOR.payload(game.occupied[ORIGIN]).duplicate(true)
				game.powered_room_cells.clear()
				npc.update(game,.6);game.grid_view._get_branforth_frame(game)
				check(not player.return_plan.is_empty(),"Normal unload power loss creates source-bound return")
				var release:float=FLOOR.release_time(player)
				if scenario=="loss_before":
					check(game.visual_time_seconds<release and FLOOR.payload(game.occupied[ORIGIN]).is_empty(),"Large interruption delta cannot publish future release early")
				else:check(not owned_before.is_empty() and FLOOR.payload(game.occupied[ORIGIN])==owned_before,"Post-cue loss retains existing case")
				game.visual_time_seconds=release+.001;npc.update(game,.02);game.grid_view._get_branforth_frame(game)
				check(FLOOR.payload(game.occupied[ORIGIN]).get("anchor")==anchor,"Interrupted source cue retains exact floor anchor")
			check(SAVE.problem(SAVE.capture(game)).is_empty(),"Ordinary/interrupted normal checkpoint remains valid")
			await record_case(view,npc,mode+"-ordinary-normal-v1-"+scenario)
			results.append({"ordinary":true,"mode":mode,"scenario":scenario,"owned":not FLOOR.payload(game.occupied[ORIGIN]).is_empty()})
	for path in [OUT+"ordinary_normal_probe.gd.uid"]:
		if not FileAccess.file_exists(path):
			var uid:=FileAccess.open(path,FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var output:=FileAccess.open(OUT+"ordinary-normal-evidence.json",FileAccess.WRITE)
	output.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Eight prescribed ordinary West unload scenarios/both gears: cue crossing, large finite completion, power loss before/after release. Normal actor/player/renderer and source-bound return. Native case/source ownership, no early release or duplicate submission, valid normal capture. No natural scheduling/all-cardinal/hazard regression or full master acceptance."},"  "))
	print("JAMES ORDINARY NORMAL: ",checks,"checks;",failures,"failures;8cases")
	quit(0 if failures==0 else 1)
'''
(p/'ordinary_normal_probe.gd').write_text(s)
prior=json.loads((p/'normal_checkpoint_probe-inputs.json').read_bytes());paths=[r/k for k in prior]+[p/'ordinary_normal_probe.gd']
(p/'ordinary-normal-inputs.json').write_text(json.dumps({str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},indent=2)+'\n')
print('Eight normal ordinary cue/large-delta/interruption cases prepared; source clocks drive release.')
