extends SceneTree
## Native depth-review fixture. Uses production actor source crop via room renderer.
## Does not create a gameplay scene or access player/fixture saves.
var view_path:=""
var output:=""
class PosePanel extends Node2D:
	const ORIGIN:=Vector2(500,540)
	var room
	var actor_texture: Texture2D
	var quarter:=0
	var prop_index:=0
	var behind:=false
	func _draw() -> void:
		room.configure_embedded(quarter,[],false,0.0)
		var prop: Dictionary=room.props[prop_index]
		room.actor=Vector2(prop.rect.get_center().x,prop.rect.position.y-8 if behind else prop.rect.end.y+8)
		room.show_actor=true
		room.external_actor_texture=actor_texture
		room.shell_pass=0
		room.render_into(self,ORIGIN,2.0)
		draw_string(ThemeDB.fallback_font,Vector2(30,28),"DEPTH REVIEW / q%d / %s / %s"%[quarter,str(prop.id),"behind" if behind else "front"],HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--view="): view_path=arg.trim_prefix("--view=")
		if arg.begins_with("--output="): output=arg.trim_prefix("--output=")
	call_deferred("run")
func run() -> void:
	assert(view_path.begins_with("res://rooms/"),"Specify an existing registered room view")
	assert(output.begins_with("res://output/") and not DirAccess.dir_exists_absolute(output),"Use a new review directory")
	DirAccess.make_dir_recursive_absolute(output)
	# Extra gutter keeps a crew member's projected head and review label apart.
	# World-to-pixel scale stays 2x; neither sprites nor crops are resized.
	root.size=Vector2i(1000,1040)
	root.content_scale_size=root.size
	var room=load(view_path).new()
	room.embedded=true
	room.hide()
	root.add_child(room)
	var image:=Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/Major_Bill/rotations/south.png"))==OK)
	var panel:=PosePanel.new()
	panel.room=room
	panel.actor_texture=ImageTexture.create_from_image(image)
	root.add_child(panel)
	var poses:=0
	var records: Array=[]
	for q in range(4):
		for index in range(room.props.size()):
			for behind in [false,true]:
				panel.quarter=q
				panel.prop_index=index
				panel.behind=behind
				panel.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				if not room.Geometry.can_stand(room.actor,room.layout,room.props,room.edges):
					push_error("Review actor must stand outside collision")
					quit(1)
					return
				var stem:="q%d-prop%d-%s"%[q,index,"behind" if behind else "front"]
				var frame:=root.get_texture().get_image()
				assert(frame.save_png(output.path_join(stem+".png"))==OK)
				# Crop native pixels around the COMPLETE host and production sprite.
				# Do not recenter only on the ground footprint: tall tops would disappear.
				var actor_rect:=Rect2(room.actor-Vector2(23.04,65.28*50.0/56.0),Vector2(46.08,65.28))
				var detail: Rect2=room.prop_visual_bounds(room.props[index]).merge(actor_rect).grow(12)
				var screen:=Rect2(PosePanel.ORIGIN+detail.position*2,detail.size*2)
				var pixels:=Rect2i(Vector2i(screen.position.floor()),Vector2i(screen.end.ceil()-screen.position.floor()))
				if not Rect2i(Vector2i.ZERO,frame.get_size()).encloses(pixels):
					push_error("Full prop/actor detail outside native frame: "+stem+" "+str(pixels))
					quit(1)
					return
				assert(frame.get_region(pixels).save_png(output.path_join(stem+"-detail.png"))==OK)
				records.append({"quarter":q,"prop":str(room.props[index].id),"index":index,"pose":"behind" if behind else "front","full":stem+".png","detail":stem+"-detail.png","crop":[pixels.position.x,pixels.position.y,pixels.size.x,pixels.size.y]})
				poses+=1
	var manifest:=FileAccess.open(output.path_join("depth-review.json"),FileAccess.WRITE)
	assert(manifest!=null)
	manifest.store_string(JSON.stringify({"view":view_path,"world_scale":2,"actor_size":[46.08,65.28],"poses":records},"\t"))
	manifest.close()
	print("DEPTH POSES: ",poses," native front/behind captures and full-host detail crops; production 46.08x65.28 actor; standability checked; visual review still required")
	quit()
