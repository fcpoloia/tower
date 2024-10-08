import pygame


def draw_progress_bar(
    x: int, y: int, width: int, height: int, screen, current, maximum, bg, fg
):
    pygame.draw.rect(screen, bg, (x, y, width, height))
    pygame.draw.rect(screen, fg, (x, y, current / maximum * width, height))


class HUDButton(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, path: str):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (300, 75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class HUDButton_Play(HUDButton):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "img/HUD/play_button.png")

    def act(self):
        return "fight"


class HUDButton_Stats(HUDButton):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "img/HUD/stats_button.png")

    def act(self):
        return "stats"


class HUDButton_Quit(HUDButton):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "img/HUD/quit_button.png")

    def act(self):
        return "quit"


class HUDButton_Back(HUDButton):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "img/HUD/back_button.png")
        self.image = pygame.transform.scale(self.image, (150, 70))

    def act(self):
        return "menu"
