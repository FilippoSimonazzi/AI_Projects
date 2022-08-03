import pygame
import random

from constants import PIPE_IMG, PIPE_GAP, DRIFT_VEL, STAT_FONT, BASE_INIT_POS

class Pipe:
    GAP = PIPE_GAP
    VEL = DRIFT_VEL

    def __init__(self, x):
        self.x = x

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height() 
        self.pipe_gap = random.randrange(PIPE_GAP, PIPE_GAP + 50)
        self.bottom = self.height + self.pipe_gap

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
        text = STAT_FONT.render('GAP', 1, 'black')
        win.blit(text, (self.x + 10, BASE_INIT_POS - 80))
        text = STAT_FONT.render(str(self.pipe_gap), 1, 'black')
        win.blit(text, (self.x + 20, BASE_INIT_POS - 50))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # compute offsets
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # check if the masks are colliding
        t_point = bird_mask.overlap(top_mask, top_offset) # if they don't collide this returns None
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) 

        if t_point or b_point:
            return True

        return False


