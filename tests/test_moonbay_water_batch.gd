extends SceneTree
const Slot=preload("res://scripts/large_room_canvas.gd")
const Studio=preload("res://rooms/large-rooms/studio_view.gd")
const Views={"moonbay":preload("res://rooms/large-rooms/moonbay.gd"),"hydroponics_farm":preload("res://rooms/large-rooms/hydroponics_farm.gd"),"storage_depot":preload("res://rooms/large-rooms/storage_depot.gd"),"tidal_power_plant":preload("res://rooms/large-rooms/tidal_power_plant.gd")}
const NormalGrid=preload("res://scripts/grid_canvas.gd")
class Grid extends NormalGrid:
	func _ready():pass
	func _process(_delta):pass
	func _draw():pass
	var occupied:Dictionary={}
	func _get_main():return self
class Reference extends Node2D:
	var rooms:Array=[]
	var rects:Array=[]
	var grid
	var offline:=false
	var clock:=.375
	func _draw():
		var previous:bool=Views.moonbay.combine_cached_water_strokes
		var previous_dynamic:bool=Views.moonbay.combine_dynamic_water_strokes
		Views.moonbay.combine_dynamic_water_strokes=false
		Views.moonbay.combine_cached_water_strokes=false
		Studio.hide_wet_equipment(self,grid.occupied)
		for i in rooms.size():
			var room:Dictionary=rooms[i]
			Views[room.id].draw(self,room,rects[i])
			Studio.draw_live(self,room,rects[i],clock,true,offline)
			if offline:draw_rect(rects[i],Color(.05,.02,.03,.35))
		Views.moonbay.combine_cached_water_strokes=previous
		Views.moonbay.combine_dynamic_water_strokes=previous_dynamic
