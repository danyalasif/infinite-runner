import random
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_X = 300
game_active = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = pixel_font.render("My Game", False, (64, 64, 64))
score_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, 50))

game_over_surf = pixel_font.render("Game Over - Press 'Space' to restart", False, (64, 64, 64))
game_over_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (800, GROUND_X))

player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, GROUND_X))

player_gravity = 0

def isJumping(rect: pygame.Rect):
    return rect.midbottom[1] < GROUND_X

def isOnGround():
    return player_rect.bottom >= GROUND_X

def isJumping():
    return player_rect.bottom < GROUND_X

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
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.x = 800
                player_rect.x = 80
                game_active = True


        if event.type == pygame.KEYUP:
            pass
    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_X))
        pygame.draw.rect(screen, "#c0e8ec", score_rect)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, width=200)
        screen.blit(score_surf, score_rect)


        # player_rect.left += 1
        snail_rect.x -= 4

        if snail_rect.right < 0 - snail_surf.get_width():
            snail_rect.left = SCREEN_WIDTH + snail_surf.get_width()


        player_gravity += 1
        player_rect.y += player_gravity


        if isOnGround():
            player_rect.bottom = GROUND_X

        if snail_rect.colliderect(player_rect):
            game_active = False
        
        screen.blit(snail_surf, snail_rect)
        screen.blit(player_surf, player_rect)

    if not game_active:
        screen.fill("red")
        screen.blit(game_over_surf, game_over_rect)

    pygame.display.update()
    clock.tick(60)
    

