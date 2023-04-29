import pygame

class Raft(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.sheet = pygame.image.load('raft-move.png') #carrega imagem
        self.sheet.set_clip(pygame.Rect(0, 0, 144, 188)) #define uma área retangular
        self.image = self.sheet.subsurface(self.sheet.get_clip()) #pega a área retangular definida e seta como imagem do sprite

        self.rect = self.image.get_rect()
        self.frame = 0
        self.left_states = { 0: (9, 472, 144, 188), 1: (174, 472, 144, 188), 2: (336, 472, 144, 188), 3: (500, 472, 144, 188) }
        self.down_states = { 0: (9, 47, 144, 188), 1: (174, 47, 144, 188), 2: (336, 47, 144, 188), 3: (500, 47, 144, 188) }
        self.up_states = { 0: (9, 656, 144, 188), 1: (174, 656, 144, 188), 2: (336, 656, 144, 188), 3: (500, 656, 144, 188) }
        self.right_states = { 0: (9, 243, 144, 188), 1: (174, 243, 144, 188), 2: (336, 243, 144, 188), 3: (500, 243, 144, 188) }

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
        if direction == 'left':
            self.clip(self.left_states) #chama o método clip passando a lista com as posições
            self.rect.x -= 5
        if direction == 'right':
            self.clip(self.right_states)
            self.rect.x += 5
        if direction == 'up':
            self.clip(self.up_states)
            self.rect.y -= 5
        if direction == 'down':
            self.clip(self.down_states)
            self.rect.y += 5

        #aqui ele "para" virado para o lado que estava indo
        if direction == 'stand_left':
            self.clip(self.left_states[0])
        if direction == 'stand_right':
            self.clip(self.right_states[0])
        if direction == 'stand_up':
            self.clip(self.up_states[0])
        if direction == 'stand_down':
            self.clip(self.down_states[0])

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def handle_event(self, event): #trata o evento que foi repassado pela main
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:

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

