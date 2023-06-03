import pygame
import random
from abc import ABC, abstractmethod

pygame.init()

menu_st = pygame.mixer.Sound('asset/Audio/lagu menu.mp3')
lose_st = pygame.mixer.Sound('asset/Audio/lagu kalah.mp3')
play_st = pygame.mixer.Sound('asset/Audio/lagu main.mp3')

global x_bg, y_bg, game_speed, obstacles
game_speed = 15
x_bg = 0
y_bg = 0
font = pygame.font.Font("asset/arialbd.ttf", 20)
title = pygame.font.Font('asset/Karasha-z8mYw.otf', 100)
obstacles = []

#fps settings
clock = pygame.time.Clock()
fps = 30

#game window
bottom_panel = 150
screenWidth = 800
screenHeight = 400 + bottom_panel

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Ninja Run')

#scoreboard settings
class point():
    def __init__(self):
        self.__point = 0
    def get_point(self):
        return self.__point
    def increase(self):
        self.__point += 1
    def reset(self):
        self.__point = 0

#control panel
class control():
    def __init__(self):
        self.panel = pygame.image.load('asset/control panel.png').convert_alpha()
    def draw(self):
        screen.blit(self.panel, (0,screenHeight - bottom_panel))

#background images
class still_bg():
    def __init__(self):
        self.img = pygame.image.load('asset/bg hutan.png').convert_alpha()
    def draw(self):
        screen.blit(self.img, (0,0))

class bg():
    def __init__(self):
        self.bg_img = pygame.image.load('asset/bg hutan.png').convert_alpha()
        self.bg_width = self.bg_img.get_width()
    def draw(self):
        global x_bg, y_bg
        screen.blit(self.bg_img, (x_bg, y_bg))
        screen.blit(self.bg_img, (self.bg_width + x_bg, y_bg))
        if x_bg <= - self.bg_width:
            screen.blit(self.bg_img, (self.bg_width + x_bg, y_bg))
            x_bg = 0
        x_bg -= game_speed

#char
class move(ABC):
    @abstractmethod
    def running(self):
        pass
    @abstractmethod
    def jumping(self):
        pass
    @abstractmethod
    def sliding(self):
        pass

class ninja(move):
    def __init__(self, x, y):
        run = pygame.image.load('asset/run.png').convert_alpha()
        run = pygame.transform.scale(run, (run.get_width() / 3.5, run.get_height() / 3.5))
        jump = pygame.image.load('asset/jump.png').convert_alpha()
        jump = pygame.transform.scale(jump, (jump.get_width() / 3.5, jump.get_height() / 3.5))
        slide = pygame.image.load('asset/slide.png').convert_alpha()
        slide = pygame.transform.scale(slide, (slide.get_width() / 3.5, slide.get_height() / 3.5))

        self.run = run
        self.jump = jump
        self.jump_speed = 7
        self.slide = slide

        self.img = self.run
        self.img_rect = self.img.get_rect()
        self.x = x
        self.y = y
        self.slide_y = y + 50
        self.img_rect.x = x
        self.img_rect.y = y

        self.ninja_run = True
        self.ninja_jump = False
        self.ninja_slide = False

    def update(self):
        if self.ninja_run:
            self.running()
        if self.ninja_jump:
            self.jumping()
        if self.ninja_slide:
            self.sliding()

        if userInput[pygame.K_UP]:
            self.ninja_jump = True
            self.ninja_run = False
        elif userInput[pygame.K_DOWN]:
            self.ninja_run = False
            self.ninja_slide = True
        elif not (self.ninja_jump or userInput[pygame.K_DOWN]): 
            self.ninja_run = True
            self.ninja_slide = False
    
    def running(self):
        self.img = self.run
        self.img_rect = self.img.get_rect()
        self.img_rect.x = self.x
        self.img_rect.y = self.y

    def jumping(self):
        self.img = self.jump
        self.img_rect.y -= self.jump_speed * 4
        self.jump_speed -= 0.5
        if self.jump_speed < -7:
            self.jump_speed = 7
            self.ninja_jump = False
            self.ninja_run = True

    def sliding(self):
        self.img = self.slide
        self.img_rect.x = self.x
        self.img_rect.y = self.slide_y

    def draw(self):
        screen.blit(self.img, self.img_rect)

