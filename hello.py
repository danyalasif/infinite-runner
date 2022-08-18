import random
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render("My Game", False, (64, 64, 64))
score_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, 50))

snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (800, 300))

player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))

GRAVITY = 3

def isJumping(rect: pygame.Rect):
    return rect.midbottom[1] < 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit();

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not isJumping(player_rect):
                    player_rect.y -= 100


        if event.type == pygame.KEYUP:
            pass

    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect, width=200)
    screen.blit(score_surf, score_rect)


    # player_rect.left += 1
    snail_rect.x -= 4

    if snail_rect.right < 0 - snail_surf.get_width():
        snail_rect.left = SCREEN_WIDTH + snail_surf.get_width()

    if isJumping(player_rect):
        player_rect.y += GRAVITY
    
    screen.blit(snail_surf, snail_rect)
    screen.blit(player_surf, player_rect)

    # keys= pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]

    # if player_rect.colliderect(snail_rect):


    pygame.display.update()
    clock.tick(60)
    

