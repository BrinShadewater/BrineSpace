extends RefCounted
## Opening stages use saved core wake time, never an independent wall clock.
const POD_START := 3.0
const SCREENS_START := 2.0

static func active(core: Dictionary) -> bool:
	return not core.is_empty() and not core.get("recovered",false)

static func elapsed(core: Dictionary) -> float:
	return float(core.get("wake",0.0)) if active(core) else 10.0

static func lights(core: Dictionary, reduced_motion := false) -> float:
	var seconds := elapsed(core)
	if reduced_motion: return clampf((seconds-0.8)/0.8,0.0,1.0)
	if seconds<0.8: return 0.0
	if seconds<1.0: return 0.3
	if seconds<1.15: return 0.08
	if seconds<1.3: return 0.6
	if seconds<1.6: return 0.15
	return 1.0

static func pod_power(core: Dictionary) -> float:
	return clampf((elapsed(core)-POD_START)/0.3,0.0,1.0)

static func screens(core: Dictionary) -> bool:
	return elapsed(core)>=SCREENS_START
