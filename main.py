#colour
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (200,255,255)

from pygame import *
import pygame.font
import random

# Window settings
width = 600
height = 500
window = display.set_mode((width, height))
window.fill(BLACK)
display.set_caption("Ping and Pong")

# Set colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Set fonts
pygame.font.init()
font = pygame.font.Font(None, 35)
left_win = font.render('BLUE PLAYER LOSE!', True, (180, 0, 0))
right_win = font.render('RED PLAYER LOSE!', True, (180, 0, 0))

# Parent class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player class
class Player(GameSprite):
    def update_left(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < height - 150: #height is win_height
            self.rect.y += self.speed
    def update_right(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < height - 150:
            self.rect.y += self.speed

# Create sprites
paddle1 = Player("paddle1.png", 20, height - 100, 40, 160, 10)
paddle2 = Player("paddle2.png", 520, height - 100, 40, 160, 10)
ball = GameSprite("ball.png", 330, 200, 50, 50, 50)

# Set game loop
game = True
finish = False
clock = time.Clock()
FPS = 60

blueScore = 0
redScore = 0

font_score = pygame.font.Font(None, 18)
blueBoard = font_score.render('BLUE: ' + str(blueScore), True, WHITE)
redBoard = font_score.render('RED: ' + str(redScore), True, WHITE)

initial_direction = random.choice([-1, 1]) 
speed_x = 3
speed_y = 3

while game:
    # Events
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:
        window.fill(BLACK)
        paddle1.update_left()
        paddle2.update_right()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        window.blit(blueBoard, (width - 80, 10))
        window.blit(redBoard, (10, 10))

        #Czech collision
        if sprite.collide_rect(paddle1, ball):
            redScore += 1
            redBoard = font_score.render('RED:' + str(redScore), True, WHITE)
            speed_x *= -1
            speed_y *= 1

        if sprite.collide_rect(paddle2, ball):
            blueScore += 1
            blueBoard = font_score.render('BLUE:' + str(blueScore), True, WHITE)
            speed_x *= -1
            speed_y *= 1

        #ball bounces when hit border
        if ball.rect.y >= height - 50 or ball.rect.y <= 10:
            speed_y *= -1

        #if ball flies behind paddle1, display loss for player left
        if ball.rect.x < 0:
            finish = False
            window.blit(right_win, (200, 200))

        #if ball flies behind paddle2, display loss for player right
        if ball.rect.x > width:
            finish = False
            window.blit(left_win, (200, 200))

        paddle1.reset()
        paddle2.reset()
        ball.reset()

    else:
        time.delay(3000)
        finish = False
        score = 0
        missed = 0
        
    # Update
    display.update()
    clock.tick(FPS)