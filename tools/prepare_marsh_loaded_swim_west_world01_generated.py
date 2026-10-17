"""Actual dispatched expedition; only the privately staged East swim loop differs."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_cargo_delivery02_actor.gd').read_text()
s=s[:s.index('\tvar cell :=')]
s=s.replace('cargo-delivery-02-2026-10-02','loaded-swim-west-world-01-2026-10-02')
s=s.replace('const MANIFEST =','const Trips=preload("res://scripts/crew_expedition.gd")\nconst Cycle=preload("res://scripts/airlock_cycle.gd")\nconst MANIFEST =')
s+='''
	var home:=Vector2i(20,19);var target:=Vector2i(21,16)
	for y in range(16,20):
		for x in [20,21]:
			var cell=Vector2i(x,y)
			if game.wrecks.get(cell,{}).get("kind","") not in ["cryo","charging","recovery"]:game.wrecks.erase(cell)
	game._place_room("airlock",home,true);game.occupied[home].rotation=0;game.powered_room_cells[home]=true
	game.resources.oxygen=50;game.resources.food=50;game.resources.metal=5;game.resources.data=0
	game.drone_fleet.sites={target:game.drone_fleet.Sites.make_site("salvage",3)}
	game.drone_fleet.sites[target].discovered=true;game.drone_fleet.sites_initialized=true
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	game.selected_card_id="";game.hovered_card_id="";game.selected_room_cell=home;game.hand_panel.hide();game._refresh_all()
	var player=game.grid_view.marsh_player
	player.load_manifest("res://character/marsh-loaded-swim-material-v1/east-loop-02-unselected/manifest.json",true)
	player.load_manifest("res://character/marsh-loaded-swim-material-v1/west-loop-01-unselected/manifest.json",true)
	check(game.marsh_npc.get_script()==Normal,"actual normal Marsh factory")
	check(Trips.dispatch(game,"marsh",home),"actual normal expedition dispatch")
	actor=game.marsh_npc
	if actor.expedition.is_empty():quit(1);return
	var phases:Dictionary={};var seen:Dictionary={};var east:Dictionary={};var pickup:Dictionary={};var unload:Dictionary={};var drain:Dictionary={};var turns:Dictionary={}
	var joins:Array=[];var restores:=0;var previous_key:="";var previous_slot:=-1;var previous_phase:=""
	for step in range(9000):
		if actor.expedition.is_empty():break
		var phase:String=actor.expedition.phase;var pose:String=actor.animation_state();phases[phase]=true
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		check(texture!=null,"actual water route has source")
		if texture==null:break
		var key:String=pose+"-"+actor.direction
		var chamber:Dictionary=Cycle.state(game.occupied[home])
		var draining:bool=phase=="drain" and chamber.phase=="draining" and float(chamber.elapsed)>=1.6 and not actor.expedition.cargo.is_empty()
		if game.grid_view._get_marsh_cargo_drain_frame(game)!=null:key="cargo-drain-"+actor.direction
		elif actor.action_elapsed()<0 and not str(player.motion.get("clip","")).is_empty():key=player.motion.clip
		check(player.frames.has(key),"declared source key exists "+key)
		if not player.frames.has(key):break
		var slot:int=player.frames[key].find(texture)
		check(slot>=0,"normal route texture belongs to actual clip "+key)
		if slot<0:break
		if key=="swim-carry-west":east[slot]=true
		if phase=="pickup":pickup[slot]=true
		if phase=="unload" and not actor.expedition.cargo.is_empty():unload[slot]=true
		if draining:drain[slot]=true
		if key.begins_with("swim-carry-turn-"):turns[key]=true
		check(game.resources.metal==5 and game.resources.data==0,"cargo not credited before complete unload")
		if previous_key!=key or previous_phase!=phase:
			joins.append({"fromPhase":previous_phase,"phase":phase,"fromKey":previous_key,"fromSlot":previous_slot,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction})
		var wanted:bool=key.begins_with("swim-pickup-") or key.begins_with("swim-carry-") or key.begins_with("cargo-drain-") or key.begins_with("unload-")
		var signature:String=key+":"+str(slot)
		if wanted and not seen.has(signature):
			seen[signature]=true
			var camera:Vector2=actor.foot/(384.0*float(game.GRID_SIZE))
			game.paused=true;check(await settle_camera(camera),"native camera and layers settled")
			await capture(signature,slot);captures.back()["expectedKey"]=key;captures.back()["phase"]=phase
			var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
			check(Normal.valid_marsh_snapshot(saved),"real expedition actor validates")
			var restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
			check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"actual water-route phase source/root restore")
			game._process(.5)
			check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"actual water-route restored pause hold")
			actor=restored;restores+=1;game.paused=false
		samples.append({"step":step,"phase":phase,"key":key,"slot":slot,"direction":actor.direction,"medium":actor.movement_medium,"foot":[actor.foot.x,actor.foot.y],"routeLeft":actor.expedition.route.size(),"next":str(actor.expedition.route[0]) if not actor.expedition.route.is_empty() else "","chamber":chamber.phase,"battery":actor.battery})
		previous_key=key;previous_slot=slot;previous_phase=phase
		game.visual_time_seconds+=.02;Cycle.advance(game,.02);game._update_test_walker(.02)
	check(actor.expedition.is_empty() and not actor.dead and actor.movement_medium=="dry","actual expedition completed dry/alive")
	check(game.drone_fleet.sites[target].units==2 and game.resources.metal==6 and game.resources.data==1,"one extraction/one safe delivery credit")
	check(phases.size()==Trips.PHASES.size(),"all twelve real expedition phases")
	check(east.size()==6 and pickup.size()==6 and unload.size()==4 and drain.size()==5,"all six West timing slots (four drawings) and pickup/unload/drain holds")
	check(not turns.is_empty(),"actual loaded route turns selected")
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"phases":phases.keys(),"westSlots":east.keys(),"pickupSlots":pickup.keys(),"unloadSlots":unload.keys(),"drainSlots":drain.keys(),"turns":turns.keys(),"joins":joins,"actorPlayerRestores":restores,"scope":"One actual normal dispatched q0 expedition with free authored airlock/site fixture and normal cost/failure flags. Actual normal actor/update/Cycle/grid/player pickup/return/West staged loop/turns/drain/exit/unload/credit. Private East02 and West01 loaded-swim source overrides, old other clips. Actor/player restore/pause. Not all route rotations/fullRunSave/visibleTitleContinue/helmet/continuousmotion/physicalcontact/coherent-family admission/fullset acceptance."},"\\t"));file.close()
	print("MARSH LOADED SWIM WORLD02: ",checks,"checks,",failures,"failures,",captures.size(),"captures,",samples.size(),"samples")
	quit(1 if failures else 0)
'''
p=ROOT/'tools/review_marsh_loaded_swim_west_world01.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://bmzw4hg3cnj\n')
f=(ROOT/'tools/fingerprint_marsh_cargo_arrival_branches01.py').read_text().replace('arrival_branches01','loaded_swim_world02')
f=f.replace("data={p.relative_to(ROOT).as_posix()", "for p in (ROOT/'character/marsh-loaded-swim-material-v1').rglob('*'):\n    if p.is_file() and p.suffix in ['.png','.json','.txt']:paths.append(p)\ndata={p.relative_to(ROOT).as_posix()")
# Replace old fixture names with the actual newly generated fixture.
f=f.replace('prepare_marsh_cargo_loaded_swim_world02.py','prepare_marsh_loaded_swim_west_world01.py').replace('review_marsh_cargo_loaded_swim_world02_actor.gd','review_marsh_loaded_swim_west_world01.gd').replace('fingerprint_marsh_cargo_loaded_swim_world02.py','fingerprint_marsh_loaded_swim_west_world01.py')
(ROOT/'tools/fingerprint_marsh_loaded_swim_west_world01.py').write_text(f)
print('Prepared one real dispatched loaded-water journey, route left automatic; staged East loop only.')
