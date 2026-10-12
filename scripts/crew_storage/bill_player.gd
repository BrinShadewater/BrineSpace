extends "res://scripts/bill_carry_player.gd"
const CpuBatch=preload("res://scripts/crew_storage/worker_batch.gd")
func begin_texture_batch(pool:RefCounted=null)->void:
	if texture_batch==null:
		texture_batch=CpuBatch.new();texture_batch.pool=pool
