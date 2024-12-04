import pygame
from src.home_screen import HomeScreen
from src.watchlist_screen import WatchlistScreen
from src.your_stocks_screen import YourStocksScreen
from src.game_screen import GameScreen

class Controller:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Stock Predictor")
        
        self.home_screen = HomeScreen(self.screen)
        self.watchlist_screen = WatchlistScreen(self.screen)
        self.your_stocks_screen = YourStocksScreen(self.screen)
        self.game_screen = GameScreen(self.screen)
        
        self.current_screen = self.home_screen

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill((0, 0, 0))  # Clear screen with black
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.current_screen.handle_events(event)

            self.current_screen.draw(mouse_pos)
            pygame.display.flip()

        pygame.quit()

    # Add this method to allow main.py to work
    def mainloop(self):
        self.run()  # Call the run method inside mainloop
