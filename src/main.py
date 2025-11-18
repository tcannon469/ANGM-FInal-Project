import random
import pygame
import sys


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Random Color Screen")

    # Generate a random color
    random_color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

    # Fill the screen with the random color
    screen.fill(random_color)
    pygame.display.flip()

    # Main loop to keep the window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()    

if __name__ == "__main__":
    main()