extends RefCounted
const Stop=preload("res://character/marsh-south-stop-v1/stop_controller.gd")
const Normal=preload("res://scripts/marsh_npc.gd")
class RestoredStop extends Stop:
	var arrival_callbacks:=0
	var choice_calls:=0
	func finish_south_stop_arrival() -> void:arrival_callbacks+=1;super.finish_south_stop_arrival()
	func choose_goal(main) -> void:choice_calls+=1;super.choose_goal(main)

static func source(tree,game,player) -> Texture2D:
	var actor=game.marsh_npc
	actor.prepare_south_gait(player,game.get_visual_time_seconds(),game.get_marsh_position()/game.get_cell_size())
	return game.grid_view._get_marsh_frame(game)
static func capture(tree,game,texture: Texture2D,label: String,moment: String):
	game.paused=true;game.grid_view.queue_redraw();await tree.process_frame;await RenderingServer.frame_post_draw
	var native_file: String="native-%03d.png"%tree.records.size();var source_file: String="source-%03d.png"%tree.records.size()
	tree.check(tree.root.get_texture().get_image().save_png(tree.OUTPUT+native_file)==OK and texture.get_image().save_png(tree.OUTPUT+source_file)==OK,"snapshot restored native/source pair captured")
	var actor=game.marsh_npc;var player=game.grid_view.marsh_player;var key: String=actor.animation_state()+"-"+actor.direction
	tree.records.append({"file":native_file,"sourceFile":source_file,"case":label,"moment":moment,"key":key,"slot":player.frames[key].find(texture),"foot":[actor.foot.x,actor.foot.y],"callbacks":actor.arrival_callbacks,"sourceShaPending":true})
static func restore_pair(tree,game,player,label: String) -> Dictionary:
	var actor=game.marsh_npc
	var packet: Dictionary={"actor":actor.snapshot(),"player":player.snapshot(),"visual_time":game.get_visual_time_seconds()}
	tree.check(Stop.valid_south_snapshot(packet.actor) and player.valid_snapshot(packet.player),"actual furnished actor/player snapshot valid")
	var path: String="user://south-snapshot-%03d.bin"%tree.records.size()
	var file=FileAccess.open(path,FileAccess.WRITE);tree.check(file!=null,"isolated actor-packet file opened")
	file.store_var(packet,false);file.close();file=FileAccess.open(path,FileAccess.READ)
	var decoded: Variant=file.get_var(false);file.close()
	tree.check(decoded is Dictionary and decoded==packet and Stop.valid_south_snapshot(decoded.actor),"Godot binary disk packet preserves Vector2/packed path/player types")
	var before: Texture2D=source(tree,game,player)
	await capture(tree,game,before,label,"before")
	var restored=RestoredStop.new();game.marsh_npc=restored;restored.bind_south_stop_player(player)
	game.visual_time_seconds=decoded.visual_time
	await restored.restore_snapshot(game,decoded.actor);player.restore_snapshot(decoded.player)
	tree.check(restored.snapshot()==decoded.actor and restored.arrival_callbacks==0 and player.snapshot()==decoded.player,"fresh actual actor rebuild restores exact packet before first draw without callback")
	var paused: Dictionary=restored.snapshot();restored.update(game,.5);restored.move(0)
	tree.check(restored.snapshot()==paused,"actual restored pause/zero retains namespaces")
	var after: Texture2D=source(tree,game,player)
	tree.check(after.get_image().get_data()==before.get_image().get_data(),"first actual restored source RGBA matches original")
	await capture(tree,game,after,label,"restored")
	return {"case":label,"actor":decoded.actor,"player":decoded.player,"diskPath":path,"normalMotionAccepted":Normal.valid_marsh_snapshot(decoded.actor)}

