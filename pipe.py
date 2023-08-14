import pygame
import os
import random


class Pipe:
    PIPE_IMG = pygame.transform.scale2x(
        pygame.image.load(os.path.join("imgs", "pipe.png"))
    )
    GAP = 200
    VELOCITY = 5

    def __init__(self, x: int):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMG
        self.passed = False  # If the bird passed this pipe
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Returns None if no collision
        bottom_collision_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_collision_point = bird_mask.overlap(top_mask, top_offset)

        if top_collision_point or bottom_collision_point:
            return True
        return False
