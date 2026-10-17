from pathlib import Path
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent
old=(R/'character/krusher-continuous-playback-v1/native/bunk.gd').read_text()
prefix=old[:old.index(' var jobs:Array=')]
prefix=prefix.replace('character/krusher-continuous-playback-v1/native/bunk.gd.uid','character/krusher-station-motion-v1/motion.gd.uid').replace('character/krusher-continuous-playback-v1/review/bunk','character/krusher-station-motion-v1/review')
prefix=prefix.replace('func run()->void:', 'func digest(data:PackedByteArray)->String:\n var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(data);return hash.finish().hex_encode()\nfunc run()->void:')
tail=''' var jobs:Array=JSON.parse_string(FileAccess.get_file_as_string(JOBS))
 var expected:Dictionary={}
 for job in jobs:
  var hashes:Array=[]
  for source in job.files:hashes.append(digest(Image.load_from_file(source).get_data()))
  expected[job.gear+":"+job.key]=hashes
 var coverage:Dictionary={}
 for gear in ["bare","helmet"]:
  actor.helmet_equipped=gear=="helmet";actor.stage="life_lie";actor.state="idle";actor.timer=actor.BUNK_SECONDS;actor.bunk_motion=motion.duplicate(true)
  actor.path.clear();actor.goal="fatigue";actor.goal_cell=HAB
  for need in actor.needs:actor.needs[need]=0.0
  player.current_key="";player.last_time=-1.0;player.motion.clear()
  var previous_action="";var stages:Array=[];var elapsed=0.0
  for frame in range(600):
   var action:String=actor.animation_state()
   game.visual_time_seconds=elapsed
   var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
   check(texture!=null,"Controller supplies a visible texture")
   var source_hash:String=digest(pixels(texture))
   var key:String=gear+":"+action+"-east"
   if expected.has(key):
    check(source_hash in expected[key],"Actual controller uses current candidate source")
    if not coverage.has(key):coverage[key]=[]
    if source_hash not in coverage[key]:coverage[key].append(source_hash)
   check(texture.get_meta("crew_standing_height")==148.0,"Station detail ruler retained")
   game._restore_grid_view_center(camera_center);game.grid_view.queue_redraw()
   await process_frame
   await RenderingServer.frame_post_draw
   var filename:String="%s-%04d.png"%[gear,frame]
   var room:Image=room_pixels(HAB);room.save_png(capture_dir.path_join(filename))
   if previous_action!=action:
    stages.append(action)
    root.get_texture().get_image().save_png(capture_dir.path_join("%s-%s-full.png"%[gear,action]))
   var world_foot:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038)+actor.observation_visual_offset()*game.get_cell_size()/384.0
   var sprite_scale:float=game.get_cell_size()/384.0*65.28/148.0
   var sprite_rect:Rect2=Rect2(world_foot-Vector2(texture.get_meta("crew_pivot"))*sprite_scale,texture.get_size()*sprite_scale)
   var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*sprite_rect
   var clip:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
   check(clip.encloses(screen),"Whole actor canvas is in the viewport")
   check(game._grid_view_center_ratio().distance_to(camera_center)<.002,"Camera remains on bunk")
   records.append({"file":filename,"gear":gear,"frame":frame,"time":elapsed,"action":action,"stage":actor.stage,"timer":actor.timer,"sourceHash":source_hash,"scale":sprite_scale,"screen":[screen.position.x,screen.position.y,screen.size.x,screen.size.y],"roomSize":[room.get_width(),room.get_height()]})
   previous_action=action
   if stages.size()>=3 and not actor.bunk_motion_active():break
   actor.update(game,1.0/30.0);elapsed+=1.0/30.0
  check(stages.slice(0,3)==["bunk-enter","bunk-sleep","bunk-exit"],"Advancing controller completes entry/sleep/exit in order")
  check(not actor.bunk_motion_active(),"Exit releases real mattress contact")
 for key in expected:
  var seen:Array=coverage.get(key,[])
  for source in expected[key]:check(source in seen,"Advancing draw covers every authored bunk hold source")
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"coverage":coverage,"scope":"Two actual main-scene bunk lifecycles advanced at 30Hz with production actor updates and rendering. Default authored bunk at centered room zoom .9. Captured native frames preserve simulated cadence; PNG capture is not a real-time video, other furniture and roster integration remain separate."},"\\t"))
 print("KRUSHER_STATION_MOTION checks=%d failures=%d frames=%d"%[checks,failures,records.size()]);game.free();quit(1 if failures else 0)
'''
(H/'motion.gd').write_text(prefix+tail)
runner=(R/'character/krusher-continuous-playback-v1/run_bunk.py').read_text().replace("review=P/'review/bunk'","review=P/'review'").replace("'native/scratch-appdata-bunk'","'scratch-appdata'").replace('character/krusher-continuous-playback-v1/native/bunk.gd','character/krusher-station-motion-v1/motion.gd').replace('KRUSHER_BUNK','KRUSHER_STATION_MOTION').replace('timeout=120','timeout=180')
(H/'run_native.py').write_text(runner)
print('Prepared bounded advancing native review')
