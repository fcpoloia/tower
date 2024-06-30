import pygame

class HUDButton(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int):
        super().__init__()
        self.image = pygame.Surface((200,50))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


class HUDButton_Play(HUDButton):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)
        self.image = pygame.image.load("img/HUD/play_button.png")
        self.image = pygame.transform.scale(self.image,(300,75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def act(self):
        return "fight"
