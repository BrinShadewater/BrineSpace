extends SceneTree
const Effects=preload("res://scripts/station_effects.gd")
var checks:=0
var failures:=0
class Actor extends RefCounted:
	var direction:="south"
func check(ok:bool,why:String):
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init():call_deferred("run")
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	var bill:=Actor.new();var james:=Actor.new();var peer:=Actor.new()
	var game:Dictionary={"bill_npc":bill,"branforth_npc":james}
	var selected:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-torch-actions-v1/torch-tip-offsets.json"))
	for direction in ["north","east","south","west"]:
		bill.direction=direction;peer.direction=direction
		check(Effects.torch_tip_offset(game,bill)==Vector2(selected[direction][0],selected[direction][1]),"Bill measured contact unchanged")
		check(Effects.torch_tip_offset(game,peer)==Effects.TORCH_TIPS[direction],"Other actor fallback unchanged")
	for path:String in ["res://character/james-repair-contact-v1/validate.gd","res://character/james-repair-contact-v1/compatibility.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var uid:=FileAccess.open(path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	var file:=FileAccess.open("res://character/james-repair-contact-v1/compatibility-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"Four Bill measured contacts and other-actor generic fallback unchanged; source/helper UID pairing."},"  "));file.close()
	print("JAMES REPAIR CONTACT COMPATIBILITY: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
