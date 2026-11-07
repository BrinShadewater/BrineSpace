extends SceneTree
const Scope=preload("res://scripts/session_art_cache.gd")
const SurfaceArt=preload("res://rooms/underwater/corridor_surfaces.gd")
const Geometry=preload("res://rooms/underwater/corridor_geometry.gd")
const Walls=preload("res://rooms/underwater/corridor_wall_art.gd")
const Doors=preload("res://rooms/doors/painted_door.gd")
const Lights=preload("res://scripts/lighting_art.gd")
const Tiles=preload("res://rooms/whole-room/modular_floor.gd")
var checks:=0
var failures:=0
class Surface extends Node2D:
	var kind:=0
	var quarter:=0
	var factor:=1.0
	var transit:=true
	var door
	var amount:=0.0
	func _draw():
		draw_set_transform(Vector2(256.5,256.5),0,Vector2.ONE*factor)
		if transit:
			SurfaceArt.draw_hull(self,Geometry.hull_for(kind==1,kind==2),Geometry.floor_for(kind==1,kind==2),Vector2.ZERO,quarter,[],kind==1,true,-1,kind==2,0,{"floor/material/0/0":1})
		else:
			door.raised_at(self,amount,0,-80,79)
			door.progress=amount
			door.low_closed(self,Vector2(0,35),false,"default")
			door.low_closed(self,Vector2(80,35),true,"default")
			Walls.detail(self,Rect2(-150,100,300,70),0,0.8)
			Walls.draw_glazing(self,"straight-panoramic",Rect2(-150,170,300,50),0.8,false)
			draw_texture(Lights.texture("warm"),Vector2(-64,-220))
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace("\\","/"):
		push_error("Transit test requires isolated user directory");quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	var capture:=SubViewport.new();capture.size=Vector2i(512,512);capture.transparent_bg=true
	capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture)
	var surface:=Surface.new();capture.add_child(surface)
	for filter_value in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
		surface.texture_filter=filter_value
		for kind in range(3):
			surface.kind=kind
			for quarter in range(4):
				surface.quarter=quarter
				for tiled in [true,false]:
					Tiles.enabled=tiled
					for scale_value in [0.73,1.0]:
						surface.factor=scale_value;SurfaceArt.current_floor=null;SurfaceArt.load_unused_deck=false
						surface.queue_redraw();await frame()
						var candidate:Image=capture.get_texture().get_image()
						check((SurfaceArt.current_floor==null)==tiled,"Only legacy drawing loads deck")
						check(not candidate.is_invisible(),"Corridor pixels visible")
						SurfaceArt.load_unused_deck=true;surface.queue_redraw();await frame()
						check(SurfaceArt.current_floor!=null,"Reference loads unused deck")
						check(candidate.get_data()==capture.get_texture().get_image().get_data(),"Exact corridor pixels")
	SurfaceArt.load_unused_deck=false;Tiles.enabled=true
	surface.queue_free();surface=null;await frame()
	for filter_value in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
		for family in ["default","reactor","hallway"]:
			for amount in [0.0,0.12,0.5,1.0]:
				surface=Surface.new();surface.transit=false;surface.texture_filter=filter_value;surface.door=Doors.for_variant(family);surface.amount=amount
				capture.add_child(surface);Scope.retain(surface)
				var other:=Node.new();root.add_child(other);Scope.retain(other)
				await frame();var pixels:Image=capture.get_texture().get_image()
				var skin=surface.door;var saved_progress:float=skin.progress
				var refs:Array=[weakref(Walls.detail_texture),weakref(Walls.tunnel_texture),weakref(Lights.texture("warm"))]
				for image in skin.textures.values():refs.append(weakref(image))
				other.queue_free();await frame()
				check(not skin.textures.is_empty() and not Lights.textures.is_empty(),"Overlapping owner protects images")
				check(pixels.get_data()==capture.get_texture().get_image().get_data(),"Surviving owner pixels exact")
				surface.queue_free();surface=null;await frame()
				check(skin.textures.is_empty() and Walls.textures.is_empty() and Walls.detail_texture==null and Walls.tunnel_texture==null and Lights.textures.is_empty() and SurfaceArt.current_floor==null,"Transit images cleared")
				check(Doors.for_variant(family)==skin and skin.progress==saved_progress,"Style identity and progress retained")
				for ref in refs:check(ref.get_ref()==null,"Transit image weak reference released")
				surface=Surface.new();surface.transit=false;surface.texture_filter=filter_value;surface.door=skin;surface.amount=amount;capture.add_child(surface);Scope.retain(surface);await frame()
				check(pixels.get_data()==capture.get_texture().get_image().get_data(),"Reloaded door/wall/light pixels exact")
				surface.queue_free();surface=null;await frame()
	capture.queue_free();await frame()
	print("TRANSIT MATERIAL CACHE: %d checks; %d failures"%[checks,failures]);quit(1 if failures else 0)
