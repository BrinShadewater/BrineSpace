extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Library=preload("res://scripts/room_asset_library.gd")
const FullWall=preload("res://rooms/full-wall-v1/full_wall_prop.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	Store.path="res://output/side-wall-regression-isolated.json"
	Store.defaults_path="user://no-side-wall-defaults.json"
	Store.loaded=true
	Store.data={}
	var ids=["research_lab","med_bay","pressure_control","listening_post","xeno_lab","isolation_vault","tidal_condenser","biodome","solar_array","radio_lab"]
	var count:=0
	for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/manifest.json")):
		if entry.room not in ids: continue
		for side in ["west","east"]:
			var id="side-"+entry.asset+"-"+side
			var registration=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/registrations/"+id+".json"))
			assert(FileAccess.get_sha256(registration.source)==registration.sha256)
			assert(not Library.template("library/"+id).is_empty())
		var view=load(entry.view).new()
		view.embedded=true
		root.add_child(view)
		view.hide()
		for q in ([0,2] if entry.room=="biodome" else [1,3]):
			view.configure_embedded(q,[],false,0.0)
			var found: Array=view.props.filter(func(p):return p.get("full_wall",false))
			assert(found.size()==1 and not found[0].side_view.is_empty())
			var id: String=found[0].id
			var authored: Rect2=found[0].rect
			Store.data[Store.key(entry.asset,q)]={id:[900,900],"size/"+id:[2.0,2.0]}
			view.configure_embedded(q,[],false,0.0)
			found=view.props.filter(func(p):return p.get("full_wall",false))
			assert(found[0].rect==authored,"Invalid old draft must fall back to authored side placement")
			assert(Store.data[Store.key(entry.asset,q)][id]==[900,900],"Do not overwrite the saved draft")
			Store.data[Store.key(entry.asset,q)]={id:[authored.position.x,authored.position.y]}
			view.configure_embedded(q,[],true,1.0)
			found=view.props.filter(func(p):return p.get("full_wall",false))
			assert(found[0].rect==authored,"Valid draft retained")
			count+=1
		view.free()
	# One authored side wall may serve both side walls, the opposite one mirrored
	# (docs/MIRRORED_SIDE_WALLS_PROPOSAL_2026-09-12.md). The polygons have to mirror
	# with the raster; if only the art flipped, placement and clearance would be
	# wrong for every asymmetric bank, which is the whole risk of the idea.
	var mirrors:=0
	var asymmetric:=0
	for entry in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/manifest.json")):
		if entry.room not in ids: continue
		var wall=FullWall.new(entry.asset)
		for side in ["west","east"]:
			var authored: Dictionary=wall.side_views[side].registration
			assert(not authored.get("mirrored",false),"Authored side art is never mirrored; the -side registration is opt-in per asset")
			assert(Library.source_uv(authored,Vector2(7,9))==Vector2(7,9),"An unmirrored registration passes its uv straight through")
			var mirror: Dictionary=Library.mirror_registration(authored)
			assert(mirror.get("mirrored",false))
			assert(mirror.width==authored.width and mirror.height==authored.height,"Mirroring must not change the footprint")
			assert(mirror.pivot==authored.pivot and mirror.outline==authored.outline,"Mirroring must not move the placement pivot")
			assert(mirror.get("wall_mount",false)==authored.get("wall_mount",false),"Mirroring must not change how the bank mounts")
			assert(mirror.pieces.size()==authored.pieces.size())
			var left:=INF
			var right:=-INF
			var mirrored_left:=INF
			var mirrored_right:=-INF
			# A mirror-symmetric bank reflects onto itself, so compare the two point
			# sets rather than their extents: only a moved point proves real work.
			var before: Array=[]
			var after: Array=[]
			for i in range(mirror.pieces.size()):
				assert(mirror.pieces[i].size()==authored.pieces[i].size(),"Mirroring must not drop points")
				for point in authored.pieces[i]:
					left=minf(left,point.x); right=maxf(right,point.x)
					before.append(point)
				for point in mirror.pieces[i]:
					mirrored_left=minf(mirrored_left,point.x); mirrored_right=maxf(mirrored_right,point.x)
					after.append(point)
					# Mirrored geometry samples the unmirrored source pixel, so the raster flips with it.
					var uv: Vector2=Library.source_uv(mirror,point)
					assert(is_equal_approx(uv.x,mirror.mirror_axis-point.x) and uv.y==point.y,"A mirrored uv must be the mirror of its own geometry")
					assert(uv.x>=authored.pivot.x-authored.width*0.5-0.01 and uv.x<=authored.pivot.x+authored.width*0.5+0.01,"A mirrored uv must stay inside the authored region")
			assert(is_equal_approx(mirrored_left,mirror.mirror_axis-right) and is_equal_approx(mirrored_right,mirror.mirror_axis-left),"Mirrored polygons must span the reflected extent")
			before.sort(); after.sort()
			if before!=after: asymmetric+=1
			# The mirror is its own inverse: the opposite wall of the opposite wall is the original.
			var back: Dictionary=Library.mirror_registration(mirror)
			for i in range(back.pieces.size()):
				for j in range(back.pieces[i].size()):
					assert(is_equal_approx(back.pieces[i][j].x,authored.pieces[i][j].x) and back.pieces[i][j].y==authored.pieces[i][j].y,"A double mirror must restore the authored polygon")
			mirrors+=1
		# Whenever an asset opts in, the wall it did not author is served by the mirror.
		var opt_in: String="res://rooms/full-wall-v1/registrations/side-"+entry.asset+"-side.json"
		if FileAccess.file_exists(opt_in):
			var declared: String=str(JSON.parse_string(FileAccess.get_file_as_string(opt_in)).get("direction",""))
			assert(declared in ["west","east"],"A mirrored side registration declares the wall it was authored for")
			var opposite: String="east" if declared=="west" else "west"
			if not FileAccess.file_exists("res://rooms/full-wall-v1/registrations/side-"+entry.asset+"-"+opposite+".json"):
				assert(wall.side_views[opposite].registration.get("mirrored",false),"The unauthored wall must be served by the mirror")
				assert(wall.side_views[opposite].art==wall.side_views[declared].art,"Both walls share the one authored raster")
	assert(asymmetric>0,"No side bank moved under the mirror, so this sweep would pass against a mirror that does nothing")
	print("SIDE WALL PASS: ",count," variants; source hashes, library entries, state, invalid-draft fallback and valid drafts; ",mirrors," side registrations mirrored, ",asymmetric," asymmetric")
	quit()
