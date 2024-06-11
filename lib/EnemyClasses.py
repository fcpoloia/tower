import pygame
import math

class Dummy(pygame.sprite.Sprite):
    def __init__(self, position: list[int,int], speed:int, target, health:int):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((30,30))
        self.image.fill((255,0,0))

        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1])

        self.TRGT = target
        self.SPD = speed
        self.HP = health

    def update(self):
        target_x, target_y = self.TRGT
        current_x, current_y = self.rect.center
        distance_x = target_x - current_x
        distance_y = target_y - current_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if distance != 0:
            direction_x = distance_x / distance
            direction_y = distance_y / distance
            move_x = direction_x * self.SPD
            move_y = direction_y * self.SPD
            if abs(move_x) > abs(distance_x):
                move_x = distance_x
            if abs(move_y) > abs(distance_y):
                move_y = distance_y
            self.rect.x += move_x
            self.rect.y += move_y

        


        





