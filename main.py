import pygame
from lib import PlayerClasses, EnemyClasses
import random

pygame.init()

# constants
WIDTH: int = 1000
HEIGHT: int = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
running = True
clock = pygame.time.Clock()

# initialize player
player = PlayerClasses.Player(1, 1, 100, 1.0, [WIDTH, HEIGHT])
player_group = pygame.sprite.Group()
player_group.add(player)
bullet_group = pygame.sprite.Group()

# Enemies
pos_enemies = [EnemyClasses.Conscript, EnemyClasses.Tank, EnemyClasses.Runner]
enemy_group = pygame.sprite.Group()
enemy_group.add(EnemyClasses.Conscript([100, 50], (WIDTH // 2, HEIGHT // 2), WIDTH / 2))
sides = ["L", "R", "U", "D"]

while running:
    # input map
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
