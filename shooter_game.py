#Create your own shooter
from time import sleep
from random import randint
from pygame import *

window = display.set_mode((700, 500))
display.set_caption("shooter")
background = transform.scale(image.load("galaxy.jpg"), (700,500))

score = 0
lost = 0
goal = 30
max_lost = 3


font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

win = font1.render("YOU WIN", True, (255,255,255))
lose = font1.render("YOU LOSE", True, (255,0,0))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 700 - 80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill



ship = player("rocket.png",5,500-100,80,100,10)


monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1,6):
    monster = enemy("ufo.png", randint(80,700-80), -40,80,50,randint(1,3))
    monsters.add(monster)

fire_sound = mixer.Sound("fire.ogg")
fps = 60
clock = time.Clock()
game = True
finish = False
while game:
    window.blit(background, (0,0))

    for e in event.get():

        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()


    if not finish:
        ship.reset()
        ship.update()

        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        monsters.update()

        text = font2.render("score : " +str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lost = font2.render("missed : " +str(lost), 1, (255,255,255))
        window.blit(text_lost, (10,50))

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = enemy("ufo.png", randint(80,700-80), -40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            window.blit(lose, (200,200))
            finish = True
        if score >= goal:
            window.blit(win,(200,200))
            finish = True
    display.update()
    clock.tick(fps)
