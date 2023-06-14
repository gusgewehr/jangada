import pygame
import raft


class Points():
    raft = raft.Raft()

    def __init__(self):
        self.total_points = 0
        self.points_dict = {
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

    

    def animação_coleta(self, pos_inic, pos_fim, frame, tipo):
        print('nada')
        
        
    def add_points(self, type):
        type_points_dict  = self.points_dict[type] 
        type_points_dict["points"] +=1

    def decrese_points(self, type, sound):
        type_points_dict  = self.points_dict[type]        
        sound.set_volume(0.1)
        sound.play()
        type_points_dict["points"] -= 1
        self.total_points += 1
            
        
    def print_points_on_screen(self, screen, ratio_resize_width, ratio_resize_height):
        font = pygame.font.SysFont(None, int(32*ratio_resize_height))
        type_options = ("Eletrônico", "Plástico", "Metal", "Vidro", "Papel", "Orgânico")
        WHITE_TEXT = (255,255,255)
        for values in self.points_dict.values():
            img = font.render(str(values["points"]), True, WHITE_TEXT)
            screen.blit(img, (values["x"]*ratio_resize_width, values["y"]*ratio_resize_height))
        
        total_points = font.render(str(self.total_points), True, WHITE_TEXT)
        screen.blit(total_points, (826*ratio_resize_width, 61*ratio_resize_height))




        
    
