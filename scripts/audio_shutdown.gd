extends RefCounted
## Normal quits drain playback before closing the engine; save decisions stay with callers.
static func request(owner: Node) -> void:
	var tree := owner.get_tree()
	if tree.root.get_meta("audio_quitting",false): return
	tree.root.set_meta("audio_quitting",true)
	for child in tree.root.get_children():
		child.process_mode = Node.PROCESS_MODE_DISABLED
		stop_audio(child)
	await tree.create_timer(0.2,true,false,true).timeout
	tree.quit()

static func stop_audio(node: Node) -> void:
	if node is AudioStreamPlayer or node is AudioStreamPlayer2D or node is AudioStreamPlayer3D:
		node.stop()
		node.stream = null
	for child in node.get_children(): stop_audio(child)
