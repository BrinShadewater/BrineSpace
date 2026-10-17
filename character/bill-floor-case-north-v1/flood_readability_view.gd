extends "res://character/bill-floor-case-north-v1/release_workshop.gd"
## Staged Bill-only high-water readability study. Original source/depth retained.
var readability_alpha := -1.0
func draw_actor() -> void:
 if readability_alpha<0 or external_actor_texture==null or flood_water<0.85 or not external_actor_texture.get_meta("crew_water_pose",false):
  super.draw_actor();return
 const WATER=preload("res://scripts/flood_visuals.gd")
 WATER.draw_crew_shadow(painter,actor,flood_water)
 var texture:Texture2D=external_actor_texture
 var scale:float=65.28/float(texture.get_meta("crew_standing_height",74.0))
 var pivot:Vector2=texture.get_meta("crew_pivot",Vector2(46,86))
 painter.draw_texture_rect(texture,Rect2(actor-pivot*scale,texture.get_size()*scale),false,Color(.72,.86,.86,readability_alpha))
 # Same submerged-head bubble locations/clock as the selected water renderer.
 var clock:float=WATER.condition_clock(flood_clock)
 var facing:String=texture.get_meta("crew_water_facing","east")
 var offset:Vector2={"east":Vector2(22,-6),"west":Vector2(-22,-6),"north":Vector2(0,-12),"south":Vector2(0,14)}.get(facing,Vector2.ZERO)
 if texture.get_meta("crew_water_kind","")=="tread":offset=Vector2(0,-13)
 var head:Vector2=actor+offset
 for i in range(3):
  var phase:float=fposmod(clock*.7+i*.33,1.0)
  painter.draw_arc(head+Vector2(sin(clock*2+i)*3,-phase*23),1+phase,0,TAU,10,Color(.6,.8,.78,(1-phase)*.65),.7,true)
