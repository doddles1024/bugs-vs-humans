# TO-DO
# priority: make it so the gun has a cooldown, add an ammo system (make a randomly spawned ammo box), 
# add a health bar, make enemies take your heal
# 
# backlog: add a weapon texture, add a better gun sound, 

#ursina helps you create 3d games middle one helps you get get random amounts and the last one helps create keys to use to move and line 7 helps you actually imput those keys that you would use to move.
from ursina import *
from random import uniform
import os  # For restart game functionality
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

# Health system
max_health = 100
current_health = max_health
health_bar = None
health_text = None
last_damage_time = 0
damage_cooldown = 0.5  # Time in seconds between taking damage from the same enemy
is_invulnerable = False  # Flag to prevent damage during invulnerability period
invulnerability_time = 1.0  # Seconds of invulnerability after taking damage

# Sprint system
normal_speed = 5
sprint_speed = 10
sprint_active = False
stamina = 100  # Maximum stamina
current_stamina = stamina
stamina_regen_rate = 10  # Stamina regained per second when not sprinting
stamina_drain_rate = 20  # Stamina drained per second when sprinting
stamina_bar = None  # Will hold the stamina bar UI element

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

def toggle_sprint(active):
    global sprint_active
    sprint_active = active
    
    # Apply the appropriate speed
    if sprint_active and current_stamina > 0:
        player.speed = sprint_speed
    else:
        player.speed = normal_speed
        
def create_health_bar():
    global health_bar, health_text
    
    # Health bar background (black border)
    health_bar_background = Entity(
        parent=camera.ui,
        model="quad",
        scale=(0.25, 0.04),
        position=(0.7, -0.45),
        color=color.black
    )
    
    # Health bar (green)
    health_bar = Entity(
        parent=camera.ui,
        model="quad",
        scale=(0.24, 0.03),
        position=(0.7, -0.45),
        color=color.green
    )
    
    # Health text
    health_text = Text(
        parent=camera.ui,
        text=f"{current_health}",
        position=(0.7, -0.45),
        origin=(0, 0),
        color=color.black,
        scale=1.5
    )

def take_damage(amount):
    global current_health, is_invulnerable, last_damage_time
    
    # Don't take damage during invulnerability period
    if is_invulnerable:
        return
    
    # Apply damage
    current_health = max(0, current_health - amount)
    
    # Update health bar
    if health_bar:
        health_bar.scale_x = 0.24 * (current_health / max_health)
    
    # Update health text
    if health_text:
        health_text.text = f"{current_health}"
    
    # Play damage sound
    Audio("assets/laser_sound.wav")  # Replace with damage sound when available
    
    # Make player temporarily invulnerable
    is_invulnerable = True
    last_damage_time = time.time()
    
    # Game over check
    if current_health <= 0:
        game_over()

def game_over():
    # Create game over text
    Text(
        text="GAME OVER",
        origin=(0, 0),
        scale=5,
        color=color.red,
        position=(0, 0.2)
    )
    
    # Create restart button
    restart_button = Button(
        text="Restart Game",
        scale=(0.4, 0.1),
        position=(0, -0.1),
        color=color.red.tint(-0.2),
        highlight_color=color.red
    )
    
    # Define restart function
    def restart():
        application.quit()
        os.startfile(__file__)  # This will restart the game on Windows
        
    restart_button.on_click = restart

def input(key):
    if key == "left mouse down":
        try_shoot()
    elif key == "r" and needs_reload and not is_reloading:
        reload_gun()
    elif key == "left shift":
        toggle_sprint(True)
    elif key == "left shift up":
        toggle_sprint(False)

