extends SceneTree
## Exercise player-selected facing transitions in all 12 directed turns.
class Review extends Node2D:
    var textures: Array=[]
    var labels: Array=[]
    func _draw() -> void:
        draw_rect(Rect2(0,0,960,460),Color("293b40"))
        for col in range(textures.size()):
            var texture: Texture2D=textures[col]
            var x: float=120+col*240
            draw_string(ThemeDB.fallback_font,Vector2(x-112,25),labels[col],HORIZONTAL_ALIGNMENT_LEFT,-1,14)
            for row in range(2):
                var scale: float=1.0 if row==0 else 65.28/float(texture.get_meta("crew_standing_height"))
                var anchor:=Vector2(x,255 if row==0 else 402)
                draw_line(anchor-Vector2(100,0),anchor+Vector2(100,0),Color("839597"))
                draw_texture_rect(texture,Rect2(anchor-texture.get_meta("crew_pivot")*scale,texture.get_size()*scale),false)
func _init() -> void:call_deferred("run")
func run() -> void:
    if DisplayServer.get_name()=="headless":quit(2);return
    root.size=Vector2i(960,460);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
    var loaded_cargo: bool="--loaded-match" in OS.get_cmdline_user_args()
    var movement: String="swim-carry" if loaded_cargo else "swim"
    var output:="res://output/marsh-animation-audit/water-turn-native/"
    if loaded_cargo:output="res://output/marsh-animation-audit/loaded-water-native/"
    DirAccess.make_dir_recursive_absolute(output)
    var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
    var loaded=grid.marsh_player
    var contract: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-water-turn-match-v1/installation.json"))
    if loaded_cargo:contract=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-loaded-water-match-v1/installation.json"))
    var references: Dictionary={}
    var failures:=0
    for target in contract.frames:
        var source: String="res://"+str(contract.frames[target].source)
        var image:=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes(source))
        var state: String=str(contract.frames[target].source).get_slice("/",3)
        var slot: int=int(source.get_file().get_basename())
        if not references.has(state):references[state]={}
        references[state][slot]=image
        if loaded.frames[state][slot].get_image().get_data()!=image.get_data():failures+=1;push_error("Loaded source mismatch: "+target)
    var view:=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
    var directions: Array=["south","north","east","west"]
    var captures:=0
    var selected: Dictionary={}
    for step in range(1,4):
        var players: Array=[]
        for col in range(4):
            var player=preload("res://scripts/crew_sprite_player.gd").new();player.frames=loaded.frames;player.timing=loaded.timing
            player.frame(movement,directions[col],0,Vector2.ZERO,"",true);players.append(player)
        for sample in range(24):
            view.textures=[];view.labels=[]
            for col in range(4):
                var origin: String=directions[col]
                var destination: String=directions[(col+step)%4]
                var key:=movement+"-turn-"+origin+"-"+destination
                var player=players[col]
                var elapsed: float=float(sample)/24.0*player.cycle_seconds(key)+(.001 if sample>0 else 0.0)
                var texture: Texture2D=player.frame(movement,destination,1.0+elapsed,Vector2.ZERO,"",true)
                var expected: Texture2D=loaded.frame_at_elapsed(key,elapsed)
                if texture.get_image().get_data()!=expected.get_image().get_data() or player.motion.clip!=key:failures+=1;push_error("Turn selection mismatch: "+key)
                var slot:=0
                var cursor:=elapsed
                for i in range(player.timing[key].durations.size()-1):
                    var duration: float=float(player.timing[key].durations[i])/1000.0
                    if cursor<duration:break
                    cursor-=duration;slot+=1
                selected[key+"/"+str(slot)]=true
                view.textures.append(texture);view.labels.append(key)
            view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
            root.get_texture().get_image().save_png(output+"frame-%03d.png"%captures);captures+=1
        for col in range(4):
            var key:=movement+"-turn-"+str(directions[col])+"-"+str(directions[(col+step)%4])
            var player=players[col]
            var completed: Texture2D=player.frame(movement,directions[(col+step)%4],1.0+player.cycle_seconds(key)+.01,Vector2.ZERO,"",true)
            if not str(player.motion.clip).is_empty():failures+=1;push_error("Turn did not finish: "+key)
            var destination_key: String=movement+"-"+str(directions[(col+step)%4])
            if completed.get_image().get_data()!=loaded.frames[destination_key][0].get_image().get_data():failures+=1;push_error("Turn completion did not join destination zero: "+key)
    if selected.size()!=76:failures+=1;push_error("Incomplete native pose coverage: "+str(selected.size()))
    if loaded_cargo:
        var players: Array=[]
        for col in range(4):
            var player=preload("res://scripts/crew_sprite_player.gd").new();player.frames=loaded.frames;player.timing=loaded.timing;players.append(player)
        for sample in range(36):
            view.textures=[];view.labels=[]
            for col in range(4):
                var key:="swim-carry-"+str(directions[col])
                var elapsed: float=float(sample)*.06+(.003 if sample>0 else 0.0)
                var texture: Texture2D=players[col].frame(movement,directions[col],elapsed,Vector2.ZERO)
                var expected: Texture2D=loaded.frame_at_elapsed(key,fposmod(elapsed,loaded.cycle_seconds(key)))
                if texture.get_image().get_data()!=expected.get_image().get_data():failures+=1;push_error("Loaded loop mismatch: "+key)
                view.textures.append(texture);view.labels.append(key)
            view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
            root.get_texture().get_image().save_png(output+"frame-%03d.png"%captures);captures+=1
    grid.free()
    print("MARSH WATER TURNS: %d source matches, %d selected poses, %d captures, %d failures"%[contract.frames.size(),selected.size(),captures,failures])
    quit(1 if failures else 0)
