import pygame
import cell


grid = cell.Cell("cell")

def main():
    

    running = True

    height = 1080
    width = 1920
    screen = pygame.display.set_mode((width,height))


    grid.build_grid(screen)


    pygame.init()
    pygame.display.update()

    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
        grid.handle_event(screen, event)


        pygame.display.update()
        
            





if __name__=="__main__":
    # call the main function
    main()