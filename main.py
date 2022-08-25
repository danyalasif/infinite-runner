import math
import pygame
from random import choice
from Bullet import Bullet
from Player import Player
from Obstacle import Obstacle


def display_score():
    current_time = math.floor((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = pixel_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_X = 300
game_active = True
start_time = 0
score = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.sprite.GroupSingle()
player.add(Player())

bullet_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
background_music = pygame.mixer.Sound('audio/music.wav')
# background_music.play(loops = -1)

def check_sprite_collision():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

def check_bullet_collision():
    for bullet in bullet_group:
        for enemy in obstacle_group:
            if bullet.rect.colliderect(enemy.rect):
                enemy.kill()
                bullet.kill()

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

snail_anim_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_anim_timer, 500)

fly_anim_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_anim_timer, 300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
                        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                print("Bullet added")
                bullet_group.add(Bullet())
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()


    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_X))
        score = display_score()
        
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        bullet_group.draw(screen)
        bullet_group.update()
        check_bullet_collision()
        game_active = check_sprite_collision()

    if not game_active:
        player_gravity = 0
        player_stand_surf = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
        player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
        player_stand_rect = player_stand_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT -180))
        score_surf = pixel_font.render(f'Your score: {score}', False, (100, 64, 64))
        score_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, 100))
        game_over_surf = pixel_font.render("Game Over", False, (100, 64, 64))
        game_over_rect = game_over_surf.get_rect(center = (SCREEN_WIDTH / 2, 50))
        start_again_surf = pixel_font.render("Press 'Space' to restart", False, (100, 64, 64))
        start_again_rect = start_again_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT -40))
        screen.fill("#c0e8ec")
        screen.blit(game_over_surf, game_over_rect)
        screen.blit(score_surf, score_rect)
        
        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(start_again_surf, start_again_rect)

    pygame.display.update()
    clock.tick(60)
    

