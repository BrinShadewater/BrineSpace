extends "res://tests/playtest_anomaly_room.gd"
## Diagnostic comparison only: removes crew rendering from this isolated fixture.
## A passing result is not normal crew/room occlusion or full-scene acceptance.
func capture(name: String) -> void:
	for npc in [game.bill_npc,game.veld_npc,game.branforth_npc]: npc.active=false
	await super.capture(name)
