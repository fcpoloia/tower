import pygame
from lib import PlayerClasses, EnemyClasses

pygame.init()

#constants
WIDTH : int = 1000
HEIGHT : int = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
running = True
clock = pygame.time.Clock()

#initialize player
player = PlayerClasses.Player(1,1,1.0,1.0,[WIDTH,HEIGHT])
player_group = pygame.sprite.Group()
player_group.add(player)
bullet_group = pygame.sprite.Group()

#dummy enemy for testing
enemy_group = pygame.sprite.Group()
enemy_group.add(EnemyClasses.Dummy([100,50],1,(WIDTH/2,HEIGHT/2)))

while running:
    #input map
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player.fire(bullet_group)

    #Update & draw
    screen.fill((100, 100, 100))

    player.update()
    player_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    enemy_group.update()
    enemy_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()