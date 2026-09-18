extends SceneTree
const Music=preload("res://scripts/station_music.gd")
const Bank=preload("res://scripts/suno_audio_bank.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	for i in range(3):
		var music:=Music.new(); root.add_child(music)
		var expected: int = Bank.CLIPS.moonlit_canyon.size() + Bank.CLIPS.moonlit_test_run.size() + Bank.CLIPS.tracks_v1.size()
		assert(music.playlist.size()==expected and music.player.stream!=null,"Recreated music retains the whole rotation")
		music.next_track(); music._on_finished(music.player)
		assert(music.rest_remaining>0,"Every second track retains its intentional quiet interval")
		music._process(31.0)
		assert(music.rest_remaining==0 and music.player.stream!=null)
		music.queue_free(); await process_frame; await create_timer(0.15).timeout
	print("MUSIC RESTART PASS: three lifecycles, owned playlist, quiet intervals and resumed tracks")
	quit()
