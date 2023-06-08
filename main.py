import os
import random
import pygame
import raft
import camera
import island
import garbage
import points
import inspect
#import cell

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()

Points = points.Points()

#grid = cell.Cell("cell")

WATER = (65,159,204)
WHITE_TEXT = (255,255,255)

raft = raft.Raft()
all_sprites = pygame.sprite.Group()
garbage_group = pygame.sprite.Group()
island_group = pygame.sprite.Group()
collide_group = pygame.sprite.Group()

gargabe_x = random.sample(range(-1000, 1000), 100)
gargabe_y = random.sample(range(-1000, 1000), 100)
for i in range(100):
    g = garbage.Garbage((gargabe_x[i], gargabe_y[i]))
    all_sprites.add(g)
    garbage_group.add(g)
    collide_group.add(g)

islands_x = random.sample(range(-1000, 1000), 3)
islands_y = random.sample(range(-1000, 1000), 3)
for i in range(3):
    isle = island.Island(f'islands/isle-{i+1}.webp', (islands_x[i], islands_y[i]))
    all_sprites.add(isle)
    island_group.add(isle)
    collide_group.add(isle)

all_sprites.add(raft)



pygame.init()

pygame.event.set_blocked(pygame.MOUSEMOTION)

info = pygame.display.Info()
screen_width,screen_height = info.current_w,info.current_h

screen = pygame.display.set_mode((screen_width,screen_height), pygame.FULLSCREEN)

camera = camera.Camera(screen_width, screen_height)
camera.update(raft, screen_width, screen_height)

ui = pygame.image.load('ui.png').convert()








def main():
    
    
    running = True

    #grid.build_grid(screen)
       

    pygame.display.update()

    while running:
        screen.fill(WATER)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("posição do mouse: "+str(event.pos))

        
        raft.handle_event(event)
        camera.update(raft, screen_width, screen_height)
        
        #screen.blit(island.image, (12, 24))
        for entity in all_sprites:
            screen.blit(entity.image, camera.apply(entity))
        
        
        #print(raft.rect.x)
        #print(raft.rect.y)
        #grid.handle_event(screen, event)
        
        collision_list = pygame.sprite.spritecollide(raft,collide_group,False)
        for item in collision_list:
            if isinstance(item, island.Island):
                item.item_drop_timer += 1
                if item.item_drop_timer >= 25:                    
                    Points.decrese_points(item.type)
                    item.item_drop_timer = 0
            elif isinstance(item, garbage.Garbage):
                item.grab_counter += 1
                if item.grab_counter >= 15:
                    item.kill()
                    Points.add_points(item.type)
        
        
        
        screen.blit(ui, (0,0)) 
        Points.print_points_on_screen(screen)    
        
        pygame.display.update()

        clock.tick(60)
        
    pygame.quit()

if __name__=="__main__":
    # call the main function
    main()
