extends SceneTree
const Player=preload("res://tests/playtest_procedural_expedition.gd")
class State extends RefCounted:
	var recovered_crew: Array=[]
	var architect_run: Dictionary={"selected":"bill"}
func _init():
	var player=Player.new(false)
	var state=State.new()
	player.game=state
	var failures:=0
	for starter in ["bill","veld","branforth","marsh"]:
		state.architect_run.selected=starter
		state.recovered_crew=[{"architect_id":starter}]
		if player.has_recovered_guest(): failures+=1;push_error("Starter alone is not a guest recovery")
		for guest in ["bill","veld","branforth","marsh"]:
			if guest==starter: continue
			state.recovered_crew=[{"architect_id":starter},{"architect_id":guest}]
			if not player.has_recovered_guest(): failures+=1;push_error("Every guest identity advances test-player strategy")
	player.free()
	print("PROCEDURAL PLAYER PROGRESS: failures=",failures)
	quit(0 if failures==0 else 1)
