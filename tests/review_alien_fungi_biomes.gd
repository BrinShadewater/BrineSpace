extends "res://tests/review_station_motion.gd"
const View := preload("res://assets/environment/alien-fungi-biomes-v1/fungi_biome_view.gd")
const Ground := preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
var destination := "res://output/alien-fungi-biomes-review/"
class Sheet extends Node2D:
	var view=View.new()
	var cell_pixels:=270.0
	var reference: Texture2D
	func _ready():
		view.prepare()
		reference=preload("res://scripts/safe_image.gd").raw_texture("res://assets/environment/ocean-floor-expansion-v1/runtime/mycelium-mat.png")
	func _draw():
		draw_rect(Rect2(0,0,1500,1480),Color("17292d"))
		var ids:=View.WIDTHS.keys();ids.append("installed-mycelium")
		for row in range(ids.size()):
			var id: String=ids[row]
			draw_string(ThemeDB.fallback_font,Vector2(10,25+row*220),id,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(270+col*280,110+row*220)
				draw_rect(Rect2(at-Vector2(120,100),Vector2(240,200)),Color("909c93") if col%2==0 else Color("233b41"))
				var tint:=Color.WHITE if col<2 else Color(.59,.68,.66,.85)
				if id=="installed-mycelium":
					var extent:=reference.get_size()/float(reference.get_width())*.65*cell_pixels
					draw_texture_rect(reference,Rect2(at-extent*.5,extent),false,tint)
				else:view.draw_prop(self,id,at,float(View.WIDTHS[id])*cell_pixels,tint)
		for row in range(2):
			var id: String="kelp-sediment" if row==0 else "fungal-sediment"
			draw_string(ThemeDB.fallback_font,Vector2(10,935+row*240),id+" / source | mirrored diagnostic | native tint | mirrored tint",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(170+col*320,955+row*240)
				var tint:=Color.WHITE if col<2 else Color(.49,.58,.57)
				var art: Texture2D=view.textures[id]
				for y in range(2):
					for x in range(2):
						var rect:=Rect2(at+Vector2(x,y)*85,Vector2(85,85))
						var flip_x:=col%2==1 and x%2==1
						var flip_y:=col%2==1 and y%2==1
						var origin:=rect.position+Vector2(85 if flip_x else 0,85 if flip_y else 0)
						draw_set_transform(origin,0,Vector2(-1 if flip_x else 1,-1 if flip_y else 1))
						draw_texture_rect(art,Rect2(Vector2.ZERO,rect.size),false,tint)
						draw_set_transform(Vector2.ZERO)
		draw_string(ThemeDB.fallback_font,Vector2(10,1450),"Measured %.1f physical pixels/cell. Mirror panels are diagnostics; live habitat fields use continuous UVs."%cell_pixels,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
class Samples extends Node2D:
	var view=View.new()
	var cell_size:=324.0
	var mesh=Ground.ground_mesh(Vector2(19.6,19.25),Vector2(.7,.45))
	func _draw():
		view.prepare()
		draw_mesh(mesh,view.textures["fungal-sediment"],Transform2D().scaled(Vector2.ONE*cell_size))
		view.draw_prop(self,"fungal-shelves",Vector2(19.3,19.2)*cell_size,.38*cell_size)
		view.draw_prop(self,"spore-rosettes",Vector2(19.8,19.4)*cell_size,.25*cell_size)
		view.draw_prop(self,"alien-sieve-pod",Vector2(20.1,19.1)*cell_size,.22*cell_size)
class PlacementProbe extends Node2D:
	var view=View.new()
	var regions: Array=[{"biome":"iron","center":Vector2(10,10),"radius":Vector2(3,3)}]
	func _draw():view.render_ground(self,100.0,regions)
func shot(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(destination+name+".png")
func run():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--out="):destination=arg.trim_prefix("--out=").trim_suffix("/")+"/"
	DirAccess.make_dir_recursive_absolute(destination)
	Settings.initialized=true;Settings.pause_unfocused=false;Settings.effects_quality=1
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://fungi-review.meta";game.run_save_path="user://fungi-review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear();game.site_layout={"seed":39,"scenery":[]}
	for identity in Architects.IDS:
		var actor=Architects.actor_for(game,identity);actor.active=false;actor.foot=Vector2.ZERO
	game.testing_free_build=true;game.testing_disable_failures=true
	for cell in [Vector2i(19,20),Vector2i(21,20)]:game._place_room("battery_array",cell,true)
	game.powered_room_cells.clear();game.unpowered_room_cells.clear()
	for room in game.placed_rooms:game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game._set_paused(true,false);game.visual_time_seconds=1.3;game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	game.grid_view.env_below_key.clear();game.grid_view.prewarm_station_views(game);game._refresh_all()
	var samples:=Samples.new();game.grid_view.env_passes[0].add_child(samples)
	for zoom in [.25,.45,.65]:
		await focus(Vector2(20,19.6),zoom);samples.cell_size=game.get_cell_size();samples.queue_redraw()
		await shot("station-%d"%roundi(zoom*100))
	await focus(Vector2(20,19.6),.45)
	var measured: float=game.get_cell_size()*root.get_final_transform().get_scale().x
	var view=View.new();view.prepare()
	check(view.textures.size()==5,"All five selected assets load")
	for id in View.SOURCES:check(view.textures.get(id)!=null,"Selected texture: "+id)
	var ground=Ground.new();ground.prepare()
	check(ground.textures["kelp-ground"].get_image().get_data()==view.textures["kelp-sediment"].get_image().get_data(),"Kelp habitat loads selected new ground pixels")
	var probe:=PlacementProbe.new();probe.position=Vector2(-2000,-2000);root.add_child(probe)
	await process_frame;RenderingServer.force_draw(false)
	var patch_count: int=probe.view.patches.size();var signature: String=probe.view.signature
	probe.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	check(patch_count==1 and probe.view.patches.size()==patch_count and probe.view.signature==signature,"Fungal placement stays stable across redraw")
	var uv: PackedVector2Array=probe.view.patches[0].mesh.surface_get_arrays(0)[Mesh.ARRAY_TEX_UV]
	check(uv[0]!=uv[1],"Continuous fungal material coordinates")
	check(game.occupied.size()==2,"New biology adds no occupancy")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No asset placeholders")
	game.hide();root.content_scale_size=Vector2i(1500,1480);root.size=Vector2i(1500,1480)
	var sheet:=Sheet.new();sheet.cell_pixels=measured;sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	await process_frame;RenderingServer.force_draw(false)
	var first:=root.get_texture().get_image();first.save_png(destination+"native-density-ground.png")
	sheet.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	check(first.get_data()==root.get_texture().get_image().get_data(),"Static biology and sediments retain pixels")
	print("ALIEN FUNGI BIOME REVIEW: %d failures"%failures)
	quit(failures)
