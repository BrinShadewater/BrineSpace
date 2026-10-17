from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent
guard=json.loads((P/'native-workshop-validation.json').read_bytes());source=Path(guard['scratch'])/'Godot/app_userdata/BrineSpace/james-workshop.loop';shutil.copy2(source,P/'workshop-completion-scratch.loop')
prefix=(P/'native-workshop.gd').read_text().split('func run() -> void:')[0]
body='''func run() -> void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(3);return
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://completion.meta";game.run_save_path="user://completion.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	var save=preload("res://scripts/run_save.gd");var data:Dictionary=save.read(OUT+"workshop-completion-scratch.loop")
	check(await save.restore_staged(game,data),"Actual last scratch checkpoint restore")
	game.run_save_path="user://completion.loop";game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
	var npc=game.branforth_npc
	game.hand_panel.hide();game.card_drag.hide();game.paused=false
	var before:Dictionary=npc.snapshot();var curiosity_before:float=npc.needs.curiosity
	print("JAMES COMPLETION BEFORE: ",npc.stage," goal",npc.goal," curiosity",curiosity_before," timer",npc.timer)
	await capture("completion-clean-000",npc)
	for i in range(100):
		npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
		if npc.stage!="workshop_unload":break
	var after:Dictionary=npc.snapshot()
	print("JAMES COMPLETION AFTER: ",npc.stage," goal",npc.goal," curiosity",npc.needs.curiosity," path",npc.path.size()," activity",npc.activity)
	var f:=FileAccess.open(OUT+"completion-probe-evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"beforeStage":before.stage,"beforeGoal":before.goal,"curiosityBefore":curiosity_before,"afterStage":after.stage,"afterGoal":after.goal,"curiosityAfter":npc.needs.curiosity,"pathSize":npc.path.size(),"activity":npc.activity,"scope":"Actual final helmet unload checkpoint from scratch, fresh-main restore and observed completion with card tray hidden for capture. Diagnostic, not original two-case acceptance."},"  "))
	if not FileAccess.file_exists(OUT+"completion-probe.gd.uid"):
		f=FileAccess.open(OUT+"completion-probe.gd.uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES COMPLETION PROBE: ",checks,"checks; ",failures,"failures")
	quit(1 if failures else 0)
'''
(P/'completion-probe.gd').write_text(prefix+body)
