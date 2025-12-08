import random
import pygame
import sys
from levelmaps import LEVEL_MAPS  
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#                        Global constants and settings
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32
FPS = 60
# Colors
SKY_BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)
RED = (200, 50, 50)

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                                 Player Class
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
class Player:
    #   Initialize the player at a given position
    def __init__(self, x,y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE*1.5)
        self.color = RED  

        self.vel_x = 0
        self.vel_y = 0  
        
        self.speed = 4
        self.jump_power = 12
        self.gravity = 0.5
        self.max_fall_speed = 15

        self.on_ground = True

    #   Response to keyboard input for movement and jumping
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
       
        #   Handle left and right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        #   Handle jumping maybe consider the negative effect of gravity
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            #   consider the negative effect of gravity
  
    # Apply gravity to the player when not on the ground 
    def apply_gravity(self):
        # increase downward velocity due to gravity
        self.vel_y += self.gravity  
        if self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed

    #   Adjust position and check for collisions 
    def move_and_collide(self, tiles):
        # --- Horizontal movement ---
        self.rect.x += self.vel_x
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_x > 0:  # moving right
                    self.rect.right = tile.left
                elif self.vel_x < 0:  # moving left
                    self.rect.left = tile.right

        # --- Vertical movement ---
        self.rect.y += self.vel_y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:  # falling
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # jumping upward
                    self.rect.top = tile.bottom
                    self.vel_y = 0


    #   Update the player's position based on velocity and apply gravity
    def update(self, tiles):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide(tiles)


    # Check if the player finished the current level
    def reached_end(self, level_width_pixels):
        return self.rect.right >= level_width_pixels

    #   Draw the player on the given surface
    def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        pygame.draw.rect(surface, self.color, draw_rect)


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                                 Camera Function
# Camera follow the player. Keep the player centered on the screen horizontally 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def get_camera_x(player, level_width_pixels):
    target_x = player.rect.centerx - WIDTH // 2
    target_x = max(0, min(target_x, level_width_pixels - WIDTH))
    return target_x

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#   Function to build the level based on the level_map found in file level_maps.py
#   Input: Level Map (2D List)
#   Output: List of Tile Rects and Player Start Position  
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    
def build_level(level_map):
    tiles = []
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == 'X':
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == 'P':
                player_start_pos = (x, y)
    return tiles, player_start_pos


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                      M A I N   P R O G R A M
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def main():
    current_level = 0
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Final Projet - Thomas Cannon  -  My Mini Mario")
   
    tiles,playerPos = build_level(LEVEL_MAPS[current_level])
   # Setting the stage and the player 
    px, py = playerPos
    player = Player(px, py)
    level_width_pixels = len(LEVEL_MAPS[current_level]) * TILE_SIZE
    running = True
      
    # Main loop to keep the window open
    while running:
        dt = clock.tick(FPS)  # Amount of seconds between each loop
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        # Update 
        player.update(tiles)
        # If player reached the end of the screen goes to the next level or game ends
        if player.reached_end(level_width_pixels):
            current_level += 1
            if current_level >= len(LEVEL_MAPS):
                screen.fill((0, 0, 0))
                font = pygame.font.SysFont(None, 48)
                text = font.render("You finished all levels!", True, (255, 255, 255))
                screen.blit(text, (100, 250))
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False
            else:
                tiles, playerPos = build_level(LEVEL_MAPS[current_level])
                player.rect.topleft = playerPos
                player.vel_x = 0
                player.vel_y = 0
                level_width_pixels = len(LEVEL_MAPS[current_level][0]) * TILE_SIZE

        camera_x = get_camera_x(player, level_width_pixels)
        
        # Draw 
        screen.fill(SKY_BLUE)

        # Draw tiles
        for tile in tiles:
            # draw relative to camera
            draw_rect = tile.copy()
            draw_rect.x -= camera_x
            pygame.draw.rect(screen, BROWN, draw_rect)
            # little green top, like grass
            grass_rect = pygame.Rect(draw_rect.x, draw_rect.y, draw_rect.width, 6)
            pygame.draw.rect(screen, GREEN, grass_rect)     

        # Draw player
        player.draw(screen, camera_x)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()    


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                         ENTRY POINT OF PROGRAM 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
if __name__ == "__main__":
    main()