import pygame
import random
import math
from pygame import mixer

pygame.init()
mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake with Pygame")

class Snake():
    def __init__(self):
        self.x = 400
        self.y = 300
        self.x_move = 0
        self.y_move = 0
        self.body = []
        self.speed = 2
        self.head_rect = pygame.draw.circle(screen, 'blue', (self.x, self.y), 10)

    def get_direction(self):
        global up_music, down_music, left_right_music
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP] and self.y_move <= 0:
            if up_music:
                mixer.music.load('up.wav')
                mixer.music.play()
                up_music = False
                down_music = True
                left_right_music = True
            self.x_move = 0
            self.y_move = -self.speed
        if key_pressed[pygame.K_DOWN] and self.y_move >= 0:
            if down_music:
                mixer.music.load('down.wav')
                mixer.music.play()
                down_music = False
                up_music = True
                left_right_music = True
            self.x_move = 0
            self.y_move = self.speed
        if key_pressed[pygame.K_LEFT] and self.x_move <= 0:
            if left_right_music:
                mixer.music.load('left-right.wav')
                mixer.music.play()
                down_music = True
                up_music = True
                left_right_music = False
            self.x_move = -self.speed
            self.y_move = 0
        if key_pressed[pygame.K_RIGHT] and self.x_move >= 0:
            if left_right_music:
                mixer.music.load('left-right.wav')
                mixer.music.play()
                down_music = True
                up_music = True
                left_right_music = False
            self.x_move = self.speed
            self.y_move = 0

    def update(self):
        # Set first element of body to be head position
        if len(self.body) >= 1:
            # Move body of snake
            for i in range(len(self.body)-1, 0, -1):
                self.body[i] = self.body[i-1]
            self.body[0] = {"x": self.x, "y": self.y}

        if self.x_move != 0:
            self.x += self.x_move
        if self.y_move != 0:
            self.y += self.y_move

    def drawSnake(self):
        self.head_rect = pygame.draw.circle(screen, 'blue', (self.x, self.y), 10)
        for body in self.body:
            pygame.draw.circle(screen, 'blue', (body['x'], body['y']), 10)

    def check_end_game(self):
        if (self.x <= 10 or self.x >= 790) or (self.y <= 10 or self.y >= 590):
            return True

class Food():
    def __init__(self, special, begin_time):
        self.x = random.randint(10, 790)
        self.y = random.randint(10, 590)
        self.special = special
        if self.special:
            self.begin_time = begin_time
            self.radius = 15
            self.rect = pygame.draw.circle(screen, 'red', (self.x, self.y), self.radius)
        else:
            self.begin_time = -1 # begin_time = -1 if normal food
            self.radius = 10
            self.rect = pygame.draw.circle(screen, 'orange', (self.x, self.y), self.radius)

    def update(self):
        if self.begin_time != -1:
            cur_time = pygame.time.get_ticks()
            if cur_time < self.begin_time + 10000:
                self.rect = pygame.draw.circle(screen, 'red', (self.x, self.y), self.radius)
        else:
            self.rect = pygame.draw.circle(screen, 'orange', (self.x, self.y), self.radius)

class Wall():
    def __init__(self):
        self.x = random.randint(0, 750)
        self.y = random.randint(0, 550)
        self.height = random.randint(50, 200)
        self.direction = random.randint(0, 1) # 0: vertical, 1: horizontal
        if self.direction == 0:
            self.rect = pygame.draw.rect(screen, '#0e7819', (self.x, self.y, 20, self.height))
        else:
            self.rect = pygame.draw.rect(screen, '#0e7819', (self.x, self.y, self.height, 20))

    def update(self):
        if self.direction == 0:
            self.rect = pygame.draw.rect(screen, '#0e7819', (self.x, self.y, 20, self.height))
        else:
            self.rect = pygame.draw.rect(screen, '#0e7819', (self.x, self.y, self.height, 20))

def create_wall():
    global wall_list
    numWall = random.randint(5, 12)
    wall_list = []
    for i in range(numWall):
        wall_temp = Wall()
        while wall_temp.rect.colliderect(snake.head_rect):
            wall_temp = Wall()
        for food in food_list:
            while wall_temp.rect.colliderect(food.rect):
                wall_temp = Wall()
        wall_list.append(wall_temp)

def create_food():
    global food_list
    numFood = random.randint(5, 10)
    food_list = []
    for i in range(numFood):
        food_list.append(Food(False, -1))

def create_special_food():
    global food_list, food_spawn_time
    current_time = pygame.time.get_ticks()
    if current_time > (food_spawn_time + random.randint(10000, 20000)):
        food_spawn_time = current_time

        food_temp = Food(True, food_spawn_time)
        while food_temp.rect.colliderect(snake.head_rect):
            food_temp = Food(True, food_spawn_time)
        for food in food_list:
            while food_temp.rect.colliderect(food.rect):
                food_temp = Food(True, food_spawn_time)
        for wall in wall_list:
            while food_temp.rect.colliderect(wall.rect):
                food_temp = Food(True, food_spawn_time)
        food_list.append(food_temp)

def collide(snake, food_list):
    global score, high_score
    for food in food_list:
        distance = math.sqrt((snake.x - food.x) ** 2 + (snake.y - food.y) ** 2)
        if distance <= food.radius + 10:
            if food.special:
                score += 10
            else:
                score += 1
            if len(snake.body) == 0:
                snake.body.append({'x': snake.x, 'y': snake.y})
            else:
                snake.body.append(snake.body[-1])
            food_list.remove(food)
            mixer.music.load('eat.wav')
            mixer.music.play()
            break
    if score > high_score:
        high_score = score

def update_wall_food():
    global food_list, wall_list
    for food in food_list:
        food.update()
        if food.special:
            cur_time = pygame.time.get_ticks()
            if cur_time >= food.begin_time + 10000: #if timeout
                food_list.remove(food)
    for wall in wall_list:
        wall.update()

running = True
FPS = 60
clock = pygame.time.Clock()

font = pygame.font.SysFont("couriernew", 28, bold=True)
score = 0
high_score = 0

snake = Snake()
create_food()
create_wall()
is_end = False
food_spawn_time = 0

bg = pygame.image.load('bg_Snake.png')
end_music = True
up_music = True
down_music = True
left_right_music = True
while running:
    clock.tick(FPS)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    for wall in wall_list:
        if wall.rect.colliderect(snake.head_rect):
            is_end = True
            break

    is_end = is_end or snake.check_end_game()
    if is_end:
        if end_music:
            mixer.music.load('die.wav')
            mixer.music.play()
            end_music = False
        game_over_text = font.render("GAME OVER!", True, 'black')
        replay_text = font.render("(Press Space to play again)", True, 'black')
        screen.blit(game_over_text, (320, 230))
        screen.blit(replay_text, (180, 280))
        #reset
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] == True:
            score = 0
            is_end = False
            end_music = True
            snake.__init__()
            create_food()
            create_wall()
            update_wall_food()
    elif score == 100:
        win_text = font.render("YOU WIN!!!", True, 'black')
        screen.blit(win_text, (320, 230))
    else:
        #update
        snake.get_direction()
        snake.update()
        snake.drawSnake()
        update_wall_food()
        create_special_food()
        #check collide
        collide(snake, food_list)
        #check level up
        if len(food_list) == 0:
            create_food()
            create_wall()

    score_text = font.render("Score: " + str(score) + ' - High score: ' + str(high_score), True, 'black')
    screen.blit(score_text, (0, 0))

    pygame.display.flip()

pygame.quit()
