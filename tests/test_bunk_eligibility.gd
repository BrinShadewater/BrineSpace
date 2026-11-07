extends SceneTree
class World extends RefCounted:
	var bill_npc=preload("res://scripts/major_bill_npc.gd").new()
	var veld_npc=preload("res://scripts/veld_npc.gd").new()
	var branforth_npc=preload("res://scripts/branforth_npc.gd").new()
	var marsh_npc=preload("res://scripts/marsh_npc.gd").new()
var failures:=0
var checks:=0
func check(value: bool,label: String):
	checks+=1
	if not value:failures+=1;push_error(label)
func _init():
	var world=World.new();var actor=world.bill_npc;var peer=world.veld_npc
	var cell=Vector2i(1,1);var center=(Vector2(cell)+Vector2.ONE*0.5)*384
	peer.active=true;peer.foot=center;peer.needs.fatigue=100;actor.needs.fatigue=0
	peer.geometry[cell]={"activity_room":"crew_hab","bunk_actor":"veld","blockers":[],"props":[{"id":"library/tileset-mb2-14","rect":Rect2(72,-126,72.46131,73.99651)}]}
	var station=actor.RoomActivity.stations(peer.geometry[cell])[0]
	peer.graph.add_point(0,peer.foot);peer.graph.add_point(1,center+station.point);peer.room_nodes[cell]=[0,1]
	check(not actor.bunk_claimed(world,cell,station),"Disconnected peer cannot hold bunk")
	peer.graph.connect_points(0,1)
	check(actor.bunk_claimed(world,cell,station),"Connected tired peer receives priority")
	peer.fire_cells[cell]=true
	check(not actor.bunk_claimed(world,cell,station),"Burning destination is not an eligible route")
	peer.fire_cells.clear();peer.active=false
	check(not actor.bunk_claimed(world,cell,station),"Inactive peer ignored")
	peer.active=true;peer.dead=true
	check(not actor.bunk_claimed(world,cell,station),"Dead peer ignored")
	peer.dead=false;peer.goal="recharge"
	check(not actor.bunk_claimed(world,cell,station),"Charging peer ignored")
	peer.goal="";peer.foot=center+Vector2(384*4,0)
	check(not actor.bunk_claimed(world,cell,station),"Distant peer ignored")
	peer.foot=center;peer.needs.fatigue=60
	check(not actor.bunk_claimed(world,cell,station),"Nonurgent fatigue does not claim bed")
	peer.needs.fatigue=100;actor.needs.fatigue=98
	check(not actor.bunk_claimed(world,cell,station),"Near-equal needs do not deadlock")
	actor.needs.fatigue=0;peer.path=PackedVector2Array([center+station.point]);peer.goal_cell=cell;peer.goal="fatigue"
	peer.needs.fatigue=0
	check(actor.bunk_claimed(world,cell,station),"Existing route retains its claim")
	peer.path.clear();peer.stage="life_get_up";peer.foot=center+station.point
	check(actor.bunk_claimed(world,cell,station),"Rising occupant retains its claim")
	peer.stage="";peer.goal=""
	check(not actor.bunk_claimed(world,cell,station),"Finished activity releases its claim")
	print("BUNK ELIGIBILITY: ",checks," checks, ",failures," failures")
	quit(failures)
