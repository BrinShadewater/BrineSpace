"""Build independent full-save/visible-Continue gate using the normal catalogue."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/review_marsh_cargo_delivery02_actor.gd').read_text()
source=source[:source.index('\tplayer.load_manifest(')]
source=source.replace('cargo-delivery-02-2026-10-02','cargo-arrival-save-01-2026-10-02')
source=source.replace('var samples: Array = []','var samples: Array = []\nvar checkpoints:Array=[]\nconst Save=preload("res://scripts/run_save.gd")')
helper='''
func quiet():
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()

func clear_loading() -> bool:
	var overlay=null
	for child in root.get_children():
		if child.get_script()==Loading:overlay=child;break
	if overlay==null:return false
	var deadline=Time.get_ticks_msec()+20000
	while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
	if overlay.continue_button.disabled:return false
	overlay.continue_button.pressed.emit()
	while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
	return not is_instance_valid(overlay)

'''
source=source.replace('func run():',helper+'func run():')
source+='''
	for spec in [{"origin":"east","elapsed":.2},{"origin":"west","elapsed":.2},{"origin":"south","elapsed":.4},{"origin":"west","elapsed":1.0}]:
		game.marsh_npc=Normal.new();actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction=spec.origin;actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=cell;actor.path=PackedVector2Array()
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		actor.arrive();game.paused=false;actor.update(game,spec.elapsed);game.paused=true
		player.current_key="";player.motion={}
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		var presentation:Dictionary=actor.workshop_arrival_presentation(player)
		check(not presentation.is_empty() and actor.workshop_arrival_origin==spec.origin,"actual arrival origin retained")
		var label:String=spec.origin+"-"+str(spec.elapsed)
		var disk:String="user://cargo-arrival-"+label+".loop"
		check(Save.write(game,disk)==OK,"full checkpoint write "+label+": "+Save.last_error)
		var data:Dictionary=Save.read(disk)
		check(not data.is_empty() and data.crew.marsh.workshop_arrival_origin==spec.origin,"full checkpoint read validates arrival "+label)
		await capture(label,-1)
		checkpoints.append({"label":label,"disk":disk,"actor":actor.snapshot(),"player":player.snapshot(),"pixels":texture.get_image().get_data(),"position":game.get_marsh_position(),"presentation":presentation})
	current_scene=null;game.queue_free();await process_frame
	var cases:Array=[]
	for item in checkpoints:
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=item.disk;title._continue_loop()
		deadline=Time.get_ticks_msec()+120000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		game=current_scene
		check(game!=title and game.get("startup_complete")==true,"fresh Title Continue startup "+item.label)
		if game==title or not game.get("startup_complete"):quit(1);return
		game.run_save_path="user://cargo-arrival-continued-scratch.loop";quiet()
		check(await clear_loading(),"actual visible Continue overlay dismissed "+item.label);quiet()
		actor=game.marsh_npc;player=game.grid_view.marsh_player
		check(actor.get_script()==Normal and game.running and game.paused,"normal paused factory restored")
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		check(actor.snapshot()==item.actor,"whole actor first draw parity "+item.label)
		check(player.snapshot()==item.player,"whole player first draw parity "+item.label)
		check(texture.get_image().get_data()==item.pixels,"normal catalogue exact first restored source "+item.label)
		check(game.get_marsh_position().is_equal_approx(item.position),"first restored root/draw position")
		check(actor.workshop_arrival_presentation(player)==item.presentation,"arrival derived clock parity")
		actor.update(game,.5);check(actor.snapshot()==item.actor and game.grid_view._get_marsh_frame(game)==texture,"pause holds restored arrival")
		game.hand_panel.hide();check(await settle_camera(camera),"restored camera/layers settled")
		await capture(item.label,-1)
		var timer_before:float=actor.timer;var foot_before:Vector2=actor.foot
		game.paused=false;actor.update(game,.02);game.paused=true
		check(is_equal_approx(actor.timer,timer_before-.02) and actor.foot==foot_before,"unpaused arrival resumes clock at fixed root")
		check(Normal.valid_marsh_snapshot(actor.snapshot()),"continued arrival validates")
		cases.append({"label":item.label,"presentation":item.presentation,"fullSave":true,"freshVisibleTitleContinue":true})
		current_scene=null;game.queue_free();await process_frame
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"scope":"Four full checkpoints and four fresh actual visible TitleContinues, current normal catalogue with no injected art. Seeded actual arrive then normal update; whole actor/player/source/root/pause/resume parity. Not staged family persistence, complete routes, helmet acceptance or full-set artwork acceptance."},"\\t"));file.close()
	print("MARSH ARRIVAL SAVES: ",checks,"checks,",failures,"failures")
	quit(1 if failures else 0)
'''
target=ROOT/'tools/review_marsh_cargo_arrival_save01_actor.gd';target.write_text(source)
target.with_suffix('.gd.uid').write_text('uid://du8cargoarrsav12\n')
fpr=(ROOT/'tools/fingerprint_marsh_cargo_arrival_branches01.py').read_text().replace('arrival_branches01','arrival_save01')
(ROOT/'tools/fingerprint_marsh_cargo_arrival_save01.py').write_text(fpr)
print('Prepared normal-catalogue full checkpoint/actual visible Continue gate; no art injection.')
