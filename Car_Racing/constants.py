import pygame 
import os

from utils import load_and_resize, scale_image, load_transparent_img, load_transparent_car

# --- Pygame Settings ---
WIN_WIDTH = 1600
WIN_HEIGHT = 900

CAR_WIDTH = 32
CAR_HEIGHT = 32

TRAIN_FPS = 30
GAME_FPS = 30
BORDER_RESET = 30
CAR_SCALE = 0.12
TOT_ITERATIONS = 500
STAT_FONT = pygame.font.SysFont('comicsans', 50)

# --- Neat Settings ---
BONUS_SCORE = 10000
DISTANCE_SCORE = 1
SURVIVAL_SCORE = 0
FINISH_SCORE = 10000

# --- Radar Settings ---
RADARS = {
    'N': 90,
    'S': 270,
    'E': 0,
    'W': 180,
    'NE': 45,
    'NW': 135,
    'SW': 225,
    'SE': 315
}

# --- Tracks Settings ---
TRACKS = {
    'TRACK_1' : {
        'TRACK_IMG': load_and_resize(os.path.join('images/track_1', 'track.png'), WIN_WIDTH, WIN_HEIGHT), 
        'TRACK_IMG_WITH_BONUS': load_and_resize(os.path.join('images/track_1', 'track_with_bonus.png'), WIN_WIDTH, WIN_HEIGHT),
        'BORDER_IMG': load_transparent_img('border', WIN_WIDTH, WIN_HEIGHT, track_num=1)[0],
        'BORDER_MASK': load_transparent_img('border', WIN_WIDTH, WIN_HEIGHT, track_num=1)[1],
        'FINISH_IMG': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=1)[0],
        'FINISH_MASK': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=1)[1],
        'FINISH_POSITION': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=1, finish_line=True)[2],
        'START_POSITION': [25, 50],
        'START_ANGLE': 270,
        'TOT_LAPS': 20,
        'BONUSES': {
            0: {'BONUS_IMG': load_transparent_img('bonus_1', WIN_WIDTH, WIN_HEIGHT, track_num=1)[0],
                  'BONUS_MASK': load_transparent_img('bonus_1', WIN_WIDTH, WIN_HEIGHT, track_num=1)[1]
            },
            1: {'BONUS_IMG': load_transparent_img('bonus_2', WIN_WIDTH, WIN_HEIGHT, track_num=1)[0],
                  'BONUS_MASK': load_transparent_img('bonus_2', WIN_WIDTH, WIN_HEIGHT, track_num=1)[1]
            },
            2: {'BONUS_IMG': load_transparent_img('bonus_3', WIN_WIDTH, WIN_HEIGHT, track_num=1)[0],
                  'BONUS_MASK': load_transparent_img('bonus_3', WIN_WIDTH, WIN_HEIGHT, track_num=1)[1]
            },
            3: {'BONUS_IMG': load_transparent_img('bonus_3', WIN_WIDTH, WIN_HEIGHT, track_num=1)[0],
                  'BONUS_MASK': load_transparent_img('bonus_3', WIN_WIDTH, WIN_HEIGHT, track_num=1)[1]
            }
        }
    },

    'TRACK_2' : {
        'TRACK_IMG': load_and_resize(os.path.join('images/track_2', 'track.png'), WIN_WIDTH, WIN_HEIGHT), 
        'TRACK_IMG_WITH_BONUS': load_and_resize(os.path.join('images/track_2', 'track_with_bonus.png'), WIN_WIDTH, WIN_HEIGHT),
        'BORDER_IMG': load_transparent_img('border', WIN_WIDTH, WIN_HEIGHT, track_num=2)[0],
        'BORDER_MASK': load_transparent_img('border', WIN_WIDTH, WIN_HEIGHT, track_num=2)[1],
        'FINISH_IMG': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=2)[0],
        'FINISH_MASK': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=2)[1],
        'FINISH_POSITION': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=2, finish_line=True)[2],
        'START_POSITION': [20, 40],
        'START_ANGLE': 270,
        'TOT_LAPS': 20,
        'BONUSES': {}
    },

    'TRACK_3' : {
        'TRACK_IMG': load_and_resize(os.path.join('images/track_3', 'track.png'), WIN_WIDTH, WIN_HEIGHT), 
        'TRACK_IMG_WITH_BONUS': load_and_resize(os.path.join('images/track_3', 'track_with_bonus.png'), WIN_WIDTH, WIN_HEIGHT),
        'BORDER_IMG': load_transparent_img('border', WIN_WIDTH, WIN_HEIGHT, track_num=3)[0],
        'BORDER_MASK': load_transparent_img('border', WIN_WIDTH, WIN_HEIGHT, track_num=3)[1],
        'FINISH_IMG': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=3)[0],
        'FINISH_MASK': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=3)[1],
        'FINISH_POSITION': load_transparent_img('finish_line', WIN_WIDTH, WIN_HEIGHT, track_num=3, finish_line=True)[2],
        'START_POSITION': [20, 80],
        'START_ANGLE': 270,
        'TOT_LAPS': 20,
        'BONUSES': {}
    },
    }


# --- Cars Settings ---
CARS = {
    'RED': {
        'NAME': 'red',
        'IMG': load_and_resize('images/cars/red.png', CAR_WIDTH, CAR_HEIGHT),
        'MAX_SPEED': 20,
        'MAX_SPEED_REV': -5,
        'ACCELERATION': 0.5,
        'BRAKE_INTENSITY': 2,
        'SLOW_DOWN_SPEED': 1/3,
        'STEERING_VELOCITY': 10,
        'MIN_SPEED': 5,
        'MIN_DIST_FRAME': 0.01,
        },

    'BLACK': {
        'NAME': 'black',
        'IMG': load_and_resize('images/cars/black.png', CAR_WIDTH, CAR_HEIGHT),
        'MAX_SPEED': 20,
        'MAX_SPEED_REV': -5,
        'ACCELERATION': 0.5,
        'BRAKE_INTENSITY': 2,
        'SLOW_DOWN_SPEED': 1/2,
        'STEERING_VELOCITY': 15,
        'MIN_SPEED': 5,
        'MIN_DIST_FRAME': 0.01,
        },

    'YELLOW': {
        'NAME': 'yellow',
        'IMG': load_and_resize('images/cars/yellow.png', CAR_WIDTH, CAR_HEIGHT),
        'MAX_SPEED': 20,
        'MAX_SPEED_REV': -5,
        'ACCELERATION': 0.5,
        'BRAKE_INTENSITY': 2,
        'SLOW_DOWN_SPEED': 1/2,
        'STEERING_VELOCITY': 12.5,
        'MIN_SPEED': 5,
        'MIN_DIST_FRAME': 0.01,
        },

    'GREEN': {
        'NAME': 'green',
        'IMG': load_and_resize('images/cars/green.png', CAR_WIDTH, CAR_HEIGHT),
        'MAX_SPEED': 25,
        'MAX_SPEED_REV': -5,
        'ACCELERATION': 0.5,
        'BRAKE_INTENSITY': 2.5,
        'SLOW_DOWN_SPEED': 1/2,
        'STEERING_VELOCITY': 12.5,
        'MIN_SPEED': 4,
        'MIN_DIST_FRAME': 0.01,
        },
}



