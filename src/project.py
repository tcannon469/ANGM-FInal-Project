import pygame
import sys
import os
from levelmaps import LEVEL_MAPS

# ************************************************************
# GLOBAL SETTINGS
# ************************************************************
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
FPS = 60

SKY_BLUE = (135, 206, 235)
RED = (200, 50, 50)

# Paths (src is one level below project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_ASSET_DIR = os.path.join(BASE_DIR, "..", "assets", "player")
TILE_ASSET_DIR = os.path.join(BASE_DIR, "..", "assets", "tiles")
END_IMAGE_PATH = os.path.join(BASE_DIR, "..", "assets", "player","end_screen.png")


# ************************************************************
# PLAYER CLASS
# ************************************************************
class Player:
    def __init__(self, x, y):
        # Collision rectangle
        self.rect = pygame.Rect(x, y, TILE_SIZE, int(TILE_SIZE * 1.5))
        self.color = RED  # fallback if images fail

        # Physics
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 4
        self.jump_power = 12
        self.gravity = 0.5
        self.max_fall_speed = 15
        self.on_ground = True

        # Animation state
        self.state = "idle"          # "idle", "run", "jump", "fall"
        self.facing_right = True
        self.frame_index = 0.0
        self.anim_speed = 0.12      # good for 2-frame run

        # Load animation frames (display already initialized in main)
        self.animations = self.load_animations()
        self.image = self.animations["idle"][0] if self.animations["idle"] else None

    #  LOAD ANIMATIONS FOR THE PLAYER DEPENDING ON ITS CURRENT STATE
    #---------------------------------------------------------
    def load_animations(self):
        animations = {}

        def load_and_scale(filename, required=False):
            path = os.path.join(PLAYER_ASSET_DIR, filename)
            if not os.path.exists(path):
                if required:
                    raise FileNotFoundError(
                        f"Required sprite '{filename}' not found in {PLAYER_ASSET_DIR}"
                    )
                return None
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (self.rect.width, self.rect.height))

        # idle.png (single frame) - REQUIRED
        idle_frames = []
        idle_img = load_and_scale("idle.png", required=True)
        idle_frames.append(idle_img)
        animations["idle"] = idle_frames

        # run1.png, run2.png (optionally run3.png later)
        run_frames = []
        for i in range(1, 4):
            img = load_and_scale(f"run{i}.png", required=False)
            if img:
                run_frames.append(img)
        if not run_frames:
            run_frames = idle_frames.copy()
        animations["run"] = run_frames

        # jump.png
        jump_frames = []
        jump_img = load_and_scale("jump.png", required=False)
        if jump_img:
            jump_frames.append(jump_img)
        else:
            jump_frames = idle_frames.copy()
        animations["jump"] = jump_frames

        # fall.png
        fall_frames = []
        fall_img = load_and_scale("fall.png", required=False)
        if fall_img:
            fall_frames.append(fall_img)
        else:
            fall_frames = jump_frames.copy()
        animations["fall"] = fall_frames

        return animations

    #  HANDLING INPUT FROM THE KEYBOARD
    #---------------------------------------------------------
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False

    #  PHYSICS - MAKE IT MORE NATURAL, there is still some work to do
    #---------------------------------------------------------
    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed

    def move_and_collide(self, tiles):
        # horizontal collisions
        self.rect.x += self.vel_x
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_x > 0:
                    self.rect.right = tile.left
                elif self.vel_x < 0:
                    self.rect.left = tile.right

        # vertical collisions
        self.rect.y += self.vel_y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:  # falling
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # going up
                    self.rect.top = tile.bottom
                    self.vel_y = 0

    # QUERING TO GET THE STATE OF THE PLAYER 
    #---------------------------------------------------------
    def update_state(self):
        if not self.on_ground:
            if self.vel_y < 0:
                self.state = "jump"
            else:
                self.state = "fall"
        else:
            if self.vel_x != 0:
                self.state = "run"
            else:
                self.state = "idle"
                
    # MAKES THE PLAYER MOVES SMOTHLY LIKE IN A SHORT VIDEO 
    #---------------------------------------------------------
    def animate(self):
        frames = self.animations.get(self.state, [])
        if not frames:
            self.image = None
            return

        self.frame_index += self.anim_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0.0

        frame = frames[int(self.frame_index)]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    #  UPDATE  PLAYER DEPENDING OF CURRENT EVENTS
    #---------------------------------------------------------
    def update(self, tiles):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide(tiles)
        self.update_state()
        self.animate()

    #  DRAW PLAYER 
    #---------------------------------------------------------
 
    def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        if self.image:
            surface.blit(self.image, draw_rect.topleft)
        else:
            pygame.draw.rect(surface, self.color, draw_rect)

    #  PLAYER REACHED THE END OF THE LEVEL  
    #---------------------------------------------------------
    def reached_end(self, level_width_pixels):
        return self.rect.right >= level_width_pixels



