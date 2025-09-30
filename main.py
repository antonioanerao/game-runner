from sys import exit
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font_test = pygame.font.Font('./font/Pixeltype.ttf', size=50)

snail_speed = 4
sky_surf = pygame.image.load('./graphics/Sky.png').convert()
ground_surf = pygame.image.load('./graphics/ground.png').convert()

title_surf = font_test.render('Runner', False, (64, 64, 64))
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
                player_gravity = -12
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                player_gravity = -12

    speed_surf = font_test.render('Speed: ' + str(round(snail_speed, 2)), False, 'Black')
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))

    pygame.draw.rect(screen, '#C0E8EC', title_rect)
    pygame.draw.rect(screen, '#C0E8EC', title_rect, 10)
    screen.blit(title_surf, title_rect)

    screen.blit(speed_surf, (340, 70))

    snail_rec.x -= 4
    if snail_rec.right <= 0:
        snail_rec.left = 800
        snail_speed += 0.1
    screen.blit(snail_surf, snail_rec)

    # Player
    player_gravity += 0.5
    player_rect.y += player_gravity
    if player_rect.bottom >= 300:
        player_rect.bottom = 300

    if player_rect.colliderect(snail_rec):
        pygame.quit()
        exit()

    screen.blit(player_surf, player_rect)

    pygame.display.update()
    clock.tick(60)
