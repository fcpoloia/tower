import pygame

class upgrade_card(pygame.sprite.Sprite):
    def __init__(self, path:str, x:int, y:int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class max_health_card(upgrade_card):
    def __init__(self, x:int, y:int):
        super().__init__("img/HUD/maxhealth_card.png",x,y)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def upgrd(self, player):
        player.MAX_HEALTH += 1

class heal_card(upgrade_card):
    def __init__(self, x:int, y:int):
        super().__init__("img/HUD/heal_card.png", x, y)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def upgrd(self, player):
        player.HEALTH += 1

class str_upgrade_card(upgrade_card):
    def __init__(self, x:int, y:int):
        super().__init__("img/HUD/strenght_card.png", x, y)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def upgrd(self, player):
        player.DAMAGE += 1

class frr_upgrade_card(upgrade_card):
    def __init__(self, x:int, y:int):
        super().__init__("img/HUD/firerate_card.png", x, y)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def upgrd(self, player):
        player.ATTACKSPEED = player.ATTACKSPEED * 0.85

class bsp_upgrade_card(upgrade_card):
    def __init__(self, x:int, y:int):
        super().__init__("img/HUD/bulletspeed_card.png",x,y)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def upgrd(self, player):
        player.BULLETSPEED += 0.5
