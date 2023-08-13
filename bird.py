import pygame


class Bird:
    BIRD_IMGS = [
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
    ]
    MAX_ROTATION = 25  # How much degrees to rotate when tilting
    ROTATION_VELOCITY = 20  # How much we rotate on each frame
    ANIMATION_TIME = 5  # How long for each bird animation

    def __init__(self, x, y):
        self.x = x  # Initial x
        self.y = y  # Initial y
        self.tilt = 0  # How much the image is tilted
        self.tick_count = 0  #
        self.velocity = 0  # Initial velocity
        self.height = self.y  #
        self.img_count = 0  # To know which image to show of the bird
        self.img = self.BIRD_IMGS[0]  # Initial image

    def jump(self):
        self.velocity = -10.5  # Negative goes upwards
        self.tick_count = 0  # Keep track of when we last jumped
        self.height = self.y  # Keep track of where did the bird jump from

    def move(self):
        self.tick_count += (
            1  # A frame went by (how many times we moved since the last jump)
        )
        displacement = (
            self.velocity * self.tick_count + 1.5 * self.tick_count**2
        )  # Makes the arc movement of the bird

        if displacement >= 16:
            displacement = 16  # not go down more than 16

        if displacement < 0:
            displacement -= 2  # go upwards a little more

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
            else:
                if self.tilt > -90:
                    self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.BIRD_IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.BIRD_IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.BIRD_IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.BIRD_IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.BIRD_IMGS[0]
            self.img_count = 0

