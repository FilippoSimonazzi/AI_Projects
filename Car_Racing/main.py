import pygame
import time
import neat
import pickle
pygame.font.init()

from player_car import PlayerCar
from ai_car import AICar

from constants import *
from utils import get_car, get_track, get_user

def draw_window(win, car, track, start_time, draw_radars=True, draw_bonus=False, crashed=False):
    if not draw_bonus:
        win.blit(track['TRACK_IMG'], (0, 0))
    else:
        win.blit(track['TRACK_IMG_WITH_BONUS'], (0, 0))

    current_lap = car.current_lap
    text = STAT_FONT.render(f'Laps: {current_lap} / {track["TOT_LAPS"]}', 1, 'black')
    win.blit(text, (WIN_WIDTH // 2 + 200 - text.get_width(), 20))

    if current_lap != track["TOT_LAPS"]:
        car.draw_car(win)
        if draw_radars:
            car.draw_radar(win)
        
        if not car.crashed:
            draw_time = time.time()
            text = STAT_FONT.render(f'Time: {round(draw_time - start_time, 2)}', 1, 'black')
            win.blit(text, (WIN_WIDTH // 2 - text.get_width(), 20))
    else:
        text = STAT_FONT.render(f'CONGRATULATIONS!', 10, 'red')
        win.blit(text, (WIN_WIDTH // 2 + 200 - text.get_width(), WIN_HEIGHT // 2 - 100 - text.get_height()))

    if crashed:
        text = STAT_FONT.render(f'CRASHED!', 10, 'red')
        win.blit(text, (WIN_WIDTH // 2 - text.get_width(), WIN_HEIGHT // 2 - 50 - text.get_height()))
    pygame.display.update()

def show_genome(genomes, config):
    car = AICar(CAR, TRACK)

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)

    run = True
    start_time = time.time()
    while run:
        clock.tick(GAME_FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        if not car.crashed:
            if car.current_lap != TRACK['TOT_LAPS'] and not car.crashed:
                output = net.activate(car.get_data())
                car.update(output)
        draw_window(win, car, TRACK, start_time, draw_radars=False, crashed=car.crashed)       
        

def play_user(car, track):
    """
    Car movements inspired by: https://github.com/techwithtim/Pygame-Car-Racer/blob/63b3d9f61bf34b7700eeba12a3e319d37f4f3c96/tutorial1-code/main.py#L4
    """
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    car = PlayerCar(car, track)

    run = True
    start_time = time.time()
    while run:
        clock.tick(GAME_FPS)
        draw_window(win, car, track, start_time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        if car.current_lap != track['TOT_LAPS']:
            pressed = pygame.key.get_pressed()
            car.update(pressed)

def play_ai(car_name):
    config_path = 'config-feedforward.txt'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    with open(f'trained_cars/{car_name}.pkl', 'rb') as f:
        genome = pickle.load(f)
        f.close()
    genomes = [(1, genome)]

    show_genome(genomes, config)

if __name__ == '__main__':
    user = get_user()
    CAR = get_car(CARS)
    TRACK = get_track(TRACKS)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    if user == 'Player':
        play_user(CAR, TRACK)
    elif user == 'Computer':
        play_ai(CAR['NAME'])
