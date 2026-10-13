extends SceneTree
const Actor=preload("res://scripts/room_scale_preview.gd")
class Board extends Node2D:
 var actors=[]
 var clock=0.0
 var family="walk"
 func _process(delta):
  clock+=delta
  queue_redraw()
 func _draw():
  draw_rect(Rect2(0,0,1400,900),Color("303b40"))
  var font=ThemeDB.fallback_font
  draw_string(font,Vector2(20,30),"Installed crew / "+family+" / Godot linear rendering",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
  var directions=["south","east","north","west"]
  for col in range(4):draw_string(font,Vector2(230+col*285,65),directions[col],HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
  for row in range(actors.size()):
   var actor=actors[row]
   draw_string(font,Vector2(15,120+row*270),Actor.CAST[actor.cast_index].name,HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color.WHITE)
   for col in range(4):
    var key=family+"-"+directions[col]
    var tex=actor.player.frame_at_elapsed(key,clock)
    assert(tex!=null)
    for size_index in range(3):
     var height=[82.0,54.0,27.0][size_index]
     var scale=height/148.0
     var foot=Vector2(220+col*285+size_index*85,250+row*270)
     draw_line(foot-Vector2(35,0),foot+Vector2(35,0),Color("66777a"))
     draw_texture_rect(tex,Rect2(foot-Vector2(92,172)*scale,Vector2(184,184)*scale),false)
func _init():call_deferred("run")
func run():
 root.size=Vector2i(1400,900)
 root.content_scale_size=Vector2i(1400,900)
 if not FileAccess.file_exists("res://tools/preview_installed_crew_directions.gd.uid"):
  var uid_file=FileAccess.open("res://tools/preview_installed_crew_directions.gd.uid",FileAccess.WRITE)
  uid_file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 var board=Board.new()
 root.add_child(board)
 for index in [0,2,3]:
  var actor=Actor.new()
  actor.mode=Actor.WALKING
  actor.set_cast(index)
  actor.load_art()
  board.actors.append(actor)
 for family in ["idle","walk"]:
  board.family=family
  board.clock=.5
  await process_frame
  await RenderingServer.frame_post_draw
  root.get_texture().get_image().save_png("res://character/crew-installed-direction-check-v1/"+family+".png")
 print("INSTALLED DIRECTION REVIEW: 3 crew x 4 directions x 3 sizes x idle/walk rendered")
 quit()
