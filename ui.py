import pygame
import sys
import json
import random
#* here is ui part

f = open("./config.json",encoding='utf-8')
CONFIG = json.loads(f.read())
print(CONFIG)
f.close()

size = width, height = (1600, 900)
SCREEN = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("微光(ui) | Glimmer - 0ojixueseno0")

HEALTH = 9

IMAGES, SOUNDS, HITMASKS = {}, {}, {}

BACKGROUND_LIST = (
  'assets/picture/background-min.png',
  'assets/picture/background2-min.png'
)

IMAGES["NUM"] = (
  pygame.image.load('assets/picture/0.png').convert_alpha(),
  pygame.image.load('assets/picture/1.png').convert_alpha(),
  pygame.image.load('assets/picture/2.png').convert_alpha(),
  pygame.image.load('assets/picture/3.png').convert_alpha(),
  pygame.image.load('assets/picture/4.png').convert_alpha(),
  pygame.image.load('assets/picture/5.png').convert_alpha(),
  pygame.image.load('assets/picture/6.png').convert_alpha(),
  pygame.image.load('assets/picture/7.png').convert_alpha(),
  pygame.image.load('assets/picture/8.png').convert_alpha(),
  pygame.image.load('assets/picture/9.png').convert_alpha()
)

IMAGES["UI"] = (
  pygame.image.load('assets/picture/startmenu.png').convert_alpha(),
  pygame.image.load('assets/picture/settingmenu.png').convert_alpha(),
  pygame.image.load('assets/picture/gamestatus.png').convert_alpha(),
  pygame.image.load('assets/picture/gameover.png').convert_alpha()
)
IMAGES["ELEMENTS"] = (
  pygame.image.load('assets/picture/wg-ball.png').convert_alpha(),
  pygame.transform.scale(pygame.image.load('assets/picture/yes.png').convert_alpha(),(45,45)),
  pygame.transform.scale(pygame.image.load('assets/picture/no.png').convert_alpha(),(45,45)),
  pygame.image.load('assets/picture/heart.png').convert_alpha(),
  pygame.image.load('assets/picture/heart_half.png').convert_alpha()
)
def updateCONFIG():
  f = open("./config.json","w",encoding='utf-8')
  f.write(json.dumps(CONFIG,indent=4,ensure_ascii=False))
  f.close()

def method(value):
    #divmod()是内置函数，返回整商和余数组成的元组
    #* 函数引用 https://www.cnblogs.com/Py00/p/9361056.html
    result = []
    while value:
        value, r = divmod(value, 10)
        result.append(r)
    # result.reverse()
    return result

class GameBackground(object):
  def __init__(self):
    self.screen = SCREEN
    self.bg1 =  pygame.transform.scale(pygame.image.load(BACKGROUND_LIST[1]).convert_alpha(),(1600,900))
    self.bg2 = pygame.transform.flip(self.bg1,True,False)
    self.bg1_rect = self.bg1.get_rect()
    self.bg2_rect = self.bg2.get_rect()
    self.x1 = 0
    self.x2 = self.x1 + self.bg2_rect.width
    # self.x1 = 1600 - self.bg1_rect.width
    # self.x2 = self.x1 - self.bg2_rect.width
  def action(self):
    self.x1 = self.x1 - 1
    self.x2 = self.x2 - 1
    if self.x1+1600 <= 0:
      self.x1 = self.x2 + self.bg1_rect.width
    if self.x2+1600 <= 0:
      self.x2 = self.x1 + self.bg2_rect.width
    # if self.x1 >= 1600:
    #     self.x1 = self.x2 - self.bg1_rect.width
    # if self.x2 >= 1600:
    #     self.x2 = self.x1 - self.bg2_rect.width

  def draw(self):
    self.screen.blit(self.bg1, (self.x1, 0))
    self.screen.blit(self.bg2, (self.x2, 0))
  

bgroll = GameBackground()

def drawscore(score):
  score = method(score)
  x=1537
  for v in score:
    if v==1:
      x=x-34+8
    else:
      x=x-34
    SCREEN.blit(IMAGES["NUM"][v], (x,36))
    # print(x)

def drawheart(health):
  half = health % 2
  full = health // 2
  if full != 0:
    for i in range(full):
      SCREEN.blit(IMAGES["ELEMENTS"][3], (40+i*67,28))
  else:
    i=-1
  if half != 0:
    SCREEN.blit(IMAGES["ELEMENTS"][4], (40+(i+1)*67,28))
  

def drawui(uipart: int):
  if uipart <= 1:
    SCREEN.blit(IMAGES["UI"][uipart], (0,0))
  else:
    SCREEN.fill((0,0,0))
  if uipart == 1:
    if CONFIG["BackgroundMusic"]:
      SCREEN.blit(IMAGES["ELEMENTS"][1], (356,234))
    else:
      SCREEN.blit(IMAGES["ELEMENTS"][2], (303,234))
    if CONFIG["BackgroundSoundEffect"]:
      SCREEN.blit(IMAGES["ELEMENTS"][1], (356,367))
    else:
      SCREEN.blit(IMAGES["ELEMENTS"][2], (303,367))
  if uipart == 2:
    bgroll.action()
    bgroll.draw()
    SCREEN.blit(IMAGES["UI"][2], (0,0))
    drawheart(HEALTH)
    drawscore(1234567890987654321)
    # pygame.draw.line(SCREEN, (0,0,0), (0,100),(1600,100),3)
    # pygame.draw.line(SCREEN, (0,0,0), (0,800),(1600,800),3)
    pass

def clickCheck(pos,x,y,w,h) -> bool:
  return (x+w >= pos[0] >= x and y+h >= pos[1] >= y)

def clickEvent(uipart, pos) -> int:
  if uipart == 0: #* StartMenu
    if clickCheck(pos, 600, 395, 400, 65):
      print("gamestart")
      return 2
    if clickCheck(pos, 600, 500, 400, 65):
      return 1
    if clickCheck(pos, 600, 605, 400, 65):
      pygame.quit()
  if uipart == 1: #* settingMenu
    if clickCheck(pos, 47, 782, 190, 61):
      return 0
    if clickCheck(pos, 295, 230, 115, 53):
      CONFIG["BackgroundMusic"] = not CONFIG["BackgroundMusic"]
      updateCONFIG()
    if clickCheck(pos, 295, 363, 115, 53):
      CONFIG["BackgroundSoundEffect"] = not CONFIG["BackgroundSoundEffect"]
      updateCONFIG()
  return uipart

def main():
  global HEALTH
  uipart = 0
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        uipart = clickEvent(uipart,event.pos)
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
        HEALTH -= 1
        # print(HEALTH)
    drawui(uipart)
    pygame.display.update()


if __name__ == "__main__":
  main()