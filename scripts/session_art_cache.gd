extends RefCounted
## Shared artwork stays resident while any gameplay or Studio owner is alive.
## Lookups may release only after the last owner has left the tree.
static var enabled := not OS.get_cmdline_user_args().has("--reference-session-art-cache")
static var release_room_materials := not OS.get_cmdline_user_args().has("--reference-room-material-lifetime")
static var release_transit_materials := not OS.get_cmdline_user_args().has("--reference-transit-material-lifetime")
static var owners:Dictionary={}

static func retain(owner:Node) -> void:
	var id:=owner.get_instance_id()
	if owners.has(id):return
	owners[id]=weakref(owner)
	owner.tree_exited.connect(release.bind(id),CONNECT_ONE_SHOT)

static func release(id:int) -> void:
	owners.erase(id)
	if not owners.is_empty() or not enabled:return
	load("res://scripts/hand_image_preparation.gd").clear()
	load("res://rooms/whole-room/room_lighting.gd").clear_room_shadow_packets()
	# Navigation snapshots keep collision/activity metadata between scenes, but
	# their prop dictionaries also copied the renderer's library image references.
	# No drawing owner remains; future room views load their own immutable images.
	var navigation=load("res://scripts/bill_npc.gd")
	for entry in navigation.room_cache.values():
		for prop in entry.data.get("props",[]):prop.erase("library_texture")
	# Decode tasks must finish even when their final owner exits. Discard unused
	# CPU results; creating GPU images here would only upload them to release them.
	var library=load("res://scripts/room_asset_library.gd")
	for path in library.image_jobs.keys():
		var job:Dictionary=library.image_jobs[path]
		WorkerThreadPool.wait_for_task_completion(job.task)
		library.image_jobs.erase(path)
	for view in library.portable_views.values():
		if is_instance_valid(view):view.queue_free()
	library.portable_views.clear()
	# template() embeds the image in its derived prop dictionary too. Clearing
	# only source_textures would leave that second strong owner resident.
	for entry in library.catalog.values():
		entry.erase("template")
		entry.erase("template_metadata")
	library.source_textures.clear()
	library.bunk_layer_cache.clear()
	load("res://rooms/whole-room/nursery_whole_view.gd").shared_source_textures.clear()
	var floor=load("res://rooms/whole-room/modular_floor.gd")
	# Both mesh generations reference floor images. Every drawing owner is gone.
	floor.cache.clear();floor.retired.clear();floor.textures.clear()
	# These factories are independently owned, even when they loaded the same
	# PNG as a tiled floor or hull pass. Preserve definitions and explicit settings.
	if release_room_materials:
		load("res://rooms/whole-room/painted_shell.gd").textures.clear()
		load("res://rooms/whole-room/ocean_windows.gd").textures.clear()
		load("res://rooms/whole-room/riser_catalog.gd").textures.clear()
		load("res://rooms/whole-room/department_wall_material.gd").textures.clear()
		load("res://rooms/whole-room/north_wall.gd").brine_texture=null
		var grain=load("res://rooms/whole-room/room_floor.gd")
		grain.grain=null;grain.department_grains.clear()
	if release_transit_materials:
		var corridor=load("res://rooms/underwater/corridor_wall_art.gd")
		corridor.textures.clear();corridor.detail_texture=null;corridor.tunnel_texture=null
		load("res://rooms/underwater/corridor_surfaces.gd").current_floor=null
		# Retain style objects/registration and progress; release only derived images.
		var doors=load("res://rooms/doors/painted_door.gd")
		for skin in doors.skins.values():skin.textures.clear()
		load("res://scripts/lighting_art.gd").textures.clear()
	load("res://scripts/environment_art.gd").cache.clear()
	var motion=load("res://scripts/drone_animation.gd")
	for path in motion.image_jobs.keys():
		var job:Dictionary=motion.image_jobs[path]
		WorkerThreadPool.wait_for_task_completion(job.task)
		motion.image_jobs.erase(path)
	motion.textures.clear();motion.texture_order.clear();motion.texture_bytes.clear()
	motion.last_used.clear();motion.cached_bytes=0;motion.active_canvas=null
	motion.weak_images.clear();motion.invisible_images.clear()
	if RenderingServer.frame_post_draw.is_connected(motion.trim_stale):RenderingServer.frame_post_draw.disconnect(motion.trim_stale)
