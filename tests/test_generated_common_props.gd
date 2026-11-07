extends SceneTree
## Native catalog -> Studio -> saved layout -> live room regression and scale review.
const Library = preload("res://scripts/room_asset_library.gd")
const Store = preload("res://scripts/room_layout_store.gd")
const Editor = preload("res://scripts/room_layout_editor.gd")
const Actor = preload("res://scripts/room_scale_preview.gd")
const Room = preload("res://rooms/whole-room/reactor_view.gd")
const NorthWall = preload("res://rooms/whole-room/north_wall.gd")
const OUT = "res://output/generated-common-install-2026-09-27"
var failures := 0
var checks := 0
var room
var actor = Actor.new()
var canvas: Review
var caption := ""

class Review extends Control:
	var host
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("101a20"))
		if host.room == null: return
		host.room.render_into(self,Vector2(800,490),1.65,true)
		draw_set_transform(Vector2(800,490),0,Vector2.ONE*1.65)
		NorthWall.draw_into(self,"reactor",Vector2i.ZERO,false,false,host.room,false)
		host.room.external_actors=host.actor.members()
		host.room.render_into(self,Vector2(800,490),1.65,false,false)
		host.room.external_actors.clear()
		draw_set_transform(Vector2.ZERO)
		draw_string(ThemeDB.fallback_font,Vector2(40,36),host.caption,HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)

func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	checks+=1
	if not ok: failures+=1; push_error(message)
func capture(name: String) -> void:
	canvas.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+"/"+name+".png")

func empty_layout() -> Dictionary:
	var draft: Dictionary={"__free_placement":true}
	for prop in room.props: draft[str(prop.id)]=null
	return draft

func apply_layout(draft: Dictionary, quarter: int) -> void:
	Store.data={Store.key(Store.asset_for(room),quarter):draft}
	Store.revision+=1
	room.configure_embedded(quarter,[0,1,2,3],true,0.0)
	Store.apply(room,Store.asset_for(room))
	Library.strip_retired(room)
	actor.rebuild(room,"reactor",quarter)

