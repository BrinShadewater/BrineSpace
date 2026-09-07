extends SceneTree
const Architects=preload("res://scripts/architects.gd")
const View=preload("res://rooms/underwater/brine-core/brine_core_view.gd")
const CELL=Vector2i(20,20)
var OUT="res://output/brine-collar-v6"
var review_only:=false
var game
var failures:=0
var steps:=0
func _init() -> void:
	review_only="--review-only" in OS.get_cmdline_user_args()
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--output="):
			OUT=argument.trim_prefix("--output=")
			if not OUT.begins_with("res://output/") or DirAccess.dir_exists_absolute(OUT):
				push_error("Use a fresh res://output directory for BRINE review")
				quit(1)
				return
	call_deferred("run")
func check(value: bool, message: String) -> void:
	if not value:
		failures+=1
		if failures<15: push_error(message)
func settle() -> void:
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
func room_pixels() -> Image:
	var local:=Rect2(Vector2(CELL)*game.get_cell_size(),Vector2.ONE*game.get_cell_size())
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local
	return root.get_texture().get_image().get_region(Rect2i(screen))
func tank_pixels() -> PackedByteArray:
	var view=game.grid_view.brine_view
	var prop: Dictionary=view.props.filter(func(p): return p.id=="brine_chamber")[0]
	var scale: float=game.get_cell_size()/384.0
	var source:=Rect2(548,574,158,200)
	var local:=Rect2(game._cell_center(CELL)+view.life_point(prop,source.position)*scale,source.size*(prop.rect.size.x/prop.registration.width)*scale)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local
	return root.get_texture().get_image().get_region(Rect2i(screen)).get_data()
func capture(label: String, full:=false) -> Image:
	game.grid_view.queue_redraw()
	await settle()
	var result:=room_pixels()
	result.save_png(OUT.path_join(label+".png"))
	if full: root.get_texture().get_image().save_png(OUT.path_join(label+"-station.png"))
	return result
class Card extends Node2D:
	var view
	func _draw() -> void:
		view.configure_embedded(0,[],false,0)
		view.render_into(self,Vector2(256,256),1.16)
