extends SceneTree
const Editor=preload("res://scripts/room_layout_editor.gd")
const Store=preload("res://scripts/room_layout_store.gd")
var failures:=0
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
 Store.path="res://output/studio-owner-2026-09-23/regression-layouts.json";Store.loaded=true;Store.data={}
 preload("res://scripts/title_settings.gd").save_path=Store.path+".cfg"
 var host=Control.new();root.add_child(host)
 var e=Editor.open(host);e.autosave_enabled=false;e.set_process(false);e.scale_actor.mode=0
 # Real effective props: stacking keeps placement and survives undo/save/reload.
 e.layer=0
 var a=e.room.props[0];var b=e.room.props[1]
 e.draft[a.id]=[0,0];e.draft[b.id]=[0,0];e.refresh()
 e.selected=a.id;e.selected_many.clear()
 var position=e.draft[a.id].duplicate()
 e.move_to_edge(true)
 var front_order=e.draft["order/"+a.id]
 var selected=e.selected_prop()
 for other in e.room.props:
  if other.id!=a.id:check(selected.sort_y>other.sort_y,"Selected prop is above every other prop")
 check(e.draft[a.id]==position,"Stacking does not move the prop")
 e.undo();check(not e.draft.has("order/"+a.id),"Stacking can be undone")
 e.redo();check(e.draft.get("order/"+a.id)==front_order,"Stacking can be redone")
 e.save_layout();e.rotation_drafts.clear();e.load_room()
 check(e.draft.get("order/"+a.id)==front_order,"Stacking survives disk save/reload")
 e.layer=0;e.selected=a.id;e.move_to_edge(false)
 selected=e.selected_prop()
 for other in e.room.props:
  if other.id!=a.id:check(selected.sort_y<other.sort_y,"Send to back is absolute")
 # A floor detail appearing after source defaults were enumerated must be draggable/removable.
 var profile=e.Floor.profile_for(e.room).duplicate(true)
 var host_prop=e.room.props[0]
 e.Floor.floor_profiles[e.room.get_script().resource_path]={"id":"late-detail-fixture","details":[{"asset":"detail-inspection_plug","hosts":[host_prop.id],"purpose":"test","scale":1.0}]}
 var detail_id="decor/detail-inspection_plug/"+str(host_prop.id)
 for key in e.draft.keys():
  if str(key).begins_with("decor/detail-inspection_plug/"):e.draft.erase(key)
 e.defaults.erase(detail_id);e.draft.erase(detail_id)
 e.refresh();e.layer=2
 var pieces=e.entities()
 check(pieces.size()>0,"Fixture resolves a newly introduced floor detail")
 if pieces.size()>0:
  var piece=pieces[0]
  check(e.draft.get(piece.id) is Array,"Late floor detail has editable position")
  var click=InputEventMouseButton.new()
  click.button_index=MOUSE_BUTTON_LEFT;click.pressed=true
  click.position=e.canvas.origin()+piece.rect.get_center()*e.canvas.factor()
  e.canvas_input(click)
  check(e.dragging and e.selected==piece.id,"Late detail can be grabbed without a missing-position error")
  click.pressed=false;e.canvas_input(click)
  e.selected=piece.id;e.remove_library_asset()
  check(e.draft.has(piece.id) and e.draft[piece.id]==null,"Removal records a durable floor-detail tombstone")
  check(e.entities().is_empty(),"Removed detail does not respawn")
  var fallback=e.room.props[1].id
  e.Floor.floor_profiles[e.room.get_script().resource_path].details[0].hosts.append(fallback)
  e.refresh()
  check(e.entities().is_empty(),"Deleted detail cannot respawn beside a fallback host")
  e.undo();check(not e.entities().is_empty(),"Floor-detail deletion supports undo")
 e.Floor.floor_profiles[e.room.get_script().resource_path]=profile
 # Construction preview must not rebuild its navigation graph for every drag event.
 for i in e.entries.size():
  if e.entries[i].room=="construction_drone_bay":e.index=i
 e.quarter=2;e.load_room();e.scale_actor.mode=2
 e.scale_actor.rebuild(e.room,"construction_drone_bay",2)
 e.dragging=true;e.refresh(true)
 for i in range(8):e._process(0.016)
 check(e.scale_actor.signature.is_empty(),"Dragging defers preview navigation rebuild")
 e.dragging=false;e._process(0.016)
 check(not e.scale_actor.signature.is_empty(),"Preview navigation refreshes immediately after drag")
 for i in e.entries.size():
  if e.entries[i].room=="airlock":e.index=i
 e.quarter=2;e.load_room();e.layer=0
 e.draft["suit_lockers"]=[35,30];e.refresh()
 for prop in e.room.props:
  if prop.id=="suit_lockers":
   check(e.room.locker_wall_art_rect(prop)==prop.rect,"Locker rendering follows saved position")
   var center=e.room.prop_visual_bounds(prop).get_center()
   check("suit_lockers" in e.hits_at(center),"180 degree locker is selectable where it is drawn")
 var bench=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/underwater/airlock-v1/composition.json")).furniture.filter(func(item):return item.id=="changing_bench")[0]
 var coil_visible:=false;var bag_visible:=false
 for polygon in bench.pieces:
  var points=PackedVector2Array()
  for point in polygon:points.append(Vector2(point[0],point[1]))
  coil_visible=coil_visible or Geometry2D.is_point_in_polygon(Vector2(1060,960),points)
  bag_visible=bag_visible or Geometry2D.is_point_in_polygon(Vector2(1060,1020),points)
 check(not coil_visible and bag_visible,"Bench registration omits the coil and retains the bag")
 print("STUDIO OWNER REGRESSIONS failures=",failures)
 quit(0 if failures==0 else 1)
