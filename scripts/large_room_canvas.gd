extends Node2D
const Retained=preload("res://scripts/moonbay_base_canvas.gd")
const Studio=preload("res://rooms/large-rooms/studio_view.gd")
var grid
var view
var room:Dictionary={}
var appearance:Dictionary={}
var rect:=Rect2()
var clock:=0.0
var operating:=true
var offline:=false
var base:Node2D
var props:Node2D
var retain_static_bases:=not OS.get_cmdline_user_args().has("--immediate-static-large-bases")
class MoonBase extends Retained:
	func _draw():
		var mark:=Time.get_ticks_usec()
		super._draw()
		var slot=get_parent()
		slot.record_draw("large_child_base",mark)
class StaticBase extends Node2D:
	var state:Dictionary={}
	var bounds:=Rect2()
	var key:Array=[]
	var redraws:=0
	var hits:=0
	func submit(room:Dictionary,rect:Rect2):
		var snapshot:=room.duplicate(true)
		# Hydroponics/storage bases and their common walls do not read this clock.
		snapshot.erase("machine_clock")
		var store=preload("res://scripts/room_layout_store.gd")
		store.prime()
		var next:Array=[snapshot,rect,preload("res://scripts/title_settings.gd").reduced_motion,store.revision]
		if next==key:hits+=1;return
		key=next;state=snapshot;bounds=rect;queue_redraw()
	func _draw():
		var slot=get_parent();var mark:=Time.get_ticks_usec();redraws+=1
		slot.view.draw(self,state,bounds)
		slot.record_draw("large_child_base",mark)
class ImmediateBase extends Node2D:
	func _draw():
		var slot=get_parent();var mark:=Time.get_ticks_usec()
		slot.view.draw(self,slot.appearance,slot.rect)
		slot.record_draw("large_child_base",mark)
# Keep each prop body and live effect adjacent; wet/special props retain original drawing.
class Context extends Studio.PaintContext:
	var actor:=Vector2.ZERO
	var external_actor_texture:Texture2D
	var quarter:=0
	func props_rebuilt_each_configure()->bool:return true
class Contents extends "res://scripts/room_content_canvas.gd":
	var owner_slot
	func paint(child):
		var mark:=Time.get_ticks_usec();super.paint(child)
		owner_slot.record_draw("large_prop_retained",mark)
class OfflineOverlay extends Node2D:
	var rect:=Rect2()
	var owner_slot
	func _draw():
		var mark:=Time.get_ticks_usec();draw_rect(rect,Color(0.05,0.02,0.03,0.35))
		owner_slot.record_draw("large_prop_overlay",mark)
class Props extends Node2D:
	var contents
	var overlay
	var context:=Context.new()
	var prepared:Array=[]
	var prepared_props:Array=[]
	var prepares:=0
	var advances:=0
	func _draw():
		var slot=get_parent();var mark:=Time.get_ticks_usec()
		var store=preload("res://scripts/room_layout_store.gd")
		var props:Array=Studio.live_props(str(slot.room.id),int(slot.room.get("rotation",0)))
		var can_split:=preload("res://scripts/room_flooding.gd").level(slot.room)<=0.001
		for prop in props:
			if not prop.get("library_asset",false) or prop.has("portable_view") or prop.get("custom_library_draw",false) or prop.registration.has("drone_dock") or prop.registration.has("aquarium"):can_split=false;break
		if not can_split:
			if contents!=null:contents.hide();overlay.hide()
			Studio.hide_wet_equipment(self,slot.grid._get_main().occupied)
			var target:CanvasItem=slot.get_parent() if preload("res://scripts/room_flooding.gd").level(slot.room)>0.001 else self
			Studio.draw_live(target,slot.room,slot.rect,slot.clock,slot.operating,slot.offline)
			if slot.offline:draw_rect(slot.rect,Color(0.05,0.02,0.03,0.35))
		else:
			if contents==null:
				contents=Contents.new();contents.owner_slot=slot;contents.cull_props=false;contents.use_parent_material=true;add_child(contents)
				overlay=OfflineOverlay.new();overlay.owner_slot=slot;overlay.use_parent_material=true;add_child(overlay)
			contents.show()
			# Studio shares read-only prop lists until the layout revision changes.
			# Identity also catches cache replacement without a revision bump.
			var next:Array=[str(slot.room.id),int(slot.room.get("rotation",0)),store.revision,slot.rect,slot.operating]
			if next!=prepared or not is_same(props,prepared_props):
				prepared=next.duplicate(true);prepared_props=props;prepares+=1
				context.props=props;context.operating=slot.operating;context.machine_clock=slot.clock;context.quarter=int(slot.room.get("rotation",0))
				contents.draw_origin=slot.rect.get_center();contents.draw_scale=slot.rect.size.x/768.0
				var queue:Array=[]
				for prop in props:queue.append({"kind":"prop","prop":prop})
				contents.submit(context,queue)
				for child in contents.slots:child.use_parent_material=true
			else:advances+=1;contents.advance_live(slot.clock)
			overlay.visible=slot.offline;overlay.rect=slot.rect
			if slot.offline:overlay.queue_redraw()
		slot.record_draw("large_child_props",mark)

func configure(owner_grid,renderer,current_room:Dictionary,current_appearance:Dictionary,bounds:Rect2,time:float,on:bool,off:bool):
	if base!=null and str(room.get("id",""))!=str(current_room.id):
		remove_child(base);base.queue_free();remove_child(props);props.queue_free();base=null;props=null
	use_parent_material=true
	grid=owner_grid;view=renderer;room=current_room;appearance=current_appearance;rect=bounds;clock=time;operating=on;offline=off
	if base==null:
		base=MoonBase.new() if str(room.id)=="moonbay" else StaticBase.new() if retain_static_bases and str(room.id) in ["hydroponics_farm","storage_depot"] else ImmediateBase.new()
		base.use_parent_material=true;add_child(base);props=Props.new();props.use_parent_material=true;add_child(props)
	if base.has_method("submit"):base.submit(appearance,rect)
	else:base.queue_redraw()
	props.queue_redraw()

# Include child callbacks in the same diagnostic budget as immediate room drawing.
func record_draw(label:String,started:int)->void:
	var elapsed:=Time.get_ticks_usec()-started
	grid.draw_usec_since_read+=elapsed
	grid.draws_since_read+=1
	if grid.profile_draw:
		grid.draw_profile_usec["live_rooms"]=int(grid.draw_profile_usec.get("live_rooms",0))+elapsed
		grid.draw_profile_totals_usec["live_rooms"]=int(grid.draw_profile_totals_usec.get("live_rooms",0))+elapsed
		grid.draw_profile_usec["setup_"+label]=int(grid.draw_profile_usec.get("setup_"+label,0))+elapsed
