extends "res://character/james-ward-lifecycle-v1/validate.gd"
const Return=preload("res://scripts/james_hull_return.gd")
func run():
	await setup_job();var actor=game.branforth_npc
	for step in range(7000):
		game._process(1.0/60.0)
		if actor.ward_animation_active() and actor.timer>=3:break
	game._toggle_wreck_work(Vector2i(19,18));game._process(1.0/60.0)
	var row:Dictionary={"timer":actor.timer,"goal":actor.goal,"state":actor.state,"returning":Return.eligible(actor),"valid":Return.valid(actor.snapshot()),"pathSize":actor.path.size(),"stage":actor.stage}
	var file:=FileAccess.open(OUT+"pause-probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify(row,"  "));file.close()
	if not FileAccess.file_exists(OUT+"pause_probe.gd.uid"):
		var uid:=FileAccess.open(OUT+"pause_probe.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES WARD PAUSE PROBE: ",row);game.queue_free();quit(0)
