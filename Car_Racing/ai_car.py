from constants import *
from car import AbstractCar

class AICar(AbstractCar):    
    def __init__(self, car_settings, track_settings):
        super().__init__(car_settings, track_settings)

        self.disabled_back = True
        
    def is_crashed(self):
        return self.crashed

    def get_score(self):
        return self.score

    def get_data(self):
        distances = list(self.distances.values())
        return distances + [self.velocity] + [self.acceleration] + [self.brake_intensity] + [self.slow_down_speed] + [self.steering_vel]

    def update(self, output):
        up, down, left, right, nothing = False, False, False, False, False
        if output[0] > 0:
            up = True
        if output[1] > 0:
            down = True
        if output[2] > 0:
            left = True
        if output[3] > 0:
            right = True
        if up and down or (not up and not down):
            nothing = True
            up, down = False, False
            left, right = False, False

        if up:
            self.move_forward()
        if down:
            self.decelerate()
        self.rotate(left, right)
        if nothing:
            self.slow_down()

        self.handle_collision()


        