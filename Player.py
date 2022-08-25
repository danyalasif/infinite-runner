import pygame

from Bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_anim_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_anim_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.gravity_force = 1
        self.jump_force = -20

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

    
    def player_input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE]) and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = self.jump_force 

    def apply_gravity(self):
        self.gravity += self.gravity_force
        self.rect.y += self.gravity
        if self.isOnGround():
            self.rect.bottom = 300

    def isJumping(self):
        return self.rect.midbottom[1] < 300

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
