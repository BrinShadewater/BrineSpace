extends SceneTree
const Motion=preload("res://scripts/james_construction_motion.gd")
const James=preload("res://scripts/branforth_npc.gd")
const Bill=preload("res://scripts/bill_npc.gd")
const Save=preload("res://scripts/run_save.gd")
const OUT:="res://character/james-construction-helmet-v1/"
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,why:String):
	checks+=1
	if not ok:failures+=1;push_error(why)
func run():
	var entries:=0
	for manifest_path in ["res://character/james-torch-material-residue-v2/bare-manifest.json","res://character/james-torch-material-residue-v2/helmet-manifest.json"]:
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path));var pixels:Dictionary={}
		for state in manifest.states:
			pixels[state.id]=[]
			check(state.frameDurationsMs==Motion.timings()[state.id],"Paired source recipe timing parity")
			for path in state.frameFiles:pixels[state.id].append(Image.load_from_file(path).get_data())
		for state in manifest.states:
			var facing:String=String(state.id).split("-")[-1];var neutral:PackedByteArray=pixels["torch-draw-"+facing][0]
			for i in range(state.frameFiles.size()):
				entries+=1;var exit:=Motion.exit_path(state.id,i);var reverse:=exit.duplicate(true);reverse.reverse()
				check(pixels[exit.front()[0]][exit.front()[1]]==pixels[state.id][i],"Exit starts at exact selected gear source")
				check(pixels[exit.back()[0]][exit.back()[1]]==neutral,"Exit reaches exact selected gear neutral")
				check(pixels[reverse.front()[0]][reverse.front()[1]]==neutral and pixels[reverse.back()[0]][reverse.back()[1]]==pixels[state.id][i],"Return reaches exact selected gear work source")
				for position in range(reverse.size()):
					var interrupted:=reverse.slice(0,position+1);interrupted.reverse()
					check(pixels[interrupted.front()[0]][interrupted.front()[1]]==pixels[reverse[position][0]][reverse[position][1]] and pixels[interrupted.back()[0]][interrupted.back()[1]]==neutral,"Repeated loss retains current whole pose and neutral seam")
	var guard:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"continue-validation.json"))
	var path:String=String(guard.scratch).path_join("Godot/app_userdata/BrineSpace/james-construction-case0.loop")
	var saved:Dictionary=Save.read(path);check(not saved.is_empty(),"Actual scratch interrupted disk checkpoint reads")
	if saved.is_empty():quit(2);return
	var data:Dictionary=saved.crew.branforth
	check(Motion.valid(data) and James.valid_branforth_snapshot(data),"Actual helmet partial exit admitted")
	var bad:=data.duplicate(true);bad.branforth_construction_motion.equipment=""
	check(not Motion.valid(bad),"Wrong saved equipment rejected")
	bad=data.duplicate(true);bad.branforth_construction_motion.erase("equipment")
	check(not Motion.valid(bad),"Missing equipment defaults bare and rejects helmet motion")
	bad.helmet_equipped=false
	check(Motion.valid(bad) and James.valid_branforth_snapshot(bad),"Prescribed legacy bare motion without equipment remains admitted")
	bad=data.duplicate(true);bad.branforth_construction_motion.sequence[0][2]+=1
	check(not Motion.valid(bad),"Changed canonical pose timing rejected")
	bad=data.duplicate(true);bad.branforth_construction_motion.foot+=Vector2(1,0)
	check(not Motion.valid(bad),"Shifted physical contact rejected")
	bad=data.duplicate(true);bad.branforth_construction_motion.elapsed=NAN
	check(not Motion.valid(bad),"Nonfinite motion time rejected")
	bad=data.duplicate(true);bad.branforth_construction_motion.index=99999
	check(not Motion.valid(bad),"Absent source index rejected")
	for direction in ["north","east","south","west"]:
		for goal in ["construction","hull-repair","ward-repair"]:
			var weld:Dictionary=data.duplicate(true);weld.branforth_construction_motion={};weld.direction=direction;weld.goal=goal;weld.state="weld"
			check(James.valid_branforth_snapshot(weld),"Explicit James helmet dry family admitted")
			check(not Bill.valid_snapshot(weld),"Default shared helmet weld rejection retained")
			weld.movement_medium="flooded"
			check(not James.valid_branforth_snapshot(weld),"Flooded standing weld rejected")
	for name in ["source_paths","bill_compat"]:
		if not FileAccess.file_exists(OUT+name+".gd.uid"):
			var uid:=FileAccess.open(OUT+name+".gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	var file:=FileAccess.open(OUT+"source-paths-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"arbitrarySourceEntries":entries,"scope":"All696 paired bare/helmet selected source indices: exact whole-RGBA exit/neutral/reentry/re-interruption algebra and paired timing parity. Corruption/family admission checks use actual helmet scratch partial-exit disk checkpoint; legacy bare case is a prescribed metadata conversion, not new bare physical Continue evidence. No all696 arbitrary native interruption coverage claim."},"  "));file.close()
	print("JAMES HELMET CONSTRUCTION SOURCE PATHS: ",checks," checks, ",entries," entries, ",failures," failures")
	quit(1 if failures else 0)
