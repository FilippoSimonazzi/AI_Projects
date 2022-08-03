import pygame
from constants import BIRD_IMGS, BIRD_MAX_ROTATION, BIRD_ROT_VEL, BIRD_ANIMATION_TIME
from rotate_image import draw_rotated_image

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = BIRD_MAX_ROTATION
    ROT_VEL = BIRD_ROT_VEL
    ANIMATION_TIME = BIRD_ANIMATION_TIME

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5 # pygame "upper row" is 0, thus we need a negative velocity to go up
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # compute "displacement" --> how many pixels we move up or down
        # s = v*t + 3/2*t^2
        d = self.vel * self.tick_count + 2.0 * self.tick_count**2
        
        if d >= 0:
            # introduce terminal velocity check
            d = min(16, d)
        else:
            # finetune while going up
            d -= 2

        # actually move
        self.y += d

        # --- tilting movements ---
        # if we are going up or if we are still close to where we started
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            # "nosedive" to the ground
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count += 1

        # --- Animation Loop ---
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # if nosediving we don't want to flap the wings
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # tilt the image
        draw_rotated_image(self.img, self.tilt, self.x, self.y, win)

        
    def get_mask(self):
        """
        Needed to get collisions
        """
        return pygame.mask.from_surface(self.img)
