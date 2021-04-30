import pygame
import sys  # 导入pygame
import time
import random

pygame.init()
vInfo = pygame.display.Info()  # 查看屏幕信息
"""
pygame.display.Info()
current_w: 当前显示模式或窗口的像素宽度
current_h: 当前显示模式或窗口的像素高度
#tip: 在.set_mode()之前调用，则显示当前系统显示的参数信息
"""
size = width, height = (1600, 900)
# size = width, height = 600, 400
speed = [1, 1]
BLACK = 255, 255, 255
# screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
# screen = pygame.display.set_mode(size, pygame.RESIZABLE)
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("微光 | Glimmer - 0ojixueseno0")
ball = pygame.image.load("assets/picture/wg-ball.png").convert_alpha()
ballrect = ball.get_rect()
ballrect = ballrect.move(400, 800)
fps = 120
fclock = pygame.time.Clock()

gravity = 0.5
friction = 1
onground = False

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      # if event.key == pygame.K_LEFT:
      #   speed[0] = speed[0] if speed[0] == 0 else (abs(speed[0]) - 1)*int(speed[0]/abs(speed[0]))
      #   print(speed[0])
      # elif event.key == pygame.K_RIGHT:
      #   speed[0] = speed[0] + 1 if speed[0] > 0 else speed[0] - 1
      #   print(speed[0])
      if event.key == pygame.K_SPACE:
        if onground:
          onground = False
          gravity *= -1
      elif event.key == pygame.K_UP:
        if onground:
          onground = False
          speed[1] = -32 * gravity
          print(speed[1])
      # elif event.key == pygame.K_DOWN:
      #   speed[1] = speed[1] if speed[1] == 0 else (abs(speed[1]) - 1)*int(speed[1]/abs(speed[1]))
      #   print(speed[1])
      elif event.key == pygame.K_ESCAPE:
        sys.exit()
      friction = 1
    elif event.type == pygame.KEYUP:
      friction = 0.99
    speed[0] = speed[0] * 0.92
    speed = [friction * s for s in speed]

  speed[1] += gravity

  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  ballrect = ballrect.move(speed[0], speed[1])
  if ballrect.top < 0 or ballrect.bottom > height:
    if abs(speed[1]) > 4:
      speed[1] = -speed[1] * 0.3
    else:
      speed[1] = 0
  ballrect.top = min(max(ballrect.top, 0), height)
  ballrect.bottom = min(max(ballrect.bottom, 0), height)
  print(speed)
  if speed[1] == 0:
    onground = True
  # time.sleep(0.01)

  screen.fill(BLACK)
  screen.blit(ball, ballrect)
  pygame.display.update()
  fclock.tick(fps)
