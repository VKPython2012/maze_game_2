from pygame import *

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

class NPCSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.partrol_down = False
    def reset(self):
        if self.partrol_down:
            self.rect.y -= self.speed
            if self.rect.y < 115: self.partrol_down = False
        else:
            self.rect.y += self.speed
            if self.rect.y > 325: self.partrol_down = True
        window.blit(self.image, (self.rect.x, self.rect.y))

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

#create game window
window = display.set_mode((700, 500))
display.set_caption("Catch")
#set scene background
background = transform.scale(image.load('background.jpg'), (700, 500))
#creat 2 sprites and place them on the scene
sprite1 = GameSprite('hero.png', 150, 400, 6)
sprite2 = NPCSprite('cyborg.png', 300, 200, 4)
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

font.init()
text = font.Font(None, 70)
lose = text.render('YOU LOSE!', True, (255, 0, 0))
Win = text.render('YOU WIN!', True, (0, 255, 0))
music_time = 120
finish = False
clock = time.Clock()
FPS = 60


game = True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:


        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and sprite1.rect.x > 5: 
            sprite1.rect.x -= sprite1.speed
        if keys_pressed[K_RIGHT] and sprite1.rect.x < 595: 
            sprite1.rect.x += sprite1.speed
        if keys_pressed[K_UP] and sprite1.rect.y > 5: 
            sprite1.rect.y -= sprite1.speed
        if keys_pressed[K_DOWN] and sprite1.rect.y < 395: 
            sprite1.rect.y += sprite1.speed
        
        window.blit(background, (0, 0))
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        wall_5.draw_wall()
        wall_6.draw_wall()
        wall_7.draw_wall()
        wall_8.draw_wall()
        sprite1.reset()
        sprite2.reset()
        gold.reset()
        clock.tick(FPS)
        
        win = sprite.collide_rect(sprite1, gold)
        died = sprite.collide_rect(sprite1, sprite2) or sprite.collide_rect(sprite1, wall_1) or sprite.collide_rect(sprite1, wall_2) or sprite.collide_rect(sprite1, wall_3) or sprite.collide_rect(sprite1, wall_4) or sprite.collide_rect(sprite1, wall_5) or sprite.collide_rect(sprite1, wall_6) or sprite.collide_rect(sprite1, wall_7) or sprite.collide_rect(sprite1, wall_8)

        if win or died:

            finish = True
            mixer.init()
            
        
    else:
        if died:
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