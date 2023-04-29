import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target, WIDTH, HEIGHT):
        x = -target.rect.x + int(WIDTH / 2) - target.center.x
        y = -target.rect.y + int(HEIGHT / 2) - target.center.y
        self.camera = pygame.Rect(x, y, self.width, self.height)