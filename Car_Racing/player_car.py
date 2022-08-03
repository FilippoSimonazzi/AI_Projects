from constants import *
from car import AbstractCar

class PlayerCar(AbstractCar):    
    def __init__(self, car_settings, track_settings):
        super().__init__(car_settings, track_settings)

    def update(self, pressed):
        moved = False
        if pressed[pygame.K_UP]:
            moved = True
            self.move_forward()
        if pressed[pygame.K_DOWN]:
            moved = True
            self.decelerate()
        if pressed[pygame.K_LEFT]:
            self.rotate(left=True)
        if pressed[pygame.K_RIGHT]:
            self.rotate(right=True)
        if not moved:
            self.slow_down()
        self.handle_collision()
    
    def get_best_time(self):
        return max(self.lap_times)