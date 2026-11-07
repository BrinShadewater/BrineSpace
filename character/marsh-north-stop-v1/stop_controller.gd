extends "res://scripts/marsh_npc.gd"
## Historical fixture adapter; current implementation lives in normal Marsh.
static func valid_north_stop_snapshot(data: Dictionary) -> bool:
	return valid_marsh_snapshot(data)
