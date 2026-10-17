extends SceneTree
## Prescribed clear-room corner; real Bill move and sprite-player clocks, not natural goal selection.
const PLAYER=preload("res://scripts/crew_sprite_player.gd")
const NPC=preload("res://scripts/bill_npc.gd")
const PREVIEW=preload("res://character/bill-carry-turn-east-south-motion-v3/carry_motion_preview.gd")
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 if failures:quit(2);return
 var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations()
 var view:=SubViewport.new();view.size=Vector2i(2000,1440);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
 var bg:=ColorRect.new();bg.color=Color("22343e");bg.size=Vector2(2000,1440);view.add_child(bg)
 var journeys:=[];var lane:=0;var source_ids:={}
 for helmet in [false,true]:
  var gear:String="diving-helmet" if helmet else ""
  for reverse in [false,true]:
   for candidate in [true,false]:
    var player=PLAYER.new()
    for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,grid.human_water_player.get(property).duplicate(true))
    if candidate:
     player.load_manifest("res://character/bill-carry-turn-east-south-motion-v3/bare-manifest.json",true)
     check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-east-south-motion-v3/helmet-manifest.json"),"Staged helmet admission")
    var actor=PREVIEW.new() if candidate else NPC.new();
    if candidate:actor.preview_player=player
    actor.active=true;actor.helmet_equipped=helmet;actor.stage="workshop_carry"
    actor.geometry={Vector2i.ZERO:{"large_room":true,"open":[],"blockers":[]}}
    actor.foot=Vector2(160,100) if reverse else Vector2(100,160)
    actor.direction="south" if reverse else "east"
    actor.path=PackedVector2Array([Vector2(160,160),Vector2(300,160) if reverse else Vector2(160,300)])
    var title:=Label.new();title.text=("STAGED" if candidate else "NORMAL")+" "+("helmet" if helmet else "bare")+" "+("S/E" if reverse else "E/S");title.position=Vector2(8,lane*180+4);title.add_theme_font_size_override("font_size",14);view.add_child(title)
    player.frame(actor.animation_state(),actor.direction,0,actor.foot/384.0,gear)
    var records:=[];var onset:=-1.0;var start_foot:=Vector2.ZERO;var end_foot:=Vector2.ZERO;var sample:=0
    for step in range(240):
     var time:float=(step+1)/60.0
     if candidate:actor.preview_time=time
     var before:Vector2=actor.foot;actor.move(1.0/60.0)
     check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"Actual movement remains clear")
     check(actor.animation_state()=="carry","Real workshop carry pose")
     var texture:Texture2D=player.frame(actor.animation_state(),actor.direction,time,actor.foot/384.0,gear)
     var turning:bool=not str(player.motion.get("clip","")).is_empty()
     if onset<0 and turning:onset=time;start_foot=actor.foot
     if onset>=0:
      var elapsed:float=time-onset
      var source_id:int=texture.get_instance_id()
      if not source_ids.has(source_id):
       var source_file:String="source-%03d.png"%source_ids.size();source_ids[source_id]=source_file
       check(texture.get_image().save_png("res://output/bill-carry-corner-planted-preview/"+source_file)==OK,"Recorded exact displayed source")
      records.append({"seconds":time,"turnElapsed":elapsed,"foot":[actor.foot.x,actor.foot.y],"sourceCapture":source_ids[source_id],"turning":turning,"gaitPhase":player.phase})
      if elapsed>=.8 and end_foot==Vector2.ZERO:end_foot=actor.foot
      if sample<10 and elapsed+0.00001>=sample*.1:
       var pivot:Vector2=texture.get_meta("crew_pivot");var scale:float=82.0/148.0
       var physical:Vector2=Vector2(90+sample*200,lane*180+103)+(actor.foot-start_foot)*82.0/(384.0*.17)
       var dot:=ColorRect.new();dot.color=Color("ffad59");dot.size=Vector2(4,4);dot.position=physical-Vector2(2,2);view.add_child(dot)
       var sprite:=Sprite2D.new();sprite.texture=texture;sprite.centered=false;sprite.scale=Vector2.ONE*scale;sprite.position=physical-pivot*scale;view.add_child(sprite)
       var label:=Label.new();label.text="%.2fs %s"%[elapsed,"turn" if turning else "walk"];label.position=Vector2(sample*200+10,lane*180+120);label.add_theme_font_size_override("font_size",12);view.add_child(label)
       sample+=1
      if elapsed>.95:break
    check(onset>0 and sample==10,"Corner and post-turn samples captured")
    var drift:float=start_foot.distance_to(end_foot)
    check(drift<1.0 if candidate else (drift>36 and drift<38),"Planted candidate compared with translating baseline; completion includes first resumed step")
    journeys.append({"candidate":candidate,"gear":gear,"reverse":reverse,"turnTravelWorldUnits":drift,"records":records});lane+=1
 await RenderingServer.frame_post_draw
 check(view.get_texture().get_image().save_png("res://output/bill-carry-corner-planted-preview/corner-board.png")==OK,"Fresh native trajectory board")
 var report:=FileAccess.open("res://output/bill-carry-corner-planted-preview/journeys.json",FileAccess.WRITE);report.store_string(JSON.stringify({"scope":"Authoring-only Bill movement subclass versus production BillNPC.move, fixture-only clear geometry/prescribed corner, real animation_state and CrewSpritePlayer. Not main-scene draw, natural navigation, services, or Continue/checkpoint compatible.","checks":checks,"failures":failures,"journeys":journeys},"  "))
 grid.free();print("BILL CARRY CORNER PLANTED PREVIEW: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
