extends RefCounted
## Shared declarations let the title's loading UI prepare these small resources
## before background Main parsing, avoiding nested background resource loads.
const DERELICT = preload("res://scripts/derelict_material.gdshader")
const FOG = preload("res://scripts/underwater_fog.gdshader")
