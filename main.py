import sys
import pygame
from random import randint, choice
import os

user_name = input("What is your name? ")


def load_images(path, prefix, count, scale=2):
    """Carrega uma sequência de imagens numeradas de uma pasta.

    Args:
        path (str): pasta onde estão as imagens.
        prefix (str): prefixo do nome do arquivo (ex: "walk" para walk1.png, walk2.png...).
        count (int): número de imagens a carregar.
        scale (int): fator de escala (2 = scale2x).

    Returns:
        list: lista de Surfaces já carregadas e escaladas.
    """
    images = []
    for i in range(1, count + 1):
        img_path = os.path.join(path, f"{prefix}{i}.png")
        image = pygame.image.load(img_path).convert_alpha()
        if scale == 2:
            image = pygame.transform.scale2x(image)
        elif scale != 1:
            w, h = image.get_size()
            image = pygame.transform.scale(image, (w * scale, h * scale))
        images.append(image)
    return images


def resource_path(relative_path):
    """Acha o caminho para recursos no dev e no executável"""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_index = 0
        self.player_jumping_index = 0
        self.gravity = 0
        self.player_walk = load_images('./graphics/Girl/walking', 'walk', 12, scale=1)
        self.player_jumping = load_images('./graphics/Girl/jumping', 'jumping', 4, scale=1)

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.player_jump = self.player_jumping[self.player_jumping_index]

        self.jump_sound = pygame.mixer.Sound('./audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -16
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_animation(self):
        if self.rect.bottom < 300:
            self.player_jumping_index += 0.15
            if self.player_jumping_index >= len(self.player_jumping):
                self.player_jumping_index = len(self.player_jumping) - 1
            self.image = self.player_jumping[int(self.player_jumping_index)]
        else:
            self.player_index += 0.25
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('./graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('./graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('./graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -50:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = custom_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def colission_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False

    return True


pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font_path = resource_path('./font/Pixeltype.ttf')
custom_font = pygame.font.Font(font_path, size=50)
start_time = 0
score = 0

# Groups

# Player Group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacle Group
obstacle_group = pygame.sprite.Group()

game_active = True
run_count = 0

sky_surf = pygame.image.load('./graphics/Sky.png').convert()
ground_surf = pygame.image.load('./graphics/ground.png').convert()

# Game Over
game_over_surf = pygame.image.load('./graphics/game_over1.png').convert_alpha()
game_over_surf = pygame.transform.scale(game_over_surf, (800, 400))
restart_info = custom_font.render("Press 1 to Restart", False, 'Yellow')

# Game Start
game_start_surf = pygame.image.load('./graphics/game_start.png').convert_alpha()
game_start_surf = pygame.transform.scale(game_start_surf, (800, 400))
start_info = custom_font.render("Press 1 to START", False, 'Yellow')
start_info_rect = start_info.get_rect(midtop=(400, 10))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if run_count == 0:
            screen.blit(game_start_surf, (0, 0))
            screen.blit(start_info, (start_info_rect))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                run_count = 1

        if event.type == obstacle_timer and game_active and run_count == 1:
            obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active and run_count == 1:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = colission_sprite()

    if game_active is False:
        screen.blit(game_over_surf, (0, 0))
        screen.blit(restart_info, (250, 20))

        player_name = custom_font.render('Hello ' + str(user_name), False, 'Yellow')
        score_info = custom_font.render('Your Score: ' + str(score), False, 'Yellow')
        screen.blit(player_name, (280, 340))
        screen.blit(score_info, (280, 370))

    pygame.display.update()
    clock.tick(60)
