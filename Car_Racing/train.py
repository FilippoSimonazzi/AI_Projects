from glob import glob
import pygame
import neat
import os
import pickle
pygame.font.init()

from ai_car import AICar
from constants import *
from utils import get_car

def draw_window(win, track, cars, gen, best_score, best_pos, draw_radars=False, draw_bonus=True):
    global current_lap

    if draw_bonus and current_lap == 0:
        win.blit(track['TRACK_IMG_WITH_BONUS'], (0, 0))
    else:
        win.blit(track['TRACK_IMG'], (0, 0))

    text = STAT_FONT.render(f'Gen: {gen}', 1, 'black')
    win.blit(text, (WIN_WIDTH // 2 - 300 -  text.get_width(), 20))

    text = STAT_FONT.render(f'Cars: {len(cars)}', 1, 'black')
    win.blit(text, (WIN_WIDTH // 2 - 100 - text.get_width(), 20))

    if len(cars) > 0:
        current_lap = max([car.current_lap for car in cars])
    text = STAT_FONT.render(f'Laps: {current_lap} / {track["TOT_LAPS"]}', 1, 'black')
    win.blit(text, (WIN_WIDTH // 2 + 125 - text.get_width(), 20))

    text = STAT_FONT.render(f'Best Score: {best_score}', 1, 'black')
    win.blit(text, (WIN_WIDTH // 2 + 500 - text.get_width(), 20))

    pygame.draw.circle(win, 'blue', best_pos, 5)

    for car in cars:
        car.draw_car(win)
        if draw_radars:
            car.draw_radar(win)
    pygame.display.update()


def evaluate_genome(genomes, config):
    """
    Neat code inspired by: https://github.com/Adil7777/AI_Learns_to_drive_car/blob/master/main.py
    """
    global generation
    global best_score
    global best_position

    generation += 1
    gen_best_score = 0
    nets = []
    cars = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(AICar(TRAIN_CAR, TRAIN_TRACK))
        g.fitness = 0

    run = True
    while run:
        clock.tick(TRAIN_FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for id, car in enumerate(cars):
            output = nets[id].activate(car.get_data())
            car.update(output)
            if car.race_completed:
                genomes[id][1].fitness = 10**6 # bigger than fitness-treshold --> training ends
                run = False
                break

        rem = []
        for id, car in enumerate(cars):
            if not car.is_crashed():
                genomes[id][1].fitness += car.get_reward()
            else:
                rem.append(id)
        
        cars = [cars[idx] for idx in range(len(cars)) if idx not in rem]
        nets = [nets[idx] for idx in range(len(nets)) if idx not in rem]
        genomes = [genomes[idx] for idx in range(len(genomes)) if idx not in rem]
        
        if len(cars) == 0:
            run = False
        else:
            scores = [car.get_score() for car in cars]
            score = max(scores) 
            best_idx = scores.index(score)
            score = round(score, 2)

            if score > gen_best_score:
                gen_best_score = score
                best_gen_position = (cars[best_idx].x, cars[best_idx].y)
                
        draw_window(win, TRAIN_TRACK, cars, generation, best_score, best_position, draw_radars=False)
    
    if gen_best_score > best_score:
        best_score = gen_best_score
    best_position = best_gen_position
        

def train():
    config_path = 'config-feedforward.txt'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(evaluate_genome, TOT_ITERATIONS)
    with open(f'trained_cars/{TRAIN_CAR["NAME"]}.pkl', 'wb') as f:
        pickle.dump(winner, f)
        f.close()

if __name__ == '__main__':
    TRAIN_CAR = get_car(CARS, train=True)
    TRAIN_TRACK = TRACKS['TRACK_1'] # training track

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    generation = 0
    best_score = 0
    best_position = TRAIN_TRACK['FINISH_POSITION']
    current_lap = 0
    train()
