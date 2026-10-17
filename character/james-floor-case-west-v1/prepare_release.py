from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
s=(p/'world.gd').read_text()
s=s[:s.index('\tvar view=preload(')]
s=s.replace('res://character/james-cargo-return-bridges-v1/return_actor.gd','res://character/james-floor-case-west-v1/floor_actor.gd').replace('res://character/james-cargo-return-bridges-v1/return_player.gd','res://character/james-floor-case-west-v1/floor_player.gd')
s=s.replace('const ORIGIN :=','const FLOOR=preload("res://character/james-floor-case-west-v1/floor_state.gd")\nconst ORIGIN :=')
s=s.replace('"enabled":view.case_enabled,','"enabled":view.case_enabled,"owned":not FLOOR.payload(game.occupied.get(ORIGIN,{})).is_empty(),"embedded":view.embedded_case,')
run='''	var view=preload("res://character/james-floor-case-west-v1/release_workshop.gd").new()
	view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
	player.preview_game=game;player.preview_view=view;player.preview_cell=ORIGIN
	check(game.grid_view._bill_room_view(game.occupied[ORIGIN])==view,"Explicit source-bound floor renderer")
	for bad in [{"version":1.0,"source":FLOOR.SOURCE,"anchor":Vector2.ZERO},{"version":2,"source":FLOOR.SOURCE,"anchor":Vector2.ZERO},{"version":1,"source":"other","anchor":Vector2.ZERO},{"version":1,"source":FLOOR.SOURCE,"anchor":Vector2.INF},{"version":1,"source":FLOOR.SOURCE,"anchor":Vector2(193,0)},{"version":1,"source":FLOOR.SOURCE,"anchor":[0,0]},{"version":1,"source":FLOOR.SOURCE,"anchor":Vector2.ZERO,"extra":true}]:
		check(not FLOOR.valid_payload(bad),"Reject malformed floor payload")
	check(FLOOR.valid_payload({"version":1,"source":FLOOR.SOURCE,"anchor":Vector2.ZERO}),"Valid finite room-local anchor")
	check(FLOOR.valid_rooms([{"id":"salvage_workshop"}]),"Legacy room without floor state valid")
	check(not FLOOR.valid_rooms([{"id":"storage_bay",FLOOR.FIELD:{"version":1,"source":FLOOR.SOURCE,"anchor":Vector2.ZERO}}]),"Floor state restricted to workshop")
	for mode in ["bare","helmet"]:
		game.occupied[ORIGIN].erase(FLOOR.FIELD);view.bind_room(game.occupied[ORIGIN]);view.embedded_case=false;view.sync_case()
		game.powered_room_cells[ORIGIN]=true;game.visual_time_seconds=100;game.paused=false
		npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.expedition.clear();npc.stage="";npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.timer=0;npc.needs.curiosity=90
		npc.foot=start;npc.direction=facing;npc.path=PackedVector2Array([contact]);npc.movement_medium="dry";npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		player.current_key="";player.motion.clear();player.last_time=-1;player.return_plan.clear();player.last_source.clear()
		var reached:=false;var carry_ticks:=0
		for tick in range(2000):
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			if npc.stage!="workshop_carry":continue
			carry_ticks+=1
			if carry_ticks>=20:reached=true;break
		check(reached,"Actual carry reached")
		game.powered_room_cells.erase(ORIGIN);npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		check(not player.return_plan.is_empty() and player.return_plan.facing=="west","Actual source-bound West return")
		if failures:quit(1);return
		var plan:Dictionary=player.return_plan.duplicate(true)
		var release:float=FLOOR.release_time(player);var until:float=plan.until;var fixed_foot:Vector2=plan.floorFoot
		check(is_finite(release) and release>plan.started and release<until,"Reviewed exact source release cue")
		var gear:String="diving-helmet" if mode=="helmet" else ""
		var bank:Dictionary=player.bank_for(gear);var retained:Texture2D=bank["unload-west"][4]
		bank["unload-west"][4]=bank["unload-west"][3]
		check(not FLOOR.cue_available(player,gear) and not is_finite(FLOOR.release_time(player)),"Reject mismatched release artwork")
		bank["unload-west"][4]=retained
		player.return_plan.rows[0].seconds=-.08
		check(not is_finite(FLOOR.release_time(player)),"Reject malformed source clock")
		player.return_plan=plan.duplicate(true)
		game.occupied[ORIGIN][FLOOR.FIELD]={"version":1,"source":FLOOR.SOURCE,"anchor":Vector2.INF}
		check(not FLOOR.observe_plan(game,npc,player,release+.001),"Never overwrite malformed existing room state")
		game.occupied[ORIGIN].erase(FLOOR.FIELD)
		check(not FLOOR.observe_plan(game,npc,player,release-.001),"Cannot release before reviewed cue")
		while game.visual_time_seconds<release-.03:
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		check(FLOOR.payload(game.occupied[ORIGIN]).is_empty() and not view.case_enabled,"No pre-release floor case")
		await record_case(view,npc,mode+"-release-before")
		for tick in range(20):
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			if not FLOOR.payload(game.occupied[ORIGIN]).is_empty():break
		var owned:Dictionary=FLOOR.payload(game.occupied[ORIGIN]).duplicate(true)
		check(not owned.is_empty() and owned.anchor==fixed_foot-center,"Actual cue creates fixed room-owned case")
		check(view.embedded_case and not view.case_enabled,"No duplicate prop while release source embeds case")
		check(not FLOOR.observe_plan(game,npc,player,game.visual_time_seconds),"Repeated observation idempotent")
		check(FLOOR.valid_rooms(game.placed_rooms),"Owned room state validates")
		await record_case(view,npc,mode+"-release-embedded")
		while game.visual_time_seconds<until-.03:
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		check(FLOOR.payload(game.occupied[ORIGIN])==owned and view.embedded_case and not view.case_enabled,"Late embedded source retains ownership without duplicate")
		await record_case(view,npc,mode+"-release-terminal")
		for tick in range(10):
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			if player.return_plan.is_empty():break
		check(player.return_plan.is_empty() and npc.foot==fixed_foot,"Finite return completes at same contact")
		check(FLOOR.payload(game.occupied[ORIGIN])==owned and view.case_enabled and not view.embedded_case,"Room automatically draws case after actor source stops embedding it")
		await record_case(view,npc,mode+"-release-idle")
		var fixed_rect:Rect2=view.case_rect();var seen:Dictionary={};var departed:=false
		for tick in range(1800):
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			check(FLOOR.payload(game.occupied[ORIGIN])==owned and view.case_rect()==fixed_rect,"Room ownership/anchor cannot follow actor")
			var distance:float=npc.foot.distance_to(fixed_foot)
			for mark in [8,24,48]:
				if distance>=mark and not seen.has(mark):
					seen[mark]=true;await record_case(view,npc,mode+"-release-depart%d"%mark)
			if distance>=48:departed=true;break
		check(departed,"Ordinary next activity leaves room-owned floor case")
		print("JAMES FLOOR RELEASE ",mode," departure=",npc.foot.distance_to(fixed_foot)," failures=",failures)
		if failures:quit(1);return
	for name in ["release.gd","floor_state.gd","floor_actor.gd","floor_player.gd","release_workshop.gd"]:
		if not FileAccess.file_exists(OUT+name+".uid"):
			var uid:=FileAccess.open(OUT+name+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var f:=FileAccess.open(OUT+"release-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Staged automatic room-owned West floor case at exact reviewed unload4 source cue. Both gears, actual prescribed power-loss carry return, no fixture case enable. Suppress duplicate embedded case, then render separate prop on finite completion and ordinary departure. State/source-clock guards. No emergency/room-removal native priority, ordinary Save/Continue, normal selection, other cardinal or continuous movie acceptance."},"  "))
	print("JAMES FLOOR RELEASE: ",checks,"checks; ",failures,"failures;14presentations")
	quit(1 if failures else 0)
'''
(p/'release.gd').write_text(s+run)
paths=[p/name for name in ['release.gd','floor_state.gd','floor_actor.gd','floor_player.gd','release_workshop.gd','workshop_preview.gd','floor-case-west.png']]+[r/name for name in ['scripts/grid_canvas.gd','scripts/branforth_npc.gd','scripts/crew_sprite_player.gd','character/james-cargo-return-bridges-v1/return_actor.gd','character/james-cargo-return-bridges-v1/return_player.gd']]
(p/'release-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Automatic source-bound West release prepared;12targeted inputs frozen.')
