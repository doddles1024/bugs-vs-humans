# TO-DO
# priority: make it so the gun has a cooldown, add an ammo system (make a randomly spawned ammo box), 
# add a health bar, make enemies take your heal
# 
# backlog: add a weapon texture, add a better gun sound, 

#ursina helps you create 3d games middle one helps you get get random amounts and the last one helps create keys to use to move and line 7 helps you actually imput those keys that you would use to move.
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

# Reload system
reload_time = 2.0  # 2 seconds for reload
reload_start_time = 0  # Track when reload started
is_reloading = False  # Track if currently reloading
reload_progress_bar = None  # Will hold the reload progress UI element
cooldown_indicator = None  # Will hold the cooldown indicator UI element

# Ladder climbing
on_ladder = False

def reload_gun():
    global current_ammo, needs_reload, is_reloading, reload_start_time
    
    # Start the reload process
    is_reloading = True
    reload_start_time = time.time()
    
    # Play reload sound
    Audio("assets/laser_sound.wav")  # Replace with reload sound when available
    
    # Update ammo display
    if ammo_text:
        ammo_text.text = "Reloading..."

def try_shoot():
    global last_shot_time, current_ammo, needs_reload
    current_time = time.time()
    
    # Don't allow shooting while reloading
    if is_reloading:
        return False
    
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

        # Raycast for more accurate hit detection
        hit_info = raycast(camera.world_position, camera.forward, distance=100)
        
        if hit_info.hit:
            if hasattr(hit_info.entity, 'is_enemy') and hit_info.entity.is_enemy:
                destroy(hit_info.entity)
        
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

def check_ladder_collision():
    global on_ladder
    
    # Raycast forward to check if player is looking at ladder
    hit_info = raycast(camera.world_position, camera.forward, distance=2)
    
    # Check if player is close to the ladder
    if hit_info.hit and hasattr(hit_info.entity, 'is_ladder') and hit_info.entity.is_ladder:
        # Set a text prompt to show player they can use the ladder
        if not on_ladder:
            Text("Press E to climb", position=(0, -0.2), origin=(0, 0), scale=1.5, color=color.yellow, parent=camera.ui)
        return True
    return False

def input(key):
    global on_ladder
    
    if key == "left mouse down":
        try_shoot()
    elif key == "r" and needs_reload and not is_reloading:
        reload_gun()
    elif key == "e":
        # Check if player is looking at the ladder
        hit_info = raycast(camera.world_position, camera.forward, distance=2)
        if hit_info.hit and hasattr(hit_info.entity, 'is_ladder') and hit_info.entity.is_ladder:
            on_ladder = not on_ladder
            
            # Change player gravity when on ladder
            if on_ladder:
                player.gravity = 0
                player.speed = 3  # Lower speed while climbing
                Text("Climbing mode ON - Use WASD to climb", position=(0, 0.3), origin=(0, 0), scale=1.5, color=color.lime, parent=camera.ui)
            else:
                player.gravity = 1
                player.speed = 5  # Reset to normal speed
                Text("Climbing mode OFF", position=(0, 0.3), origin=(0, 0), scale=1.5, color=color.red, parent=camera.ui)

