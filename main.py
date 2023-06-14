import os
import random
import pygame
import raft
import camera
import island
import garbage
import points
import inspect
import animate_garbage_collection

os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
current_user = os.getlogin()

Points = points.Points()


WATER = (65,159,204)
WHITE_TEXT = (255,255,255)
BLACK_TEXT = (0,0,0)
GREEN = (0,128,0)


islands = [
    {"type": "Eletrônico", "pos": [-1750, -1610]},
    {"type": "Plástico", "pos": [-1465, -1080]},
    {"type": "Metal", "pos": [-810, -15]},
    {"type": "Vidro", "pos": [1545, 915]},
    {"type": "Papel", "pos": [300, -300]},
    {"type": "Orgânico", "pos": [965, 1240]}
    ]

raft_menu = raft.Raft()
raft = raft.Raft()
all_sprites = pygame.sprite.Group()
garbage_group = pygame.sprite.Group()
island_group = pygame.sprite.Group()
collide_group = pygame.sprite.Group()

gargabe_x = random.sample(range(-3000, 3000), 400)
gargabe_y = random.sample(range(-3000, 3000), 400)
for i in range(400):
    g = garbage.Garbage((gargabe_x[i], gargabe_y[i]))
    all_sprites.add(g)
    garbage_group.add(g)
    collide_group.add(g)

for i in range(len(islands)):
    isle = island.Island((islands[i]["pos"][0], islands[i]["pos"][1]), islands[i]["type"])
    all_sprites.add(isle)
    island_group.add(isle)
    collide_group.add(isle)


all_sprites.add(raft)

pygame.mixer.pre_init(44100, -16, 2, 2048)


pygame.init()



pygame.mixer.init()

pygame.mixer.music.load('sounds/menu.mp3')

pygame.event.set_blocked(pygame.MOUSEMOTION)

info = pygame.display.Info()
screen_width,screen_height = info.current_w,info.current_h

screen = pygame.display.set_mode((screen_width,screen_height), pygame.FULLSCREEN)

# screen_width = 1920
# screen_height = 1080

# screen = pygame.display.set_mode((screen_width, screen_height))

camera = camera.Camera(screen_width, screen_height)
camera.update(raft, screen_width, screen_height)

ui = pygame.image.load('ui2.png')
ratio_resize_width = screen_width/ui.get_width()
ratio_resize_height = screen_height/1080
ui = pygame.transform.scale(ui, (ui.get_width()*ratio_resize_width, ui.get_height()*ratio_resize_height))

item_sound = pygame.mixer.Sound('sounds/item.mp3')
deliver_sound = pygame.mixer.Sound('sounds/deliver.mp3')

def main():
    
    running = True
    atualScreen = 'menu'   

    pygame.display.update()
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    text = ''
    cur_animation = None

    

    while running:
        raft_last_position = (raft.rect.x, raft.rect.y)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("posição do mouse: "+str(event.pos))
            elif atualScreen == 'endgame':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if text != '':
                            with open(f'C:/Users/{current_user}/documents/ranking.txt', 'a') as f:
                                f.write(f"{text}-{Points.total_points} \n")
                            text = ''
                            Points.total_points = 0
                    elif event.key == pygame.K_SPACE:
                        
                        reset()
                        text = ''
                        atualScreen = 'menu'
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode          
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if atualScreen == 'menu':
                    atualScreen = 'guide'
                elif atualScreen == 'guide':
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('sounds/ocean.mp3')
                    pygame.mixer.music.set_volume(0.05)
                    pygame.mixer.music.play(-1)
                    atualScreen = 'game'



        if atualScreen == 'menu':
            menu()
            raft_menu.update('stand_right')
        elif atualScreen == 'guide':
            guide()
        elif atualScreen == 'endgame':
            endgame(text)
        else:
            screen.fill(WATER)
            raft.handle_event(event)
            camera.update(raft, screen_width, screen_height)
        
            for entity in all_sprites:

                screen.blit(entity.image, camera.apply(entity))
        
        
            for ilha in island_group:
                gets_hit = pygame.sprite.spritecollide(ilha, garbage_group, False)
                for item in gets_hit:
                    if isinstance(item, garbage.Garbage):
                        item.kill()
            
                
                    
            collision_list = pygame.sprite.spritecollide(raft,collide_group,False)
            
            is_colliding = False
            for item in collision_list:
                if isinstance(item, island.Island):
                    raft_center = [(raft.rect.x+(raft.rect.width/2)), (raft.rect.y+(raft.rect.height/2))]
                    island_center = [(item.rect.x+(item.rect.width/2)), (item.rect.y+(item.rect.height/2))]
                    tipo_ilha = item.type
                    type_points_dict  = Points.points_dict[tipo_ilha]
                    if type_points_dict["points"] >  0:
                        if item.item_drop_timer == 0:
                            cur_animation = animate_garbage_collection.AnimateGarbageColletion(raft_center,island_center, 25, tipo_ilha)
                            all_sprites.add(cur_animation)
                        else:
                            cur_animation.update_frame(item.item_drop_timer)
                        item.item_drop_timer += 1
                        if item.item_drop_timer >= 25:                                                
                            Points.decrese_points(item.type, deliver_sound)
                            item.item_drop_timer = 0
                            cur_animation.kill()
                    raft.rect.x = raft_last_position[0]
                    raft.rect.y = raft_last_position[1]
                    is_colliding = True
                elif isinstance(item, garbage.Garbage):
                    item_sound.set_volume(0.1)
                    item.grab_counter += 1
                    if item.grab_counter >= 15:
                        item_sound.play()
                        item.kill()
                        Points.add_points(item.type)
                        raft.life += 50
            if is_colliding == False and cur_animation in all_sprites:
                cur_animation.kill()
            screen.blit(ui, (0,0)) 
            Points.print_points_on_screen(screen, ratio_resize_width, ratio_resize_height)
            
            total_life_width = 600*ratio_resize_width
            life_rect_width = ((raft.life/1500)*total_life_width)

            pygame.draw.rect(screen, BLACK_TEXT, pygame.Rect(1281*ratio_resize_width, 24*ratio_resize_height, total_life_width, 35*ratio_resize_height), 0)
            pygame.draw.rect(screen, GREEN, pygame.Rect(1281*ratio_resize_width, 24*ratio_resize_height, life_rect_width, 35*ratio_resize_height), 0)
            
            if not is_colliding:
                raft.life -= 1

            if raft.life <= 0:
                atualScreen = 'endgame'

        
        pygame.display.update()

        garbage_spawn()

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
    draw_text("- LEVE OS LIXOS QUE COLETOU PARA AS ILHAS COM A COR DE DESCARTE CORRETA E GANHE PONTOS!", 20, screen_width/2, 180, BLACK_TEXT)
    draw_text("- AO LONGO DO TEMPO A JANGADA IRÁ PERDER VIDA, COLETE LIXOS PARA RECUPERAR VIDA!", 20, screen_width/2, 210, BLACK_TEXT)
    draw_text("- SE A VIDA CHEGAR EM 0 (ZERO) O JOGO ACABA!", 20, screen_width/2, 240, BLACK_TEXT)
    draw_text("UTILIZE AS SETINHAS DO TECLADO PARA MOVER A JANGADA", 30, screen_width/2, 280, BLACK_TEXT)
    draw_text("SEGURE A SETINHA DO TECLADO EM DIREÇÃO A ILHA PARA DESCARTAR O LIXO E GANHAR PONTOS", 30, screen_width/2, 320, BLACK_TEXT)
    draw_text("EXEMPLO - LEVE O PLASTICO PARA A ILHA DE COR VERMELHA", 20, screen_width/2, 470, BLACK_TEXT)
    arrow_keys = pygame.image.load('arrowkeys.png').convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys, (150, 85))
    keys = arrow_keys.get_rect()
    keys.midtop = (screen_width/2, 370)
    screen.blit(arrow_keys, keys)
    arrow_keys = pygame.image.load('example.png').convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys, (412, 163))
    keys = arrow_keys.get_rect()
    keys.midtop = (screen_width/2, 500)
    screen.blit(arrow_keys, keys)

    draw_text("PRESSIONE [ENTER] PARA INICIAR O JOGO", 30, screen_width/2, screen_height/1.5, BLACK_TEXT)

