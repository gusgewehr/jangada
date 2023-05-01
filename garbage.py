import pygame

class Garbage(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()

        self.sheet = pygame.image.load('garbage.webp') #carrega imagem
        self.sheet.set_clip(pygame.Rect(0, 0, 1002, 692)) #define uma área retangular
        self.image = self.sheet.subsurface(self.sheet.get_clip()) #pega a área retangular definida e seta como imagem do sprite
        self.image = pygame.transform.scale(self.image, (1002 / 20, 692 / 20))
        self.rect = self.image.get_rect()

        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]