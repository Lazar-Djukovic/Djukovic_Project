import pygame
import math


pygame.init()

GREEN = (43,132,88)
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

SCREEN_W = 1280
SCREEN_H = 720
display = pygame.display.set_mode((SCREEN_W,SCREEN_H))
pygame.display.set_caption('/> Shooter')
clock = pygame.time.Clock()

class Player:
  def __init__(self, x, y, width, height):
    self.x = x
    self.y =y
    self.width = width
    self.height = height
  
  def CameraUpdate(self,display):
    pygame.draw.rect(display, RED, (self.x, self.y, self.width, self.height))


class PlayerBullet:
  def __init__(self, x, y, mouse_x, mouse_y):
    self.x = x
    self.y = y
    self.mouse_x = mouse_x
    self.mouse_y = mouse_y

    self.speed = 15
    
    self.angle = math.atan2(self.mouse_y, self.mouse_x)
    self.x_vel = math.cos(self.angle) * self.speed
    self.y_vel = math.sin(self.angle) * self.speed

  def update(self,display):
    self.x -= int(self.x_vel)
    self.y -= int(self.y_vel)

    pygame.draw.circle(display, (BLACK), (self.x, self.y),5)


player = Player(640,360,32,32)

display_scroll = [0,0]

player_bullets = []


def gameLoop():
  gameExit = False
  gameOver = False

  while not gameExit:
    display.fill(GREEN)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

    pygame.draw.rect(display, WHITE, (100-display_scroll[0],100-display_scroll[1],16,16))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
      display_scroll[0] -= 5
    if keys[pygame.K_d]:
      display_scroll[0] += 5
    if keys[pygame.K_w]:
      display_scroll[1] -= 5
    if keys[pygame.K_s]:
      display_scroll[1] += 5
  

    player.CameraUpdate(display)

    for bullet in player_bullets:
      bullet.update(display)



    clock.tick(60)
    pygame.display.update()

  
gameLoop()