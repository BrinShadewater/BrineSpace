extends Node2D
const Moon=preload("res://rooms/large-rooms/moonbay.gd")
const Settings=preload("res://scripts/title_settings.gd")
const Store=preload("res://scripts/room_layout_store.gd")
var state:Dictionary={}
var rect:=Rect2()
var key:Array=[]
var redraws:=0
var hits:=0
func submit(room:Dictionary,bounds:Rect2)->void:
	Store.prime()
	var snapshot:=room.duplicate(true)
	# This renderer does not read the generic equipment clock.
	snapshot.erase("machine_clock")
	var next:Array=[snapshot,bounds,Settings.reduced_motion,Store.revision,Store.shared_positions("room-moonbay",int(room.get("rotation",0))),owns_moonbay_tail()]
	if next==key:hits+=1;return
	key=next;state=snapshot;rect=bounds;queue_redraw()
	if owns_moonbay_tail():
		if wall_tail==null:
			wall_tail=WallTail.new();wall_tail.owner_base=self;wall_tail.use_parent_material=true;add_child(wall_tail)
		wall_tail.show();wall_tail.submit(snapshot,bounds)
	elif wall_tail!=null:wall_tail.hide()

func _draw()->void:
	redraws+=1
	Moon.draw(self,state,rect)

var retain_wall_commands:bool=not OS.get_cmdline_user_args().has("--reference-moon-walls")
var wall_tail:WallTail
func owns_moonbay_tail()->bool:
	# self_modulate affects only this item's commands, so retain the immediate
	# path when an explicit self tint would not propagate to child canvases.
	return retain_wall_commands and self_modulate==Color.WHITE
func record_tail_draw(label:String,started:int):
	var slot=get_parent()
	if slot!=null and slot.has_method("record_draw"):slot.record_draw(label,started)
class LiveGates extends Node2D:
	var draws:int=0
	func _draw():
		var base=get_parent().owner_base
		var mark:int=Time.get_ticks_usec();draws+=1
		Moon.draw_live_gates(self,base.state,base.rect)
		base.record_tail_draw("large_child_live_gates",mark)
class WallTail extends Node2D:
	var owner_base
	var state:Dictionary={}
	var rect:Rect2
	var geometry_key:Array=[]
	var redraws:int=0
	var hits:int=0
	var gates:LiveGates
	func submit(room:Dictionary,bounds:Rect2):
		if gates==null:gates=LiveGates.new();gates.use_parent_material=true;add_child(gates)
		gates.queue_redraw()
		# These are all room inputs consumed by walls/corners/windows. Store
		# revision also invalidates explicit Studio reloads. No mission clock.
		var next:Array=[bounds,int(room.get("rotation",0)),str(room.get("ocean_side","west")),bool(room.get("raised_walls",true)),Store.revision]
		if next==geometry_key:hits+=1;return
		geometry_key=next
		state={"rotation":next[1],"ocean_side":next[2],"raised_walls":next[3]}
		rect=bounds;queue_redraw()
	func _draw():
		var mark:int=Time.get_ticks_usec();redraws+=1
		Moon.draw_static_walls(self,state,rect)
		owner_base.record_tail_draw("large_child_static_walls",mark)
