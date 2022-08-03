import pygame
from math import sin, radians, cos, sqrt, pow
import numpy as np
import time

from constants import *
from utils import draw_rotated_image

class AbstractCar:
    """
    Code inspired by:
    - https://github.com/techwithtim/Pygame-Car-Racer/blob/main/tutorial1-code/main.py
    - https://github.com/Adil7777/AI_Learns_to_drive_car/blob/master/car.py
    """
    def __init__(self, car_settings, track_settings):
        # --- Car Settings ---
        self.starting_pos = self.get_initial_position(track_settings)
        self.start_angle = track_settings['START_ANGLE']
        self.img = car_settings['IMG']
        self.x, self.y = self.starting_pos[0], self.starting_pos[1]
        self.velocity = 0
        self.angle = self.start_angle
        self.acceleration = car_settings['ACCELERATION']
        self.brake_intensity = car_settings['BRAKE_INTENSITY']
        self.slow_down_speed = car_settings['SLOW_DOWN_SPEED']
        self.steering_vel = car_settings['STEERING_VELOCITY']
        self.min_speed = car_settings['MIN_SPEED']
        self.max_speed = car_settings['MAX_SPEED']
        self.max_speed_rev = car_settings['MAX_SPEED_REV']
        self.min_dist_frame = car_settings['MIN_DIST_FRAME']
        self.length = self.img.get_height()
        self.width = self.img.get_width()
        
        # --- Track Settings ---
        self.border_img = track_settings['BORDER_IMG']
        self.border_mask = track_settings['BORDER_MASK']
        self.finish_mask = track_settings['FINISH_MASK']
        self.finish_position = track_settings['FINISH_POSITION']
        self.tot_laps = track_settings['TOT_LAPS']
        self.bonus_dict = track_settings['BONUSES']
        

        # --- Ai Car Settings ---
        self.score = 0
        self.time_alive = 0
        self.bonuses = 0

        self.stuck_time = 0
        self.not_moving = 0
        self.bouncing = 0
        self.slow_control = [0]

        self.tot_distance = 0
        self.crashed = False
        self.finished = [False] * self.tot_laps
        self.collected_finish = [False] * self.tot_laps
        self.current_lap = 0
        self.race_completed = False

        self.disabled_back = False
        self.collected_bonus = [False] * len(track_settings['BONUSES'].keys())
        self.rewarded_bonus = [False] * len(track_settings['BONUSES'].keys())

        self.radars = {}
        self.distances = {}
        self.get_cardinal_points()
        self.check_radars()
    
    def get_initial_position(self, track_settings):
        x_init = track_settings['FINISH_POSITION'][0] + track_settings['START_POSITION'][0]
        y_init = track_settings['FINISH_POSITION'][1] + track_settings['START_POSITION'][1]
        return (x_init, y_init)
        
    def reset(self):
        self.x, self.y = self.starting_pos
        self.velocity = 0
        self.angle = self.start_angle
        
    def get_cardinal_points(self):
        r = radians(self.angle)

        self.rect = pygame.Rect(0, 0, self.width, self.length)
        self.rect.centerx = self.x + self.width / 2
        self.rect.centery = self.y + self.length / 2

        self.front = (self.rect.centerx - sin(r) * self.width / 2, 
                      self.rect.centery - cos(r) * self.length / 2)

        self.back = (self.rect.centerx + sin(r) * self.width / 2, 
                      self.rect.centery + cos(r) * self.length / 2)
        
    def rotate(self, left=False, right=False):
        if self.velocity > 0:
            if left:
                self.angle += self.steering_vel
            elif right:
                self.angle -= self.steering_vel
        elif self.velocity < 0:
            if left:
                self.angle -= self.steering_vel
            elif right:
                self.angle += self.steering_vel
        self.get_cardinal_points()

    def compute_distance_covered(self, start, end, _norm=np.linalg.norm):
        if self.velocity > 0:
            return _norm(start - end)
        return 0

    def move(self):
        self.distance_covered = 0
        prev_location = np.array((self.rect.centerx, self.rect.centery))
        rad_angle = radians(self.angle)
        self.y -= cos(rad_angle) * self.velocity
        self.x -= sin(rad_angle) * self.velocity

        self.get_cardinal_points()
        self.check_radars()

        self.distance_covered = self.compute_distance_covered(prev_location, np.array((self.rect.centerx, self.rect.centery)))
        if self.distance_covered < self.min_dist_frame:
            self.not_moving += 1
            if self.not_moving == 10:
                self.crashed = True
        else:
            self.not_moving = 0
        self.tot_distance += self.distance_covered

    def move_forward(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_speed)
        self.slow_control.append(self.velocity)
        self.slow_control = self.slow_control[-60:]
        if len(self.slow_control) > 50 and all([speed < self.min_speed for speed in self.slow_control]):
            self.crashed = True
        self.move()

    def slow_down(self):
        self.velocity = max(self.velocity - (self.acceleration * self.slow_down_speed), 0)
        if self.disabled_back:
            self.velocity = max(self.velocity, 0)
        self.move()

    def decelerate(self):
        self.velocity = max(self.velocity - (self.acceleration * self.brake_intensity), self.max_speed_rev)
        if self.disabled_back:
            self.velocity = max(self.velocity, 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)

        offset = (int(self.x - x), int(self.y - y))
        point = mask.overlap(car_mask, offset)
        return point

    def bounce(self):
        self.velocity = -self.velocity / 2
        self.move()

    def check_radar(self, position, degree):
        r = radians(360 - self.angle - degree)
        dist = 0
        x, y = int(self.front[0]), int(self.front[1])
        try:
            map_value = self.border_img.get_at((x, y))
        except IndexError:
            self.radars[position] = [(x, y), dist]

        while not map_value != (255, 255, 255, 0) and dist < 500:
            dist += 1
            x = min(WIN_WIDTH, int(x + cos(r) * dist))
            y = min(WIN_HEIGHT, int(y + sin(r) * dist))
            try:
                map_value = self.border_img.get_at((x, y))
            except IndexError:
                self.radars[position] = [(x, y), dist]
        
        dist = int(sqrt(pow(x - self.rect.centerx, 2) + pow(y - self.rect.centery, 2)))
        self.radars[position] = (x, y)
        self.distances[position] = dist
        if all([d <= BORDER_RESET for d in self.distances.values()]) and abs(self.velocity) < 0.5:
            self.stuck_time += 1
        else:
            self.stuck_time = 0
        if self.stuck_time == 15:
            self.crashed = True

    def check_radars(self):
        for dir, angle in RADARS.items():
            self.check_radar(dir, angle)

    def draw_radar(self, win):
        if len(self.radars.keys()) > 0:
            for pos in self.radars.values():
                pygame.draw.line(win, (255, 0, 0), self.rect.center, pos, 1)
                pygame.draw.circle(win, (0, 255, 0), pos, 3)

    def draw_car(self, win):
        draw_rotated_image(self.img, self.angle, self.x, self.y, win)

    def handle_collision(self):
        if self.collide(self.border_mask) != None:
            self.crashed = True
            self.bounce()
        
        if not all(self.collected_bonus):
            for id, imgs in self.bonus_dict.items():
                if not self.collected_bonus[id]:
                    if self.collide(imgs['BONUS_MASK']) != None:
                        self.collected_bonus[id] = True

        finish_collision = self.collide(self.finish_mask)
        if finish_collision != None:
            if finish_collision[0] > self.finish_position[0] + 3 and not self.finished[self.current_lap]:
                self.crashed = True
                self.bounce()
            else:
                self.finished[self.current_lap] = True
        else:
            if self.current_lap < self.tot_laps:
                if self.finished[self.current_lap]:
                    self.current_lap += 1
            else:
                self.race_completed = True

    def get_reward(self):
        bonus_points = 0
        for id in range(len(self.rewarded_bonus)):
            if not self.rewarded_bonus[id] and self.collected_bonus[id]:
                self.rewarded_bonus[id] = True
                bonus_points += BONUS_SCORE

        finish_points = 0
        for id in range(len(self.finished)):
            if not self.collected_finish[id] and self.finished[id]:
                self.collected_finish[id] = True
                finish_points += FINISH_SCORE

        distance_points = self.distance_covered * DISTANCE_SCORE
        
        time_points = SURVIVAL_SCORE
    
        temp_score = distance_points + time_points + bonus_points + finish_points
        self.score += temp_score
        return temp_score