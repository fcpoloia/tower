import pygame
import json
import math
from typing import Dict
import lib.HUD as HUD

###-------------------------------CLASSES-------------------------------###


# abilities
class AbilityBase(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, path: str, cd: int, level: int, screen) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.LEVEL = level
        self.CD = cd
        self.CD_current = cd
        self.screen = screen

    def level_up(self):
        self.LEVEL += 1
        self.power = 1 / self.LEVEL

    def update(self) -> None:
        if self.CD_current > 0:
            self.CD_current -= 1
        HUD.draw_progress_bar(
            self.rect.topleft[0],
            self.rect.topleft[1] - 10,
            50,
            10,
            self.screen,
            self.CD_current,
            self.CD,
            "blue",
            "red",
        )

    def effect(self, enemy_group, player):
        print("ABILITY BASE.")


class SlowDown(AbilityBase):
    def __init__(self, x: int, y: int, cd: int, level: int, screen) -> None:
        super().__init__(x, y, "img/GAME/SlowIcon.png", cd, level, screen)
        self.power = 1 / self.LEVEL
        if self.power >= 1:
            self.power = 0.85

    def effect(self, enemy_group, player):
        if self.CD_current <= 0:
            enemies = enemy_group.sprites()
            for i in enemies:
                i.SPD = i.SPD * self.power
            self.CD_current = self.CD


class Nuke(AbilityBase):
    def __init__(self, x: int, y: int, cd: int, level: int, screen) -> None:
        super().__init__(x, y, "img/GAME/NukeIcon.png", cd, level, screen)
        self.power = level

    def effect(self, enemy_group, player):
        if self.CD_current <= 0:
            enemies = enemy_group.sprites()
            for i in enemies:
                i.HP -= self.power
        self.CD_current = self.CD


class Heal(AbilityBase):
    def __init__(self, x: int, y: int, cd: int, level: int, screen) -> None:
        super().__init__(x, y, "img/GAME/HealIcon.png", cd, level, screen)
        self.power = level * 0.10

    def effect(self, enemy_group, player):
        if self.CD_current <= 0:
            to_heal = (player.MAX_HEALTH - player.HEALTH) * self.power
            to_heal = math.ceil(to_heal)
            player.HEALTH += to_heal
            if player.MAX_HEALTH < player.HEALTH:
                player.HEALTH = player.MAX_HEALTH
        self.CD_current = self.CD


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
