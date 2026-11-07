extends "res://character/bill-floor-case-north-v1/release_workshop.gd"
## Diagnostic only: keep normal placement/depth but isolate crew attenuation.
var white_crew:=false
func draw_actor()->void:
 if not white_crew or external_actor_texture==null:super.draw_actor();return
 var scale:float=65.28/float(external_actor_texture.get_meta("crew_standing_height",74.0))
 var pivot:Vector2=external_actor_texture.get_meta("crew_pivot",Vector2(46,86))
 painter.draw_texture_rect(external_actor_texture,Rect2(actor-pivot*scale,external_actor_texture.get_size()*scale),false,Color.WHITE)
