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

# 滚动背景
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

# 主要绘制
class MainDraw(object):
  def __init__(self):
    self.uipart = 0

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
      pygame.image.load('assets/picture/heart_half.png').convert_alpha()
    )

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

# 主场景
class MainScene(object):
  # 初始化主场景
  def __init__(self):
    # 游戏尺寸
    self.size = (1600,900)
    # 场景对象
    self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
    # 窗口标题
    pygame.display.set_caption("Glimmer - 微光")
    # 窗口logo
    pygame.display.set_icon(pygame.image.load('assets/logo.png').convert_alpha())
    #* 连接其他class

  # 绘制
  def draw_elements(self):
    pass

  # 动作
  def action_elements(self):
    pass

   # 处理事件
  def handle_event(self):
    pass

  # 碰撞检测
  def detect_crash(self):
    pass

  # 主循环
  def run_loop(self):
    pass

# 程序入口
if __name__ == "__main__":
  mainScene = MainScene()
  mainScene.run_loop()