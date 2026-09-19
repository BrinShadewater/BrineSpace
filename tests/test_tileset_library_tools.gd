extends SceneTree
## Tileset library tools in the Studio: star, move to category, crew picker,
## and the floor footprint that the equipment shadow shades. Every mark file is
## redirected under output/ so the owner's favourites, categories and retired
## lists are never touched.
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const OUT:="res://output/layout-editor/"

func _init() -> void: call_deferred("run")

func fail(message: String) -> void:
	push_error("TILESET TOOLS FAIL: "+message); quit(1)

func run() -> void:
	Store.path=OUT+"tileset-tools-isolated.json"; Store.loaded=true; Store.data={}
	for name in ["favourites","categories","retired","names"]:
		var path: String=OUT+"tileset-tools-"+name+".json"
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	Editor.NAMES_PATH=OUT+"tileset-tools-names.json"
	# Split writes the prop registry; give it a copy so the real one is never touched.
	var real_props:=FileAccess.get_file_as_string("res://rooms/tileset-library/props.json")
	Editor.PROPS_PATH=OUT+"tileset-tools-props.json"
	var props_copy:=FileAccess.open(Editor.PROPS_PATH,FileAccess.WRITE); props_copy.store_string(real_props); props_copy.close()
	Editor.FAVOURITES_PATH=OUT+"tileset-tools-favourites.json"
	Editor.CATEGORIES_PATH=OUT+"tileset-tools-categories.json"
	Editor.RETIRED_PATH=OUT+"tileset-tools-retired.json"
	var e=Editor.open(root)
	await process_frame
	var Library=e.Library

	# A tileset prop to work with: the first one under the first kind filter.
	var kind:=-1
	for i in range(e.library_filter.item_count):
		if e.theme_filters.has(i): kind=i; break
	if kind<0: return fail("no tileset kind filters in the dropdown")
	var theme: String=e.theme_filters[kind]
	e.library_filter.select(kind); e.rebuild_library()
	if e.library_list.item_count<2: return fail("kind filter '%s' lists nothing" % theme)
	var id: String=str(e.library_list.get_item_metadata(0))
	if not id.begins_with("library/tileset-"): return fail("first listed id is not a tileset prop: "+id)
	var entry: Dictionary=Library.entries()[id]

	# --- Star: mark, appears under Favourites with a star, unmark, gone. ---
	e.toggle_favourite(id)
	if not e.favourites.has(id): return fail("star did not mark "+id)
	e.library_filter.select(e.favourites_filter); e.rebuild_library()
	if e.library_list.item_count!=1 or str(e.library_list.get_item_metadata(0))!=id: return fail("Favourites filter does not list the starred prop")
	if not e.library_list.get_item_text(0).begins_with("★"): return fail("starred caption lacks the star: "+e.library_list.get_item_text(0))
	var saved: Variant=JSON.parse_string(FileAccess.get_file_as_string(Editor.FAVOURITES_PATH))
	if not (saved is Array and saved.has(id)): return fail("favourites.json did not persist the star")
	e.toggle_favourite(id)
	if e.favourites.has(id): return fail("second star press did not unmark")
	e.rebuild_library()
	if e.library_list.item_count!=0: return fail("Favourites still lists an unstarred prop")

	# --- Move: refile to another kind, listed there and not in its old kind; move back clears the override. ---
	var target:=""
	for candidate in e.tileset_categories:
		if str(candidate)!=theme: target=str(candidate); break
	e.recategorise(id,target)
	if e.category_of(id,entry)!=target: return fail("category_of did not follow the move")
	var target_filter:=-1
	for i in e.theme_filters:
		if e.theme_filters[i]==target: target_filter=i
	e.library_filter.select(target_filter); e.rebuild_library()
	var listed:=false
	for i in range(e.library_list.item_count):
		if str(e.library_list.get_item_metadata(i))==id: listed=true
	if not listed: return fail("moved prop is not listed under "+target)
	e.library_filter.select(kind); e.rebuild_library()
	for i in range(e.library_list.item_count):
		if str(e.library_list.get_item_metadata(i))==id: return fail("moved prop still listed under "+theme)
	var moved: Variant=JSON.parse_string(FileAccess.get_file_as_string(Editor.CATEGORIES_PATH))
	if not (moved is Dictionary and moved.get(id,"")==target): return fail("categories.json did not persist the move")
	e.recategorise(id,theme)
	if e.recategorised.has(id): return fail("moving back to the original kind left an override")

	# --- Crew picker: each cast member loads their own art. ---
	e.set_character_mode(1)
	var seen: Array=[]
	for i in range(e.scale_actor.CAST.size()):
		e.cast_pick.select(i); e.cast_pick.item_selected.emit(i)
		if e.scale_actor.cast_index!=i: return fail("cast picker did not switch to "+str(e.scale_actor.CAST[i].name))
		if e.scale_actor.player.frames.is_empty(): return fail("no art loaded for "+str(e.scale_actor.CAST[i].name))
		seen.append(e.scale_actor.player.frames.size())
	if seen.size()!=4: return fail("expected four crew members, got "+str(seen.size()))

	# --- Footprint: fractions inside the rect; mirrored art mirrors it. ---
	var prop: Dictionary=Library.template(id)
	if not prop.has("footprint"): return fail("template carries no footprint")
	var f: Array=prop.footprint
	for v in f:
		if float(v)<0.0 or float(v)>1.0: return fail("footprint fraction out of range: "+str(f))
	if float(f[0])+float(f[2])>1.0001 or float(f[1])+float(f[3])>1.0001: return fail("footprint leaves the rect: "+str(f))
	var mirror_id:="library/tileset-test-mirror"
	var data: Dictionary=entry.data.duplicate(true); data.mirror_horizontal=true; data.id="test-mirror"
	Library.catalog[mirror_id]={"data":data,"label":"mirror probe","width":entry.width,"group":"tileset","category":entry.category,"tileset":entry.tileset}
	var mirrored: Dictionary=Library.template(mirror_id)
	Library.catalog.erase(mirror_id)
	if not mirrored.registration.get("mirrored",false): return fail("mirror probe did not mirror")
	var mf: Array=mirrored.footprint
	if absf(float(mf[0])-(1.0-float(f[0])-float(f[2])))>0.0001 or mf[2]!=f[2]: return fail("mirrored footprint is not the mirror image: "+str(f)+" -> "+str(mf))

	# --- Floors: every owner-picked finish is offered and its texture loads as a 4x4 atlas. ---
	var Floor=load("res://rooms/whole-room/modular_floor.gd")
	var picked: Variant=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/tileset-library/floors.json"))
	if not (picked is Dictionary) or picked.is_empty(): return fail("floors.json is missing or empty")
	for caption in picked:
		var path: String=str(picked[caption])
		if not path in Floor.finishes().values(): return fail("finish not offered in the Studio: "+str(caption))
		var floor_texture: Texture2D=Floor.texture(path)
		if floor_texture==null or floor_texture.get_width()!=floor_texture.get_height() or floor_texture.get_width()%4!=0:
			return fail("finish texture is not a square 4x4 atlas: "+path)

	# --- Multi-select: two selected props are marked and restored together. ---
	e.library_filter.select(kind); e.library_search.text=""; e.rebuild_library()
	e.library_list.deselect_all(); e.library_list.select(0,true); e.library_list.select(1,false)
	var pair: Array=e.selected_library_ids()
	if pair.size()!=2: return fail("multi-select did not yield two ids: "+str(pair))
	e.update_retire_button()
	if not e.retire_button.text.begins_with("Mark 2"): return fail("retire button does not name the batch: "+e.retire_button.text)
	e.mark_selected(e.retired,e.save_retired)
	if not (e.retired.has(pair[0]) and e.retired.has(pair[1])): return fail("batch mark did not retire both")
	e.library_filter.select(e.library_filter.item_count-1); e.rebuild_library()
	if e.library_list.item_count!=2: return fail("Marked for removal does not list the pair: "+str(e.library_list.item_count))
	e.library_list.select(0,true); e.library_list.select(1,false); e.mark_selected(e.retired,e.save_retired)
	if e.retired.has(pair[0]) or e.retired.has(pair[1]): return fail("batch restore did not clear both")
	e.library_filter.select(kind); e.rebuild_library(); e.library_list.deselect_all(); e.library_list.select(0)

	# --- Split: the owner's case, two stacked chairs boxed as one, comes apart at the seam. ---
	var top_id:="library/tileset-h22-202"; var bottom_id:="library/tileset-h22-202b"
	if not (Library.entries().has(top_id) and Library.entries().has(bottom_id)): return fail("split fixture props are missing")
	var top: Dictionary=Library.entries()[top_id].data; var bottom: Dictionary=Library.entries()[bottom_id].data
	var ux:=minf(top.region[0],bottom.region[0]); var uy:=minf(top.region[1],bottom.region[1])
	var ur:=maxf(top.region[0]+top.region[2],bottom.region[0]+bottom.region[2]); var ub:=maxf(top.region[1]+top.region[3],bottom.region[1]+bottom.region[3])
	var glued: Dictionary=top.duplicate(true); glued.id="test-split"; glued.region=[ux,uy,ur-ux,ub-uy]
	var parts: Array=Editor.split_regions(glued)
	if parts.size()!=2: return fail("stacked chairs were not split")
	for check in [[parts[0],top.region],[parts[1],bottom.region]]:
		var got: Rect2i=check[0]; var want: Array=check[1]
		if absi(got.position.x-int(want[0]))>2 or absi(got.position.y-int(want[1]))>2 or absi(got.size.x-int(want[2]))>2 or absi(got.size.y-int(want[3]))>2:
			return fail("split part does not match the chair: "+str(got)+" vs "+str(want))
	Library.catalog["library/tileset-test-split"]={"data":glued,"label":"Splitfix 001","width":float(glued.region[2]),"group":"tileset","category":theme,"tileset":"Fixture"}
	e.library_filter.select(3); e.library_search.text="splitfix"; e.rebuild_library()
	if e.library_list.item_count!=1: return fail("split fixture is not listed: "+str(e.library_list.item_count))
	e.library_list.deselect_all(); e.library_list.select(0); e.update_retire_button()
	if e.split_button.disabled: return fail("Split button is disabled for a single tileset prop")
	e.split_selected()
	if not Library.entries().has("library/tileset-test-splitb"): return fail("split did not add the second part to the library")
	if str(Library.entries()["library/tileset-test-splitb"].label)!="Splitfix 002": return fail("second part is not numbered after the first: "+str(Library.entries()["library/tileset-test-splitb"].label))
	var second_part: Dictionary=Library.template("library/tileset-test-splitb")
	if second_part.is_empty() or not second_part.has("footprint"): return fail("second part has no drawable template or footprint")
	var written: Variant=JSON.parse_string(FileAccess.get_file_as_string(Editor.PROPS_PATH))
	var found:=0
	for row in written:
		if str(row.get("id","")) in ["test-split","test-splitb"]: found+=1
	if found!=2: return fail("split did not persist both parts: "+str(found))
	if FileAccess.get_file_as_string("res://rooms/tileset-library/props.json")!=real_props: return fail("split wrote to the real props.json")
	Library.catalog.erase("library/tileset-test-split"); Library.catalog.erase("library/tileset-test-splitb")
	e.library_search.text=""

	# --- Placement size: the owner's calibrated size applies to new placements. ---
	e.library_filter.select(kind); e.library_search.text=""; e.rebuild_library()
	e.free_placement.button_pressed=true
	e.place_scale=0.8
	var drop_id: String=str(e.library_list.get_item_metadata(0))
	if not e.add_library_asset(drop_id,Vector2(-120,60)): return fail("could not place a library prop")
	if e.draft.get("size/"+drop_id)!=[0.8,0.8]: return fail("new placement ignored the calibrated size: "+str(e.draft.get("size/"+drop_id)))

	# --- In this room: lists what is placed here and nothing else. ---
	e.library_filter.select(e.in_room_filter); e.rebuild_library()
	var saw_drop:=false
	for i in range(e.library_list.item_count):
		var listed_id: String=str(e.library_list.get_item_metadata(i))
		if listed_id==drop_id: saw_drop=true
		var is_placed:=false
		for key in e.draft:
			if e.draft[key] is Array and Library.base_id(str(key))==listed_id: is_placed=true
		if not is_placed: return fail("In this room lists a prop that is not placed here: "+listed_id)
	if not saw_drop: return fail("In this room does not list the prop just placed")
	if e.library_list.item_count>=20: return fail("In this room is not narrowing the tray: "+str(e.library_list.item_count))

	# --- Paging: a kind larger than one page is reachable, and a new filter starts at page one. ---
	var big:=-1
	for i in e.theme_filters:
		e.library_filter.select(i); e.rebuild_library()
		if e.tray_total>Editor.TRAY_LIMIT: big=i; break
	if big<0: return fail("no kind is larger than one tray page; the pager is untested")
	var first_on_page_one: String=str(e.library_list.get_item_metadata(0))
	if not e.pager_next.visible or e.pager_next.disabled or not e.pager_prev.disabled: return fail("pager buttons wrong on page one")
	e.turn_page(1)
	if e.tray_page!=1 or str(e.library_list.get_item_metadata(0))==first_on_page_one: return fail("next page did not advance the tray")
	if not e.pager_label.text.contains(" of "+str(e.tray_total)): return fail("pager label does not state the range: "+e.pager_label.text)
	e.library_filter.select(kind); e.rebuild_library()
	if e.tray_page!=0: return fail("changing the filter did not return to page one")

	# --- Copy to other rotations: the placed prop reaches all three, saved. ---
	var asset: String=str(e.entries[e.index].asset)
	var home: int=e.quarter
	e.copy_to_other_rotations()
	if e.quarter!=home: return fail("copy to other rotations did not return to the starting rotation")
	for q in range(4):
		var saved_q: Dictionary=Store.data.get(Store.key(asset,q),{})
		if not (saved_q.get(drop_id) is Array): return fail("rotation %d did not receive the placed prop: %s" % [q*90,e.status.text])

	# --- Finish strength: set per room, kept when trying another finish. ---
	e.layer=1; e.refresh()
	e.floor_tools.apply_finish(1)
	e.floor_tools.preview_strength(80.0)
	if absf(float(e.draft.get("floor/strength",0.0))-0.8)>0.001: return fail("finish strength did not reach the layout")
	e.floor_tools.apply_finish(2)
	if absf(float(e.draft.get("floor/strength",0.0))-0.8)>0.001: return fail("choosing another finish reset the strength")
	e.floor_tools.preview_strength(42.0)
	if e.draft.has("floor/strength"): return fail("the default strength should not be stored")
	e.layer=0; e.refresh()
	e.library_filter.select(kind); e.library_search.text=""; e.rebuild_library()

	# --- Rename: the owner's name shows in the tray, is found by search, persists, and clears. ---
	var original: String=str(entry.label)
	var shown_before: String=e.label_of(id,entry)       # a title, where the prop has one
	e.rename(id,"  Cryo pod  ")
	if e.label_of(id,entry)!="Cryo pod": return fail("rename did not take (and should trim spaces)")
	e.library_filter.select(kind); e.library_search.text="cryo pod"; e.rebuild_library()
	if e.library_list.item_count!=1 or str(e.library_list.get_item_metadata(0))!=id: return fail("search by the new name did not find the renamed prop")
	if e.library_list.get_item_text(0)!="Cryo pod": return fail("tray caption is not the new name: "+e.library_list.get_item_text(0))
	e.library_search.text=original.to_lower(); e.rebuild_library()
	var still_found:=false
	for i in range(e.library_list.item_count):
		if str(e.library_list.get_item_metadata(i))==id: still_found=true
	if not still_found: return fail("search by the library label no longer finds the renamed prop")
	var named: Variant=JSON.parse_string(FileAccess.get_file_as_string(Editor.NAMES_PATH))
	if not (named is Dictionary and named.get(id,"")=="Cryo pod"): return fail("names.json did not persist the rename")
	if e.display_name(id,"?")!="Cryo pod": return fail("sidebar name does not follow the rename")
	e.rename(id,"")
	if e.names.has(id) or e.label_of(id,entry)!=shown_before: return fail("clearing the field did not restore the library name")
	# --- Titles: a titled prop shows its title, the owner's rename still wins, search finds both. ---
	var titled_id:=""
	for candidate in Library.entries():
		if not str(Library.entries()[candidate].get("title","")).is_empty(): titled_id=candidate; break
	if not titled_id.is_empty():
		var titled: Dictionary=Library.entries()[titled_id]
		if e.label_of(titled_id,titled)!=str(titled.title): return fail("a titled prop does not show its title")
		e.library_filter.select(3); e.library_search.text=str(titled.label).to_lower(); e.rebuild_library()
		var by_label:=false
		for i in range(e.library_list.item_count):
			if str(e.library_list.get_item_metadata(i))==titled_id: by_label=true
		if not by_label: return fail("a titled prop is no longer found by its library label")
		e.names[titled_id]="Owner's name"
		if e.label_of(titled_id,titled)!="Owner's name": return fail("the owner's rename does not win over a title")
		e.names.erase(titled_id)
	e.library_search.text=""

	print("TILESET TOOLS PASS: star and Favourites filter, move to category and back, four crew in the picker, footprint in range and mirrored, floors offered, batch mark, stacked chairs split, calibrated size, in-room filter, paging, rotations copied, finish strength, rename shown, searched, saved and cleared")
	e.close_editor(); await process_frame; quit()
