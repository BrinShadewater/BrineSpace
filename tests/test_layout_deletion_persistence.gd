extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
func _init() -> void: call_deferred("run")
func prop_ids(room) -> Array:
 var ids: Array=[]
 for prop in room.props: ids.append(str(prop.id))
 ids.sort()
 return ids
func run() -> void:
 root.size=Vector2i(1600,900)
 Store.path="res://output/layout-deletion-regression.json"
 Store.loaded=true
 Store.data={}
 var editor=Editor.open(root)
 editor.autosave_enabled=false
 var checked:=0
 # Every Studio room must supply the same source props regardless of saved deletions.
 for room_index in editor.entries.size():
  var entry=editor.entries[room_index]
  var view=load(entry.view).new()
  if "room_id" in view: view.room_id=entry.room
  view.embedded=true
  view.set_meta("layout_editor_preview",true)
  view.set_meta("layout_draft",{})
  root.add_child(view)
  view.hide()
  for q in range(4):
   view.configure_embedded(q,[],false,0.0)
   var before:=prop_ids(view)
   var deleted: Dictionary={}
   for id in before: deleted[id]=null
   Store.data[Store.key(entry.asset,q)]=deleted
   Store.prime()
   view.configure_embedded((q+1)%4,[],false,0.0)
   view.configure_embedded(q,[],false,0.0)
   assert(prop_ids(view)==before,"Saved deletion changed Studio source props: %s/%s" % [entry.asset,q])
   checked+=1
  view.queue_free()
  await process_frame
  print("CHECKED ",entry.asset)
 # Exercise real editor deletion and both save paths against authored defaults.
 Store.data={}
 Store.prime()
 for i in editor.entries.size():
  if editor.entries[i].asset=="pressure-manifold-wall": editor.index=i
 editor.quarter=1
 editor.load_room()
 var ids:=prop_ids(editor.room)
 for id in ids: editor.draft.erase("locked/"+id)
 editor.selected=ids[0]
 editor.selected_many=ids.duplicate()
 editor.remove_library_asset()
 assert(editor.room.props.is_empty())
 editor.draft["retired_fixture_prop"]=null
 editor.save_layout()
 for iteration in range(2):
  editor.rotation_drafts.clear()
  Store.loaded=false
  editor.load_room()
  assert(editor.room.props.is_empty(),"Reload resurrected Pressure Control props")
  assert(Store.positions("pressure-manifold-wall",1).has("retired_fixture_prop"),"Missing-source deletion lost")
  editor.switch_rotation(2)
  editor.switch_rotation(1)
  editor.save_all_rotations()
  await process_frame
 print("LAYOUT DELETION PASS: ",checked," room rotations; Pressure Control delete, disk reload, rotation roundtrip, repeated save all")
 editor.queue_free()
 quit()
