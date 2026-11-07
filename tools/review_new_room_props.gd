extends SceneTree
## Isolated review only. Does not load or write player layouts/saves.
const Library=preload("res://scripts/room_asset_library.gd")
const Actor=preload("res://scripts/room_scale_preview.gd")
const View=preload("res://rooms/whole-room/nursery_south_facing.gd")
const PACK="res://assets/new-room-props-2026-09-26/catalog.json"
const OUT="res://assets/new-room-props-2026-09-26/review"
class PropReviewPanel extends Node2D:
 var painter
 var operating=false
 var machine_clock=0.0
 var props:Array=[]
 var crew:Texture2D
 var back=Color("263139")
 func _draw():
  painter=self
  for i in range(props.size()):
   var p:Dictionary=props[i]
   var origin=Vector2((i%5)*300+150,(i/5)*250+190)
   draw_rect(Rect2(origin-Vector2(145,170),Vector2(290,225)),back)
   draw_set_transform(origin)
   Library.draw(self,p)
   var pixel_scale=65.28/float(crew.get_meta("crew_standing_height",74.0))
   var foot=Vector2(p.rect.end.x+23,0)
   draw_texture_rect(crew,Rect2(foot-crew.get_meta("crew_pivot",Vector2(46,86))*pixel_scale,crew.get_size()*pixel_scale),false)
   if not p.get("floor_piece",false):
    var f:Array=p.footprint
    draw_rect(Rect2(p.rect.position+p.rect.size*Vector2(f[0],f[1]),p.rect.size*Vector2(f[2],f[3])),Color(0.2,0.8,0.65,.5),false,1)
   draw_set_transform(Vector2.ZERO)
   draw_string(ThemeDB.fallback_font,origin+Vector2(-140,32),str(p.id).trim_prefix("library/sp-new-"),HORIZONTAL_ALIGNMENT_LEFT,285,12,Color("e1e8e8") if back.r<.5 else Color("202830"))
func _init():call_deferred("run")
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 root.size=Vector2i(1500,1000);root.content_scale_size=root.size
 var records:Array=JSON.parse_string(FileAccess.get_file_as_string(PACK))
 var all=Library.entries()
 for r in records:
  all["library/"+r.id]={"data":r,"label":r.label,"width":r.display_width,"group":"station","category":r.category}
 var actor=Actor.new();actor.load_art()
 var panel=PropReviewPanel.new();panel.crew=actor.player.frame("idle","south",0.0,Vector2.ZERO)
 panel.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(panel)
 var view=View.new();view.embedded=true;view.hide();root.add_child(view)
 DirAccess.make_dir_recursive_absolute(OUT)
 var failures:Array=[];var checks=0;var pages=0
 for offset in range(0,records.size(),20):
  panel.props=[]
  for idx in range(offset,mini(offset+20,records.size())):
   var r:Dictionary=records[idx]
   var p=Library.template("library/"+r.id).duplicate(true)
   if p.is_empty():failures.append(r.id+": missing template");continue
   p.rect.position=Vector2(-p.rect.size.x*.5,-p.rect.size.y);p.sort_y=Library.base_sort_y(p)
   panel.props.append(p)
   # Single-prop central-floor placements in each supported room quarter.
   for q in range(4):
    view.configure_embedded(q,[],false,0.0)
    var trial=p.duplicate(true)
    trial.rect.position=Vector2(-trial.rect.size.x*.5,-trial.rect.size.y*.5)
    trial.sort_y=Library.base_sort_y(trial)
    view.props=[trial]
    actor.rebuild(view,"mycelium_nursery",q)
    if not actor.visible:failures.append(r.id+": no walking area q"+str(q))
    if not Rect2(-180,-180,360,360).encloses(trial.rect):failures.append(r.id+": outside floor envelope")
    for target in [Vector2(-160,0),Vector2(160,0),Vector2(0,-160),Vector2(0,160)]:
     if not actor.can_stand(target):failures.append(r.id+": obstructed perimeter")
     var near=actor.graph.get_closest_point(target)
     var start=actor.graph.get_closest_point(actor.foot)
     if near<0 or start<0 or actor.graph.get_id_path(start,near).is_empty():failures.append(r.id+": unreachable perimeter")
    checks+=1
  for ground in ["dark","light"]:
   panel.back=Color("263139") if ground=="dark" else Color("e8e3d8")
   panel.queue_redraw()
   await process_frame
   await RenderingServer.frame_post_draw
   var path=OUT+"/native-%02d-%s.png"%[pages,ground]
   if root.get_texture().get_image().save_png(path)!=OK:failures.append(path)
  pages+=1
 var result={"props":records.size(),"quarter_checks":checks,"native_pages":pages,"failures":failures,"scope":"Isolated central floor fixture and actual crew scale; no furnished-room or wall-mount acceptance."}
 var file=FileAccess.open(OUT+"/native-validation.json",FileAccess.WRITE);file.store_string(JSON.stringify(result,"  "));file.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

