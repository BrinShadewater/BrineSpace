extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
var checks:=0
var failures:=0
func check(ok: bool,label: String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	var player=Player.new()
	player.load_manifest("res://character/bunk-contact-study-2026-09-21/veld-entry/manifest.json")
	for key in ["bunk-enter-east","bunk-exit-east"]:
		for i in range(7):
			var original: int=i if key=="bunk-enter-east" else 6-i
			check(bool(player.frames[key][i].get_meta("crew_bunk_layer",false))==(original>=4),key+" contact frame "+str(i))
	check(player.load_equipment_manifest("diving-helmet","res://character/bunk-contact-study-2026-09-21/veld-entry-helmet/manifest.json"),"Equipped bunk clips share bare timing and registration")
	for key in ["bunk-enter-east","bunk-exit-east"]:
		for i in range(7):
			check(player.equipment_frames["diving-helmet"][key][i].get_meta("crew_bunk_layer",false)==player.frames[key][i].get_meta("crew_bunk_layer",false),"Equipment keeps contact layer "+key+str(i))
	for t in [0.05,0.2,0.5,0.8,1.1,1.4,1.7]:
		var a=player.frame_at_elapsed("bunk-enter-east",t,"diving-helmet")
		var b=player.frame_at_elapsed("bunk-exit-east",1.84-t,"diving-helmet")
		check(a.get_image().get_data()==b.get_image().get_data(),"Equipped reverse pose matches entry")
	check(not player.frame_at_elapsed("bunk-enter-east",0.8).get_meta("crew_bunk_layer",false),"Hanging leg stays in front")
	check(player.frame_at_elapsed("bunk-enter-east",1.0).get_meta("crew_bunk_layer",false),"Boarded pose enters furniture")
	check(player.frame_at_elapsed("bunk-exit-east",0.1).get_meta("crew_bunk_layer",false),"Exit begins inside")
	check(not player.frame_at_elapsed("bunk-exit-east",1.0).get_meta("crew_bunk_layer",false),"Exit exposes hanging leg")
	check(Player.frame_furniture({"furniture":"bunk"},0)=="bunk","Whole-clip compatibility")
	check(Player.frame_furniture({},0)=="","Ordinary clips retain ordinary depth")
	check(Player.frame_furniture({"furniture":false},0)=="","Malformed whole-clip marker stays outside")
	var entry={"furniture":"bunk","frameFiles":["a","b"],"furnitureFrames":["","bunk"]}
	check(Player.frame_furniture(entry,0)=="","Explicit front overrides whole-clip marker")
	check(Player.frame_furniture(entry,1)=="bunk","Explicit interior override")
	for invalid in [null,"bunk",[],["bunk"],["bunk","bunk","bunk"]]:
		entry.furnitureFrames=invalid
		check(Player.frame_furniture(entry,0)=="","Malformed override cannot opt into interior depth")
	entry.furnitureFrames=["unknown",false]
	check(Player.frame_furniture(entry,0)=="" and Player.frame_furniture(entry,1)=="","Unknown markers do not opt in")
	entry.furnitureFrames=["bunk","bunk"]
	check(Player.frame_furniture(entry,-1)=="" and Player.frame_furniture(entry,2)=="","Invalid indices stay outside")
	print("SPRITE FURNITURE METADATA: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
