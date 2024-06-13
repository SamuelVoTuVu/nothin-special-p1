from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.3)
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

score = 0
lost = 0
max_lost = 3
missed = 0
class GameSprite(sprite.Sprite):
    def __init__(self, char_img, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(char_img), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x < 700:
            self.rect.x +=self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed

        if self.rect.y > win_height:
            self.rect.y = 0
            missed += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500

bullets = sprite.Group()

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")

background = GameSprite('galaxy.jpg', 0,0,win_width,win_height,0)
player = Player('rocket.png', 100, win_height - 100, 80, 100, 5)

list_enemies = sprite.Group()

ufo = "ufo.png"
asteroid = "asteroid.png"

for i in range(6):
    random_X = randint( 0 , win_width )
    random_speed = randint( 4, 5)

    random_skin = randint(1,2)
    currentskin = ""
    if random_skin == 1:
        currentskin = ufo
    else:
        currentskin = asteroid


    alien = Enemy(currentskin, random_X, 0, 70, 50, random_speed)
    list_enemies.add(alien)

finish = False
run = True


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if not finish:

       text = font2.render("Score: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))

       background.reset()
       player.update()
       player.reset()
       list_enemies.update()
       list_enemies.draw(window)
       bullets.update()
       bullets.draw(window)

       font2 = font.Font(None, 20)
       score_text = font2.render("Score: "+ str(score), False, (255, 255, 255))
       missed_text = font2.render("Missed: " + str(lost), False, (255, 255, 255))
       window.blit(score_text, (50, 100))
       window.blit(missed_text, (50, 200))

       if sprite.spritecollide(player, list_enemies, False) or missed >= 4:
           
           finish = True
           window.blit(lose, (win_width/2, win_height/2))

       if sprite.groupcollide(bullets, list_enemies, True, True):
           score += 1
           random_X = randint( 0 , win_width )
           alien = Enemy("ufo.png", random_X, 0, 70, 50, 1)
           list_enemies.add(alien)

           if score >= 20:
               finish = True
               window.blit(win, (win_width/2, win_height/2))


    display.update()
    time.delay(50)