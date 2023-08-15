import pygame
import os


class Base:
    BASE_IMG = pygame.transform.scale2x(
        pygame.image.load(os.path.join("imgs", "base.png"))
    )
    VELOCITY = 5  # Same as pipe's
    WIDTH = BASE_IMG.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0  # Initial position of the first image of the base
        self.x2 = self.WIDTH  # Initial position of the second image of the base

    def move(self):
        """
        Circular loop of two images of the base which seems as an infinite number of
        base images showing at the bottom of the window
        """
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.BASE_IMG, (self.x1, self.y))
        window.blit(self.BASE_IMG, (self.x2, self.y))
