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

	# --- Rename: the owner's name shows in the tray, is found by search, persists, and clears. ---
	var original: String=str(entry.label)
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
	if e.names.has(id) or e.label_of(id,entry)!=original: return fail("clearing the field did not restore the library label")
	e.library_search.text=""

	print("TILESET TOOLS PASS: star and Favourites filter, move to category and back, four crew in the picker, footprint in range and mirrored, rename shown, searched, saved and cleared")
	e.close_editor(); await process_frame; quit()