func bake_card() -> void:
	var viewport:=SubViewport.new()
	viewport.size=Vector2i(512,512)
	viewport.transparent_bg=true
	viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(viewport)
	var view:=View.new()
	view.embedded=true
	view.visible=false
	view.architect_pod={"recovered":true}
	viewport.add_child(view)
	var card:=Card.new()
	card.view=view
	viewport.add_child(card)
	await settle()
	var path:=OUT.path_join("review-card.png") if review_only else "res://rooms/underwater/brine-core/renewal-v2/core-card-v6.png"
	viewport.get_texture().get_image().save_png(path)
	viewport.queue_free()
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	var prefix: String="user://brine_room_v2_%d" % OS.get_process_id()
	game.meta.save_path=prefix+".meta"
	game.run_save_path=prefix+".loop"
	game.Preferences.save_path=prefix+".cfg"
	game.meta.selected_architect="bill"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	# Normal recovery entry point supplies the actor; four free fixture corridors test ports.
	Architects.advance_core(game,7)
	check(game.bill_npc.active and Architects.present(game,"bill"),"Bill must emerge before traversal")
	for d in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
		var cell: Vector2i=CELL+d
		game.wrecks.erase(cell)
		if not game.occupied.has(cell): game._place_room("corridor",cell,true)
		game.occupied[cell].rotation=1 if d.x!=0 else 0
	game.paused=true
	var view=game.grid_view.brine_view
	var actor=game.bill_npc
	var center: Vector2=(Vector2(CELL)+Vector2.ONE*0.5)*384.0
	for q in range(4):
		game.occupied[CELL].rotation=q
		actor.rebuild(game)
		view.configure_embedded(q,[0,1,2,3],true,0)
		check(view.props.size()==6,"Tank, pod, pedestal and three computer assemblies registered")
		for prop in view.props:
			check(Rect2(-180,-180,360,360).encloses(view.prop_visual_bounds(prop)),"Contained furniture q%d: %s" % [q,prop.id])
		for side in range(4):
			var d: Vector2=Vector2([Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][side])
			var target:=center+d*224.0
			var source_id: int=actor.graph.get_closest_point(actor.foot)
			var target_id: int=actor.graph.get_closest_point(target)
			actor.path=actor.graph.get_point_path(source_id,target_id)
			check(not actor.path.is_empty(),"Door route exists q%d side%d" % [q,side])
			for i in range(500):
				if actor.path.is_empty(): break
				actor.move(0.05)
				check(actor.can_stand(actor.foot),"Production movement stays clear")
				steps+=1
			check(actor.foot.distance_to(actor.graph.get_point_position(target_id))<1,"Production mover reaches each entrance")
			# Return to a clear spot south of the tank without teleporting.
			var return_id: int=actor.graph.get_closest_point(center+Vector2(0,104))
			actor.path=actor.graph.get_point_path(target_id,return_id)
			for i in range(500):
				if actor.path.is_empty(): break
				actor.move(0.05)
				check(actor.can_stand(actor.foot),"Return route stays clear")
				steps+=1
			check(actor.foot.distance_to(actor.graph.get_point_position(return_id))<1,"Return from each entrance reaches tank observation area")
	var chamber: Dictionary=view.props.filter(func(p): return p.id=="brine_chamber")[0]
	var used: Rect2=Rect2(view.body_texture.get_image().get_used_rect())
	var glass:=Rect2(555,585,142,190)
	for i in range(880):
		var at: Vector2=view.BODY_RECT.position+view.float_offset(i*0.1)
		var visible:=Rect2(at+used.position*view.BODY_RECT.size/92.0,used.size*view.BODY_RECT.size/92.0)
		check(glass.encloses(visible),"Entire floating silhouette stays below cap and inside glass")
	var old_visible:=Rect2(Vector2(511,550)+used.position*2.5+Vector2(0,-5),used.size*2.5)
	check(not glass.encloses(old_visible),"Containment test rejects previous head-through-cap placement")
	var visible_bubbles:=0
	for i in range(900):
		var marks: Array=view.effect_marks(chamber,i/100.0)
		check(marks.size()<=1,"At most one bubble")
		visible_bubbles+=int(not marks.is_empty())
	check(visible_bubbles<200 and visible_bubbles>100,"Bubble occupies less than a quarter of its nine-second interval")
	if DisplayServer.get_name()!="headless":
		root.mode=Window.MODE_WINDOWED
		root.borderless=false
		root.size=Vector2i(1600,900)
		game._set_paused(true,false)
		game.selected_card_id=""
		game.hovered_card_id=""
		game.selected_room_cell=Vector2i(-1,-1)
		game.hover_cell=Vector2i(-1,-1)
		game._refresh_all()
		game._set_grid_zoom(0.8)
		await settle()
		game._center_grid_on_station_now()
		await settle()
		for q in range(4):
			game.occupied[CELL].rotation=q
			game.powered_room_cells[CELL]=true
			game.grid_view.room_light_levels[CELL]=1.0
			game.visual_time_seconds=0.2
			var before:=await capture("q%d-on-a" % q,true)
			game.visual_time_seconds=2.0
			var after:=await capture("q%d-on-b" % q)
			check(before.get_data()!=after.get_data(),"Floating changes native pixels")
			var held:=await capture("q%d-paused" % q)
			check(after.get_data()==held.get_data(),"Pause freezes native room pixels")
			game.powered_room_cells.erase(CELL)
			await capture("q%d-off-a" % q)
			var off:=tank_pixels()
			game.visual_time_seconds=5.0
			await capture("q%d-off-b" % q)
			check(off==tank_pixels(),"Offline float and bubbles stop; crew animation remains independent")
		game.occupied[CELL].rotation=0
		game.powered_room_cells[CELL]=true
		for i in range(36):
			game.visual_time_seconds=i*0.25
			await capture("float-%02d" % i)
		for width in [1280,2560]:
			root.size=Vector2i(width,roundi(width*9.0/16))
			await settle()
			game._center_grid_on_station_now()
			await capture("size-%d" % width,true)
			check(root.get_texture().get_image().get_width()==width,"Actual viewport size")
		await bake_card()
	game.free()
	for suffix in [".meta",".loop",".cfg"]:
		if FileAccess.file_exists(prefix+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(prefix+suffix))
	print("BRINE ROOM V2 %s: 4 rotations, 16 door entries and returns, %d movement samples; sparse bubbles%s" % ["PASS" if failures==0 else "FAIL",steps,"; native motion/offline/pause and 3 viewport sizes" if DisplayServer.get_name()!="headless" else ""])
	quit(0 if failures==0 else 1)
