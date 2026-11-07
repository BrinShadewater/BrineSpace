extends Sprite2D

@export var min_alpha: float = 0.5
@export var max_alpha: float = 1.0
@export var pulse_speed: float = 2.0

func _process(_delta: float) -> void:
    var t := sin(Time.get_ticks_msec() / 1000.0 * pulse_speed) * 0.5 + 0.5
    modulate.a = lerp(min_alpha, max_alpha, t)
