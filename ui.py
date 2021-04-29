import pygame
import sys
import json
#* here is ui part

f = open("./config.json",encoding='utf-8')
CONFIG = json.loads(f.read())
print(CONFIG)
f.close()

size = width, height = (1600, 900)
SCREEN = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("微光(ui) | Glimmer - 0ojixueseno0")

IMAGES, SOUNDS, HITMASKS = {}, {}, {}

BACKGROUND_LIST = (
  'assets/picture/background-min.png',
  'assets/picture/background2-min.png'
)

IMAGES["UI"] = (
  pygame.image.load('assets/picture/startmenu.png').convert_alpha(),
  pygame.image.load('assets/picture/settingmenu.png').convert_alpha(),
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

def drawui(uipart: int):
  SCREEN.blit(IMAGES["UI"][uipart], (0,0))
  if uipart == 1:
    if CONFIG["BackgroundMusic"]:
      SCREEN.blit(IMAGES["ELEMENTS"][1], (356,234))
    else:
      SCREEN.blit(IMAGES["ELEMENTS"][2], (303,234))
    if CONFIG["BackgroundSoundEffect"]:
      SCREEN.blit(IMAGES["ELEMENTS"][1], (356,367))
    else:
      SCREEN.blit(IMAGES["ELEMENTS"][2], (303,367))
    

def clickCheck(pos,x,y,w,h) -> bool:
  return (x+w >= pos[0] >= x and y+h >= pos[1] >= y)

def clickEvent(uipart, pos) -> int:
  if uipart == 0: #* StartMenu
    if clickCheck(pos, 600, 395, 400, 65):
      print("gamestart")
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
  uipart = 0
  while uipart <= 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        uipart = clickEvent(uipart,event.pos)
    
    drawui(uipart)
    pygame.display.update()


if __name__ == "__main__":
  main()