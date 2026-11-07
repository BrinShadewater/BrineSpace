extends SceneTree
const Library=preload("res://scripts/room_asset_library.gd")
var failures:=0
var checks:=0
class Preview extends Node2D:
	var room
	var host
	var retained:=false
	var draws:=0
	func _draw():
		room.retained_content_host=null
		room.shell_pass=1
		room.render_into(self,Vector2(256,290),1.06,false,true)
		host.visible=retained
		room.retained_content_host=host if retained else null
		room.shell_pass=2
		room.render_into(self,Vector2(256,290),1.06,false,false)
		draws+=1
func _init():call_deferred("run")
func check(ok: bool,label: String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func capture(preview,retained: bool) -> Image:
	preview.retained=retained
	var before: int=preview.draws
	var paints: int=preview.host.static_redraws+preview.host.live_redraws
	preview.queue_redraw()
	for unused in range(12):
		await process_frame
		await RenderingServer.frame_post_draw
		if preview.draws>before and (not retained or preview.host.static_redraws+preview.host.live_redraws>paints):return root.get_texture().get_image()
	check(false,"Renderer did not produce the requested frame")
	return root.get_texture().get_image()
func run():
	if DisplayServer.get_name()=="headless":push_error("Bunk layer parity requires native rendering");quit(1);return
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	var room=preload("res://rooms/whole-room/crew_hab_view.gd").new()
	room.embedded=true;room.hide();root.add_child(room)
	room.configure_embedded(3,[],false,0)
	# Isolate the source prop rather than requiring an owner save layout.
	room.set_meta("layout_editor_preview",true)
	var bunk:=Library.template("library/tileset-mb2-14").duplicate(true)
	bunk.rect=Rect2(72,-126,72.46131,73.99651);bunk.sort_y=bunk.rect.end.y
	room.props=[bunk]
	var preview=Preview.new();preview.room=room;preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	var host=preload("res://scripts/room_content_canvas.gd").new()
	host.draw_origin=Vector2(256,290);host.draw_scale=1.06;preview.host=host
	root.add_child(preview);preview.add_child(host)
	var original: PackedByteArray=bunk.library_texture.get_image().get_data()
	var layers:=Library.bunk_layers(bunk)
	check(layers.size()==2,"Bunk provides back/front layers")
	check(bunk.library_texture.get_image().get_data()==original,"Source atlas unchanged")
	check(is_same(layers[0].prop.library_texture,Library.bunk_layers(bunk)[0].prop.library_texture),"Layer textures cached")
	check(Library.bunk_layers({"id":"other"}).is_empty(),"Unrelated props not split")
	# Current runtime art supplies the pixels; furniture opt-in is deliberately local.
	var image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(image,"res://character/dr-veld-v2/frames/bare/sleep-east/000.png")
	var texture=ImageTexture.create_from_image(image)
	texture.set_meta("crew_pivot",Vector2(128,224));texture.set_meta("crew_standing_height",148)
	texture.set_meta("crew_depth_offset",96);texture.set_meta("crew_bunk_layer",true)
	var position=Vector2(112,-70)
	check(is_equal_approx(room.actor_draw_depth(position,texture),float(bunk.sort_y)+0.01),"Opt-in sleeper between layers")
	texture.set_meta("crew_bunk_layer",false)
	check(is_equal_approx(room.actor_draw_depth(position,texture),position.y+96),"Generic pose depth unchanged")
	texture.set_meta("crew_bunk_layer",true)
	for flip in [Vector2.ONE,Vector2(-1,1)]:
		bunk.layout_flip=flip
		room.external_actors=[]
		room.split_bunk_layers=false
		var unsplit: Image=await capture(preview,false)
		room.split_bunk_layers=true
		var split: Image=await capture(preview,false)
		check(unsplit.get_data()==split.get_data(),"Empty split exact RGBA parity "+str(flip))
		room.prop_queue_sources=[]
		var retained: Image=await capture(preview,true)
		check(split.get_data()==retained.get_data(),"Empty retained/direct parity "+str(flip))
		room.external_actors=[{"position":position,"texture":texture}]
		var direct: Image=await capture(preview,false)
		retained=await capture(preview,true)
		check(direct.get_data()==retained.get_data(),"Occupied retained/direct parity "+str(flip))
		var builds: int=room.prop_queue_builds
		room._sorted_content_queue([])
		check(room.prop_queue_builds==builds,"Stable queue reused")
	bunk.layout_flip=Vector2.ONE
	room._sorted_content_queue([])
	var changed: int=room.prop_queue_builds
	bunk.rect.position.x-=12
	var moved: Array=room._sorted_content_queue([])
	check(room.prop_queue_builds==changed+1,"Horizontal move rebuilds layer copies")
	check(moved[0].prop.rect==bunk.rect,"Moved layer tracks owner position")
	var variant=bunk.duplicate();variant.copy_source=bunk.id;variant.variant_source="other"
	check(Library.bunk_layers(variant).is_empty(),"Variant art takes precedence over copied source identity")
	print("BUNK LAYERS: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
