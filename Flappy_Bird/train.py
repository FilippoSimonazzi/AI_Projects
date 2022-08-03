import pygame
import neat
import os
import pickle
pygame.font.init()

from bird import Bird
from base import Base
from pipe import Pipe

from constants import WIN_HEIGHT, WIN_WIDTH, BG_IMG, TRAIN_FPS, BIRD_INIT_POS, PIPE_INIT_POS, BASE_INIT_POS, STAT_FONT, NUM_GENERATIONS, FITNESS_THRESHOLD

GEN = 0

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
        
    for bird in birds:
        bird.draw(win)
    base.draw(win)

    text = STAT_FONT.render(f'Score: {score}', 1, 'white')
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render(f'Gen: {gen}', 1, 'white')
    win.blit(text, (10, 10))

    text = STAT_FONT.render(f'Birds: {len(birds)}', 1, 'white')
    win.blit(text, (10, 50))

    pygame.display.update()


def get_config_path(filename):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, filename)
    return config_path
    

def eval_genome(genomes, config):
    global GEN
    nets = []
    ge = []
    birds = []
    GEN += 1

    for _, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(*(BIRD_INIT_POS)))
        ge.append(g)
    
    base = Base(BASE_INIT_POS)
    pipes = [Pipe(PIPE_INIT_POS)]
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(TRAIN_FPS) 
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        # --- move the birds ---
        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_idx = 1
        else:
            run = False

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            t_dist = abs(bird.y - pipes[pipe_idx].height)
            b_dist = abs(bird.y - pipes[pipe_idx].bottom)
            output = nets[x].activate((bird.y, t_dist, b_dist, pipes[pipe_idx].PIPE_TOP.get_width(), pipes[pipe_idx].pipe_gap))

            if output[0] > 0.5:
                bird.jump()
        # -------------------------

        base.move()
        
        add_pipe = False
        rem_pipes = []
        rem_ge = []
        for pipe in pipes:
            for idx, bird in enumerate(birds):

                if pipe.collide(bird):
                    ge[idx].fitness -= 5
                    rem_ge.append(idx)
                
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
            for idx, g in enumerate(ge):
                if idx not in rem_ge:
                    g.fitness += 10
            pipes.append(Pipe(PIPE_INIT_POS))

        for r in rem_pipes:
            pipes.remove(r)
        
        for idx, bird in enumerate(birds):
            # check if bird hits the ground
            if bird.y + bird.img.get_height() >= BASE_INIT_POS:
                ge[idx].fitness -= 10
                rem_ge.append(idx)

            elif bird.y <= 0:
                ge[idx].fitness -= 10
                rem_ge.append(idx)
        
        birds = [birds[idx] for idx in range(len(birds)) if idx not in rem_ge]
        nets = [nets[idx] for idx in range(len(nets)) if idx not in rem_ge]
        ge = [ge[idx] for idx in range(len(ge)) if idx not in rem_ge]

        if any([g.fitness > FITNESS_THRESHOLD for g in ge]):
            break
            

def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genome, NUM_GENERATIONS)

    print(winner)
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)
        f.close()

if __name__ == '__main__':
    run('config.txt')