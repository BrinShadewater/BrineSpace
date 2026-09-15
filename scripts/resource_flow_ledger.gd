extends RefCounted
## Drone and crew deliveries that actually reached storage, bucketed per cycle. The resource bar's
## +/- figure adds their recent average to the room forecast (owner direction, Sept 15), so metal
## climbing from drones no longer reads +0. Game logic keeps using the room forecast alone.
const WINDOW := 3
const SOURCES := ["drone", "crew"]
const MAX_AMOUNT := 100000

static func empty() -> Dictionary:
	return {"open": {"drone": {}, "crew": {}}, "closed": []}

# Records only what storage kept: gains are measured around the delivery, after caps apply.
static func record(ledger: Dictionary, source: String, before: Dictionary, after: Dictionary) -> void:
	if not SOURCES.has(source): return
	var bucket: Dictionary = ledger.open[source]
	for key in after:
		var gained := int(after[key]) - int(before.get(key, 0))
		if gained > 0: bucket[key] = mini(MAX_AMOUNT, int(bucket.get(key, 0)) + gained)

static func close_cycle(ledger: Dictionary) -> void:
	ledger.closed.append(ledger.open)
	while ledger.closed.size() > WINDOW: ledger.closed.pop_front()
	ledger.open = {"drone": {}, "crew": {}}

# Exact delivered totals per source over the closed cycles in the window.
static func totals(ledger: Dictionary) -> Dictionary:
	var result := {"drone": {}, "crew": {}}
	for bucket in ledger.closed:
		for source in SOURCES:
			var amounts: Dictionary = bucket.get(source, {})
			for key in amounts:
				result[source][key] = int(result[source].get(key, 0)) + int(amounts[key])
	return result

# Average delivered per cycle, per resource, rounded for the resource bar.
static func rates(ledger: Dictionary) -> Dictionary:
	var result := {}
	if ledger.closed.is_empty(): return result
	var sums := totals(ledger)
	for source in SOURCES:
		for key in sums[source]:
			result[key] = int(result.get(key, 0)) + int(sums[source][key])
	for key in result.keys():
		result[key] = roundi(float(result[key]) / float(ledger.closed.size()))
		if int(result[key]) == 0: result.erase(key)
	return result

static func _valid_bucket(bucket: Variant) -> bool:
	if not bucket is Dictionary: return false
	for source in bucket:
		if not SOURCES.has(source) or not bucket[source] is Dictionary: return false
		for key in bucket[source]:
			if not key is String or not bucket[source][key] is int or bucket[source][key] < 0 or bucket[source][key] > MAX_AMOUNT: return false
	return true

# Checkpoints before Sept 15 have no ledger; they restore an empty one.
static func valid(value: Variant) -> bool:
	if value == null: return true
	if not value is Dictionary or not value.get("closed") is Array or value.closed.size() > WINDOW: return false
	if not _valid_bucket(value.get("open")): return false
	for bucket in value.closed:
		if not _valid_bucket(bucket): return false
	return true

static func restored(value: Variant) -> Dictionary:
	if value == null or not valid(value): return empty()
	var result: Dictionary = value.duplicate(true)
	for source in SOURCES:
		if not result.open.has(source): result.open[source] = {}
	return result
