extends SceneTree
const Visibility=preload("res://scripts/underwater_visibility.gd")
const Field=preload("res://scripts/wreck_field.gd")
const Hardware=preload("res://scripts/station_hardware.gd")
class Station extends RefCounted:
	var wrecks:Dictionary={}
	var surveyed_water:Dictionary={}
	var placed_rooms:Array=[]
	var hardware:Dictionary={"power":true,"exterior":true}
	var power_blackout:=false
	var powered_room_cells:Dictionary={}
	var resources:Dictionary={"power":100}
	var power_capacity:=100
	var paused:=false
	var clock:=0.0
	func get_unscaled_time_seconds()->float:return clock
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func original(game)->Image:
	var result:=Image.create(40,40,false,Image.FORMAT_RGBA8);result.fill(Color.BLACK)
	for cell in game.wrecks:
		if Field.blocks(game.wrecks,cell):result.set_pixelv(cell,Color(1,0,0,1))
	for cell in game.surveyed_water:
		var color:=result.get_pixelv(cell);color.g=1;result.set_pixelv(cell,color)
	for room in game.placed_rooms:
		if room.id not in ["corridor","corner","tee_corridor"]:continue
		var color:=result.get_pixelv(room.pos);color.b=Hardware.exterior_light_level(game,room)*.55
		result.set_pixelv(room.pos,color)
	return result
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
	root.set_disable_input(true)
	var game:=Station.new();var effect=Visibility.new()
	var texture_id:int=effect.mask_texture.get_instance_id()
	var views:Array=[];var images:Array=[]
	for i in 2:
		var vp:=SubViewport.new();vp.size=Vector2i(320,320);vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
		var image:=TextureRect.new();image.size=Vector2(320,320);image.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;vp.add_child(image);images.append(image)
	images[1].texture=effect.mask_texture
	var a:=Vector2i(10,12);var b:=Vector2i(11,12)
	for mode in range(24):
		match mode:
			1:game.wrecks[a]={"cleared":false}
			2:game.wrecks.erase(a);game.wrecks[b]={"cleared":false}
			3:game.wrecks[b].cleared=true
			4:game.surveyed_water[b]=true
			5:game.surveyed_water.erase(b);game.surveyed_water[a]=true
			6:game.placed_rooms=[{"id":"corridor","pos":a}];game.powered_room_cells[a]=true
			7:game.placed_rooms[0].pos=b;game.powered_room_cells[b]=true
			8:game.hardware.exterior=false
			9:game.hardware.exterior=true
			10:game.power_blackout=true
			11:game.power_blackout=false
			12:game.placed_rooms[0].suspended=true
			13:game.placed_rooms[0].suspended=false;game.resources.power=5
			14,15,16,17,18:game.clock+=.173
			19:game.powered_room_cells.clear()
			20:game.placed_rooms.clear()
			21:game.surveyed_water.clear();game.wrecks.clear()
			22:game.placed_rooms=[{"id":"reactor","pos":a}]
			23:effect.reset()
		effect._update_mask(game)
		var expected:=original(game)
		check(effect.mask.get_data()==expected.get_data(),"Mask channels update immediately, case %d"%mode)
		images[0].texture=ImageTexture.create_from_image(expected)
		await process_frame;await RenderingServer.frame_post_draw
		check(views[0].get_texture().get_image().get_data()==views[1].get_texture().get_image().get_data(),"Native mask pixels match, case %d"%mode)
		var uploads:int=effect.mask_uploads
		for repeat in 8:effect._update_mask(game)
		check(effect.mask_uploads==uploads,"Unchanged inputs skip rebuild/upload, case %d"%mode)
		check(effect.mask_texture.get_instance_id()==texture_id,"GPU texture identity retained")
	var held:WeakRef=weakref(effect.mask_texture)
	for image in images:image.texture=null
	effect=null
	check(held.get_ref()==null,"Mask texture releases with its owner")
	for vp in views:vp.queue_free()
	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("UNDERWATER_MASK ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
