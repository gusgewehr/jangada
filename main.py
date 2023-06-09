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
BLACK_TEXT = (0,0,0)

raft_menu = raft.Raft()
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
    atualScreen = 'menu'

    #grid.build_grid(screen)
    

    pygame.display.update()

    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("posição do mouse: "+str(event.pos))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if atualScreen == 'menu':
                    atualScreen = 'guide'
                elif atualScreen == 'guide':
                    atualScreen = 'game'

        if atualScreen == 'menu':
            menu()
            raft_menu.update('stand_right')
        elif atualScreen == 'guide':
            guide()
        else:
            screen.fill(WATER)
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

def menu():
    screen.fill(WATER)
    menu_reft = raft_menu.image.get_rect()
    menu_reft.midtop = (screen_width/2, 300)
    screen.blit(raft_menu.image, menu_reft)
    draw_text("JANGADA", 95, screen_width/2, 100, BLACK_TEXT)
    draw_text("POLUIÇÃO NAS ÁGUAS", 15, screen_width/2, 200, BLACK_TEXT)
    draw_text("PRESSIONE [ENTER] PARA INICIAR", 30, screen_width/2, screen_height/1.5, BLACK_TEXT)
    draw_text("PRESSIONE [ESC] PARA SAIR", 25, screen_width/2, (screen_height/1.5) + 50, BLACK_TEXT)
    draw_text("Eduardo Hüther, Gustavo Gewehr", 12, screen_width/2, screen_height - 50, BLACK_TEXT)

def guide():
    screen.fill(WATER)
    draw_text("INSTRUÇÕES", 30, screen_width/2, 100, BLACK_TEXT)
    draw_text("- COLETE OS LIXOS NO MAR COM A SUA JANGADA!", 20, screen_width/2, 150, BLACK_TEXT)
    draw_text("- LEVE OS LIXOS QUE COLETOU PARA AS ILHAS E GANHE PONTOS!", 20, screen_width/2, 180, BLACK_TEXT)
    draw_text("- AO LONGO DO TEMPO A JANGADA IRÁ PERDER VIDA, COLETE LIXOS PARA RECUPERAR VIDA!", 20, screen_width/2, 210, BLACK_TEXT)
    draw_text("- SE A VIDA CHEGAR EM 0 (ZERO) O JOGO ACABA!", 20, screen_width/2, 240, BLACK_TEXT)
    draw_text("UTILIZE AS SETINHAS DO TECLADO PARA MOVER A JANGADA", 30, screen_width/2, 280, BLACK_TEXT)
    arrow_keys = pygame.image.load('arrowkeys.png').convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys, (150, 85))
    keys = arrow_keys.get_rect()
    keys.midtop = (screen_width/2, 350)
    screen.blit(arrow_keys, keys)
    draw_text("PRESSIONE [ENTER] PARA INICIAR O JOGO", 30, screen_width/2, screen_height/1.5, BLACK_TEXT)


def draw_text(text, size, x, y, color):
    '''draw text to screen'''
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

if __name__=="__main__":
    # call the main function
    main()
