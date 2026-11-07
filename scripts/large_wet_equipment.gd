extends Node2D
## Per-prop water materials for the large-room immediate renderer.
const Library=preload("res://scripts/room_asset_library.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Flood=preload("res://scripts/flood_visuals.gd")
var slots: Array=[]
var context
var origin:=Vector2.ZERO
var art_scale:=1.0
class Slot extends Node2D:
	var prop: Dictionary={}
	func _draw():
		var host=get_parent()
		host.context.painter=self
		Store.draw_flip(host.context,self,prop,host.origin,host.art_scale)
		Library.draw(host.context,prop)
func configure(view,at: Vector2,scale_value: float,water: float,clock: float,offline := false):
	context=view;origin=at;art_scale=scale_value
	# The parent's offline wash is drawn before these child commands.
	modulate=Color(.6675,.657,.6605,1) if offline else Color.WHITE
	while slots.size()<view.props.size():
		var slot:=Slot.new();add_child(slot);slots.append(slot)
	for i in range(slots.size()):
		var slot: Slot=slots[i]
		if i>=view.props.size() or view.props[i].get("layout_hidden",false):slot.hide();continue
		slot.prop=view.props[i];slot.show()
		Flood.prop_material(slot,slot.prop,water,clock,origin,art_scale)
		slot.queue_redraw()
	show()
