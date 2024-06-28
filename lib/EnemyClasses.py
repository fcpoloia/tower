import pygame
import pygame.locals

class Gibs(pygame.sprite.Sprite):
    def __init__(self, position: list[int,int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/gibs.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (position[0],position[1])

class Dummy(pygame.sprite.Sprite):
    def __init__(self, position: list[int, int], speed: float, target, health: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1])

        self.TRGT = target
        self.SPD = speed
        self.HP = health
        self.dir_vector = pygame.Vector2(
            self.TRGT[0] - self.rect.centerx, self.TRGT[1] - self.rect.centery
        ).normalize()
        self.position = pygame.Vector2(self.rect.center)

    def update(self):
        self.position += self.dir_vector * self.SPD
        self.rect.center = self.position

    def die(self,gibgroup):
        gibgroup.add(Gibs([self.rect.centerx,self.rect.centery]))


class Conscript(Dummy):
    def __init__(self, position: list[int], target, mid: int):
        super().__init__(position, 1, target, 1)
        self.image = pygame.image.load("img/conscript.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        if position[0] < mid:
            self.image = pygame.transform.flip(self.image, True, False)


class Tank(Dummy):
    def __init__(self, position: list[int], target, mid: int):
        super().__init__(position, 0.3, target, 5)
        self.image = pygame.image.load("img/Tank.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        if position[0] < mid:
            self.image = pygame.transform.flip(self.image, True, False)


class Runner(Dummy):
    def __init__(self, position: list[int], target, mid: int):
        super().__init__(position, 3, target, 1)
        self.image = pygame.image.load("img/Runner.png")
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        if position[0] < mid:
            self.image = pygame.transform.flip(self.image, True, False)
