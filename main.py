# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:39:06 2022

@author: alexhou00
"""

import pygame
import sys


class Map():
    def __init__(self, screen):
        self.img = pygame.image.load("./assets/map_.png")
        self.img.convert()
        screen.blit(self.img, (0,0))
        self.dragging = False
        self.x = 0
        self.y = 0
        self.size = self.img.get_height()
        self.reload_image = 0

    def update_pos(self, X, Y):
        self.x = X
        self.y = Y

    def place(self, screen, X, Y):
        screen.fill(BGCOLOR)
        screen.blit(self.img, (X, Y))

    def touching(self, pos):
        return self.img.get_rect().collidepoint(pos)

    def resize(self, screen, percentage, pos):
        if self.reload_image >= 10:
            self.img = pygame.image.load("./assets/map_.png")
            self.img.convert()
        newX = self.size
        newY = self.size
        x, y = pos
        self.img = pygame.transform.scale(self.img, 
                                          (newX, newY))
        self.size = self.img.get_height()
        self.place(screen, percentage/100*self.x, percentage/100*self.y)
        self.reload_image += 1


pygame.init()

screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Ideal Metro Taipei")

BGCOLOR = (170, 211, 223)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BGCOLOR)

clock = pygame.time.Clock()  
running = True

bgMap = Map(background)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False      
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left button down
                if bgMap.touching(event.pos):
                    bgMap.dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = bgMap.x - mouse_x
                    offset_y = bgMap.y - mouse_y
            if event.button == 4:  # wheel up
                bgMap.resize(background, 100+3, event.pos)
            if event.button == 5:  # wheel down
                bgMap.resize(background, 100-3, event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                bgMap.dragging = False
                mouse_x, mouse_y = event.pos
                bgMap.update_pos(mouse_x + offset_x, mouse_y + offset_y)

        elif event.type == pygame.MOUSEMOTION:
            if bgMap.dragging:
                mouse_x, mouse_y = event.pos
                bgMap.place(background, mouse_x + offset_x, mouse_y + offset_y)               

    screen.blit(background, (0,0))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()
