extends "res://character/bill-floor-case-north-v1/flood_readability_v2.gd"
var bridge_grid
var material_weight:float=-1
var material_head_offset:=Vector2.ZERO
func draw_actor()->void:
 material_weight=-1
 if is_instance_valid(bridge_grid) and external_actor_texture==bridge_grid.material_source:
  material_weight=bridge_grid.material_weight
  material_head_offset=bridge_grid.material_head_offset
 if not readable_water or material_weight<0 or external_actor_texture==null:
  super.draw_actor();return
 const WATER=preload("res://scripts/flood_visuals.gd")
 var texture:Texture2D=external_actor_texture
 var scale:float=65.28/float(texture.get_meta("crew_standing_height",148))
 var pivot:Vector2=texture.get_meta("crew_pivot",Vector2(160,224))
 var rect:=Rect2(actor-pivot*scale,texture.get_size()*scale)
 var clock:float=WATER.condition_clock(flood_clock)
 # Both waterline formulas use the same physical actor root. As the pose
 # becomes horizontal, advance the surface split toward the normal swim line.
 var dry_line:float=WATER.crew_waterline(actor.y,flood_water,false)
 var swim_line:float=WATER.crew_waterline(actor.y,flood_water,true)
 var line:float=lerpf(dry_line,swim_line,clampf(material_weight,0,1))+sin(clock*2)*.55
 var fraction:float=clampf((line-rect.position.y)/rect.size.y,0,1)
 var tex:=Vector2(texture.get_size());var wet:float=clampf(material_weight,0,1)
 var swimming:Color=body_tint(flood_water)
 WATER.draw_crew_shadow(painter,actor,flood_water)
 if fraction>0:painter.draw_texture_rect_region(texture,Rect2(rect.position,Vector2(rect.size.x,rect.size.y*fraction)),Rect2(Vector2.ZERO,Vector2(tex.x,tex.y*fraction)),Color.WHITE.lerp(swimming,wet))
 if fraction<1:painter.draw_texture_rect_region(texture,Rect2(Vector2(rect.position.x,line),Vector2(rect.size.x,rect.end.y-line)),Rect2(Vector2(0,tex.y*fraction),Vector2(tex.x,tex.y*(1-fraction))),Color(.30,.66,.70,.35 if flood_water<.85 else .22).lerp(swimming,wet))
 var head:Vector2=actor+material_head_offset
 var weight:float=wet*head_weight(flood_water)
 if weight>0:
  var points:=PackedVector2Array();var uv:=PackedVector2Array()
  for i in range(24):
   var angle:float=TAU*i/24;var point:Vector2=head+Vector2(cos(angle)*13,sin(angle)*12);points.append(point);uv.append((point-rect.position)/rect.size)
  var submersion:float=clampf((flood_water-.55)/.45,0,1)
  painter.draw_polygon(points,PackedColorArray([Color(1,1,1,(1-submersion*.5)*weight)]),uv,texture)
 draw_fading_wake(painter,Vector2(actor.x,line).lerp(head+Vector2(0,5),wet),texture,clock,lerpf(8,14,wet),lerpf(1,head_weight(flood_water),wet))
 var bubbles:float=wet*smoothstep(.75,.95,flood_water)
 for i in range(3):
  var phase:float=fposmod(clock*.7+i*.33,1);painter.draw_arc(head+Vector2(sin(clock*2+i)*3,-phase*23),1+phase,0,TAU,10,Color(.6,.8,.78,(1-phase)*.65*bubbles),.7,true)
