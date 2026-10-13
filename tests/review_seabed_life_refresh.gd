extends "res://tests/review_station_motion.gd"
const DEST="res://output/seabed-life-refresh-v1/"
const View=preload("res://assets/environment/sub-biomes-v1/sub_biome_view.gd")
const IDS=["kelp-holdfast","nodules-brittle-stars","iron-hydroids"]
const Fronds=preload("res://scripts/ambient_fronds.gd")
class Sheet extends Node2D:
	var view=View.new()
	var clock:=2.0
	var old: Dictionary={}
	func _ready():
		view.prepare()
		old["kelp-holdfast"]=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/assets/environment/sub-biomes-v1/kelp-holdfast-v1.png")
		old["nodules-brittle-stars"]=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/assets/environment/sub-biomes-v1/nodules-brittle-stars-v1.png")
		old["iron-hydroids"]=preload("res://scripts/safe_image.gd").raw_texture("res://legacy/default/assets/environment/sub-biomes-v1/iron-hydroids-v1.png")
	func _draw():
		draw_rect(Rect2(0,0,1200,640),Color("17292d"))
		for row in range(3):
			var identity: String=IDS[row]
			draw_string(ThemeDB.fallback_font,Vector2(16,25+row*210),identity+" / old | new source | new tint | dark seabed — 120px",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
			for col in range(4):
				var at:=Vector2(150+col*300,110+row*210)
				draw_rect(Rect2(at-Vector2(135,75),Vector2(270,150)),Color("233b41") if col==3 else Color("8b9a91"))
				var tex: Texture2D=old[identity] if col==0 else view.textures[identity]
				var extent:=Vector2(120,120.0*tex.get_height()/tex.get_width())
				var tint:=Color.WHITE if col<2 else Color(.59,.68,.66,.85)
				if row==2 and col>=2:Fronds.draw(self,tex,Rect2(at-extent*.5,extent),clock,1.3,tint)
				else:draw_texture_rect(tex,Rect2(at-extent*.5,extent),false,tint)
class Samples extends Node2D:
	var view=View.new()
	var size_value:=200.0
	func _ready():
		view.regions=[]
		for i in range(3):view.regions.append({"biome":["kelp","nodules","iron"][i],"center":Vector2(19.5+i,19.3),"radius":Vector2(.55,.55)})
		view.prepare();view.props.clear()
		for i in range(3):view.props.append({"id":IDS[i],"at":Vector2(19.5+i,19.3),"size":.48})
	func _draw():view.render_into(self,size_value,1.3)
func capture(name: String):
	await draw_frame();await draw_frame()
	root.get_texture().get_image().save_png(DEST+name+".png")
func sheet_capture(sheet,name: String):
	sheet.queue_redraw();await process_frame;RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(DEST+name+".png")
	return root.get_texture().get_image().get_region(Rect2i(615,455,570,150)).get_data()
func run():
	DirAccess.make_dir_recursive_absolute(DEST)
	Settings.save_path="user://seabed-life-review.cfg";Settings.pause_unfocused=false;Settings.effects_quality=1;Settings.reduced_motion=false
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://seabed-life-review.meta";game.run_save_path="user://seabed-life-review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	root.content_scale_size=Vector2i(1920,1080);root.size=Vector2i(1600,900)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.drone_fleet.restore(null)
	game.architect_run={};game.recovered_crew.clear();game.site_layout={"scenery":[],"seed":32}
	for identity in Architects.IDS:
		var actor=Architects.actor_for(game,identity)
		actor.active=false;actor.foot=Vector2.ZERO
	game.testing_free_build=true;game.testing_disable_failures=true
	for cell in [Vector2i(19,20),Vector2i(21,20)]:game._place_room("battery_array",cell,true)
	game.test_walker_cell=Vector2i(-1,-1)
	game.powered_room_cells.clear();game.unpowered_room_cells.clear()
	for room in game.placed_rooms:game.powered_room_cells[room.pos]=true;game.grid_view.room_light_levels[room.pos]=1.0
	game.visual_time_seconds=1.3;game._set_paused(true,false);game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
	game.grid_view.env_below_key.clear();game.grid_view.prewarm_station_views(game);game._refresh_all()
	var samples:=Samples.new();game.grid_view.env_passes[0].add_child(samples)
	for zoom in [.25,.45]:
		await focus(Vector2(20.5,19.8),zoom)
		samples.size_value=game.get_cell_size();samples.queue_redraw()
		await capture("station-%02d"%roundi(zoom*100))
	await focus(Vector2(21.5,19.5),.65);samples.size_value=game.get_cell_size();samples.queue_redraw()
	await capture("hydroids-close")
	var normal=View.new();normal.prepare()
	var repeated=View.new();repeated.prepare()
	check(normal.textures.size()==21,"All habitat textures load")
	check(normal.props==repeated.props,"Replacement preserves deterministic decoration")
	for identity in IDS:
		check(normal.textures[identity].get_width()==512,"Selected habitat sprite uses 512px source")
		check(normal.textures[identity].get_image().detect_alpha()!=Image.ALPHA_NONE,"Selected habitat sprite retains alpha")
	check(View.SELECTED_PATHS["kelp-holdfast"]=="res://assets/environment/seabed-life-refresh-v1/runtime/holdfast.png","Holdfast binding")
	check(View.SELECTED_PATHS["nodules-brittle-stars"]=="res://assets/environment/seabed-life-refresh-v1/runtime/brittle-stars.png","Star binding")
	check(View.SELECTED_PATHS["iron-hydroids"]=="res://assets/environment/seabed-life-refresh-v1/runtime/hydroids.png","Hydroid binding")
	check(game.occupied.size()==2,"Life artwork creates no room occupancy")
	game.hide();root.content_scale_size=Vector2i(1200,640);root.size=Vector2i(1200,640)
	var sheet:=Sheet.new();sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(sheet)
	var start=await sheet_capture(sheet,"native-comparison")
	sheet.clock=7.0
	var later=await sheet_capture(sheet,"native-fronds-later")
	check(start!=later,"New hydroids use existing native frond motion")
	Settings.reduced_motion=true;sheet.clock=2.0
	start=await sheet_capture(sheet,"reduced-start")
	sheet.clock=7.0;later=await sheet_capture(sheet,"reduced-later")
	check(start==later,"Reduced Motion freezes actual hydroid pixels")
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing source artwork")
	print("SEABED LIFE REVIEW: %d failures"%failures)
	quit(failures)
