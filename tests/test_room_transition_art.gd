extends SceneTree
const Transitions=preload("res://scripts/room_transition_art.gd")
const Fronds=preload("res://scripts/ambient_fronds.gd")
const Settings=preload("res://scripts/title_settings.gd")
const Life=preload("res://scripts/ocean_life.gd")
var failures:=0
func check(value: bool,message: String):
	if not value:failures+=1;push_error(message)
func _initialize():
	Settings.effects_quality=1;Settings.reduced_motion=false
	var events:=Transitions.new()
	var room: Dictionary={"id":"corner","pos":Vector2i(1,1),"rotation":2}
	events.add("complete",room,1.0)
	room.rotation=0
	check(events.events[0].room.rotation==2,"Events must snapshot destination state")
	events.add("scrap",room,2.0)
	check(events.events.size()==1 and events.events[0].kind=="scrap","One visual per footprint origin")
	for i in range(20):
		room.pos=Vector2i(i,2);events.add("scrap",room,2.0)
	check(events.events.size()==16,"Cosmetic events are bounded")
	room.pos=Vector2i(2,3);events.add("complete",room,20.0)
	check(events.events.size()==1,"Expired visuals are discarded")
	events.add("complete",room,0.0)
	check(events.events.size()==1,"Clock reset discards stale run effects")
	check(Fronds.offset(1.0,2.0,3.0)==0,"Plant roots remain fixed")
	check(Fronds.offset(0.0,2.0,3.0)!=Fronds.offset(0.0,3.0,3.0),"Plant tips move with visual time")
	check(Fronds.offset(0.0,2.0,3.0)==Fronds.offset(0.0,2.0,3.0),"Frozen visual time is deterministic")
	var last: float=Life.swim_clock(0.0,3)
	for i in range(1,600):
		var next: float=Life.swim_clock(float(i)/60.0,3)
		check(next>last,"Swimming cadence never reverses authored frames");last=next
	Settings.reduced_motion=true
	check(Fronds.offset(0.0,2.0,3.0)==0,"Reduced Motion fixes vegetation")
	room.pos=Vector2i(5,5);events.add("scrap",room,0.0)
	check(events.events.size()==1,"Reduced Motion adds no transient")
	Settings.reduced_motion=false;Settings.effects_quality=0
	check(Fronds.offset(0.0,2.0,3.0)==0,"Low effects fixes vegetation")
	print("ROOM TRANSITIONS: 0 failures" if failures==0 else "ROOM TRANSITIONS: %d failures"%failures)
	quit(failures)
