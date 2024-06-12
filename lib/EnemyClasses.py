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
        self.dir_vector = pygame.Vector2(self.TRGT[0] - self.rect.centerx, self.TRGT[1] - self.rect.centery).normalize()
        self.position = pygame.Vector2(self.rect.center)

    def update(self):
        self.position += self.dir_vector * self.SPD
        self.rect.center = self.position

        


        





