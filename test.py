# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 12:39:06 2022

@author: alexhou00
"""

import pygame
import sys
import random

# 全局定義
SCREEN_X = 600
SCREEN_Y = 600


# 蛇類
# 點以25為單位
class Snake(object):
    # 初始化各種需要的屬性 [開始時默認向右/身體塊x5]
    def __init__(self):
        self.dirction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.addnode()
        
    # 無論何時 都在前端增加蛇塊
    def addnode(self):
        left,top = (0,0)
        if self.body:
            left,top = (self.body[0].left,self.body[0].top)
        node = pygame.Rect(left,top,25,25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0,node)
        
    # 删除最後一塊
    def delnode(self):
        self.body.pop()
        
    # 死亡判断
    def isdead(self):
        # 撞牆
        if self.body[0].x  not in range(SCREEN_X):
            return True
        if self.body[0].y  not in range(SCREEN_Y):
            return True
        # 撞自己
        if self.body[0] in self.body[1:]:
            return True
        return False
        
    # 移動
    def move(self):
        self.addnode()
        self.delnode()
        
    # 改變方向 但是左右、上下不能被逆向改變
    def changedirection(self,curkey):
        LR = [pygame.K_LEFT,pygame.K_RIGHT]
        UD = [pygame.K_UP,pygame.K_DOWN]
        if curkey in LR+UD:
            if (curkey in LR) and (self.dirction in LR):
                return
            if (curkey in UD) and (self.dirction in UD):
                return            
            self.dirction = curkey
       
       
# 食物類
# 方法： 放置/移除
# 點以25為單位
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25,0,25,25)
        
    def remove(self):
        self.rect.x=-25
    
    def set(self):
        if self.rect.x == -25:
            allpos = []
            # 不靠牆太近 25 ~ SCREEN_X-25 之间
            for pos in range(25,SCREEN_X-25,25):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            self.rect.top  = random.choice(allpos)
            #print(self.rect)
            
class Station:
    def __init__(self):
        self.pos = (0,0)
        self.people = 0
        
class Train:
    def __init__(self):
        self.people = 0


    
def show_text(screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):   
    #獲取系统字體，並設置文字大小  
    cur_font = pygame.font.SysFont("微軟正黑體", font_size)  
    #設置是否加粗屬性  
    cur_font.set_bold(font_bold)  
    #設置是否斜體屬性  
    cur_font.set_italic(font_italic)  
    #設置文字内容  
    text_fmt = cur_font.render(text, 1, color)  
    #繪製文字  
    screen.blit(text_fmt, pos)

     
def main():
    pygame.init()
    screen_size = (SCREEN_X,SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Metro Taipei')
    clock = pygame.time.Clock()
    #scores = 0
    isdead = False
    #pygame.mixer.init()
    #pygame.mixer.music.load('media\\Despacito.mp3')
    #pygame.mixer.music.play(loops=-1)
    #soundfood = pygame.mixer.Sound('media\\Boing0.wav')
    
    
    
    # 蛇/食物
    snake = Snake()
    #food = Food()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.changedirection(event.key)
                # 死後按space重新
                if event.key == pygame.K_SPACE and isdead:
                    return main()
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                
            
        screen.fill((255,255,255))
        '''
        # 畫蛇身 / 每一步+1分
        if not isdead:
            scores+=1
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen,(20,220,39),rect,0)
            pygame.draw.line(screen, (0, 100, 255), (0, 0), (SCREEN_X, 0), 1)
            
        # 顯示死亡文字
        isdead = snake.isdead()
        if isdead:
            show_text(screen,(100,200),'YOU DEAD!',(227,29,18),False,100)
            show_text(screen,(150,260),'press space to try again...',(0,0,22),False,30)
            
        # 食物處理 / 吃到+50分
        # 當食物rect與蛇頭重合,吃掉 -> Snake增加一個Node
        if food.rect == snake.body[0]:
            scores+=50
            food.remove()
            snake.addnode()
            soundfood.play()
        
        # 食物投遞
        food.set()
        pygame.draw.rect(screen,(136,0,21),food.rect,0)
        
        # 顯示分數文字
        show_text(screen,(50,500),'Score: '+str(scores),(215,215,215))
        show_text(screen,(50,550),'Difficulty:40%',(200,200,200),True,40)
        '''
        pygame.display.update()
        clock.tick(30)
    
    
if __name__ == '__main__':
    main()
