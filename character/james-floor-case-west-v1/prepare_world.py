from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
base=(r/'character/james-cargo-return-bridges-v1/actor-return-v9.gd').read_text()
base=base[:base.index('\tfor mode in ["bare","helmet"]:')]
base=base.replace('const OUT := "res://character/james-cargo-return-bridges-v1/"','const OUT := "res://character/james-floor-case-west-v1/"')
base=base.replace('OUT+"bare-joined-manifest-v9.json"','"res://character/james-cargo-return-bridges-v1/bare-joined-manifest-v9.json"').replace('OUT+"helmet-joined-manifest-v9.json"','"res://character/james-cargo-return-bridges-v1/helmet-joined-manifest-v9.json"')
base=base.replace('func run() -> void:', '''func prop_slot():
	if not game.grid_view.content_canvases.has(ORIGIN):return null
	for slot in game.grid_view.content_canvases[ORIGIN].slots:
		if slot.visible and slot.item.get("prop",{}).get("id","")=="james-floor-case-study":return slot
	return null
func record_case(view,npc,label:String)->void:
	var texture:Texture2D=game.grid_view._get_branforth_frame(game)
	var source:String=OUT+"arrival-captures/"+label+"-source.png"
	check(texture.get_image().save_png(source)==OK,"Save current source")
	var world:String=await capture(label,npc)
	var slot=prop_slot()
	check((slot!=null)==view.case_enabled,"Separate case submission matches enabled state")
	if slot!=null:check(slot.item.prop.rect==view.case_rect(),"Submitted prop uses fixed rect")
	results.append({"label":label,"source":source,"world":world,"foot":[npc.foot.x,npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"enabled":view.case_enabled,"sortY":slot.item.sort_y if slot!=null else 0,"state":npc.animation_state(),"direction":npc.direction})
func run() -> void:''')
run='''	var view=preload("res://character/james-floor-case-west-v1/workshop_preview.gd").new()
	view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
	check(game.grid_view._bill_room_view(game.occupied[ORIGIN])==view,"Explicit fixture workshop renderer")
	for mode in ["bare","helmet"]:
		view.case_enabled=false
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
		var until:float=player.return_plan.until
		while game.visual_time_seconds<until-.03:
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		var fixed_foot:Vector2=npc.foot
		view.case_anchor=fixed_foot-center
		var fixed_rect:Rect2=view.case_rect()
		await record_case(view,npc,mode+"-terminal")
		for tick in range(10):
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			if player.return_plan.is_empty():break
		check(player.return_plan.is_empty() and npc.foot==fixed_foot,"Return reaches standing at same contact")
		await record_case(view,npc,mode+"-idle-baseline")
		view.case_enabled=true
		await record_case(view,npc,mode+"-idle-case")
		var slot=prop_slot();var actor_slot=null
		if game.grid_view.content_canvases.has(ORIGIN):
			for item in game.grid_view.content_canvases[ORIGIN].slots:
				if item.visible and item.item.get("kind","")=="crew":actor_slot=item
		check(actor_slot!=null and actor_slot.item.member.texture==game.grid_view._get_branforth_frame(game),"Identify actual James crew slot by current texture")
		check(slot!=null and actor_slot!=null and slot.get_index()<actor_slot.get_index(),"Registered case floor draws behind James boots")
		if slot!=null and actor_slot!=null:
			results.append({"depthDiagnostic":true,"mode":mode,"caseDepth":slot.item.sort_y,"crewDepth":actor_slot.item.sort_y,"caseIndex":slot.get_index(),"crewIndex":actor_slot.get_index(),"crewPosition":[actor_slot.item.member.position.x,actor_slot.item.member.position.y],"physicalAnchor":[view.case_anchor.x,view.case_anchor.y]})
		var seen:Dictionary={};var departed:=false
		for tick in range(1800):
			npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			check(view.case_anchor==fixed_foot-center and view.case_rect()==fixed_rect,"Case cannot follow actor")
			var distance:float=npc.foot.distance_to(fixed_foot)
			for mark in [8,24,48]:
				if distance>=mark and not seen.has(mark):
					seen[mark]=true;await record_case(view,npc,mode+"-depart%d"%mark)
			if distance>=48:departed=true;break
		check(departed,"Ordinary next activity departs fixed case")
		print("JAMES FLOOR CASE WORLD ",mode," departure=",npc.foot.distance_to(fixed_foot)," goal=",npc.goal," state=",npc.state," failures=",failures)
		if failures:quit(1);return
	for name in ["world.gd","workshop_preview.gd"]:
		if not FileAccess.file_exists(OUT+name+".uid"):
			var uid:=FileAccess.open(OUT+name+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var f:=FileAccess.open(OUT+"world-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Unselected fixed West floor-case prop, actual prescribed workshop carry power-loss return using v9 staged actor/player, both gears. Fixture enables prop only after finite return. Native terminal/idle/departure source/world captures, fixed anchor and sorted queue. No automatic release/ownership, priorities, save/Continue, other cardinals or continuous movie acceptance."},"  "))
	print("JAMES FLOOR CASE WORLD: ",checks,"checks; ",failures,"failures;12presentations")
	quit(1 if failures else 0)
'''
(p/'world.gd').write_text(base+run)
paths=[p/'world.gd',p/'workshop_preview.gd',p/'floor-case-west.png',r/'scripts/grid_canvas.gd',r/'scripts/branforth_npc.gd',r/'scripts/crew_sprite_player.gd',r/'character/james-cargo-return-bridges-v1/return_actor.gd',r/'character/james-cargo-return-bridges-v1/return_player.gd']
(p/'world-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Actual West return/idle/departure contact fixture prepared;8targeted inputs frozen.')
