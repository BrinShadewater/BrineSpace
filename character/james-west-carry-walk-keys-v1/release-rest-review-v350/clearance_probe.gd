extends SceneTree
const LIFE=preload("res://scripts/crew_life.gd")
const OUT="res://character/james-west-carry-walk-keys-v1/release-rest-review-v350/"
class JamesSpy:
	extends "res://scripts/james_cargo_actor.gd"
	var observed:Array=[]
	func swim_segment_clear(_a:Vector2,_b:Vector2,_facing:String,_previous:String="",_treading:bool=false,additional_extent:Array=[])->bool:
		observed=additional_extent.duplicate();return true
class BillSpy:
	extends "res://scripts/major_bill_npc.gd"
	var observed:Array=[]
	func swim_segment_clear(_a:Vector2,_b:Vector2,_facing:String,_previous:String="",_treading:bool=false,additional_extent:Array=[])->bool:
		observed=additional_extent.duplicate();return true
class VeldSpy:
	extends "res://scripts/veld_npc.gd"
	var observed:Array=[]
	func swim_segment_clear(_a:Vector2,_b:Vector2,_facing:String,_previous:String="",_treading:bool=false,additional_extent:Array=[])->bool:
		observed=additional_extent.duplicate();return true
var checks:=0
var failures:=0
func check(ok:bool,label:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init()->void:call_deferred("run")
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Isolated APPDATA")
	for row in [[JamesSpy.new(),"branforth"],[BillSpy.new(),"bill"],[VeldSpy.new(),"veld"]]:
		var npc=row[0];var id:String=row[1];npc.movement_medium="flooded"
		var expected:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(preload("res://scripts/crew_sprite_player.gd").REVISION_ROOTS[id]+"clearance.json")).life
		for gear in ["bare","helmet"]:
			npc.helmet_equipped=gear=="helmet"
			for direction in ["west","east","north","south"]:
				npc.direction=direction
				for action in ["swim-distress","cargo-turn"]:
					check(LIFE.clear(npc,action) and npc.observed==expected[gear][action+"-"+direction],"Inherited "+id+" actor receives its selected clearance outline")
				if id=="branforth":
					npc.tank_oxygen=12;npc.breath_oxygen=5
					check(LIFE.pose(npc)=="swim-distress" and npc.observed==expected[gear]["swim-distress-"+direction],"Actual low-air pose admission uses James outline")
	if not FileAccess.file_exists(OUT+"clearance_probe.gd.uid"):FileAccess.open(OUT+"clearance_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	print("JAMES LIFE CLEARANCE checks=",checks," failures=",failures)
	quit(1 if failures else 0)
