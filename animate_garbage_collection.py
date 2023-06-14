import pygame
import random


class AnimateGarbageColletion(pygame.sprite.Sprite):

    def __init__(self, start_pos, end_pos, time, type):
        super().__init__()

        self.type = type

        self.clip_dict  = {
            "Eletrônico": [pygame.Rect(24,21,95,117),#celular
                           pygame.Rect(175,20,75,149),#pilha
                           pygame.Rect(317,40,64,92),#lampada                
            ],
            "Plástico": [pygame.Rect(443,24,163,183),#sacola
                           pygame.Rect(684,30,95,159),#garrafa_amassada
                           pygame.Rect(875,32,70,101),#garrafa
                
                 
            ],
            "Metal": [pygame.Rect(1016,47,162,134),#lata
                           pygame.Rect(1257,53,85,110),#refri
                           pygame.Rect(1427,71,74,92),#lampada
                 
            ],
            "Vidro": [pygame.Rect(6,300,140,194),#suco
                           pygame.Rect(251,268,106,233),#vinho
                           pygame.Rect(435,325,75,108),#lata_amassada
                 
            ],
            "Papel": [pygame.Rect(635,301,172,166),#jornal
                           pygame.Rect(845,320,175,109),#caixa
                           pygame.Rect(1085,327,77,92),#papel
                 
            ],
            "Orgânico": [pygame.Rect(1245,289,104,163),#melancia
                           pygame.Rect(1403,288,137,149),#banana
                           pygame.Rect(1602,314,79,107),#ovo
                 
            ]
        }

        self.sprite = random.choice(self.clip_dict[self.type])

        self.sheet = pygame.image.load('garbage.png') #carrega imagem
        self.sheet.set_clip(self.sprite)
        #self.sheet.set_clip(pygame.Rect(0, 0, 1002, 692)) #define uma área retangular
        self.image = self.sheet.subsurface(self.sheet.get_clip()) #pega a área retangular definida e seta como imagem do sprite
        self.image = pygame.transform.scale(self.image, (self.sprite.size[0]/2.5, self.sprite.size[1]/2.5))
        self.rect = self.image.get_rect()

        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]


        self.route = []

        for t in range(time+1,1, -1):
            delta_pos_x = end_pos[0] - start_pos[0]
            cur_pos_x = start_pos[0]+(delta_pos_x/t)
            delta_pos_y = end_pos[1] - start_pos[1]
            cur_pos_y = start_pos[1]+(delta_pos_y/t)
            self.route.append([cur_pos_x,cur_pos_y])

        
    def update_frame(self, frame):
        cur_pos = self.route[frame]
        self.rect.x = cur_pos[0]
        self.rect.y = cur_pos[1]
        #self.image = pygame.transform.scale(self.image, (self.sprite.size[0]/(2.5*frame), self.sprite.size[1]/2.5*frame))