# ************************************************************
# CREATES THE  CURRENT  LEVEL ENVIRONMENT BASED ON THE TEXT BASED FILE FOUND IN LEVELMAPS
# ************************************************************
def build_level(level_map):
    tiles = []
    player_start_pos = (0, 0)

    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == "X":
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == "P":
                player_start_pos = (x, y)

    return tiles, player_start_pos


# ************************************************************
# HELPS WITH THE SCROLLING OF THE BACKGROUND WHILE THE PLAYER RUNS
# ************************************************************
def get_camera_x(player, level_width_pixels):
    target_x = player.rect.centerx - WIDTH // 2
    return max(0, min(target_x, level_width_pixels - WIDTH))


# ************************************************************
# TILE IMAGE LOADING (called AFTER pygame.init)
# ************************************************************
def load_tile_images():
    def load_tile(name):
        path = os.path.join(TILE_ASSET_DIR, name)
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    tiles = {
        "grass_single": load_tile("grass_single.png"),
        "grass_left": load_tile("grass_block_left.png"),
        "grass_middle": load_tile("grass_block_middle.png"),
        "grass_right": load_tile("grass_block_right.png"),
        "dirt": load_tile("dirt.png"),
    }
    return tiles


# ************************************************************
# FINAL SCREEN AND CLOSING THE PROGRAM
# ************************************************************
def show_end_screen(screen):
    """Show final image and wait for key press or window close."""
    # Try to load end_screen image; if not, fallback to text
    if os.path.exists(END_IMAGE_PATH):
        img = pygame.image.load(END_IMAGE_PATH).convert_alpha()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        screen.blit(img, (0, 0))
    else:
        # Fallback: simple message
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 64)
        text = font.render("You finished all levels!", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, rect)

    pygame.display.flip()

    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False


# ************************************************************
#                M A I N   R O U T I N E
# ************************************************************
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Platformer with Tiles & Sprites - Dev. Thomas Cannon - 2025")
    clock = pygame.time.Clock()

    # Now it's safe to load images with convert_alpha()
    tile_images = load_tile_images()

    current_level = 0
    tiles, player_pos = build_level(LEVEL_MAPS[current_level])
    player = Player(*player_pos)

    level_width_pixels = len(LEVEL_MAPS[current_level][0]) * TILE_SIZE
    running = True

    while running:
        dt = clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Update
        player.update(tiles)

        # Level switching or end of game
        if player.reached_end(level_width_pixels):
            current_level += 1
            if current_level >= len(LEVEL_MAPS):
                running = False
                current_level-=1
                # Show final image then exit
                show_end_screen(screen)
                
            else:
                tiles, player_pos = build_level(LEVEL_MAPS[current_level])
                player = Player(*player_pos)
                level_width_pixels = len(LEVEL_MAPS[current_level][0]) * TILE_SIZE

        camera_x = get_camera_x(player, level_width_pixels)

        # Drawing background
        screen.fill(SKY_BLUE)

        # Draw tilemap with grass top + dirt underneath
        level_rows = LEVEL_MAPS[current_level]
        for tile in tiles:
            r = tile.copy()
            r.x -= camera_x

            col = tile.x // TILE_SIZE
            row = tile.y // TILE_SIZE

            # Neighboring blocks
            left_exists = col > 0 and level_rows[row][col - 1] == "X"
            right_exists = col < len(level_rows[0]) - 1 and level_rows[row][col + 1] == "X"
            above_exists = row > 0 and level_rows[row - 1][col] == "X"

            if not above_exists:
                #  Put grass at the top
                if not left_exists and not right_exists:
                    img = tile_images["grass_single"]
                elif not left_exists and right_exists:
                    img = tile_images["grass_left"]
                elif left_exists and right_exists:
                    img = tile_images["grass_middle"]
                elif left_exists and not right_exists:
                    img = tile_images["grass_right"]
            else:
                # Put dirt if there is a block  above 
                img = tile_images["dirt"]

            screen.blit(img, r)

        # Draw player
        player.draw(screen, camera_x)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
