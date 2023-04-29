import pygame

states = {
    'left': (324, 25, 162, 191),
    'stand_left': (324, 251, 162, 191),
    'right': (165, 18, 162, 191),
    'stand_right': (165, 245, 162, 191),
    'up': (485, 0, 162, 191),
    'stand_up': (485, 209, 162, 191),
    'down': (7, 30, 162, 191),
    'stand_down': (7, 257, 162, 191),
}

class Raft(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.sheet = pygame.image.load('raft.gif') #carrega imagem
        self.sheet.set_clip(pygame.Rect(0, 0, 162, 191)) #define uma área retangular
        self.image = self.sheet.subsurface(self.sheet.get_clip()) #pega a área retangular definida e seta como imagem do sprite

        self.rect = self.image.get_rect()

        self.center = pygame.math.Vector2(162/2, 191/2)

    def get_frame(self, frame_set): #este método simplesmente vai alterando o índice
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect): #recebe a lista de posiçoes ou somente a primeira posição
        self.sheet.set_clip(pygame.Rect(clipped_rect)) #define que o clip será um retangulo das posições definidas 
        return clipped_rect

    def update(self, direction):
        if direction == 'left':
            self.clip(states['left']) #chama o método clip passando a lista com as posições
            self.rect.x -= 1 # altera a posição em 5 pixels
        if direction == 'right':
            self.clip(states['right'])
            self.rect.x += 1
        if direction == 'up':
            self.clip(states['up'])
            self.rect.y -= 1
        if direction == 'down':
            self.clip(states['down'])
            self.rect.y += 1

        #aqui ele "para" virado para o lado que estava indo
        if direction == 'stand_left':
            self.clip(states['stand_left'])
        if direction == 'stand_right':
            self.clip(states['stand_right'])
        if direction == 'stand_up':
            self.clip(states['stand_up'])
        if direction == 'stand_down':
            self.clip(states['stand_down'])

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

