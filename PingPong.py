import pygame
from pygame import *

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Пинг-Понг')
back = (200, 255, 255)
window.fill(back)
mixer.init()

hit = mixer.Sound('hit.ogg')
firee = mixer.Sound('lose.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=60, size_y=60):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_l(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed
            
    def update_r(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed


class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, speed_x, speed_y, size_x=50, size_y=50):
        super().__init__(player_image, player_x, player_y, player_speed, size_x, size_y)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y < 0 or self.rect.y > win_height - self.rect.height:
            self.speed_y *= -1

play1 = Player('racket.png', 30, 200, 5, 20, 100)
play2 = Player('racket.png', 650, 200, 5, 20, 100)
ball = Ball('ball.png', 300, 200, 5, 3, 3, 50, 50)


game = True
finish = False
clock = time.Clock()
FPS = 60
font.init()

font1 = font.Font(None, 35)
lose1 = font1.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font1.render('PLAYER 2 LOSE!', True, (180, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)
        
        play1.reset()
        play2.reset()
        ball.reset()

        play1.update_l()
        play2.update_r()
        ball.update()

        if sprite.collide_rect(play1, ball) or sprite.collide_rect(play2, ball):
            ball.speed_x *= -1
            hit.play()
        
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            firee.play()
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            firee.play()
    display.update()
    clock.tick(FPS)

