## Infinite Runner Python Project

I am following Clear Code's tutorial at https://www.youtube.com/watch?v=AY9MnQ4x3zk as the basis of this project


### Adding images on screen
Use surfaces to load images:
`player_stand_surf = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()`

Use rectangles around these surfaces to control their position and dimensions:
`player_stand_rect = player_stand_surf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT -180))`

And finally add them to the pygame screen with:
`screen.blit(player_surf, player_rect)`

> Screen is a pygame variable which defines the width/height of playable area and handles drawing on it
`screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))`

### Collision
Check collision between two rectangles with:
`rect_1.colliderect(rect_2):`



### Technologies
🐍 Python
+ Pygame