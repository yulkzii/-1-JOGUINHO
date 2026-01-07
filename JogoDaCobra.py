import pygame, sys, random
from pygame.math import Vector2
from pygame.locals import *

pygame.init()

#Game sound
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.load('BoxCat Games - Love Of My Life.mp3')
pygame.mixer.music.play(-1)

#classes main=principal
class Main:
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()
    def update(self):
        self.snake.move_snake()
        self.ifcollision()
        self.GAMEOVER()

    def draw_elements(self):
        self.draw_grass()
        self.apple.draw_apple()
        self.snake.draw_snake()
        self.score()

    def ifcollision(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.randomize()
            self.snake.addbody()
            self.snake.mordida_som()
        
        for snake in self.snake.body[1:]:
            if snake == self.apple.pos:
                self.apple.randomize()

    def GAMEOVER(self):
        if not 0 <= self.snake.body[0].x < grade_numbr or not 0 <= self.snake.body[0].y < grade_numbr:
            self.gameover()
        for snake in self.snake.body[1:]:
            if snake == self.snake.body[0]:
                self.gameover()

    def gameover(self):
        self.snake.reset()

    def draw_grass(self):
        color_grass = (148,230,73)
        for row in range(grade_numbr):
            if row % 2 == 0:
                for col in range(grade_numbr):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*grade_size,row*grade_size,grade_size,grade_size)
                        pygame.draw.rect(screen,color_grass,grass_rect)
            else:
                for col in range(grade_numbr):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*grade_size,row*grade_size,grade_size,grade_size)
                        pygame.draw.rect(screen,color_grass,grass_rect)

    def score (self):
         scoretext = str(len(self.snake.body) - 3)
         score_Surface = font_game.render(scoretext,False,(56,74,12))
         score_x = int(grade_size*grade_numbr - 38)
         score_y = int(grade_size*grade_numbr - 455)
         score_rect = score_Surface.get_rect(center = (score_x,score_y))
         applescore_rect = applescore.get_rect(midright = (score_rect.left - 2, score_y - 5))
         bg_rect = pygame.Rect(applescore_rect.left - 5,applescore_rect.top - 3,applescore_rect.width + score_rect.width + 15,applescore_rect.height + 5)

         pygame.draw.rect(screen,(167,209,61),bg_rect)
         screen.blit(score_Surface, score_rect)
         screen.blit(applescore,applescore_rect)
         pygame.draw.rect(screen,(56,74,12),bg_rect,2)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.newpart_body = False

        self.head_up = pygame.image.load('graficos/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graficos/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('graficos/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('graficos/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('graficos/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graficos/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('graficos/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('graficos/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('graficos/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graficos/body_horizontal.png').convert_alpha()

        self.body_bl = pygame.image.load('graficos/body_bl.png').convert_alpha()
        self.body_br = pygame.image.load('graficos/body_br.png').convert_alpha()
        self.body_tl = pygame.image.load('graficos/body_tl.png').convert_alpha()
        self.body_tr = pygame.image.load('graficos/body_tr.png').convert_alpha()
        self.mordida = pygame.mixer.Sound('crunch.wav')

    def draw_snake(self):
        self.update_snake_head()
        self.update_snake_tail()

        for index,snake in enumerate(self.body):
            Xpos = int(snake.x*grade_size)
            Ypos = int(snake.y*grade_size)
            snake_rect = pygame.Rect(Xpos,Ypos,grade_size,grade_size)

            if index == 0:
                screen.blit(self.head,snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,snake_rect)
            else:
                previous_snake = self.body[index + 1] - snake
                next_snake = self.body[index - 1] - snake
                if previous_snake.x == next_snake.x:
                    screen.blit(self.body_vertical,snake_rect)
                if previous_snake.y == next_snake.y:
                    screen.blit(self.body_horizontal,snake_rect)
                else:
                    if previous_snake.x == -1 and next_snake.y == -1 or previous_snake.y == -1 and next_snake.x == -1:
                        screen.blit(self.body_tl,snake_rect)
                    elif previous_snake.x == 1 and next_snake.y == -1 or previous_snake.y == -1 and next_snake.x == 1:
                        screen.blit(self.body_tr,snake_rect)
                    elif previous_snake.x == -1 and next_snake.y == 1 or previous_snake.y == 1 and next_snake.x == -1:
                        screen.blit(self.body_bl,snake_rect)
                    elif previous_snake.x == 1 and next_snake.y == 1 or previous_snake.y == 1 and next_snake.x == 1:
                        screen.blit(self.body_br,snake_rect)

    def update_snake_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_snake_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.newpart_body == True:
            copy_body = self.body[:]
            copy_body.insert(0,copy_body[0] + self.direction)
            self.body = copy_body[:]
            self.newpart_body = False
        else:
            copy_body = self.body[:-1]
            copy_body.insert(0,copy_body[0] + self.direction)
            self.body = copy_body[:]

    def addbody(self):
        self.newpart_body = True

    def mordida_som(self):
        self.mordida.play()
        self.mordida.set_volume(1)

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class Apple:
    def __init__(self):
        self.randomize()

    def draw_apple(self):
        apple_rect = pygame.Rect(int(self.pos.x*grade_size),int(self.pos.y*grade_size),grade_size,grade_size)
        screen.blit(apples, apple_rect)

    def randomize(self):
        self.x = random.randint(0,grade_numbr - 1)
        self.y = random.randint(0,grade_numbr - 1)
        self.pos = Vector2(self.x,self.y)

#variaveis
grade_size = 25
grade_numbr = 20
screen = pygame.display.set_mode((grade_size*grade_numbr, grade_size*grade_numbr))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
principal = Main()
apples = pygame.image.load('graficos/apple.png').convert_alpha()
applescore = pygame.image.load('graficos/applescore.png').convert_alpha()
font_game = pygame.font.Font('Fonts/Minecraft.ttf',(20))
fontGame = pygame.font.Font('Fonts/Minecraft.ttf',(100))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            principal.update()
        if event.type == KEYDOWN:
            if event.key == K_w:
                if principal.snake.direction.y != 1:
                    principal.snake.direction = Vector2(0,-1)
            if event.key == K_s:
                if principal.snake.direction.y != -1:
                    principal.snake.direction = Vector2(0,1)
            if event.key == K_a:
                if principal.snake.direction.x != 1:
                    principal.snake.direction = Vector2(-1,0)
            if event.key == K_d:
                if principal.snake.direction.x != -1:
                    principal.snake.direction = Vector2(1,0)


    screen.fill((161, 250, 79))
    principal.draw_elements()
    pygame.display.update()