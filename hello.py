import math
import pygame
from random import randint

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
game_active = False
start_time = 0
score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()


# Obstacles
snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
fly_surf = pygame.image.load("graphics/fly/fly1.png").convert_alpha()

obstacle_rect_list = []


# Player
player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, GROUND_X))

player_stand_surf = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT -180))

player_gravity = 0

def isJumping(rect: pygame.Rect):
    return rect.midbottom[1] < GROUND_X

def isOnGround():
    return player_rect.bottom >= GROUND_X

def isJumping():
    return player_rect.bottom < GROUND_X

def obstacle_movement(obstacle_list):
    if not obstacle_list:
        return []
    for obstacle_rect in obstacle_list:
        obstacle_rect.x -= randint(2, 5)

        if obstacle_rect.bottom == GROUND_X:
            screen.blit(snail_surf, obstacle_rect)
        else:
            screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

    return obstacle_list

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit();

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and isOnGround():
                player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and isOnGround():
                    player_gravity = -20
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(800, 1100), GROUND_X)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(800, 1100), GROUND_X - player_surf.get_height() - 10)))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_rect.x = 80
                game_active = True
                start_time = pygame.time.get_ticks()


        if event.type == pygame.KEYUP:
            pass
    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_X))
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, width=200)
        # screen.blit(score_surf, score_rect)
        score = display_score()


        # player_rect.left += 1
        # snail_rect.x -= 4

        # if snail_rect.right < 0 - snail_surf.get_width():
        #     snail_rect.left = SCREEN_WIDTH + snail_surf.get_width()


        player_gravity += 1
        player_rect.y += player_gravity

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)


        if isOnGround():
            player_rect.bottom = GROUND_X

        # if snail_rect.colliderect(player_rect):
        #     game_active = False
        
        # screen.blit(snail_surf, snail_rect)
        screen.blit(player_surf, player_rect)

    if not game_active:
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
    

