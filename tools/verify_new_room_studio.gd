extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
const Library=preload("res://scripts/room_asset_library.gd")
const OUT="res://assets/new-room-props-2026-09-26/review"
var failures:Array=[]
func check(ok:bool,message:String):if not ok:failures.append(message)
func _init():call_deferred("run")
func run():
 root.size=Vector2i(1600,900)
 Store.path=OUT+"/isolated-layouts.json";Store.defaults_path=OUT+"/no-defaults.json"
 Store.loaded=true;Store.data={}
 var editor=Editor.open(root);editor.autosave_enabled=false
 await process_frame
 var records:Array=JSON.parse_string(FileAccess.get_file_as_string("res://assets/new-room-props-2026-09-26/catalog.json"))
 var themes={"operations":4,"life_support":7,"recreation":8,"anomaly":9,"robotics":10}
 var shown=0;var placed=0
 editor.group_variants=false
 for category in themes:
  editor.library_filter.select(themes[category]);editor.library_search.text="";editor.tray_page=0
  editor.rebuild_library()
  var ids:Array=[]
  for i in range(editor.library_list.item_count):ids.append(str(editor.library_list.get_item_metadata(i)))
  for record in records:
   if record.category!=category:continue
   var id="library/"+record.id
   check(id in ids,id+": absent from department tray")
   check(not Library.template(id).is_empty(),id+": missing texture")
   shown+=1
  var match=records.filter(func(r):return r.category==category)[0]
  var baseline=editor.draft.duplicate(true)
  check(editor.add_library_asset("library/"+match.id,Vector2.ZERO),"Failed Studio placement "+match.id)
  check(Library.keeps_in_room("mycelium_nursery",editor.selected_prop()),"Filtered from live room")
  placed+=1
  editor.draft=baseline;editor.dirty=false;editor.refresh()
 editor.library_filter.select(10);editor.library_search.text="Battery";editor.rebuild_library()
 for frame in range(600):
  var ready=true
  for i in range(editor.library_list.item_count):
   if not Library.entries().get(str(editor.library_list.get_item_metadata(i)),{}).get("preview_ready",false):ready=false
  if ready:break
  await process_frame
 for i in range(editor.library_list.item_count):check(Library.entries().get(str(editor.library_list.get_item_metadata(i)),{}).get("preview_ready",false),"Thumbnail failed")
 check(editor.add_library_asset("library/sp-new-battery-service-bay-5",Vector2(0,-30)),"Console review placement")
 await process_frame
 await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png(OUT+"/studio-installed.png")
 var file=FileAccess.open(OUT+"/studio-validation.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"tray_props":shown,"department_placements":placed,"failures":failures},"  "));file.close()
 if not FileAccess.file_exists("res://tools/verify_new_room_studio.gd.uid"):
  file=FileAccess.open("res://tools/verify_new_room_studio.gd.uid",FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");file.close()
 print("NEW PROP STUDIO: ",shown," visible; ",placed," department placements; failures=",failures)
 quit(0 if failures.is_empty() else 1)

