import pygame
import neat
import os
import pickle
pygame.font.init()

from bird import Bird
from base import Base
from pipe import Pipe

from constants import WIN_HEIGHT, WIN_WIDTH, BG_IMG, SHOW_FPS, BIRD_INIT_POS, PIPE_INIT_POS, BASE_INIT_POS, STAT_FONT

GEN = 0

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
        
    bird.draw(win)
    base.draw(win)

    text = STAT_FONT.render(f'Score: {score}', 1, 'white')
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()


def get_config_path(filename):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, filename)
    return config_path
    

def show_genome(genomes, config):
    bird = Bird(*(BIRD_INIT_POS))

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
    
    base = Base(BASE_INIT_POS)
    pipes = [Pipe(PIPE_INIT_POS)]
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(SHOW_FPS) 
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        

        if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_idx = 1
        else:
            pipe_idx = 0

        bird.move()

        t_dist = abs(bird.y - pipes[pipe_idx].height)
        b_dist = abs(bird.y - pipes[pipe_idx].bottom)
        output = net.activate((bird.y, t_dist, b_dist, pipes[pipe_idx].PIPE_TOP.get_width(), pipes[pipe_idx].pipe_gap))

        if output[0] > 0.5:
            bird.jump()
        # -------------------------

        base.move()
        
        add_pipe = False
        rem_pipes = []
        rem_ge = []
        for pipe in pipes:

            if pipe.collide(bird):
                run = False
                
            # check if we passed the pipe
            if not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < bird.x:
                pipe.passed = True
                add_pipe = True
            
            # check if pipe is completely off the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem_pipes.append(pipe)

            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(PIPE_INIT_POS))

        for r in rem_pipes:
            pipes.remove(r)

        draw_window(win, bird, pipes, base, score)


def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    with open("winner.pkl", "rb") as f:
        genome = pickle.load(f)

    genomes = [(1, genome)]

    show_genome(genomes, config)

if __name__ == '__main__':
    run('config.txt')
