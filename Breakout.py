from time import sleep
import pygame
import random
import tkinter
from tkinter import messagebox
root = tkinter.Tk()
root.withdraw()
pygame.init()

screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()

class Player(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 25) # TODO CHANGE NUMBERS LATER IDK
        self.vx = 0
    def draw(self):
        pygame.draw.rect(screen, "lavender", self, 0) # 0 = fill
        pygame.draw.rect(screen, "purple", self, 1) # 1 = outline
    def update(self):
        self.x += self.vx
        if self.x < 0:
            self.x =0
        elif self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width
class Ball(pygame.Rect):
    width = 20
    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = random.randint(5,8) * random.choice([1,-1])
        self.vy = random.randint(5,8)
    def draw(self):
        pygame.draw.ellipse(screen, "white", self, 0) # 0 = fill
        pygame.draw.ellipse(screen, "darkblue", self, 1) # 1 = outline
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x + self.width > screen.get_width():
            self.vx *= -1
        if self.y < 0: # or self.y + self.width > screen.get_height():
            self.vy *= -1
        if self.y + self.width > screen.get_height():
            self.x = screen.get_width()/2
            self.y = screen.get_height()/2+150
class Brick(pygame.Rect):
    width = 160
    height = 50
    def __init__(self, x, y):
        super().__init__(x, y, Brick.width, Brick.height)
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    def draw(self):
        pygame.draw.rect(screen, self.color, self, 0, border_radius=10) # 0 = fill
        pygame.draw.rect(screen, "black", self, 1, border_radius=10) # 1 = outline
    def update(self, Ball):
        if Ball.colliderect(self):
            #ball hits bottom or top
            if (Ball.y <= self.y + self.height and self.x <= Ball.x <= self.x + self.width)\
                    or (Ball.y+Ball.width >= self.y and self.x <= Ball.x <= self.x + self.width):
                Ball.vy *= -1
            elif (Ball.x <= self.x + self.width and self.y <= Ball.y <= self.y + self.height)\
                or (Ball.x+Ball.width >= self.x and self.y <= Ball.y <= self.y + self.height):
                Ball.vx *= -1

def reset():
    for x in range(0, 8):
        for y in range(0, 10):
            bricks.append(Brick(x * Brick.width, y * Brick.height))
    player.x = screen.get_width()/2 - 50
    player.y = screen.get_height() - 50


ball = Ball(screen.get_width()/2 - 50, screen.get_height()/2+150, 20)
player = Player(screen.get_width()/2 - 50, screen.get_height() - 50)
bricks = []
for x in range(0,8):
    for y in range(0,10):
        bricks.append(Brick(x*Brick.width, y*Brick.height))
while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player.x = mouse_x - player.width/2

    # Do logical updates here.
    player.update()
    ball.update()
    for brick in bricks:
        brick.update(ball)
    if ball.colliderect(player):
        ball.vy *= -1
        ball.y = player.y - ball.width # TODO maybe add sideways colision idk
        diff = (ball.x + ball.w/2) - (player.x + player.w/2)
        ball.vx += diff // 10
    for b in bricks:
        if ball.colliderect(b):
            bricks.remove(b)
    if len(bricks) == 0:
        sleep(100)
        messagebox.showinfo("GGS", "YOU WIN")
        game_over = messagebox.askyesno("GGS", "Play Again?")
        if game_over:
            reset()
        else:
            pygame.quit()
            raise SystemExit


    screen.fill("black")  # Fill the display with a solid color

    # Render the graphics here.
    player.draw()
    ball.draw()
    for x in bricks:
        x.draw()
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)


