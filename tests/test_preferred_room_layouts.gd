extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Walker=preload("res://scripts/bill_npc.gd")
const Geometry=preload("res://tools/modular_room_geometry.gd")
const OUT="user://"
func _init():call_deferred("run")
func run():
 Store.loaded=true;Store.data={};Store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
 var walker=Walker.new();var report=[]
 for e in JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json")):
  if e.room in ["corridor","corner","tee_corridor"]:continue
  var view=load(e.view).new()
  if "room_id" in view:view.room_id=e.room
  view.embedded=true;root.add_child(view);view.hide()
  for q in range(4):
   view.configure_embedded(q,[],false,0)
   var sides=[]
   for side in range(4):
    if Geometry.has_port(view.layout[0],side):sides.append(side)
   view.configure_embedded(q,sides,false,0);Store.apply(view,e.asset)
   var blockers=[]
   for p in view.props:
    if not p.get("layout_hidden",false):
     for rect in Geometry.prop_collision_rects(p):blockers.append(rect.grow(10))
   for edge in view.edges:
    for r in Geometry.wall_rects(edge):blockers.append(r.grow(10))
   walker.geometry={Vector2i.ZERO:{"open":sides,"blockers":blockers}}
   var points={};var graph=AStar2D.new()
   for y in range(-176,177,16):
    for x in range(-176,177,16):
     var p=Vector2(x,y)+Vector2(192,192)
     if walker.can_stand(p):
      var n=graph.get_available_point_id();graph.add_point(n,p);points[Vector2i(x,y)]=n
   for p in points:
    for shift in [Vector2i(16,0),Vector2i(0,16),Vector2i(16,16),Vector2i(-16,16)]:
     var other=p+shift
     if points.has(other) and walker.segment_clear(graph.get_point_position(points[p]),graph.get_point_position(points[other])):graph.connect_points(points[p],points[other])
   var doors=[];var errors=[]
   for side in sides:
    var p=Geometry.DIRS[side]*176
    if not points.has(p):errors.append("blocked door "+str(side))
    else:doors.append(points[p])
   for i in range(1,doors.size()):
    if graph.get_id_path(doors[0],doors[i]).is_empty():errors.append("disconnected door "+str(i))
   if points.size()<20:errors.append("insufficient interior")
   report.append({"key":Store.key(e.asset,q),"points":points.size(),"errors":errors})
  view.free()
 var f=FileAccess.open(OUT+"routes.json",FileAccess.WRITE);f.store_string(JSON.stringify(report,"  "));f.close()
 var failures=report.filter(func(r):return not r.errors.is_empty())
 if not failures.is_empty():
  printerr("PREFERRED LAYOUT FAIL: ",failures);quit(1);return
 print("PREFERRED LAYOUT PASS: ",report.size()," furnished orientations, all ports connected with production crew collision and segment checks");quit()