class idle():
    def __init__(self, x, y):
        idle = pygame.image.load('asset/idle.png').convert_alpha()
        idle = pygame.transform.scale(idle, (idle.get_width() / 3.5, idle.get_height() / 3.5))
        self.idle = idle
        self.img = self.idle
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y

    def draw(self):
        screen.blit(self.img, self.img_rect)


#obstacle
rock0 = pygame.image.load('asset/Rocks/0.png').convert_alpha()
rock0 = pygame.transform.scale(rock0, (rock0.get_width() * 1.5, rock0.get_height() * 1.5))
rock1 = pygame.image.load('asset/Rocks/1.png').convert_alpha()
rock1 = pygame.transform.scale(rock1, (rock1.get_width() * 1.5, rock1.get_height() * 1.5))
bird = pygame.image.load('asset/bird.png').convert_alpha()
bird = pygame.transform.scale(bird, (bird.get_width() * 2, bird.get_height() * 2))
bandit = pygame.image.load('asset/bandit.png').convert_alpha()
bandit = pygame.transform.scale(bandit, (bandit.get_width() * 3, bandit.get_height() * 3))
bandit_rect = bandit.get_rect()
class Obstacle():
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = screenWidth

    def update(self):
        if self.image == bird:
            self.rect.x -= game_speed * 1.5
        else:
            self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop()

    def draw(self):
        screen.blit(self.image, self.rect)

class rock_0(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 287

class rock_1(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 295

class birds(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        if random.randint(0, 1) == 0:
            self.rect.y = 160
        elif random.randint(0, 1) == 1:
            self.rect.y = 250

class bandits(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 245

#load and updates assets
def draw_assets(assets):
    assets.draw()

def update_assets(assets):
    assets.update()

#Main Program
panel = control()
still = still_bg()
moving = bg()
player = ninja(80, 225)
menu_idle = idle(80, 225)
scores = point()
death_count = 0
awal = True
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    userInput = pygame.key.get_pressed()

    draw_assets(panel)

    if awal == True and death_count == 0:
        #menu_st.play()
        draw_assets(still)
        text = title.render('Ninja Run', True, (235,235,235))
        textRect = text.get_rect()
        textRect.center = (screenWidth // 2, screenHeight // 3)
        screen.blit(text, textRect)
        draw_assets(menu_idle)
        if userInput[pygame.K_SPACE]:
            #menu_st.stop()
            awal = False
            player.running()
    elif awal == True and death_count > 0 :
        #lose_st.play()
        draw_assets(still)
        text = title.render('Ninja Run', True, (235,235,235))
        score = font.render('Scores: ' + str(scores.get_point()), True, (235,235,235))
        textRect = text.get_rect()
        textRect.center = (screenWidth // 2, screenHeight // 3)
        scoreRect = score.get_rect()
        scoreRect.center = (screenWidth // 2, screenHeight // 3 + 100)
        screen.blit(text, textRect)
        screen.blit(score, scoreRect)
        draw_assets(menu_idle)
        if userInput[pygame.K_SPACE]:
            #lose_st.stop()
            game_speed = 15
            scores.reset()
            awal = False
            player.running()

    if not awal:
        #play_st.play()
        draw_assets(moving)
        update_assets(player)
        draw_assets(player)

        scores.increase()
        if scores.get_point() % 100 == 0:
            game_speed += 1
        text = font.render("Scores: " + str(scores.get_point()), True, (235, 235, 235))
        text_rect = text.get_rect()
        text_rect.center = (700,25)
        screen.blit(text, text_rect)

        if len(obstacles) == 0:
            if random.randint(0, 3) == 0:
                obstacles.append(rock_0(rock0))
            elif random.randint(0, 3) == 1:
                obstacles.append(rock_1(rock1))
            elif random.randint(0, 3) == 2:
                obstacles.append(birds(bird))
            elif random.randint(0, 3) == 3:
                obstacles.append(bandits(bandit))

        for obstacle in obstacles:
            draw_assets(obstacle)
            update_assets(obstacle)
            if player.img_rect.colliderect(obstacle.rect):
                #play_st.stop()
                obstacles.pop()
                death_count += 1
                awal = True

    clock.tick(fps)
    pygame.display.update()

pygame.quit()
