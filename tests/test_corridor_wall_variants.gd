extends SceneTree
const Art=preload("res://rooms/underwater/corridor_surfaces.gd")
const Geometry=preload("res://rooms/underwater/corridor_geometry.gd")
const Dressing=preload("res://rooms/underwater/corridor_dressing.gd")
const Walls=preload("res://rooms/underwater/corridor_wall_art.gd")
var OUT="res://output/corridor-wall-variants-v1/"
var CARDS="res://assets/corridor-wall-variants-v1/cards/"
class Preview extends Node2D:
	var id:="corridor"
	var variant:=0
	var q:=0
	var raised:=true
	var light:=1.0
	var neighbors: Array=[]
	var textures: Array=[]
	func _draw() -> void:
		draw_rect(Rect2(0,0,512,512),Color("10282e"))
		draw_set_transform(Vector2(256,275),0,Vector2.ONE*1.05)
		var corner:=id=="corner"
		var tee:=id=="tee_corridor"
		var rotation:=Geometry.rotation({"id":id,"rotation":q})
		Art.draw_hull(self,Geometry.hull_for(corner,tee),Geometry.floor_for(corner,tee),Vector2.ZERO,rotation,textures,corner,true,light,tee,variant)
		if raised:Dressing.draw_risers(self,Geometry.hull_for(corner,tee),rotation,variant,lerpf(.35,1.0,light),neighbors)
		else:Dressing.draw_entries(self,Geometry.hull_for(corner,tee),rotation,false,neighbors)
		Dressing.draw_props(self,rotation,variant,lerpf(.35,1.0,light))
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--out="): OUT=arg.trim_prefix("--out=").trim_suffix("/")+"/"
		if arg.begins_with("--cards="): CARDS=arg.trim_prefix("--cards=").trim_suffix("/")+"/"
	call_deferred("run")
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT);DirAccess.make_dir_recursive_absolute(CARDS)
	for path in ["res://tests/test_corridor_wall_variants.gd","res://rooms/underwater/corridor_wall_art.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var f=FileAccess.open(path+".uid",FileAccess.WRITE)
			f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	assert(Art.detail_parts(false).is_empty() and Art.detail_parts(true).is_empty(),"Legacy floor and wall fittings removed")
	var turn=preload("res://tools/modular_room_geometry.gd")
	for id in ["corridor","corner","tee_corridor"]:
		var ports: Array=[Vector2.LEFT,Vector2.RIGHT] if id=="corridor" else [Vector2.LEFT,Vector2.DOWN] if id=="corner" else [Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN]
		var hull=Geometry.hull_for(id=="corner",id=="tee_corridor")
		for q in range(4):
			var rotation=Geometry.rotation({"id":id,"rotation":q})
			var expected:=0
			for port in ports:
				if turn.turn(port,rotation).is_equal_approx(Vector2.UP):expected+=1
			var found:=0
			for i in range(hull.size()):
				if Dressing.is_north_entry(turn.turn(hull[i],rotation),turn.turn(hull[(i+1)%hull.size()],rotation)):found+=1
			assert(found==expected,"Raised entry follows the rotated room port")
	assert(Walls.catalog().size()==6)
	for id in Walls.catalog():
		for part in ["face","cap","low","return"]:
			assert(Rect2(Vector2.ZERO,Walls.texture(id).get_size()).encloses(Walls.region(id,part)))
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	var p=Preview.new();p.textures=Art.load_sources();root.add_child(p)
	var records: Array=[]
	for id in ["corridor","corner","tee_corridor"]:
		p.id=id
		var hashes: Array=[]
		for v in range(3):
			p.variant=v
			var frames: Array=[]
			for q in range(4):
				p.q=q
				for raised in [true,false]:
					p.raised=raised;p.queue_redraw()
					await process_frame;await RenderingServer.frame_post_draw
					var im=root.get_texture().get_image()
					var name="%s-%d-q%d-%s.png"%[id,v,q,"raised" if raised else "low"]
					assert(im.save_png(OUT+name)==OK)
					frames.append(name)
					if q==0 and raised:
						var hash_value=hash(im.get_data())
						assert(not hash_value in hashes,"Variants must have distinct native output")
						hashes.append(hash_value)
						assert(im.save_png(CARDS+id+("" if v==0 else "-"+str(v))+".png")==OK)
			var row={"id":id,"variant":Walls.NAMES[v],"number":v,"frames":frames}
			records.append(row)
	# Culling evidence for a north-facing socket and dark material response.
	p.id="corridor";p.q=0;p.variant=2;p.raised=true;p.neighbors=[];p.light=0;p.queue_redraw()
	await process_frame;await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(OUT+"dark.png")==OK)
	p.light=1;p.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var exposed=root.get_texture().get_image()
	p.neighbors=[Vector2i.UP];p.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var joined=root.get_texture().get_image()
	assert(exposed.get_data()!=joined.get_data(),"Neighbor suppresses exposed socket face")
	assert(joined.save_png(OUT+"joined.png")==OK)
	var file=FileAccess.open(OUT+"review.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"\t"));file.close()
	print("CORRIDOR WALL VARIANTS PASS: six registered skins, nine distinct room variants, 72 rotated raised/low captures, neighbor culling")
	quit()
