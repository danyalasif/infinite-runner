import math
import pygame
from random import randint, choice

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

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
            self.move_speed = randint(3, 6)
        else:
            snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
            self.move_speed = randint(1, 4)


        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animate(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate()
        self.rect.x -= self.move_speed
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

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

obstacle_group = pygame.sprite.Group()

pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

pixel_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()


def isJumping(rect: pygame.Rect):
    return rect.midbottom[1] < GROUND_X


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
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
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
        
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()


        # game_active = check_collisions(player_rect, obstacle_rect_list)

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
    

