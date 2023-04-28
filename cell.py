import pygame
from pygame.locals import *
from random import choice

class Cell(pygame.sprite.Sprite):

    def __init__(self, type):
        self.type = ""
        self.type_sprites = {
            'water': (0, 0, 255),
            'grass': (0,255,0),
            'boat': (139,69,19)
        }
        self.size = (50,50)
        self.width = 2
        self.cells_matrix = {}
        pygame.sprite.Sprite.__init__(self)

    
    def handle_event(self, screen,event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                index = (event.pos[0] // self.size[0], event.pos[1] // self.size[1])
                pos = self.cells_matrix[index]
                pygame.draw.rect(screen, self.type_sprites['boat'], Rect(pos, self.size))

    def build_grid(self, screen):
        for width in range(screen.get_width()):
            for height in range(screen.get_height()):
                random_color = choice(['water', 'grass', 'boat'])
                pos = (self.size[0]*width, self.size[1]*height)
                self.cells_matrix[(width,height)] = pos
                
                pygame.draw.rect(screen, self.type_sprites[random_color], Rect(pos, self.size))                

        
            
        

    


    








