extends SceneTree
const Motion = preload("res://scripts/james_construction_motion.gd")
const OUT := "res://character/james-construction-motion-v1/"
var checks := 0
var failures := 0
func check(ok: bool, why: String):
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init():call_deferred("run")
func run():
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(Motion.MANIFEST))
	var pixels:Dictionary={};var paths:=0
	for state in manifest.states:
		pixels[state.id]=[]
		for path in state.frameFiles:pixels[state.id].append(Image.load_from_file(path).get_data())
	for state in manifest.states:
		var facing:String=String(state.id).split("-")[-1]
		var neutral:PackedByteArray=pixels["torch-draw-"+facing][0]
		for i in range(state.frameFiles.size()):
			var exit:=Motion.exit_path(state.id,i);var reverse:=exit.duplicate(true);reverse.reverse();paths+=1
			check(pixels[exit.front()[0]][exit.front()[1]]==pixels[state.id][i],"Every arbitrary exit retains exact whole selected entry")
			check(pixels[exit.back()[0]][exit.back()[1]]==neutral,"Every arbitrary exit reaches exact whole idle seam")
			check(pixels[reverse.front()[0]][reverse.front()[1]]==neutral and pixels[reverse.back()[0]][reverse.back()[1]]==pixels[state.id][i],"Every arbitrary return reaches exact whole original work pose")
			for position in range(reverse.size()):
				var interrupted:=reverse.slice(0,position+1);interrupted.reverse()
				check(pixels[interrupted.front()[0]][interrupted.front()[1]]==pixels[reverse[position][0]][reverse[position][1]] and pixels[interrupted.back()[0]][interrupted.back()[1]]==neutral,"Every return reversal retains current whole pose and idle seam")
	# Exercise admission using a real saved motion, not invented actor state.
	var guard:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"continue-validation.json"))
	var path:String=String(guard.scratch).path_join("Godot/app_userdata/BrineSpace/james-construction-case0.loop")
	var saved:Dictionary=preload("res://scripts/run_save.gd").read(path)
	check(not saved.is_empty(),"Actual isolated interrupted disk checkpoint reads")
	if not saved.is_empty():
		var data:Dictionary=saved.crew.branforth
		check(Motion.valid(data),"Actual saved partial exit admissible")
		var bad:=data.duplicate(true);bad.branforth_construction_motion.sequence[0][2]+=1
		check(not Motion.valid(bad),"Changed pose clock rejected")
		bad=data.duplicate(true);bad.branforth_construction_motion.foot+=Vector2(1,0)
		check(not Motion.valid(bad),"Shifted interruption contact rejected")
		bad=data.duplicate(true);bad.branforth_construction_motion.elapsed=NAN
		check(not Motion.valid(bad),"Nonfinite interruption clock rejected")
		bad=data.duplicate(true);bad.branforth_construction_motion.index=999999
		check(not Motion.valid(bad),"Missing source index rejected")
		bad=data.duplicate(true);bad.branforth_construction_motion.sequence.reverse()
		check(not Motion.valid(bad),"Wrong direction of interrupted sequence rejected")
	for path_name in ["res://scripts/james_construction_motion.gd","res://character/james-construction-motion-v1/validate.gd","res://character/james-construction-motion-v1/north.gd","res://character/james-construction-motion-v1/east.gd","res://character/james-construction-motion-v1/south.gd","res://character/james-construction-motion-v1/west.gd","res://character/james-construction-motion-v1/continue.gd","res://character/james-construction-motion-v1/safety.gd","res://character/james-construction-motion-v1/source_paths.gd"]:
		if not FileAccess.file_exists(path_name+".uid"):
			var uid:=FileAccess.open(path_name+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var report:=FileAccess.open(OUT+"source-paths-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"arbitrarySourceEntries":paths,"scope":"Exact whole-RGBA entry/idle/reversed return/re-interrupted return seams for all348 selected bare torch source indices. Admission corruption checks use actual saved partial exit. Source-path algebra, not native gameplay coverage of all348 phases."},"  "))
	print("JAMES CONSTRUCTION SOURCE PATHS: ",checks," checks, ",paths," entries, ",failures," failures");quit(1 if failures else 0)