static func run(tree,game,cell: Vector2i,start: Vector2,player):
	var cases: Array=[]
	for clock in [.04,.18,.28,.36,.4,.7]:
		var actor=RestoredStop.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction="south";actor.state="idle";actor.goal="curiosity";actor.goal_cell=cell;actor.timer=10
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0};actor.bind_south_stop_player(player)
		player.current_key="";player.motion={};actor.path=PackedVector2Array([start+Vector2(0,100)]);actor._arm_selected_route()
		game.paused=false
		for step in range(roundi(clock/.02)):
			game.visual_time_seconds+=.02;actor.update(game,.02)
			if step*.02+.02<.4-.000001:source(tree,game,player)
		game.paused=true
		cases.append(await restore_pair(tree,game,player,"start-%.2f"%clock))
		tree.check(not cases[-1].normalMotionAccepted,"normal actor guard rejects staged active/pending start")
		if clock>=.4:tree.check(cases[-1].actor.south_start.pending,"unrendered gait distance seed survives real navigation packet")
	for phase in range(6):
		for clock in [.04,.18,.28,.36]:
			tree.stop_interruption_actor(game,cell,start,player,"curiosity",clock,phase);game.paused=true
			cases.append(await restore_pair(tree,game,player,"stop-%d-%.2f"%[phase,clock]))
			tree.check(not cases[-1].normalMotionAccepted,"normal actor guard rejects staged active stop")
			var actor=game.marsh_npc;var anchor: Vector2=actor.foot
			game.paused=false;var delta: float=.4-actor.south_stop_clock
			game.visual_time_seconds+=delta;actor.update(game,delta);game.paused=true
			tree.check(actor.arrival_callbacks==1 and actor.foot==anchor and not actor.south_stop_active(),"real restored ordinary stop finishes one callback at anchor")
		var actor=tree.stop_interruption_actor(game,cell,start,player,"curiosity",.18,phase)
		game.powered_room_cells.erase(cell);game.visual_time_seconds+=.02;actor.update(game,.02);game.paused=true
		tree.check(actor.south_stop_cancelled and actor.goal.is_empty(),"actual power loss creates cancelled packet with cleared goal")
		cases.append(await restore_pair(tree,game,player,"cancel-%d"%phase));actor=game.marsh_npc
		game.paused=false;var delta: float=.4-actor.south_stop_clock+.02
		game.visual_time_seconds+=delta;actor.update(game,delta);game.paused=true
		tree.check(actor.arrival_callbacks==0 and not actor.south_stop_active() and actor.choice_calls>=1,"restored cancelled service settles and invokes fresh chooser without old callback")
		game.powered_room_cells[cell]=true
		actor=tree.stop_interruption_actor(game,cell,start,player,"curiosity",.18,phase)
		game.visual_time_seconds+=.52;actor.update(game,.52);game.paused=true
		tree.check(actor.south_stop_idle_pending and actor.arrival_callbacks==1 and is_equal_approx(actor.south_stop_idle_elapsed,.3),"actual completion owns large-delta idle seed")
		cases.append(await restore_pair(tree,game,player,"idle-pending-%d"%phase))
		tree.check(not cases[-1].normalMotionAccepted and cases[-1].actor.south_stop.idle_pending,"normal guard rejects undrawn completion seed until admission")
		game.paused=false;game.visual_time_seconds+=.351;game.marsh_npc.update(game,.351);game.paused=true
		var idle: Texture2D=source(tree,game,player)
		tree.check(idle==player.frames["idle-south"][1],"restored completion advances actual650ms idle hold")
		cases.append(await restore_pair(tree,game,player,"idle-drawn-%d"%phase))
		tree.check(not cases[-1].actor.south_stop.idle_pending and game.marsh_npc.arrival_callbacks==0,"consumed idle handoff uses saved playback without callback replay")
	# Present topology is authoritative over valid serialized contact/route fields.
	for kind in ["start","stop"]:
		var actor=tree.stop_interruption_actor(game,cell,start,player,"curiosity",.18,4)
		if kind=="start":
			actor.foot=start;actor.state="idle";actor.clear_south_stop();actor.path=PackedVector2Array([start+Vector2(0,100)]);actor._arm_selected_route();actor.move(.18)
		var saved: Dictionary=actor.snapshot();tree.check(Stop.valid_south_snapshot(saved),"pre-removal actual snapshot validates")
		var room: Dictionary=game.occupied[cell];var index: int=game.placed_rooms.find(room)
		game.occupied.erase(cell);game.placed_rooms.remove_at(index)
		var restored=RestoredStop.new();game.marsh_npc=restored;restored.bind_south_stop_player(player)
		await restored.restore_snapshot(game,saved)
		tree.check(not restored.active and restored.path.is_empty() and not restored.south_active() and not restored.south_stop_active() and restored.arrival_callbacks==0,"real rebuilt removed-floor topology cancels serialized South motion without callback")
		tree.check(Stop.valid_south_snapshot(restored.snapshot()),"topology-invalidated actual actor serializes canonical inactive South fields")
		game.occupied[cell]=room;game.placed_rooms.insert(index,room)
	var file=FileAccess.open(tree.OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":tree.checks,"failures":tree.failures,"cases":cases.size(),"captures":tree.records,"casePackets":cases,"topologyCases":2,"scope":"Staged actual furnished-room actor fresh rebuild + saved player parity, Godot binary actor/player packet disk roundtrip (not RunSave checkpoint). Six starts including pending .4/.7s,24stops over6phases/4clocks,6actual power-loss cancellations,6completion idle seeds/residue,6drawn idle phases and2real removed-floor rebuilds. Pause/zero, first submitted source parity, delayed/no stale callback, normal unadmitted motion rejection. Normal paid/failure flags/world+peers paused between prescribed actor updates. No full fresh station/RunSave disk/titleContinue, normal admission, natural traffic or full-family art acceptance."},"\t"));file.close()
	print("MARSH SOUTH SNAPSHOT ACTUAL: %d checks,%d cases,%d captures,%d failures"%[tree.checks,cases.size(),tree.records.size(),tree.failures]);tree.quit(1 if tree.failures else 0)
