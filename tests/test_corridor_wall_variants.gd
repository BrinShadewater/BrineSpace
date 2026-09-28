extends SceneTree
const Art=preload("res://rooms/underwater/corridor_surfaces.gd")
const Geometry=preload("res://rooms/underwater/corridor_geometry.gd")
const Dressing=preload("res://rooms/underwater/corridor_dressing.gd")
const Walls=preload("res://rooms/underwater/corridor_wall_art.gd")
var OUT="res://output/corridor-wall-variants-v1/"
# Test runs must not rewrite tracked art. Rebake the shipped cards explicitly with
# --cards=res://assets/corridor-wall-variants-v1/cards
var floor_finish:=""
var CARDS="res://output/corridor-wall-variants-v1/cards/"
class Preview extends Node2D:
	var id:="corridor"
	var variant:=0
	var q:=0
	var raised:=true
	var light:=1.0
	var neighbors: Array=[]
	var textures: Array=[]
	var furnishing
	var floor_values:Dictionary={}
	func _draw() -> void:
		draw_rect(Rect2(0,0,512,512),Color("10282e"))
		draw_set_transform(Vector2(256,275),0,Vector2.ONE*1.05)
		var corner:=id=="corner"
		var tee:=id=="tee_corridor"
		var rotation:=Geometry.rotation({"id":id,"rotation":q})
		Art.draw_hull(self,Geometry.hull_for(corner,tee),Geometry.floor_for(corner,tee),Vector2.ZERO,rotation,textures,corner,true,light,tee,variant,floor_values)
		if furnishing!=null:
			furnishing.room_id=id
			furnishing.configure_embedded(q,[],true,0.0)
			furnishing.render_into(self,Vector2(256,275),1.05,false,false)
			draw_set_transform(Vector2(256,275),0,Vector2.ONE*1.05)
		if raised:Dressing.draw_risers(self,Geometry.hull_for(corner,tee),rotation,variant,lerpf(.35,1.0,light),neighbors)
		else:Dressing.draw_entries(self,Geometry.hull_for(corner,tee),rotation,false,neighbors)
		Dressing.draw_props(self,rotation,variant,lerpf(.35,1.0,light))
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--floor="): floor_finish=arg.trim_prefix("--floor=")
		if arg.begins_with("--out="): OUT=arg.trim_prefix("--out=").trim_suffix("/")+"/"
		if arg.begins_with("--cards="): CARDS=arg.trim_prefix("--cards=").trim_suffix("/")+"/"
	call_deferred("run")
func run() -> void:
	check_sampling()
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
	assert(Walls.catalog().size()==3*Walls.NAMES.size(),"Three hull shapes each retain every finish selection")
	for id in Walls.catalog():
		for part in ["face","cap","low","return"]:
			assert(Rect2(Vector2.ZERO,Walls.texture(id).get_size()).encloses(Walls.region(id,part)))
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	var p=Preview.new();p.floor_values={"floor/finish":floor_finish} if not floor_finish.is_empty() else {};p.textures=Art.load_sources();root.add_child(p)
	p.furnishing=preload("res://scripts/corridor_layout_view.gd").new();p.furnishing.embedded=true;root.add_child(p.furnishing);p.furnishing.hide()
	var records: Array=[]
	for id in ["corridor","corner","tee_corridor"]:
		p.id=id
		var hashes: Array=[]
		for v in range(Walls.NAMES.size()):
			p.variant=v
			var frames: Array=[]
			var raised_hashes: Array=[]
			for q in range(4):
				p.q=q
				for raised in [true,false]:
					p.raised=raised;p.queue_redraw()
					await process_frame;await RenderingServer.frame_post_draw
					var im=root.get_texture().get_image()
					var name="%s-%d-q%d-%s.png"%[id,v,q,"raised" if raised else "low"]
					assert(im.save_png(OUT+name)==OK)
					frames.append(name)
					if raised:raised_hashes.append(hash(im.get_data()))
					if q==0 and raised:
						assert(im.save_png(CARDS+id+("" if v==0 else "-"+str(v))+".png")==OK)
			var hash_value=hash(raised_hashes)
			assert(not hash_value in hashes,"Variants must have distinct native output across rotations")
			hashes.append(hash_value)
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
	print("CORRIDOR WALL VARIANTS PASS: 36 shape/finish registrations, 36 distinct room variants, 288 rotated raised/low captures, neighbor culling")
	quit()

func check_sampling() -> void:
	var full:=Rect2(20,122,2130,470)
	for width in [70.0,200.0,328.0]:
		var raised:=Walls.glazing_crop(full,Vector2(width,60))
		var low:=Walls.glazing_crop(full,Vector2(width,18))
		assert(is_equal_approx(raised.size.x/width,raised.size.y/60.0),"Raised ocean must retain aspect")
		assert(is_equal_approx(low.size.x/width,low.size.y/18.0),"Low ocean must retain aspect")
		assert(is_equal_approx(raised.size.x,low.size.x),"Opposite glass must retain scene scale")
		assert(full.encloses(raised) and full.encloses(low))
	var floors=preload("res://rooms/whole-room/modular_floor.gd")
	for path in [floors.HALL_TILES]+floors.HALL_ALTERNATES:
		var divisions:int=floors.hall_divisions(path)
		for shape in ["corridor","corner","tee_corridor"]:
			for q in range(4):
				var values:Dictionary={"floor/finish":path}
				for cell in floors.cells(true,q,shape):values[floors.tile_key(cell)]=[2,3]
				var batches:Array=floors.meshes(values,true,q,1.0,floors.SCIENCE,shape,0)
				assert(batches.size()==1)
				for uv in batches[0].mesh.surface_get_arrays(0)[Mesh.ARRAY_TEX_UV]:
					assert(uv.x>=2.0/divisions-0.0001 and uv.x<=3.0/divisions+0.0001,"Selected tile U bounds")
					assert(uv.y>=3.0/divisions-0.0001 and uv.y<=4.0/divisions+0.0001,"Selected tile V bounds")
	print("SAMPLING PASS: 48 manual-floor shape/rotation cases and raised/low glass aspect/scale")
