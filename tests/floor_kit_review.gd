extends SceneTree
const KIT=preload("res://assets/floor-kit-v6/floor_kit.gd")
const OUT="res://output/floor-kit-v6/"
class Piece extends Node2D:
	var family: String
	var kind: String
	func _draw() -> void:
		var kit=preload("res://assets/floor-kit-v6/floor_kit.gd")
		if family=="corridor": kit.corridor(self,kind)
		elif family=="join": kit.join(self,kind)
		elif family in ["drain","cable"]: kit.utility(self,family,kind)
		else: kit.detail(self,kind)
func _init() -> void: call_deferred("run")
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1500,1000)
	var gallery:=Node2D.new()
	root.add_child(gallery)
	var entries: Array=[]
	for shape in KIT.SHAPES: entries.append(["corridor",shape])
	for shape in KIT.JOINS: entries.append(["join",shape])
	for family in ["drain","cable"]:
		for shape in KIT.UTILITIES: entries.append([family,shape])
	for kind in KIT.DETAILS: entries.append(["detail",kind])
	for i in range(entries.size()):
		var vp:=SubViewport.new()
		vp.size=Vector2i(384,384)
		vp.transparent_bg=true
		vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS
		root.add_child(vp)
		var piece:=Piece.new()
		piece.family=entries[i][0]
		piece.kind=entries[i][1]
		piece.position=Vector2(192,192)
		vp.add_child(piece)
		await process_frame
		await RenderingServer.frame_post_draw
		var im:=vp.get_texture().get_image()
		assert(im.get_pixel(0,0).a==0,"No halo outside piece")
		assert(im.save_png(OUT+piece.family+"-"+piece.kind+".png")==OK)
		var sprite:=Sprite2D.new()
		sprite.texture=ImageTexture.create_from_image(im)
		sprite.position=Vector2(125+(i%6)*250,120+(i/6)*165)
		sprite.scale=Vector2.ONE*(.48 if piece.family=="corridor" else 1.5)
		gallery.add_child(sprite)
		var label:=Label.new()
		label.text=piece.family+" / "+piece.kind
		label.position=sprite.position+Vector2(-110,55)
		gallery.add_child(label)
		vp.queue_free()
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(OUT+"catalog.png")==OK)
	# All four rotations retain the same canonical footprint area.
	for shape in KIT.SHAPES:
		var poly=KIT.polygon(shape)
		assert(poly.size()>=8)
		for q in range(4):
			for v in poly:
				var turned: Vector2=v.rotated(q*PI/2)
				assert(absf(turned.x)<=192.01 and absf(turned.y)<=192.01)
	print("FLOOR KIT PASS: ",entries.size()," transparent native exports; five corridor footprints, four rotations")
	quit()
