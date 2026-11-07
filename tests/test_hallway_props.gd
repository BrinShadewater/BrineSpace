extends SceneTree
const G=preload("res://tools/modular_room_geometry.gd")
const C=preload("res://rooms/underwater/corridor_geometry.gd")
const L=preload("res://scripts/room_asset_library.gd")
const S=preload("res://rooms/underwater/corridor_surfaces.gd")
const D=preload("res://rooms/underwater/corridor_dressing.gd")
const IDS=["library/sp-hall-breathing-cabinet","library/sp-hall-maintenance-caddy","library/sp-hall-pressure-pedestal","library/sp-hall-stacked-sage-crates","library/sp-hall-stacked-slate-cases","library/sp-hall-sealed-sage-barrel","library/sp-hall-paired-slate-barrels","library/sp-hall-stacked-crates-depth","library/sp-hall-long-slate-case","library/sp-hall-hex-clay-crate","library/sp-hall-olive-capsule-crate","library/sp-hall-sage-leaf-planter","library/sp-hall-fern-trough-planter","library/sp-hall-snake-plant-pot","library/sp-hall-cane-plant-pot","library/sp-hall-succulent-bowl","library/sp-hall-rubber-plant-pot","library/sp-hall-asparagus-fern-pot","library/sp-hall-dwarf-palm-pot"]
class Preview extends Node2D:
	var props:Array=[]
	var room_id:="corridor"
	var q:=0
	var painter:CanvasItem
	var operating:=false
	var machine_clock:=0.0
	func _draw():
		painter=self
		draw_rect(Rect2(0,0,512,512),Color("10282e"))
		draw_set_transform(Vector2(256,275),0,Vector2.ONE*1.05)
		S.draw_hull(self,C.hull_for(room_id=="corner",room_id=="tee_corridor"),C.floor_for(room_id=="corner",room_id=="tee_corridor"),Vector2.ZERO,q,[],room_id=="corner",true,1.0,room_id=="tee_corridor",11)
		for prop in props:L.draw(self,prop)
		D.draw_risers(self,C.hull_for(room_id=="corner",room_id=="tee_corridor"),q,11,1.0)
func _init():call_deferred("run")
func place(id:String,contact:Vector2)->Dictionary:
	var prop:Dictionary=L.template(id).duplicate(true)
	assert(not prop.is_empty(),"Registered prop loads")
	var f:Array=prop.footprint
	prop.rect.position=contact-Vector2(f[0]+f[2]*0.5,f[1]+f[3]*0.5)*prop.rect.size
	prop.sort_y=L.base_sort_y(prop)
	return prop
func run():
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	var preview=Preview.new();root.add_child(preview)
	var grid=preload("res://scripts/grid_canvas.gd").new()
	var checked:=0
	for prop_id in IDS:
		for id in ["corridor","corner","tee_corridor"]:
			for quarter in range(4):
				var room:Dictionary={"id":id,"rotation":quarter,"pos":Vector2i.ZERO}
				var q:=C.rotation(room)
				var data:Dictionary=grid.bill_room_geometry(room,[0,1,2,3])
				data.props=[place(prop_id,G.turn(Vector2(-100,-23),q))]
				data.open=[0,1,2,3];data.blockers=[]
				for prop in data.props:
					for rect in G.prop_collision_rects(prop):data.blockers.append(rect.grow(10))
				var npc=preload("res://scripts/bill_npc.gd").new();npc.geometry={Vector2i.ZERO:data}
				for rect in data.blockers:assert(not npc.can_stand(Vector2(192,192)+rect.get_center()))
				var exits=D.corridor_exit_directions(C.hull_for(id=="corner",id=="tee_corridor"),q)
				var start:=Vector2i(exits[0]*176)
				var seen:Dictionary={start:true};var queue:Array[Vector2i]=[start];var index:=0
				while index<queue.size():
					var at:Vector2i=queue[index];index+=1
					for offset in [Vector2i(16,0),Vector2i(-16,0),Vector2i(0,16),Vector2i(0,-16)]:
						var next:Vector2i=at+offset
						if seen.has(next) or absi(next.x)>176 or absi(next.y)>176:continue
						if npc.segment_clear(Vector2(at)+Vector2(192,192),Vector2(next)+Vector2(192,192)):
							seen[next]=true;queue.append(next)
				for exit in exits:
					if not seen.has(Vector2i(exit*176)):
						push_error("Blocked route: %s %s q%d"%[prop_id,id,quarter]);grid.free();quit(1);return
				preview.props=data.props;preview.room_id=id;preview.q=q;preview.queue_redraw()
				await process_frame;await RenderingServer.frame_post_draw
				assert(root.get_texture().get_image().save_png("res://assets/hallway-props-v1/review/"+prop_id.trim_prefix("library/sp-hall-")+"-"+id+"-q"+str(quarter)+".png")==OK)
				checked+=1
	grid.free();print("HALLWAY PROPS PASS: ",checked," native placements, registered blockers and all ports reachable with 10-unit crew clearance")
	quit()
