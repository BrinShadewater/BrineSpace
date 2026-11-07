extends SceneTree
## Native selected-player review; does not simulate a maintenance room assignment.
class Review extends Node2D:
    var textures: Array=[]
    var state: String=""
    func _draw() -> void:
        draw_rect(Rect2(0,0,960,460),Color("293b40"))
        for col in range(textures.size()):
            var texture: Texture2D=textures[col]
            if texture==null:continue
            var x: float=120+col*240
            draw_string(ThemeDB.fallback_font,Vector2(x-80,26),["south","north","east","west"][col]+" / "+state,HORIZONTAL_ALIGNMENT_LEFT,-1,16)
            draw_string(ThemeDB.fallback_font,Vector2(x-75,54),"Source / station scale",HORIZONTAL_ALIGNMENT_LEFT,-1,14)
            for row in range(2):
                var scale: float=1.0 if row==0 else 65.28/float(texture.get_meta("crew_standing_height"))
                var anchor:=Vector2(x,255 if row==0 else 402)
                draw_line(anchor-Vector2(100,0),anchor+Vector2(100,0),Color("839597"))
                draw_texture_rect(texture,Rect2(anchor-texture.get_meta("crew_pivot")*scale,texture.get_size()*scale),false)
func _init() -> void:call_deferred("run")
func run() -> void:
    if DisplayServer.get_name()=="headless":quit(2);return
    root.size=Vector2i(960,460);root.content_scale_size=Vector2i.ZERO;root.content_scale_factor=1.0
    var seated: bool="--seated-match" in OS.get_cmdline_user_args()
    var rest: bool="--rest-match" in OS.get_cmdline_user_args()
    var water: bool="--water-match" in OS.get_cmdline_user_args()
    var galley: bool="--galley-match" in OS.get_cmdline_user_args()
    var recovery: bool="--water-recovery-match" in OS.get_cmdline_user_args()
    var shutdown: bool="--shutdown-match" in OS.get_cmdline_user_args()
    var output: String="res://output/marsh-animation-audit/maintenance-native/"
    if seated:output="res://output/marsh-animation-audit/seated-native/"
    if rest:output="res://output/marsh-animation-audit/rest-native/"
    if water:output="res://output/marsh-animation-audit/water-native/"
    if shutdown:output="res://output/marsh-animation-audit/shutdown-native/"
    if recovery:output="res://output/marsh-animation-audit/water-recovery-native/"
    if galley:output="res://output/marsh-animation-audit/galley-native/"
    DirAccess.make_dir_recursive_absolute(output)
    var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations()
    var loaded=grid.marsh_player
    var contract: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-maintenance-match-v1/installation.json"))
    if seated:contract=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-seated-match-v1/installation.json"))
    if rest:contract=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-rest-match-v1/installation.json"))
    if water:contract=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-water-match-v1/installation.json"))
    if shutdown:contract=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-shutdown-injury-match-v1/installation.json"))
    if recovery:contract=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-water-recovery-match-v1/installation.json"))
    if galley:contract=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-galley-match-v1/installation.json"))
    if not (seated or rest or water or shutdown or recovery or galley):
        var tone: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-controller-tone-v1/installation.json"))
        contract.frames.merge(tone.frames,true)
    var polish: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-full-polish-v1/colour-lock.json"))
    for path in contract.frames.keys():
        if polish.has(path):contract.frames[path]=polish[path]
    var references: Dictionary={}
    var failures:=0
    if galley:
        var actor=preload("res://scripts/marsh_npc.gd").new()
        var life=preload("res://scripts/crew_life.gd")
        for direction in ["south","north","east","west"]:
            actor.direction=direction
            if not life.begin(actor,{"room":"galley"}) or actor.animation_state()!="eat":failures+=1;push_error("Galley meal selection")
            if not life.next(actor) or actor.animation_state()!="drink":failures+=1;push_error("Galley drink transition")
            if actor.needs_air() or actor.helmet_equipped:failures+=1;push_error("Galley android traits")
        actor=null
    if recovery:
        var actor=preload("res://scripts/marsh_npc.gd").new()
        var life=preload("res://scripts/crew_life.gd")
        actor.movement_medium="exterior";actor.breath_oxygen=0.0;actor.tank_oxygen=0.0
        if actor.needs_air() or life.pose(actor)=="swim-distress":failures+=1;push_error("Android incorrectly needs air")
        actor.die()
        if not actor.dead or actor.animation_state()!="death-water":failures+=1;push_error("Android wet shutdown selection")
        actor=null
    if shutdown:
        var actor=preload("res://scripts/marsh_npc.gd").new()
        actor.movement_medium="dry";actor.die()
        if actor.needs_air() or not actor.dead or actor.animation_state()!="death-ground":failures+=1;push_error("Android dry shutdown selection")
        actor=null
    if rest:
        var actor=preload("res://scripts/marsh_npc.gd").new()
        var life=preload("res://scripts/crew_life.gd")
        for direction in ["south","north","east","west"]:
            actor.direction=direction;actor.stage="";actor.dead=false;actor.movement_medium="dry"
            if not life.begin(actor,{"room":"crew_quarters","mode":"sleep"}):failures+=1
            for expected in ["lie-down","sleep","get-up"]:
                if actor.animation_state()!=expected or actor.berth_motion_active() or actor.bunk_motion_active():
                    failures+=1;push_error("Generic rest stage selection: "+direction+" / "+expected)
                if expected!="get-up":life.next(actor)
        actor=null
    for target in contract.frames:
        var source: String="res://"+str(contract.frames[target].source)
        var image:=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes(source))
        var state: String=str(contract.frames[target].source).get_slice("/",3)
        var slot: int=int(str(contract.frames[target].source).get_file().get_basename())
        if not references.has(state):references[state]={}
        references[state][slot]=image
        if loaded.frames[state][slot].get_image().get_data()!=image.get_data():
            failures+=1;push_error("Loaded selected source mismatch: "+str(target))
    if shutdown:
        var polish_selection: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-full-polish-v1/selection.json"))
        for direction in ["south","north","east","west"]:
            var key: String="injury-ground-"+direction
            references[key]={};loaded.frames[key]=[]
            loaded.timing[key]=loaded.timing["death-ground-"+direction].duplicate(true)
            for slot in range(6):
                var image:=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+str(polish_selection.stagedFrames[key][slot])))
                var texture:=ImageTexture.create_from_image(image)
                texture.set_meta("crew_standing_height",148);texture.set_meta("crew_pivot",Vector2(92,172))
                loaded.frames[key].append(texture);references[key][slot]=image
    var players: Array=[]
    for direction in ["south","north","east","west"]:
        var player=preload("res://scripts/crew_sprite_player.gd").new()
        player.frames=loaded.frames;player.timing=loaded.timing;players.append(player)
    var view:=Review.new();view.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(view)
    var capture:=0
    var clock:=0.0
    var segments: Array=[{"state":"kneel","samples":20},{"state":"repair","samples":80},{"state":"stand","samples":20},{"state":"interact","samples":24},{"state":"inspect","samples":24}]
    if seated:segments=[{"state":"sit-down","samples":16},{"state":"sit-idle","samples":24},{"state":"read-seated","samples":36},{"state":"sit-rise","samples":16}]
    if rest:segments=[{"state":"lie-down","samples":16},{"state":"sleep","samples":72},{"state":"get-up","samples":16}]
    if water:segments=[{"state":"tread","samples":40},{"state":"swim-start","samples":10},{"state":"swim","samples":32},{"state":"swim-stop","samples":10}]
    if shutdown:segments=[{"state":"death-ground","samples":48},{"state":"injury-ground","samples":48}]
    if recovery:segments=[{"state":"death-water","samples":48},{"state":"swim-distress","samples":48},{"state":"recover-air","samples":72}]
    if galley:segments=[{"state":"eat","samples":40},{"state":"drink","samples":40}]
    for segment in segments:
        for sample in range(segment.samples):
            var elapsed: float=0.0 if sample==0 else sample*.05+.007
            view.textures=[];view.state=segment.state
            for col in range(4):
                var direction: String=["south","north","east","west"][col]
                var player=players[col]
                var texture: Texture2D=player.frame(segment.state,direction,clock+elapsed,Vector2.ZERO)
                var key: String=segment.state+"-"+direction
                var timing: Dictionary=player.timing[key]
                var cursor: float=fposmod(elapsed,timing.seconds) if timing.loop else minf(elapsed,timing.seconds)
                var slot:=0
                for i in range(timing.durations.size()-1):
                    var duration: float=float(timing.durations[i])/1000.0
                    if cursor<duration:break
                    cursor-=duration;slot+=1
                if texture.get_image().get_data()!=references[key][slot].get_data():
                    failures+=1;push_error("Playback mismatch: %s sample %d"%[key,sample])
                view.textures.append(texture)
            view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
            root.get_texture().get_image().save_png(output+"frame-%03d.png"%capture)
            capture+=1
        clock+=segment.samples*.05
    grid.free()
    print("MARSH ACTION NATIVE: %d source matches, %d four-direction captures, %d failures"%[contract.frames.size(),capture,failures])
    quit(1 if failures else 0)

