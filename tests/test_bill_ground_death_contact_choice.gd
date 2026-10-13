extends SceneTree
const BILL=preload("res://scripts/bill_npc.gd")
const DEATH=preload("res://scripts/bill_ground_death.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	print("BILL GROUND CONTACT CHOICE profile: "+OS.get_user_data_dir())
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations();var player=grid.human_water_player
	player.load_manifest("res://character/bill-death-ground-contact-family-v1/manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/bill-death-ground-contact-family-v1/helmet-manifest.json"),"Paired candidates")
	var actor=BILL.new();actor.foot=Vector2(192,192);actor.state="idle"
	for gear in [false,true]:
		var clips:Dictionary=player.equipment_frames["diving-helmet"] if gear else player.frames
		for direction in ["north","south"]:
			actor.direction=direction;actor.helmet_equipped=gear
			var key:String="death-ground-"+direction
			actor.geometry[Vector2i.ZERO]={"props":[]}
			check(not DEATH._choose_lateral(actor,clips,key),"Open floor retains original")
			actor.geometry[Vector2i.ZERO].props=[{"rect":Rect2(-40,-40,100,20)}]
			check(DEATH._choose_lateral(actor,clips,key),"Blocked original with clear lateral settled poses")
			DEATH.prepare(actor,{"grid_view":grid})
			check(actor.death_ground_variant=="lateral" and actor.death_entry_seconds==0,"Upright caller can choose lateral without lowered prefix")
			var missing:Dictionary=clips.duplicate();missing.erase("death-ground-lateral-"+direction)
			check(not DEATH._choose_lateral(actor,missing,key),"Missing alternative retains original")
			actor.geometry[Vector2i.ZERO].props.append({"rect":Rect2(-40,-15,100,30)})
			check(not DEATH._choose_lateral(actor,clips,key),"Blocked lateral settled poses reject alternative")
			actor.geometry.clear();check(not DEATH._choose_lateral(actor,clips,key),"Unknown geometry retains original")
	grid.free();print("BILL GROUND CONTACT CHOICE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
