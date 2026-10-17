extends SceneTree
## Guard the source head lurch independently of the playback clock.
const Player = preload("res://scripts/crew_sprite_player.gd")
func head_center(image: Image) -> float:
	var visited = {}
	var best_count = 0
	var best_center = NAN
	for y in range(20, 62):
		for x in range(75, 140):
			var pending = [Vector2i(x, y)]
			var count = 0
			var left = 999
			var right = -1
			while not pending.is_empty():
				var point: Vector2i = pending.pop_back()
				if point.x < 75 or point.x >= 140 or point.y < 20 or point.y >= 62 or visited.has(point): continue
				visited[point] = true
				var c = image.get_pixelv(point)
				if not (c.a > 0.63 and c.r > 50.0 / 255.0 and c.r > c.g * 1.12 and c.g > c.b * 1.1): continue
				count += 1
				left = mini(left, point.x)
				right = maxi(right, point.x + 1)
				for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]: pending.append(point + offset)
			if count > best_count:
				best_count = count
				best_center = (left + right) * 0.5
	return best_center

func _init(): call_deferred("run")
func run():
	var path = "res://character/marsh-v2/catalog.json"
	var catalog = JSON.parse_string(FileAccess.get_file_as_string(path))
	var player = Player.new()
	for relative in catalog.body: player.load_manifest(path.get_base_dir().path_join(str(relative)), true)
	var centers = []
	for texture in player.frames["run-east"]: centers.append(head_center(texture.get_image()))
	var failures = 0
	var maximum = 0.0
	for i in centers.size():
		if not is_finite(centers[i]): failures += 1; continue
		maximum = maxf(maximum, absf(centers[i] - centers[(i + 1) % centers.size()]))
	if maximum > 7.0: failures += 1
	if absf(centers[2] - centers[5]) > 1.5: failures += 1
	print("MARSH EAST RUN REGISTRATION: centers=", centers, "; maximum adjacent=", maximum, "; failures=", failures)
	quit(0 if failures == 0 else 1)
