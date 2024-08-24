import pygame
from lib import PlayerClasses, EnemyClasses, upgrade, HUD
import random
import sys
import json

pygame.init()
pygame.font.init()

# constants
WIDTH: int = 1000
HEIGHT: int = 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
running = True
state = "menu"
clock = pygame.time.Clock()

# initialize player
player = PlayerClasses.Player(10, 1, 100, 1.0, [WIDTH, HEIGHT])
player_group = pygame.sprite.Group()
player_group.add(player)
bullet_group = pygame.sprite.Group()
with open("data/highscore.json") as HS_file:
    HSHM = json.load(HS_file)

# Enemies
pos_enemies = [EnemyClasses.Conscript, EnemyClasses.Tank, EnemyClasses.Runner]
enemy_group = pygame.sprite.Group()
sides = ["L", "R", "U", "D"]
gibgroup = pygame.sprite.Group()

wave = 0
kills = 0
# Cards
L:float = WIDTH/5
M:float = WIDTH/2
R:float = WIDTH-WIDTH/5
sequance = [L,M,R]
pos_cards = [upgrade.str_upgrade_card,upgrade.frr_upgrade_card,upgrade.bsp_upgrade_card,upgrade.heal_card,upgrade.max_health_card]
cards = pygame.sprite.Group()

# HUD
font = pygame.font.SysFont("Arial", 30)
wave_display_surf = font.render("Wave: " + str(wave), True, (255,255,255))
kills_display_surf = font.render("Kills: " + str(kills), True, (255,255,255))
S_MaxWave = HSHM["max_wave"]
DS_MaxWave = font.render("Highest round reached: " + str(S_MaxWave), True, (255,255,255))
S_MaxKills = HSHM["max_kills"]
DS_MaxKills = font.render("Most kills in a game: " + str(S_MaxKills), True, (255,255,255))
Stat_DS_group = [DS_MaxWave,DS_MaxKills]

Play_Button = HUD.HUDButton_Play(50,100)
Stats_Button = HUD.HUDButton_Stats(50,200)
Quit_Button = HUD.HUDButton_Quit(50,300)
Back_Button = HUD.HUDButton_Back(50,50)
button_group = pygame.sprite.Group()
button_group.add(Play_Button,Stats_Button,Quit_Button)
bbg = pygame.sprite.Group()
bbg.add(Back_Button)

# Main loop
while True:
    # Menu loop
    while state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                M_POS = event.pos
                buttons = button_group.sprites()
                clicked_button = [c for c in buttons if c.rect.collidepoint(M_POS)]
                if clicked_button:
                    state = clicked_button[0].act()            

        screen.fill((80, 80, 80))

        button_group.update()
        button_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    while state == "stats":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                M_POS = event.pos
                buttons = bbg.sprites()
                clicked_button = [c for c in buttons if c.rect.collidepoint(M_POS)]
                if clicked_button:
                    state = clicked_button[0].act()
             

        screen.fill((80,80,80))

        for i in range(len(Stat_DS_group)):
            screen.blit(Stat_DS_group[i],(50,HEIGHT-500+i*50))

        bbg.update()
        bbg.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    while state == "dead":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                M_POS = event.pos
                buttons = bbg.sprites()
                clicked_button = [c for c in buttons if c.rect.collidepoint(M_POS)]
                if clicked_button:
                    state = clicked_button[0].act()

        wave = 0
        kills = 0
 
        bbg.update()
        bbg.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    # Fighting loop
    while state == "fight":
        # input map
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            keys = pygame.key.get_pressed()
            if any(keys):
                player.fire(bullet_group)
        # collision detection
        player_hit = pygame.sprite.spritecollide(player, enemy_group, False)
        for i in player_hit:
            player.HEALTH -= 1
            enemy_group.remove(i)
            if player.HEALTH <= 0:
                player.death(wave, kills, HSHM)
                state = "dead"
   
        bullet_hits = pygame.sprite.groupcollide(bullet_group, enemy_group, False, False)
        for bullet in bullet_hits:
            for enemy in bullet_hits[bullet]:
                enemy.HP -= bullet.DAMAGE
            bullet_group.remove(bullet)

        # check for enemies to kill off
        if enemy_group.sprites():
            for i in enemy_group.sprites()[:]:
                if i.HP <= 0:
                    kills += 1
                    kills_display_surf = font.render("Kills: " + str(kills), True, (255,255,255))
                    i.die(gibgroup)
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

        gibgroup.draw(screen)

        player.update()
        player_group.draw(screen)

        bullet_group.update()
        bullet_group.draw(screen)

        enemy_group.update()
        enemy_group.draw(screen)

        screen.blit(wave_display_surf, (WIDTH/2,HEIGHT/2+50))
        screen.blit(kills_display_surf,(WIDTH/2,HEIGHT/2+100))

        HUD.draw_progress_bar(int(WIDTH/2-40),int(HEIGHT/2-30),80,15,screen,player.delay,player.ATTACKSPEED,(80,165,80),(80,255,80))
        HUD.draw_progress_bar(int(WIDTH/2-40),int(HEIGHT/2-45),80,15,screen,player.HEALTH,player.MAX_HEALTH,(165,80,80),(255,80,80))

        pygame.display.flip()
        clock.tick(60)

    # buffing loop
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
    
    if state == "quit":
        sys.exit()

pygame.quit()
