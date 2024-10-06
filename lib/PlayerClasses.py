import pygame
import json
import math
from typing import Dict

###-------------------------------CLASSES-------------------------------###


# player
class Player(pygame.sprite.Sprite):
    def __init__(self, hp=10, dmg=1, attspd=100, bulspd=1.0, pos=[500, 325]) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("img/GAME/PlayerImage.png")
        self.image = pygame.image.load("img/GAME/PlayerImage.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0] / 2, pos[1] / 2)

        self.HEALTH = hp
        self.MAX_HEALTH = hp
        self.DAMAGE = dmg
        self.ATTACKSPEED = attspd
        self.delay = 0
        self.BULLETSPEED = bulspd

    def death(self, wave: int, kills: int, hashmap: Dict[str, int]):
        if hashmap["max_wave"] < wave:
            hashmap["max_wave"] = wave
        if hashmap["max_kills"] < kills:
            hashmap["max_kills"] = kills
        with open("data/highscore.json", "w") as f:
            json.dump(hashmap, f)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = ((180 / math.pi) * -math.atan2(rel_y, rel_x)) - 90
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.delay:
            self.delay -= 1

        if self.HEALTH > self.MAX_HEALTH:
            self.HEALTH = self.MAX_HEALTH

    def fire(self, bulgrp: pygame.sprite.Group):
        if self.delay:
            pass
        else:
            bulgrp.add(Bullet(self.BULLETSPEED, self.DAMAGE, self.rect.center))
            self.delay = self.ATTACKSPEED
        if self.delay < 0:
            self.delay = 0


# bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, spd: float, dmg: int, pos) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/GAME/BulletImage.png")
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.original_image = pygame.image.load("img/GAME/BulletImage.png")
        self.original_image = pygame.transform.scale(self.original_image, (10, 20))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.angle = 0
        self.position = pygame.Vector2(self.rect.center)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        angle = ((180 / math.pi) * -math.atan2(rel_y, rel_x)) - 90
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.DIRECTION = pygame.Vector2(rel_x, rel_y).normalize()

        self.SPEED = spd
        self.DAMAGE = dmg

    def update(self):
        self.position += self.DIRECTION * self.SPEED
        self.rect.center = self.position
