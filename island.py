import pygame

class Island(pygame.sprite.Sprite):
    def __init__(self, name, start_pos):
        super().__init__()

        self.sheet = pygame.image.load(name) #carrega imagem
        self.sheet.set_clip(pygame.Rect(0, 0, 1024, 1024)) #define uma área retangular
        self.image = self.sheet.subsurface(self.sheet.get_clip()) #pega a área retangular definida e seta como imagem do sprite
        self.image = pygame.transform.scale(self.image, (1024, 1024))
        self.rect = self.image.get_rect()

        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]