# Update function for game logic
def update():
    global ammo_text, is_reloading, current_ammo, needs_reload, reload_progress_bar, cooldown_indicator, on_ladder
    
    current_time = time.time()
    
    # Handle ladder climbing
    if on_ladder:
        # Allow vertical movement while on ladder
        if held_keys['w']:
            player.y += time.dt * 3  # Climb up
        if held_keys['s']:
            player.y -= time.dt * 3  # Climb down
            
        # Check if player is still near ladder
        hit_info = raycast(camera.world_position, camera.forward, distance=2)
        if not (hit_info.hit and hasattr(hit_info.entity, 'is_ladder') and hit_info.entity.is_ladder):
            # Player moved away from ladder
            on_ladder = False
            player.gravity = 1
            player.speed = 5  # Reset to normal speed
    
    # Handle reload timer
    if is_reloading:
        # Calculate reload progress (0 to 1)
        reload_progress = min(1.0, (current_time - reload_start_time) / reload_time)
        
        # Update reload progress bar
        if reload_progress_bar is None:
            reload_progress_bar = Entity(parent=camera.ui, model='quad', color=color.red, 
                                       scale=(.2, .02), position=(0.7, -0.35))
        else:
            reload_progress_bar.scale_x = 0.2 * reload_progress
        
        # If reload is complete
        if reload_progress >= 1.0:
            is_reloading = False
            current_ammo = max_ammo
            needs_reload = False
            
            # Update ammo display
            if ammo_text:
                ammo_text.text = f"Ammo: {current_ammo}/{max_ammo}"
            
            # Remove the progress bar
            if reload_progress_bar:
                destroy(reload_progress_bar)
                reload_progress_bar = None
    
    # Calculate cooldown percentage for shooting
    cooldown_pct = min(1.0, (current_time - last_shot_time) / cooldown_time)
    
    # Create or update the cooldown indicator
    if cooldown_indicator:
        destroy(cooldown_indicator)
    
    cooldown_indicator = Entity(parent=camera.ui, model='quad', scale=(.1, .02), 
                              position=(0.7, -0.4), 
                              color=color.green if cooldown_pct >= 1.0 else color.red)
    cooldown_indicator.scale_x = 0.1 * cooldown_pct
    
    # Create ammo text if it doesn't exist
    if ammo_text is None:
        ammo_text = Text(text=f"Ammo: {current_ammo}/{max_ammo}", position=(0.7, -0.45), 
                        parent=camera.ui, scale=1.5)
    
    # Check for ladder interaction
    check_ladder_collision()

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
        self.is_enemy = True
        self.original_x = x
        self.move_distance = 0.5
        self.speed = 0.2
        
    def update(self):
        # Check for wall collision before moving
        hit_info = raycast(
            self.position + Vec3(self.move_distance, 0, 0), 
            self.right, 
            distance=0.2, 
            ignore=(self,)
        )
        
        if hit_info.hit:
            # If about to hit a wall, reverse direction
            self.move_distance *= -1
        
        # Only animate if not clipping
        if not hit_info.hit:
            # Stop any existing animations
            for seq in self.animations:
                seq.pause()
            
            # Create a new animation that respects walls
            self.animate_x(
                self.original_x + self.move_distance, 
                duration=self.speed, 
                curve=curve.linear
            )
            
            # Update original position for next cycle
            self.original_x = self.position.x

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
        self.is_enemy = True
        self.original_x = x
        self.move_distance = 0.5
        self.speed = 0.2
        
    def update(self):
        # Check for wall collision before moving
        hit_info = raycast(
            self.position + Vec3(self.move_distance, 0, 0), 
            self.right, 
            distance=0.2, 
            ignore=(self,)
        )
        
        if hit_info.hit:
            # If about to hit a wall, reverse direction
            self.move_distance *= -1
        
        # Only animate if not clipping
        if not hit_info.hit:
            # Stop any existing animations
            for seq in self.animations:
                seq.pause()
            
            # Create a new animation that respects walls
            self.animate_x(
                self.original_x + self.move_distance, 
                duration=self.speed, 
                curve=curve.linear
            )
            
            # Update original position for next cycle
            self.original_x = self.position.x

class Ladder(Entity):
    def __init__(self, position, height):
        super().__init__(
            parent=scene,
            model="cube",
            texture="brick",
            color=color.brown,
            position=position,
            scale=(0.5, height, 0.5),
            collider="box",
        )
        self.is_ladder = True
        
        # Create ladder rungs
        rung_count = int(height * 2)  # One rung every 0.5 units
        for i in range(rung_count):
            rung = Entity(
                parent=self,
                model="cube",
                color=color.dark_gray,
                position=(0, -height/2 + (i+0.5) * (height/rung_count), 0.3),
                scale=(0.7, 0.1, 0.1)
            )

app = Ursina()

# Add walls
walls = []

# sky is the world border and line 45-47 is your character and texture
#line 49-55 is the walls that are on the map that you can't go through and their textures collision and color is there too.
#line 57-59 is you weapon which is a golden gun with a scale of 08 and a postion of .3 and -.2 and the rotation is -5, -10, -10
#line 61-76 is the amount of enimies that can spawn and their animations
Sky()
player = FirstPersonController(y=2, origin_y=-.5)
ground = Entity(model='plane', scale=(100, 1, 100), color=color.lime, texture="white_cube",
    texture_scale=(100, 100), collider='box')

