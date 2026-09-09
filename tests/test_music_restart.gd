extends SceneTree
const Music=preload("res://scripts/station_music.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	for i in range(3):
		var music:=Music.new(); root.add_child(music)
		assert(music.playlist.size()==4 and music.player.stream!=null,"Recreated music retains four tracks")
		music.next_track(); music._on_finished(music.player)
		assert(music.rest_remaining>0,"Every second track retains its intentional quiet interval")
		music._process(31.0)
		assert(music.rest_remaining==0 and music.player.stream!=null)
		music.queue_free(); await process_frame; await create_timer(0.15).timeout
	print("MUSIC RESTART PASS: three lifecycles, owned playlist, quiet intervals and resumed tracks")
	quit()
