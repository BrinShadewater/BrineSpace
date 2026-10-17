extends SceneTree
class Original extends RefCounted:
	static var catalog:Dictionary={}
	static var room_assets:Dictionary={}
	static func style_override(room_id:String, quarter:int) -> String:
		if catalog.is_empty():catalog=JSON.parse_string(FileAccess.get_file_as_string("res://assets/architecture-rollout-2026-09-26/doors.json"))
		if room_assets.is_empty():
			for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json")): room_assets[str(entry.room)]=str(entry.asset)
		var style=load("res://scripts/room_layout_store.gd").shared_positions(str(room_assets.get(room_id,"room-"+room_id)),quarter).get("door/style","")
		return str(style) if style is String and catalog.styles.has(style) else ""

const Candidate=preload("res://rooms/doors/painted_door.gd")
const Store=preload("res://scripts/room_layout_store.gd")
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	Store.loaded=true;Store.defaults_path="user://missing-defaults.json";Store.data={}
	# Load real catalog mappings before varying isolated layout state.
	Original.style_override("reactor",0);Candidate.style_override("reactor",0)
	var ids:Array=Original.room_assets.keys();ids.append("unknown-room")
	for reuse in [false,true]:
		Store.reuse_layout_store=reuse
		for room in ids:
			for q in [-1,0,1,2,3,4]:
				var key:String=Store.key(str(Original.room_assets.get(room,"room-"+room)),q)
				for style in Original.catalog.styles.keys()+["", "not-a-style", 7, null]:
					Store.data={key:{"door/style":style}};Store.revision+=1
					check(Original.style_override(room,q)==Candidate.style_override(room,q),"Style lookup exact")
	var room:String="reactor";var key:String=Store.key(str(Original.room_assets.get(room,"room-"+room)),0)
	Store.reuse_layout_store=true;Store.data={key:{"door/style":"default"}};Store.revision+=1
	check(Candidate.style_override(room,0)=="default","Current explicit style visible")
	Store.data={key:{"door/style":"not-a-style"}}
	check(Candidate.style_override(room,0)=="","Wholesale data replacement observed without revision")
	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("DOOR_STYLE ",checks," checks, ",failures," failures");quit(1 if failures else 0)
