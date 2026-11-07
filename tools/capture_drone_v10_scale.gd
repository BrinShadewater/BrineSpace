extends SceneTree
## Review fixture only: production room/crew and proposed v10 NPC widths.
const Grid = preload("res://scripts/grid_canvas.gd")
const DB = preload("res://scripts/room_database.gd")
const ScaleCrew = preload("res://scripts/room_scale_preview.gd")
const OUT = "res://output/drone-npc-pilot-2026-09-26"
const SOURCE = "C:/Users/Alex/Desktop/Projects/Gaming/Brine Space Art/BrineSpace Clean Prop Exports/drone-animation-bases/approved-v10/sources/construction-base.png"

class DroneScalePanel extends Node2D:
	var room
	var crew
	var drone: Texture2D
	var width: float
	var origin: Vector2
	func _draw() -> void:
		room.configure_embedded(0,[],false,0.0)
		room.set_meta("raised_north_visible",true)
		room.render_into(self,origin,1.0,true)
		crew.rebuild(room,"construction_drone_bay",0)
		crew.foot=Vector2(-48,62)
		crew.visible=true
		room.external_actors=crew.members()
		draw_set_transform(origin)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self,"construction_drone_bay",Vector2i.ZERO,false,false,room)
		room.render_into(self,origin,1.0,false,false)
		room.external_actors.clear()
		draw_set_transform(origin)
		var size=Vector2(width,width*drone.get_height()/drone.get_width())
		draw_texture_rect(drone,Rect2(Vector2(36,43)-size*0.5,size),false)
		draw_set_transform(Vector2.ZERO)
		draw_string(ThemeDB.fallback_font,origin+Vector2(-180,-223),"Construction / %.1f world units wide"%width,HORIZONTAL_ALIGNMENT_LEFT,-1,18)

func _init() -> void: call_deferred("run")

func run() -> void:
	root.size=Vector2i(1320,530)
	root.content_scale_size=root.size
	var bg=ColorRect.new()
	bg.size=root.size
	bg.color=Color("17272e")
	root.add_child(bg)
	var image=Image.new()
	if image.load(SOURCE)!=OK:
		quit(1)
		return
	image=image.get_region(image.get_used_rect())
	var drone=ImageTexture.create_from_image(image)
	var grid=Grid.new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var widths=[28.9,48.0,69.12]
	for i in range(widths.size()):
		var p=DroneScalePanel.new()
		p.room=grid._bill_room_view(DB.get_room("construction_drone_bay"))
		p.crew=ScaleCrew.new()
		p.crew.load_art()
		p.crew.mode=1
		p.drone=drone
		p.width=widths[i]
		p.origin=Vector2(220+i*440,275)
		root.add_child(p)
	await process_frame
	RenderingServer.force_draw(false)
	DirAccess.make_dir_recursive_absolute(OUT)
	var error=root.get_texture().get_image().save_png(OUT+"/construction-room-scale.png")
	print("DRONE SCALE CAPTURE: ",error," widths=",widths,"; production room and Bill; review overlay, not collision acceptance")
	quit(0 if error==OK else 1)
