import pygame
import os

WIN_WIDTH = 500
WIN_HEIGHT = 800
DRIFT_VEL = 5
TRAIN_FPS = 1000
SHOW_FPS = 50
STAT_FONT = pygame.font.SysFont('comicsans', 50)
NUM_GENERATIONS = 100
FITNESS_THRESHOLD = 1500


BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
             pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]
BIRD_MAX_ROTATION = 25
BIRD_ROT_VEL = 20
BIRD_ANIMATION_TIME = 5
BIRD_INIT_POS = (230, 350)


PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
PIPE_GAP = 100
PIPE_INIT_POS = 600

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
BASE_INIT_POS = 730

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))

