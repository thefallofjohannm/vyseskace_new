from config import *
import random
import pygame

#původně to měla být mince, ale pak jsem to předělal na diamant

class Coin(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        diamond_points = [(10, 0), (30, 0), (40, 10), (20, 30), (0,10)]
        pygame.draw.polygon(self.image, COIN, diamond_points)
        #coin je nakonec diamond a je to udělané pomoci polygondraw,
        #takže jsou nadefinované body pro pentagon a to je pak vykresleno

        self.rect = self.image.get_rect() #obalim do čtverce
        self.screen = screen
        self.spawn()

    def spawn(self):
        x = random.randint(10, 1050) #omezení, kde se to může objevit
        y = random.randint(10, 550)
        self.rect.topleft = (x, y)

    def draw(self):
        self.screen.blit(self.image, self.rect)
