extends "object_growth.gd"
## Read-only attribution: count stale WeakRefs without retaining their targets.
const CrewRouter = preload("res://scripts/crew_storage/router.gd")
func configure() -> bool:
	if not super.configure(): return false
	evidence["router_audit"] = "Counts live/dead registry references and existing fixed-size presenter diagnostics; no pruning, reset or gameplay mutation."
	return true
func append_periodic(label: String) -> void:
	super.append_periodic(label)
	if periodic.size() % 6 == 0 and not periodic.is_empty():
		var row: Dictionary = periodic.back().census
		print("ROUTER_MEMORY objects=", row.objects, " nodes=", row.nodes,
			" entries=", row.crew_router.canvas_entries, " expired=", row.crew_router.expired_canvas_refs)
func census(label: String, game = null) -> Dictionary:
	var row := super.census(label, game)
	var router = CrewRouter.active
	if router == null:
		row["crew_router"] = {"active": false}
		return row
	var expired := 0
	var classes: Dictionary = {}
	for reference in router.canvas.values():
		var target = reference.get_ref()
		if target == null: expired += 1
		else:
			var kind: String = target.get_class()
			classes[kind] = int(classes.get(kind, 0)) + 1
	var tracked_expired := 0
	for record in router.tracked_owners.values():
		if record.owner.get_ref() == null: tracked_expired += 1
	row["crew_router"] = {"active": true, "canvas_entries": router.canvas.size(), "expired_canvas_refs": expired,
		"live_canvas_classes": classes, "tracked_owners": router.tracked_owners.size(), "expired_tracked_owners": tracked_expired,
		"epochs": router.epochs.size(), "diagnostics": router.diagnostics_snapshot()}
	return row
