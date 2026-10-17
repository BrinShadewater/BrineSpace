extends "res://character/bill-floor-case-north-v1/release_workshop.gd"
## Staged water material continuity; unchanged original source, pivot and depth.
var readable_water := true
static func body_tint(water:float)->Color:
 var depth:float=clampf((water-.55)/.45,0,1)
 var original:=Color(.37,.71,.74,lerpf(.70,.23,depth))
 return original.lerp(Color(.72,.86,.86,.90),smoothstep(.55,.95,water))
static func head_weight(water:float)->float:
 return 1.0-smoothstep(.70,.95,water)
func draw_actor()->void:
 if not readable_water or external_actor_texture==null or flood_water<=.55 or not external_actor_texture.get_meta("crew_water_pose",false):
  super.draw_actor();return
 const WATER=preload("res://scripts/flood_visuals.gd")
 WATER.draw_crew_shadow(painter,actor,flood_water)
 var texture:Texture2D=external_actor_texture
 var scale:float=65.28/float(texture.get_meta("crew_standing_height",74.0))
 var pivot:Vector2=texture.get_meta("crew_pivot",Vector2(46,86))
 var rect:=Rect2(actor-pivot*scale,texture.get_size()*scale)
 painter.draw_texture_rect(texture,rect,false,body_tint(flood_water))
 var clock:float=WATER.condition_clock(flood_clock)
 var facing:String=texture.get_meta("crew_water_facing","east")
 var offset:Vector2={"east":Vector2(22,-6),"west":Vector2(-22,-6),"north":Vector2(0,-12),"south":Vector2(0,14)}.get(facing,Vector2.ZERO)
 if texture.get_meta("crew_water_kind","")=="tread":offset=Vector2(0,-13)
 var head:Vector2=actor+offset
 var weight:float=head_weight(flood_water)
 if weight>0:
  var points:=PackedVector2Array();var uv:=PackedVector2Array()
  for i in range(24):
   var angle:float=TAU*i/24.0
   var point:Vector2=head+Vector2(cos(angle)*13,sin(angle)*12)
   points.append(point);uv.append((point-rect.position)/rect.size)
  var submersion:float=clampf((flood_water-.55)/.45,0,1)
  painter.draw_polygon(points,PackedColorArray([Color(1,1,1,(1-submersion*.5)*weight)]),uv,texture)
  # Fade the surface wake with the head, instead of removing both at .85.
  draw_fading_wake(painter,head+Vector2(0,5),texture,clock,14.0,weight)
 var bubbles:float=smoothstep(.75,.95,flood_water)
 for i in range(3):
  var phase:float=fposmod(clock*.7+i*.33,1.0)
  painter.draw_arc(head+Vector2(sin(clock*2+i)*3,-phase*23),1+phase,0,TAU,10,Color(.6,.8,.78,(1-phase)*.65*bubbles),.7,true)

static func draw_fading_wake(canvas,contact: Vector2,texture: Texture2D,clock: float,width: float, weight: float) -> void:
 clock=preload("res://scripts/flood_visuals.gd").condition_clock(clock)
 var facing: String=texture.get_meta("crew_water_facing","south")
 var direction: Vector2={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}.get(facing,Vector2.DOWN)
 var side := Vector2(-direction.y,direction.x)
 var kind: String=texture.get_meta("crew_water_kind","")
 var moving := kind in ["walk","swim"]
 # Two separated, tapered disturbances leave the front and center open.
 # Moving poses trail behind the body; idle/treading only stirs nearby water.
 for bank in [-1,1]:
  var previous := Vector2.ZERO
  for i in range(9):
   var t := i/8.0
   var pulse := sin(clock*3.1+bank*1.7-t*4)
   var lateral := width*(0.58+t*0.45)+pulse*0.6
   var behind := lerpf(-2.0,20.0 if moving else 6.0,t)
   var offset: Vector2 = side*lateral*float(bank)-direction*behind
   offset.y*=0.38
   var point: Vector2 = contact+offset
   if i>0:
    var alpha := sin(PI*(t-0.0625))*0.28*(0.85+sin(clock*2+bank)*0.15)
    canvas.draw_line(previous,point,Color(0.62,0.76,0.72,alpha*weight),0.7,true)
   previous=point

