extends "res://tests/review_station_motion.gd"
const View := preload("res://assets/environment/upright-kelp-v1/upright_kelp_view.gd")
var destination := "res://output/upright-kelp-review/"
class Sheet extends Node2D:
	var view=View.new()
	var cell_pixels:=270.0
	var reference: Texture2D
	func _ready():
		view.prepare()
		reference=preload("res://scripts/safe_image.gd").raw_texture("res://assets/environment/seabed-refresh-v1/runtime/ribbon-kelp.png")
	func _draw():
		draw_rect(Rect2(0,0,1500,1500),Color("17292d"))
		var ids:=View.WIDTHS.keys();ids.append("installed-ribbon-kelp")
		for row in range(ids.size()):
			var id: String=ids[row]
			draw_string(ThemeDB.fallback_font,Vector2(10,25+row*350),id,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(270+col*280,310+row*350)
				draw_rect(Rect2(at-Vector2(120,275),Vector2(240,290)),Color("909c93") if col%2==0 else Color("233b41"))
				var tint:=Color.WHITE if col<2 else Color(.59,.68,.66,.85)
				if id=="installed-ribbon-kelp":
					var extent:=reference.get_size()/float(reference.get_width())*.6*cell_pixels
					draw_texture_rect(reference,Rect2(at-Vector2(0,140)-extent*.5,extent),false,tint)
				else:view.draw_asset(self,id,at,float(View.WIDTHS[id])*cell_pixels,tint)
		draw_string(ThemeDB.fallback_font,Vector2(10,1475),"Source on pale/dark | existing submerged tint on pale/dark. %.1f physical pixels/cell."%cell_pixels,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
class Samples extends Node2D:
	var view=View.new()
	var cell_size:=324.0
	func _draw():
		view.draw_asset(self,"sea-white-reed-kelp",Vector2(19.2,19.6)*cell_size,.30*cell_size)
		view.draw_asset(self,"violet-reed-kelp",Vector2(19.9,19.6)*cell_size,.28*cell_size)
		view.draw_asset(self,"emerald-reed-kelp",Vector2(20.6,19.6)*cell_size,.28*cell_size)
class SwaySheet extends Node2D:
	var view=View.new()
	var clock:=0.0
	func _draw():
		draw_rect(Rect2(0,0,1000,650),Color("233b41"))
		for i in range(View.WIDTHS.size()):
			var id: String=View.WIDTHS.keys()[i]
			draw_string(ThemeDB.fallback_font,Vector2(80+i*280,28),id,HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color.WHITE)
			for row in range(2):
				var tint:=Color.WHITE if row==0 else Color(.59,.68,.66,.85)
				view.draw_swaying_asset(self,id,Vector2(140+i*280,300+row*300),float(View.WIDTHS[id])*270,clock,i*1.8,tint)
		draw_string(ThemeDB.fallback_font,Vector2(15,640),"Native scale: source above, underwater tint below. Holdfasts fixed; eight-second sway.",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
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
		await focus(Vector2(20,19.2),zoom);samples.cell_size=game.get_cell_size();samples.queue_redraw()
		await shot("station-%d"%roundi(zoom*100))
	await focus(Vector2(20,19.2),.45)
	var measured: float=game.get_cell_size()*root.get_final_transform().get_scale().x
	var view=View.new();view.prepare()
	check(view.textures.size()==3,"All three plants load")
	for id in View.SOURCES:
		var art: Texture2D=view.textures[id]
		check(art.get_height()==1024,"Measured source density: "+id)
		check(art.get_image().get_pixel(0,0).a==0,"Transparent exterior: "+id)
	var regions: Array=[{"biome":"kelp","center":Vector2(10,10),"radius":Vector2(3,3)},{"biome":"coral","center":Vector2(30,30),"radius":Vector2(3,3)}]
	check(view.placements(regions)==view.placements(regions),"Placement stable on redraw")
	check(view.placements(regions).size()==4,"Kelp and coral habitat assignments")
	check(view.placements([{"biome":"kelp","center":Vector2(20.5,20.5),"radius":Vector2(.1,.1)}]).is_empty(),"Quiet station core retained")
	check(game.occupied.size()==2,"Decorative plants add no occupancy")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No asset placeholders")
	samples.queue_free()
	await process_frame
	var background=game.grid_view.seabed_background
	var live=view.placements(background.sub_biomes.regions)
	check(not live.is_empty(),"Production habitats contain tall plants")
	var seen: Dictionary={}
	for plant in live:
		if seen.has(plant.id):continue
		seen[plant.id]=true
		await focus(plant.at,.45)
		game.grid_view.env_below_key.clear()
		await shot("habitat-"+plant.id)
	check(seen.size()==3,"All three plants occur in production habitats")
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear()
	for cell in [Vector2i(9,28),Vector2i(11,28)]:game._place_room("battery_array",cell,true)
	game.powered_room_cells.clear();game.unpowered_room_cells.clear()
	for room in game.placed_rooms:game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	for biome in ["kelp","coral"]:
		game.site_layout={"seed":biome.hash(),"scenery":[],"habitats":[{"biome":biome,"center":Vector2(10.5,26),"radius":Vector2(2,2)}]}
		game.grid_view.env_below_key.clear();game.grid_view.prewarm_station_views(game);game._refresh_all()
		await focus(Vector2(10.5,26.8),.45)
		await shot("lit-habitat-"+biome)
	game.hide();root.content_scale_size=Vector2i(1500,1500);root.size=Vector2i(1500,1500)
	var sheet:=Sheet.new();sheet.cell_pixels=measured;sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	await process_frame;RenderingServer.force_draw(false)
	var first:=root.get_texture().get_image();first.save_png(destination+"native-density-upright-kelp.png")
	sheet.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	check(first.get_data()==root.get_texture().get_image().get_data(),"Static canopies retain pixels")
	sheet.queue_free();await process_frame
	root.content_scale_size=Vector2i(1000,650);root.size=Vector2i(1000,650)
	Settings.reduced_motion=false;Settings.effects_quality=1
	var sway:=SwaySheet.new();sway.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sway)
	await process_frame;RenderingServer.force_draw(false)
	var initial:=root.get_texture().get_image()
	sway.clock=2.0;sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	var changed:=root.get_texture().get_image()
	check(initial.get_data()!=changed.get_data(),"Rendered blades change with the clock")
	for i in range(3):
		for row in range(2):
			var id: String=View.WIDTHS.keys()[i]
			var tex: Texture2D=sway.view.textures[id]
			var width: float=View.WIDTHS[id]*270
			var height: float=width*tex.get_height()/tex.get_width()
			var rect:=Rect2i(roundi(140+i*280-width*.5)-1,ceili(300+row*300-height*.05),ceili(width)+2,maxi(1,floori(height*.07)-1))
			check(initial.get_region(rect).get_data()==changed.get_region(rect).get_data(),"Rendered holdfast stays planted: "+id)
	sway.clock=8.0;sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	check(initial.get_data()==root.get_texture().get_image().get_data(),"Eight-second loop closes exactly")
	sway.clock=2.0;sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	var frozen:=root.get_texture().get_image().get_data()
	sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	check(frozen==root.get_texture().get_image().get_data(),"Frozen clock is pixel-stable")
	Settings.reduced_motion=true
	sway.clock=1.0;sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	var reduced:=root.get_texture().get_image().get_data()
	sway.clock=3.0;sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	check(reduced==root.get_texture().get_image().get_data(),"Reduced Motion freezes all kelp")
	Settings.reduced_motion=false;Settings.effects_quality=0
	sway.clock=1.0;sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	var low:=root.get_texture().get_image().get_data()
	sway.clock=4.0;sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	check(low==root.get_texture().get_image().get_data(),"Effects off keeps static kelp")
	Settings.effects_quality=1
	game.site_layout={}
	game.running=true;game.paused=true
	var before_clock: float=game.get_visual_time_seconds()
	game._process(.25)
	check(game.get_visual_time_seconds()==before_clock,"Expedition pause freezes kelp clock")
	game.paused=false;game.time_speed_index=0;game._process(.25)
	check(is_equal_approx(game.get_visual_time_seconds()-before_clock,.25),"Normal speed advances kelp clock")
	var before_fast: float=game.get_visual_time_seconds()
	game.time_speed_index=1;game._process(.25)
	check(is_equal_approx(game.get_visual_time_seconds()-before_fast,.25*game.time_speeds[1]),"Selected speed scales kelp clock")
	game.paused=true;game.time_speed_index=0
	DirAccess.make_dir_recursive_absolute(destination+"sway-frames")
	for frame in range(240):
		sway.clock=frame/30.0;sway.queue_redraw();await process_frame;RenderingServer.force_draw(false)
		root.get_texture().get_image().save_png(destination+"sway-frames/frame-%03d.png"%frame)
	print("UPRIGHT KELP SWAY REVIEW: %d failures"%failures)
	quit(failures)
