from typing import Any
from pygame import *


class GameSprite(sprite.Sprite):
   

   def __init__(self, char_img, char_x, char_y, char_width, char_height, char_speed):
       super().__init__()
       self.image = transform.scale(image.load(char_img), (char_width, char_height))
       self.speed = char_speed
       self.rect = self.image.get_rect()
       self.rect.x = char_x
       self.rect.y = char_y

    # Update character on the screen
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -=self.speed
        if keys[K_RIGHT]:
            self.rect.x +=self.speed
        if keys[K_UP]:
            self.rect.y -=self.speed
        if keys[K_DOWN]:
            self.rect.y +=self.speed

class Enemy(GameSprite):
    goLeft = False
    def update(self):
        if self.rect.x < 20:
            self.goLeft = False
        if self.rect.x > 596:
            self.goLeft = True

        if self.goLeft:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = GameSprite("background.jpg", 0,0,win_width, win_height,0)

player = Player('hero.png', 5, win_height - 80, 65, 65, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 65, 65, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 65, 65, 0)

w1 = GameSprite("wall_v.png", 250, 100, 187, 200, 0)
w2 = GameSprite("wall_h.png", 500, 375, 69, 420, 0)
w3 = GameSprite("wall_h.png", 400, 186, 290, 87, 0)

run = True
clock = time.Clock()
FPS = 60


mixer.init()
mixer.music.load('inksanstheme.mp3')
mixer.music.play()

mixer.music.set_volume(0.3)

money = mixer.Sound('cha_ching.mp3')
kick = mixer.Sound('hit.mp3')

finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
             run = False
    if not finish:
        background.reset()
        player.update()
        player.reset()
        monster.update()
        monster.reset()
        final.update()
        final.reset()
        w1.reset()
        w2.reset()
        w3.reset()

        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3):
            finish = True
            kick.play()

        if sprite.collide_rect(player, final):
            finish = True
            money.play()

    display.update()
    clock.tick(FPS)