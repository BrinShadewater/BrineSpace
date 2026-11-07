extends SceneTree
const Stop=preload("res://character/marsh-south-stop-v1/stop_controller.gd")
const Normal=preload("res://scripts/marsh_npc.gd")
class Probe extends Stop:
	var arrivals:=0
	var rebuilds:=0
	var clear:=true
	func can_stand(_p: Vector2) -> bool:return clear
	func segment_clear(_a: Vector2,_b: Vector2) -> bool:return clear
	func crew_clear(_a: Vector2,_b: Vector2) -> bool:return clear
	func rebuild(_main,_staged:=false) -> void:rebuilds+=1
	func finish_south_stop_arrival() -> void:arrivals+=1;state="idle";timer=6
class Gate:
	var paused:=true
	var running:=true
	func get_visual_time_seconds() -> float:return 5.0
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func actor_start():
	var a=Probe.new();a.active=true;a.battery=100;a.foot=Vector2(100,200);a.state="idle";a.direction="south";a.goal="curiosity";a.timer=10
	a.path=PackedVector2Array([Vector2(100,280)]);a.begin_south_start();return a
func actor_stop(player,phase: int):
	var a=Probe.new();a.active=true;a.battery=100;a.state="walk";a.direction="south";a.goal="curiosity"
	a.foot=Vector2(100,200);a.path=PackedVector2Array([Vector2(100,212)]);a.bind_south_stop_player(player);a.south_stop_time=1
	player.current_key="walk-south";player.current_equipment="";player.phase=fposmod(phase*.15+.04-12/(.128*384)*.9,.9)
	player.last_position=a.south_stop_position_cells();player.last_time=0;player.started=0;player.motion={"state":"walk","direction":"south","clip":"","started":0.0}
	a.move(12/46.0);return a
func copy_player(player):
	var p=preload("res://scripts/crew_sprite_player.gd").new()
	p.frames=player.frames;p.timing=player.timing;p.strides=player.strides;p.gait_phase_groups=player.gait_phase_groups
	return p
