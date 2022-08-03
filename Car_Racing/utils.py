from logging.config import valid_ident
from math import radians, sin, cos
import pygame
import numpy as np
import os
from PIL import Image

def rotate_image(img, angle, x, y):
    """
    Rotates an image around its center by an angle.
    Center coordinates: (x, y)

    Returns the rotated image and the position where to draw it
    """
    # rotate around the top-left corner
    rotated_image = pygame.transform.rotate(img, angle) 

    # center img
    topleft = (x, y)
    new_rect = rotated_image.get_rect(center=img.get_rect(topleft=topleft).center)
    return rotated_image, new_rect.topleft

def draw_rotated_image(img, angle, x, y, win):
    """
    Rotates the image by 'angle' and draws it in (x, y)
    """
    img, pos = rotate_image(img, angle, x, y)
    win.blit(img, pos)

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def load_and_resize(img_path, width, height):
    img = pygame.image.load(img_path)
    return pygame.transform.scale(img, (width, height))

def convert_png_transparent(src_file, dst_file, bg_color=(255,255,255)):
    """
    code from https://stackoverflow.com/questions/765736/how-to-use-pil-to-make-all-white-pixels-transparent
    """
    image = Image.open(src_file).convert("RGBA")
    array = np.array(image, dtype=np.ubyte)
    mask = (array[:,:,:3] == bg_color).all(axis=2)
    alpha = np.where(mask, 0, 255)
    array[:,:,-1] = alpha
    Image.fromarray(np.ubyte(array)).save(dst_file, "PNG")

def load_transparent_img(filename, width, height, track_num, finish_line=False):
    """
    Returns image and mask.
    If finish_line is true, it also returns the initial position
    """
    track_num = str(track_num)
    try:
        img = load_and_resize(os.path.join(f'images/track_{track_num}', f'transparent-{filename}.png'), width, height)
    except FileNotFoundError:
        convert_png_transparent(os.path.join(f'images/track_{track_num}', filename + '.png'), os.path.join(f'images/track_{track_num}', f'transparent-{filename}.png'))
        img = load_and_resize(os.path.join(f'images/track_{track_num}', f'transparent-{filename}.png'), width, height)
    mask = pygame.mask.from_surface(img)
    if finish_line:
        return img, mask, mask.outline()[0]
    return img, mask

def load_transparent_car(color, width, height):
    """
    Returns img of the car
    """
    try:
        img = load_and_resize(os.path.join(f'images/cars', f'transparent-{color}.png'), width, height)
    except FileNotFoundError:
        convert_png_transparent(os.path.join(f'images/cars', color + '.png'), os.path.join(f'images/cars', f'transparent-{color}.png'))
        img = load_and_resize(os.path.join(f'images/cars', f'transparent-{color}.png'), width, height)
    return img

def get_car(CARS, train=False):
    car = None
    valid_inputs = {'1': 'RED', '2': 'BLACK', '3': 'YELLOW', '4': 'GREEN'}
    car_description = '[1: RED], [2: BLACK], [3: YELLOW], [4: GREEN]'
    question = 'What car do you want to play with?' if not train else 'What car do you want to train?'
    while car not in valid_inputs.keys():
        car = input(f'\n{question}\n'
                    f'{car_description}\n'
                    f'Insert Number: ')
        if car not in valid_inputs.keys():
            print(f'\nYour input is not valid!\n')
    selected = CARS[valid_inputs[car]]
    print(f'\nYou selected: {selected["NAME"]}')
    return selected

def get_track(TRACKS):
    track = None
    valid_inputs = ['1', '2', '3']
    track_description = '[1: Train Track], [2: Round Track], [3: Test Track]'
    while track not in valid_inputs:
        track = input(f'\nWhat track do you want to play?\n'
                    f'{track_description}\n'
                    f'Insert Number: ')
        if track not in valid_inputs:
            print(f'\nYour input is not valid!\n')
    print(f'\nYou selected: TRACK_{track}')
    return TRACKS[f'TRACK_{track}']

def get_user():
    user = None
    valid_inputs = {'1': 'Player', '2': 'Computer'}
    user_description = '[1: Player], [2: Computer]'
    while user not in valid_inputs.keys():
        user = input(f'\nWho wants to play?\n'
                    f'{user_description}\n'
                    f'Insert Number: ')
        if user not in valid_inputs.keys():
            print(f'\nYour input is not valid!\n')
    print(f'You selected: {valid_inputs[user]}')
    return valid_inputs[user]

def get_num_computer_cars():
    out = ''
    while not out.isdigit():
        out = input(f'\nHow many different cars do you want to see?\n'
                    f'Insert Number: ')
        if not out.isdigit():
            print('Your input is not valid!')
    print(f'You selected {out} cars')
    return int(out)

#convert_png_transparent('images/cars/redbull.png', 'images/cars/redbull.png')