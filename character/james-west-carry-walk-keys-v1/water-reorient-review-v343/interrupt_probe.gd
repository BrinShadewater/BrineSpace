extends SceneTree
const OUT="res://character/james-west-carry-walk-keys-v1/water-reorient-review-v343/"
const Player=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/reorient_player.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:
	if a==null or b==null:return false
	var aa:Texture2D=a.diffuse_texture if a is CanvasTexture else a
	var bb:Texture2D=b.diffuse_texture if b is CanvasTexture else b
	return aa.get_image().get_data()==bb.get_image().get_data()
func clone(normal):
	var player=Player.new()
	for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides"]:player.set(field,normal.get(field).duplicate(true))
	player.install_bridges();return player
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	if failures:quit(2);return
	var grid=preload("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
	var player=clone(grid.branforth_player);var fresh=clone(grid.branforth_player)
	var samples:=0
	for gear in ["","diving-helmet"]:
		var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
		var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
		for direction in ["east","south","west","north"]:
			for phase in range(1,5):
				var key:String="swim-stop-phase-"+str(phase)+"-"+direction
				var cumulative:=0.0
				for slot in range(bank[key].size()):
					var elapsed:float=cumulative+float(clocks[key].durations[slot])/2000.0
					player.restore_snapshot({"key":"swim-"+direction,"equipment":gear,"phase":0.0,"last_time":9.9,"started":9.0,"last_position":Vector2.ZERO,"motion":{"state":"tread","direction":direction,"clip":key,"started":10.0}})
					var time:float=10.0+elapsed
					var before:Texture2D=player.frame("tread",direction,time,Vector2.ZERO,gear,true)
					check(same(before,bank[key][slot]),"Bridge clock samples authored row")
					check(same(before,player.frame("tread",direction,time,Vector2.ZERO,gear,true)),"Paused clock holds source pose")
					var saved:Dictionary=player.snapshot();fresh.restore_snapshot(saved)
					check(same(before,fresh.frame("tread",direction,time,Vector2.ZERO,gear,true)),"Fresh staged player restores exact bridge pose")
					fresh.restore_snapshot(saved)
					check(same(before,fresh.frame("swim",direction,time+.001,Vector2(.02,0),gear,true)),"Restart entry does not replay transition travel")
					var restart:Texture2D=player.frame("swim",direction,time,Vector2.ZERO,gear,true)
					check(same(before,restart),"Restart preserves current stop pose "+direction+str(phase)+":"+str(slot)+gear)
					var restarting:String=player.motion.clip
					if restarting.begins_with("swim-restart-phase-"):
						var restart_saved:Dictionary=player.snapshot();fresh.restore_snapshot(restart_saved)
						check(same(restart,fresh.frame("swim",direction,time,Vector2.ZERO,gear,true)),"Fresh restore preserves restart entry")
						check(same(restart,player.frame("tread",direction,time,Vector2.ZERO,gear,true)),"Stopping interrupted restart retains pose")
						fresh.restore_snapshot(restart_saved)
						check(same(fresh.frame("swim",direction,time+fresh.cycle_seconds(restarting,gear)+.001,Vector2.ZERO,gear,true),bank["swim-"+direction][0]),"Restart completes at neutral swim zero")
					player.restore_snapshot(saved)
					check(same(player.frame("tread",direction,10.0+player.cycle_seconds(key,gear)+.001,Vector2.ZERO,gear,true),bank["tread-"+direction][0]),"Stop finishes at authored tread zero")
					var extent:Array=player.clip_extent(key,gear)
					check(not extent.is_empty(),"Full bridge collision extent available")
					cumulative+=float(clocks[key].durations[slot])/1000.0;samples+=1
	if not FileAccess.file_exists(OUT+"interrupt_probe.gd.uid"):
		var uidfile=FileAccess.open(OUT+"interrupt_probe.gd.uid",FileAccess.WRITE)
		uidfile.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");uidfile.close()
	FileAccess.open(OUT+"interrupt-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"normalChanged":false,"scope":"Staged source playback holds, all bridge poses/restarts/re-interruptions and independent fresh player restore. Clearance metadata availability only; not an actor collision route or whole-run Continue."},"\t"))
	grid.free();print("JAMES STAGED WATER INTERRUPT checks=",checks," failures=",failures," samples=",samples);quit(0 if failures==0 else 1)
