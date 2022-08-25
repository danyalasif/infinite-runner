import math
import pygame
from random import randint

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.move_speed = 20
        self.image = pygame.Surface((5, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(midbottom = (80, 250))
        mouse = pygame.mouse.get_pos()

        self.floating_point_x = self.rect.x
        self.floating_point_y = self.rect.y
 
        x_diff = mouse[0] - self.rect.x
        y_diff = mouse[1] - self.rect.y
        angle = math.atan2(y_diff, x_diff);
        self.change_x = math.cos(angle) * self.move_speed
        self.change_y = math.sin(angle) * self.move_speed

    def update(self):
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)
        self.destroy()
    
    def destroy(self):
        if self.rect.x > 800:
            self.kill()