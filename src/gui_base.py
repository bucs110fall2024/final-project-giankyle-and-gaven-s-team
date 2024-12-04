import pygame

class GUIBase:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        
    def draw_button(self, name, rect, color, mouse_pos):
        button_color = color if rect.collidepoint(mouse_pos) else (100, 100, 255)
        pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
        text = self.font.render(name, True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def draw_centered_text(self, text, font, color, y_offset=0):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + y_offset))
        self.screen.blit(text_surface, text_rect)
