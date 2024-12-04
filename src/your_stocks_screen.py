import pygame
from src.gui_base import GUIBase

class YourStocksScreen(GUIBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.user_input = ""
        self.response_message = ""
        self.home_button = pygame.Rect(20, 530, 150, 50)
        self.end_button = pygame.Rect(630, 530, 150, 50)
        self.clear_button = pygame.Rect(450, 250, 100, 50)
        self.forecast_days = None

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.forecast_days = self.user_input
                self.response_message = f"Forecasting for {self.forecast_days} days."
                self.user_input = ""
            else:
                self.user_input += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.home_button.collidepoint(event.pos):
                from home_screen import HomeScreen
                self.current_screen = HomeScreen(self.screen)
            elif self.end_button.collidepoint(event.pos):
                pygame.quit()
            elif self.clear_button.collidepoint(event.pos):
                self.user_input = ""

    def draw(self, mouse_pos):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.draw_centered_text("Enter Stock Ticker:", self.title_font, (255, 255, 255), -150)

        input_box = pygame.Rect(200, 250, 400, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), input_box)
        pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)
        text_surface = self.font.render(self.user_input, True, (0, 0, 0))
        self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        if self.response_message:
            self.draw_centered_text(self.response_message, self.font, (255, 255, 255), 100)

        self.draw_button("Clear", self.clear_button, (169, 169, 169), mouse_pos)
        self.draw_button("Home", self.home_button, (0, 0, 255), mouse_pos)
        self.draw_button("End", self.end_button, (255, 0, 0), mouse_pos)
