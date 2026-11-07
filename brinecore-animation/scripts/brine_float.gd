extends AnimatedSprite2D

@export var bob_amount: float = 3.0
@export var bob_speed: float = 1.2

var start_position: Vector2

func _ready() -> void:
    start_position = position
    if sprite_frames and sprite_frames.has_animation("idle"):
        play("idle")

func _process(_delta: float) -> void:
    var bob := sin(Time.get_ticks_msec() / 1000.0 * bob_speed) * bob_amount
    position = start_position + Vector2(0, bob)
