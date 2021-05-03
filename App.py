import pygame
import sys
import time
import random
import json
import os

'''
                            _ooOoo_
                           o8888888o
                           88" . "88
                           (| -_- |)
                            O\ = /O
                        ____/`---'\____
                      .   ' \\| |// `.
                       / \\||| : |||// \
                     / _||||| -:- |||||- \
                       | | \\\ - /// | |
                     | \_| ''\---/'' | |
                      \ .-\__ `-` ___/-. /
                   ___`. .' /--.--\ `. . __
                ."" '< `.___\_<|>_/___.' >'"".
               | | : `- \`.;`\ _ /`;.`/ - ` : | |
                 \ \ `-. \_ __\ /__ _/ .-` / /
         ======`-.____`-.___\_____/___.-`____.-'======
                            `=---='

         .............................................
                  佛祖保佑             永无BUG
                   希望人没事 -- 0ojixueseno0
'''

# 资源文件
class Assets(object):
  def __init__(self):
    self.images, self.sounds = {}, {}
    # 游戏背景
    self.background_list = (
      'assets/picture/background-min.png',
      'assets/picture/background2-min.png'
    )
    # 数字字体
    self.images["NUM"] = (
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
    # UI界面
    self.images["UI"] = (
      pygame.image.load('assets/picture/startmenu.png').convert_alpha(),
      pygame.image.load('assets/picture/settingmenu.png').convert_alpha(),
      pygame.image.load('assets/picture/gamestatus.png').convert_alpha(),
      pygame.image.load('assets/picture/gameover.png').convert_alpha()
    )
    # 组件
    self.images["ELEMENTS"] = (
      pygame.image.load('assets/picture/wg-ball.png').convert_alpha(),
      pygame.transform.scale(pygame.image.load('assets/picture/yes.png').convert_alpha(),(45,45)),
      pygame.transform.scale(pygame.image.load('assets/picture/no.png').convert_alpha(),(45,45)),
      pygame.image.load('assets/picture/heart.png').convert_alpha(),
      pygame.image.load('assets/picture/heart_half.png').convert_alpha(),
      #* 障碍物
      pygame.image.load('assets/picture/cloud.png').convert_alpha(),
      pygame.image.load('assets/picture/airplane.png').convert_alpha(),
      pygame.image.load('assets/picture/skyisland.png').convert_alpha(),
      pygame.image.load('assets/picture/stree.png').convert_alpha(),
      pygame.image.load('assets/picture/ttree.png').convert_alpha(),
      pygame.image.load('assets/picture/built.png').convert_alpha()

    )
    #音效
    
    self.sounds["bgm"] = pygame.mixer.Sound('assets/sounds/bgm.mp3')
    self.sounds["jump"] = pygame.mixer.Sound('assets/sounds/jump.wav')
    self.sounds["gameover"] = pygame.mixer.Sound('assets/sounds/gameover.mp3')
    self.sounds["switch"] = pygame.mixer.Sound('assets/sounds/switch.mp3')
    self.sounds["pickheart"] = pygame.mixer.Sound('assets/sounds/pickheart.ogg')

# 配置文件
class Config(object):
  def __init__(self):
    #* 配置文件读取/生成
    self.config = {
      "BackgroundMusic": True,
      "BackgroundSoundEffect": True
    }
    if not os.path.exists("./config.json"):
      self.updateCONFIG()
    with open("./config.json",'r',encoding='utf-8') as f:
      self.config = json.loads(f.read())

  def updateCONFIG(self):
    with open("./config.json",'w',encoding='utf-8') as f:
      f.write(json.dumps(self.config,indent=4,ensure_ascii=False))

# 精灵
class GSprite(pygame.sprite.Sprite):
  def __init__(self, image, speed=1):
    pygame.sprite.Sprite.__init__(self)
    self.image = image
    self.rect = self.image.get_rect()
    self.speed = speed

  # #X 属性
  # def _getx(self): return self.rect.x
  # def _setx(self,value): self.rect.x = value
  # X = property(_getx,_setx)

  # #Y 属性
  # def _gety(self): return self.rect.y
  # def _sety(self,value): self.rect.y = value
  # Y = property(_gety,_sety)

  #position 属性
  def _getpos(self): return self.rect.topleft
  def _setpos(self,pos): self.rect.topleft = pos
  position = property(_getpos,_setpos)

class Player(object):
  def __init__(self,screen):
    self.screen = screen
    #* 玩家变量
    self.score = 0                      # 初始得分
    self.health = 9                     # 初始血量
    self.onground = False               # 是否触地
    self.gravity = 0.5                  # 重力
    self.friction = 1                   # 摩擦力
    self.speed = 1                      # 重力速度
    self.hurttime = self.screen.fps * 3 # 受伤后的无敌时间(s)
    
    # 精灵组
    self.player_group = pygame.sprite.Group()
    # 玩家初始化
    self.player = GSprite(screen.assets.images["ELEMENTS"][0], speed = self.speed)
    self.player.position = (400,800)
    self.player_group.add(self.player)


  #TODO: voice
  def Jump(self):
    print("Jump")
    if self.onground:
      self.onground = False
      self.speed = -32 * self.gravity
  
  def Switch(self):
    print("Switch")
    if self.onground:
      self.onground = False
      self.gravity *= -1

  # 重力 摩擦力计算
  def Action(self):
    self.speed *= self.friction # 空气摩擦
    self.speed += self.gravity # 重力加速度
    self.player.rect.y += self.speed #! 让它动!!!
    if self.player.rect.top < 100 or self.player.rect.bottom > self.screen.height - 100:
      if abs(self.speed) > 4:
        self.speed *= -0.3
      else:
        self.speed = 0
    self.player.rect.top = min(max(self.player.rect.top,100),self.screen.height-100)
    self.player.rect.bottom = min(max(self.player.rect.bottom,100), self.screen.height-100)
    if self.speed == 0:
      self.onground = True


# 点击事件判断
class ClickEvent(object):
  def __init__(self, screen):
    self.screen = screen

  def clickCheck(self,pos,x,y,w,h) -> bool:
    return (x+w >= pos[0] >= x and y+h >= pos[1] >= y)

  def LeftClick(self, pos):
    if self.screen.mainDraw.uipart == 0: #* StartMenu
      print(pos)
      if self.clickCheck(pos, 600, 395, 400, 65):
        self.screen.mainDraw.uipart = 2
      if self.clickCheck(pos, 600, 500, 400, 65):
        self.screen.mainDraw.uipart = 1
      if self.clickCheck(pos, 600, 605, 400, 65):
        pygame.quit()
    if self.screen.mainDraw.uipart == 1: #* settingMenu
      if self.clickCheck(pos, 47, 782, 190, 61):
        self.screen.mainDraw.uipart = 0
      if self.clickCheck(pos, 295, 230, 115, 53):
        self.screen.config.config["BackgroundMusic"] = not self.screen.config.config["BackgroundMusic"]
        self.screen.config.updateCONFIG()
      if self.clickCheck(pos, 295, 363, 115, 53):
        self.screen.config.config["BackgroundSoundEffect"] = not self.screen.config.config["BackgroundSoundEffect"]
        self.screen.config.updateCONFIG()

# 滚动背景
class GameBackground(object):
  def __init__(self, screen):
    self.screen = screen
    self.bg1 =  pygame.transform.scale(
      pygame.image.load(
        self.screen.assets.background_list[random.randint(0,len(self.screen.assets.background_list)-1)]
        ).convert_alpha(),(1600,900))
    self.bg2 = pygame.transform.flip(self.bg1,True,False)
    self.bg1_rect = self.bg1.get_rect()
    self.bg2_rect = self.bg2.get_rect()
    self.x1 = 0
    self.x2 = self.x1 + self.bg2_rect.width

  def action(self):
    self.x1 = self.x1 - 1
    self.x2 = self.x2 - 1
    if self.x1+1600 <= 0:
      self.x1 = self.x2 + self.bg1_rect.width
    if self.x2+1600 <= 0:
      self.x2 = self.x1 + self.bg2_rect.width

  def draw(self):
    self.screen.scene.blit(self.bg1, (self.x1, 0))
    self.screen.scene.blit(self.bg2, (self.x2, 0))

# 处理各种动作
class MainAction(object):
  def __init__(self, screen):
    self.screen = screen
    
  def Actions(self):
    if self.screen.mainDraw.uipart == 2:
      self.screen.roolBG.action() # 背景滚动
      
      #* 玩家数值
      self.screen.player.Action()
      
    pass

# 主要绘制
class MainDraw(object):
  def __init__(self, screen):
    self.uipart = 0
    self.screen = screen
  
  def method(self, value):
    """
    输入数字 倒序输出每位内容
    """
    result = []
    while value:
      value, r = divmod(value, 10)
      result.append(r)
    return result

  def drawscore(self):
    if self.screen.player.score == 0:
      self.screen.scene.blit(self.screen.assets.images["NUM"][0], (1537, 36))
    score = self.method(self.screen.player.score)
    x = 1537
    for v in score:
      if v == 1:
        x = x - 34 + 8
      else:
        x = x - 34
      self.screen.scene.blit(self.screen.assets.images["NUM"][v], (x, 36))

  def drawheart(self):
    health = self.screen.player.health
    if health > 0:
      half = health % 2
      full = health // 2
      if full != 0:
        for i in range(full):
          self.screen.scene.blit(self.screen.assets.images["ELEMENTS"][3], (40+i*67,28))
      else:
        i=-1
      if half != 0:
        self.screen.scene.blit(self.screen.assets.images["ELEMENTS"][4], (40+(i+1)*67,28))
  
  def DrawUI(self):
    if self.uipart <= 1:
      self.screen.scene.blit(self.screen.assets.images["UI"][self.uipart], (0,0))
    else:
      self.screen.scene.fill((0,0,0))
    if self.uipart == 1: # SettingMenu
      if self.screen.config.config["BackgroundMusic"]:
        self.screen.scene.blit(self.screen.assets.images["ELEMENTS"][1], (356,234))
      else:
        self.screen.scene.blit(self.screen.assets.images["ELEMENTS"][2], (303,234))
      if self.screen.config.config["BackgroundSoundEffect"]:
        self.screen.scene.blit(self.screen.assets.images["ELEMENTS"][1], (356,367))
      else:
        self.screen.scene.blit(self.screen.assets.images["ELEMENTS"][2], (303,367))
    if self.uipart == 2: # GamePart
      # self.screen.roolBG.action()
      #TODO: draw ball
      self.screen.roolBG.draw()
      self.screen.scene.blit(self.screen.assets.images["UI"][2], (0,0))
      self.drawheart()
      self.drawscore()
      # self.screen.player.player_group.draw(self.screen.scene)
      self.screen.scene.blit(self.screen.player.player.image, self.screen.player.player.rect)

# 主场景
class MainScene(object):
  # 初始化主场景
  def __init__(self):
    # 游戏尺寸
    self.size = self.width, self.height = (1600,900)
    # 场景对象
    self.scene = pygame.display.set_mode([self.size[0], self.size[1]])

    pygame.init()
    # 窗口标题
    pygame.display.set_caption("Glimmer - 微光")
    # 窗口logo
    pygame.display.set_icon(pygame.image.load('assets/logo.png').convert_alpha())

    # 帧率
    self.fps = 120
    self.fclock = pygame.time.Clock()

    # 调试模式
    self.debug = False

    # pygame.mixer.init()

    #* 连接其他class
    self.assets = Assets()              # 资源文件
    self.config = Config()              # 配置文件
    # self.gsprite = GSprite(self)
    self.player = Player(self)          # 玩家信息
    self.clickEvent = ClickEvent(self)  # 点击事件
    self.roolBG = GameBackground(self)  # 滚动背景
    self.mainDraw = MainDraw(self)      # 绘制
    self.mainAction = MainAction(self)  # 动作



  # 绘制
  def draw_elements(self):
    self.mainDraw.DrawUI()
    pass

  # 动作
  def action_elements(self):
    self.mainAction.Actions()
    pass

   # 处理事件
  def handle_event(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        self.clickEvent.LeftClick(event.pos)
      if event.type == pygame.KEYDOWN and self.mainDraw.uipart == 2:
        self.player.friction = 1
        if event.key == pygame.K_SPACE:
          self.player.Switch()
        elif event.key == pygame.K_UP:
          self.player.Jump()
      elif event.type == pygame.KEYUP and self.mainDraw.uipart == 2:
        self.player.friction = 0.99
    pass

  # 碰撞检测
  def detect_crash(self):
    pass

  # 主循环
  def run_loop(self):
    while True:
      self.action_elements()
      self.draw_elements()
      self.handle_event()
      self.detect_crash()
      pygame.display.update()
      self.fclock.tick(self.fps)

# 程序入口
if __name__ == "__main__":
  mainScene = MainScene()
  mainScene.run_loop()