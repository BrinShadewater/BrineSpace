extends SceneTree
## Prescribed runtime texture scale comparisons over real room art; no actor motion claim.
class Poses extends Node2D:
	var textures:Array=[]
	var anchors:Array=[]
	var scales:Array=[]
	func _draw():
		for i in range(textures.size()):
			var texture:Texture2D=textures[i];var scale:float=scales[i]
			draw_texture_rect(texture,Rect2(anchors[i]-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale),false)
var failures:=0
var checks:=0
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
	if not OS.get_environment("APPDATA").contains("marsh-scale-density"):quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1600,900)
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	preload("res://scripts/title_settings.gd").reduced_motion=true
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://scale-density.meta";game.run_save_path="user://scale-density.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss();game.paused=true
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	var player=game.grid_view.marsh_player
	var frozen:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-scale-density-review-2026-10-14/selected-before.json"))
	check(player.frames.size()==frozen.size(),"runtime state coverage")
	var holds:=0
	for key in frozen:
		var record:Dictionary=frozen[key]
		check(player.frames[key].size()==record.files.size(),"runtime hold count "+key)
		check(player.timing[key].durations==record.state.frameDurationsMs and player.timing[key].loop==record.state.loop,"runtime clocks "+key)
		for i in range(record.files.size()):
			var texture:Texture2D=player.frames[key][i]
			var image:=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+str(record.files[i].path)))
			check(texture.get_image().get_data()==image.get_data(),"runtime pixels "+key+"/"+str(i))
			check(float(texture.get_meta("crew_standing_height"))==148,"runtime standing ruler")
			check(Vector2(texture.get_meta("crew_pivot"))==Vector2(record.metadata.pivot[0],record.metadata.pivot[1]),"runtime pivot")
			holds+=1
	check(game.grid_view.texture_filter==CanvasItem.TEXTURE_FILTER_NEAREST,"renderer samples nearest")
	var cell:=Vector2i(20,20)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game._place_room("galley",cell,true);game.powered_room_cells[cell]=true
	game.selected_room_cell=cell;game._refresh_all();game.hand_panel.hide()
	var layer:=CanvasLayer.new();layer.layer=1000;root.add_child(layer)
	var view:=Poses.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;layer.add_child(view)
	var marker:=ColorRect.new();marker.size=Vector2(8,8);layer.add_child(marker)
	var output:="res://character/marsh-scale-density-review-2026-10-14/native/"
	DirAccess.make_dir_recursive_absolute(output)
	var cases:Array=[["idle-south",0],["eat-south",3],["carry-south",2]];var captures:Array=[]
	for zoom_case in [["fit",.32],["normal",game.DEFAULT_GRID_ZOOM*.52],["close",game.MAX_GRID_ZOOM]]:
		var camera:Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
		game._set_grid_zoom(zoom_case[1],true,camera);game.grid_view.queue_redraw()
		var settled:=false
		for attempt in range(180):
			await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
			if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:settled=true;break
		check(settled,"room/camera settled "+str(zoom_case[0]))
		view.textures=[];view.anchors=[];view.scales=[]
		# CanvasLayer drawing already receives the viewport's final transform.
		# Supply logical canvas coordinates here, not twice-transformed screen ones.
		var transform:Transform2D=game.grid_view.get_global_transform_with_canvas()
		for i in range(cases.size()):
			var texture:Texture2D=player.frames[cases[i][0]][cases[i][1]]
			var world:Vector2=(Vector2(cell)+Vector2.ONE*.5+Vector2((i-1)*.25,.05))*game.get_cell_size()
			view.textures.append(texture);view.anchors.append(transform*world)
			view.scales.append(game.get_cell_size()*.17/148*transform.get_scale().y)
		view.queue_redraw();marker.color=Color8(51+captures.size(),99,155)
		var image:Image
		for attempt in range(20):
			await process_frame;await RenderingServer.frame_post_draw;image=root.get_texture().get_image()
			if image.get_pixel(2,2).is_equal_approx(marker.color):break
		check(image.get_pixel(2,2).is_equal_approx(marker.color),"current native pose comparison drawn")
		check(image.save_png(output+str(zoom_case[0])+".png")==OK,"native room comparison saved")
		var screen_transform:Transform2D=root.get_final_transform()
		for anchor in view.anchors:
			var screen:Vector2=screen_transform*Vector2(anchor)
			check(screen.x>300 and screen.x<1000 and screen.y>200 and screen.y<750,"comparison anchors stay inside room viewport")
		captures.append({"zoom":zoom_case[0],"actualGridZoom":game.grid_zoom,"nominalStandingScreenPixels":view.scales[0]*148*screen_transform.get_scale().y,"cases":cases})
	check(not game.testing_free_build and not game.testing_disable_failures,"normal economy/failure flags retained")
	var file=FileAccess.open(output+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"states":frozen.size(),"holds":holds,"captures":captures,"scope":"All runtime source pixels/clocks/pivots/rulers; three prescribed idle/eat/carry texture overlays against real galley at fit/normal/close zoom. Not actor placement, live motion, furniture acceptance or release validation."},"\t"));file.close()
	print("MARSH SCALE/DENSITY: ",checks," checks, ",failures," failures; ",holds," holds; 3 room comparisons")
	layer.queue_free();await process_frame;quit(1 if failures else 0)
