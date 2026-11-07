extends SceneTree
## Presentation-only study; no production renderer, geometry or save changes.
const Geometry = preload("res://tools/modular_room_geometry.gd")
var output := ""

class MiningStudy extends "res://rooms/production-ten/mining_drone_bay_view.gd":
	var wall_rise := 0.0
	var study_light_level := 1.0
	func shade_projection(rect: Rect2) -> void:
		if wall_rise<=0 or rect.get_center().y>=-190: return
		var bounds:=Rect2(rect.position-Vector2(0,wall_rise+3),rect.size+Vector2(0,wall_rise+4))
		bounds=bounds.intersection(Rect2(-200,-300,400,108))
		painter.draw_rect(bounds,Color(0.025,0.045,0.07,lerpf(0.72,0.0,study_light_level)))
	func draw_wall(rect: Rect2,horizontal: bool) -> void:
		if horizontal and rect.get_center().y<-190 and wall_rise>0:
			painter.draw_rect(Rect2(rect.position.x,rect.end.y-wall_rise-3,rect.size.x,wall_rise+3),Color("465256"))
			super.draw_wall(Rect2(rect.position-Vector2(0,wall_rise),rect.size),horizontal)
		else: super.draw_wall(rect,horizontal)
		if horizontal: shade_projection(rect)
	func draw_cap(rect: Rect2) -> void:
		if rect.get_center().y<-190 and wall_rise>0:
			painter.draw_rect(Rect2(rect.position.x,rect.end.y-wall_rise-3,rect.size.x,wall_rise+3),Color("354246"))
			super.draw_cap(Rect2(rect.position-Vector2(0,wall_rise),rect.size))
		else: super.draw_cap(rect)
		shade_projection(rect)

class SalvageStudy extends "res://rooms/production-ten/salvage_drone_bay_view.gd":
	var wall_rise := 0.0
	var raise_south_boundary := false
	var study_light_level := 1.0
	func shade_projection(rect: Rect2) -> void:
		if wall_rise<=0 or rect.get_center().y>=-190: return
		var bounds:=Rect2(rect.position-Vector2(0,wall_rise+3),rect.size+Vector2(0,wall_rise+4))
		bounds=bounds.intersection(Rect2(-200,-300,400,108))
		painter.draw_rect(bounds,Color(0.025,0.045,0.07,lerpf(0.72,0.0,study_light_level)))
	func draw_wall(rect: Rect2,horizontal: bool) -> void:
		if horizontal and (rect.get_center().y<-190 or (raise_south_boundary and rect.get_center().y>190)) and wall_rise>0:
			painter.draw_rect(Rect2(rect.position.x,rect.end.y-wall_rise-3,rect.size.x,wall_rise+3),Color("465256"))
			super.draw_wall(Rect2(rect.position-Vector2(0,wall_rise),rect.size),horizontal)
		else: super.draw_wall(rect,horizontal)
		if horizontal: shade_projection(rect)
	func draw_cap(rect: Rect2) -> void:
		if (rect.get_center().y<-190 or (raise_south_boundary and rect.get_center().y>190)) and wall_rise>0:
			painter.draw_rect(Rect2(rect.position.x,rect.end.y-wall_rise-3,rect.size.x,wall_rise+3),Color("354246"))
			super.draw_cap(Rect2(rect.position-Vector2(0,wall_rise),rect.size))
		else: super.draw_cap(rect)
		shade_projection(rect)

class StudyPanel extends Node2D:
	var room
	var heading := ""
	func _draw() -> void:
		draw_rect(Rect2(0,0,1600,760),Color("14282d"))
		draw_string(ThemeDB.fallback_font,Vector2(25,35),heading,HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
		draw_string(ThemeDB.fallback_font,Vector2(25,65),"PROPOSAL ONLY / same prop placements, foot position and 72-unit socket / no actor clipping",HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color("b6c7ca"))
		for column in range(3):
			var rise: float = [0.0,32.0,56.0][column]
			var origin := Vector2(270+530*column,410)
			draw_set_transform(origin,0,Vector2(1.2,1.2))
			room.painter=self
			# Elevate the real cap too: a backdrop behind the old cap reads as a ledge.
			room.wall_rise=rise
			room.draw_room_world()
			draw_set_transform(Vector2.ZERO)
			var label := "Current low cutaway" if rise==0 else "Rear backing +%d units"%int(rise)
			draw_string(ThemeDB.fallback_font,Vector2(origin.x-190,705),label,HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
		draw_string(ThemeDB.fallback_font,Vector2(25,740),"Native isolated-room study; simplified backing material. Shared neighbours, lighting and final art are not validated.",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color("b6c7ca"))

func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output=arg.trim_prefix("--output=")
	call_deferred("run")

func run() -> void:
	assert(output.begins_with("res://output/") and not DirAccess.dir_exists_absolute(output))
	DirAccess.make_dir_recursive_absolute(output)
	root.size=Vector2i(1600,760)
	root.content_scale_size=root.size
	var actor_image:=Image.new()
	var actor_path:="res://character/major-bill-v2/rotations/south.png"
	assert(actor_image.load_png_from_buffer(FileAccess.get_file_as_bytes(actor_path))==OK)
	var actor_texture:=ImageTexture.create_from_image(actor_image)
	actor_texture.set_meta("major_bill_v2",true)
	var records: Array=[]
	var failures:=0
	for kind in ["mining","salvage"]:
		var room=MiningStudy.new() if kind=="mining" else SalvageStudy.new()
		room.embedded=true
		room.hide()
		root.add_child(room)
		var panel:=StudyPanel.new()
		panel.room=room
		root.add_child(panel)
		for q in range(4):
			for socket in [false,true]:
				if socket and q%2==1: continue # No north port in these rotations.
				room.configure_embedded(q,[0] if socket else [],true,0.0)
				# Choose a real clear rear-wall foot position, without moving furniture.
				var found:=false
				for x in [-111,-80,-48,48,80,111]:
					var point:=Vector2(x,-167)
					if room.can_stand(point):
						room.actor=point
						found=true
						break
				if not found:
					failures+=1
					continue
				room.external_actor_texture=actor_texture
				room.show_actor=true
				var name:="%s-q%d-%s"%[kind,q,"exposed-socket" if socket else "sealed"]
				panel.heading=name+" / actor foot "+str(room.actor)
				panel.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				var frame:=root.get_texture().get_image()
				if frame.get_size()!=Vector2i(1600,760): failures+=1
				frame.save_png(output.path_join(name+".png"))
				var north_open:=false
				for edge in room.edges:
					if edge.horizontal and edge.center.y<-190: north_open=edge.open
				if north_open!=socket: failures+=1
				records.append({"capture":name,"foot":str(room.actor),"standable":found,"north_open":north_open,"requested_socket":socket,"renderer_sha256":FileAccess.get_sha256(room.get_script().resource_path)})
		panel.free()
		room.free()
	var report:=FileAccess.open(output.path_join("review.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"scope":"Native isolated rear-wall presentation candidates, not adopted art, shared-neighbour or gameplay acceptance","actor_sha256":FileAccess.get_sha256(actor_path),"failures":failures,"records":records},"\t"))
	print("REAR WALL STUDY: ",records.size()," comparisons; ",failures," fixture failures")
	quit(1 if failures else 0)