var checks:=0
var failures:=0
var pairs:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(720,720)
	var grid:=Grid.new();root.add_child(grid)
	var views:Array=[];var hosts:Array=[];var slots:Array=[]
	for mode in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(720,720);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
		var host=Reference.new();host.grid=grid;host.modulate=Color(.87,.94,1,.8);vp.add_child(host);hosts.append(host)
		if mode==1:
			for id in Views:
				var slot:=Slot.new();slot.show_behind_parent=true;host.add_child(slot);slots.append(slot)
	var shader:=Shader.new();shader.code="shader_type canvas_item; void fragment(){ COLOR *= vec4(0.8,0.9,0.7,1.0); }"
	var mat:=ShaderMaterial.new();mat.shader=shader
	for material_enabled in [false,true]:
		for filtering in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
			for host in hosts:host.material=mat if material_enabled else null;host.texture_filter=filtering
			for wet in [false,true]:
				for q in range(4):
					for offline in [false,true]:
						for host in hosts:host.queue_redraw()
						var rooms:Array=[];var rects:Array=[];var i:=0
						for entry in range(Views.size()):
							var id:String=Views.keys()[(entry+q)%Views.size()]
							var room:Dictionary={"id":id,"pos":Vector2i(i,0),"rotation":q,"ocean_side":"west","raised_walls":true,"shelf_helmet_visible":true,"water_level":.4 if wet else 0.0,"machine_clock":.375,"moonbay_mission":{"phase":"idle"},"tidal_chamber":{"water":.4,"spinning":true,"rotor_angle":.375},"ports":[],"port_open":[]}
							var rect:=Rect2(40.375+float(i)*88,55.1875+float(i)*83,380,380)
							grid.occupied[room.pos]=room;rooms.append(room);rects.append(rect)
							slots[i].configure(grid,Views[id],room,room,rect,.375,true,offline);i+=1
						hosts[0].rooms=rooms;hosts[0].rects=rects;hosts[0].offline=offline;hosts[0].queue_redraw()
						await process_frame;await RenderingServer.frame_post_draw;pairs+=1
						var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
						var equal:=a.get_data()==b.get_data()
						if not equal and failures==0:a.save_png("user://reference.png");b.save_png("user://candidate.png")
						check(equal,"Overlapping large-room composition "+str([material_enabled,filtering,wet,q,offline]))
						if not wet and q==0 and not offline:
							var static_counts:Array=[]
							for slot in slots:
								check(slot.props.contents!=null and slot.props.contents.slots.size()>0,"Retained prop candidate executes")
								static_counts.append(slot.props.contents.static_redraws)
								check(static_counts.back()>0,"Static prop draw exercised")
							for host in hosts:host.queue_redraw()
							hosts[0].clock=.875
							for index in rooms.size():slots[index].configure(grid,Views[rooms[index].id],rooms[index],rooms[index],rects[index],.875,true,false)
							await process_frame;await RenderingServer.frame_post_draw;pairs+=1
							check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Animated clock changes remain exact")
							for index in slots.size():check(slots[index].props.contents.static_redraws==static_counts[index] and slots[index].props.advances>0,"Static bodies retained while effects advance")
							hosts[0].clock=.375

	for filtering in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
		for material_enabled in [false,true]:
			for host in hosts:host.material=mat if material_enabled else null;host.texture_filter=filtering;host.queue_redraw()
			for index in hosts[0].rooms.size():
				var room:Dictionary=hosts[0].rooms[index]
				slots[int(room.pos.x)].configure(grid,Views[room.id],room,room,hosts[0].rects[index],.375,true,hosts[0].offline)
			await process_frame;await RenderingServer.frame_post_draw;pairs+=1
			check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Stable room filter/material transition")
	var moon_index:=0
	for i in hosts[0].rooms.size():
		if hosts[0].rooms[i].id=="moonbay":moon_index=i
	var moon=slots[moon_index]
	var store=preload("res://scripts/room_layout_store.gd")
	for change in ["dry","helmet","port","mission","layout","hide","show","remove"]:
		for host in hosts:host.queue_redraw()
		var room:Dictionary=hosts[0].rooms[moon_index]
		match change:
			"dry":room.water_level=0.0
			"helmet":room.shelf_helmet_visible=false
			"port":room.ports=[{"cell":Vector2i(1,0),"side":"east"}];room.port_open=[1.0]
			"mission":room.moonbay_mission={"phase":"flood","chamber_water":.7,"cycle_clock":1.75,"progress":.5}
			"layout":store.data={"room-moonbay/3":{"door/style":"engineering"}};store.revision+=1
			"hide":moon.hide();hosts[0].rooms.remove_at(moon_index);hosts[0].rects.remove_at(moon_index)
			"show":moon.show();hosts[0].rooms.insert(moon_index,moon.room);hosts[0].rects.insert(moon_index,moon.rect)
			"remove":moon.get_parent().remove_child(moon);moon.queue_free();hosts[0].rooms.remove_at(moon_index);hosts[0].rects.remove_at(moon_index)
		for index in hosts[0].rooms.size():
			var current:Dictionary=hosts[0].rooms[index]
			slots[int(current.pos.x)].configure(grid,Views[current.id],current,current,hosts[0].rects[index],.375,true,hosts[0].offline)
		hosts[0].queue_redraw()
		await process_frame;await RenderingServer.frame_post_draw;pairs+=1
		check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Lifecycle "+change)
	check(grid.draw_usec_since_read>0 and grid.draws_since_read>0,"Child callbacks included in draw diagnostics")
	# Exercise actual normal Grid visibility/ownership cleanup without gameplay writes.
	var kept:=Node2D.new();hosts[1].add_child(kept)
	var anchor:=Vector2i(9,9)
	grid.large_slots[anchor]=kept;grid.occupied[anchor]={"id":"moonbay","pos":anchor}
	grid.visible_draw_rooms=[grid.occupied[anchor]]
	grid._sync_large_room_canvases(grid)
	check(kept.visible,"Visible room preserved")
	grid.visible_draw_rooms=[];grid._sync_large_room_canvases(grid)
	check(not kept.visible,"Culled room hidden")
	grid.visible_draw_rooms=[grid.occupied[anchor]];kept.show();grid._sync_large_room_canvases(grid)
	check(kept.visible,"Returned room preserved")
	grid.occupied[anchor]={"id":"corridor","pos":anchor};grid._sync_large_room_canvases(grid)
	check(not grid.large_slots.has(anchor) and kept.is_queued_for_deletion(),"Replacement releases old large room")
	var removed:=Node2D.new();hosts[1].add_child(removed);grid.large_slots[anchor]=removed;grid.occupied.erase(anchor);grid._sync_large_room_canvases(grid)
	check(grid.large_slots.is_empty() and removed.is_queued_for_deletion(),"Demolition releases large room")
	var weak:WeakRef=weakref(hosts[1])

	for vp in views:vp.queue_free()
	for attempt in range(8):
		if weak.get_ref()==null:break
		await process_frame
	check(weak.get_ref()==null,"Whole retained container released")
	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"raster_pairs":pairs}))
	print("LARGE_COMPOSITION ",checks," checks, ",failures," failures");quit(1 if failures else 0)
