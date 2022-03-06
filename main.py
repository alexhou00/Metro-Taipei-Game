# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:39:06 2022

@author: alexhou00
"""

import pygame
import sys

# To Do:
# 


class Map():
    sc = 0

    def __init__(self, screen, start_x, start_y):
        self.sc = screen
        self.img = pygame.image.load("./assets/map_.png")
        self.img.convert()
        self.sc.blit(self.img, (start_x, start_y))
        self.dragging = False
        self.x = start_x
        self.y = start_y
        self.size = 100
        self.width = self.img.get_height()
        self.reload_image = 0

    def update_pos(self, X, Y):
        self.x = X
        self.y = Y

    def place(self, X, Y):
        self.sc.fill(BGCOLOR)
        self.sc.blit(self.img, (X, Y))

    def go_to(self, X, Y):
        x, y = X, Y
        if x > 0: x = 0
        if y > 0: y = 0
        if x < SCREEN_WIDTH - self.width: x = SCREEN_WIDTH - self.width
        if y < SCREEN_HEIGHT - self.width: y = SCREEN_HEIGHT - self.width
        self.place(x, y)
        self.update_pos(x, y)

    def touching_point(self, pos):
        return self.img.get_rect().collidepoint(pos)

    def resize(self, dsize, mouse_pos=(0,0)):
        # For example if dsize is 3
        # Then the new_size will be 1.03 * old_size
        if self.reload_image >= 10:
            self.img = pygame.image.load("./assets/map_.png")
            self.img.convert()
        ratio = 1+dsize/100
        new_width = self.width*ratio  # Restrict from out of border
        if new_width < SCREEN_WIDTH:
            new_width = SCREEN_WIDTH
        elif new_width < SCREEN_HEIGHT:
            new_width = SCREEN_HEIGHT  # end Restrict
        mouse_x, mouse_y = mouse_pos
        self.img = pygame.transform.scale(self.img, (new_width, new_width))
        self.width = self.img.get_height()
        self.go_to(  # Let the image scale (resize) around mouse pointer
            self.x-(mouse_x-self.x)*(ratio-1),  # This is Meth
            self.y-(mouse_y-self.y)*(ratio-1)   # Draw it and you'll figure out why
        )
        self.reload_image += 1


class Station(pygame.sprite.Sprite):
    def __init__(self):
        self.pos = (0,0)
        self.people = 0
        self.capacity = 50


class Train(pygame.sprite.Sprite):
    def __init__(self):
        self.people = 0


pygame.init()

BGCOLOR = (170, 211, 223)
BGCOLOR = (255, 255, 255)
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ideal Metro Taipei")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BGCOLOR)

clock = pygame.time.Clock()  
running = True

bgMap = Map(background, -1131, -1734)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False      
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left button down
                if bgMap.touching_point(event.pos):
                    bgMap.dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = bgMap.x - mouse_x
                    offset_y = bgMap.y - mouse_y
            if event.button == 4:  # wheel up
                bgMap.resize(3, mouse_pos=event.pos)
            if event.button == 5:  # wheel down
                bgMap.resize(-3, mouse_pos=event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                print(f"Map:(%.6f, %.6f); Mouse:{event.pos}" % (bgMap.x, bgMap.y))
            if event.button == 1:            
                bgMap.dragging = False
                mouse_x, mouse_y = event.pos
                bgMap.go_to(mouse_x + offset_x, mouse_y + offset_y)

        elif event.type == pygame.MOUSEMOTION:
            if bgMap.dragging:
                mouse_x, mouse_y = event.pos
                bgMap.go_to(mouse_x + offset_x, mouse_y + offset_y)

    screen.blit(background, (0,0))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()
