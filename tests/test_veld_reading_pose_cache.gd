extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const Pool=preload("res://scripts/crew_texture_pool.gd")
const Actor=preload("res://scripts/veld_npc.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
class Context extends RefCounted:
	var grid_view
	func _init(grid):grid_view=grid
class Grid extends RefCounted:
	var veld_player
	var source:Texture2D
	func _init(player):veld_player=player
	func _get_veld_live_frame_source(_main):return source
func same_sources(a:Array,b:Array)->bool:
	if a.size()!=b.size():return false
	for i in a.size():
		if a[i]!=b[i]:return false
	return true
func compare(actor,player,label:String):
	actor.cache_reading_poses=false
	var reference:Array=actor.reading_return_sources(player)
	actor.cache_reading_poses=true
	check(same_sources(reference,actor.reading_return_sources(player)),"Exact pose identities: "+label)
func run():
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/")!=expected:
		push_error("Reading cache requires isolated BRINESPACE_TEST_USER_DIR");quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	var player=Player.new();var pool=Pool.new();player.begin_texture_batch(pool)
	player.load_manifest("res://character/veld-seated-south-selected-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/veld-seated-south-selected-v1/helmet-manifest.json"),"Selected helmet manifest")
	player.finish_texture_batch();pool.clear_lookup()
	var actor=Actor.new();actor.direction="south"
	var grid=Grid.new(player);var context=Context.new(grid)
	var measurements:=[]
	for helmet in [false,true]:
		actor.helmet_equipped=helmet
		var bank:Dictionary=player.equipment_frames["diving-helmet"] if helmet else player.frames
		var poses:Array=actor.reading_return_sources(player)
		check(poses.size()==6,"Selected six unique poses")
		for pose in range(6):
			grid.source=poses[pose]
			actor.cache_reading_poses=false
			check(actor.begin_interrupted_reading(context),"Reference interruption")
			var reference:=[actor.stage,actor.state,actor.timer,actor.tablet_exit_pose]
			actor.cache_reading_poses=true
			check(actor.begin_interrupted_reading(context),"Cached interruption")
			check(reference==[actor.stage,actor.state,actor.timer,actor.tablet_exit_pose],"Exact interruption state/timing")
			for elapsed in [0.0,0.01,0.03,0.059,0.06]:
				actor.timer=.48-elapsed
				actor.cache_reading_poses=false;var ref:Texture2D=actor.reading_return_frame(context)
				actor.cache_reading_poses=true
				check(actor.reading_return_frame(context)==ref,"Exact retained frame through exit hold")
		compare(actor,player,"warm bank")
		# Warm cache invalidates on changed wrapper, storage, metadata and timing.
		var original:Texture2D=bank["read-seated-south"][0]
		var copy:=CanvasTexture.new();copy.diffuse_texture=original.diffuse_texture
		copy.set_meta("crew_seat_contact_depth",true)
		bank["read-seated-south"][0]=copy;compare(actor,player,"wrapper replacement")
		copy.diffuse_texture=ImageTexture.create_from_image(original.get_image());compare(actor,player,"equal pixels distinct storage")
		var changed:Image=original.get_image();changed.fill(Color.CORAL)
		copy.diffuse_texture=ImageTexture.create_from_image(changed);compare(actor,player,"different storage pixels")
		copy.set_meta("crew_seat_contact_depth",false);compare(actor,player,"contact metadata removed")
		bank["read-seated-south"][0]=original
		compare(actor,player,"restored bank")
		var timing:Dictionary=player.equipment_timing["diving-helmet"] if helmet else player.timing
		timing["read-seated-south"].loop=true;compare(actor,player,"legacy loop")
		timing["read-seated-south"].loop=false
		for pair in range(3):
			for cached in ([false,true] if pair%2==0 else [true,false]):
				actor.cache_reading_poses=cached
				actor.reading_return_sources(player)
				var samples:=[]
				for tick in range(60):
					var start:=Time.get_ticks_usec();var row:Array=actor.reading_return_sources(player)
					samples.append(Time.get_ticks_usec()-start)
					check(row.size()==6,"Measured complete pose set")
				measurements.append({"helmet":helmet,"cached":cached,"pair":pair,"samples":samples})
		poses.clear()
	actor.cache_reading_poses=true;actor.helmet_equipped=false
	compare(actor,player,"bare after equipment switch")
	actor.direction="north";compare(actor,player,"other facing");actor.direction="south"
	# Direct textures remain mutable and must bypass the immutable-bank cache.
	var row:Array=player.frames["read-seated-south"]
	var original:Texture2D=row[0];var direct:=ImageTexture.create_from_image(original.get_image())
	direct.set_meta("crew_seat_contact_depth",true);row[0]=direct;compare(actor,player,"direct texture")
	var changed:Image=direct.get_image();changed.fill(Color.CORAL);direct.set_image(changed)
	compare(actor,player,"direct in-place mutation");row[0]=original
	actor.reading_return_sources(player)
	var weak:WeakRef=weakref(player.frames["read-seated-south"][0])
	grid.source=null;row.clear();original=null;direct=null
	player.frames.clear();player.equipment_frames.clear()
	check(weak.get_ref()==null,"Cache cannot retain an abandoned frame bank")
	FileAccess.open("user://reading-cache.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"measurements":measurements}))
	print("VELD READING CACHE: %d checks; %d failures"%[checks,failures])
	quit(1 if failures else 0)
