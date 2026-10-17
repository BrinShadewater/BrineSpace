extends "res://character/james-ward-cardinal-v1/west.gd"
const RESULT:="res://character/james-ward-clearance-v1/"
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await setup_job();var actor=game.branforth_npc
	for step in range(5000):
		game._process(1.0/60.0)
		if actor.ward_animation_active() and actor.timer>=3:break
	var cell:=Vector2i(19,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384;var data:Dictionary=actor.geometry[cell];var props:Array=[];var candidates:Array=[]
	for prop in data.props:
		var rect:Rect2=prop.rect
		props.append({"id":prop.id,"rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"sortY":prop.get("sort_y",0),"floorPiece":prop.get("floor_piece",false),"wallAttachment":prop.get("wall_attachment",false),"footprint":prop.get("footprint",[])})
	for node in actor.room_nodes[cell]:
		var point:Vector2=actor.graph.get_point_position(node);var local:Vector2=point-center
		if local.x < -80 and absf(local.y)<110:
			candidates.append({"point":[point.x,point.y],"local":[local.x,local.y],"standable":actor.can_stand(point)})
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(RESULT+"west-before.png")
	var foot_view:Vector2=root.get_stretch_transform()*(game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384))
	var f:=FileAccess.open(RESULT+"probe-evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"foot":[actor.foot.x,actor.foot.y],"local":[actor.foot.x-center.x,actor.foot.y-center.y],"footViewport":[foot_view.x,foot_view.y],"props":props,"candidates":candidates},"  "));f.close()
	if not FileAccess.file_exists(RESULT+"probe.gd.uid"):
		var u:=FileAccess.open(RESULT+"probe.gd.uid",FileAccess.WRITE);u.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));u.close()
	print("JAMES WARD CLEARANCE PROBE: ",candidates.size()," candidates / ",props.size()," props");game.queue_free();quit()
