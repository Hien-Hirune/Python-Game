import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("T-rex Game")

class Dino():
    def __init__(self):
        self.image = []
        for i in range(4):
            self.image.append(pygame.image.load('Dino'+str(i+1)+'.jpg'))
        self.order = 0
        self.y = 250

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and self.y > 50:
            self.y -= 40
            self.order = 3
        elif self.y < 250:
            self.y += 20
        screen.blit(self.image[self.order], (100, self.y))
        self.order += 1
        if self.order > 3:
            self.order = 0

        return self.image[self.order].get_rect(topleft=(100, self.y))

class Cactus():
    def __init__(self):
        self.image = []
        for i in range(4):
            self.image.append(pygame.image.load('Cactus'+str(i+1)+'.jpg'))
        self.x = 800
        self.speed = 10
        self.order = random.randint(0, 3)
        if self.order == 4:
            self.y = random.randint(220, 240)
        else:
            self.y = random.randint(280, 290)

    def update(self):
        self.x -= self.speed
        screen.blit(self.image[self.order], (self.x, self.y))
        return self.image[self.order].get_rect(topleft=(self.x, self.y))

class Cloud():
    def __init__(self):
        self.image = pygame.image.load('Cloud.jpg')
        self.x = 800
        self.y = random.randint(0, 50)
    def update(self):
        screen.blit(self.image, (self.x, self.y))
        self.x -= 3


running = True
FPS = 16
clock = pygame.time.Clock()
font = pygame.font.SysFont("couriernew", 28, bold=True)
end_game = False
score = 0

dino = Dino()
cactuses = []
clouds = []
pipe_spawn_time = 0

while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, 'white', (0, 350), (800, 350))

    if end_game:
        game_over_text = font.render("Game Over!", True, 'white', 'black')
        screen.blit(game_over_text, (320, 210))
    else:
        current_dino = dino.update()
        # get time
        current_time = pygame.time.get_ticks()
        if current_time > (pipe_spawn_time + random.randint(2000, 7000)):
            cactuses.append(Cactus())
            clouds.append(Cloud())
            pipe_spawn_time = current_time

        for cloud in clouds:
            cloud.update()
            if cloud.x < -50:
                clouds.remove(cloud)

        for cactus in cactuses:
            current_cactus = cactus.update()
            if current_cactus.colliderect(current_dino):
                end_game = True
                break
            if cactus.x < 0:
                cactuses.remove(cactus)
        score += 1

    score_text = font.render("Score: " + str(score), True, 'white', 'black')
    screen.blit(score_text, (620, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    pygame.display.flip()

pygame.quit()