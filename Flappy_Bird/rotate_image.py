import pygame

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
    img, pos = rotate_image(img, angle, x, y)
    win.blit(img, pos)
