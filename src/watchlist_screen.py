import pygame
from src.gui_base import GUIBase

class WatchlistScreen(GUIBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.watchlist = [("AAPL", 30), ("TSLA", 60)]  # Example data
        self.home_button = pygame.Rect(20, 530, 150, 50)
        self.end_button = pygame.Rect(630, 530, 150, 50)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.home_button.collidepoint(event.pos):
                from home_screen import HomeScreen
                self.current_screen = HomeScreen(self.screen)
            elif self.end_button.collidepoint(event.pos):
                pygame.quit()

    def draw(self, mouse_pos):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.draw_centered_text("Watchlist", self.title_font, (255, 255, 255), -200)

        y_offset = 0
        for stock, days in self.watchlist:
            stock_button_rect = pygame.Rect(300, 250 + y_offset, 300, 50)
            self.draw_button(f"{stock} ({days} days)", stock_button_rect, (0, 0, 255), mouse_pos)
            y_offset += 100

        self.draw_button("Home", self.home_button, (0, 0, 255), mouse_pos)
        self.draw_button("End", self.end_button, (255, 0, 0), mouse_pos)
