# Modules imported
import pygame
import neat
import time
import os
import random
from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("comicsans", 50)


# Functions defined
def draw_window(window, bird, pipes, base, score):
    window.blit(BG_IMG, (0, 0))  # Draws the image
    for pipe in pipes:
        pipe.draw(window)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    base.draw(window)
    bird.draw(window)
    pygame.display.update()


# Main
def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True
    clock = pygame.time.Clock()
    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()

        add_pipe = False
        remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # Pipe is out of the screen
                remove.append(pipe)
            if not pipe.passed and pipe.x < bird.x:  # Bird passes the pipe
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for pipe in remove:  # Remove pipes
            pipes.remove(pipe)

        if bird.y + bird.img.get_height() >= 730:
            pass

        base.move()
        draw_window(window, bird, pipes, base, score)

    pygame.quit()
    quit()


# Starting point
if __name__ == "__main__":
    main()