# Update function for game logic
def update():
    # Update function for game logic
    global ammo_text, is_reloading, current_ammo, needs_reload, reload_progress_bar, cooldown_indicator
    global sprint_active, current_stamina, stamina_bar
    global is_invulnerable, last_damage_time  # Added is_invulnerable to global declaration
    
    current_time = time.time()
    # Handle invulnerability timer
    
    if is_invulnerable and current_time - last_damage_time >= invulnerability_time:
        is_invulnerable = False
    
    # Check for enemy collisions and apply damage
    for enemy in [*wasps, *spiders]:
        if enemy and enemy.enabled:
            distance_to_player = (player.position - enemy.position).length()
            if distance_to_player < 0.8:  # Close enough to damage player
                take_damage(5)  # Take 5 damage points per hit
    # Handle sprint and stamina
    if sprint_active and current_stamina > 0:
        # Drain stamina while sprinting
        current_stamina = max(0, current_stamina - stamina_drain_rate * time.dt)
        player.speed = sprint_speed
        
        # If stamina is depleted, disable sprint
        if current_stamina <= 0:
            player.speed = normal_speed
    else:
        # Regenerate stamina when not sprinting
        current_stamina = min(stamina, current_stamina + stamina_regen_rate * time.dt)
        player.speed = normal_speed
    
    # Update stamina bar
    if stamina_bar is None:
        stamina_bar = Entity(parent=camera.ui, model='quad', color=color.blue, 
                           scale=(.2, .02), position=(0.7, -0.3))
    stamina_bar.scale_x = 0.2 * (current_stamina / stamina)
    
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
    
    # Create sprint text if it doesn't exist
    if not hasattr(camera.ui, 'sprint_text'):
        camera.ui.sprint_text = Text(text="Sprint: Left Shift", position=(0.7, -0.25), 
                            parent=camera.ui, scale=1.5)

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
        self.original_position = Vec3(x, y, z)  # Store original position for patrolling
        self.move_distance = 0.5
        self.patrol_speed = 0.2
        self.follow_speed = 4  # Faster when following player
        self.detection_range = 30  # How far the wasp can detect the player
        self.following_player = False
        
    def update(self):
        # Calculate distance to player
        distance_to_player = (player.position - self.position).length()
        
        # Check if player is within detection range
        if distance_to_player <= self.detection_range:
            self.following_player = True
        else:
            self.following_player = False
        
        if self.following_player:
            # Follow player behavior
            self.follow_player()
        else:
            # Normal patrol behavior
            self.patrol()
    
    def follow_player(self):
        # Get direction to player
        direction = (player.position - self.position).normalized()
        
        # Calculate next position
        next_position = self.position + direction * self.follow_speed * time.dt
        
        # Check for wall collision before moving
        hit_info = raycast(
            self.position, 
            direction, 
            distance=0.3, 
            ignore=(self,)
        )
        
        if not hit_info.hit:
            # Safe to move toward player
            self.position = next_position
            
            # Look at player (only y-rotation/yaw)
            self.look_at_2d(player.position)
        
        # Check if close enough to attack - damage is handled in main update function
        # This is just for visual/sound effects when attacking
        distance_to_player = (player.position - self.position).length()
        if distance_to_player < 0.8:
            if not hasattr(self, 'last_attack_time') or time.time() - self.last_attack_time > 1.0:
                self.last_attack_time = time.time()
                # Play attack animation or sound here if you have one
                self.animate_scale(self.scale * 1.2, duration=0.1, curve=curve.out_bounce)
                self.animate_scale(self.scale, duration=0.1, delay=0.1)
    
    def patrol(self):
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
                duration=self.patrol_speed, 
                curve=curve.linear
            )
            
            # Update original position for next cycle
            self.original_x = self.position.x
    
    def look_at_2d(self, target_pos):
        """Make entity look at target but only rotate on y-axis"""
        direction = target_pos - self.position
        # Only care about horizontal direction (y is up in Ursina)
        self.rotation_y = math.degrees(math.atan2(direction.x, direction.z))

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
        self.original_position = Vec3(x, y, z)  # Store original position for patrolling
        self.move_distance = 0.5
        self.patrol_speed = 0.2
        self.follow_speed = 1
        self.detection_range = 60  # Shorter detection range than wasps
        self.following_player = False
        
    def update(self):
        # Calculate distance to player
        distance_to_player = (player.position - self.position).length()
        
        # Check if player is within detection range
        if distance_to_player <= self.detection_range:
            self.following_player = True
        else:
            self.following_player = False
        
        if self.following_player:
            # Follow player behavior
            self.follow_player()
        else:
            # Normal patrol behavior
            self.patrol()
    
    def follow_player(self):
        # Get direction to player - spiders stay on the ground
        player_ground_pos = Vec3(player.position.x, self.y, player.position.z)
        direction = (player_ground_pos - self.position).normalized()
        
        # Calculate next position
        next_position = self.position + direction * self.follow_speed * time.dt
        
        # Check for wall collision before moving
        hit_info = raycast(
            self.position, 
            direction, 
            distance=0.3, 
            ignore=(self,)
        )
        
        if not hit_info.hit:
            # Safe to move toward player
            self.position = next_position
            
            # Look at player (only y-rotation/yaw)
            self.look_at_2d(player_ground_pos)
    
    def patrol(self):
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
                duration=self.patrol_speed, 
                curve=curve.linear
            )
            
            # Update original position for next cycle
            self.original_x = self.position.x
    
    def look_at_2d(self, target_pos):
        """Make entity look at target but only rotate on y-axis"""
        direction = target_pos - self.position
        # Only care about horizontal direction (y is up in Ursina)
        self.rotation_y = math.degrees(math.atan2(direction.x, direction.z))

app = Ursina()
create_health_bar()
# Add walls
walls = []

# sky is the world border and line 45-47 is your character and texture
#line 49-55 is the walls that are on the map that you can't go through and their textures collision and color is there too.
#line 57-59 is you weapon which is a golden gun with a scale of 08 and a postion of .3 and -.2 and the rotation is -5, -10, -10
#line 61-76 is the amount of enimies that can spawn and their animations
Sky()
player = FirstPersonController(y=2, origin_y=-.5)
player.speed = normal_speed  # Set initial speed to normal
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

gun = Entity(model="assets/gun.obj", parent=camera.ui, scale=.08, color=color.gold, position=(.3, -.2),
    rotation=(-5, -10, -10))

# Add sprint instructions on screen
Text("Hold Left Shift to Sprint", position=(0, 0.4), origin=(0, 0), scale=1.5, color=color.yellow, parent=camera.ui)

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