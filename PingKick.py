
from pygame import *
from random import *
from time import time as tm
window = display.set_mode((800, 700))
display.set_caption('Shooter game')
background = transform.scale(image.load('galaxy.jpg'), (800, 700))
clock = time.Clock()

font.init()
font1 = font.Font(None, 30)
font2 = font.Font(None, 100)
winLabel = font2.render('YOU WIN!', True, (252, 253, 222))
loseLabel = font2.render('YOU LOSE!', True, (252, 253, 222))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fireSound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, imageName, x, y, speed, sizeX=75, sizeY=75):
        self.image = transform.scale(image.load(imageName), (sizeX, sizeY))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.bSpeed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x <800 - 80:
            self.rect.x += self.speed

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        pass

score_lose = 0

class Enemy(GameSprite):
    def update(self):
        if self.rect.y <= 620:
            self.rect.y += self.speed
        else:
            global score_lose
            score_lose += 1
            if score_lose >= 10:
                global finish 
                finish = True
            self.respawn()
    def respawn(self):        
        self.rect.y = 0
        self.rect.x = randint (0, 700-20)
        self.speed = randint(int(self.bSpeed - 0.5*self.bSpeed),int(self.bSpeed + 0.5*self.bSpeed))
        if self.speed == 0:
            self.speed = 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            global bullets
            bullets.remove(self)
            #self.kill()

player = Player('rocket.png', 10, 620, 10)
#enemies = sprite.Group()
enemies = list()
for i in range (20):
    enemy = (Enemy('ufo.png', randint (0, 700), 0, randint(1, 5)))
    enemies.append(enemy)
    

run = True
finish = False
bullets = list()
shotTime = 0
btwnShotTime = 0.015
score = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    window.blit(background, (0, 0))        
    if not finish:
        player.move()
        if tm() - shotTime >= btwnShotTime:
            keys = key.get_pressed()
            if keys[K_UP]:
                fireSound.play()
                bullets.append(Bullet('bullet.png', player.rect.centerx-10, player.rect.top, 30, 20, 40))
                shotTime = tm()    
        for bullet in bullets:
            bullet.update()
            bullet.reset()
            for enemy in enemies:
                if sprite.collide_rect(bullet, enemy):
                    enemy.respawn()
                    if (score % 10) == 0:
                        enemies.append(Enemy('ufo.png', randint(0, 775), 0, randint(1,4 + (score // 50))))
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 1
                    if score >= 200:
                        #finish = True
                        finish = False
                    enemy.reset()

        player.reset()    
        for enemy in enemies:
            enemy.update()
            if sprite.collide_rect(player, enemy):
                #finish = True
                finish = False
            enemy.reset()

    else:
        if score >= 10:
            window.blit(winLabel, (225, 275))
        else:
            window.blit(loseLabel, (225, 275))


    window.blit(font1.render('FN F2000 Tactical' + str(score), True, (255, 255, 255)), (0, 0))
    window.blit(font1.render('ВСК' + str(score_lose), True, (255, 255, 255)), (0, 35))
    display.update()
    clock.tick(60)
