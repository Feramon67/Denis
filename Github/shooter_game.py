from pygame import *
from random import *
FPS = 60
window = display.set_mode((700,500))
display.set_caption('Шутер')
galaxy = transform.scale(image.load('galaxy.jpg'),(700,500))
game = True
clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, x, y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (x, y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.speed
    def fire(self):
        bull = Bullet('bullet.png',wer.rect.centerx ,wer.rect.top,10,20,10)
        bullets.add(bull)

prop = 0
win = 0
speed = 25
class Enemy(GameSprite):
    def update(self):
        global prop
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(5,600)
            self.rect.y = 0
            prop += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= speed
        if self.rect.y < 0:
            self.kill()

wer = Player('rocket.png',5,400,80,100,10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1,6):
    qwe = Enemy('ufo.png',randint(60,600),-40,80,50,randint(1,3))
    monsters.add(qwe)
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 100)
finish = False
while game:    
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                wer.fire()
                fire_sd = mixer.Sound('fire.ogg')
                fire_sd.play()
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(galaxy,(0,0))
        text = font1.render('Пропущено:' + str(prop), 1, (255, 255, 255))
        window.blit(text,(10,50))
        sett = font1.render('Счет:' + str(win), 1, (255, 255, 255))
        bullets.update()
        bullets.draw(window)
        monsters.update()
        window.blit(sett,(10,20))
        monsters.draw(window)
        sprites_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        for m in sprites_list:
            win += 1
            qwe = Enemy('ufo.png',randint(60,600),-40,80,50,randint(1,3))
            monsters.add(qwe)
        if prop >= 3:
            finish = True
            text1 = font2.render('Ты проиграл!', 1, (255, 255, 255))
            window.blit(text1,(125,200))
        if win >= 10:
            finish = True
            text2 = font2.render('Ты выйграл!', 1, (255, 255, 255))
            window.blit(text2,(125,200))
        wer.reset()
        wer.update()
    display.update()
    clock.tick(FPS)