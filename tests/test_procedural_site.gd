extends SceneTree
const Generator=preload("res://scripts/site_generator.gd")
var failures := 0
func _init() -> void:
	call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures+=1;push_error(message)
func run() -> void:
	var worst := 0
	var attempts := 0
	var fingerprints := {}
	for seed_value in range(1000):
		var site := Generator.generate(seed_value)
		check(Generator.valid(site),"invalid seed %d"%seed_value)
		check(preload("res://scripts/wreck_field.gd").valid(site.wrecks,{}),"invalid obstacles %d"%seed_value)
		check(site.attempt<32 and site.generation_usec<250000,"bounded generation %d"%seed_value)
		worst=maxi(worst,site.generation_usec)
		attempts+=int(site.attempt)
		var duplicate := Generator.generate(seed_value)
		site.erase("generation_usec");duplicate.erase("generation_usec")
		check(site==duplicate,"non-deterministic seed %d"%seed_value)
		fingerprints[str(site.recovery_cells)+str(site.wrecks.keys())]=true
	check(fingerprints.size()==1000,"duplicate geography")
	check(Generator.valid(Generator.candidate(20260923,0)),"invalid fallback")
	print("PROCEDURAL SITE: 1000 seeds, %d unique, retries=%d worst_us=%d failures=%d"%[fingerprints.size(),attempts,worst,failures])
	quit(0 if failures==0 else 1)
