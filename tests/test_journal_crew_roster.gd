extends SceneTree
# The Journal's crew row shows the portrait of the crew member it names. The architect who
# wakes in BRINE's core is whoever was selected for the loop, not always Bill.
const Journal := preload("res://scripts/journal_widgets.gd")
const Architects := preload("res://scripts/architects.gd")
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
func _init() -> void: call_deferred("run")
func portrait_of(card: Control) -> TextureRect:
	return card.get_child(0).get_node("Portrait")
func run() -> void:
	for id in Architects.IDS:
		var member := {"id": "core_architect", "architect_id": id, "name": str(Architects.NAMES[id]), "origin": Architects.CORE_CELL, "alive": true}
		var card: Control = Journal._member_row(null, member)
		var picture := portrait_of(card)
		if Architects.SELECTION_PORTRAITS.has(id):
			check(picture.visible and picture.texture == Architects.selection_portrait(id), "%s in the core shows their own portrait" % id)
		else:
			check(not picture.visible, "%s has no portrait, so none is shown" % id)
		if id != "bill" and Architects.SELECTION_PORTRAITS.has("bill"):
			check(picture.texture != Architects.selection_portrait("bill") or not picture.visible, "%s in the core does not borrow Bill's portrait" % id)
		card.free()
	# A checkpoint from before crew rows recorded who woke in the core means Bill.
	var old: Control = Journal._member_row(null, {"id": "core_architect", "name": "Major Bill", "origin": Architects.CORE_CELL, "alive": true})
	check(portrait_of(old).texture == Architects.selection_portrait("bill"), "An old core record without an architect id is Bill")
	old.free()
	var ward: Control = Journal._member_row(null, {"id": "pod_1", "architect_id": "veld", "name": str(Architects.NAMES["veld"]), "origin": Vector2i(16, 21), "alive": false})
	check(portrait_of(ward).texture == Architects.selection_portrait("veld"), "A ward recovery shows that crew member")
	ward.free()
	# Survivors who arrive with a Crew Hab are listed by name: fixed for a loop, no repeats.
	var names := {}
	for index in range(Journal.SURVIVOR_NAMES.size()): names[Journal.survivor_name(479821352, index)] = true
	check(names.size() == Journal.SURVIVOR_NAMES.size(), "Sixteen survivors in one loop get sixteen different names, not %d" % names.size())
	var firsts := {}
	for seed in range(40): firsts[Journal.survivor_name(seed, 0)] = true
	check(firsts.size() > 4, "Different loops start with different survivors: %d names over 40 loops" % firsts.size())
	check(Journal.survivor_name("legacy", 20) != Journal.survivor_name("legacy", 4), "A seventeenth survivor and beyond is still told apart")
	var survivor: Control = Journal._survivor_row("Petra Lindqvist")
	check(not portrait_of(survivor).visible and survivor.find_children("*", "Label", true, false).any(func(label): return label.text == "Petra Lindqvist"), "A survivor row shows the name and no portrait")
	survivor.free()
	print("JOURNAL CREW ROSTER: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
