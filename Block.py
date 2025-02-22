from config import *
import pygame
import random

class Block:  # fake bloky, aby zmátly hráče a bylo to celkově více zákeřné

    def __init__(self, screen, y):
        self.screen = screen
        self.width = 15
        self.height = 10
        self.color = BLUE2
        self.position_x = random.randint(self.width, screen.get_width() - self.width)  # ohraničení, aby nebyly všude
        self.position_y = y

    def draw(self):
        pygame.draw.rect(self.screen,
                         self.color,
                         [self.position_x, self.position_y, self.width, self.height],
                         10)

    def shift(self):
        self.position_y += 1  # posouvání bloku
