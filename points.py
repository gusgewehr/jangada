import pygame


class Points():
    def __init__(self):
        
        self.points_dict = {
            "Eletrônico": {
                "points": 0,
                "x": 40,
                "y": 20,
            },
            "Plástico": {
                "points": 0,
                "x": 170,
                "y": 20,
            },
            "Metal": {
                "points": 0,
                "x": 297,
                "y": 20,
            },
            "Vidro": {
                "points": 0,
                "x": 424,
                "y": 20,
            },
            "Papel": {
                "points": 0,
                "x": 553,
                "y": 20,
            },
            "Orgânico": {
                "points": 0,
                "x": 674,
                "y": 20,
            }
        }

        
    def add_points(self, type):
        type_points_dict  = self.points_dict[type]
        type_points_dict["points"] +=1

    def print_points_on_screen(self, screen,):
        font = pygame.font.SysFont(None, 32)
        type_options = ("Eletrônico", "Plástico", "Metal", "Vidro", "Papel", "Orgânico")
        WHITE_TEXT = (255,255,255)
        for values in self.points_dict.values():
        #for key in self.points_dict:
            #values = self.points_dict[key]    
            img = font.render(str(values["points"]), True, WHITE_TEXT)
            screen.blit(img, (values["x"], values["y"]))
            




        
    
