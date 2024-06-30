import pygame

class HUDButton(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((200,50))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def act(self):
        print("CLICK")
