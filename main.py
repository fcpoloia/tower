import pygame
from lib import PlayerClasses, EnemyClasses, upgrade, HUD
import random
import sys

pygame.init()
pygame.font.init()

# constants
WIDTH: int = 1000
HEIGHT: int = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
running = True
state = "fight"
clock = pygame.time.Clock()

# initialize player
player = PlayerClasses.Player(1, 1, 100, 1.0, [WIDTH, HEIGHT])
player_group = pygame.sprite.Group()
player_group.add(player)
bullet_group = pygame.sprite.Group()

# Enemies
pos_enemies = [EnemyClasses.Conscript, EnemyClasses.Tank, EnemyClasses.Runner]
enemy_group = pygame.sprite.Group()
sides = ["L", "R", "U", "D"]

# Cards
wave = -1
L:int = 150
M:int = 500
R:int = 850
sequance = [L,M,R]
pos_cards = [upgrade.str_upgrade_card,upgrade.frr_upgrade_card,upgrade.bsp_upgrade_card]
cards = pygame.sprite.Group()

# HUD
font = pygame.font.SysFont("Arial", 30)
wave_display_surf = font.render("Wave: " + str(wave), True, (255,255,255))

while state == "fight":
    # input map
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.fire(bullet_group)

    # collision detection
    player_hit = pygame.sprite.spritecollide(player, enemy_group, False)
    for i in player_hit:
        player.HEALTH -= 1
        enemy_group.remove(i)

    bullet_hits = pygame.sprite.groupcollide(bullet_group, enemy_group, False, False)
    for bullet in bullet_hits:
        for enemy in bullet_hits[bullet]:
            enemy.HP -= bullet.DAMAGE
        bullet_group.remove(bullet)

    # check for enemies to kill off
    if enemy_group.sprites():
        for i in enemy_group.sprites():
            if i.HP <= 0:
                enemy_group.remove(i)
    # spawn new enemy
    else:
        for i in range(wave+1):
            enemy = random.choice(pos_enemies)
            side = random.choice(sides)
            if side == "L":
                enemy_group.add(
                    enemy(
                        [50, random.randint(0, HEIGHT)], (WIDTH / 2, HEIGHT / 2), WIDTH / 2
                    )
                )
            if side == "R":
                enemy_group.add(
                    enemy(
                        [950, random.randint(0, HEIGHT)], (WIDTH / 2, HEIGHT / 2), WIDTH / 2
                    )
                )
            if side == "U":
                enemy_group.add(
                    enemy(
                        [random.randint(0, WIDTH), 50], (WIDTH / 2, HEIGHT / 2), WIDTH / 2
                    )
                )
            if side == "D":
                enemy_group.add(
                    enemy(
                        [random.randint(0, WIDTH), 650], (WIDTH / 2, HEIGHT / 2), WIDTH / 2
                    )
                )
        wave += 1
        wave_display_surf = font.render("Wave: "+str(wave), True, (255,255,255))
        if wave > 1:
            state = "buff"
            for i in range(3):
                cards.add(random.choice(pos_cards)(sequance[i],300))

    # check for bullets out of bounds
    for bullet in bullet_group.sprites():
        if (
            bullet.rect.centerx < 0
            or bullet.rect.centerx > WIDTH
            or bullet.rect.centery < 0
            or bullet.rect.centery > HEIGHT
        ):
            bullet_group.remove(bullet)

    # Update & draw
    screen.fill((80, 80, 80))

    player.update()
    player_group.draw(screen)

    bullet_group.update()
    bullet_group.draw(screen)

    enemy_group.update()
    enemy_group.draw(screen)

    screen.blit(wave_display_surf, (WIDTH/2,HEIGHT/2+50))

    pygame.display.flip()
    clock.tick(60)

    while state == "buff":
        
        #input map
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                M_POS = event.pos
                clicked_card = [c for c in cards if c.rect.collidepoint(M_POS)]
                if clicked_card:
                    clicked_card[0].upgrd(player)
                    state = "fight"
 
        cards.update()
        cards.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