# Create boundary walls to prevent falling off the map
# North wall
boundary_north = Entity(model="cube", collider="box", position=(0, 0, 50), 
                       scale=(100, 10, 1), color=color.rgba(200, 200, 200, 200), 
                       texture="brick", texture_scale=(30, 3))
walls.append(boundary_north)

# South wall
boundary_south = Entity(model="cube", collider="box", position=(0, 0, -50), 
                       scale=(100, 10, 1), color=color.rgba(200, 200, 200, 200), 
                       texture="brick", texture_scale=(30, 3))
walls.append(boundary_south)

# East wall
boundary_east = Entity(model="cube", collider="box", position=(50, 0, 0), 
                      scale=(1, 10, 100), color=color.rgba(200, 200, 200, 200), 
                      texture="brick", texture_scale=(30, 3))
walls.append(boundary_east)

# West wall
boundary_west = Entity(model="cube", collider="box", position=(-50, 0, 0), 
                      scale=(1, 10, 100), color=color.rgba(200, 200, 200, 200), 
                      texture="brick", texture_scale=(30, 3))
walls.append(boundary_west)

# Original walls from the game
wall_1 = Entity(model="cube", collider="box", position=(-8, 0, 0), scale=(8, 5, 1), rotation=(0,0,0),
    texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))
walls.append(wall_1)

wall_2 = duplicate(wall_1, z=5)
walls.append(wall_2)

wall_3 = duplicate(wall_1, z=10)
walls.append(wall_3)

wall_4 = Entity(model="cube", collider="box", position=(-15, 0, 10), scale=(1,5,20), rotation=(0,0,0),
    texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))
walls.append(wall_4)

# Add a taller wall to climb
tall_wall = Entity(model="cube", collider="box", position=(5, 5, 5), scale=(5, 15, 1), 
                 texture="brick", texture_scale=(3,9), color=color.orange)
walls.append(tall_wall)

# Add a platform on top of the tall wall
platform_top = Entity(model="cube", collider="box", position=(5, 12.5, 7), 
                     scale=(5, 0.5, 5), color=color.gray, texture="white_cube")

# Add a ladder to climb the tall wall
ladder = Ladder(position=(3, 5, 5.6), height=12)

# Add instruction text for the ladder
Text("Find the ladder and press E to climb", position=(0, 0.4), origin=(0, 0), scale=1.5, color=color.yellow, parent=camera.ui)

gun = Entity(model="assets/gun.obj", parent=camera.ui, scale=.08, color=color.gold, position=(.3, -.2),
    rotation=(-5, -10, -10))

num = 6
wasps = [None] * num
spiders = [None] * num

# Helper function to check if a position is inside a wall
def is_position_valid(pos, buffer=0.5):
    for wall in walls:
        # Simple AABB collision check
        wall_min = Vec3(
            wall.position.x - wall.scale_x/2 - buffer,
            wall.position.y - wall.scale_y/2 - buffer,
            wall.position.z - wall.scale_z/2 - buffer
        )
        wall_max = Vec3(
            wall.position.x + wall.scale_x/2 + buffer,
            wall.position.y + wall.scale_y/2 + buffer,
            wall.position.z + wall.scale_z/2 + buffer
        )
        
        # Check if position is inside wall bounds
        if (pos.x >= wall_min.x and pos.x <= wall_max.x and
            pos.y >= wall_min.y and pos.y <= wall_max.y and
            pos.z >= wall_min.z and pos.z <= wall_max.z):
            return False
    return True

# Spawn enemies making sure they don't clip into walls
for i in range(num):
    # Try to find valid positions for wasps
    valid_pos = False
    while not valid_pos:
        wx = uniform(-12, -7)
        wy = uniform(.1, 1.8)
        wz = uniform(.8, 3.8)
        pos = Vec3(wx, wy, wz)
        valid_pos = is_position_valid(pos)
    
    wasps[i] = Wasp(wx, wy, wz)
    
    # Try to find valid positions for spiders
    valid_pos = False
    while not valid_pos:
        sx = uniform(-12, -7)
        sy = uniform(.1, 1.8)
        sz = uniform(5.8, 8.8)
        pos = Vec3(sx, sy, sz)
        valid_pos = is_position_valid(pos)
    
    spiders[i] = Spider(sx, sy, sz)

app.run()           