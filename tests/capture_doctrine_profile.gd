extends SceneTree

const MainScene := preload("res://scenes/main.tscn")

func _init() -> void:
	call_deferred("_stage_doctrine_profile")

func _stage_doctrine_profile() -> void:
	var game = MainScene.instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	game._on_doctrine_button_pressed("science")
	game._on_doctrine_button_pressed("anomaly")