def endgame(text):
    ranking = []
    screen.fill(WATER)
    draw_text("FIM DE JOGO!", 72, screen_width/2, 50, BLACK_TEXT)
    draw_text("Sua pontuação: {}".format(Points.total_points), 52, screen_width/2, 250, BLACK_TEXT)
    draw_text("Digite seu nome e pressione [ENTER] para salvar sua pontuação", 30, screen_width/2, 800, BLACK_TEXT)
    draw_text("Pressione [ESPAÇO] para reiniciar o jogo", 30, screen_width/2, 900, BLACK_TEXT)


    font = pygame.font.Font(pygame.font.match_font('arial'), 52)  
    txt_surface = font.render('Jogador: '+text, True, BLACK_TEXT)
    # Resize the box if the text is too long.
    text_rect = txt_surface.get_rect()
    # Blit the text.    
    text_rect.midtop = (screen_width/2, 150)
    screen.blit(txt_surface, text_rect)
    # Blit the input_box rect.
    
    try:
        with open(f'C:/Users/{current_user}/documents/ranking.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line_content = line.split('-')
                dict = {
                    'player': line_content[0],
                    'points': line_content[1].strip()
                }
                ranking.append(dict)
    except:
        ranking = []

    if len(ranking) > 0:
        ranking.sort(reverse=True,key=lambda d: int(d['points']))
        pos_y = 335
        for i, item in enumerate(ranking):
            draw_text(f"{i+1}º {item['player']} - {item['points']}", 24, screen_width/2, pos_y, BLACK_TEXT)
            pos_y += 50
            if i == 5:
                break
    pygame.display.flip()


    
def reset():
    points.total_points = 0
    points.points_dict = {
            "Eletrônico": {
                "points": 0,
                "x": 44,
                "y": 32,
            },
            "Plástico": {
                "points": 0,
                "x": 170,
                "y": 32,
            },
            "Metal": {
                "points": 0,
                "x": 297,
                "y": 32,
            },
            "Vidro": {
                "points": 0,
                "x": 424,
                "y": 32,
            },
            "Papel": {
                "points": 0,
                "x": 553,
                "y": 32,
            },
            "Orgânico": {
                "points": 0,
                "x": 674,
                "y": 32,
            }
        }
    raft.life = 1500






def draw_text(text, size, x, y, color):
    '''draw text to screen'''
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def garbage_spawn():
    if len(garbage_group) < 400:
        gargabe_x = random.randint(-3000, 3000)
        gargabe_y = random.randint(-3000, 3000)
        g = garbage.Garbage((gargabe_x, gargabe_y))
        all_sprites.add(g)
        garbage_group.add(g)
        collide_group.add(g)

if __name__=="__main__":
    # call the main function
    main()
