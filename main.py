import math
import pygame
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_anim_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_anim_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0
        self.gravity_force = 1
        self.jump_force = -20

    
    def player_input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE] or mouse[0]) and self.rect.bottom >= 300:
            self.gravity = self.jump_force 

    def apply_gravity(self):
        self.gravity += self.gravity_force
        self.rect.y += self.gravity
        if self.isOnGround():
            self.rect.bottom = 300

    def isJumping(self):
        return self.rect.midbottom[1] < GROUND_X

    def isOnGround(self):
        return self.rect.bottom >= 300

    def animate(self):
        if self.isOnGround():
            self.player_anim_index += 0.1
            if self.player_anim_index >= len(self.player_walk):
                self.player_anim_index = 0
            self.image = self.player_walk[int(self.player_anim_index)]
        else:
            self.image = self.player_jump


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()


def display_score():
    current_time = math.floor((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = pixel_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def player_animation():
    global player_surf, player_index

    if isOnGround():
        # show walk
        player_index += 0.1
        if (player_index >= len(player_walk)):
            player_index = 0
        player_surf = player_walk[int(player_index)]
    else:
        #show walk anim
        player_surf = player_jump
    # play walking animation if the player is on floor

    # show jump animation if player is jumping
    pass

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

pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()


# Obstacles
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_anim = [snail_frame_1, snail_frame_2]
snail_anim_index = 0
snail_surf = snail_anim[snail_anim_index]

fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_anim = [fly_frame_1, fly_frame_2]
fly_anim_index = 0
fly_surf = fly_anim[fly_anim_index]

obstacle_rect_list = []


# Player
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

player_surf = player_walk[player_index]
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

def check_collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True



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
            
            if event.type == snail_anim_timer:
                if snail_anim_index == 0: snail_anim_index = 1
                else: snail_anim_index = 0
                snail_surf = snail_anim[snail_anim_index]
            if event.type == fly_anim_timer:
                if fly_anim_index == 0: fly_anim_index = 1
                else: fly_anim_index = 0
                fly_surf = fly_anim[fly_anim_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()


        if event.type == pygame.KEYUP:
            pass
    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_X))
        score = display_score()
        player_animation()
        screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()

        player_gravity += 1
        player_rect.y += player_gravity

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)


        # Collisions
        if isOnGround():
            player_rect.bottom = GROUND_X

        game_active = check_collisions(player_rect, obstacle_rect_list)

    if not game_active:
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, GROUND_X)
        player_gravity = 0

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
    