func run() -> void:
	if DisplayServer.get_name()=="headless": quit(2); return
	if OS.get_environment("BRINE_COMMON_TEST")!="isolated":
		print("SKIP: run python tools/check_generated_common_props.py for isolated native verification"); quit(2); return
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900); root.content_scale_size=root.size
	Store.path="user://generated-common-layouts.json"
	Store.defaults_path="user://empty-defaults.json"
	Store.loaded=true; Store.data={}
	var ids: Array=[]
	for id in Library.entries():
		if str(id).begins_with("library/sp-generated-"): ids.append(id)
	check(ids.size()==112,"All 112 selected props registered")
	for id in ids:
		var entry: Dictionary=Library.entries()[id]
		var prop:=Library.template(id)
		check(not prop.is_empty(),"Template loads "+id)
		check(entry.group=="station" and entry.category=="common","Active Common catalog "+id)
		check(not Store.is_common_decoration(prop) and Library.keeps_in_room("reactor",prop),"Not filtered as retired/common dressing "+id)
		check(prop.library_texture.get_size()==Vector2(entry.data.region[2],entry.data.region[3]),"Native calibrated texture "+id)
		check(is_equal_approx(prop.rect.size.x,float(entry.width)),"Calibrated world width "+id)
	# Exercise the actual Common tray and normal add/save actions.
	var editor=Editor.open(root)
	await process_frame
	editor.autosave_enabled=false
	editor.library_filter.select(Editor.TRAY_COMMON)
	editor.library_search.text=""; editor.rebuild_library()
	var offered: Array=[]
	for i in range(editor.library_list.item_count): offered.append(editor.library_list.get_item_metadata(i))
	for id in ids: check(offered.has(id),"Common tray offers "+id)
	var until:=Time.get_ticks_msec()+20000
	while (not editor.thumbnail_queue.is_empty() or editor.thumbnail_render_busy or not editor.thumbnail_active.is_empty()) and Time.get_ticks_msec()<until:
		await process_frame
	for id in ids: check(Library.entries()[id].get("preview_ready",false),"Rendered tray thumbnail "+id)
	var sample_id: String="library/sp-generated-common-comms-panel"
	editor.draft["wall/riser"]="engineering"
	editor.free_placement.button_pressed=false
	check(editor.add_library_asset(sample_id,Vector2(-110,-220)),"Studio mounts wall panel in constrained mode")
	check(editor.issues().is_empty(),"Mounted panel fits raised-wall envelope")
	var mounted:=Library.template(sample_id)
	check(mounted.get("wall_attachment",false) and mounted.collision_boxes.is_empty(),"Wall attachment has no floor collision")
	check(preload("res://tools/modular_room_geometry.gd").prop_collision_rects(mounted).is_empty(),"Navigation gives the wall panel no fallback blocker")
	var saved_asset: String=Store.asset_for(editor.room)
	var saved_q: int=editor.quarter
	editor.save_layout()
	Store.loaded=false; Store.data={}
	check(Store.positions(saved_asset,saved_q).has(sample_id),"Studio wall mount survives disk reload")
	editor.library_search.text="Comms"; editor.rebuild_library()
	var scroll: Node=editor.library_list.get_parent()
	while scroll!=null and not scroll is ScrollContainer: scroll=scroll.get_parent()
	if scroll is ScrollContainer: scroll.scroll_vertical=2000
	await process_frame; await RenderingServer.frame_post_draw
	if scroll is ScrollContainer: scroll.scroll_vertical=2000
	await process_frame; await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(OUT+"/studio-common.png")
	editor.dirty=false; editor.rotation_drafts.clear(); editor.close_editor()
	await process_frame
	paused=false
	# The saved Studio addition must also arrive through the actual gameplay scene.
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://generated-common.loop"; game.meta.save_path="user://generated-common.meta"
	root.add_child(game); current_scene=game
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	game.occupied.clear(); game.placed_rooms.clear(); game.wrecks.clear()
	game._place_room("research_lab",Vector2i(20,20),true)
	game.selected_card_id=""; game._refresh_all()
	await process_frame
	game._fit_station_view()
	await process_frame; await RenderingServer.frame_post_draw
	var live=game.grid_view._bill_room_view({"id":"research_lab"})
	check(live.props.any(func(p):return p.id==sample_id),"Studio-saved wall panel reaches actual gameplay")
	root.get_texture().get_image().save_png(OUT+"/gameplay-saved-panel.png")
	game.queue_free(); await process_frame
	current_scene=null; paused=false
	root.content_scale_factor=1.0; root.content_scale_size=root.size
	room=Room.new(); room.embedded=true; root.add_child(room); room.hide()
	room.configure_embedded(0,[0,1,2,3],true,0.0)
	var base:=empty_layout()
	actor.load_art(); actor.mode=2; actor.visible=true
	canvas=Review.new(); canvas.host=self; canvas.size=Vector2(1600,900)
	canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST; root.add_child(canvas)
	# Each new prop independently survives the production layout/retirement filters
	# in every room rotation, with a path between all four doorway approach points.
	for q in range(4):
		for id in ids:
			var draft:=base.duplicate(true); draft[id]=[-180,-190]
			apply_layout(draft,q)
			var present: Array=room.props.filter(func(p):return p.id==id)
			check(present.size()==1,"Live room retains %s q%d"%[id,q])
			for at in [Vector2(0,-160),Vector2(160,0),Vector2(0,160),Vector2(-160,0)]:
				check(actor.can_stand(at),"Door approach clear %s q%d %s"%[id,q,at])
				var route: PackedVector2Array=actor.graph.get_point_path(actor.graph.get_closest_point(Vector2.ZERO),actor.graph.get_closest_point(at))
				check(route.size()>1,"Door route exists %s q%d"%[id,q])
			if present.size()==1 and present[0].has("corner"):
				var prop: Dictionary=present[0]
				var inside: Vector2=prop.rect.position+prop.rect.size*Vector2(0.5,0.75)
				check(actor.can_stand(inside),"L-counter recess is walkable "+id)
		await process_frame
		print("Generated common rotation %d: %d live placements checked"%[q,ids.size()])
	# Three furnished scale/clearance pilots, shown through the native room renderer.
	var pilots: Array=[
		{"corner-wood-refined":[-180,-190],"corner-sink-refined":[60,-190],"plant-tall-ficus":[125,55],"seat-utility-chair-blue":[-130,-65],"surface-small-side-table":[-85,-65]},
		{"dining-kitchen-four-seats":[-180,-180],"common-compact-fridge":[105,-175],"counter-galley-prep":[70,60],"plant-trough":[70,140]},
		{"lounge-blue-reading-chair":[-180,-170],"metal-samples-east":[60,-190],"storage-book-shelf":[-175,130],"plant-tall-palm":[125,55],"seat-task-chair-metal":[-95,-75]},
		{"common-server-cabinet":[-180,-175],"common-server-pedestal":[80,-175],"common-comms-console":[65,60],"common-comms-panel":[-130,-242],"common-shelf-supplies":[-175,95],"common-shelf-personal":[70,115],"utility-water-cooler":[-90,-175]},
		{"utility-supply-crates":[-175,-175],"utility-wooden-crate":[-95,-165],"utility-fire-station":[70,-175],"utility-hvac":[-175,85],"utility-air-scrubber":[110,90],"utility-emergency-cabinet":[115,-175],"utility-maintenance-cart":[-100,135]}
	]
	for i in range(pilots.size()):
		for q in range(4):
			var draft:=base.duplicate(true)
			for key in pilots[i]: draft["library/sp-generated-"+key]=pilots[i][key]
			# Existing accepted prop remains beside the new furniture for scale comparison.
			if i<3: draft["library/sp-crew_lounge-1"]=[-175,35]
			if i>=3: draft["wall/riser"]="engineering"
			apply_layout(draft,q)
			actor.place(Vector2.ZERO)
			var travelled:=0.0
			for step in range(100):
				var before: Vector2=actor.foot
				actor.advance(0.1)
				travelled+=before.distance_to(actor.foot)
				check(actor.segment_clear(before,actor.foot),"Pilot walking clearance %d q%d"%[i,q])
			check(travelled>80,"Pilot walks beyond a standing pose %d q%d"%[i,q])
			actor.mode=1; actor.moving=false; actor.direction="south"
			actor.place(Vector2(-70,-95) if i==0 else Vector2(0,30))
			caption="Generated common props | pilot %d | rotation %d | existing furniture + Bill"%[i+1,q]
			await capture("pilot-%d-q%d"%[i+1,q])
			actor.mode=2
	print("GENERATED COMMON PROPS: %d checks, %d failures; %d assets, Studio save/reload, %d live placements, %d native pilot captures"%[checks,failures,ids.size(),ids.size()*4,pilots.size()*4])
	quit(1 if failures else 0)
