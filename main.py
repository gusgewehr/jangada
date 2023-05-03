import os
import random
import pygame
import raft
import camera
import island
import garbage
#import cell

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()

#grid = cell.Cell("cell")

WATER = (65,159,204)

raft = raft.Raft()
all_sprites = pygame.sprite.Group()

gargabe_x = random.sample(range(-10000, 10000), 3000)
gargabe_y = random.sample(range(-10000, 10000), 3000)
for i in range(3000):
    g = garbage.Garbage((gargabe_x[i], gargabe_y[i]))
    all_sprites.add(g)

islands_x = random.sample(range(-10000, 10000), 25)
islands_y = random.sample(range(-10000, 10000), 25)
for i in range(25):
    isle = island.Island(f'islands/isle-{i+1}.webp', (islands_x[i], islands_y[i]))
    all_sprites.add(isle)

all_sprites.add(raft)

pygame.init()

pygame.event.set_blocked(pygame.MOUSEMOTION)

info = pygame.display.Info()
screen_width,screen_height = info.current_w,info.current_h

screen = pygame.display.set_mode((screen_width,screen_height), pygame.FULLSCREEN)

camera = camera.Camera(screen_width, screen_height)
camera.update(raft, screen_width, screen_height)

def main():
    
    running = True

    #grid.build_grid(screen)

    pygame.display.update()

    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # change the value to False, to exit the main loop
                running = False
        
        raft.handle_event(event)
        camera.update(raft, screen_width, screen_height)
        screen.fill(WATER)
        #screen.blit(island.image, (12, 24))
        for entity in all_sprites:
            screen.blit(entity.image, camera.apply(entity))
        
        #print(raft.rect.x)
        #print(raft.rect.y)
        #grid.handle_event(screen, event)

        pygame.display.update()

        clock.tick(60)
        
    pygame.quit()

if __name__=="__main__":
    # call the main function
    main()
