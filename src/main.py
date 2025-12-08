import random
import pygame
import sys
from levelmaps import LEVEL_MAPS  
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#                        Global constants and settings
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
WIDTH, HEIGHT = 800, 600
TILESIZE = 32
FPS = 60


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# Function to build the level based on the level_map found in file level_maps.py
# Input: Level Map (2D List)
# Output: List of Tile Rects and Player Start Position  
# # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *    
def build_level(level_map):
    tiles = []
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILESIZE
            y = row_index * TILESIZE
            if tile == 'X':
                tiles.append(pygame.Rect(x, y, TILESIZE, TILESIZE))
            elif tile == 'P':
                player_start_pos = (x, y)
    return tiles, player_start_pos

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                                 Player Class
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
class Player:
    #   Initialize the player at a given position
    def __init__(self, position):
        self.rect = pygame.Rect(position[0], position[1], TILESIZE, TILESIZE)
        self.color = (0, 255, 0)  # Green color for the player
        self.vel_x = 0
        self.vel_y = 0  
        self.speed = 5
        self.jump_strength = 10
        self.gravity = 0.5
        self.on_ground = False
        self.max_fall_speed = 10

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
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False
            #   consider the negative effect of gravity
  
   # Apply gravity to the player when not on the ground 
    def apply_gravity(self):
        # increase downward velocity due to gravity
        self.vel_y += self.gravity  
        if self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed

    #   Check for collisions and adjust position accordingly
    def move_and_collide(self, tiles):
        # Horizontal movement
        self.rect.x += self.vel_x
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_x > 0:  # moving right
                    self.rect.right = tile.left
                elif self.vel_x < 0:  # moving left
                    self.rect.left = tile.right

        # Vertical movement
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
        self. handle_input()
        self.apply_gravity()
        self.move_and_collide(tiles)

    #   Draw the player on the given surface
    def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        pygame.draw.rect(surface, self.color, self.rect)


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                                 Camera Function
# Camera follow the player. Keep the player centered on the screen horizontally 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def get_camera_x(player, level_width_pixels):
    target_x = player.rect.centerx - WIDTH // 2
    target_x = max(0, min(target_x, level_width_pixels - WIDTH))
    return target_x


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#                      M A I N   P R O G R A M
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
def main():
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Final Projet - Thomas Cannon")

    tiles,playerPos = build_level(LEVEL_MAPS[0])
                                      # Generate a random color
    random_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

    # Fill the screen with the random color
    screen.fill(random_color)
    #pygame.display.flip()

    # Main loop to keep the window open
    running = True
    dt = clock.tick(FPS)  # Amount of seconds between each loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        # Update 
        player.update(tiles)
        #camera_x = get_camera_x(player, level_width_pixels)
        camera_x = get_camera_x(player, len(LEVEL_MAPS[0][0]) * TILESIZE)
        
        # Draw 
        screen.fill(SKY_BLUE)

        # Draw tiles
        for tile in tiles:
            #pygame.draw.rect(screen, (255, 255, 255), tile)
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