extends SceneTree
const Scope=preload("res://scripts/session_art_cache.gd")
const Library=preload("res://scripts/room_asset_library.gd")
const View=preload("res://rooms/whole-room/nursery_whole_view.gd")
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
const EnvArt=preload("res://scripts/environment_art.gd")
const Motion=preload("res://scripts/drone_animation.gd")
const Navigation=preload("res://scripts/bill_npc.gd")
var checks:=0
var failures:=0
class Painter extends Node2D:
	var source:Texture2D
	var batches:Array=[]
	var prop:Dictionary={}
	var painter:CanvasItem=self
	func _draw():
		draw_texture_rect(source,Rect2(0,0,256,256),false)
		for batch in batches:draw_mesh(batch.mesh,batch.texture,Transform2D(0,Vector2(256,256)),Color.WHITE)
		if not prop.is_empty():Library.draw_base(self,prop)
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace("\\","/"):
		push_error("Session art test requires isolated user directory");quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	var capture:=SubViewport.new();capture.size=Vector2i(512,512)
	capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture)
	var first:=Node2D.new();capture.add_child(first);Scope.retain(first);Scope.retain(first)
	var second:=Node2D.new();capture.add_child(second);Scope.retain(second)
	check(Scope.owners.size()==2,"Duplicate retain has one lease per owner")
	var painter:=Painter.new();second.add_child(painter)
	Motion.begin(painter)
	check(RenderingServer.frame_post_draw.is_connected(Motion.trim_stale),"Drawing owner connects stale drone cleanup")
	painter.source=View.load_source_texture(View.SOURCE)
	painter.batches=Floor.meshes({},false)
	for index in range(110):Floor.meshes({},false,0,0.1+index/1000.0)
	check(not Floor.retired.is_empty(),"Fixture exercises retired floor generations")
	var source_ref:WeakRef=weakref(painter.source)
	var floor_ref:WeakRef=weakref(painter.batches[0].texture)
	EnvArt.texture("silt-plain")
	var prop:=Library.template("library/sp-crew_hab-3")
	check(not prop.is_empty(),"Selected prop template")
	var prop_pixels:PackedByteArray=prop.library_texture.get_image().get_data()
	var prop_metadata:Dictionary=prop.duplicate(true);prop_metadata.erase("library_texture")
	painter.prop=prop.duplicate(true)
	var nav_prop:Dictionary=prop.duplicate(true)
	Navigation.room_cache["image-lifetime-fixture"]={"data":{"props":[nav_prop],"blockers":[Rect2(1,2,3,4)]},"points":[Vector2i(8,16)],"links":[[Vector2i(8,16),Vector2i(24,16)]]}
	var nav_metadata:Dictionary=nav_prop.duplicate(true);nav_metadata.erase("library_texture")
	var prop_ref:WeakRef=weakref(prop.library_texture);prop.clear()
	await frame();var reference:PackedByteArray=capture.get_texture().get_image().get_data()
	first.queue_free();await frame()
	check(Scope.owners.size()==1,"Overlapping owner remains")
	check(RenderingServer.frame_post_draw.is_connected(Motion.trim_stale),"Overlapping owner preserves drone cleanup")
	check(nav_prop.has("library_texture"),"Navigation image survives while a drawing owner remains")
	check(source_ref.get_ref()!=null and floor_ref.get_ref()!=null and prop_ref.get_ref()!=null,"Another owner protects images and cached templates")
	check(not Library.source_textures.is_empty() and not Floor.cache.is_empty(),"Closing one owner preserves lookups")
	check(reference==capture.get_texture().get_image().get_data(),"Surviving owner's retained pixels unchanged")
	# Pending decodes are joined and discarded safely after the final owner leaves.
	var pending_source:String=Library.entries()["library/sp-crew_hab-3"].data.source
	Library.source_textures.erase(pending_source);Library.request_texture(pending_source)
	Motion.request_texture("res://assets/mining-rover-v1-2026-09-26/completion/atlases/empty-120.png")
	second.queue_free();painter=null;await frame()
	check(Scope.owners.is_empty(),"Last owner released")
	check(Motion.weak_images.is_empty() and not RenderingServer.frame_post_draw.is_connected(Motion.trim_stale),"Final owner clears weak images and disconnects drone cleanup")
	check(not nav_prop.has("library_texture") and nav_prop==nav_metadata,"Navigation drops only its drawing image reference")
	check(Navigation.room_cache["image-lifetime-fixture"].points==[Vector2i(8,16)] and Navigation.room_cache["image-lifetime-fixture"].links==[[Vector2i(8,16),Vector2i(24,16)]] and Navigation.room_cache["image-lifetime-fixture"].data.blockers==[Rect2(1,2,3,4)],"Navigation topology and collision cache survive scene exit")
	check(Library.source_textures.is_empty() and Library.bunk_layer_cache.is_empty() and Library.portable_views.is_empty(),"Library storage released")
	check(Library.image_jobs.is_empty() and Motion.image_jobs.is_empty(),"Both worker queues safely drained")
	check(Floor.cache.is_empty() and Floor.retired.is_empty() and Floor.textures.is_empty(),"Both floor generations released")
	check(View.shared_source_textures.is_empty() and EnvArt.cache.is_empty(),"Room source and environment lookups released")
	check(source_ref.get_ref()==null and floor_ref.get_ref()==null and prop_ref.get_ref()==null,"No cache retains abandoned images")
	var templates:=0
	for entry in Library.catalog.values():
		if entry.has("template"):templates+=1
	check(templates==0,"All derived prop templates released")
	var third:=Node2D.new();capture.add_child(third);Scope.retain(third)
	painter=Painter.new();third.add_child(painter)
	Motion.begin(painter)
	check(RenderingServer.frame_post_draw.is_connected(Motion.trim_stale),"Next drawing session reconnects drone cleanup")
	painter.source=View.load_source_texture(View.SOURCE);painter.batches=Floor.meshes({},false)
	painter.prop=Library.template("library/sp-crew_hab-3").duplicate(true)
	check(painter.prop.library_texture.get_image().get_data()==prop_pixels,"Reloaded selected prop has exact pixels")
	var reloaded_metadata:Dictionary=painter.prop.duplicate(true);reloaded_metadata.erase("library_texture")
	check(reloaded_metadata==prop_metadata,"Reloaded prop preserves registration and metadata")
	check(not nav_prop.has("library_texture"),"Reloaded drawing images do not refill old navigation snapshots")
	await frame()
	check(reference==capture.get_texture().get_image().get_data(),"Next session reload has exact source/floor pixels")
	# Diagnostic reference mode retains earlier caches, but still drops owner leases.
	Scope.enabled=false;third.queue_free();painter=null;await frame()
	check(Scope.owners.is_empty() and not Floor.textures.is_empty(),"Reference switch preserves old cache behavior")
	Scope.enabled=true
	var last:=Node.new();root.add_child(last);Scope.retain(last);last.queue_free();await frame()
	capture.queue_free();await frame()
	Navigation.room_cache.erase("image-lifetime-fixture")
	print("SESSION ART CACHE: %d checks; %d failures"%[checks,failures]);quit(1 if failures else 0)
