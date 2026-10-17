extends SceneTree
## Actual manifest loader, gait fractions, pause/Continue and per-pose registration.
var failures:=0
var checks:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	var Player=load("res://scripts/crew_sprite_player.gd")
	var p=Player.new()
	var catalog:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-v2/catalog.json"))
	for path in catalog.body:p.load_manifest("res://character/marsh-v2/"+str(path),true)
	for direction in ["south","north","east","west"]:
		for sample in range(24):
			for action in ["walk","run"]:
				var next: String="run" if action=="walk" else "walk"
				p.current_key="";p.last_time=-1;p.motion.clear()
				p.frame(action,direction,1,Vector2.ZERO)
				var fraction:=float(sample)/24
				p.phase=fraction*p.cycle_seconds(action+"-"+direction)
				p.frame(next,direction,1.01,Vector2.ZERO)
				check(is_equal_approx(p.phase/p.cycle_seconds(next+"-"+direction),fraction),"Speed switch preserves gait "+direction+str(sample))
				var saved:Dictionary=p.snapshot()
				check(p.valid_snapshot(saved),"Gait checkpoint valid")
				p.phase=0;p.restore_snapshot(saved)
				p.frame(next,direction,1.01,Vector2.ZERO)
				check(is_equal_approx(p.phase,saved.phase),"Continue and pause preserve gait")
				p.frame(next,direction,1.02,Vector2.ONE)
				check(p.phase==0,"Teleport resets gait")
				p.phase=.2;p.frame("idle",direction,1.03,Vector2.ONE)
				check(p.phase==0,"Action resets gait")
	# Independent actors do not inherit the Marsh-only opt-in.
	for actor in ["bill","veld","branforth"]:
		var player=Player.new()
		var base:String=Player.REVISION_ROOTS[actor]
		var other:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(base+"catalog.json"))
		for path in other.body:player.load_manifest(base+str(path),true)
		check(player.gait_phase_groups.is_empty(),"Other actor has no Marsh gait group")
	var plain=load("res://scripts/crew_sprite_player.gd").new()
	plain.frames=p.frames;plain.timing=p.timing;plain.strides=p.strides
	plain.frame("walk","east",1,Vector2.ZERO);plain.phase=.35
	plain.frame("run","east",1.01,Vector2.ZERO)
	check(plain.phase==0,"Actor without opt-in retains speed-switch reset")
	for key in p.frames:
		var elapsed:=0.0
		var length:float=p.cycle_seconds(key)
		while elapsed<length*2:
			var cursor:float=fposmod(elapsed,length) if p.timing[key].loop else minf(elapsed,length)
			var slot:=0
			while slot<p.frames[key].size()-1 and cursor>=float(p.timing[key].durations[slot])/1000:
				cursor-=float(p.timing[key].durations[slot])/1000;slot+=1
			p.current_key=key;p.last_time=1;p.last_position=Vector2.ZERO;p.phase=elapsed;p.motion.clear()
			var split:int=key.rfind("-")
			var action:String=key.substr(0,split);var direction:String=key.substr(split+1)
			check(p.frame(action,direction,1,Vector2.ZERO)==p.frames[key][slot],"Continuous playback "+key)
			elapsed+=1.0/60
	var spec:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-consistency-review-v1/runtime-contract.json"))
	var tread:Array=spec.states["tread-north"].files
	for slot in range(tread.size()):
		var path:String=tread[slot]
		var im:=Image.new();check(im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+path))==OK,"Tread source decoded")
		check(p.frames["tread-north"][slot].get_image().get_data()==im.get_data(),"Current tread source loaded")
		check(p.frames["tread-north"][slot].get_meta("crew_standing_height")==148,"Density calibrated")
	print("MARSH QUALITY V2: %d checks, %d failures"%[checks,failures]);quit(1 if failures else 0)
