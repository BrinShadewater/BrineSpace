extends SceneTree
const Details=preload("res://rooms/floor-profiles-v1/details.gd")
const Art=preload("res://rooms/floor-profiles-v1/modern_details.gd")
const Decor=preload("res://rooms/whole-room/decoration_props.gd")
const Services=preload("res://rooms/whole-room/room_services.gd")
const Floor=preload("res://rooms/whole-room/room_floor.gd")
const OUT="res://output/gameplay-cables-20260912/"
var failures:=0
class CablePanel extends Node2D:
	var mode:="empty"
	var view
	func _draw() -> void:
		if view!=null:
			view.render_into(self,Vector2(256,280),1.0)
			return
		draw_rect(Rect2(0,0,512,512),Color("20282b"))
		if mode=="empty": return
		var id: String="cable_straight" if mode=="cable" else "pipe_straight"
		Decor.service_run(self,PackedVector2Array([Vector2(60,60),Vector2(300,60)]),8,id)
		Services.run(self,PackedVector2Array([Vector2(-60,120),Vector2(100,120)]),Color.WHITE,true,id)
		if mode=="cable": Art.stamp(self,"cable-equipment_entry",Vector2(200,200))
func _init() -> void: call_deferred("run")
func check(ok: bool,message: String) -> void:
	if not ok: failures+=1;push_error(message)
func capture(panel) -> Image:
	panel.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	return root.get_texture().get_image()
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(512,512);root.content_scale_size=root.size
	var panel:=CablePanel.new();root.add_child(panel)
	Decor.automatic_floor_art_enabled=true
	var baseline: Image=await capture(panel)
	panel.mode="cable"
	var retired: Image=await capture(panel)
	check(baseline.get_data()==retired.get_data(),"Cable aliases, service runs and bridge plates emit no pixels even with decoration enabled")
	panel.mode="pipe"
	var pipe: Image=await capture(panel)
	check(pipe.get_data()!=baseline.get_data(),"Equipment plumbing is preserved")
	Decor.automatic_floor_art_enabled=false
	var grid=preload("res://scripts/grid_canvas.gd").new()
	grid.hide();grid.process_mode=Node.PROCESS_MODE_DISABLED;root.add_child(grid)
	var checked:=0
	for entry in preload("res://scripts/room_database.gd").all_rooms().values():
		if grid._is_narrow_corridor(entry): continue
		var view=grid._bill_room_view(entry)
		for q in range(4):
			view.configure_embedded(q,[],false,0.0)
			var resolved:=Details.resolve(view,Floor.profile_for(view))
			for piece in resolved.pieces: check(not Art.retired_cable(piece.asset),"Catalog excludes retired cable "+entry.id)
			for missing in resolved.missing: check(not Art.retired_cable(missing.asset),"Retired cable is not missing equipment")
			checked+=1
			if entry.id=="data_archive":
				view.set_meta("layout_editor_preview",true);panel.view=view
				var picture: Image=await capture(panel)
				picture.save_png(OUT+"data-archive-q%d.png"%q)
				view.remove_meta("layout_editor_preview");panel.view=null
	print("DECORATIVE CABLE REMOVAL: ","PASS" if failures==0 else "FAIL"," / ",checked," room rotations, failures=",failures)
	quit(0 if failures==0 else 1)
