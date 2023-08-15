# Modules imported
import pygame
import neat
import time
import os
import random
from bird import Bird
from pipe import Pipe
from base import Base

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


# Functions defined
def draw_window(window, bird):
    window.blit(BG_IMG, (0, 0))  # Draws the image
    bird.draw(window)
    pygame.display.update()


# Main
def main():
    bird = Bird(200, 200)
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(window, bird)

    pygame.quit()
    quit()


# Starting point
if __name__ == "__main__":
    main()
