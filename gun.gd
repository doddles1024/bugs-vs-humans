extends Node2D

export var cooldown_time = 0.5  # Cooldown in seconds
var can_shoot = true

func _process(delta):
    if Input.is_action_pressed("shoot") and can_shoot:
        shoot()
        start_cooldown()

func shoot():
    # Your shooting logic here
    print("Bang!")
    
    # Example: Spawn bullet, play sound, etc.
    # var bullet = bullet_scene.instance()
    # bullet.global_position = $FirePoint.global_position
    # get_tree().current_scene.add_child(bullet)

func start_cooldown():
    can_shoot = false
    $CooldownTimer.wait_time = cooldown_time
    $CooldownTimer.start()

func _on_CooldownTimer_timeout():
    can_shoot = true
