import pygame
from src.gui_base import GUIBase

class GameScreen(GUIBase):
    def __init__(self, screen):
        super().__init__(screen)
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
        self.draw_centered_text("Game Screen", self.title_font, (255, 255, 255), -150)
        self.draw_button("Home", self.home_button, (0, 0, 255), mouse_pos)
        self.draw_button("End", self.end_button, (255, 0, 0), mouse_pos)
