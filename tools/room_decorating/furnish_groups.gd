extends SceneTree
## Furnish rooms in WORKING GROUPS, the way the owner does (see
## skills/.../references/room-decorating.md): an anchor against the wall, its companions
## touching it, open floor between groups, the weight at the back, one side heavier.
## Drives the real Studio on a COPY of the layout store:
##   1. copy the owner's room_layouts.json to output/decorate/room_layouts.json
##   2. python tools/room_decorating/plan_groups.py
##   3. godot --path . --script tools/room_decorating/furnish_groups.gd -- all   (needs a display)
##   4. LOOK at output/decorate/<asset>.png, then merge only rooms the owner has not made.
## It never writes the owner's file.
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Geometry=preload("res://tools/modular_room_geometry.gd")
func _init() -> void: call_deferred("run")
func lanes(e) -> Array:
	var out: Array=[]
	for side in range(4):
		if Geometry.has_port(e.room.layout[0],side): out.append(Store.door_lane(side).grow(4))
	return out
func ok(rect: Rect2, taken: Array, doors: Array, margin: float) -> bool:
	if rect.position.x<-178 or rect.end.x>178 or rect.position.y<-182 or rect.end.y>174: return false
	for other in taken:
		if rect.grow(margin).intersects(other): return false
	for lane in doors:
		if rect.intersects(lane): return false
	return true
## Where a group's anchor may stand. Group 0 owns the back-left, group 1 the back-right,
## group 2 a side wall further forward: weight at the back, never mirrored.
func anchor_spots(size: Vector2, group: int) -> Array:
	var out: Array=[]
	var top:=-178.0      # flush to the back wall; companions share the anchor's baseline
	if group==0:
		for step in range(0,30): out.append(Rect2(Vector2(-174+step*8,top),size))
	elif group==1:
		for step in range(0,30): out.append(Rect2(Vector2(174-size.x-step*8,top),size))
	else:
		for y in range(-20,150-int(size.y),8):
			out.append(Rect2(Vector2(174-size.x,y),size)); out.append(Rect2(Vector2(-174,y),size))
	for y in range(-100,150-int(size.y),10):      # anywhere on a side wall, as a last resort
		out.append(Rect2(Vector2(-174,y),size)); out.append(Rect2(Vector2(174-size.x,y),size))
	return out
## A companion touches the group: beside it on the same baseline, else just in front.
func companion_spots(size: Vector2, members: Array) -> Array:
	var out: Array=[]
	var box: Rect2=members[0]
	for m in members: box=box.merge(m)
	var last: Rect2=members[members.size()-1]
	out.append(Rect2(Vector2(box.end.x+3,last.end.y-size.y),size))
	out.append(Rect2(Vector2(box.position.x-size.x-3,last.end.y-size.y),size))
	out.append(Rect2(Vector2(box.position.x+4,box.end.y+4),size))
	out.append(Rect2(Vector2(box.end.x-size.x-4,box.end.y+4),size))
	out.append(Rect2(Vector2(box.end.x+3,box.end.y+4),size))
	return out
func run() -> void:
	Store.path="res://output/decorate/room_layouts.json"; Store.loaded=false; Store.data={}
	var args:=OS.get_cmdline_user_args()
	var only: Array=Array(args[0].split(",")) if args.size()>0 and args[0]!="all" else []
	var plan: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://output/decorate/plan2.json"))
	var e=Editor.open(root)
	await process_frame
	for i in range(e.entries.size()):
		var asset:=str(e.entries[i].asset)
		if not plan.has(asset) or (not only.is_empty() and asset not in only): continue
		e.switch_room(i); await process_frame
		var remembered: Dictionary={}
		for q in range(4):
			if e.quarter!=q: e.switch_rotation(q); await process_frame
			for prop in e.base_props:
				if prop.has("flush_region") or prop.get("library_asset",false): continue
				var id:=str(prop.id)
				if e.defaults.has(id) and e.draft.get(id)!=null:
					var before: Dictionary=e.draft.duplicate(true)
					e.draft[id]=null; e.refresh()
					if not e.issues().is_empty(): e.draft=before; e.refresh()
			var taken: Array=[]
			for prop in e.room.props:
				if not prop.has("flush_region"): taken.append(prop.rect)
			var doors:=lanes(e)
			var placed:=0; var wanted:=0; var touching:=0
			for g in range(plan[asset].size()):
				var members: Array=[]
				for n in range(plan[asset][g].size()):
					var want: Dictionary=plan[asset][g][n]
					wanted+=1
					var id:=str(want.id)
					var size:=Vector2(float(want.w),float(want.h))*float(want.s)
					var tries: Array=[]
					if remembered.has(id): tries.append(remembered[id])
					if members.is_empty(): tries.append_array(anchor_spots(size,g))
					else: tries.append_array(companion_spots(size,members))
					for rect in tries:
						# a companion may sit 2 units from its own group but groups keep 26 apart
						var others: Array=taken.filter(func(r): return r not in members)
						if not ok(rect,others,doors,26.0 if members.is_empty() else 8.0): continue
						if not ok(rect,members,[],1.0): continue
						e.place_scale=float(want.s)
						if e.add_library_asset(id,rect.get_center()):
							if not remembered.has(id): remembered[id]=rect
							if not members.is_empty(): touching+=1
							members.append(rect); taken.append(rect); placed+=1; break
			e.save_layout(); await process_frame
			print("GROUPS %s/%d: placed %d of %d, %d beside their group, issues %d" % [asset,q,placed,wanted,touching,e.issues().size()])
			if q==0:
				await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png("res://output/decorate/"+asset+".png")
	print("GROUPS DONE"); quit()
