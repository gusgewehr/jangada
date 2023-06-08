import pygame
import islands

class Raft(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.moving = False

        self.frame = 0
        self.frame_change = 0
        self.left_states = { 0: (9, 472, 144, 188), 1: (174, 472, 144, 188), 2: (336, 472, 144, 188), 3: (500, 472, 144, 188) }
        self.down_states = { 0: (9, 47, 144, 188), 1: (174, 47, 144, 188), 2: (336, 47, 144, 188), 3: (500, 47, 144, 188) }
        self.up_states = { 0: (9, 656, 144, 188), 1: (174, 656, 144, 188), 2: (336, 656, 144, 188), 3: (500, 656, 144, 188) }
        self.right_states = { 0: (9, 243, 144, 188), 1: (174, 243, 144, 188), 2: (336, 243, 144, 188), 3: (500, 243, 144, 188) }

        self.state = self.right_states

        self.change_image(self.state)

        self.rect = self.image.get_rect()

        self.center = pygame.math.Vector2(144/2, 188/2)

    def get_frame(self, frame_set): #este método simplesmente vai alterando o índice
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect): #recebe a lista de posiçoes ou somente a primeira posição
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect)) #define que o clip será um retangulo das posições definidas 
        return clipped_rect

    def update(self, direction):
        state_ant = self.state
        self.frame_change += 1
        moving_ant = self.moving


        if direction == 'left':
            self.rect.x -= 5
            self.moving = True
            self.state = self.left_states
        if direction == 'right':
            self.rect.x += 5
            self.moving = True
            self.state = self.right_states
        if direction == 'up':
            self.rect.y -= 5
            self.moving = True
            self.state = self.up_states
        if direction == 'down':
            self.rect.y += 5
            self.moving = True
            self.state = self.down_states

        #aqui ele "para" virado para o lado que estava indo
        if direction == 'stand_left':
            self.moving = False
            self.state = self.left_states
        if direction == 'stand_right':
            self.moving = False
            self.state = self.right_states
        if direction == 'stand_up':
            self.moving = False
            self.state = self.up_states
        if direction == 'stand_down':
            self.moving = False
            self.state = self.down_states

        if (moving_ant != self.moving) :
            self.change_image(self.state)

        if self.frame_change > 10 or state_ant != self.state:
            self.frame_change = 0
            self.clip(self.state)
        
        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def handle_event(self, event): #trata o evento que foi repassado pela main
        #print(event)
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN: #temos q impedir q a jangada atravesse as ilhas

            if event.key == pygame.K_LEFT:
                self.update('left') #chama o método update passando um parâmetro
            if event.key == pygame.K_RIGHT:
                self.update('right')
            if event.key == pygame.K_UP:
                self.update('up')
            if event.key == pygame.K_DOWN:
                self.update('down')

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')

    def change_image(self, clipped_rect):
        self.sheet = pygame.image.load('raft-move.webp' if self.moving else 'raft_idle.webp') #carrega imagem
        self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        self.image = self.sheet.subsurface(self.sheet.get_clip()) #pega a área retangular definida e seta como imagem do sprite