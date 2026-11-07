extends SceneTree
const Activity=preload("res://scripts/crew_room_activity.gd")
func _init():
	var path="res://tests/test_lounge_seat_contacts.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run():
	assert(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"))
	var sofa={"id":"lounge_sofa","rect":Rect2(90,66,75,75),"sort_y":141.0}
	var data={"activity_room":"crew_lounge","props":[sofa],"blockers":[Rect2(90,66,75,75).grow(12),Rect2(-192,167,384,25)]}
	var s:Dictionary=Activity.stations(data)[0]
	assert(s.point==Vector2(127.5,165) and s.rest_point==Vector2(127.5,133),"Nearest clear front replaces blocked wall gap")
	assert(s.exact_approach and s.service_limit==165 and s.seat_depth==141.01,"Exact registered approach/depth expands only service search")
	assert(not Activity._approach_blocked(data,s.point),"Collision remains authoritative")
	var old_contact:=Vector2(64,96)
	assert(Activity.at(data,old_contact).is_empty(),"Old side contact is not offered for new visits")
	var retained:Dictionary=Activity.seated_contact(data,old_contact)
	assert(retained.rest_point==Vector2(127.5,133) and retained.seat_depth==141.01,"Existing seated checkpoint re-resolves its chair")
	var actor=load("res://scripts/veld_npc.gd").new()
	actor.active=true;actor.goal_cell=Vector2i(20,21);actor.geometry[actor.goal_cell]=data
	actor.foot=(Vector2(actor.goal_cell)+Vector2.ONE*.5)*384+old_contact
	actor.stage="life_seated";actor.timer=7.4;actor.goal="fatigue"
	var life=preload("res://scripts/crew_life.gd")
	assert(life.offset(actor)==Vector2(63.5,37),"Old seated contact offset remains exact until exit")
	var marked=ImageTexture.create_from_image(Image.create(1,1,false,Image.FORMAT_RGBA8));marked.set_meta("crew_seat_contact_depth",true)
	assert(is_equal_approx(life.seated_draw_depth(actor,marked,Vector2(127.5,133)),141.01),"Old seated draw depth retained")
	data.blockers=[Rect2(90,66,75,75).grow(12)]
	assert(Activity.stations(data)[0].point==Vector2(127.5,169),"Clear original front remains unchanged")
	data.blockers.append(Rect2(124,150,7,30))
	var fallback:Dictionary=Activity.stations(data)[0]
	assert(not fallback.get("exact_approach",false) and fallback.point.x!=fallback.rest_point.x,"Fully blocked front retains side fallback, distinct unresolved motion context")
	assert(not Activity._approach_blocked(data,fallback.point),"Fallback remains clear")
	print("LOUNGE SEAT CONTACTS: 11 assertions,0 failures");quit(0)
