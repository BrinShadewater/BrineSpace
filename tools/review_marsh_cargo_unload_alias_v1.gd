extends SceneTree
const Player=preload("res://scripts/crew_sprite_player.gd")
const Actor=preload("res://scripts/marsh_npc.gd")
const INDEX="res://character/marsh-v2/supplemental/cargo-unload-matched-v1/selection.json"
const CATALOG="res://character/marsh-v2/catalog.json"
const ADMISSION="res://character/marsh-v2/supplemental/cargo-unload-matched-v1/admission.json"
const OUTPUT="res://output/marsh-animation-audit/cargo-unload-alias-player-v1-2026-10-03/"
class Review extends Node2D:
 var textures:Array=[]
 var heading:String=""
 func _draw():
  draw_rect(Rect2(0,0,672,490),Color("293b40"))
  for col in range(textures.size()):
   var t:Texture2D=textures[col]
   for row in range(2):
    var z:float=1.0 if row==0 else 65.28/float(t.get_meta("crew_standing_height"))
    var anchor=Vector2(112+224*col,275 if row==0 else 440)
    draw_texture_rect(t,Rect2(anchor-Vector2(t.get_meta("crew_pivot"))*z,t.get_size()*z),false)
   draw_string(ThemeDB.fallback_font,Vector2(4+224*col,25),heading+" / "+["Old elapsed","Selected","Own idle"][col],HORIZONTAL_ALIGNMENT_LEFT,-1,10)
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func player_for(catalog:Dictionary):
 var p=Player.new()
 for f in catalog.body:p.load_manifest(CATALOG.get_base_dir().path_join(f).simplify_path(),true)
 var equipment_ok:=true
 for f in catalog.equipment:
  var loaded:bool=p.load_equipment_manifest("diving-helmet",CATALOG.get_base_dir().path_join(f).simplify_path())
  if not loaded:equipment_ok=false
 check(equipment_ok and p.frames.size()==228,"normal body/equipment profile loaded")
 return p
func same(a:Texture2D,b:Texture2D)->bool:return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func _init():call_deferred("run")
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 root.size=Vector2i(672,490);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
 DirAccess.make_dir_recursive_absolute(OUTPUT)
 var catalog:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(CATALOG))
 var player=player_for(catalog);var clone=player_for(catalog)
 var receipt:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(ADMISSION));var old=player_for(receipt.catalogBefore)
 var empty:Dictionary=player.snapshot();var view=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
 var actor=Actor.new();check(not actor.needs_air() and not actor.begin_helmet_action(true),"android air/helmet remains unchanged")
 var selection:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(INDEX));var captures:Array=[];var samples:Array=[];var states:=0;var slots:=0;var restores:=0
 for rel in selection.manifests:
  var mp:String="res://"+rel;var data:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(mp))
  for entry in data.states:
   states+=1;var key:String=entry.id;var split:int=key.rfind("-");var state:String=key.substr(0,split);var direction:String=key.substr(split+1)
   var durations:Array=entry.frameDurationsMs;var total:float=0
   for ms in durations:total+=float(ms)/1000.0
   check(player.frames.has(key) and player.frames[key].size()==entry.frameFiles.size(),"actual selected state count")
   check(is_equal_approx(player.cycle_seconds(key),total) and player.timing[key].loop==entry.loop,"original timing/loop preserved")
   player.restore_snapshot(empty);player.frame(state,direction,100,Vector2.ZERO)
   var elapsed:=0.0
   for i in range(entry.frameFiles.size()):
    slots+=1;var image:=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes(entry.frameFiles[i]));var reference=ImageTexture.create_from_image(image)
    var texture:Texture2D=player.frames[key][i]
    check(same(reference,texture),"normal source RGBA exact "+key+str(i))
    check(texture.get_meta("crew_pivot")==Vector2(data.pivot[0],data.pivot[1]) and texture.get_meta("crew_standing_height")==data.standingHeight,"source-specific profile retained")
    var middle:float=elapsed+float(durations[i])/2000.0
    var has_stride:bool=player.strides.has(key) or player.strides.has(state)
    var stride:float=float(player.strides.get(key,player.strides.get(state,.12)))
    var position:Vector2=Vector2(middle*stride/total,0) if has_stride else Vector2.ZERO
    var presented:Texture2D=player.frame(state,direction,100+middle,position)
    check(same(presented,texture) and same(player.frame_at_elapsed(key,middle),texture),"stateful midpoint and elapsed source agree")
    var snap:Dictionary=player.snapshot();check(Player.valid_snapshot(snap),"actual player cursor validates")
    clone.restore_snapshot(bytes_to_var(var_to_bytes(snap)))
    check(same(clone.frame(state,direction,100+middle,position),texture) and clone.snapshot()==snap,"normal player same-clock restore hold");restores+=1
    samples.append({"key":key,"slot":i,"elapsed":middle,"stride":stride if has_stride else 0})
    if i in [0,int(entry.frameFiles.size()/2),entry.frameFiles.size()-1]:
     view.heading=key+" slot"+str(i);view.textures=[old.frame_at_elapsed(key,middle),texture,player.frames["idle-"+direction][0]]
     view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
     var name:String="native-%s-%02d.png"%[key,i];check(root.get_texture().get_image().save_png(OUTPUT+name)==OK,"native source/station comparison capture")
     captures.append({"file":name,"key":key,"slot":i})
    elapsed+=float(durations[i])/1000.0
   var tail:float=total+.001;var position:Vector2=Vector2(tail*float(player.strides.get(key,player.strides.get(state,.12)))/total,0) if player.strides.has(key) or player.strides.has(state) else Vector2.ZERO
   check(same(player.frame(state,direction,100+tail,position),player.frames[key][0 if entry.loop else entry.frameFiles.size()-1]),"loop wraps or finite clip holds endpoint")
 check(states==4 and slots==16 and restores==16,"complete admitted cargo source/player coverage")
 var f=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"states":states,"slots":slots,"playerRestores":restores,"samples":samples,"captures":captures,"scope":"Normal catalogue/equipment loaded; all4retained cargo-unload aliases/16exact sources, source-specific pivots/height, midpoint stateful/elapsed clocks,16player restore holds and loop/finite endpoints. First/middle/last native source/station comparison captures. No live actor/contact/fullRunSave/Continue or continuous cadence/full-set acceptance."},"\t"));f.close()
 print("MARSH CARGO UNLOAD ALIAS PLAYER: ",checks,"checks,",failures,"failures,",captures.size(),"captures")
 quit(1 if failures else 0)
