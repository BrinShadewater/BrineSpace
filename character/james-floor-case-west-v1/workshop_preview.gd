extends "res://rooms/underwater/salvage-workshop-v1/workshop_view.gd"
## Unselected visual fixture: fixed floor prop in the normal sorted room queue.
const CASE_PATH="res://character/james-floor-case-west-v1/floor-case-west.png"
const CASE_ID="james-floor-case-study"
const CASE_PIXEL_SCALE=65.28/148.0
var case_enabled:=false
var case_anchor:=Vector2.ZERO
var case_texture:Texture2D
func _ready()->void:
 super._ready()
 var image:=Image.new()
 preload("res://scripts/safe_image.gd").load_png(image,CASE_PATH)
 case_texture=ImageTexture.create_from_image(image)
func case_rect()->Rect2:
 return Rect2(case_anchor-Vector2(128,224)*CASE_PIXEL_SCALE,Vector2(256,256)*CASE_PIXEL_SCALE)
func _sorted_content_queue(live:Array)->Array:
 var queue:Array=super._sorted_content_queue(live)
 if case_enabled:
  var prop:Dictionary={"id":CASE_ID,"rect":case_rect(),"sort_y":case_anchor.y-2*CASE_PIXEL_SCALE,"registration":{},"library_asset":true,"custom_library_draw":true}
  var item:Dictionary={"kind":"prop","sort_y":prop.sort_y,"prop":prop}
  var at:int=queue.size()
  for index in queue.size():
   if float(queue[index].sort_y)>float(item.sort_y):at=index;break
  queue.insert(at,item)
 return queue
func prop_visual_bounds(prop:Dictionary)->Rect2:
 if prop.id==CASE_ID:return prop.rect
 return super.prop_visual_bounds(prop)
func draw_registered_prop(prop:Dictionary)->void:
 if prop.id==CASE_ID:
  painter.draw_texture_rect(case_texture,prop.rect,false)
  return
 super.draw_registered_prop(prop)