func run():
	var grid=load("res://scripts/grid_canvas.gd").new();grid._load_replacement_crew_animations();var player=grid.marsh_player
	for manifest in ["res://character/marsh-south-walk-material-v1/candidate-02/manifest.json","res://character/marsh-south-idle-material-v1/candidate-01/manifest.json","res://character/marsh-south-idle-material-v1/candidate-01/south-start/manifest.json","res://character/marsh-south-stop-v1/candidate-06/phase-0/manifest.json","res://character/marsh-south-stop-v1/candidate-06/phase-1/manifest.json","res://character/marsh-south-stop-v1/candidate-06/phase-2/manifest.json","res://character/marsh-south-stop-v1/candidate-01/phase-3/manifest.json","res://character/marsh-south-stop-v1/candidate-07/phase-4/manifest.json","res://character/marsh-south-stop-v1/candidate-01/phase-5/manifest.json"]:player.load_manifest(manifest,true)
	var main=Gate.new()
	for clock in [.0,.18,.26,.31,.36,.4,.7]:
		var actor=actor_start();actor.move(clock);var saved: Dictionary=actor.snapshot()
		check(Stop.valid_south_snapshot(saved),"active/pending South start snapshot matches actual curve")
		check(Normal.valid_marsh_snapshot(saved),"normal actor owns validated South start restoration")
		var restored=Probe.new();await restored.restore_snapshot(main,saved)
		check(restored.rebuilds==1 and restored.snapshot()==saved,"South start restores through base actor fields and exact authored namespace")
		var before: Dictionary=restored.snapshot();restored.update(main,.5);restored.move(0)
		check(restored.snapshot()==before,"restored paused/zero start retains curve and handoff")
		var p=copy_player(player)
		if restored.south_pending:
			restored.prepare_south_gait(p,5,restored.south_stop_position_cells())
			check(p.current_key=="walk-south" and is_equal_approx(p.phase,.68+restored.foot.distance_to(restored.south_gait_origin)/(.128*384)*.9),"restored pending gait owns distance seed once")
		else:
			actor.move(.4-clock);restored.move(.4-clock)
			check(restored.snapshot()==actor.snapshot(),"restored start continuation matches uninterrupted actor")
	for phase in range(6):
		for clock in [.04,.18,.28,.36]:
			var actor=actor_stop(player,phase);actor.advance_south_stop(clock)
			var saved: Dictionary=actor.snapshot();var playback: Dictionary=player.snapshot()
			check(actor.south_stop_phase==phase and Stop.valid_south_snapshot(saved),"selected finite South stop snapshot valid")
			check(Normal.valid_marsh_snapshot(saved),"normal Continue accepts supported active stop")
			var restored=Probe.new();var p=copy_player(player);restored.bind_south_stop_player(p);await restored.restore_snapshot(main,saved);p.restore_snapshot(playback)
			check(restored.snapshot()==saved and p.snapshot()==playback and restored.arrivals==0,"actor and outgoing player restore without callback")
			check(p.frame_at_elapsed(restored.animation_state()+"-south",restored.action_elapsed()).get_image().get_data()==player.frame_at_elapsed(actor.animation_state()+"-south",actor.action_elapsed()).get_image().get_data(),"restored stop source RGBA equals uninterrupted pose")
			var before: Dictionary=restored.snapshot();restored.update(main,.5);restored.move(0)
			check(restored.snapshot()==before,"restored stop pause/zero retains phase and root")
			restored.advance_south_stop(.4-clock)
			check(restored.arrivals==1 and restored.foot==saved.foot and not restored.south_stop_active() and Stop.valid_south_snapshot(restored.snapshot()),"restored stop completes one callback at fixed actual anchor")
			restored.advance_south_stop(1);check(restored.arrivals==1,"restored completed stop cannot replay callback")
			actor.goal="";actor.choose_goal(null);saved=actor.snapshot()
			check(Stop.valid_south_snapshot(saved) and saved.south_stop.cancelled and saved.south_stop.goal.is_empty(),"cancelled service identity serializes without old work")
			restored=Probe.new();await restored.restore_snapshot(main,saved);restored.advance_south_stop(.4-clock)
			check(restored.arrivals==0 and restored.timer==0 and Stop.valid_south_snapshot(restored.snapshot()),"restored cancellation finishes without stale arrival callback")
		var actor=actor_stop(player,phase);actor.advance_south_stop(.7)
		var saved: Dictionary=actor.snapshot();check(saved.south_stop.idle_pending and is_equal_approx(saved.south_stop.idle_elapsed,.3),"completion snapshot preserves large-delta idle residue")
		var restored=Probe.new();var p=copy_player(player);await restored.restore_snapshot(main,saved)
		restored.prepare_stop_pose(p,5,restored.south_stop_position_cells())
		check(is_equal_approx(p.phase,.3) and p.frame("idle","south",5,restored.south_stop_position_cells())==p.frames["idle-south"][0],"restored completion seeds idle phase at consumed remainder")
		check(p.frame("idle","south",5.351,restored.south_stop_position_cells())==p.frames["idle-south"][1] and restored.arrivals==0,"restored idle advances650ms cycle without repeating finished callback")
		var drawn: Dictionary=restored.snapshot();var playback: Dictionary=p.snapshot();var again=Probe.new();var q=copy_player(player)
		await again.restore_snapshot(main,drawn);q.restore_snapshot(playback)
		check(not drawn.south_stop.idle_pending and q.snapshot()==playback and again.snapshot()==drawn,"consumed idle seed restores through ordinary player playback")
	var start: Dictionary=actor_start().snapshot();var stop: Dictionary=actor_stop(player,3).snapshot()
	for pair in [[start,"south_start"],[stop,"south_stop"]]:
		var good: Dictionary=pair[0];var key: String=pair[1]
		for field in good[key]:
			for value in [null,"bad",NAN,INF]:
				var bad: Dictionary=good.duplicate(true);bad[key][field]=value
				check(not Stop.valid_south_snapshot(bad) and not Normal.valid_marsh_snapshot(bad),"malformed South field rejected before restore: "+key+"/"+field)
			var missing: Dictionary=good.duplicate(true);missing[key].erase(field)
			check(not Stop.valid_south_snapshot(missing),"partial South namespace cannot fabricate defaults")
		for clock in [-2.0,.4,.7]:
			var bad: Dictionary=good.duplicate(true);bad[key].clock=clock
			check(not Stop.valid_south_snapshot(bad),"out-of-range finite South clock rejected")
		var bad: Dictionary=good.duplicate(true);bad[key]="bad";var sentinel=Probe.new();sentinel.foot=Vector2(9,11)
		await sentinel.restore_snapshot(main,bad)
		check(sentinel.foot==Vector2(9,11) and sentinel.rebuilds==0,"malformed input causes no navigation rebuild or actor mutation")
	for change in [{"active":false},{"dead":true},{"helmet_equipped":true},{"direction":"west"},{"stage":"inspect"},{"goal":"hunger"},{"movement_medium":"water"},{"battery":35.0},{"returning_to_pod":true},{"recharge_docked":true},{"run_motion":true},{"foot":Vector2(101,212)}]:
		var bad: Dictionary=stop.duplicate(true)
		for field in change:bad[field]=change[field]
		check(not Stop.valid_south_snapshot(bad),"ineligible stop context rejected: "+str(change))
	for phase in [-1,6,1.5]:
		var bad: Dictionary=stop.duplicate(true);bad.south_stop.phase=phase;check(not Stop.valid_south_snapshot(bad),"invalid or fractional outgoing phase rejected")
	var bad: Dictionary=stop.duplicate(true);bad.south_stop.cancelled=true;check(not Stop.valid_south_snapshot(bad),"cancelled stop cannot retain work goal")
	bad=stop.duplicate(true);bad.south_stop.idle_pending=true;check(not Stop.valid_south_snapshot(bad),"active stop cannot simultaneously seed completed idle")
	bad=start.duplicate(true);bad.south_start.pending=true;check(not Stop.valid_south_snapshot(bad),"active start cannot also be pending")
	bad=start.duplicate(true);bad.south_start.gait_origin+=Vector2(0,1);check(not Stop.valid_south_snapshot(bad),"gait origin must match source advance")
	bad=start.duplicate(true);bad.path.append(Vector2(100,400));check(not Stop.valid_south_snapshot(bad),"serialized route extending into run rejects ordinary start")
	for collision in [{"cardinal_north":{"clock":.1}},{"cardinal_north":{"pending":true}},{"north_stop":{"clock":.1}},{"north_short":{"elapsed":.1}},{"west_ground":{"phase":"start"}},{"west_short":{"elapsed":.1}},{"ground_start":{"pose":0}},{"ground_stop":{"elapsed":.1}},{"short_step":{"elapsed":.1}}]:
		var conflict: Dictionary=stop.duplicate(true)
		for key in collision:conflict[key]=collision[key]
		check(not Normal.valid_marsh_snapshot(conflict),"South stop cannot revive another authored controller: "+str(collision))
	var extended=actor_start();extended.path.append(Vector2(100,400));check(not extended.south_active() and Stop.valid_south_snapshot(extended.snapshot()),"actual run-extension invalidates held start into canonical inactive fields")
	for clear in [false,true]:
		var restored=Probe.new();restored.clear=clear;await restored.restore_snapshot(main,stop)
		check(restored.south_stop_active()==clear,"restored stop revalidates present floor/peer eligibility")
		check(Stop.valid_south_snapshot(restored.snapshot()),"topology-invalidated restored stop serializes canonical state")
	var legacy: Dictionary=Normal.new().snapshot();check(Normal.valid_marsh_snapshot(legacy) and Stop.valid_south_snapshot(legacy),"legacy checkpoint without South namespaces remains accepted")
	var restored=Probe.new();await restored.restore_snapshot(main,legacy);check(restored.south_clock==-1 and restored.south_stop_clock==-1 and not restored.south_pending,"legacy restoration clears candidate-only state")
	var crew={"version":1,"bill":preload("res://scripts/major_bill_npc.gd").new().snapshot(),"veld":preload("res://scripts/veld_npc.gd").new().snapshot(),"marsh":legacy}
	check(preload("res://scripts/run_save.gd").valid_crew(crew),"actual RunSave gate accepts legacy normal crew")
	crew.marsh=stop;check(preload("res://scripts/run_save.gd").valid_crew(crew),"actual RunSave gate accepts supported South motion")
	crew.marsh=bad;check(not preload("res://scripts/run_save.gd").valid_crew(crew),"actual RunSave gate rejects malformed South extension")
	grid.free();print("MARSH SOUTH SNAPSHOTS: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
