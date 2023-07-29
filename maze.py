# Create your game in this file!
from pygame import *
num_shots, reload_time = 0, 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5)
        bullets_group.add(bullet)

class NPCSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.partrol_down = False

        self.monsters = sprite.Group()
    def reset(self):
        if self.partrol_down:
            self.rect.y -= self.speed
            if self.rect.y < 115: self.partrol_down = False
        else:
            self.rect.y += self.speed
            if self.rect.y > 325: self.partrol_down = True
        window.blit(self.image, (self.rect.x, self.rect.y))
        self.monsters.draw(window)

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        # self.color_1 = color_1
        # self.color_2 = color_2
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(sprite.Sprite):
    def __init__(self, bullet_image, bullet_x, bullet_y, bullet_speed):
        super().__init__()
        self.image = transform.scale(image.load(bullet_image), (50, 35))
        self.speed = bullet_speed
        self.rect = self.image.get_rect()
        self.rect.x = bullet_x
        self.rect.y = bullet_y
    def update(self):
        if self.rect.x == 0: self.kill()
        if self.rect.x > 0: self.rect.x += self.speed
        window.blit(self.image, (self.rect.x, self.rect.y))

#create game window
window = display.set_mode((700, 500))
display.set_caption("Catch")
#set scene background
background = transform.scale(image.load('background.jpg'), (700, 500))
#creat 2 sprites and place them on the scene
player = GameSprite('hero.png', 150, 400, 6)
monster = NPCSprite('cyborg.png', 300, 200, 4)
gold = GameSprite('treasure.png', 600, 250, 0)
wall_1 = Wall(0, 0, 255, 100, 50, 500, 10)
wall_2 = Wall(0, 0, 255, 250, 400, 220, 10)
wall_3 = Wall(0, 0, 255, 100, 50, 10, 400)
wall_4 = Wall(0, 0, 255, 250, 200, 10, 200)
wall_5 = Wall(0, 0, 255, 450, 50, 10, 200)
wall_6 = Wall(0, 0, 255, 590, 150, 10, 250)
wall_7 = Wall(0, 0, 255, 390, 400, 10, 100)
wall_8 = Wall(0, 0, 255, 600, 325, 100, 10)
# mixer.init()
# mixer.music.load('jungles.ogg')
# mixer.music.play()
wall_list = [wall_1, wall_2, wall_3, wall_4, wall_5, wall_6, wall_7, wall_8]
wall_group = sprite.Group()
for wall in wall_list:
    wall_group.add(wall)
hits = 0
monsters_group = sprite.Group()
monsters_group.add(monster)
bullets_group = sprite.Group()
font.init()
text = font.Font(None, 70)
lose = text.render('YOU LOSE!', True, (255, 0, 0))
Win = text.render('YOU WIN!', True, (0, 255, 0))
music_time = 120
finish = False
clock = time.Clock()
FPS = 60

reload_pause_time = None
elapsed_time = 750
game = True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and player.rect.x > 5: 
            player.rect.x -= player.speed
            push_back = sprite.spritecollide(player, wall_group, False)
            for p in push_back:
                player.rect.left = max(player.rect.left, p.rect.right)
        if keys_pressed[K_RIGHT] and player.rect.x < 600: 
            player.rect.x += player.speed
            push_back = sprite.spritecollide(player, wall_group, False)
            for p in push_back:
                player.rect.right = min(player.rect.right, p.rect.left)
        if keys_pressed[K_UP] and player.rect.y > 5: 
            player.rect.y -= player.speed
            push_back = sprite.spritecollide(player, wall_group, False)
            for p in push_back:
                player.rect.top = max(player.rect.top, p.rect.bottom)
        if keys_pressed[K_DOWN] and player.rect.y < 400: 
            player.rect.y += player.speed
            push_back = sprite.spritecollide(player, wall_group, False)
            for p in push_back:
                player.rect.bottom = min(player.rect.bottom, p.rect.top)


        if keys_pressed[K_SPACE]: 
            if not reload_pause_time:
                player.fire()
                num_shots += 1

        if num_shots >= 5: 
            reload_time = True
            reload_pause_time = time.get_ticks()
            num_shots = 0       

        elapsed_time = time.get_ticks() - reload_pause_time if reload_pause_time else 750

        if reload_time: 
            if elapsed_time < 750:
                font.init()
                text = font.Font(None, 30)
                reload_text = text.render('WAIT, RELOAD...', True, (255, 255, 255))
                window.blit(reload_text, (200, 470))
            else:
                reload_text = text.render('WAIT, RELOAD...', False, (255, 255, 255))
                reload_pause_time = None
                reload_time = False

        sprite_list = sprite.spritecollide(player, monsters_group, True)
        bullet_hits = sprite.groupcollide(bullets_group, monsters_group, True, True)
        hits += len(bullet_hits)
        for bullet, monster in bullet_hits.items():
            print(':)')
            bullets_group.remove(bullet)
            monsters_group.remove(monster)
        window.blit(background, (0, 0))
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        wall_5.draw_wall()
        wall_6.draw_wall()
        wall_7.draw_wall()
        wall_8.draw_wall()
        player.reset()
        monster.reset()
        gold.reset()
        clock.tick(FPS)
        bullets_group.update()
        # monsters_group.update()
        win = sprite.collide_rect(player, gold)
        # died = sprite.collide_rect(player, monsters) or sprite.collide_rect(player, wall_group)
        
        died = sprite.spritecollide(player, monsters_group, False)
        enemy_died = None
        
        if win or died:

            finish = True
            mixer.init()           
        
    else:
        if len(died) > 0:
            print('I die')
            mixer.init()
            mixer.music.load('kick.ogg')
            if music_time > 0:
                mixer.music.play()
                music_time = 120
            window.blit(lose, (200, 200))
            break
        elif win:
            mixer.init()
            mixer.music.load('money.ogg')
            mixer.music.play()
            break
            window.blit(Win, (200, 200))
            
        clock.tick(FPS)
        mixer.music.pause()
    display.update()
#handle "click on the "Close the window"" event

display.update()
