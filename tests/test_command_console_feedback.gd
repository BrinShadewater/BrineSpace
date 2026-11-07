extends SceneTree
const OUT="res://output/command-operating-feedback-2026-09-21"
class Preview extends Node2D:
	var room
	var q=0
	var live=false
	var clock=0.0
	func _draw()->void:
		room.configure_embedded(q,[],live,clock)
		room.set_meta("raised_north_visible",true)
		room.render_into(self,Vector2(256,290),1.06,true)
		draw_set_transform(Vector2(256,290),0,Vector2.ONE*1.06)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self,"command_center",Vector2i.ZERO,false,false,room)
		room.render_into(self,Vector2(256,290),1.06,false,false)
var failures=0
func _init()->void:call_deferred("run")
func check(ok:bool,message:String)->void:
	if not ok:failures+=1;push_error(message)
func run()->void:
	if DisplayServer.get_name()=="headless":push_error("Native rendering required");quit(2);return
	var store=preload("res://scripts/room_layout_store.gd")
	store.loaded=true;store.data={}
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	var room=load("res://rooms/full-wall-v1/command_center_view.gd").new()
	room.embedded=true;room.hide();root.add_child(room)
	var preview=Preview.new();preview.room=room;preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(preview)
	DirAccess.make_dir_recursive_absolute(OUT)
	for q in range(4):
		var shots=[]
		preview.q=q
		for state in [[false,0.0],[false,0.4],[true,0.0],[true,0.4],[true,0.4]]:
			preview.live=state[0];preview.clock=state[1];preview.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var image=root.get_texture().get_image();image.save_png(OUT+"/q%d-%d.png"%[q,shots.size()]);shots.append(image)
		check(shots[0].get_data()==shots[1].get_data(),"Off room must ignore animation clock q%d"%q)
		check(shots[3].get_data()==shots[4].get_data(),"Held clock must freeze feedback q%d"%q)

		var allowed: Array[Rect2] = []
		for registration in [["sf-04",Rect2(188,28,14,9)],["spa-109g",Rect2(492,155,30,12)]]:
			var props=room.props.filter(func(p):return p.id=="library/tileset-"+registration[0])
			check(props.size()==1,"Installed console present: %s q%d"%[registration[0],q])
			if props.size()!=1:continue
			var prop=props[0];var factor=prop.rect.size.x/prop.registration.width
			var screen: Rect2=registration[1]
			var origin=Vector2(prop.rect.get_center().x,prop.rect.end.y)+(screen.position-prop.registration.pivot)*factor
			allowed.append(Rect2(Vector2(256,290)+origin*1.06,screen.size*factor*1.06).grow(3))
		var changed=[0,0];var escaped=0
		for y in range(512):
			for x in range(512):
				if shots[2].get_pixel(x,y)!=shots[3].get_pixel(x,y):
					var matched=false
					for i in range(allowed.size()):
						if allowed[i].has_point(Vector2(x,y)):changed[i]+=1;matched=true
					if not matched:escaped+=1
		check(changed[0]>0 and changed[1]>0 and escaped==0,"Both console traces move inside screens q%d changed=%s escaped=%d"%[q,changed,escaped])

	print("COMMAND CONSOLE FEEDBACK: four views; operating motion, off-state and held-clock checks; %d failures"%failures)
	quit(0 if failures==0 else 1)
