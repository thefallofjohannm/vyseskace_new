from config import *
import pygame

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, velocity):
        super().__init__()

        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity

    def update(self):
        self.rect.y += self.velocity
        if self.rect.top <= 50:
            self.velocity *= -1
        if self.rect.bottom > 610:
            self.velocity *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
