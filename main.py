import pygame
from src import Controller

def main():
    pygame.init()
    game = Controller.Controller()
    game.mainloop()
    
# https://codefather.tech/blog/if-name-main-python/
if __name__ == '__main__':
    main()