from sys import exit
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font_test = pygame.font.Font('./font/Pixeltype.ttf', size=50)

sky_surface = pygame.image.load('./graphics/Sky.png')
ground_surface = pygame.image.load('./graphics/ground.png')
text_surface = font_test.render('Runner', False, 'Black')

snail_surface = pygame.image.load('graphics/snail/snail1.png')
snail_x_position = 800
snail_speed = 4

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (350, 50))
    snail_x_position -= snail_speed
    if snail_x_position < -100:
        snail_x_position = 800
        snail_speed += 1
    screen.blit(snail_surface, (snail_x_position, 265))

    pygame.display.update()
    clock.tick(60)
