# TO-DO
# priority: make it so the gun has a cooldown, add an ammo system (make a randomly spawned ammo box), 
# add a health bar, make enemies take your heal
# 
# backlog: add a weapon texture, add a better gun sound, 

#ursina helps you create 3d games middle one helps you get get random amounts and the last one helps create keys to use to move and line 7 helps you actually imput those keys that you would use to move.
from ursina import *
from random import uniform
from ursina.prefabs.first_person_controller import FirstPersonController

#what does hovered mean in this code
from ursina import *
from random import uniform
from ursina.prefabs.first_person_controller import FirstPersonController

# Gun cooldown settings
cooldown_time = 0.35  # 0.5 seconds
last_shot_time = 0   # Track when the last shot was fired

# Ammo system
max_ammo = 5
current_ammo = max_ammo
needs_reload = False
ammo_text = None  # Will hold the ammo counter UI element

def reload_gun():
    global current_ammo, needs_reload
    current_ammo = max_ammo
    needs_reload = False
    # Play reload sound
    Audio("assets/laser_sound.wav")  # Replace with reload sound when available
    # Update ammo display
    if ammo_text:
        ammo_text.text = f"Ammo: {current_ammo}/{max_ammo}"

def try_shoot():
    global last_shot_time, current_ammo, needs_reload
    current_time = time.time()
    
    # Check if player needs to reload
    if needs_reload:
        # Show reload message
        if ammo_text:
            ammo_text.text = "Press R to reload!"
        return False
    
    # Check if enough time has passed since the last shot and has ammo
    if current_time - last_shot_time >= cooldown_time and current_ammo > 0:
        # Shooting logic
        Audio("assets/laser_sound.wav")
        Animation("assets/spark", parent=camera.ui, fps=5, scale=.1, position=(.19, -.03), loop=False)

        for wasp in wasps:
            if wasp.hovered:
                destroy(wasp)
        for spider in spiders:
            if spider.hovered:
                destroy(spider)
        
        # Update the last shot time and decrease ammo
        last_shot_time = current_time
        current_ammo -= 1
        
        # Check if we're out of ammo
        if current_ammo <= 0:
            needs_reload = True
            
        # Update ammo display
        if ammo_text:
            ammo_text.text = f"Ammo: {current_ammo}/{max_ammo}" if not needs_reload else "Press R to reload!"
            
        return True
    return False

def input(key):
    if key == "left mouse down":
        try_shoot()
    elif key == "r" and needs_reload:
        reload_gun()

# Add this to your update function or create one if it doesn't exist
def update():
    global ammo_text
    
    # Calculate cooldown percentage
    current_time = time.time()
    cooldown_pct = min(1.0, (current_time - last_shot_time) / cooldown_time)
    
    # Update cooldown indicator (you may need to adjust this based on your UI setup)
    cooldown_indicator = Entity(parent=camera.ui, model='quad', scale=(.1, .02), position=(0.7, -0.4))
    cooldown_indicator.scale_x = 0.1 * cooldown_pct
    cooldown_indicator.color = color.green if cooldown_pct >= 1.0 else color.red
    
    # Create ammo text if it doesn't exist
    if ammo_text is None:
        ammo_text = Text(text=f"Ammo: {current_ammo}/{max_ammo}", position=(0.7, -0.45), parent=camera.ui, scale=1.5)

class Wasp(Button):
    def __init__(self, x, y, z):
        super().__init__(
            parent=scene,
            model="assets/wasp.obj",
            scale=.1,
            position=(x,y,z),
            rotation=(0, 90, 0),
            collider="box"
            )

class Spider(Button):
    def __init__(self, x, y, z):
        super().__init__(
            parent=scene,
            model="assets/spider.obj",
            scale=.02,
            position=(x,y,z),
            rotation=(0, 90, 0),
            collider="box"
            )

app=Ursina()

# sky is the world border and line 45-47 is your character and texture
#line 49-55 is the walls that are on the map that you can't go through and their textures collision and color is there too.
#line 57-59 is you weapon which is a golden gun with a scale of 08 and a postion of .3 and -.2 and the rotation is -5, -10, -10
#line 61-76 is the amount of enimies that can spawn and their animations
Sky()
player=FirstPersonController(y=2, origin_y=-.5)
ground=Entity(model='plane', scale=(100, 1, 100), color=color.lime, texture="white_cube",
    texture_scale=(100, 100), collider='box')

wall_1=Entity(model="cube", collider="box", position=(-8, 0, 0), scale=(8, 5, 1), rotation=(0,0,0),
    texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))
wall_2 = duplicate(wall_1, z=5)
wall_3=duplicate(wall_1, z=10)
wall_4=Entity(model="cube", collider="box", position=(-15, 0, 10), scale=(1,5,20), rotation=(0,0,0),
    texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))

gun=Entity(model="assets/gun.obj", parent=camera.ui, scale=.08, color=color.gold, position=(.3, -.2),
    rotation=(-5, -10, -10))

num=6
wasps=[None]*num
spiders=[None]*num
for i in range(num):
    wx=uniform(-12, -7)
    wy=uniform(.1, 1.8)
    wz=uniform(.8, 3.8)
    wasps[i]=Wasp(wx, wy, wz)
    wasps[i].animate_x(wx+.5, duration=.2, loop=True)

    sx=uniform(-12, -7)
    sy=uniform(.1, 1.8)
    sz=uniform(5.8, 8.8)
    spiders[i]=Spider(sx, sy, sz)
    spiders[i].animate_x(sx+.5, duration=.2, loop=True)

app.run()