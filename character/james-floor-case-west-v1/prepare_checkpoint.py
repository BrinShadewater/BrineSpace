from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
source=(p/'priority.gd').read_text()
prefix=source[:source.index('\tvar original_rooms:Array=')]
prefix=prefix.replace('const FLOOR=','const CHECKPOINT=preload("res://character/james-floor-case-west-v1/checkpoint.gd")\nconst SAVE=preload("res://scripts/run_save.gd")\nconst FLOOR=')
helper='''func install_candidate()->Dictionary:
	var baseline=game.grid_view.branforth_player
	var candidate=preload("res://character/james-floor-case-west-v1/floor_player.gd").new()
	for key in ["frames","timing","strides","gait_phase_groups","equipment_frames","equipment_timing","equipment_strides"]:candidate.set(key,baseline.get(key).duplicate(true))
	candidate.load_manifest("res://character/james-cargo-return-bridges-v1/bare-joined-manifest-v9.json",true)
	check(candidate.load_equipment_manifest("diving-helmet","res://character/james-cargo-return-bridges-v1/helmet-joined-manifest-v9.json"),"Fresh paired source bank")
	game.grid_view.branforth_player=candidate
	var view=preload("res://character/james-floor-case-west-v1/release_workshop.gd").new()
	view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
	candidate.preview_game=game;candidate.preview_view=view;candidate.preview_cell=ORIGIN
	return {"player":candidate,"view":view}
'''
prefix=prefix.replace('func run() -> void:',helper+'func run() -> void:')
setup=source[source.index('\t\t\t\tgame.occupied.clear()'):source.index('\t\t\t\tvar release:float=')]
setup=setup.replace('\t\t\t\t','\t\t\t')
setup=setup.replace('mode+phase+hazard','mode+phase')
tail='''	var original_rooms:Array=game.placed_rooms.duplicate(true)
	for mode in ["bare","helmet"]:
		for phase in ["before","after","idle"]:
'''+setup+'''			var release:float=FLOOR.release_time(player)
			check(not player.return_plan.is_empty() and is_finite(release),"Actual return before checkpoint")
			if failures:quit(1);return
			var until:float=player.return_plan.until
			while game.visual_time_seconds<release-.03:
				npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			if phase!="before":
				game.visual_time_seconds=release+.001;npc.update(game,.02);game.grid_view._get_branforth_frame(game)
			if phase=="idle":
				game.visual_time_seconds=until+.001;npc.update(game,.02);game.grid_view._get_branforth_frame(game)
			var label:String=mode+"-checkpoint-"+phase
			var initial:Texture2D=game.grid_view._get_branforth_frame(game)
			var expected_plan:Dictionary=player.return_plan.duplicate(true)
			var expected_room:Dictionary=FLOOR.payload(game.occupied[ORIGIN]).duplicate(true)
			var foot:Vector2=npc.foot;var clock:float=game.visual_time_seconds
			var packet:Dictionary=CHECKPOINT.capture(game)
			check(CHECKPOINT.admits_loaded(packet,player),"Strict paired candidate admission")
			check(not SAVE.problem(packet).is_empty(),"Ordinary loader rejects unadmitted candidate marker")
			var bad:Dictionary=packet.duplicate(true);bad[CHECKPOINT.FIELD].binding="other"
			check(not CHECKPOINT.valid_shape(bad),"Reject wrong binding")
			bad=packet.duplicate(true);bad[CHECKPOINT.FIELD].version=1.0
			check(not CHECKPOINT.valid_shape(bad),"Reject wrong version type")
			bad=packet.duplicate(true);bad.crew.branforth.stage=""
			check(not CHECKPOINT.valid_shape(bad),"Reject missing admission marker")
			if phase!="idle":
				bad=packet.duplicate(true);bad[CHECKPOINT.FIELD].plan.rows[0].seconds=.09
				check(not CHECKPOINT.admits_loaded(bad,player),"Reject altered plan clock")
				bad=packet.duplicate(true);bad[CHECKPOINT.FIELD].sourceBindings[0].rgba="0".repeat(64)
				check(not CHECKPOINT.admits_loaded(bad,player),"Reject altered original/candidate pixels")
				bad=packet.duplicate(true);bad[CHECKPOINT.FIELD].plan.floorFoot+=Vector2(1,0)
				check(not CHECKPOINT.admits_loaded(bad,player),"Reject actor-floor mismatch")
				bad=packet.duplicate(true);bad.state.visual_time_seconds=until
				check(not CHECKPOINT.valid_shape(bad),"Reject expired finite plan")
				if phase=="after":
					bad=packet.duplicate(true)
					for room in bad.state.placed_rooms:room.erase(FLOOR.FIELD)
					check(not CHECKPOINT.admits_loaded(bad,player),"Released plan requires owned room payload")
			check(SAVE.problem(CHECKPOINT.base_packet(packet)).is_empty(),"Base station/legacy schema retained")
			var path:String="user://"+label+".save"
			check(CHECKPOINT.write(game,path)==OK,"Candidate disk write")
			var loaded:Dictionary=CHECKPOINT.read(path)
			check(not loaded.is_empty() and CHECKPOINT.admits_loaded(loaded,player),"Candidate actual disk read/paired validation")
			if failures:quit(1);return
			await record_case(view,npc,label+"-saved")
			var previous=game
			game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
			game.meta.save_path="user://james-checkpoint.meta";game.run_save_path="user://james-checkpoint.loop"
			root.add_child(game);current_scene=game
			while not game.startup_complete:await process_frame
			game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
			var installed:Dictionary=install_candidate();player=installed.player;view=installed.view
			check(await CHECKPOINT.restore_staged(game,loaded),"Fresh main candidate paired staged restore")
			previous.queue_free();await process_frame
			game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
			npc=game.branforth_npc
			check(game.paused and game.visual_time_seconds==clock,"Fresh resume paused at exact clock")
			check(npc.foot==foot and player.return_plan==expected_plan,"Fresh actor contact/finite plan exact")
			check(FLOOR.payload(game.occupied[ORIGIN])==expected_room,"Fresh room ownership/anchor exact")
			var restored:Texture2D=game.grid_view._get_branforth_frame(game)
			check(restored.get_size()==initial.get_size() and restored.get_image().get_data()==initial.get_image().get_data(),"Immediate resumed source whole RGBA exact")
			await record_case(view,npc,label+"-restored")
			game.paused=false
			for tick in range(200):
				npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
				if player.return_plan.is_empty():break
			check(player.return_plan.is_empty() and not FLOOR.payload(game.occupied[ORIGIN]).is_empty(),"Restored finite sequence completes with room-owned case")
			await record_case(view,npc,label+"-completed")
			results.append({"checkpoint":true,"mode":mode,"phase":phase,"clock":clock,"disk":path,"sourceExact":true,"floorRestored":true,"completed":true})
			print("JAMES FLOOR CHECKPOINT ",mode," ",phase," failures=",failures)
			if failures:quit(1);return
	for name in ["checkpoint.gd","checkpoint_probe.gd"]:
		if not FileAccess.file_exists(OUT+name+".uid"):
			var uid:=FileAccess.open(OUT+name+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var f:=FileAccess.open(OUT+"checkpoint_probe-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Six actual carry returns/both gears/before release, after release, idle. Staged paired candidate disk codec with normal station capture/base validation and actual SAVE.restore_staged in fresh main, then fixture actor/player/renderer restore.18native source/room pairs. Ordinary loader rejects marker; no normal title/new-process Continue admission, full future trajectory, normal selection or other cardinal acceptance."},"  "))
	print("JAMES FLOOR CHECKPOINT: ",checks,"checks; ",failures,"failures;6cases;18presentations")
	quit(1 if failures else 0)
'''
(p/'checkpoint_probe.gd').write_text(prefix+tail)
prior=json.loads((p/'priority-inputs.json').read_bytes())
paths=[r/k for k in prior if Path(k).name!='priority.gd']+[p/'checkpoint.gd',p/'checkpoint_probe.gd',r/'scripts/run_save.gd',r/'scripts/bill_npc.gd']
(p/'checkpoint_probe-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Six paired staged disk/fresh-main cases prepared;'+str(len(paths))+' targeted inputs frozen.')
