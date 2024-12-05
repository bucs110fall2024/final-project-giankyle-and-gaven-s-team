from src.gui_base import screen, draw_button, WHITE, BLUE
import pygame
import yfinance as yf
from src.stockprediction import stockpredictor

user_input = ""
ticker = None
forecast_days = None
current_question = "stock_ticker"

def draw_your_stocks_screen(mouse_pos, event):
    global user_input, ticker, forecast_days, current_question

    input_box = pygame.Rect(200, 250, 400, 50)
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)

    text_surface = pygame.font.Font(None, 36).render(user_input, True, (0, 0, 0))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            user_input = user_input[:-1]
        elif event.key == pygame.K_RETURN:
            if current_question == "stock_ticker":
                ticker = user_input.upper()
                current_question = "forecast_days"
                user_input = ""
            elif current_question == "forecast_days":
                forecast_days = int(user_input)
                predictor = stockpredictor(ticker)
                predictor.data_fetch()
                predictor.model_training()
                predictor.stock_prediction(forecast_days)
                user_input = ""
        else:
            user_input += event.unicode

    draw_button("Home", pygame.Rect(650, 500, 100, 50), BLUE, mouse_pos, screen)

    return "your_stocks"
