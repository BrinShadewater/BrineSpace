extends "res://scripts/james_cargo_workshop.gd"
## Unselected visual fixture: fixed floor prop in the normal sorted room queue.
const VELD_CASE_PATH="res://character/veld-cargo-north-master-family-v1/rise-join-v3/floor-case-canvas.png"
const VELD_CASE_ID="veld-floor-case-study"
const VELD_CASE_PIXEL_SCALE=65.28/148.0
var veld_case_enabled:=false
var veld_case_anchor:=Vector2.ZERO
var veld_case_texture:Texture2D
func _ready()->void:
 super._ready()
 var image:=Image.new()
 preload("res://scripts/safe_image.gd").load_png(image,VELD_CASE_PATH)
 veld_case_texture=ImageTexture.create_from_image(image)
func veld_case_rect()->Rect2:
 return Rect2(veld_case_anchor-Vector2(128,224)*VELD_CASE_PIXEL_SCALE,Vector2(256,256)*VELD_CASE_PIXEL_SCALE)
func _sorted_content_queue(live:Array)->Array:
 var queue:Array=super._sorted_content_queue(live)
 if veld_case_enabled:
  var prop:Dictionary={"id":VELD_CASE_ID,"rect":veld_case_rect(),"sort_y":veld_case_anchor.y-7*VELD_CASE_PIXEL_SCALE,"registration":{},"library_asset":true,"custom_library_draw":true}
  var item:Dictionary={"kind":"prop","sort_y":prop.sort_y,"prop":prop}
  var at:int=queue.size()
  for index in queue.size():
   if float(queue[index].sort_y)>float(item.sort_y):at=index;break
  queue.insert(at,item)
 return queue
func prop_visual_bounds(prop:Dictionary)->Rect2:
 if prop.id==VELD_CASE_ID:return prop.rect
 return super.prop_visual_bounds(prop)
func draw_registered_prop(prop:Dictionary)->void:
 if prop.id==VELD_CASE_ID:
  painter.draw_texture_rect(veld_case_texture,prop.rect,false)
  return
 super.draw_registered_prop(prop)
