extends SceneTree
const BARE := "res://character/veld-cargo-east-original-master-v3/bare-manifest.json"
const HELMET := "res://character/veld-cargo-east-original-master-v3/helmet-manifest.json"
const CONTRACT := "res://character/veld-cargo-east-original-master-v3/cargo-contract.json"
const PROP := preload("res://character/veld-cargo-east-original-master-v3/cargo_prop.gd")
const CASE := "res://character/veld-cargo-east-original-master-v3/floor-case.png"
const OUT := "res://output/veld-cargo-east-original-master-v3/"
var checks := 0
var failures := 0
var records: Array = []
func check(ok: bool, message: String) -> void:
 checks+=1
 if not ok: failures+=1;push_error(message)
class Board extends Node2D:
 var body: Texture2D
 var box: Texture2D
 var actor_foot:=Vector2.ZERO
 var prop_foot:=Vector2.ZERO
 var offset:=Vector2.ZERO
 var prop_visible:=false
 func _draw() -> void:
  draw_rect(Rect2(0,0,900,400),Color("202a30"))
  for i in range(3):
   var scale: float=[47.0,93.0,148.0][i]/148.0
   var anchor:=Vector2([110.0,360.0,680.0][i],335.0)
   draw_line(anchor+Vector2(-110,0),anchor+Vector2(110,0),Color("46545c"))
   draw_string(ThemeDB.fallback_font,Vector2(anchor.x-75,30),"Case stays on floor · %d"%int([47,93,148][i]),HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color.WHITE)
   if prop_visible: draw_texture_rect(box,Rect2(anchor+(prop_foot+offset)*scale,Vector2(box.get_width(),box.get_height())*scale),false)
   if body!=null: draw_texture_rect(body,Rect2(anchor+(actor_foot-Vector2(128,224))*scale,Vector2(256,256)*scale),false)
func _init() -> void: call_deferred("run")
func run() -> void:
 check(OS.get_environment("APPDATA").contains("veld-east-cargo-prop-scratch"),"Scratch profile required")
 if failures: quit(1);return
 DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUT));root.size=Vector2i(900,400);root.content_scale_size=Vector2i.ZERO
 var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(CONTRACT))
 var b:=Board.new();b.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;b.box=ImageTexture.create_from_image(Image.load_from_file(CASE));b.offset=Vector2(data.topLeftOffsetFromFoot[0],data.topLeftOffsetFromFoot[1]);root.add_child(b)
 var player=load("res://scripts/crew_sprite_player.gd").new();player.load_manifest(BARE);check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired gear")
 var keys: Array=["carry-east","unload-east","idle-east","pickup-east","carry-east"]
 var spans: Array=[0.2,0.52,0.8,0.52,0.2]
 for gear in ["bare","helmet"]:
  var prop=PROP.new();prop.configure(data);var equipment: String="" if gear=="bare" else "diving-helmet"
  var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BARE if gear=="bare" else HELMET));var states: Dictionary={}
  for state in pack.states:
   states[state.id]=state;check(state.frameCount==state.frameFiles.size(),"Count matches source")
   check(state.frameDurationsMs.size()==state.frameFiles.size(),"Timing count")
  for key in ["unload-east","pickup-east"]:
   check(is_equal_approx(player.cycle_seconds(key,equipment),.52),"Finite action timing")
   check(not states[key].loop,"Finite action")
   check(player.frame_at_elapsed(key,9.0,equipment).get_image().get_data()==Image.load_from_file(states[key].frameFiles[-1]).get_data(),"Finite tail")
  var seen: Dictionary={};var prior_segment: int=-1;var restored:=false;var held=player.frame_at_elapsed("carry-east",0.0,equipment).get_image().get_data()
  for n in range(71):
   var time: float=n/30.0;var local: float=time;var segment: int=4
   for i in range(5):
    if local<float(spans[i]) or i==4:segment=i;break
    local-=float(spans[i])
   var key: String=keys[segment];var state: Dictionary=states[key]
   if segment!=prior_segment:prop.begin(key);prior_segment=segment
   var actor_foot:=Vector2.ZERO
   # Prescribed root-position probe, not walking or navigation acceptance.
   if segment==2:actor_foot.x=-70.0*sin(clampf(local/.8,0.0,1.0)*PI)
   prop.advance(local,actor_foot)
   var slot: int=state.frameFiles.size()-1;var remaining: float=local
   for i in range(state.frameFiles.size()):
    if remaining<float(state.frameDurationsMs[i])/1000.0:slot=i;break
    remaining-=float(state.frameDurationsMs[i])/1000.0
   b.body=player.frame_at_elapsed(key,local,equipment);b.actor_foot=actor_foot;b.prop_foot=prop.foot;b.prop_visible=prop.present
   check(b.body.get_image().get_data()==Image.load_from_file(state.frameFiles[slot]).get_data(),"Actual body clock source")
   check(b.body.get_meta("crew_pivot")==Vector2(128,224),"Fixed physical root")
   check(b.body.get_meta("crew_standing_height")==148.0,"Original physical ruler")
   check(not b.body.get_meta("crew_water_pose"),"Dry body")
   var expected: bool=(segment==1 and local>=.26) or segment==2 or (segment==3 and local<.26)
   check(prop.present==expected,"Floor case ownership at contact/take")
   if prop.present:check(prop.foot==Vector2.ZERO,"Deposited case anchor independent of body")
   if segment==2 and local>.3 and not restored:
    var snapshot: Dictionary=JSON.parse_string(JSON.stringify(prop.snapshot()));var replacement=PROP.new();replacement.configure(data);check(replacement.restore(snapshot),"Serialized visual checkpoint restores");check(replacement.snapshot()==prop.snapshot(),"Visual snapshot exact");prop=replacement;restored=true
    var unchanged: Dictionary=prop.snapshot();check(not prop.restore({"present":true,"foot":["bad",0],"action":"idle-east","eventDone":false}),"Invalid visual checkpoint rejected");check(prop.snapshot()==unchanged,"Rejected restore preserves state")
   if segment==4:check(b.body.get_image().get_data()==held,"Original held return")
   seen[key+str(slot)]=true;b.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   var name: String=gear+"-%03d"%n;check(root.get_texture().get_image().save_png(OUT+name+"-native.png")==OK,"Native prop capture")
   records.append({"name":name,"gear":gear,"time":time,"localTime":local,"state":key,"slot":slot,"source":state.frameFiles[slot],"actorFoot":[actor_foot.x,actor_foot.y],"propFoot":[prop.foot.x,prop.foot.y],"propVisible":prop.present})
  check(seen.size()==14,"Every action body source observed");check(restored,"Visual checkpoint exercised")
  prop.begin("unload-east");prop.advance(.26,Vector2(12,8));check(prop.present and prop.foot==Vector2(12,8),"Fresh deposit anchors once")
  prop.advance(.5,Vector2(80,0));check(prop.foot==Vector2(12,8),"Same action cannot re-anchor case")
  prop.retire_on_delivery();check(not prop.present,"Delivery retirement hook")
  prop.advance(1.0,Vector2(80,0));check(not prop.present,"Delivery retirement not undone by completed action")
 var f:=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"  "));f.close()
 print("VELD EAST SEPARATE PROP: %d checks,%d failures;%dpresentations"%[checks,failures,records.size()]);quit(1 if failures else 0)
