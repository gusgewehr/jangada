import pygame



def main():
    pygame.init()

    running = True

    height = 1080
    width = 1920
    screen = pygame.display.set_mode((width,height))

    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
            





if __name__=="__main__":
    # call the main function
    main()