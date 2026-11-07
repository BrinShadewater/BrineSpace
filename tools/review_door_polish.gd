extends SceneTree
const Door=preload("res://rooms/doors/department_door.gd")
const Finish=preload("res://rooms/doors/door_finish.gd")
const Wet=preload("res://rooms/doors/door_water.gd")
const OUT="res://output/door-polish-v1/"
class View extends Node2D:
	var materials: Dictionary
	var variant: String="generic"
	var kind: String="front"
	var frame:=0
	var wet:=false
	var clock:=0.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,480,320),Color("223338"))
		draw_set_transform(Vector2(240,160) if kind!="raised" else Vector2(240,685),0,Vector2.ONE*2.4)
		if kind=="raised":
			Finish.raised(self,frame/9.0,variant)
		else:
			draw_rect(Rect2(-68,-58,136,116),Color("36474a"))
			if wet: draw_rect(Rect2(-68,-58,68,116) if kind=="side" else Rect2(-68,-58,136,58),Color("386366"))
			var parts:=Door.parts(frame,kind=="side",variant)
			for pass_floor in [true,false]:
				for part in parts:
					if part.floor==pass_floor: Door.draw_piece(self,materials,variant,part,1)
			if wet: Wet.draw(self,Vector2.ZERO,Vector2.RIGHT if kind=="side" else Vector2.DOWN,frame/9.0,0.6,0.8,true,clock,1)
		draw_set_transform(Vector2.ZERO)
		draw_string(ThemeDB.fallback_font,Vector2(18,28),variant+" / "+kind+(" / flooding closure" if wet else " / dry"),HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color("d1dfd9"))
func _init(): call_deferred("run")
func run():
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(480,320);root.content_scale_size=root.size
	var source:=Image.new();assert(source.load_png_from_buffer(FileAccess.get_file_as_bytes(Door.SOURCE))==OK)
	var view:=View.new();view.materials=Door.make_materials(root,ImageTexture.create_from_image(source));root.add_child(view)
	await process_frame;await RenderingServer.frame_post_draw
	var records: Array=[]
	for variant in Door.VARIANTS:
		for kind in ["front","side","raised"]:
			view.variant=variant;view.kind=kind;view.wet=false
			var files: Array=[]
			for frame in range(10):
				view.frame=frame;view.queue_redraw()
				await process_frame;await RenderingServer.frame_post_draw
				var name: String=variant+"-"+kind+"-"+str(frame)+".png"
				assert(root.get_texture().get_image().save_png(OUT+name)==OK);files.append(name)
			records.append({"variant":variant,"kind":kind,"frames":files})
	for kind in ["front","side"]:
		view.kind=kind;view.variant="brine";view.wet=true
		var files: Array=[]
		for i in range(20):
			view.frame=maxi(0,9-i/2);view.clock=i/18.0;view.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var name: String="wet-"+kind+"-"+str(i)+".png"
			assert(root.get_texture().get_image().save_png(OUT+name)==OK);files.append(name)
		records.append({"variant":"flooding","kind":kind,"frames":files})
	var f:=FileAccess.open(OUT+"manifest.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"\t"));f.close()
	for path in ["res://rooms/doors/door_finish.gd","res://rooms/doors/door_water.gd",get_script().resource_path]:
		if not FileAccess.file_exists(path+".uid"):
			var file:=FileAccess.open(path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));file.close()
	print("DOOR POLISH NATIVE PASS: 5 finishes, 3 geometries, 150 dry frames, 40 wet closing frames")
	quit()
