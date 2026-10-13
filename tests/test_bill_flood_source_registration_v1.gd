extends SceneTree
func _init():call_deferred("run")
func run():
 var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations()
 var player=grid.human_water_player;var found:Dictionary={};var count:=0
 for gear in ["","diving-helmet"]:
  var clips:Dictionary=player.frames if gear=="" else player.equipment_frames[gear]
  for key in clips:
   if not (key.begins_with("walk-") or key.begins_with("swim-") or key.begins_with("tread-") or key.begins_with("idle-")):continue
   for index in clips[key].size():
    var texture:Texture2D=clips[key][index];var im:Image=texture.get_image();im.convert(Image.FORMAT_RGBA8)
    var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(im.get_data());var hash:String=h.finish().hex_encode()
    var pivot:Vector2=texture.get_meta("crew_pivot",Vector2(46,86));var standing:float=texture.get_meta("crew_standing_height",74.0)
    if not found.has(hash):found[hash]=[]
    found[hash].append({"key":key,"gear":gear,"index":index,"pivot":[pivot.x,pivot.y],"standingHeight":standing,"size":[im.get_width(),im.get_height()]});count+=1
 var f=FileAccess.open("res://output/bill-flood-source-registration-v1/metadata.json",FileAccess.WRITE);f.store_string(JSON.stringify(found,"  "));grid.free()
 print("BILL FLOOD SOURCE REGISTRATION V1: %d checks,0 failures"%count);quit()
