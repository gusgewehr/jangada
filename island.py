import pygame
import random

class Island(pygame.sprite.Sprite):
    def __init__(self, start_pos, type):
        super().__init__()

        #type_options = ["Eletrônico", "Plástico", "Metal", "Vidro", "Papel", "Orgânico"]

        #type = random.choices(type_options)

        self.item_drop_timer = 0

        self.type = type


        img_dict  = {
            "Eletrônico": ['ilha_eletronico.png'],
            "Plástico": ["ilha_plastico.png"],
            "Metal": ['ilha_metal.png'],
            "Vidro": ['ilha_vidro.png',],
            "Papel": ['ilha_papel.png',],
            "Orgânico": ['ilha_organico.png',]
        }

        sprite = random.choice(img_dict[self.type])

        self.sheet = pygame.image.load('islands/novas_ilhas/'+sprite) #carrega imagem
        self.sheet.set_clip(pygame.Rect(0, 0, 500, 500)) #define uma área retangular
        self.image = self.sheet.subsurface(self.sheet.get_clip()) #pega a área retangular definida e seta como imagem do sprite
        #self.image = pygame.transform.scale(self.image, (1024, 1024))
        self.rect = self.image.get_rect()

        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]


        # def block_raft_movement(self, direction):

        #     if direction == 'left' and self.rect.x > 0 and colliding:

        #     if direction == 'right':
        #     if direction == 'up':
        #     if direction == 'down':
            
