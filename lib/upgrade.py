import pygame

class upgrade_card(pygame.sprite.Sprite):
    def __init__(self, path:str, x:int, y:int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class str_upgrade_card(upgrade_card):
    def __init__(self, x:int, y:int):
        super().__init__("img/strenght_card.png", x, y)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def upgrd(self, player):
        player.DAMAGE += 1

class frr_upgrade_card(upgrade_card):
    def __init__(self, x:int, y:int):
        super().__init__("img/firerate_card.png", x, y)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def upgrd(self, player):
        player.ATTACKSPEED = player.ATTACKSPEED * 0.85

class bsp_upgrade_card(upgrade_card):
    def __init__(self, x:int, y:int):
        super().__init__("img/bulletspeed_card.png",x,y)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def upgrd(self, player):
        player.BULLETSPEED += 0.5