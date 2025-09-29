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
text_surf = font_test.render('Runner', False, 'Black')

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rec = snail_surf.get_rect(midbottom=(800, 300))


player_surf = pygame.image.load('./graphics/Player/player_walk_1.png').convert_alpha()
player_rec = player_surf.get_rect(midbottom=(80, 300))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    speed_surf = font_test.render('Speed: ' + str(round(snail_speed, 2)), False, 'Black')
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    screen.blit(text_surf, (350, 50))
    screen.blit(speed_surf, (350, 80))

    snail_rec.x -= 4
    if snail_rec.right <= 0:
        snail_rec.left = 800
        snail_speed += 0.1
    screen.blit(snail_surf, snail_rec)
    screen.blit(player_surf, player_rec)

    if player_rec.colliderect(snail_rec):
        print("collision")

    pygame.display.update()
    clock.tick(60)
