# Modules imported
import pygame
import neat
import os
from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("", 50)
GEN = -1


# Functions defined
def draw_window(window, birds, pipes, base, score, gen):
    window.blit(BG_IMG, (0, 0))  # Draws the image
    for pipe in pipes:
        pipe.draw(window)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    window.blit(text, (10, 10))

    base.draw(window)

    for bird in birds:
        bird.draw(window)
    pygame.display.update()


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    # Detailed information (Optional)
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(main, 50)


# Main
def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []  # Genomes
    birds = []

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(
            genome, config
        )  # setup a neural network
        nets.append(net)
        birds.append(Bird(230, 350))
        genome.fitness = 0
        ge.append(genome)

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
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            # If the birds passed the first pipe
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                pipe_index = 1
        else:  # No birds left
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1  # Adding fitness while bird is moving

            # Giving all needed inputs to get the output
            output = nets[x].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_index].height),
                    abs(bird.y - pipes[pipe_index].bottom),
                )
            )
            if output[0] < 0.5:
                bird.jump()

        add_pipe = False
        remove = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:  # Bird passes the pipe
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:  # Pipe is out of the screen
                remove.append(pipe)
            pipe.move()

        if add_pipe:  # Update the score, add a pipe & increase fitness
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for pipe in remove:  # Remove pipes
            pipes.remove(pipe)

        for x, bird in enumerate(birds):
            # Bird hits the ground or the ceiling
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(window, birds, pipes, base, score, GEN)


# Starting point
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
    main()
