import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FPS Gun Demo")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)  # Lighter background

class Gun:
    def __init__(self):
        self.cooldown_time = 500  # 0.5 seconds in milliseconds
        self.last_shot_time = 0
        self.ammo = 30
        self.is_reloading = False
        self.reload_start_time = 0
        self.reload_duration = 2000  # 2 seconds to reload
        
    def try_shoot(self):
        current_time = pygame.time.get_ticks()
        
        # Check if reloading
        if self.is_reloading:
            if current_time - self.reload_start_time >= self.reload_duration:
                self.is_reloading = False
                self.ammo = 30
            return False
            
        # Check if can shoot (cooldown passed and has ammo)
        if current_time - self.last_shot_time >= self.cooldown_time and self.ammo > 0:
            self.shoot()
            self.last_shot_time = current_time
            self.ammo -= 1
            return True
        return False
            
    def shoot(self):
        # Your shooting logic here
        print("Bang!")
        # In a real game, you'd create a bullet sprite here
        
    def reload(self):
        if not self.is_reloading and self.ammo < 30:
            self.is_reloading = True
            self.reload_start_time = pygame.time.get_ticks()
            print("Reloading...")

# Create gun instance
gun = Gun()

# Font for UI
try:
    font = pygame.font.SysFont(None, 36)
except:
    print("Font initialization failed, trying default font")
    font = pygame.font.Font(None, 36)

# Debug text function
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Main game loop
clock = pygame.time.Clock()
running = True
frame_count = 0

while running:
    current_time = pygame.time.get_ticks()
    frame_count += 1
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                gun.reload()
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    # Check for mouse clicks to shoot
    if pygame.mouse.get_pressed()[0]:  # Left mouse button
        gun.try_shoot()
    
    # Clear screen with a GRAY background instead of BLACK
    screen.fill(GRAY)
    
    # Draw a visible border around the screen
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, HEIGHT), 5)
    
    # Draw crosshair
    pygame.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), 10, 3)
    pygame.draw.line(screen, RED, (WIDTH // 2 - 15, HEIGHT // 2), (WIDTH // 2 + 15, HEIGHT // 2), 3)
    pygame.draw.line(screen, RED, (WIDTH // 2, HEIGHT // 2 - 15), (WIDTH // 2, HEIGHT // 2 + 15), 3)
    
    # Draw UI with more visible elements
    # Title
    draw_text("FPS Gun Demo", BLACK, WIDTH // 2 - 100, 20)
    
    # Instructions
    draw_text("Click to shoot, Press R to reload", BLACK, WIDTH // 2 - 180, 60)
    
    # Cooldown indicator
    cooldown_pct = min(1.0, (current_time - gun.last_shot_time) / gun.cooldown_time)
    cooldown_color = GREEN if cooldown_pct >= 1.0 else RED
    pygame.draw.rect(screen, cooldown_color, (20, HEIGHT - 100, 200 * cooldown_pct, 30))
    pygame.draw.rect(screen, BLACK, (20, HEIGHT - 100, 200, 30), 3)
    draw_text("Cooldown", BLACK, 80, HEIGHT - 95)
    
    # Ammo counter
    ammo_text = f"Ammo: {gun.ammo}/30"
    draw_text(ammo_text, BLACK, 20, HEIGHT - 50)
    
    # Reloading indicator
    if gun.is_reloading:
        reload_pct = (current_time - gun.reload_start_time) / gun.reload_duration
        pygame.draw.rect(screen, GREEN, (250, HEIGHT - 50, 200 * reload_pct, 30))
        pygame.draw.rect(screen, BLACK, (250, HEIGHT - 50, 200, 30), 3)
        draw_text("Reloading...", BLACK, 300, HEIGHT - 45)
    
    # Debug info
    draw_text(f"Frame: {frame_count}", BLACK, WIDTH - 150, 20)
    draw_text(f"FPS: {int(clock.get_fps())}", BLACK, WIDTH - 150, 50)
    
    # Update display
    try:
        pygame.display.flip()
    except pygame.error as e:
        print(f"Display error: {e}")
        running = False
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
