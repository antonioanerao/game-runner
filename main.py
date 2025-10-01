from sys import exit
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
custom_font = pygame.font.Font('./font/Pixeltype.ttf', size=50)

game_active = True

snail_speed = 4
sky_surf = pygame.image.load('./graphics/Sky.png').convert()
ground_surf = pygame.image.load('./graphics/ground.png').convert()

title_surf = custom_font.render('Runner', False, (64, 64, 64))
title_rect = title_surf.get_rect(center=(400, 50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rec = snail_surf.get_rect(midbottom=(800, 300))

# Player
player_surf = pygame.image.load('./graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                player_gravity = -12.5
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                player_gravity = -12.5

        if game_active is False and event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            snail_rec.left = 800
            game_active = True
            snail_speed = 4
            print("Game Restarted")

    if game_active:
        speed_surf = custom_font.render('Speed: ' + str(round(snail_speed - 3, 2)), False, 'Black')
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        pygame.draw.rect(screen, '#C0E8EC', title_rect)
        pygame.draw.rect(screen, '#C0E8EC', title_rect, 10)
        screen.blit(title_surf, title_rect)

        screen.blit(speed_surf, (340, 70))

        snail_rec.x -= snail_speed
        if snail_rec.right <= 0:
            snail_rec.left = 800
            snail_speed += 0.5
        screen.blit(snail_surf, snail_rec)

        # Player
        player_gravity += 0.5
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        screen.blit(player_surf, player_rect)

        if player_rect.colliderect(snail_rec):
            game_active = False
            print("Game Over")

    else:
        game_over_surf = pygame.image.load('./graphics/game_over1.png').convert_alpha()
        game_over_surf = pygame.transform.scale(game_over_surf, (800, 400))
        screen.blit(game_over_surf, (0, 0))
        restart_info = custom_font.render("Press 1 to Restart", False, 'Yellow')
        screen.blit(restart_info, (250, 20))
        if snail_speed == 4:
            score_info = custom_font.render('Speed Record: 1. You suck', False, 'Yellow')
            screen.blit(score_info, (200, 350))
        else:
            score_info = custom_font.render('Speed Record: ' + str(round(snail_speed - 3, 2)), False, 'Yellow')
            screen.blit(score_info, (280, 350))

    pygame.display.update()
    clock.tick(60)
